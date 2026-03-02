---
name: proofread-reference-audit
description: Proofread scientific writing for grammar, factual consistency, and citation correctness. Use when revising TeX/Markdown drafts, checking whether cited claims match references, validating citation keys against bibliography files, and proposing additional references (preferably from refs/summaries one-hop records).
---

# Proofread Reference Audit

Run a focused editorial and reference-integrity pass on project text.

## Workflow

1. Define scope.
- Work on files requested by the user (for example `tex/sections/*.tex`).
- Keep edits minimal and preserve technical meaning.

2. Proofread language.
- Correct grammar, wording, punctuation, and clarity.
- Preserve domain terms and historical naming conventions.

3. Check factual consistency.
- Flag claims that are likely incorrect, unsupported, or overstated.
- Prefer conservative rewrites when certainty is limited.

4. Audit citation correctness.
- Run:
```bash
scripts/audit_citations.py --tex <tex-file> --bib <bib-file>
```
- Fix missing/invalid citation keys when evidence is available.
- Identify statements that need citations and mismatches between claim and cited source.

5. Suggest new references.
- Review `refs/summaries/INDEX.md` and one-hop entries in relevant summary files.
- Propose a short list of additional references, prioritizing one-hop sources not yet cited.
- Explain each suggestion in one line (what gap it fills).

## Output Requirements

- Report edits and citation fixes with file paths.
- Report unresolved fact-check uncertainties explicitly.
- End with suggested references, emphasizing one-hop candidates.

## Resource Files

- Citation audit helper: `scripts/audit_citations.py`
- Proofread checklist: `references/proofread-checklist.md`
