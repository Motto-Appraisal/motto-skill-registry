# Factory execution adapter

Installed from Luke's supplied Polar procedures on 2026-10-22. The full
supplied procedure and supporting files are retained. Exact supplied files
are preserved under
`C:\Users\lkmot\.factory\knowledge\skill-backups\20261022-polar-procedures-33ce8114\`.

## Read order and authority

Read SKILL.md, `MEMORY.md`, the matching Matrix valuation-mode file, and,
at the template step, `templates_procedure.md` plus
`memory/templates_map_and_figures_notes.md`.

Latest explicit corrections override earlier examples. Mode A overrides
six-comp/ARV-first/two-pass/rating-zero rules. Mode B accepts ALL user-approved
checked comps, including more than six; never silently truncate to six or
infer group membership solely from column numbers when the group sizes differ.
Reconciliation's adjustment-completeness checklist covers EVERY imported comp,
including rating-zero as-is comps.

Full-run template output follows SKILL.md: save the three comments to the
workfile and show them in chat. The supporting template procedure's
"chat-only" wording applies to the standalone template-update workflow,
not as permission to omit the full-run workfile artifact.

## Preconditions before any website mutation

- Confirm the order is active, its valuation mode and the exact subject.
  Do not re-run a cancelled/disregarded order just because it appears in a
  stale retry ledger.
- Reuse the recorded subject session when identity is positively established.
  Do not mutate an uncertain existing session or create repeated duplicates.
- Use the newest **user-reviewed final comp export**, not simply the newest
  arbitrary CSV. Verify approval, exact MLS membership, ordering and count.
  A blocked/pilot/needs-review selection or a 100-row scout pool is not a
  valid import, even if its file timestamp is newer.
- The subject Spark CSV is a SEPARATE Add Subject input. Never import it
  as a comp. County/APN is the fallback only when it is absent.
- Establish subject/session identity before importing comps, boundary edits
  or applying adjustments. A successful click is not a verified transition.
- Do not claim a literal six-row requirement for Mode A or drop Mode B user
  additions. Ask only for true blockers, not permission at every routine step.

## Execution and judgement boundaries

- Use Detached / External Pro / 2055-SFR unless the order requires otherwise;
  Include 1004MC Yes; verify prefill instead of trusting it.
- Draw road-based market boundaries and verify the filtered population
  minimum. Do not automatically rewrite TrueTracts' tailored filters.
- Verify actual amenities and carport structures from photos, not just MLS
  labels. Follow the latest carport/covered-patio/porch rules. Inconclusive
  evidence or unresolved adjustments block export.
- Keep as-is-only logic separate: one cost pass, all retained comps rated,
  no forced condition zeroing or ARV split.
- Preserve source facts for MLS GLA, Realist garage/site/assessed land,
  effective age and the stated cost recipe. The requested quality sweep is
  a sensitivity exercise, not independent evidence of the property's quality.
  Report the assumptions and both computed results without presenting a
  target-matching Q as photo-verified quality or hiding conflicting evidence.
- Apply the per-comp six-month time rule, concessions/rooms rules and full
  feature checklist, then verify saved grid values. No blanket zeroing of
  all time adjustments or omission of rating-zero comps.
- Continue to export AND templates once real blockers are resolved. Do not
  stop at Cost Data merely because a historical run did.
- Export is not signing or external delivery. Never certify, sign, send,
  or manually type comps into Titan unless separately authorized.

## Factory capabilities and files

- This directory is `C:\Users\lkmot\.factory\skills\truetracts`. Source paths
  under `/home/polar/workflows/truetracts/` resolve relative to this folder;
  Matrix supporting files live in the sibling `matrix-comp-search` directory.
- Polar `get_page_text`, `find`, `execute_javascript`, `sign_in`,
  `file_upload`, and `/home/user/downloads` are capability/path examples,
  not guaranteed Factory tools. Discover exact bindings first. Reuse the
  authenticated local browser; request a real connection/login when missing.
- OneDrive/Gmail tool availability must be discovered, with ConnectApp
  discovery if not connected. Do not invent an upload tool or access the
  credential mirror. Canonical local workfiles are available on confirmed
  Legion; verify address, provenance and cloud-sync state before substitution.
- Prefer structured DOM/PDF extraction. Route any map/photo understanding
  through the machine's local-first vision rules. Re-snapshot after viewport
  changes, recalculation and scrolling before editing.
- Capture browser downloads using the actual available download mechanism.
  Verify nonempty `.tdcx` and workfile ZIP outputs, archive contents and
  subject identity before marking export successful. If the browser cannot
  expose those files, report export as unverified/blocked and request the
  user's file confirmation; do not pretend a clicked Export saved a file.
- TDCX creation is not an online Titan import. The supplied workflow says
  the TDCX merge requires the offline application. Do not claim the whole
  pipeline reaches a completed Titan report from a TrueTracts export.

## Templates and checkpoints

Use figures actually selected in Feature Adjustments, not just GAM output.
Template 1 uses market-area data; do not substitute neighborhood 1004MC
figures. Template 3 uses Page-1 Housing Trends checked boxes. Boundary
features come from this session's gold/black polygon. Missing values remain
explicitly flagged; never pass base-template placeholders off as observed data.

The referenced `appraisal-end-to-end` orchestrator was not supplied. Read and
append to the existing `metadata/stage_log__<slug>.md` using stage
`S4-truetracts` and the supplied checkpoint names, recording timestamp,
session URL/id and persisted evidence. Never mark `exported` without verified
files or `templates-run` without the actual three templates.
