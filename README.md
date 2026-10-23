# motto-skills

Portable personal Factory skills bundle for fast agent stand-up on new machines.

## Quick stand-up

```bash
git clone https://github.com/lkmotto/motto-skills.git "$HOME/motto-skills"
cd "$HOME/motto-skills"
bash install.sh
```

Done — skills are installed into `~/.factory/skills/`.

## What gets installed

| Repo path     | Target                        | Update policy                          |
| ------------- | ----------------------------- | -------------------------------------- |
| `skills/`     | `~/.factory/skills/`          | Overwritten on every install           |
| `droids/`     | `~/.factory/droids/`          | Overwritten on every install           |
| `agent/AGENTS.md` | `~/.factory/AGENTS.md`    | Fresh only; `-Force` to overwrite      |
| `knowledge/`  | `~/.factory/knowledge/`       | Fresh only; `-Force` to overwrite      |
| `policy/`     | `~/.factory/skill-broker.policy.json`, `~/.factory/hooks.json` | Fresh only; `-Force` to overwrite |

Re-running `install.ps1`/`install.sh` after pulling the repo is the way to
propagate skill and droid updates to a machine.

## Fast Agent Standup

Bring a brand-new machine or agent fully online in one step. `standup.sh`
installs the skills, then installs the required CLIs (idempotent — already
present tools are skipped), and prints a readiness summary.

```bash
git clone https://github.com/lkmotto/motto-skills.git "$HOME/motto-skills"
cd "$HOME/motto-skills"
bash standup.sh
```

That's it. See [STANDUP.md](STANDUP.md) for prerequisites and verification.
