#!/usr/bin/env bash
# Memory system installer — portable (macOS/Linux/WSL).
# Copies the memory scripts into ~/.factory and bootstraps memory.db if absent.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_SCRIPTS="$HOME/.factory/scripts"
TARGET_MEMORY="$HOME/.factory/memory"
TARGET_DB="$HOME/.factory/memory.db"

echo "=== memory-system installer ==="
mkdir -p "$TARGET_SCRIPTS" "$TARGET_MEMORY"

for s in kb-query.py parts-bin.py full-session-search.py verify-done.py context-pack.py; do
  cp "$SCRIPT_DIR/scripts/$s" "$TARGET_SCRIPTS/$s"
  echo "  + scripts/$s"
done

cp "$SCRIPT_DIR/scripts/harvester.py" "$TARGET_MEMORY/harvester.py"
echo "  + memory/harvester.py"

if [ -f "$TARGET_DB" ]; then
  echo "  ~ memory.db already exists — left untouched"
else
  python3 - "$TARGET_DB" "$SCRIPT_DIR/bootstrap-schema.sql" <<'PY'
import sqlite3, sys
db = sqlite3.connect(sys.argv[1])
db.executescript(open(sys.argv[2], encoding="utf-8").read())
db.commit()
print("  + memory.db bootstrapped from bootstrap-schema.sql")
PY
fi

echo "=== done — memory system installed ==="
