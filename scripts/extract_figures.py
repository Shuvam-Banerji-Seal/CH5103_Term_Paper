"""Extract the figures/schemes of the review as 300-dpi PNGs and write a JSONL index of captions.

Usage:  python -I scripts/extract_figures.py [--pdf paper/....pdf] [--out assets]

Each figure is rendered from its region of the PDF page (so vector labels drawn over the raster
images are included); captions are read verbatim from the PDF text layer.
"""
import argparse
import json
import pathlib
import re

import fitz  # PyMuPDF

# name: (1-based PDF page, bounding box in PDF points [x0, y0, x1, y1]) — from page.get_image_info()
FIGURES = {
    "fig01_two_electron_determinants": (2, [325, 71, 536, 150]),
    "fig02_state_energies_H2_ethylene_TM": (3, [49, 512, 526, 685]),
    "scheme01_dynamic_spin_polarization": (4, [140, 648, 225, 697]),
    "fig03_high_low_spin_polyradicals": (5, [50, 478, 277, 686]),
    "fig04_topology_driven_multiplicity": (5, [298, 507, 525, 676]),
    "fig05_tropylidene_orbitals": (6, [69, 71, 296, 261]),
    "fig06_ionic_resonance_spin_reversal": (6, [75, 318, 289, 515]),
    "fig07_spin_crossover_external_stimuli": (7, [117, 71, 458, 549]),
    "fig08_borderline_triplet_closed_shell": (8, [83, 71, 282, 279]),
    "fig09_protonation_induced_magnetization": (8, [68, 335, 545, 697]),
    "fig10_aufbau_vs_non_aufbau": (10, [69, 71, 296, 239]),
    "scheme02_VO_oep": (10, [374, 71, 487, 175]),
    "fig11_tempo_dithiolate_non_aufbau": (11, [49, 71, 526, 450]),
    "fig12_nitronyl_nitroxide_donors": (11, [50, 498, 277, 639]),
    "scheme03_donor_HOMO_spin_polarization": (11, [312, 498, 512, 610]),
    "fig13_disjoint_nondisjoint_orbital_conversion": (12, [68, 71, 545, 266]),
    "fig14_oxidation_induced_ferromagnetic_coupling": (12, [68, 309, 545, 575]),
    "fig15_donors_other_radicals": (13, [300, 402, 523, 686]),
    "scheme04_conductivity_magnetism": (13, [50, 475, 277, 552]),
    "scheme05_conducting_magnets_ETBN_ESBN": (13, [50, 611, 277, 686]),
    "fig16_distonic_radical_anions": (14, [136, 71, 477, 565]),
    "fig17_non_aufbau_by_electron_addition": (15, [117, 71, 458, 255]),
}
# Scheme 1's caption is not laid out as a separate "SCHEME 1 |" text block in the PDF.
MANUAL_CAPTIONS = {("Scheme", 1): (4, "Dynamic spin polarization.")}
FIRST_JOURNAL_PAGE = 440


def captions(doc):
    found = dict(MANUAL_CAPTIONS)
    for i, page in enumerate(doc):
        for block in page.get_text("blocks"):
            text = re.sub(r"\s+", " ", block[4]).strip()
            m = re.match(r"^(F ?I ?G ?U ?R ?E|S ?C ?H ?E ?M ?E)\s*(\d+)\s*\|\s*(.*)", text)
            if m:
                kind = "Figure" if m.group(1).replace(" ", "") == "FIGURE" else "Scheme"
                found[(kind, int(m.group(2)))] = (i + 1, m.group(3).replace("high- spin", "high-spin"))
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", default="paper/Uncommon_Molecular_Electronic_Configuration.pdf")
    ap.add_argument("--out", default="assets")
    ap.add_argument("--dpi", type=int, default=300)
    args = ap.parse_args()

    out = pathlib.Path(args.out)
    (out / "figures").mkdir(parents=True, exist_ok=True)
    doc = fitz.open(args.pdf)
    caps = captions(doc)
    rows = []
    for name, (page, bbox) in FIGURES.items():
        rect = fitz.Rect(bbox[0] - 3, bbox[1] - 3, bbox[2] + 3, bbox[3] + 3)
        pix = doc[page - 1].get_pixmap(dpi=args.dpi, clip=rect, colorspace=fitz.csRGB)
        pix.save(out / "figures" / f"{name}.png")
        kind = "Figure" if name.startswith("fig") else "Scheme"
        num = int(re.search(r"\d+", name).group())
        cap_page, cap = caps[(kind, num)]
        rows.append({"id": f"{kind.lower()}{num}", "label": f"{kind} {num}", "number": num,
                     "type": kind.lower(), "file": f"figures/{name}.png",
                     "journal_page": FIRST_JOURNAL_PAGE - 1 + cap_page, "pdf_page": cap_page,
                     "caption": cap})
    rows.sort(key=lambda r: (r["type"] != "figure", r["number"]))
    (out / "figures.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    print(f"wrote {len(rows)} figures to {out / 'figures'} and {out / 'figures.jsonl'}")


if __name__ == "__main__":
    main()
