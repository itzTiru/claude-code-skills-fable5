#!/usr/bin/env python3
"""Fable-book build pipeline.

Turns an authored book.html (built on the fable-book design system) into a finished,
iPad-ready PDF: two-pass Chrome render with real ToC page numbers, full-bleed ivory
underlay, footer page numbers, botanical vignettes on pages with empty bottoms,
nested bookmark outline, and metadata.

Usage:
  uv run --with pypdf --with reportlab --with pillow --with numpy \
      python3 build.py <workdir>

<workdir> must contain:
  book.html          authored content on top of assets/design-system.html
  book.config.json   title/author/outline/options (see skill references/components.md)

Produces <workdir>/final.pdf.
"""
import io, json, re, shutil, subprocess, sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from PIL import Image
import numpy as np

SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS = SKILL_DIR / "assets"
CHROME = shutil.which("google-chrome-stable") or shutil.which("chromium") or shutil.which("google-chrome")

IVORY, CORAL, MANILLA, GRAY = "#FAF9F5", "#D97757", "#EBDBBC", "#8C887C"


def render(html: Path, pdf: Path):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", str(html)], capture_output=True, check=True)


def page_count(pdf: Path) -> int:
    info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    return int(re.search(r"Pages:\s+(\d+)", info).group(1))


def extract_pagemap(pdf: Path) -> dict:
    """Read the invisible [[ref]] markers each chapter page carries."""
    pages = {}
    for p in range(1, page_count(pdf) + 1):
        txt = subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), str(pdf), "-"],
                             capture_output=True, text=True).stdout
        for m in re.findall(r"\[\[([a-z0-9]+)\]\]", txt):
            pages.setdefault(m, p)
    return pages


def inject_toc(src: Path, out: Path, pagemap: dict):
    html = src.read_text()
    html = re.sub(r'(<span class="(?:pg|tp-pg)" data-ref="([a-z0-9]+)">)[^<]*(</span>)',
                  lambda m: m.group(1) + str(pagemap.get(m.group(2), "·")) + m.group(3), html)
    out.write_text(html)


def main():
    workdir = Path(sys.argv[1]).resolve()
    cfg = json.loads((workdir / "book.config.json").read_text())
    W = float(cfg.get("page_width_pt", 504.0))
    H = float(cfg.get("page_height_pt", 725.04))

    # the authored HTML references fonts/ relatively; provide them if absent
    if not (workdir / "fonts").exists():
        shutil.copytree(ASSETS / "fonts", workdir / "fonts")

    book = workdir / "book.html"
    final_html = workdir / "book_final.html"
    pass1, pass2 = workdir / "pass1.pdf", workdir / "pass2.pdf"

    # ---- two-pass render until the pagemap is stable ----
    render(book, pass1)
    pagemap = extract_pagemap(pass1)
    for _ in range(4):
        inject_toc(book, final_html, pagemap)
        render(final_html, pass2)
        new_map = extract_pagemap(pass2)
        if new_map == pagemap:
            break
        pagemap = new_map
    (workdir / "pagemap.json").write_text(json.dumps(pagemap))
    n = page_count(pass2)
    print(f"render stable: {n} pages, {len(pagemap)} anchors")

    # ---- find pages with a large empty bottom (vignette candidates) ----
    vignette_on = {}
    if cfg.get("vignettes", True):
        detect = workdir / ".detect"
        shutil.rmtree(detect, ignore_errors=True)
        detect.mkdir()
        dpi = 30
        subprocess.run(["pdftoppm", "-r", str(dpi), "-gray", str(pass2), str(detect / "pg")], check=True)
        pad = len(str(n))
        skip = {1} | {pagemap[r] for r in cfg.get("vignette_skip_refs", []) if r in pagemap}
        vigs = sorted((ASSETS / "vign").glob("v*.png"))
        vi = 0
        for i in range(1, n):
            if i + 1 in skip:
                continue
            img = Image.open(detect / f"pg-{i+1:0{pad}d}.pgm")
            a = np.asarray(img)
            ink = np.where((a < 200).any(axis=1))[0]
            bottom_pt = (float(ink.max()) * 72.0 / dpi) if len(ink) else 0.0
            if bottom_pt < H - 56 - 100 - 30:
                vignette_on[i] = vigs[vi % len(vigs)]
                vi += 1
        print(f"vignettes on {len(vignette_on)} pages")

    # ---- underlay (ivory + cover band) and overlay (page numbers + vignettes) ----
    pdfmetrics.registerFont(TTFont("Archivo", str(ASSETS / "fonts" / "Archivo-Medium.ttf")))
    reader = PdfReader(str(pass2))
    under_buf, over_buf = io.BytesIO(), io.BytesIO()
    uc = canvas.Canvas(under_buf, pagesize=(W, H))
    oc = canvas.Canvas(over_buf, pagesize=(W, H))
    for i in range(n):
        uc.setFillColor(HexColor(IVORY))
        uc.rect(-2, -2, W + 4, H + 4, fill=1, stroke=0)
        if i == 0 and cfg.get("cover_band", True):
            uc.setFillColor(HexColor(CORAL))
            uc.rect(0, H - 11.5, W, 11.5, fill=1, stroke=0)
            uc.setFillColor(HexColor(MANILLA))
            uc.rect(0, H - 14.8, W, 3.3, fill=1, stroke=0)
        uc.showPage()
        if i > 0:
            oc.setFont("Archivo", 8)
            oc.setFillColor(HexColor(GRAY))
            oc.drawCentredString(W / 2, 24, str(i + 1))
        if i in vignette_on:
            img = Image.open(vignette_on[i])
            wpt, hpt = img.width / 3.6, img.height / 3.6
            oc.drawImage(str(vignette_on[i]), (W - wpt) / 2, 58, width=wpt, height=hpt, mask="auto")
        oc.showPage()
    uc.save(); oc.save()
    under = PdfReader(io.BytesIO(under_buf.getvalue()))
    over = PdfReader(io.BytesIO(over_buf.getvalue()))

    writer = PdfWriter()
    for i, page in enumerate(reader.pages):
        page.merge_page(under.pages[i], over=False)
        if i > 0:
            page.merge_page(over.pages[i], over=True)
        writer.add_page(page)

    # ---- nested outline from config ----
    def add(items, parent=None):
        for it in items:
            ref = it.get("ref")
            if ref not in pagemap:
                print(f"warning: outline ref '{ref}' has no page marker, skipped")
                continue
            node = writer.add_outline_item(it["title"], pagemap[ref] - 1, parent=parent)
            add(it.get("children", []), node)
    writer.add_outline_item("Cover", 0)
    add(cfg.get("outline", []))

    writer.add_metadata({
        "/Title": cfg.get("title", ""),
        "/Author": cfg.get("author", ""),
        "/Subject": cfg.get("subject", ""),
        "/Keywords": cfg.get("keywords", ""),
        "/Creator": "fable-book skill (Claude Code, Fable 5)",
    })
    writer.page_mode = "/UseOutlines"

    for page in writer.pages:
        page.compress_content_streams(level=9)
    writer.compress_identical_objects(remove_duplicates=True, remove_unreferenced=True)

    out = workdir / cfg.get("output", "final.pdf")
    with open(out, "wb") as f:
        writer.write(f)
    print(f"{out} written: {n} pages")


if __name__ == "__main__":
    main()
