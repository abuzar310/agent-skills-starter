#!/usr/bin/env bash
set -euo pipefail

DEST="${1:-}"
shift || true

if [[ -z "${DEST}" ]]; then
  echo "Usage: ./scripts/install.sh <destination> [skill-name ...]"
  echo "Example: ./scripts/install.sh ~/.claude/skills copywriting cro seo"
  exit 1
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/skills"

mkdir -p "$DEST"

if [[ "$#" -eq 0 ]]; then
  echo "Installing all skills -> $DEST"
  cp -R "$SRC"/. "$DEST"/
else
  for name in "$@"; do
    if [[ ! -d "$SRC/$name" ]]; then
      echo "Skip (not found): $name"
      continue
    fi
    echo "Install $name"
    rm -rf "$DEST/$name"
    cp -R "$SRC/$name" "$DEST/$name"
  done
fi

echo "Done."
