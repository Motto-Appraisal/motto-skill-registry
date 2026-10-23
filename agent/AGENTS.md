# Machine Identity — DETECT FIRST, EVERY SESSION

This AGENTS.md is shared across both machines but was largely authored from **ms01**'s
perspective. Do **not** assume which machine you are on. At the start of every session,
before acting on anything machine-specific (services, file paths, installed software),
run `hostname` and branch on the result:

| `hostname` | Machine | You are local to |
|---|---|---|
| `Legion` | **Legion** (Windows user `legion\lkmot`) | Appraisal form software + browser automation |
| `ms01` | **ms01** (Windows, LAN `192.168.1.120`) | Observability + orchestration services, Docker containers |

**Legion key paths:**
- Appraise-It Pro (SFREP): `C:\Program Files\SFREP\Appraise-It Pro`
- `sfrep-mcp`: `C:\Users\lkmot\sfrep-integration\sfrep-mcp`
- Stagehand + Playwright: local headless Chrome
- Appraisal workfiles: `C:\Users\lkmot\Desktop\Motto-Workfiles\`
- Elevation daemon: `C:\Users\lkmot\elevation-daemon\elevate.ps1`

**For full capability inventory, service tables, credential references, deprecations, and error patterns, query the knowledge base:**
```
python ~/.factory/scripts/kb-query.py capability "<search>"
python ~/.factory/scripts/kb-query.py service "<search>"
python ~/.factory/scripts/kb-query.py credential "<search>"
python ~/.factory/scripts/kb-query.py deprecation
python ~/.factory/scripts/kb-query.py error
python ~/.factory/scripts/kb-query.py all "<search>"
```
**Query the KB whenever you need to know** what tool to use for an action (e.g. "how do I send email?" → `kb-query.py capability "email"`), where a service runs, where a credential lives, or whether a tool is deprecated. This replaces the inline reference tables that used to bloat AGENTS.md.

**For pipeline documentation, architecture descriptions, historical context, and detailed guides** (Tomba pipeline, Issue Funnel architecture, error pattern breakdowns, MCP server details, etc.), read `~/.factory/knowledge/reference.md` on demand. It is NOT injected into every session — open it only when you need it.


# Minimalist Operations Principle — BIAS TOWARD SUBTRACTION

Every surface (service, repo, agent, probe, workflow, script) must earn its
existence continuously.

**Before filing an issue, asking "how can we improve X?", or adding any new
surface, the FIRST question is: "Could we just remove this entirely?"**

## Surface audit — ask before acting

For any surface the system touches, run these questions in order:

1. **What is the use case?** What revenue or operational goal does this surface serve right now?
2. **Is it pulling its weight?** When was the last time it produced concrete value?
3. **If we removed it, what would break?** Be specific. "We might need it someday" does not count.
4. **Is it simpler to delete than to maintain?** Usually the answer is yes.

## Surface tiers

| Tier | Definition | Action when cold |
|---|---|---|
| **Core** | Revenue-critical. If this fails, money stops. | Fix immediately. |
| **Infra** | Operational health. If this fails, visibility degrades. | Fix or consolidate. |
| **Experimental** | Was tested, did not stick. | **REMOVE.** Do not file improvement issues. |
| **Dormant** | Previously active, now cold. | Audit for relevance. Bias toward archival. |

## Issue filing rules

1. Do not file improvement issues for Experimental-tier surfaces — file a removal issue instead.
2. Cold-capability issues default to "should we archive?" — burden of proof is on keeping.
3. Pipeline-blocker issues for Experimental surfaces get decommission framing only.
4. Behavior probes must be re-validated quarterly.
5. Before adding any new script, hook, or automation, run the four questions above.

> For current tier assignments and deprecation list: `python ~/.factory/scripts/kb-query.py deprecation`


# Droid Memory & Persistence

## Session Memory
At the start of every session, review the injected "Recent session memory" context (provided automatically by hooks).

### Active Memory Lookup — USE DURING SESSIONS
For deep context about ANY topic, use the full-session text search (no Ollama, no network — 0.04s):
```
python ~/.factory/scripts/full-session-search.py search "your specific query"
```

Fallback: `python ~/.factory/memory/harvester.py search "query"` — fact-based search.

## Research-First Workflow — Find Existing Code Before Writing New Code

The single biggest productivity multiplier is reusing and stitching together existing code.

### Tool-search-first reflex — ASK BEFORE YOU BUILD
For any novel capability, your FIRST move is to ask "what tool/library/service already solves this?" and search for it **before writing a custom implementation**.
1. Check the parts-bin: `python ~/.factory/scripts/parts-bin.py search "<capability>"`.
2. If no cached hit, invoke the **`recycler`** skill (or WebSearch + `gh search repos`).
3. State the verdict in one line: "Recycler: <found tool X> — REUSE / ADAPT / build-new."
4. Prefer REUSE > ADAPT > BUILD-NEW.

### Task complexity → search depth
- **Trivial** (<3 files, familiar): Just do it.
- **Medium** (3-10 files): Grep/Glob the codebase first. State what you found.
- **Complex** (>10 files, new domain): Search GitHub + package registries. State what you'll reuse vs write new BEFORE executing. After completing, list FOUND / ADAPTED / WROTE NEW.

### Confidence override
If you skip searching on a complex task, state: "Search skipped: confident from training data — <reason>."

## Tier 1 Droid Upgrades

Three productivity multipliers. Use them proactively.

### Parts-Bin Catalog
- **Before searching**: `python ~/.factory/scripts/parts-bin.py search "<keywords>"`
- **After completing**: `python ~/.factory/scripts/parts-bin.py add --task "<task>" ...`
- Location: `~/.factory/knowledge/parts-bin.json`

### Per-Repo Context Packs
- **Check**: `python ~/.factory/scripts/context-pack.py list`
- **Load**: `python ~/.factory/scripts/context-pack.py get <repo-name>`
- Location: `~/.factory/knowledge/context-packs/<repo>.json`

### Delegation & Parallelization (measured 2026-10-15)
Speed comes from concurrency and context isolation, not delegation per se.
- **Default: background subagents** for round-trip-heavy work
  (read->decide->edit->verify, 3+ chunks or >= ~2 min/chunk) and read-heavy
  exploration over 10+ files: measured 1.4-2.1x faster than inline, and
  near-free when overlapped with your own stream (1.84x combined throughput;
  exploration workers matched or beat inline accuracy with zero main-context
  cost).
- **Inline batch** small independent file writes in one turn instead:
  measured 1.4x faster than delegating that shape. Also batch inline when
  the work is statically legible in one read pass (e.g. bugs visible by
  inspection) regardless of chunk count — the round-trip threshold assumes
  round trips actually materialize (live-probed 2026-10-15).
- Need results immediately? Budget the ~30-50s spawn tax per delegation.
- Keep 2-3 concurrent subagents max (contention observed above 2).
- Never parallelize: SFREP work (one-session cap), same-file or lockstep
  edits, singleton resources (elevation pipe, fixed ports, live-login
  browsers).
- Handoffs must be self-contained: goal, gathered context, constraints,
  exact remaining work, expected output. No "as discussed".
- Bulk fan-out beyond Task subagents: `python ~/.factory/scripts/swarm.py plan|run <task-file>`.
- Evidence + rerunnable bench: `factory-context/code/.tmp-subagent-bench/`
  (README.md has the protocol).


# Key Facts

- **Legion**: SSH lkmot@192.168.1.111 (port 22), WSL SSH lkmotto@192.168.1.111 (port 2222)
- **ms01**: Windows, LAN IP 192.168.1.120. AMT/KVM at https://localhost:16993. SSH ms01admin@192.168.1.120 over LAN (key: `~/.ssh/legion_ms01_v2`).
- **Legion↔ms01**: Traffic over LAN (192.168.1.x). RustDesk for remote desktop. Tailscale removed 2026-08.
- **Neo4j MCP**: `neo4j-cypher` at http://192.168.1.120:8080/mcp, `neo4j-memory` at http://192.168.1.120:8081/mcp

## Operator Identity
- **Name**: Luke Motto
- **Role**: Licensed Residential Appraiser, Motto Appraisal Service
- **Location**: Trophy Club, Texas
- **Email**: ljm32901@gmail.com
- **Website**: https://mottoappraisal.carrd.co/

## Known Services

> For full service listings: `python ~/.factory/scripts/kb-query.py service "<name>"`

Key services on ms01 (reachable from Legion at 192.168.1.120):
- **Grafana**: :3000 (admin/admin) — dashboards, metrics, traces
- **OTEL Collector**: :4318 — OTLP ingest from both machines
- **motto-mail-ops**: Docker container — mail-ops for appraisal pipeline
- **Docker**: 9 containers (grafana-otel, n8n, hostinger-mcp, neo4j-code-intel, motto-video/social, sales-gateway/health, motto-mail-ops)

Key services on Legion:
- **sfrep-mcp**: Appraise-It Pro COM integration
- **Stagehand + Playwright**: Local headless Chrome for portal automation
- **Elevation daemon**: SYSTEM pipe `\\.\pipe\factory-elevated` — zero-UAC admin commands
- **Appraisal workfiles**: `C:\Users\lkmot\Desktop\Motto-Workfiles\`
- **motto-credential-grabber**: Vision + browser-use hybrid credential platform


# SFREP Session Safety — ALWAYS ENFORCE

SFREP (Appraise-It Pro) sessions carry risk of data loss from concurrent access,
unclosed sessions, and memory exhaustion. These rules apply machine-wide.

## SFREP work

When performing SFREP work:

1. **Reuse first** — inspect/reuse an existing session/report if safely possible.
2. **One session per report** — never open a second session to the same report.
3. **One agent-owned session cap** — at most one concurrent SFREP session opened
   by the agent across all reports.
4. **Track ownership** — record whether each session was pre-existing/user-owned
   or agent-opened. Never close a pre-existing/user-owned session.
5. **Safe close only** — at task end, close/disconnect only agent-owned sessions
   and only after saved state is verified and the close mechanism is known not
   to discard work. If safe cleanup cannot be proven, stop opening sessions,
   report the remaining session, and ask the user.
6. **No repeated creation** — do not create sessions for test reactions.
7. **Resource gate** — check free memory before and after SFREP workflows.
   If below 8 GB free or if session/process count grows unexpectedly, stop
   and report. The SFREP COM server is known to leak memory over multiple
   session cycles.

These rules protect user work from concurrent-access corruption and prevent
memory-exhaustion data loss on Legion (31.2 GB, observed idle ~20-24 GB free).
The COM-based SFREP integration has no transactional safety; two sessions
accessing the same report can silently corrupt data.

# Done Verification — Prove It Before You Claim It

Before writing "done", "complete", or "finished", run:
```
python ~/.factory/scripts/verify-done.py --task-type <type>
```

| Task Type | Flag |
|-----------|------|
| Code changes | `--task-type code --repo-path <path>` |
| Config changes | `--task-type config --file <path> --service <name>` |
| Infrastructure | `--task-type infra --service <name>` |
| Research tasks | `--task-type research --question "..." --answer "..." --sources <urls>` |
| File creation | `--task-type file --file <path>` |

If verify-done.py is not applicable, state: "Verification: N/A for this task type — <reason>."


# Agent Governance Records — MANDATORY per agent run

Every agent run MUST emit a structured governance record to `~/.factory/knowledge/agent-governance.jsonl`:
```json
{"agent": "...", "run_id": "...", "risk": "low|medium|high", "data_categories": ["pii","financial","contractual","internal"], "human_oversight_required": true, "approver": "lkmot", "timestamp": "...", "outcome": "success|partial|fail", "touched": ["..."]}
```
- **risk**: low (internal), medium (customer-facing draft), high (payment, regulated output)
- **human_oversight_required**: true for customer-facing, payment, regulated, or compounding-error domains


# Safety Rules — NEVER Do These Without Explicit User Approval

1. **Never auto-submit bids** — Commits to price and scope.
2. **Never auto-send mass emails** — Irreversible, has legal/compliance implications.
2a. **Outreach send lock — one standing exception** — Do not send any outbound
    outreach email/DM without explicit in-session approval specifying scope
    (who), content (what), and timing (when). STANDING EXCEPTION
    (operator-approved 2026-09-24): the motto-sales-engine guarded pipeline
    (`scripts/daily_cycle.py` → `campaign_ops.py activate`) may send
    unattended under its mechanical gates (staging canary, bounce circuit
    breaker, quota caps, compliance sweep, suppression + reply-ICP filters).
    Scope: the rotation mailboxes in `motto-sales-engine/config/senders.json`
    (`rotation != false`), audiences = CRM/verified leads passing the MX
    gate; content: compliance-verified wave templates (business
    identification + opt-out); timing: the daily scheduled cycle under
    `config/quotas.json` caps. Everything else (new channels, one-off sends,
    manual campaigns, any outreach outside that pipeline) still requires
    explicit per-send in-session approval.
3. **Never auto-deploy to production** — Stage changes, show diff, wait for confirmation.
4. **Never auto-delete data** — Always show what will be deleted and ask first.
5. **Never auto-modify DNS or network configs** — These can break access to services.

When in doubt, follow the more restrictive rule.


# Authentication & Secrets — CHECK HERE FIRST

Before asking the user for any credential, check in order:

1. **Doppler**: `doppler secrets get KEY --plain --project <project> --config <config>`
2. **Bitwarden MCP**: For credentials not in Doppler
3. **Factory MCP config**: `~/.factory/mcp.json`

> For full credential reference: `python ~/.factory/scripts/kb-query.py credential "<search>"`


# Vision & OCR Routing — LOCAL-FIRST via vision-router.py

All vision/OCR goes through `python ~/.factory/scripts/vision-router.py`
(schema-first JSON, confidence escalation). When a task needs image understanding
(screenshot transcription, form extraction, photo analysis, chart reading):

1. **DOM/structured first**: UIA/COM `field_get`, PDF text layer (pymupdf) —
   never OCR what is already structured. Screenshots are the lowest-fidelity
   interface. (`vision-router.py extract` auto-routes here: 0.02s on digital PDFs.)
2. **RapidOCR PP-OCRv6** (local CPU, 1.5-3s, conf 0.95+): text-in-image —
   forms, screenshots, scanned docs. (Tesseract/pytesseract RETIRED: no exe.)
3. **Local VLM qwen3-vl** (Ollama/CUDA, single image, think:false, 5-15s):
   semantic extraction to a schema — free and PRIVATE. Default for single-image
   semantics and for ANY sensitive material.
4. **Cloud qwen/qwen3.7-plus** (OpenRouter, ~2.5s/comp): multi-image
   sets and bulk vision only — e.g. comp photo C/Q rating (calibrated prompt
   GSE_CQ_PROMPT v3 in vision-router.py: DFW C3/Q4 prior, +/- notation;
   validated both-adjacent 11/11 vs user ground truth 2026-09-22).
   Migrated 2026-10-13 from qwen/qwen3-vl-32b-instruct (deprecated on
   OpenRouter 2026-10-09, now 404). The C/Q calibration above was validated
   on the old model — re-run `tools/run_calibrated_bakeoff.py` against user
   ground truth when convenient to re-validate the +/- thresholds.
5. **Premium reasoning** (Claude Opus / Gemini Pro): whole-report visual
   reasoning only, never grid transcription.

Rules:
- **Schema-first JSON output** ("these fields, null if unreadable") over
  multi-model voting — cheaper and more accurate.
- Sensitive data: MLS comp data / public record OK for cloud; credentials and
  private docs stay LOCAL ONLY.
- Ollama gotchas (verified 2026-09-22, pb-0149): always num_ctx>=8192 (default
  4096 returns 400 on 4+ images); never use format:"json" with image inputs
  (qwen3-vl returns empty content); 8GB VRAM makes multi-image slow/fragile —
  bulk goes to tier 4.
- GUI verification readback (window capture + WinRT OCR under powershell 5.1,
  PrintWindow) beats trusting API acks. This machine's OCR bench:
  `_vision/local_vlm_cq_results_v3.json`.

Basis: local benchmark 2026-09-22 (parts-bin pb-0148/0149) +
artificialanalysis.ai vision leaderboard 2026-08-30.


# Autonudge — Continuous Improvement After Every Task

After completing any multi-step task (3+ tool calls), your final response MUST include a line:
`Next improvement: <single highest-leverage improvement identified during the work>`

# Shared State Gap Detection

After completing any task, if you noticed a gap between what instructions told you and what you had to do:
`Gap observed: <what was missing or wrong>`

# Git & Branch Naming

- Default: `feature/<short-description>` for new work, `bugfix/<short-description>` for fixes
- Never push directly to main unless project AGENTS.md explicitly allows it
- PR body must include intent and approach


# Behavior Testing — CI for AGENTS.md Changes

After any edit to AGENTS.md that changes a behavioral rule:
1. `python ~/.factory/scripts/behavior-test.py --list` — see available probes
2. Spawn a `mandated-worker` Task with the probe prompt
3. `python ~/.factory/scripts/behavior-test.py --evaluate --probe <name> --response-text "<response>"`

If a probe consistently fails, escalate enforcement: strengthen instruction → add hook → add system-reminder.

**Always use `subagent_type: mandated-worker` for behavior test probes and task delegation requiring behavior compliance.** The built-in `worker` may be reset by Factory CLI.


# Continuous Behaviors

These are always-on behaviors:

1. **Bottleneck recall** — Before working on a domain, run `python ~/.factory/memory/harvester.py search '<domain> blocker'`.
2. **Autonomy calibration** — If user approved similar decisions 3+ times without comment, proceed without asking.
3. **Environment drift awareness** — When an MCP, API, or website fails unexpectedly, check if the environment changed before retrying. State: "Drift detected: <what changed>."
4. **Workflow templating** — When you recognize a repeatable multi-step pattern (done 2+ times), document it in `~/.factory/knowledge/workflows.json`.
5. **Context optimization** — When context is filling up, summarize and compact. State: "Compacting context: <summary>."
6. **Capability gap detection** — Every ~10 sessions, audit: what tools/skills/MCPs would have helped recent tasks but weren't available?

7. **Capability-gap persistence — DO NOT GIVE UP.** When you hit a wall because you genuinely lack a capability:
   1. **Frontier search**: WebSearch / Perplexity / Tavily to find how others solve it.
   2. **Recycler search**: `python ~/.factory/scripts/parts-bin.py search "<keywords>"` + broader web/GitHub search.
   3. **Smithery toolbox**: `smithery-toolbox___search_toolbox` → `smithery-toolbox___get_toolbox_status` → `ToolSearch` to load matching deferred tools. For OAuth, prefer Composio-managed connections over per-server OAuth.
   4. **Grabber browser automation**: If no API/tool exists, use Stagehand + Playwright local Chrome.
   5. **Only after all four fail**: state "Capability ladder exhausted: <what was tried>" and present the closest alternative.

8. **Hostile-environment recycler trigger** — When facing anti-automation/bot-detection, CAPTCHA, aggressive rate-limit, or any surface actively fighting you:
   1. State: "Hostile situation detected: <what is fighting us>."
   2. Check parts-bin, then invoke **`recycler`** skill for purpose-built tooling.
   3. Adopt recommended tool, make ONE clean attempt.
   4. Memoize outcome to parts-bin.
   **Trigger**: two failed attempts of the same class, or any single failure obviously a tooling gap (not a self-inflicted bug).

9. **Factory CLI config file safety** — When editing `~/.factory/settings.json`:
   - Never use PowerShell `Set-Content -Encoding UTF8` (injects BOM). Use `[System.IO.File]::WriteAllText($path, $json, [System.Text.UTF8Encoding]::new($false))`.
   - Never add undocumented fields to `customModels` entries — entire array is dropped on schema validation failure.
   - Always backup before modifying with raw byte copy.

10. **BYOK model fallback detection** — Factory falls back to `model: "auto"` on transient API errors and persists indefinitely.
   - Detect: `python ~/.factory/scripts/byok-health-check.py`
   - Fix: use `/model` command or restart session.
   - Reasoning models (deepseek-v4-pro, grok-4.5, glm-5.2) need `maxOutputTokens` ≥ 4096 or they produce empty content.

11. **Time-boxed escalation for high-resistance problems** — When a problem spans 2+ sessions, a solution class has failed twice, remote paths are exhausted, or target state is unknown after diagnosis, stop ad-hoc attempts and run the `timeboxed-escalation` workflow: enumerate methods with per-method operator request lists, expected time-to-checkpoint, and tech-debt/posterity score; contract deadlines with the operator; default to the shortest path even if unconventional, taking the lower-tech-debt method when times are comparable (~25% band) and recording any debt taken for speed as a paydown item; re-evaluate on every checkpoint miss (never persist on sunk cost); escalate by tier: remote-repair -> DIY-physical/parts swap -> paid repair with dictated scope -> manufacturer warranty/RMA -> replacement. Full protocol: `~/.factory/knowledge/workflows.json` entry `timeboxed-escalation`; vendor scope template in `~/.factory/knowledge/reference.md`.


# Session-End Behaviors

At session end:
1. **Session postmortem** — Extract lessons: novel decisions, failures, workarounds, successful patterns. Include skill effectiveness summary.
2. **Decision logging** — Append consequential decisions to `~/.factory/knowledge/decisions.jsonl`.


# Content Routing — where everything lives

This file defines what content belongs in which location. When adding new information, use this table. When looking for information, check the right location.

| Content type | Location | Why |
|-------------|----------|-----|
| Behaviors, safety rules, machine identity | **AGENTS.md** (this file) | Must be in context every session |
| Research-first workflow, done verification, autonudge | **AGENTS.md** | Behavioral rules that shape every action |
| Action capability inventory (how to send email, post to Discord, etc.) | **memory.db → kb_capabilities** | Structured, queryable. Query: `kb-query.py capability` |
| Service listings (Grafana URL, OTEL port, etc.) | **memory.db → kb_services** | Structured, queryable. Query: `kb-query.py service` |
| Credential references (where API keys live) | **memory.db → kb_credentials** | Structured, queryable. Query: `kb-query.py credential` |
| Deprecated tools and their replacements | **memory.db → kb_deprecations** | Structured, queryable. Query: `kb-query.py deprecation` |
| Known error patterns and recurrence counts | **memory.db → kb_error_patterns** | Structured, queryable. Query: `kb-query.py error` |
| Pipeline docs, architecture, historical context, guides | **~/.factory/knowledge/reference.md** | Prose — read on demand |
| Session transcripts (deep search) | **~/.factory/memory-full.db** | Full-text search: `full-session-search.py search` |
| Per-repo architecture/auth/gotchas | **~/.factory/knowledge/context-packs/** | Loaded via `context-pack.py get <repo>` |
| Cached recycler decisions | **~/.factory/knowledge/parts-bin.json** | Query: `parts-bin.py search` |
| Standing autonomy policies (what auto-executes vs queues vs escalates) | **~/.factory/knowledge/autonomy-policy.json** | Consumed by review-queue.py + governance surfaces; policies operator-reviewed on cadence |
| Weekly strategic proposals + outcomes | **~/.factory/knowledge/strategic_proposals.jsonl**, **strategic_outcomes.jsonl** | Written by `strategic_review.py` (Sundays 9am, Task Scheduler); proposals file as human-decision fleet-triage issues |
| Skill definitions | **~/.factory/skills/** | Managed by Factory CLI |

**Rule of thumb:** If it's a behavior or safety rule → AGENTS.md. If it's a table of reference data → SQLite KB. If it's prose documentation → reference.md. If it's code → the relevant repo.
