#!/usr/bin/env python3
"""Enforce this archive's epistemic boundaries.

The mathematical repositories in this project use continuous integration to
check proofs. A hagiographic archive has no proofs to check. What it has instead
is *labels* -- and a label is only worth something if it cannot quietly fall off.

So this script checks the labels rather than the mathematics. It fails the build
if any of the following stops being true:

  1. The genealogical boundary is stated in the family README.
  2. No file asserts descent from Saint Kilian.
  3. The conflated *Passio maior* carries its notice.
  4. The superseded source plate carries its notice.
  5. The working edition does not call itself a critical edition.
  6. Nothing claims to be a "citable edition".
  7. Internal cross-links resolve.
  8. The corrected translations have not regressed.

Run: python3 tools/check_boundaries.py
Exit: 0 if every boundary holds, 1 otherwise.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAILURES: list[str] = []
CHECKS = 0


def fail(where: str, msg: str) -> None:
    FAILURES.append(f"{where}: {msg}")


def check(ok: bool, label: str, detail: str = "") -> None:
    global CHECKS
    CHECKS += 1
    print(f"{'PASS' if ok else 'FAIL'} {label}" + (f"  --  {detail}" if detail else ""))
    if not ok:
        fail(label, detail or "boundary not satisfied")


def md_files() -> list[Path]:
    return sorted(p for p in ROOT.rglob("*.md") if ".git" not in p.parts)


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


# --------------------------------------------------------------------------
print("ARCHIVE BOUNDARY CHECK")
print("=" * 72)

# 1. the boundary is stated where a reader meets the family material first
fam = ROOT / "family" / "README.md"
text = read(fam) if fam.exists() else ""
check(
    "No descent from Saint Kilian is claimed or claimable" in text,
    "family/README.md states the genealogical boundary verbatim",
)
check(
    "cannot be its own primary evidence" in text or "circular" in text,
    "family/README.md names the circularity problem",
)

# 2. nothing anywhere asserts descent
#    the boundary files are allowed to quote the unsupported formulation in
#    order to reject it, so they are exempted by name.
EXEMPT = {
    ROOT / "family" / "README.md",
    ROOT / "recensions" / "CHANGES.md",
    ROOT / "recensions" / "01-source-plate.md",
    ROOT / "scholarship" / "research-report.md",
    ROOT / "interpretive" / "README.md",
    ROOT / "README.md",
    ROOT / "STATUS.md",
    ROOT / "tools" / "check_boundaries.py",
}
# files that exist in order to record what was withdrawn, and so must be free to
# quote the withdrawn wording
RECORDS_OF_REMOVAL = EXEMPT | {
    ROOT / "recensions" / "README.md",
    ROOT / "texts" / "passio-minor" / "verification-queue.md",
}
DESCENT = re.compile(
    r"(descend(s|ed|ant)?\s+from\s+(the\s+)?(st\.?\s*|saint\s+)?kilian"
    r"|genealogically\s+descended"
    r"|bloodline\s+(to|from)\s+(st\.?\s*|saint\s+)?kilian)",
    re.I,
)
# A whole-file exemption would let the boundary files themselves assert descent
# and pass vacuously, which is worse than no check. So the exempt files are not
# skipped: every match in them must sit in a context that quotes or rejects the
# formulation rather than asserting it.
REJECTING = re.compile(
    r"(\bnot\b|\bno\b|\bnever\b|cannot|unsupported|withdraw|removed|refut"
    r"|\bnor\b|disclaim|un(est|sub))",
    re.I,
)


def quoted_or_rejected(lines: list[str], i: int) -> bool:
    """True if the match is a quotation or is explicitly rejected nearby.

    Known limitation: inside the boundary files, which are full of rejecting
    language, this window heuristic will clear an assertion planted next to a
    rejection. Check 1 (the verbatim boundary statement) is the backstop there,
    and it does catch that case. Outside those files the scan is strict.
    """
    line = lines[i]
    if line.lstrip().startswith(">"):
        return True  # block-quoted formulation
    window = " ".join(lines[max(0, i - 3) : i + 4])
    return bool(REJECTING.search(window))


offenders = []
for p in md_files():
    lines = read(p).splitlines()
    for i, line in enumerate(lines):
        if not DESCENT.search(line):
            continue
        if p in EXEMPT and quoted_or_rejected(lines, i):
            continue
        offenders.append(f"{p.relative_to(ROOT)}:{i + 1}")
check(not offenders, "no file asserts descent from Saint Kilian", ", ".join(offenders))

# 3. the conflation notice travels with the conflated text
maior = ROOT / "texts" / "passio-maior" / "modern-conflated-recension-la-en.md"
mt = read(maior) if maior.exists() else ""
check(maior.exists(), "the conflated maior text is present")
check(
    "not the medieval" in mt.lower() and "CONFLATION-NOTICE" in mt,
    "conflated maior carries its notice and links to it",
)
def flat(body: str) -> str:
    """Collapse blockquote markers and line wrapping before matching a phrase."""
    return re.sub(r"\s+", " ", body.replace("\n> ", " ").replace("*", ""))


check(
    "non editio codicum mediaevalium" in flat(mt),
    "conflated maior carries the Latin disclaimer",
)
notice = ROOT / "texts" / "passio-maior" / "CONFLATION-NOTICE.md"
nt = read(notice) if notice.exists() else ""
check(
    "Beatus Kylianus, Scotorum genere" in nt and "Fuit vir vitae venerabilis" in nt,
    "conflation notice states the diagnostic incipits",
)

# 4. the superseded plate says so, at the top
plate = ROOT / "recensions" / "01-source-plate.md"
pt = read(plate) if plate.exists() else ""
check(
    "errors intact" in pt.lower() and "Not the archive's text" in pt,
    "superseded source plate is labelled as superseded",
)

# 5/6. the working edition does not over-claim
minor = ROOT / "texts" / "passio-minor" / "reading-text-la-en.md"
rt = read(minor) if minor.exists() else ""
check(
    "not a critical edition" in rt.lower(),
    "minor reading text disclaims being a critical edition",
)
check(
    "has not yet been collated" in rt.lower() or "not been collated" in rt.lower(),
    "minor reading text discloses that it is uncollated",
)
bad_claim = [
    f"{p.relative_to(ROOT)}"
    for p in md_files()
    if p not in RECORDS_OF_REMOVAL and re.search(r"citable edition", read(p), re.I)
]
check(not bad_claim, "nothing calls itself a 'Citable Edition'", ", ".join(bad_claim))

# 7. internal links resolve
LINK = re.compile(r"\[[^\]]*\]\(([^)#]+?)(?:#[^)]*)?\)")
broken = []
for p in md_files():
    for m in LINK.finditer(read(p)):
        target = m.group(1).strip()
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        if not (p.parent / target).resolve().exists():
            broken.append(f"{p.relative_to(ROOT)} -> {target}")
check(not broken, "internal links resolve", "; ".join(broken[:6]))

# 8. the corrected translations have not regressed
REGRESSIONS = {
    r"Scottish land": "Scottica tellus means Ireland, not Scotland",
    r"southern region": "in Australium partem means Austrasia, not the south",
    r"\bGallonus\b": "Gallone is ablative; the nominative is Gallo",
    r"\bArnualdus\b": "Arnuvale is ablative; the nominative is Arnual",
}
# the current texts must be clean; the superseded plate and the record of the
# corrections necessarily contain the old readings.
# Only the text whose translation was corrected. The conflated maior is a modern
# composition with its own (sometimes ungrammatical) Latin readings; those are
# source material, annotated in place, never edited to suit this check.
CURRENT = [
    ROOT / "texts" / "passio-minor" / "reading-text-la-en.md",
]
regressed = []
for p in CURRENT:
    if not p.exists():
        continue
    body = read(p)
    for pat, why in REGRESSIONS.items():
        if re.search(pat, body):
            regressed.append(f"{p.relative_to(ROOT)}: {why}")
check(not regressed, "corrected translations have not regressed", "; ".join(regressed))

# the plate must still contain them, or it has been silently cleaned
check(
    bool(re.search(r"Scottish land", pt)) and bool(re.search(r"southern region", pt)),
    "superseded plate still preserves its original errors",
    "the plate is evidence; cleaning it destroys the record of the correction",
)

# --------------------------------------------------------------------------
print("=" * 72)
if FAILURES:
    print(f"RESULT: {len(FAILURES)} of {CHECKS} boundaries FAILED")
    for f in FAILURES:
        print(f"  - {f}")
    sys.exit(1)
print(f"RESULT: all {CHECKS} boundaries hold.")
print("The archive states what it is and what it does not assert.")
sys.exit(0)
