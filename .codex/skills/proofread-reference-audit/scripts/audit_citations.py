#!/usr/bin/env python3
import argparse
import json
import pathlib
import re

CITE_RE = re.compile(r"\\cite[a-zA-Z*]*\s*(?:\[[^\]]*\]\s*)?(?:\[[^\]]*\]\s*)?\{([^}]*)\}")
BIB_RE = re.compile(r"@[A-Za-z]+\s*\{\s*([^,\s]+)\s*,")


def parse_cites(path: pathlib.Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    keys: list[str] = []
    for m in CITE_RE.finditer(text):
        raw = m.group(1)
        for part in raw.split(","):
            key = part.strip()
            if key:
                keys.append(key)
    return keys


def parse_bib_keys(path: pathlib.Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return [m.group(1).strip() for m in BIB_RE.finditer(text)]


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit TeX citation keys against .bib files.")
    ap.add_argument("--tex", action="append", required=True, help="TeX file path (repeatable)")
    ap.add_argument("--bib", action="append", required=True, help="BibTeX file path (repeatable)")
    ap.add_argument("--json", action="store_true", help="Emit JSON output")
    args = ap.parse_args()

    tex_paths = [pathlib.Path(p).resolve() for p in args.tex]
    bib_paths = [pathlib.Path(p).resolve() for p in args.bib]

    cited: list[str] = []
    for p in tex_paths:
        cited.extend(parse_cites(p))

    bib_keys: list[str] = []
    for p in bib_paths:
        bib_keys.extend(parse_bib_keys(p))

    cited_unique = sorted(set(cited))
    bib_unique = sorted(set(bib_keys))

    cited_set = set(cited_unique)
    bib_set = set(bib_unique)

    missing = sorted(cited_set - bib_set)
    unused = sorted(bib_set - cited_set)

    result = {
        "tex_files": [str(p) for p in tex_paths],
        "bib_files": [str(p) for p in bib_paths],
        "cited_keys_total": len(cited),
        "cited_keys_unique": len(cited_unique),
        "bib_keys_unique": len(bib_unique),
        "missing_in_bib": missing,
        "unused_in_bib": unused,
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"TeX files: {len(tex_paths)}")
        print(f"Bib files: {len(bib_paths)}")
        print(f"Cited keys (total): {result['cited_keys_total']}")
        print(f"Cited keys (unique): {result['cited_keys_unique']}")
        print(f"Bib keys (unique): {result['bib_keys_unique']}")
        print("\nMissing in bibliography:")
        if missing:
            for k in missing:
                print(f"- {k}")
        else:
            print("- none")

        print("\nUnused bibliography keys:")
        if unused:
            for k in unused:
                print(f"- {k}")
        else:
            print("- none")

    return 2 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
