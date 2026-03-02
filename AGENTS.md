# AGENTS.md instructions for /Users/changchunshi/codebase/AlternativeKeplerToNewton

## Skills

A skill is a set of local instructions stored in a `SKILL.md` file.

### Available skills

- rebuild-latex-pdf: Rebuild LaTeX PDFs after `.tex` updates with repeated compile verification and failure handling. (file: `/Users/changchunshi/codebase/AlternativeKeplerToNewton/.codex/skills/rebuild-latex-pdf/SKILL.md`)
- reference-curator: Build and maintain per-reference summaries and a unique one-hop reference index in `refs/summaries/`. (file: `/Users/changchunshi/codebase/AlternativeKeplerToNewton/.codex/skills/reference-curator/SKILL.md`)
- proofread-reference-audit: Proofread writing for grammar, factual consistency, and citation correctness, then suggest additional references. (file: `/Users/changchunshi/codebase/AlternativeKeplerToNewton/.codex/skills/proofread-reference-audit/SKILL.md`)

### How to use skills

- Discovery: Use the list above to locate the right skill file for the task.
- Trigger rules: If the user explicitly names a skill (for example `$reference-curator`) or the task clearly matches a listed skill, use that skill for the turn.
- Loading strategy: Read `SKILL.md` first, then load only the needed resource files in that skill (`scripts/`, `references/`, `assets/`).
- Multi-skill requests: Use the minimal set of skills that covers the request.
