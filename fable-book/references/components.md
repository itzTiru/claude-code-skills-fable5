# Fable-book markup cookbook

Every book is `assets/design-system.html` + your body sections + `</body></html>`.
The design system already defines all CSS tokens/classes and the SVG defs
(`#spark`, butterflies `#b1`..`#b7`, `#specimen` shadow filter). Copy these snippets
verbatim and fill in content.

## Page anchors (required on every chapter/section page)

Every page-starting element needs an `id` (for links) and an invisible `pgmark`
marker (for page mapping). Marker text is `[[` + the id + `]]`, lowercase letters
and digits only.

```html
<div class="page" id="c01"><span class="pgmark">[[c01]]</span>
  ...
</div>
```

`.page` starts a new printed page. `.part` (below) does too.

## Chapter opener

```html
<div class="page" id="c01"><span class="pgmark">[[c01]]</span>
  <div class="eyebrow"><span>Chapter 1</span><span class="sep">·</span><span style="color:var(--ink-3)">Part name</span></div>
  <h2 class="ch">Chapter title</h2>
  <div class="ch-rule"></div>
  <p>Lead paragraph...</p>
</div>
```

Subheads inside a chapter: `<h3>` (serif) and `<h4>` (small caps label).

## Part opener (full page)

```html
<div class="part" id="p1"><span class="pgmark">[[pone]]</span>
  <div class="pnum"><svg width="11" height="11" viewBox="0 0 100 100" style="color:var(--coral)"><use href="#spark"/></svg>Part I</div>
  <h1>Part title</h1>
  <div class="pdesc">One italic sentence describing the part.</div>
  <div class="plist">
    <a href="#c01"><span class="n">01</span><span>Chapter title</span></a>
  </div>
  <div class="motif"><!-- optional small footer SVG --></div>
</div>
```

Caution: part markers extract more reliably with letter-only ids (pone, ptwo...).

## Table of contents (tappable, real page numbers)

Page numbers are injected by build.py into `data-ref` spans. Use `·` as the
placeholder text.

```html
<div class="toc-part"><a href="#p1" style="color:inherit">Part I · Name</a><span class="tp-pg" data-ref="pone">·</span></div>
<div class="toc-line"><span class="n">1</span><a class="t" href="#c01">Chapter title</a><span class="dots"></span><span class="pg" data-ref="c01">·</span></div>
```

## Callout notes

```html
<div class="note">
  <div class="nt"><svg width="10" height="10" viewBox="0 0 100 100" style="color:var(--coral)"><use href="#spark"/></svg>Label in caps</div>
  <p>Body text.</p>
</div>
```

Key-idea variant (manilla wash): `<div class="note key">` with icon color
`var(--crail)`.

## Formulas and code

```html
<div class="formula">bytes = B × T × L × 2 × H_kv × d_h × s
<b>highlighted line</b></div>

<div class="codewrap">
  <div class="codehead"><span class="dot"></span>Snippet label</div>
  <pre class="code"><span class="k">def</span> f():  <span class="c"># comment</span>
    <span class="k">return</span> <span class="s">"string"</span></pre>
</div>
```

Formula/code blocks preserve whitespace; never indent their inner lines to match
the surrounding HTML.

## Tables

```html
<table class="tbl">          <!-- add class "dense" for smaller text -->
  <tr><th style="width:22%">Col</th><th>Col</th></tr>
  <tr><td class="lead">Bold lead cell</td><td>Body</td></tr>
</table>
```

Numeric columns: `class="num"` on th/td. Inline mono: `<span class="m">x</span>`.

## Lists

```html
<ul class="b"><li>Coral-dash bullets.</li></ul>
<ol class="steps"><li>Numbered coral circles.</li></ol>
```

## Figures (inline SVG in the house style)

```html
<div class="fig">
  <div class="figtitle">Caps label with trailing rule</div>
  <svg viewBox="0 0 520 160" width="100%"><!-- 1.3px ink strokes, rounded rects,
    fills #F4F1E9 / #EBDBBC / coral #D97757 at 0.16 opacity, Archivo caps labels --></svg>
  <div class="figcap">Italic caption.</div>
</div>
```

Keep every SVG element inside the viewBox; text near edges clips in print.

## Cover skeleton

```html
<div class="cover">
  <div class="cover-eyebrow"><svg width="13" height="13" viewBox="0 0 100 100" style="color:var(--coral)"><use href="#spark"/></svg>Eyebrow · Label</div>
  <h1>Title</h1>
  <div class="sub">Subtitle</div>
  <div class="desc">Italic description.</div>
  <div style="flex:1;display:flex;align-items:center;justify-content:center;min-height:0">
    <svg viewBox="0 0 400 220" style="width:100%">
      <g filter="url(#specimen)">
        <use href="#b1" transform="translate(216,108) rotate(4) scale(1.08)"/>
        <!-- compose a loose kettle from #b1..#b7; keep every wing inside the viewBox -->
      </g>
    </svg>
  </div>
  <div class="coverart"><!-- optional subject motif strip --></div>
  <div class="foot">
    <div class="who">Prepared for NAME <span>· by Claude Fable 5</span></div>
    <div class="ed">Month Year</div>
  </div>
</div>
```

The coral top band is stamped by build.py (config `cover_band`), not drawn in HTML.

## Butterfly library

`#b1` Papilio blumei (emerald swallowtail), `#b2` Papilio demoleus, `#b3` Cymothoe
sangaris, `#b4` Morpho peleides, `#b5` Phoebis philea, `#b6` Daphnis nerii hawk-moth,
`#b7` Vanessa cardui. Wingspans are roughly 130 units; always wrap uses in
`<g filter="url(#specimen)">` for the cut-out shadow.

## book.config.json

```json
{
  "title": "Book title",
  "author": "Claude Fable 5 · prepared for NAME",
  "subject": "One line",
  "keywords": "comma, separated",
  "output": "final.pdf",
  "cover_band": true,
  "vignettes": true,
  "vignette_skip_refs": ["toc"],
  "outline": [
    {"title": "Front matter", "ref": "fm", "children": [
      {"title": "Contents", "ref": "toc"}
    ]},
    {"title": "Part I · Name", "ref": "pone", "children": [
      {"title": "1. Chapter title", "ref": "c01"}
    ]}
  ]
}
```

Every outline ref must match a pgmark id. `vignette_skip_refs` lists pages that
must never receive a botanical tailpiece (ToC pages usually).
