from PIL import Image, ImageDraw, ImageFont
import pathlib, re

F = "/tmp/fonts"
def lit(sz, w="400"): return ImageFont.truetype(f"{F}/literata-latin-{w}-normal.ttf", sz)
def lit_i(sz):        return ImageFont.truetype(f"{F}/literata-latin-400-italic.ttf", sz)
def mono(sz, med=False):
    return ImageFont.truetype(f"{F}/IBMPlexMono-{'Medium' if med else 'Regular'}.ttf", sz)

PAPER="#0E1215"; INK="#DCE3E7"; MUTED="#8B99A3"
RULE="#263037"; RULE_STRONG="#3A474F"; SIGLUM="#E29286"; OPEN="#D7AC48"

W, H, M = 1200, 630, 84
OUT = pathlib.Path("/home/claude/ogk"); OUT.mkdir(exist_ok=True)

def runs(text):
    """split *italic* markers into (text, is_italic) runs"""
    out, i = [], 0
    for m in re.finditer(r"\*([^*]+)\*", text):
        if m.start() > i: out.append((text[i:m.start()], False))
        out.append((m.group(1), True)); i = m.end()
    if i < len(text): out.append((text[i:], False))
    return out

def run_width(d, rs, rf, itf):
    return sum(d.textlength(t, font=(itf if it else rf)) for t, it in rs)

def draw_runs(d, xy, rs, rf, itf, fill):
    x, y = xy
    for t, it in rs:
        f = itf if it else rf
        d.text((x, y), t, font=f, fill=fill); x += d.textlength(t, font=f)
    return x

def wrap_runs(d, text, rf, itf, maxw):
    """wrap while preserving italic runs"""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if run_width(d, runs(t), rf, itf) <= maxw: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def track(d, xy, text, font, fill, sp=0):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill); x += d.textlength(ch, font=font) + sp
    return x

def card(name, eyebrow, title, sub=None, facts=None, sigla=None, note=None, tag=None):
    im = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 7, H], fill=SIGLUM)                       # oxblood spine

    d.text((M, 50), "Kiliani", font=lit(30, "700"), fill=INK)
    if tag:
        tf = mono(19)
        track(d, (W - M - (d.textlength(tag, font=tf) + len(tag)*1.6), 60), tag, tf, MUTED, sp=1.6)
    d.line([(M, 104), (W - M, 104)], fill=RULE, width=1)

    track(d, (M, 140), eyebrow.upper(), mono(17, True), MUTED, sp=2.6)

    # title, italic-aware
    y, size = 192, 62
    rf, itf = lit(size, "700"), lit_i(size)
    lines = wrap_runs(d, title, rf, itf, W - 2*M - 10)
    while len(lines) > 2 and size > 44:
        size -= 6; rf, itf = lit(size, "700"), lit_i(size)
        lines = wrap_runs(d, title, rf, itf, W - 2*M - 10)
    for ln in lines:
        draw_runs(d, (M, y), runs(ln), rf, itf, INK); y += int(size * 1.15)

    if sub:
        y += 8
        srf, sitf = lit_i(30), lit_i(30)
        for ln in wrap_runs(d, sub, srf, sitf, W - 2*M - 80):
            draw_runs(d, (M, y), runs(ln), srf, sitf, MUTED); y += int(30 * 1.34)

    if sigla:
        sy, x, gf = y + 58, M + 13, mono(38, True)
        for s in sigla:
            wdt = d.textlength(s, font=gf)
            d.rectangle([x - 13, sy - 11, x + wdt + 13, sy + 50], outline=RULE_STRONG, width=1)
            d.text((x, sy), s, font=gf, fill=SIGLUM); x += wdt + 48

    if note:
        d.text((M, max(y + 34, 420)), note, font=lit_i(27), fill=OPEN)

    if facts:
        d.line([(M, 482), (W - M, 482)], fill=RULE, width=1)
        x, nf, lf = M, mono(33, True), mono(16)
        for i, (num, lbl) in enumerate(facts):
            d.text((x, 502), num, font=nf, fill=OPEN if i == 0 else INK)
            track(d, (x, 546), lbl.upper(), lf, MUTED, sp=1.8)
            x += max(d.textlength(num, font=nf),
                     d.textlength(lbl.upper(), font=lf) + len(lbl)*1.8) + 70

    ff = mono(18)
    d.text((M, 592), "nicholaskouns-create.github.io/Kiliani", font=ff, fill=MUTED)
    by = "Nicholas Shane Kouns, DO"
    d.text((W - M - d.textlength(by, font=ff), 592), by, font=ff, fill=MUTED)

    im.save(OUT / name, "PNG"); print(f"{OUT/name}  {W}×{H}")

card("og-home.png", "Open archive · dataset",
     "The *Passiones* of St Kilian",
     "and the record of how they were transmitted",
     tag="BHL 4660 · 4661",
     note="No descent from Saint Kilian is claimed or claimable.",
     facts=[("2", "Passiones"), ("7", "witnesses"), ("361", "readings"), ("251", "lemma entries")])

card("og-collation.png", "Apparatus criticus",
     "Every reading Emmerich recorded, and who reads it",
     "*Passio minor Kiliani* · Würzburg, 1896",
     tag="BHL 4660",
     facts=[("251", "lemma entries"), ("361", "readings"), ("7", "witnesses")])

card("og-witnesses.png", "Witnesses",
     "The seven manuscripts Emmerich collated",
     sigla=["Sg", "V", "M¹", "M²", "Ad", "W", "P"],
     facts=[("7", "shelfmarks"), ("s. IX–XV", "dated"), ("IIIF", "manifests served")])

card("og-verification.png", "Verification record",
     "What was read, and from what",
     "Counts, residue, and the limits of the affinity figures",
     note="A signal, not a stemma.",
     facts=[("354 / 361", "readings parsed"), ("98%", "coverage"), ("7", "need autopsy")])
