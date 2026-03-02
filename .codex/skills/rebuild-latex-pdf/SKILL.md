---
name: rebuild-latex-pdf
description: Rebuild LaTeX PDFs after `.tex` updates with repeated compile verification and failure handling. Use when TeX sources changed, when PDF generation is flaky, when citations or cross-references need extra passes, or when Codex must keep compiling until success or explicit attempt exhaustion.
---

# Rebuild Latex Pdf

## Overview

Use this skill to regenerate a LaTeX PDF whenever `.tex` files are updated and to iterate compilation until the build is stable or the configured attempt limit is reached.

## Workflow

1. Identify the project root and main TeX entry file.
- Default entry file is `main.tex`.

2. Run iterative rebuild after updates.
- Command:
```bash
$CODEX_HOME/skills/rebuild-latex-pdf/scripts/rebuild_pdf.sh \
  --root <project-root> \
  --main <entry-tex> \
  --max-attempts 8 \
  --required-successes 2
```
- This keeps compiling with `latexmk` until either:
  - the PDF is generated and considered stable for `required-successes` consecutive runs, or
  - attempts are exhausted.

3. Run continuous rebuild when the user wants automatic regeneration on file edits.
- Command:
```bash
$CODEX_HOME/skills/rebuild-latex-pdf/scripts/rebuild_pdf.sh \
  --root <project-root> \
  --main <entry-tex> \
  --watch
```
- `--watch` uses `latexmk -pvc` to recompile whenever source files change.

4. Treat completion strictly.
- Report success only if the script exits with status `0`.
- Report failure if attempts are exhausted or if `latexmk` cannot produce a valid PDF.

## Failure Handling

1. On failure, include:
- command used
- number of attempts completed
- final status code
- log path (`<entry>.log`) and PDF path (`<entry>.pdf`)

2. If failure is due to missing packages or source errors, surface the specific error lines from the log and stop claiming build success.

## Notes

- Prefer this script over ad-hoc compile loops to keep behavior consistent.
- Keep the loop bounded by `--max-attempts`; do not retry forever in non-watch mode.
