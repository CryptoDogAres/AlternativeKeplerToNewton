#!/usr/bin/env python3
import argparse
import datetime as dt
import pathlib
import re
import urllib.error
import urllib.request

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    m = FRONTMATTER_RE.search(text)
    if not m:
        return {}, text
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        fm[k.strip()] = v.strip()
    return fm, text[m.end():]


def render_frontmatter(fm: dict[str, str], body: str) -> str:
    order = [
        "id",
        "title",
        "type",
        "source",
        "verified_url",
        "verified_url_status",
        "verified_url_checked_on",
        "created",
        "updated",
        "one_hop_policy",
    ]
    lines = []
    for k in order:
        if k in fm:
            lines.append(f"{k}: {fm[k]}")
    for k in sorted(fm.keys()):
        if k not in order:
            lines.append(f"{k}: {fm[k]}")
    return "---\n" + "\n".join(lines) + "\n---\n" + body


def try_verify(url: str, timeout: float = 10.0) -> bool:
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return 200 <= resp.status < 400
    except Exception:
        pass

    req = urllib.request.Request(url, method="GET", headers={"Range": "bytes=0-0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return 200 <= resp.status < 400
    except (urllib.error.URLError, ValueError):
        return False


def main() -> int:
    ap = argparse.ArgumentParser(description="Try verifying summary URLs and update verification metadata.")
    ap.add_argument("--root", required=True, help="Project root containing refs/summaries")
    args = ap.parse_args()

    root = pathlib.Path(args.root).resolve()
    summary_dir = root / "refs" / "summaries"
    if not summary_dir.exists():
        print(f"[INFO] Missing directory: {summary_dir}")
        return 0

    today = dt.date.today().isoformat()
    total = 0
    verified = 0
    unverified = 0
    na = 0

    for path in sorted(summary_dir.glob("*.md")):
        if path.name == "INDEX.md":
            continue
        text = path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        if not fm:
            continue

        source = fm.get("source", "none")
        vurl = fm.get("verified_url", "none")
        if (not vurl or vurl == "none") and source.startswith(("http://", "https://")):
            vurl = source
        fm["verified_url"] = vurl if vurl else "none"

        if fm["verified_url"] == "none":
            fm["verified_url_status"] = "not_applicable"
            fm["verified_url_checked_on"] = "n/a"
            na += 1
        else:
            ok = try_verify(fm["verified_url"])
            fm["verified_url_status"] = "verified" if ok else "unverified"
            fm["verified_url_checked_on"] = today
            if ok:
                verified += 1
            else:
                unverified += 1

        path.write_text(render_frontmatter(fm, body), encoding="utf-8")
        total += 1

    print(f"[OK] Processed {total} summary files")
    print(f"[INFO] verified={verified} unverified={unverified} not_applicable={na}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
