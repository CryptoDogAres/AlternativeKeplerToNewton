#!/usr/bin/env bash

set -u
set -o pipefail

ROOT="."
MAIN_TEX="main.tex"
MAX_ATTEMPTS=8
REQUIRED_SUCCESSES=2
WATCH=0

usage() {
  cat <<'USAGE'
Usage:
  rebuild_pdf.sh [--root <dir>] [--main <file.tex>] [--max-attempts <n>] [--required-successes <n>] [--watch]

Options:
  --root <dir>               Project root directory (default: .)
  --main <file.tex>          Main TeX entry file (default: main.tex)
  --max-attempts <n>         Max compile attempts in iterative mode (default: 8)
  --required-successes <n>   Consecutive stable successes required (default: 2)
  --watch                    Continuous rebuild on source updates using latexmk -pvc
  -h, --help                 Show this help
USAGE
}

is_positive_int() {
  [[ "$1" =~ ^[1-9][0-9]*$ ]]
}

log_needs_rerun() {
  local logfile="$1"
  if [[ ! -f "$logfile" ]]; then
    return 0
  fi

  local pattern='Rerun to get cross-references right|Rerun to get citations correct|Label\(s\) may have changed'
  if command -v rg >/dev/null 2>&1; then
    rg -q -i "$pattern" "$logfile"
    return $?
  fi

  grep -Eiq "$pattern" "$logfile"
  return $?
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root)
      ROOT="$2"
      shift 2
      ;;
    --main)
      MAIN_TEX="$2"
      shift 2
      ;;
    --max-attempts)
      MAX_ATTEMPTS="$2"
      shift 2
      ;;
    --required-successes)
      REQUIRED_SUCCESSES="$2"
      shift 2
      ;;
    --watch)
      WATCH=1
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

if ! is_positive_int "$MAX_ATTEMPTS"; then
  echo "[ERROR] --max-attempts must be a positive integer." >&2
  exit 2
fi

if ! is_positive_int "$REQUIRED_SUCCESSES"; then
  echo "[ERROR] --required-successes must be a positive integer." >&2
  exit 2
fi

if ! command -v latexmk >/dev/null 2>&1; then
  echo "[ERROR] latexmk is not installed or not in PATH." >&2
  exit 2
fi

if ! cd "$ROOT"; then
  echo "[ERROR] Cannot access project root: $ROOT" >&2
  exit 2
fi

ROOT_ABS="$(pwd)"

if [[ ! -f "$MAIN_TEX" ]]; then
  echo "[ERROR] Main TeX file not found: $ROOT_ABS/$MAIN_TEX" >&2
  exit 2
fi

BASE_NAME="${MAIN_TEX%.tex}"
PDF_FILE="${BASE_NAME}.pdf"
LOG_FILE="${BASE_NAME}.log"

if [[ "$WATCH" -eq 1 ]]; then
  echo "[INFO] Watch mode enabled. Rebuilding on file updates..."
  exec latexmk -pdf -pvc -interaction=nonstopmode -halt-on-error -file-line-error "$MAIN_TEX"
fi

attempt=1
stable_successes=0
last_exit=0

while [[ "$attempt" -le "$MAX_ATTEMPTS" ]]; do
  echo "[INFO] Attempt $attempt/$MAX_ATTEMPTS: compiling $MAIN_TEX"
  latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error "$MAIN_TEX"
  last_exit=$?

  if [[ "$last_exit" -ne 0 ]]; then
    stable_successes=0
    echo "[WARN] latexmk failed on attempt $attempt (exit $last_exit)."
    attempt=$((attempt + 1))
    continue
  fi

  if [[ ! -s "$PDF_FILE" ]]; then
    stable_successes=0
    echo "[WARN] Build completed but PDF is missing or empty: $ROOT_ABS/$PDF_FILE"
    attempt=$((attempt + 1))
    continue
  fi

  if log_needs_rerun "$LOG_FILE"; then
    stable_successes=0
    echo "[INFO] Log requests another pass (citations/cross-references not stable yet)."
    attempt=$((attempt + 1))
    continue
  fi

  stable_successes=$((stable_successes + 1))
  echo "[INFO] Stable success count: $stable_successes/$REQUIRED_SUCCESSES"

  if [[ "$stable_successes" -ge "$REQUIRED_SUCCESSES" ]]; then
    echo "[OK] PDF build stable: $ROOT_ABS/$PDF_FILE"
    echo "[OK] Log file: $ROOT_ABS/$LOG_FILE"
    exit 0
  fi

  attempt=$((attempt + 1))
done

echo "[ERROR] Failed to reach stable PDF generation after $MAX_ATTEMPTS attempts."
echo "[ERROR] Last latexmk exit code: $last_exit"
if [[ -f "$LOG_FILE" ]]; then
  echo "[ERROR] Last 40 lines of log ($ROOT_ABS/$LOG_FILE):"
  tail -n 40 "$LOG_FILE"
else
  echo "[ERROR] Log file not found: $ROOT_ABS/$LOG_FILE"
fi

exit 1
