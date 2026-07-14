---
name: fable-book
description: Use when asked to turn a PDF, Markdown, HTML, or text source into a beautiful iPad-readable book or "fable book", to restyle a document in the Anthropic/Fable theme (warm ivory, coral, serif), or to make a long technical document "extremely readable" as a PDF for tablet reading.
---

# Fable Book

Produce a print-quality PDF book in the Anthropic Fable design language: warm ivory
paper, book-cloth coral accents, Source Serif 4 + Archivo + JetBrains Mono, tappable
table of contents, nested bookmarks, exotic butterfly cover art, and botanical
vignettes on pages with room to spare. Pages are 504 × 725 pt, the exact iPad Air 11"
aspect ratio, so the book fills the screen with no letterboxing.

The output is not a conversion; it is a re-authored book. You read the source, then
write structured HTML on top of the bundled design system.

## Requirements

Chrome or Chromium headless, `pdftotext`/`pdftoppm`/`pdfinfo` (poppler), `uv`, and the
JetBrains Mono font installed (falls back to any mono otherwise). Fonts for the theme
are bundled in `assets/fonts/`.

## Workflow

1. **Extract the source.** PDFs: `pdftotext -layout src.pdf`. Markdown/HTML: read
   directly. Understand the full content before structuring; never drop content
   silently.
2. **Plan the book.** Chapters, parts, front matter, appendices. Decide which prose
   becomes callouts, tables, formulas, code blocks, and figures. For long sources,
   keep the author's structure; for loose notes, impose one.
3. **Author `book.html`** in a work directory: concatenate
   `assets/design-system.html`, your body sections, then `</body></html>`. Replace
   `{{TITLE}}`. The HTML references `fonts/fonts.css` relatively; build.py copies the
   bundled fonts into the workdir automatically, so do not vendor them yourself. Use ONLY the markup patterns in `references/components.md`; that file
   is the contract. Every page-starting element needs an `id` plus a `[[id]]` pgmark
   marker, and the ToC uses `data-ref` placeholders.
4. **Write `book.config.json`** (schema at the end of components.md): title, author,
   metadata, and the nested outline whose refs match your pgmark ids.
5. **Build:**
   `uv run --with pypdf --with reportlab --with pillow --with numpy python3 scripts/build.py <workdir>`
   The script renders twice through Chrome (real ToC page numbers), stamps the ivory
   underlay and cover band, detects pages with empty bottoms and adds plant-and-
   butterfly vignettes, then writes page numbers, bookmarks, and metadata into
   `final.pdf`.
6. **Visual QA, always.** Render pages with `pdftoppm -png -r 120` and LOOK at them:
   cover, ToC, one chapter opener, every figure, one table-heavy page, the closing
   page. Fix and rebuild until clean. Common defects: SVG text clipped at a viewBox
   edge, a table splitting awkwardly, a butterfly overlapping text.
7. **Deliver** the PDF next to the source, named after the book title in kebab-case
   (or the name the user asked for). Keep the workdir if the user may iterate.

## Design rules

- Follow the palette and type roles in the design system; do not invent new colors.
  Chart series colors: coral `#D97757` first, teal `#0B9678` second (both validated
  for colorblind contrast on ivory).
- Figures are hand-drawn-style inline SVG: 1.3 px ink strokes, rounded corners,
  manilla/ivory fills, coral accents, Archivo caps labels.
- Prose style: no em dashes, ever. Use commas, colons, or semicolons.
- The cover credit reads "Prepared for NAME · by Claude Fable 5".
- Butterflies and vignettes decorate; they never overlap or crowd text.

## Gotchas (each cost a debugging round once)

- Chrome does not paint backgrounds into `@page` margins; the ivory full-bleed comes
  from the build script's underlay stamp. Do not fight it in CSS.
- URLs inside `fonts/fonts.css` are relative to that CSS file, not the HTML.
- pgmark markers must be the visible-ish 2.5pt paper-colored spans the design system
  defines; at 1pt Chrome drops glyphs and page mapping silently fails.
- Internal `#anchor` links survive Chrome print-to-pdf as tappable PDF links; the
  outline and ToC depend on them.
- `break-inside: avoid` is already set on notes, figures, and code; do not wrap
  whole chapters in it or pagination degrades.
- A pagination-affecting edit requires a full rebuild; ToC numbers and vignette
  placement both depend on the final layout.

## Layout of this skill

- `assets/design-system.html`: CSS tokens, all components, spark + butterfly SVG defs
- `assets/fonts/`, `assets/vign/`: bundled fonts and six vignette PNGs
- `scripts/build.py`: the whole pipeline (render, ToC, underlay, vignettes, outline)
- `references/components.md`: copy-paste markup for every component + config schema
