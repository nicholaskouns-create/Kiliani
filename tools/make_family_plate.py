#!/usr/bin/env python3
"""The full family tree, as a publication plate in the Kiliani site grammar.

Confidence is drawn, not described: every card carries the archive's own grading
as a coloured spine and a mono label. Entries the archive has removed are kept
and struck through, because a chart that hides its corrections is worth less than
one that shows them.
"""
from PIL import Image, ImageDraw, ImageFont
import pathlib

F = "/tmp/fonts"
def lit(sz, w="400"):  return ImageFont.truetype(f"{F}/literata-latin-{w}-normal.ttf", sz)
def lit_i(sz):         return ImageFont.truetype(f"{F}/literata-latin-400-italic.ttf", sz)
def mono(sz, med=False):
    return ImageFont.truetype(f"{F}/IBMPlexMono-{'Medium' if med else 'Regular'}.ttf", sz)

PAPER="#0E1215"; SURFACE="#161C20"; INK="#DCE3E7"; MUTED="#8B99A3"
RULE="#263037"; RULE_STRONG="#3A474F"; SIGLUM="#E29286"; OPEN="#D7AC48"

# grading -> (spine colour, label, label colour)
G = {
 "val":  (INK,     "VALIDATED",   INK),
 "doc":  (INK,     "DOCUMENTED",  INK),
 "star": (INK,     "",            INK),
 "lik":  (RULE_STRONG, "LIKELY",  MUTED),
 "spec": (OPEN,    "SPECULATIVE", OPEN),
 "unres":(OPEN,    "UNRESOLVED",  OPEN),
 "rm":   (SIGLUM,  "REMOVE",      SIGLUM),
 "fig":  (RULE_STRONG, "A FIGURE, NOT AN ANCESTOR", MUTED),
}

MATERNAL = [
 ("fig",  "St Kilian", "c. 640–689", "Ireland · Würzburg", "", "A FIGURE, NOT AN ANCESTOR"),
 ("rm",   "“St Clegwallabog Killian”", "1490–1555", "—", "", "FICTION — REMOVE"),
 ("rm",   "Hans Kilian", "1516–1583", "Augsburg", "", "CONFLATION — REMOVE"),
 ("star", "Bartholomäus Kilian I", "1548–1587/88", "Silesia · Augsburg", "", "THE LINE STARTS HERE"),
 ("doc",  "Wolfgang Kilian", "1581–1662", "Augsburg · Italy", "", ""),
 ("doc",  "Philipp Kilian", "1628–1693", "Augsburg · Italy", "", ""),
 ("val",  "Johannes Killian", "1689–1742", "Augsburg · Königsberg",
          "Elisabetha Kilian  1712–1777", "VALIDATED · FS"),
 ("val",  "Johann Killion", "1732–1781", "Germany · North Carolina",
          "Anne Balschbach  1734–1816", "VALIDATED · FS"),
 ("val",  "William Killion", "1768–1850", "N. Carolina · Tennessee",
          "Alley Coleman  b. 1789", "VALIDATED · FS"),
 ("val",  "John Jonas Killion", "1813–1890", "Tennessee · Laurel Co., Ky.",
          "Martha Lanham  1817–1869", "L66J-QKB"),
 ("val",  "Arthur L. Killion", "1848–1920", "Laurel Co., Kentucky",
          "Susan Goins  1855–1889", "9QYK-CY4"),
 ("val",  "Alex Killion", "1885–1961", "Kentucky",
          "Edna Elizabeth Hill  1895–1973", "G86V-J98"),
 ("val",  "Anna Rose Killion Kouns", "1931–2015", "Lancaster, Kentucky", "", "G86H-5RY"),
]

PATERNAL = [
 ("lik",  "Henchin / Johann Henchin Cuntze", "c. 1500–1570", "Niederndorf · Oberfischbach", "", ""),
 ("lik",  "Arnold Cuntze", "c. 1530–1590", "Nassau-Siegen", "", ""),
 ("lik",  "Johannes Cuntze", "c. 1574–1640", "Nassau-Siegen", "", ""),
 ("lik",  "Johannes Kuntze / Cuntze", "c. 1640–1675", "Niederndorf", "", "GUILD STEELSMITHS"),
 ("star", "Joseph Jost Cuntze", "1674–1731", "Niederndorf · Virginia",
          "Anna Gertrud Reinschmidt  m. 1704", "THE 1714 CROSSING"),
 ("lik",  "Georg Heinrich Koontz", "1708–1796", "Shenandoah, Virginia", "", ""),
 ("lik",  "Balthasar Koontz / Balser Counts", "1735–1835", "Virginia · frontier", "", ""),
 ("lik",  "Christian Kouns / Kunz / Coontz", "1759–1837", "Shenandoah · Greenbrier", "", ""),
 ("spec", "John Lamp Kouns", "c. 1780–1826 or 1851", "Ohio · Kentucky", "", "DATES DISAGREE"),
 ("lik",  "Christian Kouns", "1815–1870", "Greenup Co., Kentucky", "", ""),
 ("val",  "George W. Kouns", "1863–1952", "Kentucky",
          "Lucy Kouns  1868–", "L615-BHK"),
 ("val",  "Edgar Kouns", "1902–1967", "Kentucky",
          "Evelyn Alma Unrue  1907–1996", "LCT2-XN4"),
 ("val",  "Donald Ray Kouns", "1932–2003", "Kentucky", "", "LH8V-CLD"),
]

REYNOLDS = [
 ("Henry Reynolds", "1737–1824", "Elizabeth McClain  d. 1826"),
 ("Henry Reynolds Jr.", "1771/1774–1856", "Elizabeth Willis  m. 25 Nov 1797"),
 ("Henry A. Reynolds", "1801–1865", "Patsy Goins"),
 ("John Wesley “Creek John” Reynolds", "1833–1921", "Francena Baker  1834–1899"),
 ("Ann Elizabeth “Eliza” Reynolds", "1856–1944", "John Patterson Hill  1849–1923"),
 ("Elizabeth “Lizzie” Hill", "1895–1973", "m. Alex Killion, 8 June 1910"),
]

W, H = 2200, 3910
M = 96
COLW = 880
GUT = W - 2*M - 2*COLW
CARD_H, GAP = 168, 20

def track(d, xy, text, font, fill, sp=0):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill); x += d.textlength(ch, font=font) + sp
    return x

def fit(d, text, font_fn, maxw, start, floor=26):
    sz = start
    while sz > floor and d.textlength(text, font=font_fn(sz)) > maxw:
        sz -= 2
    return font_fn(sz)

def card(d, x, y, w, rec, idx):
    grade, name, dates, place, spouse, note = rec
    spine, _, _ = G[grade]
    d.rectangle([x, y, x + w, y + CARD_H], fill=SURFACE, outline=RULE, width=1)
    d.rectangle([x, y, x + 6, y + CARD_H], fill=spine)

    # generation chip
    cf = mono(26, True)
    n = str(idx)
    d.ellipse([x + 26, y + 26, x + 74, y + 74], outline=RULE_STRONG, width=2)
    d.text((x + 50 - d.textlength(n, font=cf)/2, y + 36), n, font=cf, fill=MUTED)

    tx = x + 98
    nf = fit(d, name, lambda s: lit(s, "700"), w - 130 - 230, 40, 26)
    col = SIGLUM if grade == "rm" else INK
    d.text((tx, y + 26), name, font=nf, fill=col)
    if grade == "rm":                      # struck through, kept visible
        wd = d.textlength(name, font=nf)
        d.line([(tx, y + 26 + nf.size*0.62), (tx + wd, y + 26 + nf.size*0.62)],
               fill=SIGLUM, width=2)

    df = mono(25)
    d.text((tx, y + 78), dates, font=df, fill=MUTED if grade != "rm" else SIGLUM)
    pf = lit_i(24)
    d.text((tx + d.textlength(dates, font=df) + 26, y + 79), place, font=pf, fill=MUTED)

    if spouse:
        sf = lit_i(24)
        d.text((tx + 26, y + 118), spouse, font=sf, fill=MUTED)
        d.ellipse([tx, y + 128, tx + 12, y + 140], outline=MUTED, width=2)

    if note:
        lf = mono(19, True)
        nc = OPEN if grade in ("spec", "unres") else (SIGLUM if grade == "rm" else MUTED)
        tw = d.textlength(note, font=lf) + len(note)*1.4
        nx = x + w - 26 - tw
        if grade in ("star", "val"):
            cy0 = y + 36
            d.polygon([(nx - 30, cy0), (nx - 21, cy0 - 9), (nx - 12, cy0), (nx - 21, cy0 + 9)], fill=INK)
        track(d, (nx, y + 28), note, lf, nc, sp=1.4)

def column(d, x, rows, title, sub):
    tf = lit(40, "700")
    d.text((x, 496), title, font=tf, fill=INK)
    track(d, (x, 550), sub.upper(), mono(21, True), MUTED, sp=2.4)
    d.line([(x, 592), (x + COLW, 592)], fill=RULE_STRONG, width=1)
    y = 622
    for i, rec in enumerate(rows, 1):
        card(d, x, y, COLW, rec, i)
        y += CARD_H + GAP
        if i < len(rows):
            cx = x + COLW/2
            d.line([(cx, y - GAP), (cx, y)], fill=RULE_STRONG, width=2)
    return y

def build():
    im = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 10, H], fill=SIGLUM)

    # masthead
    d.text((M, 96), "The Killion–Kouns Family", font=lit(86, "700"), fill=INK)
    d.text((M, 206), "Two lines, iron and gold. Validated through the Church's record, generation by generation.",
           font=lit_i(38), fill=MUTED)
    d.line([(M, 286), (W - M, 286)], fill=RULE, width=1)

    # legend
    lx, ly = M, 322
    track(d, (lx, ly), "CONFIDENCE  ·  THE FAMILYSEARCH LINE IS STIPULATED PRIMARY BY THE COMPILER, A MEMBER OF THE CHURCH", mono(20, True), MUTED, sp=2.4)
    items = [(INK, "validated — FamilySearch, stipulated"), (INK, "documented — scholarly record"),
             (RULE_STRONG, "likely"), (OPEN, "speculative"),
             (SIGLUM, "removed — kept struck through")]
    x = lx
    for colr, lab in items:
        d.rectangle([x, ly + 40, x + 26, ly + 62], fill=colr)
        f = lit(26)
        d.text((x + 38, ly + 36), lab, font=f, fill=MUTED)
        x += 38 + d.textlength(lab, font=f) + 54

    nf = lit_i(25)
    d.text((M, ly + 84), "A filled mark denotes an entry validated through FamilySearch; "
           "where an identifier was captured it stands in place of the label.", font=nf, fill=MUTED)
    d.text((M, ly + 114), "The Augsburg generations rest on independent scholarly record, "
           "not on the stipulation. The removed entries stay removed.", font=nf, fill=MUTED)

    ymat = column(d, M, MATERNAL, "Maternal — Kilian / Killion",
                  "Augsburg goldsmiths and engravers, into Appalachia")
    ypat = column(d, M + COLW + GUT, PATERNAL, "Paternal — Cuntze / Kouns",
                  "Nassau-Siegen ironworkers, to Germanna in 1714")
    ybot = max(ymat, ypat)

    # convergence
    lcx = M + COLW/2
    rcx = M + COLW + GUT + COLW/2
    ccx = W/2
    jy = ybot + 44
    d.line([(lcx, ybot - GAP), (lcx, jy)], fill=RULE_STRONG, width=2)
    d.line([(rcx, ybot - GAP), (rcx, jy)], fill=RULE_STRONG, width=2)
    d.line([(lcx, jy), (rcx, jy)], fill=RULE_STRONG, width=2)
    d.line([(ccx, jy), (ccx, jy + 46)], fill=SIGLUM, width=3)

    bw, bh = 1000, 150
    bx, by = ccx - bw/2, jy + 46
    d.rectangle([bx, by, bx + bw, by + bh], fill=SURFACE, outline=SIGLUM, width=2)
    nf = lit(50, "700")
    d.text((ccx - d.textlength("Nicholas Shane Kouns", font=nf)/2, by + 28),
           "Nicholas Shane Kouns", font=nf, fill=INK)
    sf = mono(26)
    s = "1965–    ·    Danville, Kentucky    ·    GKX3-5D2"
    d.text((ccx - d.textlength(s, font=sf)/2, by + 96), s, font=sf, fill=MUTED)

    # Reynolds inset
    ry = by + bh + 70
    d.line([(M, ry), (W - M, ry)], fill=RULE, width=1)
    track(d, (M, ry + 30), "THE REYNOLDS–HILL BRANCH  ·  ENTERS AT ALEX KILLION'S MARRIAGE, 1910",
          mono(21, True), MUTED, sp=2.4)
    d.text((M, ry + 64), "The best-evidenced stretch in the archive — the family's own papers, not a derivative tree.",
           font=lit_i(27), fill=MUTED)
    cw = (W - 2*M - 5*16) / 6
    for i, (nm, dt, sp_) in enumerate(REYNOLDS):
        cx = M + i * (cw + 16)
        cy = ry + 118
        d.rectangle([cx, cy, cx + cw, cy + 176], fill=SURFACE, outline=RULE, width=1)
        d.rectangle([cx, cy, cx + 4, cy + 176], fill=INK)
        f = fit(d, nm, lambda s: lit(s, "600"), cw - 32, 27, 17)
        words, line, yy = nm.split(), "", cy + 18
        for wd in words:
            t = (line + " " + wd).strip()
            if d.textlength(t, font=f) <= cw - 32: line = t
            else:
                d.text((cx + 16, yy), line, font=f, fill=INK); yy += int(f.size*1.22); line = wd
        if line: d.text((cx + 16, yy), line, font=f, fill=INK); yy += int(f.size*1.22)
        d.text((cx + 16, cy + 104), dt, font=mono(20), fill=MUTED)
        f2 = fit(d, sp_, lambda s: lit_i(s), cw - 32, 20, 14)
        d.text((cx + 16, cy + 138), sp_, font=f2, fill=MUTED)
        if i < 5:
            d.line([(cx + cw, cy + 88), (cx + cw + 16, cy + 88)], fill=RULE_STRONG, width=2)

    # colophon
    fy = H - 92
    d.line([(M, fy - 34), (W - M, fy - 34)], fill=RULE, width=1)
    ff = mono(22)
    d.text((M, fy), "nicholaskouns-create.github.io/Kiliani/family.html", font=ff, fill=MUTED)
    t = "Revised 18 November 2026 · FamilySearch line stipulated primary · family/familysearch-ids.md"
    d.text((W - M - d.textlength(t, font=ff), fy), t, font=ff, fill=MUTED)

    out = pathlib.Path("family/plates/killion-kouns-full-tree.png")
    im.save(out, "PNG"); print(f"{out}  {W}×{H}  {out.stat().st_size//1024}K")
    return out

if __name__ == "__main__":
    build()
