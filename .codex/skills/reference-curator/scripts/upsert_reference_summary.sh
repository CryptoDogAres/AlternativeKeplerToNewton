#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  upsert_reference_summary.sh \
    --root <project-root> \
    --ref-id <reference-id> \
    [--title <title>] \
    [--type <paper|book|chapter|web|other>] \
    [--source <path-or-url>] \
    [--verified-url <url>] \
    [--url-status <verified|unverified|not_applicable>] \
    [--hint <hint-text>] \
    [--refresh]

Notes:
- Without --refresh, an existing summary file is kept as-is.
- With --refresh, the summary file is recreated and updated date is refreshed.
- URL verification metadata is always written:
  - verified_url
  - verified_url_status
  - verified_url_checked_on
USAGE
}

ROOT=""
REF_ID=""
TITLE="TBD"
TYPE="other"
SOURCE="TBD"
VERIFIED_URL=""
URL_STATUS=""
HINT="none"
REFRESH=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root)
      ROOT="$2"
      shift 2
      ;;
    --ref-id)
      REF_ID="$2"
      shift 2
      ;;
    --title)
      TITLE="$2"
      shift 2
      ;;
    --type)
      TYPE="$2"
      shift 2
      ;;
    --source)
      SOURCE="$2"
      shift 2
      ;;
    --verified-url)
      VERIFIED_URL="$2"
      shift 2
      ;;
    --url-status)
      URL_STATUS="$2"
      shift 2
      ;;
    --hint)
      HINT="$2"
      shift 2
      ;;
    --refresh)
      REFRESH=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "[ERROR] Unknown argument: $1" >&2
      usage
      exit 2
      ;;
  esac
done

if [[ -z "$ROOT" || -z "$REF_ID" ]]; then
  echo "[ERROR] --root and --ref-id are required" >&2
  usage
  exit 2
fi

if [[ -n "$URL_STATUS" ]]; then
  case "$URL_STATUS" in
    verified|unverified|not_applicable)
      ;;
    *)
      echo "[ERROR] --url-status must be one of: verified, unverified, not_applicable" >&2
      exit 2
      ;;
  esac
fi

slug=$(printf '%s' "$REF_ID" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9._-]+/-/g; s/^-+//; s/-+$//')
if [[ -z "$slug" ]]; then
  echo "[ERROR] ref id '$REF_ID' becomes empty after slug normalization" >&2
  exit 2
fi

summary_dir="$ROOT/refs/summaries"
out_file="$summary_dir/${slug}.md"
now=$(date +%F)

mkdir -p "$summary_dir"

if [[ -f "$out_file" && "$REFRESH" -eq 0 ]]; then
  echo "[INFO] Summary already exists: $out_file"
  echo "[INFO] Use --refresh to recreate it with new hints"
  exit 0
fi

created="$now"
if [[ -f "$out_file" ]]; then
  prior_created=$(awk -F': ' '/^created:/ {print $2; exit}' "$out_file" || true)
  if [[ -n "$prior_created" ]]; then
    created="$prior_created"
  fi
fi

if [[ -z "$VERIFIED_URL" ]]; then
  if [[ "$SOURCE" =~ ^https?:// ]]; then
    VERIFIED_URL="$SOURCE"
  else
    VERIFIED_URL="none"
  fi
fi

if [[ -z "$URL_STATUS" ]]; then
  if [[ "$VERIFIED_URL" == "none" ]]; then
    URL_STATUS="not_applicable"
  else
    # Caller should pass --url-status verified after actively checking.
    URL_STATUS="unverified"
  fi
fi

if [[ "$URL_STATUS" == "not_applicable" ]]; then
  checked_on="n/a"
else
  checked_on="$now"
fi

cat > "$out_file" <<EOF_SUMMARY
---
id: $REF_ID
title: $TITLE
type: $TYPE
source: $SOURCE
verified_url: $VERIFIED_URL
verified_url_status: $URL_STATUS
verified_url_checked_on: $checked_on
created: $created
updated: $now
one_hop_policy: selective
---

# Summary

## High-Level Contribution
TBD

## Relevance to This Project
TBD

## Notes / Evidence
- Scope:
- Method:
- Key claim(s):

## Principia Edition Basis
- Basis in this summary/project:
- Evidence status (verified/unverified):

## One-Hop References
- none recorded yet

## Refresh Hints
$HINT
EOF_SUMMARY

echo "[OK] Wrote summary template: $out_file"
