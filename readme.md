# AlternativeKeplerToNewton

This repository contains a full geometric manuscript on the Kepler problem in a Principia-style spirit, with modern organization and notation.

## Scope

The paper develops a geometry-first treatment of:

- Kepler's laws (especially area law and conic orbits)
- Newton's central-force direction and inverse-square law
- Geometric properties of conics (ellipse, hyperbola, parabola, and degenerate limits)
- Auxiliary-circle and affine-map constructions
- Hodograph-style arguments and interpretations

The emphasis is synthetic geometry and explicit constructions rather than differential-equation-driven derivations.

## Main claims of the manuscript

- From constant areal speed, the force/acceleration direction is central.
- From conic geometry (with focus at the force center), the acceleration magnitude follows an inverse-square dependence.
- The same geometric framework extends to non-elliptic conics and connects naturally to hodograph viewpoints.

## Repository layout

- `main.tex`: main manuscript source
- `references.bib`, `references_2.bib`: bibliography sources
- `*.png`: figures used in the manuscript
- `*.ggb`: GeoGebra construction files
- `reference/`: reference PDFs used during development

## Build

From the repository root:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

If your LaTeX setup supports it, `latexmk -pdf main.tex` is also fine.
