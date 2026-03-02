---
name: reference-curator
description: Build and maintain per-source reference summaries plus a unique one-hop reference index. Use when adding a new paper/book/web source, refreshing a source summary with new hints, curating references-of-references without recursive expansion, or updating shared reference notes in refs/summaries.
---

# Reference Curator

Maintain a concise, reusable knowledge base for references in this project.

## Workflow

1. Identify the source to summarize.
- Collect a stable reference id (BibTeX key if available), title, source path/URL, and type (`paper`, `book`, `chapter`, `web`, `other`).
- If a URL exists, always try to verify it (open/retrieve the URL). Record verification metadata in frontmatter:
  - `verified_url`
  - `verified_url_status` (`verified`, `unverified`, or `not_applicable`)
  - `verified_url_checked_on`

2. Create or refresh the per-reference summary file.
- Run:
```bash
scripts/upsert_reference_summary.sh \
  --root <project-root> \
  --ref-id <reference-id> \
  --title "<title>" \
  --type <paper|book|chapter|web|other> \
  --source "<path-or-url>" \
  --verified-url "<verified-url-if-known>" \
  --url-status <verified|unverified|not_applicable>
```
- If the user asks to re-summarize with new guidance, rerun with `--refresh --hint "<prompt hint>"` and overwrite the old summary content.
- If verification is blocked (network/restrictions), keep the best candidate URL but mark it `unverified` and explain why in `## Notes / Evidence`.
- To actively verify all known summary URLs, run:
```bash
scripts/verify_summary_urls.py --root <project-root>
```

3. Fill the summary content.
- Edit `refs/summaries/<reference-id>.md` and keep these sections:
  - `## High-Level Contribution`
  - `## Relevance to This Project`
  - `## Notes / Evidence`
  - `## Principia Edition Basis`
  - `## One-Hop References`
- Keep contribution summary high-level and project-relevant.
- Keep URL verification metadata accurate whenever new evidence is available.

4. Maintain one-hop references only.
- In `## One-Hop References`, use one line per reference:
  - `- <ref-id> | <title> | <type> | <why relevant>`
- Add only direct references cited by the source itself (one indirection).
- Do not expand references of those references.
- Be selective for large bibliographies (especially books). Keep only the references most relevant to this project.

5. Rebuild the shared unique index.
- Run:
```bash
scripts/rebuild_one_hop_index.py --root <project-root>
```
- This regenerates `refs/summaries/INDEX.md` with:
  - known summaries
  - unique one-hop references and where they were seen

## Resource Files

- Template: `references/summary-template.md`
- Selection policy: `references/one-hop-policy.md`
- Summary scaffolder: `scripts/upsert_reference_summary.sh`
- URL verifier: `scripts/verify_summary_urls.py`
- Index builder: `scripts/rebuild_one_hop_index.py`
