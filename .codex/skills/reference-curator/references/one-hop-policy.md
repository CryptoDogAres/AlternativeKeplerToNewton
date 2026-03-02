# One-Hop Policy

Use this policy when filling `## One-Hop References` in each summary file.

## Scope

- Include only references directly cited by the summarized source.
- Stop at one indirection. Do not expand references of references.

## Relevance Filter

- Keep only references that help this repository's mathematical or historical argument.
- Prefer primary sources, standard reconstructions, and directly comparable proofs.

## Size Guardrails

- Paper/chapter with compact bibliography: usually keep up to 15 one-hop references.
- Book/monograph with expansive bibliography: keep a selective subset (typically 8-12).
- If many references are skipped, mention that selection was intentional in `## Notes / Evidence`.

## Formatting

- Write one reference per line in this exact format:
  - `- <ref-id> | <title> | <type> | <why relevant>`
