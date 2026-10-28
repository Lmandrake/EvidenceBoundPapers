#!/bin/bash
# Finals-compliance build: draft.md -> assembled markdown -> DOCX -> PDF -> page count.
#   1. assemble masthead + body (claim-binding comments stripped) + author-year references
#   2. EM-DASH GATE: abort if any em-dash (U+2014) remains anywhere (voice guide: strongest model tell)
#   3. render DOCX via pandoc, optionally against a pinned reference doc (font size, spacing)
#   4. render to PDF headlessly with LibreOffice (never drive a word processor's GUI: focus steal)
#   5. THEN evaluate the real page limit against the rendered PDF (body pages, refs excluded);
#      over the limit exits 3 and publishes nothing
#   6. copy the PDF to a review folder, if one is configured (replacing only this paper's finals)
# Usage: tools/build-final.sh vNNN       (run from anywhere; the instance is tools/..)
#
# Venue-specific inputs, all optional except the masthead:
#   00-seed/masthead.md    title, call, authors, affiliation, contact. Prepended verbatim.
#   EBP_REFERENCE_DOCX     pandoc --reference-doc (fonts, margins). Default: pandoc's own.
#   EBP_REVIEW_DIR         a folder to copy the final PDF into for co-author review.
#   EBP_PAPER_ID           short name used in output filenames (default: the instance folder name),
#                          so a shared review folder only ever loses this paper's older finals.
#   EBP_PAGE_LIMIT         body-page limit to check (default 7; references excluded).
#   SOFFICE                LibreOffice binary (default: soffice on PATH, else the macOS app).

set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXPORTS="$ROOT/04-log/exports"
DRAFT="$ROOT/03-state/draft.md"
MASTHEAD="$ROOT/00-seed/masthead.md"
VER="${1:?usage: build-final.sh vNNN}"
DATE="$(date +%F)"
PAPER_ID="${EBP_PAPER_ID:-$(basename "$ROOT")}"
BASE="$EXPORTS/${DATE}-${PAPER_ID}-final-${VER}"
PAGE_LIMIT="${EBP_PAGE_LIMIT:-7}"
[ -f "$MASTHEAD" ] || { echo "ABORT: write $MASTHEAD first (title, authors, contact)"; exit 1; }
mkdir -p "$EXPORTS"

# --- 1. assemble ---------------------------------------------------------
python3 - "$DRAFT" "$BASE.md" "$MASTHEAD" <<'PY'
import re, sys, unicodedata
draft, out, masthead_path = sys.argv[1], sys.argv[2], sys.argv[3]

# corpus keys may contain underscores and digits (smith_2019, survey_v4)
KEY = r'[A-Za-z0-9_]+'

_raw = open(draft).read()
_refblk = re.sub(r'<!--.*?-->','', _raw.split("## References",1)[1], flags=re.S).strip()
_entries = re.findall(r'\[(' + KEY + r')\]\s*(.*?)(?=\s*\[' + KEY + r'\]\s|\Z)', _refblk, flags=re.S)
def _short(authors):
    a = authors.strip()
    if a.startswith("National Academies"): return "National Academies"
    if " et al." in a:
        first = re.split(r',|&', a.split(" et al.")[0])[0].strip()
        return first + " et al."
    parts = [p.strip() for p in re.split(r',|&', a) if p.strip()]
    if len(parts) == 1: return parts[0]
    if len(parts) == 2: return parts[0] + " & " + parts[1]
    return parts[0] + " et al."
CITE, REFENTRY = {}, {}
for key, rest in _entries:
    rest = rest.strip().rstrip('-').strip()
    ym = re.search(r'\((\d{4})\)', rest)
    year = ym.group(1) if ym else ""
    authors = rest[:ym.start()].strip() if ym else rest
    CITE[key] = f"{_short(authors)}, {year}"
    REFENTRY[key] = rest
def convert_intext(text):
    def repl(mo):
        keys = [k.strip() for k in mo.group(1).split(",")]
        return "(" + "; ".join(CITE.get(k, k) for k in keys) + ")"
    return re.sub(r'\[(' + KEY + r'(?:\s*,\s*' + KEY + r')*)\]', repl, text)

masthead = open(masthead_path, encoding="utf-8").read()
lines = _raw.splitlines()
body, dropped = [], False
for ln in lines:
    if ln.strip().startswith("<!-- claims:"):
        continue
    if not dropped and ln.startswith("# "):
        dropped = True; continue
    if ln.startswith("Response type:"):
        continue
    body.append(ln)
text = "\n".join(body).strip()
head = text.split("## References", 1)[0].rstrip()
head = convert_intext(head)
def _sortkey(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)).lower()
reflist = "\n\n".join(sorted(REFENTRY.values(), key=_sortkey))
text = head + "\n\n## References\n\n::: {custom-style=\"Bibliography\"}\n\n" + reflist + "\n\n:::\n"
open(out, "w").write(masthead.rstrip() + "\n\n" + text + "\n")
print("assembled:", out)
PY

# --- 2. em-dash gate -----------------------------------------------------
EMDASH=$'\xe2\x80\x94'   # U+2014 as UTF-8 bytes; bash 3.2 has no \u
if grep -qF -- "$EMDASH" "$BASE.md"; then
  echo "ABORT: em-dash(es) present in assembled draft:"; grep -nF -- "$EMDASH" "$BASE.md"; exit 1
fi
echo "em-dash gate: clean (0)"

# --- 3. DOCX --------------------------------------------------------------
REFARG=()
[ -n "${EBP_REFERENCE_DOCX:-}" ] && REFARG=(--reference-doc="$EBP_REFERENCE_DOCX")
pandoc "$BASE.md" -o "$BASE.docx" --from markdown+raw_attribute "${REFARG[@]+"${REFARG[@]}"}"
echo "docx: $BASE.docx"

# --- 4. PDF via headless LibreOffice (no GUI, no focus steal) -----------
SOFFICE="${SOFFICE:-$(command -v soffice || echo /Applications/LibreOffice.app/Contents/MacOS/soffice)}"
"$SOFFICE" --headless --convert-to pdf --outdir "$EXPORTS" \
  -env:UserInstallation="file://${TMPDIR:-/tmp}/ebp-lo-profile" "$BASE.docx" >/dev/null 2>&1
echo "pdf: $BASE.pdf"

# --- 5. evaluate page limit against the rendered PDF --------------------
python3 - "$BASE.pdf" "$PAGE_LIMIT" <<'PY'
import subprocess, sys
limit = int(sys.argv[2])
txt = subprocess.check_output(["pdftotext", sys.argv[1], "-"]).decode("utf8","replace")
pages = txt.split("\f")
total = len([p for p in pages if p.strip()])
refpage = next((i for i,pg in enumerate(pages,1)
                if any(l.strip()=="References" for l in pg.splitlines())), None)
if refpage is None:
    body = total
else:
    # The page where References begins counts as body only if body text precedes the heading.
    before = pages[refpage-1].split("References", 1)[0]
    body = refpage if before.strip() else refpage - 1
print("==============================================")
print(f"TOTAL pages:            {total}")
print(f"References begins on:    page {refpage}")
print(f"BODY pages (counted):   {body}   (limit = {limit}; references EXCLUDED)")
print("PAGE LIMIT:", f"OK (body <= {limit})" if body <= limit else "OVER — trim body")
print("==============================================")
sys.exit(0 if body <= limit else 3)
PY

# --- 6. publish to a review folder (only this paper's finals) ----------
if [ -n "${EBP_REVIEW_DIR:-}" ] && [ -d "$EBP_REVIEW_DIR" ]; then
  find "$EBP_REVIEW_DIR" -maxdepth 1 -name "*-${PAPER_ID}-final-*.pdf" -delete
  cp "$BASE.pdf" "$EBP_REVIEW_DIR/"
  echo "published for review: $(basename "$BASE.pdf")"
fi
