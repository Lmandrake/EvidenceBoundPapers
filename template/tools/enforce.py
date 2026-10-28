#!/usr/bin/env python3
"""
enforce.py — the deterministic gate for the evidence-bound paper loop.

FROZEN LOGIC. Generated once from 01-spec/enforcer-spec.md (v1.0) plus one call's
E-16 population (the only venue-specific check). After review, no agent edits the
check logic. A wrong check is a spec-amendment request in
04-log/rubric-amendments.md, applied by a human.

Hard constraints (see 01-spec/enforcer-spec.md):
  - This is a script, not an agent. It calls no LLM. It does not reason.
  - Its verdict is not advisory. A HALT stops the loop.
  - It parses markdown state only: claims.md blocks, draft.md binding comments,
    corpus.md table + config. No database.

Checks implemented: E-01 .. E-21 (21 total; E-16.4, .6, .7 are left to review). Severities: HALT | BLOCK | WARN.
Tri-state status per check: pass | fail | na (not-yet-applicable).

Usage:
    python3 tools/enforce.py            # run, write report, update iteration line
    python3 tools/enforce.py --quiet    # same, minimal stdout
    python3 tools/enforce.py --root DIR # check the instance at DIR instead

Paths are resolved relative to the instance root: the parent of tools/, or --root.
"""

import os, re, sys, json, datetime, difflib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def p(*parts): return os.path.join(ROOT, *parts)

def set_root(root):
    """Point every state path at another instance root (--root)."""
    global ROOT, CLAIMS, DRAFT, CORPUS, PROTECT, STRUCT, DECIS, ISSUES, REPORT, ITER, VERSIONS, STATEF
    ROOT = os.path.abspath(root)
    CLAIMS, DRAFT, CORPUS = p("03-state", "claims.md"), p("03-state", "draft.md"), p("03-state", "corpus.md")
    PROTECT, STRUCT = p("03-state", "protected.md"), p("03-state", "structure.md")
    DECIS, ISSUES, REPORT = p("04-log", "decisions.md"), p("04-log", "issues.md"), p("04-log", "enforcer-report.md")
    ITER, VERSIONS, STATEF = p("04-log", "iterations.md"), p("03-state", "versions"), p("04-log", ".enforcer-state.json")

def resolve_corpus_path(rel):
    """corpus.md lives in 03-state/ and its 'local path' column is written
    relative to that directory (e.g. 'corpus-text/foo.txt'). Anchor there.
    Absolute paths are honored as-is."""
    if not rel or rel == "—":
        return ""
    if os.path.isabs(rel):
        return rel
    return os.path.join(ROOT, "03-state", rel)

CLAIMS   = p("03-state", "claims.md")
DRAFT    = p("03-state", "draft.md")
CORPUS   = p("03-state", "corpus.md")
PROTECT  = p("03-state", "protected.md")
STRUCT   = p("03-state", "structure.md")
DECIS    = p("04-log", "decisions.md")
ISSUES   = p("04-log", "issues.md")
REPORT   = p("04-log", "enforcer-report.md")
ITER     = p("04-log", "iterations.md")
VERSIONS = p("03-state", "versions")
STATEF   = p("04-log", ".enforcer-state.json")

# ----------------------------------------------------------------------------
# wordlists (deterministic; documented in enforcer-spec.md / claim-schema.md)
# ----------------------------------------------------------------------------
INCIDENCE_CATEGORIES = {
    "decision-makers","decision makers","stakeholders","the community","community",
    "end users","end-users","managers","planners","practitioners","operators","users",
    "scientists","researchers","the field","modelers","developers","analysts",
}
COMPARATIVE_TRIGGERS = [  # E-03: illegal without named baseline+metric
    "outperforms","better than","state of the art","state-of-the-art","superior","leading",
]
# E-06 FRAMING prohibited comparatives/superlatives (explicit list, not suffix heuristics)
COMPARATIVE_WORDS = [
    "better","best","worse","worst","more","most","fewer","fewest","few","less","least",
    "greater","greatest","larger","largest","smaller","smallest","higher","highest",
    "lower","lowest","faster","fastest","slower","slowest","leading","superior","inferior",
    "outperforms","unprecedented","largely","majority","dominant","optimal","superior",
]
OBS_DESIGN_MARKERS = ["observed","associated","correlat","linked to","correlation"]
# E-06 FRAMING: mission/instrument/system proper nouns are subject matter but still
# forbidden in FRAMING paragraphs, and the digits inside them ("Probe-2") are
# identifiers, not statistics. Institutions/programs live in the advocacy list.
# Domain-specific, so they are read from corpus.md `identifier-tokens:` (see
# parse_corpus); this module-level list is filled per run.
MISSION_TOKENS = []
METRIC_HINTS = [  # E-03 metric presence heuristic
    "crps","rmse","brier","log score","log-score","coverage","calibration","reliability",
    "resolution","sharpness","bias","skill","accuracy","precision","psu","ppm","score",
    "anomaly correlation","rank histogram","pit","error","%","percent","sigma","psu",
]
BASELINE_CONNECTIVES = ["than","versus","vs.","vs ","relative to","compared to","compared with","over the","against"]

# ----------------------------------------------------------------------------
# small helpers
# ----------------------------------------------------------------------------
def read(fp):
    try:
        with open(fp, encoding="utf-8") as f: return f.read()
    except FileNotFoundError:
        return ""

def strip_html_comments(s):
    return re.sub(r"<!--.*?-->", "", s, flags=re.DOTALL)

def norm_ws(s):
    return re.sub(r"\s+", " ", s).strip()

def now_iso():
    return datetime.datetime.now().replace(microsecond=0).isoformat()

# ----------------------------------------------------------------------------
# parsers
# ----------------------------------------------------------------------------
LIST_KEYS = {"nearest-miss", "competing", "alternatives"}

def parse_claims(text):
    """Return list of dicts. Template blocks inside HTML comments are stripped."""
    text = strip_html_comments(text)
    nodes = []
    cur = None
    cur_list_key = None
    for raw in text.splitlines():
        line = raw.rstrip("\n")
        m = re.match(r"^###\s+([A-Za-z]+-\S+)\s*$", line)
        if m:
            if cur: nodes.append(cur)
            cur = {"id": m.group(1).strip(), "_lists": {}, "_order": []}
            cur_list_key = None
            continue
        if cur is None:
            continue
        # top-level "- key: value"
        mk = re.match(r"^-\s+([a-zA-Z][\w-]*):\s?(.*)$", line)
        if mk:
            key = mk.group(1).strip().lower()
            val = mk.group(2).strip()
            cur[key] = val
            cur["_order"].append(key)
            if key in LIST_KEYS:
                cur["_lists"][key] = []
                cur_list_key = key
            else:
                cur_list_key = None
            continue
        # indented list item "  - ..."
        mi = re.match(r"^\s+-\s+(.*)$", line)
        if mi and cur_list_key:
            cur["_lists"][cur_list_key].append(mi.group(1).strip())
            continue
        # blank or other -> ends a list context but keeps node
        if line.strip() == "":
            cur_list_key = None
    if cur: nodes.append(cur)
    return nodes

def parse_corpus(text):
    """Return (keys:dict[key->{year,span_verifiable,path}], config:dict)."""
    keys = {}
    cfg = {"recency_window_years": 5, "advocacy": []}
    # config block
    mrec = re.search(r"recency-window-years:\s*(\d+)", text)
    if mrec: cfg["recency_window_years"] = int(mrec.group(1))
    madv = re.search(r"advocacy-wordlist:\s*(.+)", text)
    if madv:
        cfg["advocacy"] = [t.strip() for t in re.split(r"[,\n]", madv.group(1)) if t.strip()
                           and not t.strip().startswith("#")]
    # identifier-tokens: same line only, inline '#' comment dropped. Longest first,
    # so "Probe-2" is stripped before "Probe".
    mid = re.search(r"identifier-tokens:[ \t]*([^\n]*)", text)
    toks = [t.strip() for t in mid.group(1).split("#", 1)[0].split(",")] if mid else []
    cfg["identifier_tokens"] = sorted({t for t in toks if t}, key=lambda t: (-len(t), t))
    # recency base year (from note); default to current year
    mbase = re.search(r"base(?:\s+year)?\s*(\d{4})", text)
    cfg["recency_base"] = int(mbase.group(1)) if mbase else datetime.date.today().year
    # entries table rows: | key | authors | year | venue | path | span-verifiable |
    for line in text.splitlines():
        if not line.strip().startswith("|"): continue
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) < 6: continue
        key = cols[0]
        if key in ("key", "---", "") or set(key) <= {"-"}: continue
        if re.match(r"^-+$", key): continue
        yr = re.search(r"(\d{4})", cols[2])
        sv = cols[5].lower().startswith("y")
        keys[key] = {"year": int(yr.group(1)) if yr else None,
                     "span_verifiable": sv, "path": cols[4]}
    return keys, cfg

BINDING_RE = re.compile(r"^\s*<!--\s*claims:\s*(.*?)\s*-->\s*$")
SENTINEL = "Nothing to render"

def _strip_nonbinding_comments(draft_text):
    """Remove HTML comment blocks (possibly multi-line) EXCEPT single-line binding
    comments `<!-- claims: ... -->`, which are structural delimiters. Handles the
    template's nested example bindings inside the outer doc comment correctly by
    tracking multi-line comment state rather than regex-matching across nesting."""
    out = []
    in_comment = False
    for line in draft_text.splitlines():
        if in_comment:
            if "-->" in line:
                in_comment = False
                # keep any tail after the closing marker
                tail = line.split("-->", 1)[1]
                if tail.strip():
                    out.append(tail)
            continue
        if BINDING_RE.match(line):
            out.append(line)  # preserve binding delimiter verbatim
            continue
        # a single-line non-binding comment
        if "<!--" in line and "-->" in line:
            line = re.sub(r"<!--.*?-->", "", line)
            if line.strip():
                out.append(line)
            continue
        # start of a multi-line comment
        if "<!--" in line:
            head = line.split("<!--", 1)[0]
            if head.strip():
                out.append(head)
            in_comment = True
            continue
        out.append(line)
    return "\n".join(out)

def draft_rendered(draft_text):
    if SENTINEL in draft_text:
        return False
    body = _strip_nonbinding_comments(draft_text)
    body = re.sub(r"^\s*<!--\s*claims:.*?-->\s*$", "", body, flags=re.MULTILINE)  # drop bindings for prose test
    body = re.sub(r"^#.*$", "", body, flags=re.MULTILINE)                          # drop headings
    return bool(norm_ws(body))

def parse_paragraphs(draft_text):
    """Yield (paragraph_text, claim_ids_or_None). None binding => unbound.
    Binding comments delimit and label the preceding paragraph."""
    body = _strip_nonbinding_comments(draft_text)
    paras = []
    buf = []
    def flush(binding):
        txt = "\n".join(buf).strip()
        if txt:
            paras.append((txt, binding))
        buf.clear()
    for line in body.splitlines():
        mb = BINDING_RE.match(line)
        if mb:
            binding = [x.strip() for x in mb.group(1).split(",") if x.strip()]
            flush(binding)
            continue
        if line.strip() == "":
            flush(None); continue
        if line.strip().startswith("#"):
            flush(None); continue
        buf.append(line)
    flush(None)
    return paras

# ----------------------------------------------------------------------------
# check framework
# ----------------------------------------------------------------------------
class Result:
    def __init__(self):
        self.checks = {}   # id -> {"sev","status","msgs"}
    def add(self, cid, sev, status, msgs=None):
        self.checks[cid] = {"sev": sev, "status": status, "msgs": msgs or []}

def admitted_ids(decis_txt):
    """Ids named on `- accepted:` lines, with ranges (`SUP-0001..0012`) expanded."""
    out = set()
    for m in re.finditer(r"^\s*-\s*accepted:\s*(.+)$", strip_html_comments(decis_txt), flags=re.MULTILINE):
        for tok in re.split(r"[,\s]+", m.group(1)):
            tok = tok.strip().rstrip(".;")
            r = re.match(r"^([A-Za-z]+-)(\d+)\.\.(?:[A-Za-z]+-)?(\d+)$", tok)
            if r:
                pre, a, b = r.group(1), r.group(2), r.group(3)
                for i in range(int(a), int(b) + 1):
                    out.add(f"{pre}{i:0{len(a)}d}")
            elif tok:
                out.add(tok)
    return out

def cite_keys_in(node):
    """All corpus keys a node references (SUPPORT cite:, REMEDY inline [cite: ...])."""
    ks = []
    if node.get("cite"): ks += [k.strip() for k in re.split(r"[,\s]+", node["cite"]) if k.strip()]
    for fld in ("enabling-now", "precedent"):
        if node.get(fld):
            for m in re.finditer(r"\[cite:\s*([^\]]+)\]", node[fld]):
                ks += [k.strip() for k in re.split(r"[,\s]+", m.group(1)) if k.strip()]
    return ks

def run():
    claims_txt = read(CLAIMS)
    corpus_txt = read(CORPUS)
    draft_txt  = read(DRAFT)
    protect_txt= read(PROTECT)
    struct_txt = read(STRUCT)
    decis_txt  = read(DECIS)
    issues_txt = read(ISSUES)

    nodes = parse_claims(claims_txt)
    by_id = {n["id"]: n for n in nodes}
    corpus, cfg = parse_corpus(corpus_txt)
    MISSION_TOKENS[:] = cfg["identifier_tokens"]
    rendered = draft_rendered(draft_txt)
    R = Result()

    def accepted(n): return n.get("status", "").lower() == "accepted"
    acc = [n for n in nodes if accepted(n)]
    def role(n): return n.get("role", "").upper()

    # ---- E-01 citation resolves (HALT) ----
    bad = []
    for n in nodes:
        for k in cite_keys_in(n):
            if k not in corpus:
                bad.append(f"{n['id']} cites '{k}' not in corpus")
    R.add("E-01", "HALT", "fail" if bad else "pass", bad)

    # ---- E-02 span verbatim (HALT; WARN if source not local) ----
    e02_fail, e02_warn = [], []
    src_cache = {}
    for n in nodes:
        if role(n) != "SUPPORT" or not n.get("span"): continue
        span = n["span"].strip().strip('"').strip("'")
        cks = cite_keys_in(n)
        if not cks: continue
        k = cks[0]
        meta = corpus.get(k)
        if not meta:
            continue  # E-01 owns unresolved keys
        if not meta["span_verifiable"] or not meta["path"] or meta["path"] == "—":
            e02_warn.append(f"{n['id']} cites {k} (span-unverifiable); strength={n.get('strength')}")
            if (n.get("strength","").lower() == "strong"):
                e02_fail.append(f"{n['id']} marked Strong on an unverifiable span (cite {k})")
            continue
        if k not in src_cache:
            src_cache[k] = norm_ws(read(resolve_corpus_path(meta["path"])))
            if not src_cache[k]:
                # span-verifiable=yes but the cache file is missing/empty: cannot
                # verify. Fail closed, but say why (config error, not fabrication).
                e02_fail.append(f"{n['id']} cite {k}: text cache '{meta['path']}' missing/empty — cannot verify span")
                continue
        if norm_ws(span) not in src_cache[k]:
            e02_fail.append(f"{n['id']} span not found verbatim in {k}")
    R.add("E-02", "HALT", "fail" if e02_fail else "pass", e02_fail + [f"WARN {w}" for w in e02_warn])

    # ---- E-03 comparative completeness (BLOCK) ----
    # AMD-003 (ratified at G2, 2026-07-17): the check applies to claims the author
    # MAKES as comparative — i.e. tag: comparative. A bare trigger word (e.g. a
    # descriptive "state-of-the-art" echoed from a quoted span in an empirical
    # claim) is NOT a comparative claim by this paper and does not fire. This scopes
    # E-03 to its intent (policing comparative claims) and removes the false
    # positive on descriptive/quoted trigger words.
    e03 = []
    for n in nodes:
        if role(n) != "SUPPORT": continue
        if n.get("tag","").lower() != "comparative": continue
        txt = (n.get("text","") or "").lower()
        has_baseline = any(b in txt for b in BASELINE_CONNECTIVES)
        has_metric = any(mh in txt for mh in METRIC_HINTS) or bool(re.search(r"\d", txt))
        if not (has_baseline and has_metric):
            e03.append(f"{n['id']} comparative lacks "
                       f"{'baseline ' if not has_baseline else ''}"
                       f"{'metric' if not has_metric else ''}".strip())
    R.add("E-03", "BLOCK", "fail" if e03 else "pass", e03)

    # ---- E-04 causal discipline (BLOCK + WARN) ----
    e04, e04w = [], []
    for n in nodes:
        if role(n) != "SUPPORT" or n.get("tag","").lower() != "causal": continue
        if not (n.get("mechanism") or "").strip():
            e04.append(f"{n['id']} tag:causal with no mechanism: field")
        span = (n.get("span","") or "").lower()
        if any(mk in span for mk in OBS_DESIGN_MARKERS) and not (n.get("mechanism") or "").strip():
            e04w.append(f"{n['id']} cited span is observational with no mechanism")
    R.add("E-04", "BLOCK", "fail" if e04 else "pass", e04 + [f"WARN {w}" for w in e04w])

    # ---- E-05 named incidence (BLOCK) ----
    # Scope: accepted GAPs only. A proposed GAP with a category/empty incidence is
    # the expected output of extraction; the hole is surfaced in the extraction
    # report and reviewed at G1/G3, not blocked pre-admission. Consistent with
    # E-07/E-08/E-09/E-12/E-17, which all gate on accepted. (Ratify at G2 —
    # see 04-log/rubric-amendments.md AMD-001.)
    e05 = []
    for n in acc:
        if role(n) != "GAP": continue
        inc = n.get("incidence","")
        if not inc.strip():
            e05.append(f"{n['id']} incidence empty")
            continue
        segs = [s.strip() for s in inc.split("|")]
        if len(segs) != 3 or not all(segs):
            e05.append(f"{n['id']} incidence needs 3 non-empty segments <name>|<decision>|<metric>")
            continue
        if segs[0].lower() in INCIDENCE_CATEGORIES:
            e05.append(f"{n['id']} incidence name '{segs[0]}' is a category, not a named person/office")
    R.add("E-05", "BLOCK", "fail" if e05 else "pass", e05)

    # ---- E-07 gap completeness (HALT) ----  [defined before E-06 for reuse]
    e07 = []
    for n in acc:
        if role(n) != "GAP": continue
        for fld in ("scope","magnitude","incidence","tractability"):
            if not (n.get(fld) or "").strip():
                e07.append(f"{n['id']} missing {fld}")
        nm = n["_lists"].get("nearest-miss", [])
        good_nm = [x for x in nm if len([f for f in x.split("|")]) >= 4 and x.split("|")[3].strip()]
        if len(good_nm) < 3:
            e07.append(f"{n['id']} has {len(good_nm)} complete nearest-miss (need 3 with exclusion rationale)")
        sc = n.get("scope","")
        if not re.search(r"\d{4}-\d{2}-\d{2}", sc):
            e07.append(f"{n['id']} scope has no search date (YYYY-MM-DD)")
        if "quer" not in sc.lower():
            e07.append(f"{n['id']} scope names no query string")
    R.add("E-07", "HALT", "fail" if e07 else "pass", e07)

    # ---- E-10 definitional dependency (HALT) ----
    # Scope: accepted GAPs only (see E-05 note). The single highest-severity check
    # in the system, but it adjudicates an ADMITTED definitional gap — pre-
    # admission, an underspecified DEF is a hole for G1/G3, not a halt. Ratify at
    # G2 (AMD-001).
    e10 = []
    for n in acc:
        if role(n) != "GAP": continue
        par = n.get("parent","").strip()
        if par and par in by_id and role(by_id[par]) == "DEFINITION":
            d = by_id[par]
            comp = d["_lists"].get("competing", [])
            if len([c for c in comp if c.strip()]) < 2:
                e10.append(f"{n['id']} parent {par} has <2 competing definitions")
            if not (d.get("excludes") or "").strip():
                e10.append(f"{n['id']} parent {par} has empty 'excludes'")
    R.add("E-10", "HALT", "fail" if e10 else "pass", e10)

    # ---- E-08 remedy completeness (BLOCK) ----
    e08 = []
    for n in acc:
        if role(n) != "REMEDY": continue
        for fld in ("mechanism","enabling-now","precedent","yield","cost-class"):
            if not (n.get(fld) or "").strip():
                e08.append(f"{n['id']} missing {fld}")
        alts = [a for a in n["_lists"].get("alternatives", []) if len(a.split("|")) >= 3 and a.split("|")[2].strip()]
        if len(alts) < 2:
            e08.append(f"{n['id']} has {len(alts)} complete alternatives (need 2 with exclusion rationale)")
    R.add("E-08", "BLOCK", "fail" if e08 else "pass", e08)

    # ---- E-09 yield specificity + reachability (BLOCK) ----
    e09 = []
    for n in acc:
        if role(n) == "REMEDY":
            if not re.search(r"GAP-\S+/\w", n.get("yield","")):
                e09.append(f"{n['id']} yield names no GAP-nn/<component>")
        if role(n) == "ASK":
            par = n.get("parent","").strip()
            if par not in by_id or role(by_id.get(par,{})) != "REMEDY":
                e09.append(f"{n['id']} ASK parent is not a REMEDY ({par})")
            else:
                rem = by_id[par]; gpar = rem.get("parent","").strip()
                if gpar not in by_id or role(by_id.get(gpar,{})) != "GAP":
                    e09.append(f"{n['id']} -> {par} does not reach a GAP")
        if role(n) == "SUPPORT":
            par = n.get("parent","").split("/")[0].strip()
            if par not in by_id or role(by_id.get(par,{})) not in ("GAP","DEFINITION","REMEDY","TENSION"):
                e09.append(f"{n['id']} SUPPORT reaches no GAP/DEF/REMEDY/TENSION ({par})")
    R.add("E-09", "BLOCK", "fail" if e09 else "pass", e09)

    # ---- E-19 tension completeness (BLOCK; accepted-only) — added AMD-002 ----
    # A TENSION is the "honest about tension" requirement made structural. When
    # accepted, it must actually name what it qualifies and how the paper answers
    # it, else it is decorative. Not on any ASK path, so no strength/reachability duty.
    e19 = []
    for n in acc:
        if role(n) != "TENSION": continue
        for fld in ("text","bears-on","disposition"):
            if not (n.get(fld) or "").strip():
                e19.append(f"{n['id']} missing {fld}")
        bo = n.get("bears-on","").strip()
        # bears-on must reference at least one real node id
        if bo and not any(tok.strip() in by_id for tok in re.split(r"[,\s]+", bo)):
            e19.append(f"{n['id']} bears-on names no known node ({bo})")
    R.add("E-19", "BLOCK", "fail" if e19 else "pass", e19)

    # ---- E-12 enabling-now recency (BLOCK) ----
    e12 = []
    base = cfg["recency_base"]; win = cfg["recency_window_years"]
    for n in acc:
        if role(n) != "REMEDY": continue
        en = n.get("enabling-now","")
        cites = re.findall(r"\[cite:\s*([^\]]+)\]", en)
        cites = [c.strip() for grp in cites for c in re.split(r"[,\s]+", grp) if c.strip()]
        ok = False
        for c in cites:
            yr = corpus.get(c, {}).get("year")
            if yr and (base - yr) <= win:
                ok = True
        if not ok:
            e12.append(f"{n['id']} enabling-now has no cite within {base-win}-{base}")
    R.add("E-12", "BLOCK", "fail" if e12 else "pass", e12)

    # ---- E-17 asserted load-bearing path (BLOCK) ----
    e17 = []
    def is_asserted(n): return n.get("strength","").lower() == "asserted"
    def def_passes_e10(d):
        comp = d["_lists"].get("competing", [])
        return len([c for c in comp if c.strip()]) >= 2 and bool((d.get("excludes") or "").strip())
    for n in acc:
        if role(n) != "ASK": continue
        rem = by_id.get(n.get("parent","").strip())
        if not rem: continue
        gap = by_id.get(rem.get("parent","").strip())
        for node in (rem, gap):
            if node and is_asserted(node):
                if role(node) == "DEFINITION" and def_passes_e10(node): continue
                e17.append(f"{n['id']} path traverses Asserted {node['id']}")
        if gap:
            d = by_id.get(gap.get("parent","").strip())
            if d and role(d)=="DEFINITION" and is_asserted(d) and not def_passes_e10(d):
                e17.append(f"{n['id']} path traverses Asserted DEF {d['id']} failing E-10")
    R.add("E-17", "BLOCK", "fail" if e17 else "pass", e17)

    # ---- E-18 admission integrity (HALT) ----
    # An admission is an id on a `- accepted:` line of decisions.md. Any other
    # mention (pending, rejected, a note) is not one: matching the id anywhere in
    # the file let "- pending: SUP-0006" count as admitting SUP-0006.
    admitted = admitted_ids(decis_txt)
    e18 = []
    for n in acc:
        if n["id"] not in admitted:
            e18.append(f"{n['id']} accepted with no entry in decisions.md")
    R.add("E-18", "HALT", "fail" if e18 else "pass", e18)

    # ---- prose-layer checks: E-06, E-11, E-15, E-16 ----
    citation_re = re.compile(r"\[([^\]\n]+)\]")
    if not rendered:
        for cid, sev in (("E-06","BLOCK"),("E-11","WARN"),("E-15","HALT"),("E-16","BLOCK"),("E-20","BLOCK"),("E-21","BLOCK")):
            R.add(cid, sev, "na", ["draft not yet rendered — deferred"])
    else:
        paras = parse_paragraphs(draft_txt)
        e06, e11 = [], []
        for txt, binding in paras:
            # The response-type/sphere declaration line is a required structural
            # header that E-16.2/E-16.3 look for by regex; it legitimately carries
            # the call's own terms ("contextual-topic", a sphere name) and is not
            # prose. Exempt it from E-06 binding rules.
            if re.match(r"^\s*Response type:\s*(science-target|implementation|contextual-topic|combination)",
                        txt, re.IGNORECASE):
                continue
            low = txt.lower()
            cites = [c for m in citation_re.findall(txt) for c in re.split(r"[,\s]+", m) if c in corpus]
            # For numeral tracing, remove citation markers (their years are not
            # quantities) and processing-level terminology ("Level 2" is a product
            # tier, not a statistic) before extracting numerals. Normalize trailing
            # punctuation so '2,' matches '2'.
            num_scan = citation_re.sub(" ", txt)
            num_scan = re.sub(r"[Ll]evel[\s-]*[0-4]\b", " ", num_scan)   # "Level 2", "Level-1"
            # Mission/instrument names carry digits that are identifiers, not
            # statistics ("Probe-2", "Sat-5P"). Strip the configured
            # identifier tokens before numeral extraction.
            for mt in MISSION_TOKENS:
                num_scan = re.sub(re.escape(mt), " ", num_scan)
            nums = [n.rstrip(".,") for n in re.findall(r"\d[\d.,]*", num_scan)]
            nums = [n for n in nums if n]
            comps = [w for w in COMPARATIVE_WORDS if re.search(r"\b"+re.escape(w)+r"\b", low)]
            if binding is None:
                e06.append(f"unbound paragraph: \"{norm_ws(txt)[:60]}...\"")
                continue
            if binding == ["REFERENCES"]:
                # A reference list is a bibliography rendered from cited corpus keys.
                # It is neither claim-prose nor FRAMING: exempt from numeral/proper-
                # noun rules; instead require every bracketed key to resolve (closure
                # is also enforced against the body by E-16.5).
                for m in citation_re.findall(txt):
                    for c in re.split(r"[,\s]+", m):
                        if c and re.match(r"^[a-z]", c) and c not in corpus:
                            e06.append(f"REFERENCES lists '{c}' not in corpus")
                continue
            if binding == ["FRAMING"]:
                if nums: e06.append(f"FRAMING paragraph contains numerals: {nums[:3]}")
                if comps: e06.append(f"FRAMING paragraph contains comparatives: {comps[:3]}")
                if cites: e06.append(f"FRAMING paragraph contains citations: {cites[:3]}")
                miss = [m for m in MISSION_TOKENS if re.search(r"\b"+re.escape(m)+r"\b", txt)]
                inst = [a for a in cfg["advocacy"] if a and re.search(r"\b"+re.escape(a)+r"\b", txt)]
                if miss or inst: e06.append(f"FRAMING paragraph names proper nouns: {(miss+inst)[:3]}")
            else:
                # Traceable text for a bound claim = ALL of its renderable component
                # fields (text, span, and role components like magnitude, incidence,
                # scope, tractability, mechanism, yield, disposition, bears-on, ...)
                # plus its list items (nearest-miss, alternatives, competing). A fact
                # the drafter renders may legitimately come from any of these, not
                # only `text`/`span`.
                SKIP = {"role","status","strength","tag","parent","history","notes","id"}
                def claim_blob(b):
                    nd = by_id.get(b, {})
                    parts = []
                    for k, v in nd.items():
                        if k in SKIP or k.startswith("_"): continue
                        if isinstance(v, str): parts.append(v)
                    for items in nd.get("_lists", {}).values():
                        parts.extend(items)
                    return " ".join(parts)
                for b in binding:
                    if b not in by_id:
                        e06.append(f"paragraph bound to unknown claim '{b}'")
                    elif not accepted(by_id[b]):
                        e06.append(f"paragraph bound to {b}, which is {by_id[b].get('status') or 'unadmitted'}, not accepted")
                bound_txt = " ".join(claim_blob(b) for b in binding).lower()
                bound_txt = re.sub(r"[Ll]evel[\s-]*[0-4]\b", " ", bound_txt)
                for mt in MISSION_TOKENS:
                    bound_txt = re.sub(re.escape(mt).lower(), " ", bound_txt)
                for num in nums:
                    # whole-token match: "2" must not be found inside "2000" or "0.12"
                    if not re.search(r"(?<![\d.,])" + re.escape(num) + r"(?![\d]|[.,]\d)", bound_txt):
                        e06.append(f"numeral '{num}' in bound para not in claims {binding}")
                for w in comps:
                    if not re.search(r"\b" + re.escape(w) + r"\b", bound_txt):
                        e06.append(f"comparative '{w}' in bound para not in claims {binding}")
                for c in cites:
                    if c not in " ".join(binding) and c not in bound_txt:
                        # citation key must be traceable to a bound claim's cite
                        bound_cites = [ck for b in binding for ck in cite_keys_in(by_id.get(b,{}))]
                        if c not in bound_cites:
                            e06.append(f"citation '{c}' in bound para not in bound claims {binding}")
                # advocacy tokens in FRAMING handled above; here flag in prose for E-11
            # E-11 advocacy: institution/program nouns anywhere in FRAMING or ASK.action
            if binding == ["FRAMING"]:
                for a in cfg["advocacy"]:
                    if a and re.search(r"\b"+re.escape(a)+r"\b", txt):
                        e11.append(f"advocacy token '{a}' in FRAMING paragraph")
        for n in acc:
            if role(n) == "ASK":
                for a in cfg["advocacy"]:
                    if a and re.search(r"\b"+re.escape(a)+r"\b", n.get("action","")):
                        e11.append(f"advocacy token '{a}' in {n['id']}.action")
        R.add("E-06", "BLOCK", "fail" if e06 else "pass", e06)
        R.add("E-11", "WARN", "fail" if e11 else "pass", e11)

        # ---- E-20/E-21 evidence-table discipline (BLOCK) — AMD-011, ratified 2026-07-19 ----
        # Scope: claims RENDERED in the draft (bound in a paragraph), non-SUPPORT. Legacy
        # accepted-but-unrendered nodes are not policed here (they make no claim in the paper).
        # E-20: every rendered non-SUPPORT claim must declare a claim-type.
        # E-21: any rendered claim of type inferred-from-shared-architecture must carry a
        #       non-empty generalization-boundary (an inference may not read as a measurement).
        bound_ids = set()
        for _txt, _b in paras:
            if _b and _b not in (["FRAMING"], ["REFERENCES"]):
                for _id in _b:
                    bound_ids.add(_id.strip())
        e20, e21 = [], []
        for _id in sorted(bound_ids):
            nd = by_id.get(_id)
            if not nd or role(nd) == "SUPPORT":
                continue
            ct = (nd.get("claim-type") or "").strip()
            if not ct:
                e20.append(f"{_id} rendered without a claim-type")
            if ct == "inferred-from-shared-architecture" and not (nd.get("generalization-boundary") or "").strip():
                e21.append(f"{_id} is inferred-from-shared-architecture with empty generalization-boundary")
        R.add("E-20", "BLOCK", "fail" if e20 else "pass", e20)
        R.add("E-21", "BLOCK", "fail" if e21 else "pass", e21)

        # E-15 protected text.
        # E-15's job is to catch protected text SILENTLY DROPPED during revision —
        # a phrase that was present in the prior draft version and has vanished.
        # A protected phrase that has NEVER been rendered yet (its section is not
        # drafted) is pending, not dropped: that is a WARN, not a HALT. Only a
        # phrase that regressed (present before, gone now) HALTs. At the final
        # gate (G4) the human treats any remaining WARN as must-resolve.
        e15_halt, e15_warn = [], []
        prev_draft = ""
        if os.path.isdir(VERSIONS):
            _vs = sorted(f for f in os.listdir(VERSIONS) if re.match(r"draft-v\d+\.md$", f))
            if _vs:
                prev_draft = norm_ws(read(p("03-state","versions",_vs[-1])))
        cur_norm = norm_ws(draft_txt)
        for m in re.finditer(r"^\|\s*(P-\d+)\s*\|\s*(.*?)\s*\|", protect_txt, flags=re.MULTILINE):
            pid, ptxt = m.group(1), m.group(2).strip()
            if not ptxt: continue
            if (pid + " released") in decis_txt: continue
            if norm_ws(ptxt) in cur_norm: continue
            # not in current draft: dropped (was in prev) => HALT; never present => WARN
            if prev_draft and norm_ws(ptxt) in prev_draft:
                e15_halt.append(f"protected {pid} was present in prior draft and is now missing (silent drop)")
            else:
                e15_warn.append(f"protected {pid} not yet rendered (pending section); resolve before G4")
        R.add("E-15", "HALT", "fail" if e15_halt else "pass",
              e15_halt + [f"WARN {w}" for w in e15_warn])

        # E-16 call conformance (venue-specific: populated for the original call)
        e16 = []
        # E-16.1 length proxy. The REFERENCES bibliography is excluded from the word
        # count: that call's page limit did not count references toward the ~7pp
        # body (AMD-009b, human-ruled 2026-07-18).
        words = sum(len(norm_ws(t).split()) for t,b in paras if b != ["FRAMING"] or True)
        body_words = sum(len(norm_ws(t).split()) for t,b in paras if b != ["REFERENCES"])
        if body_words > 5300:
            e16.append(f"E-16.1 body ~{body_words} words > 5300 (>7pp proxy) BLOCK")
        elif body_words > 4900:
            R.checks.setdefault("_notes",{})
        # E-16.2 response type
        if not re.search(r"response type:\s*(science-target|implementation|contextual-topic|combination)",
                         draft_txt, re.IGNORECASE):
            e16.append("E-16.2 no declared response type")
        # E-16.3 sphere
        if not (re.search(r"\b(Atmosphere|Biosphere|Cryosphere|Geosphere|Hydrosphere)\b", draft_txt)
                or re.search(r"cross-sphere", draft_txt, re.IGNORECASE)):
            e16.append("E-16.3 no sphere named / no cross-sphere justification")
        # E-16.5 reference closure
        for t,b in paras:
            for m in citation_re.findall(t):
                for c in re.split(r"[,\s]+", m):
                    if re.match(r"^[a-z].*\d{4}", c) and c not in corpus:
                        e16.append(f"E-16.5 draft cites '{c}' not in corpus")
        R.add("E-16", "BLOCK", "fail" if e16 else "pass", e16)

    # ---- E-13 churn (WARN) ----
    e13 = []
    vers = sorted([f for f in os.listdir(VERSIONS) if re.match(r"draft-v\d+\.md$", f)]) if os.path.isdir(VERSIONS) else []
    if len(vers) >= 1 and rendered:
        prev = read(p("03-state","versions",vers[-1]))
        ratio = 1 - difflib.SequenceMatcher(None, prev, draft_txt).ratio()
        transitions = len(re.findall(r"status:\s*(closed|wont-fix)", issues_txt))
        if ratio > 0.35 and transitions == 0:
            e13.append(f"churn {ratio:.2f} with 0 issue transitions")
        R.add("E-13", "WARN", "fail" if e13 else "pass", e13 or [f"churn {ratio:.2f}"])
    else:
        R.add("E-13", "WARN", "na", ["no prior version to diff"])

    # ---- E-14 regression (HALT) — compare to stored prior states ----
    prior = {}
    if os.path.exists(STATEF):
        try: prior = json.load(open(STATEF)).get("checks", {})
        except Exception: prior = {}
    newly_failing, newly_passing = [], []
    for cid, c in R.checks.items():
        if cid.startswith("_"): continue
        was = prior.get(cid)
        if was == "pass" and c["status"] == "fail":
            newly_failing.append(cid)
        if was == "fail" and c["status"] == "pass":
            newly_passing.append(cid)
    R.add("E-14", "HALT", "fail" if newly_failing else "pass",
          [f"REGRESSION {c} pass->fail" for c in newly_failing])

    return R, rendered, newly_failing, newly_passing, len(vers)

# ----------------------------------------------------------------------------
# report + verdict
# ----------------------------------------------------------------------------
CHECK_ORDER = ["E-01","E-02","E-03","E-04","E-05","E-06","E-07","E-08","E-09","E-10",
               "E-11","E-12","E-13","E-14","E-15","E-16","E-17","E-18","E-19","E-20","E-21"]

def verdict_of(R):
    # Skip `_`-prefixed bookkeeping keys (e.g. "_notes"): they carry no status/sev.
    halts  = [c for c,v in R.checks.items() if not c.startswith("_") and v["status"]=="fail" and v["sev"]=="HALT"]
    blocks = [c for c,v in R.checks.items() if not c.startswith("_") and v["status"]=="fail" and v["sev"]=="BLOCK"]
    warns  = [c for c,v in R.checks.items() if not c.startswith("_") and v["status"]=="fail" and v["sev"]=="WARN"]
    if halts:  return "HALT", halts, blocks, warns
    if blocks: return "BLOCKED", halts, blocks, warns
    return "CLEAN", halts, blocks, warns

def write_report(R, rendered, newly_failing, newly_passing):
    ver = "unrendered"
    if os.path.isdir(VERSIONS):
        vs = sorted([f for f in os.listdir(VERSIONS) if re.match(r"draft-v\d+\.md$", f)])
        if vs: ver = vs[-1].replace("draft-","").replace(".md","")
    v, halts, blocks, warns = verdict_of(R)
    applic = [c for c in CHECK_ORDER if R.checks.get(c,{}).get("status") in ("pass","fail")]
    npass = sum(1 for c in applic if R.checks[c]["status"]=="pass")
    na = [c for c in CHECK_ORDER if R.checks.get(c,{}).get("status")=="na"]

    L = []
    L.append("# Enforcer report")
    L.append("")
    L.append(f"- run: {now_iso()}")
    L.append(f"- draft version: {ver}{' (not yet rendered)' if not rendered else ''}")
    L.append(f"- verdict: {v}")
    advisory_warns = sum(1 for k,c in R.checks.items() if not k.startswith("_") for m in c["msgs"] if m.startswith("WARN "))
    failing_warns = sum(len(c["msgs"]) for k,c in R.checks.items() if not k.startswith("_") and c["sev"]=="WARN" and c["status"]=="fail")
    total_warns = advisory_warns + failing_warns
    L.append(f"- halts: {len(halts)} | blocks: {len(blocks)} | warns: {total_warns}")
    L.append(f"- checks passed: {npass}/{len(applic)} applicable  ({len(na)} n/a: {', '.join(na) if na else 'none'})")
    L.append("")
    for band, sev in (("HALT","HALT"),("BLOCK","BLOCK"),("WARN","WARN")):
        L.append(f"## {band}")
        any_line = False
        if band == "WARN":
            # WARN band collects: (a) failing WARN-severity checks, and (b) any
            # WARN-prefixed advisory message from ANY check regardless of its
            # severity (e.g. E-15 pending-protected-text, E-02 unverifiable-span).
            # A HALT/BLOCK check that passes can still carry advisory warnings.
            for c in CHECK_ORDER:
                v2 = R.checks.get(c)
                if not v2: continue
                for m in v2["msgs"]:
                    if m.startswith("WARN "):
                        L.append(f"- {c} | {m[5:]}"); any_line=True
                    elif v2["sev"]=="WARN" and v2["status"]=="fail":
                        L.append(f"- {c} | {m}"); any_line=True
        else:
            for c in CHECK_ORDER:
                v2 = R.checks.get(c)
                if not v2 or v2["sev"]!=sev: continue
                if v2["status"]=="fail":
                    for m in v2["msgs"]:
                        if not m.startswith("WARN "):
                            L.append(f"- {c} | {m}"); any_line=True
        if not any_line: L.append("- none")
        L.append("")
    L.append("## Delta vs previous run")
    L.append(f"- newly failing: {', '.join(newly_failing) if newly_failing else 'none'}")
    L.append(f"- newly passing: {', '.join(newly_passing) if newly_passing else 'none'}")
    L.append("")
    L.append("## Per-check status")
    for c in CHECK_ORDER:
        v2 = R.checks.get(c, {"status":"?","sev":"?"})
        L.append(f"- {c} [{v2['sev']}]: {v2['status']}")
    L.append("")
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(L))

    # append one-line summary to iterations.md
    line = (f"- [enforcer] {now_iso()} verdict={v} halts={len(halts)} "
            f"blocks={len(blocks)} warns={len(warns)} passed={npass}/{len(applic)} "
            f"draft={ver} newly_failing={','.join(newly_failing) or 'none'}\n")
    with open(ITER, "a", encoding="utf-8") as f:
        f.write(line)

    # persist state for regression
    json.dump({"run": now_iso(),
               "checks": {c: R.checks[c]["status"] for c in CHECK_ORDER if c in R.checks}},
              open(STATEF,"w"), indent=2)
    return v, npass, len(applic), len(na)

def main():
    quiet = "--quiet" in sys.argv
    if "--root" in sys.argv:
        i = sys.argv.index("--root")
        if i + 1 >= len(sys.argv):
            sys.exit("usage: enforce.py [--quiet] [--root DIR]")
        set_root(sys.argv[i + 1])
        if not os.path.isfile(CLAIMS):
            sys.exit(f"--root {sys.argv[i + 1]}: no 03-state/claims.md there")
    R, rendered, nf, npss, _ = run()
    v, npass, napp, na = write_report(R, rendered, nf, npss)
    if not quiet:
        print(f"verdict={v}  passed={npass}/{napp} applicable ({na} n/a)")
        if nf: print(f"REGRESSION newly failing: {', '.join(nf)}")
        print(f"report -> {os.path.relpath(REPORT, ROOT)}")
    # exit code: 2 on HALT, 1 on BLOCKED, 0 on CLEAN
    sys.exit(2 if v=="HALT" else (1 if v=="BLOCKED" else 0))

if __name__ == "__main__":
    main()
