# Memory System

Portable custom memory machinery for Factory/Droid sessions. This is the code
and schema only — **no personal data ships with it**. Each machine grows its own
memory from its own sessions.

## What's here

| File | Purpose | Installs to |
|------|---------|-------------|
| `scripts/kb-query.py` | Query the KB tables (capabilities, services, credentials, deprecations, error patterns) | `~/.factory/scripts/` |
| `scripts/parts-bin.py` | Memoized reuse-vs-build decision catalog (the "recycler" cache) | `~/.factory/scripts/` |
| `scripts/full-session-search.py` | Fast full-text search over past session transcripts (stdlib FTS, no embeddings) | `~/.factory/scripts/` |
| `scripts/verify-done.py` | Pre-"done" verification harness (code/config/infra/research/file) | `~/.factory/scripts/` |
| `scripts/context-pack.py` | Per-repo context pack manager | `~/.factory/scripts/` |
| `scripts/harvester.py` | Session harvester: extracts facts from session JSONL, optional Ollama embeddings, hybrid search | `~/.factory/memory/` |
| `bootstrap-schema.sql` | Full `memory.db` DDL (KB tables + facts/session_summaries/embeddings + fleet tables) | applied at install if `memory.db` is absent |

## Install

`bash install.sh` at the repo root installs everything including this. To install
only the memory system:

```bash
bash memory-system/install.sh
```

The installer copies the scripts, then bootstraps `~/.factory/memory.db` from
`bootstrap-schema.sql` **only if the file does not already exist** (never
overwrites live memory).

## Prerequisites (macOS)

- Python 3.10+ (stdlib only — everything runs without pip installs)
- Optional: [Ollama](https://ollama.com) + `nomic-embed-text` — enables
  embedding-based search in `harvester.py` (text search works without it)
- Optional: `docker` + `curl` — only for `verify-done.py` infra checks

## Session locations

- `full-session-search.py` reads session JSONL dirs from the `SESSIONS_DIRS`
  env var (colon-separated, default `~/.factory/sessions`).
- `harvester.py` reads from `HARVEST_SESSION_DIRS` (colon-separated,
  optionally `label=path`; default `~/.factory/sessions`).

On a Mac, Factory session transcripts typically live under
`~/.factory/sessions`; point the env vars wherever yours land.

## Growing the KB

The KB tables (`kb_capabilities`, `kb_services`, `kb_credentials`,
`kb_deprecations`, `kb_error_patterns`) bootstrap empty on purpose. Populate
them as you work:

- Credentials: store **where the key lives** (Doppler project/config/key-name,
  Bitwarden item), never the secret value itself.
- Services: host/URL/port of internal services.
- Capabilities: "how do I do X" one-liners with the tool to use.

Then query with `python ~/.factory/scripts/kb-query.py capability "<search>"` etc.

## Personal data policy

Facts, session summaries, transcripts, and KB rows are machine-local personal
history. Never commit them to this repo. The `sync.sh` knowledge sync at the
repo root covers the shared `knowledge/` JSON files only.
