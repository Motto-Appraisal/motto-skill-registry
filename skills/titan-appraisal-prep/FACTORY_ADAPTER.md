# Factory execution adapter

Installed from {{OPERATOR_NAME}}'s supplied Polar procedures on 2026-10-22. The supplied
body is retained below this adapter's link in SKILL.md. Exact supplied files
and the previous Factory skill are preserved outside skill discovery under
`~/.factory/knowledge/skill-backups/20261022-polar-procedures-33ce8114\`.

## Rule precedence

1. Machine-wide safety rules and explicit instructions for the current order.
2. The latest explicit user corrections in SKILL.md.
3. The verified Exterior-Only starter/form-order shortcut.
4. The older numbered procedure, then historical memory examples.

Read `MEMORY.md` and `memory/run-notes.md` as supporting experience, not as
authority to reinstate a superseded rule. In particular:

- Use **Exterior-Only [UAD Version]**, not the old URAR starter.
- Search for an existing report and read the stage log before creating one.
- Create without merging; generate and save Flood/Aerial images and FEMA
  values in the SAME report; then perform the ONE Forms AND data merge from
  the exact `ZZ TEMPLATE TEST` source. Never repeat an uncertain merge.
- Select `[Scanned Page] Addendum` before adding Building Sketch; verify its
  resulting position rather than performing a fixed number of down clicks.
- RW assignment type is **Other / Ascertain Market Value**, not Purchase.
  Contract transaction type is None Selected; financial assistance amount is
  empty. Spot-check the corrected template, never edit the template here.
- Preserve standing Effective Age, Window Type and Gutters. Do not substitute
  chronological age for effective age.
- Only overwrite subject-specific facts with verified replacements. Preserve
  and explicitly flag unverified template values instead of silently clearing
  them. The specific contract/assistance corrections above remain exceptions.
- No appraiser inspection or visit claims. RW's scoping visit is a different
  source. Do not use `sfrep/narratives.json` as a source of report prose.
- No comp, market, reconciliation, Location Map, certification, signature or
  delivery work in this prep skill.
- Save and leave the same report OPEN. A successful field write alone does
  not prove the complete prep sequence.

## Factory paths and capabilities

- This skill directory is `~/.factory/skills/titan-appraisal-prep`.
  `/home/polar/workflows/<skill>/...` references mean the corresponding
  installed Factory skill directory, not a path that exists on {{HOSTNAME}}.
- On confirmed {{HOSTNAME}}, existing workfiles are normally under
  `~/Desktop\{{WORKFILES_ROOT}}\by_address\<slug>`. Resolve canonical
  paths using the pipeline's `agent.workfile_paths`; verify address, recency
  and artifact identity. Do not assume the cloud mirror has settled.
- `/home/user/work` and `/home/user/downloads` are Polar sandbox paths.
  Use an explicitly chosen local workspace staging directory and the actual
  download tool's returned path. No download acknowledgement proves a file
  was saved.
- OneDrive/Gmail tool names in the source describe capabilities, not guaranteed
  Factory bindings. Discover exact available tools first. If the service is
  not connected, use ConnectApp discovery and request its connection. Do not
  invent tools or read `Appraisal-Creds`.
- Reuse the operator's authenticated Titan tab. Do not launch a new credential
  login to make an old script work: it can invalidate the user's only session.
  If the available browser shows only blank tabs, stop and report that the
  working browser is not attached.
- Map Polar's `find`/`get_page_text`/`execute_javascript` to available DOM or
  accessibility tools. `notify_user` means report the blocker to the user,
  using AskUser for a blocking decision. File chooser and coordinate actions
  must use the actual available browser tool. Coordinates are historical
  hints only; inspect the current DOM/viewport before each action.
- Extract PDF text before OCR. Image understanding follows the machine's
  local-first `vision-router.py` rules. Do not send private scope documents
  to cloud vision.

## Checkpoints and verification

The referenced `appraisal-end-to-end` orchestrator was not supplied and is not
installed by this import. Use the checkpoint names in SKILL.md directly:
`report-created`, `maps-fema`, `template-merged`, `manage-fixed`,
`order-form-page1`, `saved-open`.

Read the existing `metadata/stage_log__<slug>.md` before acting. Append only
observed checkpoints, with timestamp, stage `S2-titan-prep`, status, report
URL/id and evidence path. Never mark a queued action DONE, overwrite another
stage's log, or infer that an absent merge log means no merge occurred.

Before reporting prep success, re-read saved subject/order facts, invoice,
maps/FEMA, images and final Manage form order. Record unverified template
content and TrueTracts-pending sections. A report id or field count alone is
not sufficient. No live E2E certification follows from installing this skill.

## Missing historical material

`reference/old-skill-full-history-2026-10-04.md` and
`reference/lessons-log-2026-10-02.md` were referenced but not supplied. Do not
fabricate them or silently substitute old experiments. The supplied current
procedure and memory are available.
