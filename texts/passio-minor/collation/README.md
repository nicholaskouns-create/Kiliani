# Emmerich's collation, made machine-readable

**What this is.** Franz Emmerich's apparatus criticus to the *Passio minor
Kiliani* — *Der heilige Kilian, Regionarbischof und Martyrer* (Würzburg 1896),
pp. 3–10 — transcribed entry by entry and parsed into a dataset: **251 lemma
entries, 361 readings, 7 witnesses.**

**What this is not.** It is **not a collation of manuscripts.** Not one
manuscript was consulted. Every witness attribution here is Emmerich's, made in
the 1890s, and inherits whatever he got wrong. It is not an edition, and
[../reading-text-la-en.md](../reading-text-la-en.md) remains uncollated in the
sense that file states: no one in this archive has compared a manuscript against
the Latin it prints. What has changed is only that Emmerich's record of the
manuscripts is now queryable instead of being locked in a printed apparatus.

**It is not Levison.** [../editions.md](../editions.md) is right that Levison
(1910) is the standard text. Emmerich is earlier, independent, and in hand.

---

## Why the plates and not the OCR

The scan's text layer is OCR of 1896 antiqua. It confuses `V` with `F`, `Sg`
with `8g`, `M²` with `ilf"`, drops the semicolons that separate readings, and
breaks words at line-ends. A first pass over that layer attributed **two**
readings to M² where the page shows dozens.

So every entry was read by eye from the page rendered at about 430 dpi. The
verbatim string of each apparatus entry is kept in
[apparatus_verbatim.py](apparatus_verbatim.py) as the primary datum — one Python
string per entry, in Emmerich's own abbreviations — so that any record can be
checked against the printed page without re-reading the whole apparatus.
Everything else is derived from those strings by
[build_model.py](build_model.py) and regenerates from them.

```
python3 -I build_model.py     # rebuilds data/
python3 -I make_plate.py      # rebuilds the figure
```

## The witnesses

Transcribed from Emmerich's manuscript list, with his foliation.

| siglum | shelfmark | repository | date | locus | cited |
|---|---|---|---|---|---|
| **Sg** | Cod. Sang. 566 | Stiftsbibliothek St Gallen | s. IX | pp. 212–219 | 24 |
| **V** | Cod. 552 | ÖNB Vienna | s. X in. | f. 107v–112r | 45 |
| **M¹** | Clm 4585 | BSB Munich | s. IX–XI | f. 115r–119v | 41 |
| **M²** | Clm 4332 | BSB Munich | s. XII | f. 68r–70v | 82 |
| **Ad** | Cod. 412 | Stiftsbibliothek Admont | s. XII | f. 118r–120v | 81 |
| **W** | M.p.th.f. 64 | UB Würzburg | s. XI | f. 304r–307 | 111 |
| **P** | Cod. 2896 | Schönborn, Pommersfelden | s. XIII–XIV | f. 182v–183v | 57 |

[../witnesses.md](../witnesses.md) records nineteen witnesses from the
repertory. These seven are the ones Emmerich actually collated.

## Two things the citation counts show

Emmerich's apparatus is **mixed**: he prints a normalised text and names a
witness only where it departs from what he set. Under that convention the
citation count runs *inverse* to how closely his text follows a manuscript.

**Sg is cited 24 times, the fewest by a wide margin.** His base is St Gallen 566.
The arithmetic says so without his having stated it.

**W is cited 111 times, the most** — and Emmerich notes of that manuscript,
*"Aliquibus locis omittuntur, quae pertinent ad ornatum orationis."* The Würzburg
copy abridges rhetorical ornament and the apparatus registers every omission. His
prose note and the citation count agree, which is the best available check that
the transcription is sound.

## Affinity, and the three reasons it is not a stemma

`data/agreement_matrix.csv` counts lemmas where two witnesses are cited **in the
same reading**; `data/opposition_matrix.csv` counts lemmas where they are cited
in **different** readings. Affinity is agreements ÷ (agreements + oppositions).

| pair | agree | oppose | affinity |
|---|---|---|---|
| Sg–M¹ | 8 | 3 | **0.727** |
| V–M¹ | 9 | 6 | 0.600 |
| V–M² | 9 | 9 | 0.500 |
| V–W | 9 | 11 | 0.450 |
| M²–W | 14 | 18 | 0.438 |
| Ad–P | 7 | 9 | 0.438 |

Sg–M¹ stands clear, with V–M¹ behind it: the early witnesses group, and the two
latest (Ad, P) pair at the other end. **This is a signal and must not be
published as a stemma**, for three reasons:

1. The apparatus is mixed, so agreement with the base text is invisible. Sg's
   affinities are depressed by precisely the thing that makes Sg the base.
2. Descent is argued from shared **errors**. Emmerich does not mark which
   readings are errors, and nothing here infers it.
3. Orthographic agreement — *uuirziburc*, *wirzipurch*, *wirzeburg* — is scribal
   habit and region, not lineage. The `orthographic` tag in the data is
   heuristic and wants a philologist's pass.

## One lemma, read across the witnesses

p. 4, lemma 8. The adopted text: *propria contempni patriamque et parentes
secundum Domini evangelium relinquere et nudos sequi Christum.*

| witness | date | reading | |
|---|---|---|---|
| **Sg** | s. IX | propria **contempni** | passive infinitive; the adopted reading |
| **W** | s. XI | propria **contempnere** | active |
| **M²** | s. XII | propria **contemnere** | active, classical orthography |
| **P** | s. XIII–XIV | **propriam** contempnere | accusative singular |
| **Ad** | s. XII | *secundum evangelium domini* **nudosque Christum sequi** | clause transposed |

*Contemnere* and *sequi* hold across every witness. *Propria* does not — and in
P, by assimilation to the *patriam* that follows, it stops being the companions'
possessions and becomes their country.

## Files

| file | contents |
|---|---|
| [apparatus_verbatim.py](apparatus_verbatim.py) | **the primary datum** — 251 entries transcribed from the plates |
| [witnesses_data.py](witnesses_data.py) | the seven witnesses, from Emmerich's manuscript list |
| [build_model.py](build_model.py) | parser; regenerates everything in `data/` |
| [make_plate.py](make_plate.py) | regenerates the figure |
| [emmerich-chapter-15.md](emmerich-chapter-15.md) | the closing chapter, printed in full, with its apparatus |
| `data/witnesses.json` · `.csv` | repository, shelfmark, date, format, extent, locus, incipit, explicit |
| `data/variants.json` · `.csv` | 361 readings: verbatim source, witnesses, type, marginal notes |
| `data/agreement_matrix.csv` | pairwise shared readings |
| `data/opposition_matrix.csv` | pairwise disagreement at the same lemma |
| `data/stemma_signal.json` | citation counts and ranked affinities |
| `data/apparatus_tei.xml` | TEI P5 `<listWit>` and `<app>`/`<rdg>` encoding |
| `passio_minor_collation.png` | the figure |

## Seven readings still needing autopsy

Entries where Emmerich's own prose note is split by a semicolon, so the parser
could not attribute a witness. Each is transcribed correctly; only the machine
attribution is missing. They are listed with `parsed: false` in
`data/variants.json`, at p. 4 n. 2; p. 5 n. 40; p. 6 nn. 28, 29; p. 7 n. 25;
p. 8 n. 15; p. 9 n. 29.

## Still open

- **IIIF.** Every `iiif` field is `null`. St Gallen (e-codices), the ÖNB and the
  BSB all serve IIIF; Admont partly. Filling them turns each citation into a link
  to the folio, and bears on queue item 6.
- **Line numbering**, which needs the printed text keyed line by line, not by
  lemma.
- **Emendations against all witnesses.** Where Emmerich emends silently, with no
  manuscript cited, only autopsy will show it. The data distinguishes what he
  printed from what each manuscript has; it cannot distinguish what he printed
  from what no manuscript has.

---

## On the signature

Nicholas Shane Kouns asked me to sign this, and I would rather sign it accurately
than generously.

Emmerich collated the manuscripts. He did the work this file depends on, in the
1890s, by hand, with seven codices in front of him. Nicholas Shane Kouns built
this archive, set its boundaries, and wrote the verification queue that told me
where to look — item 7 of that queue is the reason this directory exists, and
item 1 is the reason I read as far as page 10.

What is mine: the transcription from the plates; the parser and the data model;
the observation that the citation counts identify Emmerich's base text and
corroborate his own note on W; the affinity measure and the three reasons it is
not a stemma; the figure; and noticing that the chapter the archive had only at
second hand was printed in full on a page already in the file.

What is not mine is the text, the manuscripts, the scholarship, or the archive.

— **Claude** (Anthropic, Opus 5), 28 October 2026, in conversation with
Nicholas Shane Kouns.
