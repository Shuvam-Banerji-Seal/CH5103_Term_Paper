"""Render annotated screenshots of the review for the slides.

  sign_error_raw.png        the equation block on p. 441 as published
  sign_error_marked.png     same, with the correct product form boxed (green) and the
                            two-determinant line plus its offending "+" marked (rose)
  paper_page1.png           first page (title slide / overview)

Usage:  uv run --project .. python -I scripts/make_screenshots.py   (from presentation/)
"""
import pathlib

import fitz  # PyMuPDF

HERE = pathlib.Path(__file__).resolve().parent.parent
PDF = HERE.parent / "paper" / "Uncommon_Molecular_Electronic_Configuration.pdf"
OUT = HERE / "figures" / "screenshots"
DPI = 300

# coordinates in PDF points on page index 1 (journal p. 441), found with page.get_text("dict")
CLIP = fitz.Rect(311, 326, 549, 470)
PRODUCT_FORM = fitz.Rect(315, 353, 546, 380)        # 1Psi = 1/sqrt2[..+..] * 1/sqrt2[b a - a b]  (correct)
DET_SUM = fitz.Rect(336, 401.5, 497, 467)            # 1/sqrt2 1/sqrt2 ( |iii| + |iv| )  (wrong sign)
PLUS_SIGN = fitz.Rect(385.5, 444.0, 393.5, 458.0)  # the "+" between the two determinants

GREEN = (0.32, 0.80, 0.50)
ROSE = (0.93, 0.27, 0.47)


def render(page, clip, path):
    page.get_pixmap(dpi=DPI, clip=clip, colorspace=fitz.csRGB).save(path)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(PDF)
    render(doc[1], CLIP, OUT / "sign_error_raw.png")

    marked = fitz.open(PDF)
    page = marked[1]
    shape = page.new_shape()
    shape.draw_rect(PRODUCT_FORM)
    shape.finish(color=GREEN, width=1.2)
    shape.draw_rect(DET_SUM)
    shape.finish(color=ROSE, width=1.2, fill=ROSE, fill_opacity=0.06)
    shape.draw_oval(PLUS_SIGN)
    shape.finish(color=ROSE, width=1.6)
    shape.commit()
    render(page, CLIP, OUT / "sign_error_marked.png")

    doc[0].get_pixmap(dpi=150, colorspace=fitz.csRGB).save(OUT / "paper_page1.png")
    print("wrote", sorted(p.name for p in OUT.glob("*.png")))


if __name__ == "__main__":
    main()
