# Factory execution adapter

Installed from Luke's supplied Polar procedures on 2026-10-22. Supplied files
and the previous Factory skill are preserved under
`C:\Users\lkmot\.factory\knowledge\skill-backups\20261022-polar-procedures-33ce8114\`.

## Scope and precedence

This is **manual/on-demand appraisal comp search**, not the previous Factory
creative-finance lead screen. Mode A means AS-IS ONLY and Mode B means
AS-IS + SUBJECT-TO. The old meaning of "Mode B" must not leak into this skill.
No scheduler is created or changed by this installation.

Read `MEMORY.md`, then ONLY the matching mode file for selection logic:

- `mode_as_is_only.md`: current-condition relevance, no price/ppsf ranking
  or rejection; typically closed comparables plus active listings. Subject
  current condition comes first, not an automatic dated-C4 assumption.
- `mode_as_is_subject_to.md`: as-is purchase-ppsf alignment is not a hard price
  exclusion. Renovated choices prioritize supported renovation quality and
  completeness, with the latest proximity/bracketing correction applied.
  Price above ARV never disqualifies a renovated comparable.

The selected mode and latest dated corrections override shared instructions
and historical examples. Do NOT apply the shared ppsf-sort step to Mode A.
Do NOT use the older +/-15% band as a hard eligibility gate in either mode.
Do NOT force six comps or drop user additions to obtain 3+3.

First-pass area is a two-mile radius, no city filter, acres minimum 0.05 with
the computed +/-20% maximum. Use the classic form to set it, then review in
the new UI. Pool must initially match the subject. Any relaxation is explicit
and reported. Mode A retains active/listing statuses as its mode file requires.
Clear unintended prior filters, not the mode's intended statuses.

## Mandatory user-review boundary

1. Show the FULL new-UI candidate pool with proposed picks checked. Inspect
   all grid pages and the selected count; do not replace the pool with a
   speedbar MLS list for review.
2. Explain the proposals, evidence and uncertainties. STOP for the user's
   approval. A prior pilot-review count or an algorithm's `auto_export`
   disposition is NOT approval for this run.
3. After approval, re-read the actual checked rows across every page and
   de-duplicate the duplicated DOM grid by MLS number. This final user set,
   including additions, is authoritative.
4. Export directly from that full grid; verify CSV MLS membership and row
   count. Mode B preserves all approved rows, renovated ascending by sale
   price first, then as-is ascending. Mode A has no ARV/as-is split.
5. Export the subject listing separately when available, after the comps.
   Do not let `__subject.csv` become a comparable or scout-pool input.
6. File under a new unused name and verify it persisted. Do not overwrite
   prior exports. Machine-wide delete-approval rules override any source
   instruction to delete a superseded export automatically: show the exact
   file and obtain explicit approval before deleting.

## Factory execution

- This directory is `C:\Users\lkmot\.factory\skills\matrix-comp-search`.
  Resolve the source's `/home/polar/workflows/matrix-comp-search/...` to
  files here. Read `photo_sheet.js` before injecting it into a Matrix tab.
- OneDrive/Gmail/browser tool names are Polar-specific examples. Discover
  actual available bindings; use ConnectApp discovery if a named service
  is not connected. Local canonical Legion workfiles may supply already
  verified inputs; do not assume their cloud copy is current.
- `/home/user` scratch/download paths are not Legion paths. Save to a
  deliberate workspace location; verify the downloaded CSV, not a tool ack.
- Use the operator's Matrix session. On login/challenge failure, report and
  stop rather than retrying credentials or rotating browser identity.
- Browser DOM/accessibility inspection precedes coordinate input. Screenshots
  are viewport-specific. PDF text precedes OCR; photo understanding follows
  the machine's local-first vision routing.
- The classic combined Photo Count field and new-UI separate min/max boxes
  differ. Inspect the actual form before filling; do not type `4-999` into
  a single Min box. Avoid the known broken "+N" chip expansion.

## Photo helper limitation

The supplied `photo_sheet.js` is preserved exactly, NOT silently repaired.
Its implementation discards the first three URLs and samples the rest.
`sheet2(rid, 30)` therefore does **not** prove all listing photos were
reviewed, especially with more than 33 images or a failed image fetch.
Use the original full gallery (including the first three and tail images)
to close that evidence gap. Treat failed or unviewed images as a partial
look; do not label their condition or amenities photo-verified.

## Checkpoints

The referenced `appraisal-end-to-end` skill was not supplied. Use the source's
`S3-matrix` checkpoint names directly in the existing
`metadata/stage_log__<slug>.md`, appending timestamp, status and evidence.
Resume from observed state, not an old checkbox/export assumption. No
`exported`/`filed-onedrive` checkpoint before mandatory approval and actual
file verification.
