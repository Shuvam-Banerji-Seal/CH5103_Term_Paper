"""Render the last overlay of frames whose title contains any of the given strings (review helper).
usage: python render_frames.py OUTDIR DPI "title fragment" ...   (run from presentation/)"""
import sys, re, fitz
out, dpi, wants = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
d = fitz.open("build/main.pdf")
last, title_hit = {}, {}
for i, p in enumerate(d):
    t = p.get_text().replace("\u2019", "'")
    head = t.splitlines()[0] if t.strip() else ""
    for w in wants:
        if w in head:  # frame title match wins over a mention in the body
            title_hit[w] = i
        elif w in t:
            last[w] = i
last.update(title_hit)
for w, i in last.items():
    fn = f"{out}/{re.sub(r'[^A-Za-z0-9]+', '_', w)[:40]}.png"
    d[i].get_pixmap(dpi=dpi).save(fn)
    print(i + 1, fn)
