---
name: gitpush
description: Stage, commit, and push repository changes in one clean flow. Use when the user asks to "check in all changes", include untracked/modified/deleted files in a commit, push to origin, or re-run push to verify remote sync.
---

# Gitpush

Run a reliable git check-in and push flow for the current repository, then report the key result lines.

## Workflow

1. Inspect current branch and changes:
```bash
git status --short --branch
```

2. Stage everything, including untracked files and deletions:
```bash
git add -A
git status --short --branch
```

3. Commit once with a clear message:
- Use a user-provided message when available.
- Use `Check in all pending changes` when no message is provided.
```bash
git commit -m "<message>"
```

4. Push to remote:
```bash
git push
```

5. If user asks to "redo push", run:
```bash
git push
```
Treat `Everything up-to-date` as success and report that explicitly.

## Guardrails

- Do not drop or unstage files unless the user asks.
- Include tracked and untracked files in the same commit when user asks for "all changes".
- If staging or commit fails due permission/sandbox lock errors, request elevated execution and retry.
- If there are no local commits to push, still run `git push` and report the up-to-date result.

## Response Format

- Report commit hash and commit message after commit.
- Report branch push result after `git push` (for example, `main -> main` or `Everything up-to-date`).
- Keep output short and factual.
