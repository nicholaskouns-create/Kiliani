# Editorial status

Every file, with what kind of claim it makes. The arrangement of this repository
is its argument, and this is the table that states it.

## Evidence classes

| Class | Meaning |
|---|---|
| **E1 — Medieval source** | Latin text descending from manuscript witnesses |
| **E2 — Working edition** | A reading text derived from printed editions; not collated; not citable |
| **E3 — Modern reconstruction** | Composed in the modern period from medieval material; labelled as such |
| **E4 — Apparatus** | Notes, witness lists, edition lists, verification queues |
| **E5 — Secondary literature** | Research reports, reviews, bibliography |
| **E6 — Genealogical record** | Family lines, graded documented / likely / speculative |
| **E7 — Interpretation** | Not a historical claim |

---

## Texts

| File | Class | Status |
|---|---|---|
| `texts/passio-minor/reading-text-la-en.md` | **E2** | Abridged reading text. **Not collated against Levison.** Four marked defects. Cite Levison, not this. |
| `texts/passio-minor/apparatus.md` | E4 | Eight notes; nn. 4, 6, 7, 8 flag defects |
| `texts/passio-minor/witnesses.md` | E4 | Contains an unresolved disagreement, recorded not settled |
| `texts/passio-minor/editions.md` | E4 | Two unresolved page ranges |
| `texts/passio-minor/verification-queue.md` | E4 | Seven open items |
| `texts/passio-maior/modern-conflated-recension-la-en.md` | **E3** | ⚠ **Modern conflation.** Not the medieval *maior*. Not citable as a tenth-century source. |
| `texts/passio-maior/CONFLATION-NOTICE.md` | E4 | The diagnostic and the correct label |
| `texts/passio-maior/witnesses.md` | E4 | Authentic witnesses, none inspected |
| `texts/passio-maior/editions.md` | E4 | No modern critical edition exists |

**No file in this repository is class E1.** No manuscript has been transcribed
and no witness has been inspected. Everything textual here descends from printed
editions at one or more removes. That is the single most important line in this
table.

## Recensions

| File | Class | Status |
|---|---|---|
| `recensions/01-source-plate.md` | **E3** | ⚠ Superseded first state, **errors intact by design** |
| `recensions/CHANGES.md` | E4 | Complete change record with reasons |

## Scholarship

| File | Class | Status |
|---|---|---|
| `scholarship/research-report.md` | E5 | Current. The spine of the archive. |
| `scholarship/multilingual-dossier.txt` | E5 | Current |
| `scholarship/ecclesiastical-review.txt` | E5 | Kept as written. Contains three claims corrected elsewhere — see its README caution. |
| `scholarship/modern-archive-monograph.txt` | E5 | **Superseded** in its translations and its genealogy; kept as written |
| `scholarship/bibliography.md` | E4 | Current |

## Family

| File | Class | Status |
|---|---|---|
| `family/README.md` | E4 | **States the claim boundary.** Read before anything else in that directory. |
| `family/maternal-killion-line.md` | **E6** | Graded. Generations 6–7 unresolved; one name uncorroborated |
| `family/paternal-kouns-line.md` | **E6** | Graded. Generation 5 fully documented; generation 11 unresolved |
| `family/augsburg-artistic-corpus.md` | E6 | Documented; accession numbers given |
| `family/discrepancies.md` | E4 | Ten internal contradictions, recorded not reconciled |
| `family/open-questions.md` | E4 | Prioritised archival checklist |
| `family/iron-and-gold.txt` | E5 | Critical synthesis of both plates, as written |
| `family/augsburg-artistic-corpus-source.txt` | **E7 / E5 mixed** | Documentary catalogue woven with interpretive framing; read with its register in mind |

## Interpretive

| File | Class | Status |
|---|---|---|
| `interpretive/README.md` | E4 | States that nothing in the directory is a historical claim |
| `interpretive/kkp-factual-monograph.pdf` | **E7** | Mathematics. Not hagiography. Not evidence for anything in `texts/` or `family/`. |

---

## The three standing labels

Carried on the files that need them, and enforced by
[`tools/check_boundaries.py`](tools/check_boundaries.py):

1. The *maior* text is a modern conflation.
2. The first source plate is superseded, with its errors intact.
3. No descent from Saint Kilian is claimed or claimable.

## What would change this table

A single inspected manuscript would put the first E1 in it. A collation against
Levison would move the *minor*'s reading text from E2 toward E1. Reading the
Augsburg family chronicle would move several E6 rows toward **documented**.

Those three are the whole programme, and they are in
[`texts/passio-minor/verification-queue.md`](texts/passio-minor/verification-queue.md)
and [`family/open-questions.md`](family/open-questions.md).
