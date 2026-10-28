# Agent Standup Checklist

Get a fresh machine/agent online fast with the full Motto Droid kit.

## Prerequisites

- `git` — to clone this repo
- `gh` authenticated (`gh auth status`) — for GitHub-aware skills
- `python3` 3.10+ — for the memory system (stdlib only, no pip installs required)
- Optional: `node` + `npm` — for `wrangler` and other JS CLIs
- Optional: [Ollama](https://ollama.com) + `nomic-embed-text` — embedding search in `harvester.py`
- Optional: `doppler` — secrets are pulled from Doppler/Bitwarden at runtime (never committed)

## One-liner

```bash
git clone https://github.com/Motto-Appraisal/motto-skill-registry.git ~/motto-skill-registry \
  && cd ~/motto-skill-registry \
  && bash standup.sh
```

`standup.sh` is idempotent — safe to re-run. It installs skills, installs the
memory system (scripts + `memory.db` schema bootstrap), then installs missing
CLIs.

## Verify

```bash
ls ~/.factory/skills | head          # skills from this repo + Factory catalog
ls ~/.factory/scripts/kb-query.py    # memory system installed
python3 ~/.factory/scripts/kb-query.py deprecation   # KB responds (empty is fine)
python3 -m pytest ~/motto-skill-registry/tests       # skill structure validation
```

Then fill in `templates/AGENTS.md.template` → `~/.factory/AGENTS.md`:
operator identity, machine table (run `hostname`), workfile paths.

## First-run memory setup

- Point `SESSIONS_DIRS` / `HARVEST_SESSION_DIRS` at your Factory session
  transcripts (default `~/.factory/sessions`) if they live elsewhere.
- `python3 ~/.factory/scripts/full-session-search.py rebuild` — build the
  transcript search index from your sessions.
- Populate `kb_*` tables as you work (where things live, never secret values).

## Skills from outside this repo

Factory catalog skills come from the Factory CLI. External-repo skills
(davinci-resolve-* family, modern-web-guidance, chrome-extensions) are cloned
from their source repos and linked into `~/.factory/skills/` — see the README
section "Skills NOT stored here".

## Secrets

Keep all tokens in Doppler/Bitwarden. Never commit tokens or live recipe
files (`*.live-*.json` is gitignored).
