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

2. Stage everything, including untracked files and deletions (unless user explicitly requests a subset):
```bash
git add -A
git status --short --branch
```

3. Confirm exactly what will be committed:
```bash
git diff --cached --name-status
```
- If this list is empty, do not create an empty commit.
- If user requested "all changes", ensure no intended file is missing before commit.

4. Commit once with a clear message:
- Use a user-provided message when available.
- Use `Check in all pending changes` when no message is provided.
```bash
git commit -m "<message>"
```

5. Push to remote:
```bash
git push
```

6. Verify remote sync and detect leftover local changes:
```bash
git status --short --branch
```
- If branch is ahead, behind, or diverged, call that out explicitly.
- If files are still staged/unstaged/untracked, report that they are not pushed yet.

7. If user asks to "redo push", run:
```bash
git push
```
Treat `Everything up-to-date` as success and report that explicitly.

## Guardrails

- Do not drop or unstage files unless the user asks.
- Include tracked and untracked files in the same commit when user asks for "all changes".
- If staging or commit fails due permission/sandbox lock errors, request elevated execution and retry.
- If commit is blocked by README guard, either stage README per policy or use `SKIP_README_CHECK=1` only when user confirms bypass intent.
- If there are no local commits to push, still run `git push` and report the up-to-date result.
- Always state that Git pushes commits, not working-tree changes.

## Response Format

- Report commit hash and commit message after commit.
- Report branch push result after `git push` (for example, `main -> main` or `Everything up-to-date`).
- Report post-push `git status --short --branch` in one line.
- If any files remain local after push, list them as "not pushed yet".
- Keep output short and factual.
