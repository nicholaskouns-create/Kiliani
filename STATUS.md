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

⚠ **And it is now known to have cost something.** The October 2026 research pass
established that the archive's closing sentence for the *Passio minor* is **not
the genuine chapter 15** — it is a different sentence, missing the mediation of
Boniface, missing *primus Wirziburegensium episcopus*, and reducing *Pippino
primo orientalium Francorum rege* to a bare *Pippini regis*, which deletes the
evidence for Levison's dating. See
[`texts/passio-minor/apparatus.md`](texts/passio-minor/apparatus.md) n. 8.

## Saints and cult — new, October 2026

| File | Class | Status |
|---|---|---|
| `saints/kilian-of-aubigny.md` | E5 | The second saint, d. c. 670, feast 13 Nov. Conflation risk stated; no medieval conflation found |
| `saints/cilline-of-iona.md` | E5 | Two Iona abbots; the Ó Cillín clerics who are not saints; the Trithemius origin of the Iona claim |
| `cult/relics-and-pilgrimage.md` | E5 | Busts melted 1794, relics hidden 1795, rediscovered 1849, returned 1949 |
| `cult/kilian-gospels.md` | **E4/A** | Würzburg UB M.p.th.q.1a located, dated by the library, digitised |
| `cult/worldwide.md` | E5 | Dedications, Ireland, the papal texts, and why no canonisation act exists |

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
| `scholarship/bibliography.md` | E4 | Current; expanded Oct 2026 with full citations and post-2015 work |
| `scholarship/web-survey-2026-10.md` | E5 | Index of the October 2026 research pass: what it resolved, added, and could not do |

## Family

| File | Class | Status |
|---|---|---|
| `family/README.md` | E4 | **States the claim boundary.** Read before anything else in that directory. |
| `family/maternal-killion-line.md` | **E6** | Graded. Generations 6–7 unresolved; one name uncorroborated |
| `family/paternal-kouns-line.md` | **E6** | Graded. Generation 5 fully documented; generation 11 unresolved |
| `family/augsburg-artistic-corpus.md` | E6 | Documented; accession numbers given |
| `family/discrepancies.md` | E4 | Ten internal contradictions, recorded not reconciled |
| `family/open-questions.md` | E4 | Prioritised archival checklist |
| `family/reynolds-hill-branch.md` | **E6** | ⭐ The best-evidenced stretch. **Resolves discrepancy 1.** Cherokee tradition labelled [D] |
| `family/surname.md` | E5 | Etymology, Griffith's distribution, bearers worldwide. **Polygenetic** |
| `family/irish-leads.md` | **E6/C** | Five leads, all from one amateur page, three corrected, each with a record set |
| `family/plates/` | **E3** | The family's own charts, kept as issued with their errors listed |
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

Two more, cheaper than any of those and added in October 2026:

- **Donald Ray Kouns's death certificate** settles which of two irreconcilable
  paternal lines is real.
- **Two Kentucky cemeteries and a handful of county death certificates** move the
  whole Reynolds–Hill–Killion branch from *likely* to *documented*.

Queues:
[`texts/passio-minor/verification-queue.md`](texts/passio-minor/verification-queue.md),
[`family/open-questions.md`](family/open-questions.md),
[`family/irish-leads.md`](family/irish-leads.md),
[`cult/relics-and-pilgrimage.md`](cult/relics-and-pilgrimage.md),
[`cult/worldwide.md`](cult/worldwide.md).

## October 2026 ledger

| | Count |
|---|---|
| Earlier questions **closed** | 5 |
| Corrections of this archive **reversed against it** | 1 (Bartholomäus I's death year) |
| **New** problems surfaced | 3, one of them the most serious in the archive |
| Witnesses recorded for the *minor* | 5 → **19** |
| Saints named Kilian distinguished | 1 → **3** |
| Lineage generations struck as non-existent | **2** |
