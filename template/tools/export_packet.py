#!/usr/bin/env python3
"""
export_packet.py — assemble a self-contained, blinded packet for a cross-family
(non-Claude, e.g. ChatGPT) audit.

This is the RARE, ON-DEMAND check described in 01-spec/stopping-rules.md. It is
scarce by design. Do not spend it on "read my paper and tell me what you think."
Spend it on one of three deliberate jobs:

  --mode draft     Audit the current rendered draft against the FROZEN rubric, in
                   the SAME blind, offline configuration as the internal panel.
                   Purpose: calibrate the internal reviewers, not fix the draft.
                   EXCLUDES (load-bearing): claims table, revision history, prior
                   scores, adjudicator notes, issue log. The external model must
                   see exactly what an internal blind reviewer sees: draft +
                   rubric + style-anchor. Nothing else.

  --source KEY     Assess one citable source's fitness for the claims that cite
                   it. Ships the corpus record, the cached source text (if on
                   disk), and every claim (with span) that cites KEY. Purpose:
                   an independent read on whether the span supports the claim and
                   whether the strength grade is honest.

  --process        Audit the machinery itself: the spec files, the enforcer
                   source, the taxonomy, the stopping rules. Purpose: a critique
                   of the reward function and the loop design. Ships specs +
                   enforce.py + the iteration log, NOT the draft.

Output: a single Markdown file in 04-log/exports/ that can be pasted whole into an
external model, plus a companion "instructions" header telling the external model
how to respond so its output is comparable to the internal panel.

Also opens an ESC entry stub text on stdout for the adjudicator to paste into
04-log/escalation-queue.md.

Usage:
    python3 tools/export_packet.py --mode draft
    python3 tools/export_packet.py --mode source --source nguyen2019
    python3 tools/export_packet.py --mode process
"""

import os, sys, re, argparse, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def p(*a): return os.path.join(ROOT, *a)
def read(fp):
    try:
        with open(fp, encoding="utf-8") as f: return f.read()
    except FileNotFoundError:
        return f"[missing: {os.path.relpath(fp, ROOT)}]"
def now(): return datetime.datetime.now().replace(microsecond=0).isoformat()

EXPORTS = p("04-log", "exports")

RUBRIC = p("01-spec", "rubric.md")
STYLE  = p("01-spec", "style-anchor.md")
DRAFT  = p("03-state", "draft.md")
CLAIMS = p("03-state", "claims.md")
CORPUS = p("03-state", "corpus.md")

# ---------------------------------------------------------------- blinding
def latest_draft_version():
    vd = p("03-state", "versions")
    if not os.path.isdir(vd): return None
    vs = sorted(f for f in os.listdir(vd) if re.match(r"draft-v\d+\.md$", f))
    return os.path.join("03-state", "versions", vs[-1]) if vs else None

DRAFT_INSTRUCTIONS = """\
# CROSS-FAMILY AUDIT PACKET — DRAFT REVIEW (blind, offline)

You are an independent reviewer from a different model family. You are being used
to CALIBRATE a panel of reviewers, not to rewrite this paper. Follow these rules
exactly, or the comparison is meaningless:

1. You receive ONLY: the draft, the frozen rubric, and the style anchor. You do
   NOT receive revision history, prior scores, other reviewers' output, the claim
   table, or any statement of what changed. If you think you can infer those, do
   not; score only what is in front of you.
2. Score R-01 through R-08 strictly on the rubric's behavioral anchors. Do not
   average toward the middle. Match the anchor.
3. Every score MUST carry a located instance — the specific sentence that drove
   it. A score with no located instance is void; write "VOID" instead of a guess.
4. Do NOT suggest fixes. Describe what is wrong and where. You are not the reviser.
5. End with the rubric's `reviewer meta` block: items you could not apply, and
   items where the rubric did not fit the draft. That block is the most valuable
   thing you produce — it audits the rubric, not the paper.

Return your review in the rubric's exact reporting format.
--------------------------------------------------------------------------------
"""

SOURCE_INSTRUCTIONS = """\
# CROSS-FAMILY AUDIT PACKET — SOURCE / CITATION ASSESSMENT

You are an independent reviewer assessing whether a single cited source actually
supports the claims that cite it. You are NOT reviewing the paper.

For each claim below, answer three questions, tersely:
1. Does the quoted span appear to support the claim's text as written? (yes / no /
   partial — and if partial, what inferential step is missing.)
2. Is the assigned strength grade honest? (Strong = span entails claim, no leap;
   Suggestive = indirect/analogical/single-source/contested; Asserted = no
   support.) If you would grade it lower, say so and why.
3. Is the tag correct? (empirical / causal — needs a mechanism / comparative —
   needs a named baseline AND a named metric.)

Do not fix anything. Report per claim. Flag any claim where the span looks
stretched, the grade looks inflated, or a causal/comparative obligation is unmet.
--------------------------------------------------------------------------------
"""

PROCESS_INSTRUCTIONS = """\
# CROSS-FAMILY AUDIT PACKET — PROCESS / REWARD-FUNCTION AUDIT

You are auditing the DESIGN of a self-improving writing loop, not any draft it
produced. The central risk this system fights is reward hacking: the reviewers
and the author share a model and can jointly please the rubric while the paper
gets worse. Read the spec files and the enforcer source below and answer:

1. Where can an agent satisfy a check mechanically while defeating its intent?
   Name the check and the exploit.
2. Which judgmental rubric items (R-nn) could be converted to mechanical enforcer
   checks (E-nn)? Every such conversion is a permanent improvement.
3. Where is the enforcer's implementation likely to diverge from the spec's
   stated intent (false positives that would wrongly HALT, or false negatives
   that would let a real failure through)?
4. Is anything in the stopping rules gameable — a way to hit a stop condition
   that looks like success but is not?

Be concrete and cite file/section. Do not propose prose edits to any paper.
--------------------------------------------------------------------------------
"""

def claims_citing(key):
    txt = read(CLAIMS)
    blocks = re.split(r"(?=^###\s)", txt, flags=re.MULTILINE)
    hits = []
    for b in blocks:
        if re.search(r"cite:\s*.*\b" + re.escape(key) + r"\b", b) or \
           re.search(r"\[cite:\s*[^\]]*\b" + re.escape(key) + r"\b", b):
            hits.append(b.strip())
    return hits

def corpus_record(key):
    for line in read(CORPUS).splitlines():
        if line.strip().startswith("|") and line.strip().strip("|").split("|")[0].strip() == key:
            return line.strip()
    return f"[key '{key}' not found in corpus]"

def corpus_path(key):
    for line in read(CORPUS).splitlines():
        if line.strip().startswith("|"):
            cols = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cols) >= 6 and cols[0] == key:
                return cols[4]
    return None

def build_draft(out, version=None):
    # The CURRENT draft by default. A saved version is reviewed only when named:
    # preferring the latest snapshot silently reviewed text older than draft.md.
    if version:
        dv = os.path.join("03-state", "versions", f"draft-{version}.md")
        if not os.path.isfile(p(dv)):
            sys.exit(f"--version {version}: {dv} does not exist")
    else:
        dv = "03-state/draft.md"
    raw = read(p(dv))
    # Strip ALL HTML comments — including binding comments <!-- claims: ... -->.
    # Binding comments embed claim IDs; a blind reviewer must not see the claim
    # graph (see CLAUDE.md rule 6, rubric instructions). The reviewer scores the
    # rendered prose, exactly as a reader would see it.
    blinded = re.sub(r"<!--.*?-->", "", raw, flags=re.DOTALL).strip()
    leaks = re.findall(r"\b(?:GAP|REM|ASK|SUP|DEF)-\d", blinded)
    parts = [DRAFT_INSTRUCTIONS,
             "## DRAFT UNDER REVIEW (rendered prose only; binding comments stripped)\n",
             blinded,
             "\n\n## FROZEN RUBRIC\n", read(RUBRIC),
             "\n\n## STYLE ANCHOR\n", read(STYLE)]
    out.write("\n".join(parts))
    if leaks:
        out.write(f"\n\n<!-- WARN: {len(leaks)} claim-id-like tokens remain in visible prose; "
                  f"a drafter should not put claim IDs in prose. Review before external send. -->\n")
    return dv, leaks

def build_source(out, key):
    out.write(SOURCE_INSTRUCTIONS)
    out.write(f"\n## CORPUS RECORD for `{key}`\n\n{corpus_record(key)}\n")
    cp = corpus_path(key)
    if cp and cp != "—":
        srctxt = read(p("03-state", cp))
        out.write(f"\n## CACHED SOURCE TEXT (`{cp}`)\n\n")
        out.write("```\n" + srctxt[:60000] + ("\n...[truncated]..." if len(srctxt) > 60000 else "") + "\n```\n")
    else:
        out.write("\n## CACHED SOURCE TEXT\n\n[not on disk — span-unverifiable; grade caps at Suggestive]\n")
    hits = claims_citing(key)
    out.write(f"\n## CLAIMS CITING `{key}` ({len(hits)})\n\n")
    for h in hits:
        out.write("```\n" + h + "\n```\n\n")
    if not hits:
        out.write("[no claims currently cite this key]\n")

def build_process(out):
    out.write(PROCESS_INSTRUCTIONS)
    for label, fp in [("CLAUDE.md (operating contract)", p("CLAUDE.md")),
                      ("claim-schema.md", p("01-spec","claim-schema.md")),
                      ("failure-taxonomy.md", p("01-spec","failure-taxonomy.md")),
                      ("rubric.md", RUBRIC),
                      ("enforcer-spec.md", p("01-spec","enforcer-spec.md")),
                      ("stopping-rules.md", p("01-spec","stopping-rules.md")),
                      ("enforce.py (enforcer source)", p("tools","enforce.py")),
                      ("iterations.md (loop history)", p("04-log","iterations.md"))]:
        out.write(f"\n\n## {label}\n\n```\n{read(fp)}\n```\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["draft","source","process"], required=True)
    ap.add_argument("--source", help="corpus key, required for --mode source")
    ap.add_argument("--version", help="with --mode draft: review saved draft-<version>.md (e.g. v007) instead of the current draft")
    args = ap.parse_args()
    os.makedirs(EXPORTS, exist_ok=True)
    ts = datetime.date.today().isoformat()
    if args.mode == "source" and not args.source:
        ap.error("--mode source requires --source KEY")
    name = f"{ts}-{args.mode}{('-'+args.source) if args.source else ''}.md"
    fp = os.path.join(EXPORTS, name)
    with open(fp, "w", encoding="utf-8") as out:
        leaks = []
        if args.mode == "draft":   dv, leaks = build_draft(out, args.version)
        elif args.mode == "source": build_source(out, args.source); dv = "n/a"
        else:                       build_process(out); dv = "n/a"

    rel = os.path.relpath(fp, ROOT)
    print(f"packet written -> {rel}")
    if args.mode == "draft" and leaks:
        print(f"WARNING: {len(leaks)} claim-id-like tokens remain in visible prose — review before sending.")
    print()
    print("Paste this ESC stub into 04-log/escalation-queue.md:\n")
    print(f"""## ESC-XXX — {now()}
- kind: CROSS-FAMILY-AUDIT ({args.mode})
- trigger: <which stopping-rules trigger, or 'human requested'>
- ask: <the specific question the external model must answer>
- packet: {rel}
- config: blind, offline — external model runs in the SAME configuration as the
  internal panel. For --mode draft, claims/history/scores are NOT in the packet.
- status: open
- resolution: <paste external output to 04-log/reviews/rNNN-external.md; record
  agreement / one-off / patterned divergence in 04-log/rubric-amendments.md>""")

if __name__ == "__main__":
    main()
