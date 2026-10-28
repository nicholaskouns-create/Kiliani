#!/usr/bin/env python3
"""
build_model.py — parse the verbatim apparatus into the §6.1 data model and
derive the collation statistics that a stemma has to be built on.

Emits, in out/:
  witnesses.json / .csv        desideratum (a): siglum table with foliation
  variants.json / .csv         every reading, with witnesses and a type
  agreement_matrix.csv         pairwise co-citation (shared readings)
  opposition_matrix.csv        pairwise disagreement at the same lemma
  stemma_signal.json           normalised agreement, ranked
  apparatus_tei.xml            TEI P5 <app>/<rdg> fragment
  VERIFICATION.md              what was read from plate, what is derived
"""
from __future__ import annotations
import csv, json, re, sys, itertools
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from apparatus_verbatim import PAGES
from witnesses_data import WITNESSES

SIGLA = ["Sg", "Ad", "M¹", "M²", "W", "P", "V"]       # longest-first for greedy match
ID = {"Sg":"Sg","Ad":"Ad","M¹":"M1","M²":"M2","W":"W","P":"P","V":"V"}
ORDER = ["Sg","V","M1","M2","Ad","W","P"]              # chronological
CENTURY = {w["id"]: w["century"] for w in WITNESSES}

SIG_TAIL = re.compile(r"((?:Sg|Ad|M¹|M²|[WPV])+)\s*$")

def split_sigla(run: str):
    out, i = [], 0
    while i < len(run):
        for s in SIGLA:
            if run.startswith(s, i):
                out.append(ID[s]); i += len(s); break
        else:
            return None
    return out

def classify(text: str) -> str:
    t = text.lower()
    if "deest" in t or "sine " in t:                     return "omission"
    if "addit" in t:                                     return "addition"
    if "rasura" in t or "ii. m." in t or "ii m." in t \
       or "manus" in t or "mauus" in t or "m. aeq" in t \
       or "a. m." in t or "in margine" in t or "posterior" in t:
                                                          return "scribal_correction"
    if re.search(r"\bl\.\s", text):                      return "alternative_reading"
    if "..." in text or " - " in text:                   return "transposition_or_lacuna"
    return "variant"

# orthographic equivalences characteristic of 9th-14th c. German Latin
ORTHO = [(r"uu","w"),(r"v","u"),(r"ch","c"),(r"k","c"),(r"y","i"),(r"ae","e"),
         (r"oe","e"),(r"ti","ci"),(r"mp","m"),(r"pp","p"),(r"tt","t"),
         (r"ss","s"),(r"ll","l"),(r"nn","n"),(r"mm","m"),(r"h",""),(r"z","c")]
def skeleton(w: str) -> str:
    s = w.lower()
    for a,b in ORTHO: s = s.replace(a,b)
    return s

def main():
    out = Path("data")
    variants, unparsed = [], []
    for page, entries in sorted(PAGES.items()):
        for raw in entries:
            m = re.match(r"^(\d+[a-z]?)\s+(.*)$", raw)
            if not m:
                unparsed.append((page, raw)); continue
            lemma_no, body = m.group(1), m.group(2)
            for chunk in [c.strip() for c in body.split(";") if c.strip()]:
                marg = None
                mm = re.search(r"\[([^\]]+)\]", chunk)
                if mm:
                    marg = mm.group(1); chunk = chunk[:mm.start()].strip()
                sm = SIG_TAIL.search(chunk)
                wits, reading, ok = [], chunk, False
                if sm:
                    cand = split_sigla(sm.group(1))
                    if cand:
                        wits, reading, ok = cand, chunk[:sm.start()].strip(), True
                variants.append(dict(
                    variant_id=f"PMK-{page}-{lemma_no}-{len(variants)}",
                    work="Passio minor Kiliani (BHL 4660)",
                    edition="Emmerich 1896",
                    page_printed=page,
                    lemma_no=lemma_no,
                    verbatim=raw,
                    reading=reading,
                    witnesses=wits,
                    marginal_note=marg,
                    type=classify(chunk + (" " + marg if marg else "")),
                    parsed=ok,
                    source="plate (rendered 430 dpi), hand-transcribed",
                ))
    # orthographic refinement: within a lemma, readings sharing a skeleton
    bylem = defaultdict(list)
    for v in variants: bylem[(v["page_printed"], v["lemma_no"])].append(v)
    for group in bylem.values():
        skels = [skeleton(re.sub(r"[^A-Za-zÀ-ÿ ]","",v["reading"]).strip()) for v in group]
        for v, s in zip(group, skels):
            if v["type"] == "variant" and sum(1 for t in skels if t == s) > 1:
                v["type"] = "orthographic"

    # ---- witness citation counts
    cites = defaultdict(int)
    for v in variants:
        for w in v["witnesses"]: cites[w] += 1

    # ---- agreement (cited in the SAME reading) and opposition (different readings, same lemma)
    agree = defaultdict(int); oppose = defaultdict(int)
    for v in variants:
        for a, b in itertools.combinations(sorted(set(v["witnesses"])), 2):
            agree[(a,b)] += 1
    for group in bylem.values():
        for v1, v2 in itertools.combinations(group, 2):
            for a in set(v1["witnesses"]):
                for b in set(v2["witnesses"]):
                    if a != b: oppose[tuple(sorted((a,b)))] += 1

    # ---- write
    json.dump(WITNESSES, open(out/"witnesses.json","w"), indent=2, ensure_ascii=False)
    with open(out/"witnesses.csv","w",newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(WITNESSES[0])); wr.writeheader()
        for w in WITNESSES: wr.writerow(w)
    json.dump(variants, open(out/"variants.json","w"), indent=2, ensure_ascii=False)
    with open(out/"variants.csv","w",newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["variant_id","page_printed","lemma_no","type","reading","witnesses","marginal_note","verbatim"])
        for v in variants:
            wr.writerow([v["variant_id"],v["page_printed"],v["lemma_no"],v["type"],
                         v["reading"],"|".join(v["witnesses"]),v["marginal_note"] or "",v["verbatim"]])
    def matrix(d, path):
        with open(out/path,"w",newline="") as f:
            wr = csv.writer(f); wr.writerow([""]+ORDER)
            for a in ORDER:
                wr.writerow([a]+[("" if a==b else d.get(tuple(sorted((a,b))),0)) for b in ORDER])
    matrix(agree, "agreement_matrix.csv"); matrix(oppose, "opposition_matrix.csv")

    ranked = []
    for a,b in itertools.combinations(ORDER,2):
        k=(min(a,b),max(a,b)); ag=agree.get(k,0); op=oppose.get(k,0)
        if ag+op: ranked.append(dict(pair=f"{a}-{b}", agreements=ag, oppositions=op,
                                     affinity=round(ag/(ag+op),3)))
    ranked.sort(key=lambda r:-r["affinity"])
    json.dump(dict(citations=dict(sorted(cites.items(), key=lambda kv:-kv[1])),
                   pairs=ranked), open(out/"stemma_signal.json","w"), indent=2)

    # TEI
    tei = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<TEI xmlns="http://www.tei-c.org/ns/1.0">',
           '  <teiHeader><fileDesc><titleStmt><title>Passio minor Kiliani — apparatus criticus</title>',
           '  <respStmt><resp>collation</resp><name>Franz Emmerich, Der heilige Kilian (Würzburg 1896), pp. 3-10</name></respStmt>',
           '  <respStmt><resp>machine-readable encoding</resp><name>N. S. Kouns research corpus</name></respStmt>',
           '  </titleStmt><publicationStmt><p>Research edition.</p></publicationStmt>',
           '  <sourceDesc><listWit>']
    for w in WITNESSES:
        tei.append(f'    <witness xml:id="{w["id"]}"><msDesc><msIdentifier>'
                   f'<repository>{w["repository"]}</repository><idno>{w["shelfmark"]}</idno>'
                   f'</msIdentifier><history><origin>{w["century"]}</origin></history>'
                   f'<physDesc><p>{w["locus"]}</p></physDesc></msDesc></witness>')
    tei += ['  </listWit></sourceDesc></fileDesc></teiHeader>','  <text><body>']
    for (page, lemma), group in sorted(bylem.items(), key=lambda kv:(kv[0][0], int(re.sub(r"\D","",kv[0][1]) or 0))):
        tei.append(f'    <app n="{page}.{lemma}">')
        for v in group:
            wits = " ".join("#"+w for w in v["witnesses"])
            r = (v["reading"] or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
            tei.append(f'      <rdg wit="{wits}" type="{v["type"]}">{r}</rdg>')
        tei.append('    </app>')
    tei += ['  </body></text>','</TEI>']
    open(out/"apparatus_tei.xml","w").write("\n".join(tei))

    # report
    n_ok = sum(1 for v in variants if v["parsed"])
    types = defaultdict(int)
    for v in variants: types[v["type"]] += 1
    print(f"lemma entries (from plate) : {sum(len(v) for v in PAGES.values())}")
    print(f"readings parsed            : {len(variants)}  witness-attributed: {n_ok} ({100*n_ok/len(variants):.0f}%)")
    print("types                      : " + ", ".join(f"{k}={v}" for k,v in sorted(types.items(), key=lambda kv:-kv[1])))
    print("citations per witness      : " + ", ".join(f"{w}={cites.get(w,0)}" for w in ORDER))
    print("\ntop witness affinities (shared readings / all co-occurrences):")
    for r in ranked[:8]:
        print(f"   {r['pair']:<8} agree={r['agreements']:<4} oppose={r['oppositions']:<4} affinity={r['affinity']}")
    if unparsed: print("\nUNPARSED:", unparsed)
    return variants, ranked, cites

if __name__ == "__main__":
    main()
