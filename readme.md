# AlternativeKeplerToNewton

This repository contains a geometry-first manuscript on the Kepler problem in a Principia-style spirit, with modern organization and notation.

## Scope

The paper develops a synthetic treatment of:

- Kepler's laws (especially areal speed and conic orbits)
- Newton's central-force direction and inverse-square law
- Geometric properties of conics (ellipse, hyperbola, parabola, and degenerate limits)
- Auxiliary-circle and affine-map constructions
- Hodograph-style arguments and interpretations

## Repository layout

- `main.tex`: root compile entrypoint (assembles the whole document)
- `tex/preamble/`: package setup and theorem/style configuration
- `tex/frontmatter/`: title block and abstract
- `tex/sections/`: one source file per top-level section
- `tex/backmatter/`: bibliography commands
- `assets/images/`: manuscript figures (`.png`)
- `assets/ggb/`: GeoGebra construction files (`.ggb`)
- `bib/references.bib`: active bibliography database
- `bib/archive/references_2.bib`: archived bibliography file
- `refs/pdf/`: external reference PDFs used during drafting

## Build

From the repository root:

```bash
latexmk -pdf -interaction=nonstopmode -file-line-error main.tex
```

Manual BibTeX sequence is also supported:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```
