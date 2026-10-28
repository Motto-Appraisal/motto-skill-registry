#!/usr/bin/env bash
# Hook script — called by Droid on SessionEnd to sync knowledge to the repo
set -euo pipefail

SYNC_SCRIPT="${MOTTO_SKILLS_HOME:-${HOME}/motto-skill-registry}/sync.sh"

if [ -f "$SYNC_SCRIPT" ]; then
  bash "$SYNC_SCRIPT" push 2>/dev/null || true
fi

# Always exit 0 — sync is a best-effort background task
exit 0
