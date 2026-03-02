#!/usr/bin/env python3
import argparse
import datetime as dt
import pathlib
import re
from collections import defaultdict

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def parse_frontmatter(text: str) -> dict[str, str]:
    m = FRONTMATTER_RE.search(text)
    if not m:
        return {}
    out: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        out[k.strip()] = v.strip()
    return out


def parse_one_hop_lines(text: str) -> list[tuple[str, str, str, str]]:
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == "## One-Hop References":
            start = i + 1
            break
    if start is None:
        return []

    records: list[tuple[str, str, str, str]] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        s = line.strip()
        if not s.startswith("- "):
            continue
        payload = s[2:].strip()
        parts = [p.strip() for p in payload.split("|", 3)]
        if len(parts) < 4:
            continue
        ref_id, title, ref_type, note = parts
        if not ref_id:
            continue
        records.append((ref_id, title, ref_type, note))
    return records


def render_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(row) + " |")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Rebuild refs/summaries/INDEX.md from one-hop lines in summary files.")
    ap.add_argument("--root", required=True, help="Project root that contains refs/summaries")
    args = ap.parse_args()

    root = pathlib.Path(args.root).resolve()
    summary_dir = root / "refs" / "summaries"
    summary_dir.mkdir(parents=True, exist_ok=True)

    summary_files = sorted(
        p for p in summary_dir.glob("*.md")
        if p.name != "INDEX.md" and not p.name.startswith("_")
    )

    summary_rows: list[list[str]] = []
    one_hop_map: dict[str, dict[str, object]] = {}
    cited_by: dict[str, set[str]] = defaultdict(set)

    for path in summary_files:
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        sid = fm.get("id", path.stem)
        title = fm.get("title", "")
        stype = fm.get("type", "")
        updated = fm.get("updated", "")
        source = fm.get("source", "")
        verified_url = fm.get("verified_url", "")
        verified_url_status = fm.get("verified_url_status", "")

        summary_rows.append([sid, title, stype, updated, source, verified_url, verified_url_status, path.name])

        for ref_id, ref_title, ref_type, note in parse_one_hop_lines(text):
            k = ref_id.strip().lower()
            if k not in one_hop_map:
                one_hop_map[k] = {
                    "ref_id": ref_id.strip(),
                    "title": ref_title.strip(),
                    "type": ref_type.strip(),
                    "note": note.strip(),
                }
            cited_by[k].add(sid)

    one_hop_rows: list[list[str]] = []
    for k in sorted(one_hop_map.keys()):
        item = one_hop_map[k]
        one_hop_rows.append([
            str(item["ref_id"]),
            str(item["title"]),
            str(item["type"]),
            ", ".join(sorted(cited_by[k])),
        ])

    today = dt.date.today().isoformat()
    out_lines: list[str] = [
        "# Reference Summary Index",
        "",
        f"Generated: {today}",
        "",
        "## Summary Files",
        "",
    ]

    if summary_rows:
        out_lines.extend(
            render_table(
                ["id", "title", "type", "updated", "source", "verified_url", "url_status", "file"],
                summary_rows,
            )
        )
    else:
        out_lines.append("No summary files yet.")

    out_lines.extend(["", "## Unique One-Hop References", ""])
    if one_hop_rows:
        out_lines.extend(render_table(["ref-id", "title", "type", "cited-by"], one_hop_rows))
    else:
        out_lines.append("No one-hop references recorded yet.")

    out_lines.extend([
        "",
        "## Rules",
        "",
        "- Keep only one-hop references (do not recurse).",
        "- Keep book reference extraction selective and project-focused.",
    ])

    out_path = summary_dir / "INDEX.md"
    out_path.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    print(f"[OK] Wrote {out_path}")
    print(f"[INFO] Processed {len(summary_files)} summary file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
