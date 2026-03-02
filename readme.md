# AlternativeKeplerToNewton

This repository contains a geometry-first manuscript on the Kepler problem in a Principia-style spirit, with modern organization and notation.

## Scope

The paper develops a synthetic treatment of:

- Kepler's laws (especially areal speed and conic orbits)
- Newton's central-force direction and inverse-square law
- Geometric properties of conics (ellipse, hyperbola, parabola, and degenerate limits)
- Auxiliary-circle and affine-map constructions
- Hodograph-style arguments and interpretations

## Current manuscript map

Main entrypoint:

- `main.tex`: includes frontmatter and sections in compile order.

Section files currently used by `main.tex`:

- `tex/sections/00-abstract.tex`
- `tex/sections/01-introduction.tex`
- `tex/sections/02-setup-and-assumptions.tex`
- `tex/sections/03-auxiliary-circle-and-affine-map.tex`
- `tex/sections/04-alternative-auxiliary-circle-proof.tex`
- `tex/sections/05-other-conic-sections.tex`
- `tex/sections/06-forward-problem-hodograph.tex` (Forward Proof `1F`)
- `tex/sections/07-forward-problem-proof2F.tex` (Forward Proof `2F`, variants `2F'`)
- `tex/sections/08-summary-and-future-work.tex`

Supporting files:

- `main.tex`: root compile entrypoint (assembles the whole document)
- `tex/preamble/`: package setup and theorem/style configuration
- `tex/frontmatter/`: title block and abstract
- `tex/backmatter/`: bibliography commands
- `assets/images/`: manuscript figures (`.png`)
- `assets/ggb/`: GeoGebra construction files (`.ggb`)
- `bib/references.bib`: active bibliography database
- `bib/archive/references_2.bib`: archived bibliography file
- `refs/pdf/`: external reference PDFs used during drafting
- `refs/summaries/`: per-reference summaries and one-hop reference index
- `.codex/skills/`: project-local Codex skills used for maintenance workflows

## Build and iteration process

Recommended workflow from repo root:

1. Edit target section files in `tex/sections/`.
2. Rebuild PDF.
3. Review `main.pdf`.
4. Repeat.

### Makefile commands

This repository includes a `Makefile`:

- `make pdf` (or `make`): force a full PDF build via `latexmk`.
- `make watch`: continuous rebuild on file changes (`latexmk -pvc`, no viewer).
- `make clean`: remove generated build artifacts (`latexmk -C`).

### Direct latexmk command

If you prefer not to use `make`:

```bash
latexmk -pdf -interaction=nonstopmode -file-line-error main.tex
```

Manual BibTeX sequence is supported:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

If LaTeX/BibTeX state gets inconsistent, run `make clean` and rebuild with `make pdf`.

## Project skills

This project ships with local Codex skills in `.codex/skills/`:

- `rebuild-latex-pdf`: iterative LaTeX build/rebuild workflow with stability checks.
- `reference-curator`: maintain per-reference summaries and a unique one-hop references index in `refs/summaries/`.
- `proofread-reference-audit`: proofread grammar/facts/citations and suggest additional references (prioritizing one-hop candidates).

## Known limitations / open issues

1. Some `.ggb` constructions are not fully constrained for full proof-level motion. When movable objects (for example points `A` or `V`) are dragged, dependent geometry may fail to follow correctly.
2. Despite item 1, the current static GeoGebra views and exported `.png` figures are reliable for manuscript use.
3. Some `.ggb` files may not render optimally on black-and-white printers. A future polish pass should normalize visual settings (for example, set label opacity to `1` and improve contrast consistently).
4. Section 3 may be extendable to hyperbola and parabola with the same general strategy; this is not fully developed yet.
5. The rotation-direction convention between hodograph and geometric proxy can be explained more explicitly for clarity.
6. The circular-nature explanation involving the LRL-vector connection can be presented more naturally in this manuscript, instead of leaning on external exposition.
7. A direct Binet-equation explanation from the manuscript's discrete interpretation is still missing and would improve cohesion.
8. Figure 2 is less visually explicit than Figure 1 (Newton's construction). The current construction is correct in the limit/tangent sense, but the diagram can be made more self-evident.
9. Historically, a denser geometric plotting style may improve modern readability, while Newton's original compression was likely constrained by presentation technology of his time.

## Acknowledgment note

The project is motivated by deep appreciation for the geometric tradition across generations, including Euclid, Galileo, Kepler, Apollonius, Newton, Leibniz, Cauchy, Hamilton, Maxwell, Feynman, Bernoulli, and modern contributors such as the Goodsteins, Chandrasekhar, Markowsky, Derbes, van Haandel--Heckman (vHH), Carinena, Ranada, Santander (CRS), and many others.

This study was specifically motivated by working on geometric approaches and their generalization, especially ellipse properties, the auxiliary circle, and related identities. Those geometric structures led to a deeper reading of Newton's \emph{Principia} treatment of space-time Euclidean geometry, and then to possible new exploration routes in both inverse and forward problems. The manuscript is intended as a useful read for audiences interested in pedagogical accounts of science, geometry, and classical mechanics.
