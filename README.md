# motto-skill-registry

The single source of truth for the Motto team's Droid/Factory setup: skills,
the custom memory system, the AGENTS.md behavioral template, and shared
knowledge sync. Portable across machines — the current stand-up target is
**macOS**, but everything here is cross-platform.

## Quick stand-up (new teammate)

```bash
git clone https://github.com/Motto-Appraisal/motto-skill-registry.git ~/motto-skill-registry
cd ~/motto-skill-registry
bash standup.sh
```

Then fill in `templates/AGENTS.md.template` (operator name, machine table,
paths) and save it as `~/.factory/AGENTS.md`. See [STANDUP.md](STANDUP.md) for
prerequisites and verification.

## What's in here

| Path | Contents |
|------|----------|
| `skills/` | 44 skills: 8 custom appraisal/Resolve skills + 36 agent-ops skills |
| `memory-system/` | Custom memory machinery: `kb-query.py`, `parts-bin.py`, `full-session-search.py`, `harvester.py`, `verify-done.py`, `context-pack.py`, plus `bootstrap-schema.sql` |
| `templates/AGENTS.md.template` | Sanitized behavioral framework (safety rules, memory workflow, done-verification, content routing) — fill in placeholders, install to `~/.factory/AGENTS.md` |
| `knowledge/` | Shared knowledge files (workflows, decisions, error patterns) — synced via `sync.sh`, bootstrapped empty on purpose |
| `policy/` | Skill-broker policy, hook and mission templates |
| `sync.sh` | Cross-machine knowledge sync (push/pull/auto) |
| `hooks/` | Session-end knowledge sync hook |

## Skills NOT stored here (by design)

Some skills deliberately live outside this repo so they stay updateable from
their sources. Install them alongside the registry:

- **Factory catalog skills** (cloudflare, wrangler, sandbox-*, agents-sdk,
  web-perf, …) — provided by the Factory CLI itself; reinstalling from the
  catalog on each machine avoids version drift.
- **External repo skills** (davinci-resolve-* family, social-video-folder-autocutter,
  modern-web-guidance, chrome-extensions) — clone their source repos and link
  them into `~/.factory/skills/` (see `skills/resolve-motion/SKILL.md` for the
  documented update path).

## Knowledge sync

`bash sync.sh push|pull|auto` merges the shared `knowledge/` JSON files between
`~/.factory/knowledge/` and this repo (union-merge by id, append for JSONL).
The `hooks/sync-knowledge.sh` hook runs `sync.sh push` on session end.

## Data policy

This repo contains **code, schema, and sanitized procedure only**. Personal
data — session history, facts, KB rows, subject property addresses, client
contact details, credentials — stays on each machine. Never commit
`memory.db`, `memory-full.db`, or live `parts-bin.json` contents.

## Development

```bash
bash install.sh        # install skills + memory system to ~/.factory
python -m pytest tests # skill structure validation
npx prettier --check "**/*.{yml,yaml,md,json}"   # lint
```
