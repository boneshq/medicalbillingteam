#!/usr/bin/env bash
# Pull copywriter output into the build. Filenames must equal page keys (see _build/src/pages.py; home = index.md).
set -euo pipefail
SRC="${1:-/workspace/alliance-global/medbill/site-content}"
DST="$(cd "$(dirname "$0")" && pwd)/content"
for f in "$SRC"/*.md; do [ -e "$f" ] || continue; cp -p "$f" "$DST/"; echo "synced $(basename "$f")"; done
