---
name: matrix-comp-search
description: Manual Renters Warehouse MLS Matrix comparable search. Separate as-is-only and as-is plus subject-to modes, photo review, mandatory full-grid user approval, Spark comps and subject exports, and workfile filing. Not creative-finance lead screening.
disable-model-invocation: true
---

## Factory execution adapter (read first)
Read [FACTORY_ADAPTER.md](FACTORY_ADAPTER.md) and [MEMORY.md](MEMORY.md) before following the procedure below. The adapter maps Polar paths/tools to Factory and resolves dated corrections without changing the supplied source. For this installation, do not start a live appraisal unless an active order and the correct browser are available.

This workflow runs an on-demand comparable-property search in MLS Matrix (NTREIS) for a subject property, narrows to the best as-is and as-renovated comps, marks them, exports them in Spark format, and files the export in the subject's OneDrive workfile.


Trigger: user invokes this manually. Manual/on-demand only; never schedule it.

## STEP ZERO: PICK THE MODE (two independent logic files; never mix them)
Read the LOE/order and decide, then read ONLY the matching file and follow it for subject-condition analysis, candidate ranking, picks and report:
- **AS-IS ONLY** (as-is value only; no ARV/subject-to/scope) => `/home/polar/workflows/matrix-comp-search/mode_as_is_only.md`. Refi-style: relevance to the subject's current condition; price/ppsf never matters.
- **AS-IS + SUBJECT-TO** (purchase + renovation scope, ARV, two valuation groups) => `/home/polar/workflows/matrix-comp-search/mode_as_is_subject_to.md`. 3 as-is (aligned to purchase $/sf) + 3 as-renovated (fullest renovations).
- Unsure => read the LOE and any scope PDF; "as-is" alone = Mode A. If still unclear, ask the user.
Edits to one mode's logic must not change the other file. This SKILL.md holds only the shared mechanics (subject data, filters, search build, photo tooling, user review, export, filing, reporting skeleton).

## 0. Subject data (PDF first, OneDrive if the PDF is bad)
1. Read the attached PDF (pdf skill). Extract: GLA (use "MLS Sq Ft"/"Building Sq Ft", not Total Bldg Sq Ft which includes garage), land acres ("Estimated Lot Acres"), year built, pool (blank/absent = No), address, city, zip.
2. If the PDF has no usable data (e.g. a screenshot of an empty Matrix page), do NOT guess. Search the user's OneDrive for the address (ONE_DRIVE_SEARCH_ITEMS, search_scope "drive"). Workfile layout: `Appraisal-Mirror/{{WORKFILES_ROOT}}/by_address/<street>_<city>_<st>_<zip>/` with `subject/` (subject_realist_tax_pdf__<slug>.pdf; the `__2.pdf` is often the real Realist report), `metadata/` (artifact_intake, artifact_matrix_saved_search, artifact_renovation_scope.json, artifact_stage0_loe_scope.json), `comps/` (existing comps_matrix_spark_export_csv__<slug>[__N].csv, selected_comps.json, adjustments*.json) and the LOE text (purchase price, ARV, rehab). Download via ONE_DRIVE_DOWNLOAD_FILE (then curl the s3url).
3. From the OneDrive artifacts also pull: purchase price (as-is ppsf basis = purchase price / GLA), ARV, as-is vs ARV condition (e.g. C4 -> C2), and the renovation scope summary (finishes: cabinets, counters, flooring, baths, etc.).

## 1. Compute filter ranges
- GLA: subject GLA +/-20%. Acres: subject acres +/-20% (round to 2 decimals; Matrix rejects 3+). Year built: +/-10 years.
- Photo count 4-999. POOL FILTER MUST ALIGN WITH THE SUBJECT'S POOL STATUS (added 2026-10-07, user request): subject has pool => Pool = Yes; no pool / blank / absent in Realist => Pool = No. Run the aligned-pool search FIRST. Only relax (drop the pool filter, or run a second pass with the opposite pool status) when the aligned pool yields too few quality comps (fewer than ~3 usable as-is or ~3 usable as-renovated), and say so in the report (a pool comp needs a pool adjustment). If the aligned pool is thin, report how many usable comps each pool status offered. Closed, 0-365 days. Property SubType = Single Family Residence (never set Property Type).
- Area: 2-mile radius around the subject, NO city filter. Acres MINIMUM lowered to 0.05 (keep the +/-20% max). (First-pass default before the narrowing stage was City = subject city; the user now wants radius + no city + 0.05 min acres by default so distances can be seen at a glance.)

## 2. Build the search (new search UI is the user's preference)
- Matrix's new-style panel has no City field and its map radius draw is unreliable. Use the classic form only as a setup tool: `https://ntrdd.mlsmatrix.com/Matrix/Search/Residential/Detailed`. Wait for load, click Clear (bottom bar), tick Closed, select-all in the closed-date box before typing 0-365 (it keeps default text), enter Sq Ft "min-max", Acres "min-max", Year Built "min-max", Pool select "N", Photo Count "4-999" (re-check it stuck), and for the radius type 2 in "Within ___ miles of" plus the subject full address, then accept the geocoded suggestion. Add City only if the user wants it. Click the bottom "Results" link.
- IMMEDIATELY click "Try Our New Search" (top-left) to convert the search into the new UI. Do all review there. Never review in the classic grid.
- In the new UI: collapse the left criteria panel (<< at top-left) and expand the grid (arrows at right) so the Distance and $/LivSqFt columns are visible; sort by $/LivSqFt by clicking that header (toggle asc/desc).
- Do not click the "+N" chip-expansion control after searching (has triggered a "criteria not understood" stuck state; reload fixes it).

## 3. Candidate narrowing and picks
Follow the selected mode file (Mode A: `mode_as_is_only.md`; Mode B: `mode_as_is_subject_to.md`). Shared mechanics below.
- Read the listing description/remarks for every finalist and combine with photos.
- MARK the picks with the row checkboxes (x~17) in the new-UI grid. Marks are lost if criteria change, so export before changing filters. To select programmatically for the user: JS `tr.scrollIntoView({block:'center'})` on the row, then click the checkbox at (16,483); use the check-list dropdown at the top-left of the grid > Clear Selected to start over.

## Shared tooling: photo contact sheets
Load `/home/polar/workflows/matrix-comp-search/photo_sheet.js` with execute_javascript `code_file` on the results tab. `sheet2(recordId, N)` returns up to N photos as one contact sheet (use N=24-30 so every bath/bedroom shows; `batch2` gives 12 evenly spaced photos only for a cheap first screen, never enough to grade). Run in the background (`window.__x={}` filled in a loop, poll a done flag), save with `file_path`, in chunks of ~15 comps per file (a single huge JSON string gets truncated), decode with PIL, label each (MLS#, address, sf, price, date, distance) and view with `read` (4 per JPEG at 900px wide works). Record ids come from each row's ToFull link (recordId=...).

## 4. Export in Spark format
- Top-right three vertical dots (Actions) -> Export -> choose format "Spark" -> Export. Verify the dialog says "Export N Listings" for the number of checked comps. The download lands in the sandbox at `/home/user/downloads/Spark.csv` (it does not save to the user's machine). Check it has N rows with the expected MLS numbers.

- SUBJECT SPARK EXPORT (feature, user request 2026-10-21): when the subject has an MLS listing, ALSO export it as its own Spark CSV after the comps export (details in the mode file, A4b for Mode A; do the same in Mode B). Type the subject MLS# in the shorthand box, check the single row, Actions > Export > Spark (dialog says 'Export 1 Listing'; the format select needs click, type Spark, Enter), copy `/home/user/downloads/Spark.csv` (it is overwritten by each export, copy immediately) to `comps_matrix_spark_export_csv__<slug>__subject.csv`, and upload it with the comps file. The shorthand search replaces the pool, so do it last; Recent Searches restores the pool.

## 5. File the export in the OneDrive workfile
- Copy to `comps_matrix_spark_export_csv__<slug>__<N>.csv` where N is the next unused number (existing files: base, __2, __3 ...). Never overwrite existing files. If you re-export after the user revises the picks, upload the new export as the next N and then delete ONLY the superseded export that this run created (OneDrive recycle bin, via the web UI: select that single row, Delete, confirm) so the folder is unambiguous; never delete exports or JSON files from earlier pipeline runs.
- There is no OneDrive upload connector tool. Upload with the browser: open `https://onedrive.live.com/my?id=%2Fpersonal%2Fbd23459b22a7306d%2FDocuments%2FAppraisal%2DMirror%2FMotto%2DWorkfiles%2Fby%5Faddress%2F<slug with _ as %5F>%2Fcomps&view=0` (the id=/Appraisal-Mirror/... form without /personal/.../Documents fails), click the blue + -> "Files upload", then use file_upload with the intercepted filechooser ref. Verify with ONE_DRIVE_LIST_FOLDER_CHILDREN (folder_item_id of comps, use_me_drive true, orderby lastModifiedDateTime desc).

## 6. Report back
Subject details (and where they came from), filter ranges, area filter used, match count, the 3 + 3 picks with distance, sold price, ppsf and a one-line photo-based condition note for each, rejected near-misses with why, alternates, the OneDrive file names (comps and __subject), and a clear note of anything uncertain. Leave the results on screen in Matrix with the picks checked.

## Stage log checkpoints (see /appraisal-end-to-end "Stage log"; stage id S3-matrix)
Read `metadata/stage_log__<slug>.md` first and resume at the last DONE checkpoint. Append a line at: `subject-data` (GLA/acres/yr/price/ARV noted), `search-built` (match count + filters), `shortlist` (MLS#s reviewed), `picks-marked` (6 MLS#s), `exported` (file name, N), `filed-onedrive` (or BLOCKED storage full). Marks and the search live only in the Matrix tab, so after `picks-marked` without `exported` the resume step is "re-run the search and re-mark".

## USER REVIEW OF SELECTIONS (MANDATORY EVERY RUN; user request 2026-10-13, <subject-address>)
The user wants to review and edit the picks IN the full search session, not as a pasted MLS# list. Every run, after choosing the picks and BEFORE exporting/filing:
1. Leave the Matrix tab on the FULL search results (new UI, the whole pool, e.g. 65 matches) with the picks CHECKED in the grid. Do NOT replace the grid with a speedbar MLS# list for the user's review (a shorthand list replaces the pool; if you used one to export, press browser Back to restore the pool, then re-check the picks by paging; checkmarks are cleared on Back).
2. Re-check the picks across all grid pages (25 rows per page; checkmarks persist when paging). Verify the header says "N Selected of M matches".
3. Report the picks (as-is / as-renovated, with distance, price, date, condition note) and tell the user the session is ready to review. Warn them not to click the speedbar search icon (it re-runs the pasted text and drops the pool). STOP and wait for the user to review/add/remove selections.
4. When the user says go, READ the final checked set from the grid (page through all pages; JS: rows with input[type=checkbox].checked, de-dupe by MLS#, the grid is rendered twice in the DOM) because the user may have added or removed comps. The checked set (not your original six) is the final selection. Export THAT set. To export: use Actions (3 dots) > Export > Spark DIRECTLY from the full grid with the final set checked (the dialog says 'Export N Listings'); do NOT paste the MLS#s into the speedbar (that replaces the pool and clears the checks). MODE B ONLY: reorder the CSV rows as-renovated first, then as-is (TrueTracts/Spark expect ARV comps first; renovated ascending by price, then as-is ascending by price). MODE A: no reorder needed; keep grid order or order by closeness.
5. Export the user's final set as the Spark CSV and file it (next __N). Flag in the report which comps were user additions.
Example (3304 Sedona): picked 6, user added 5 (2704 Aspen, 3211 Juniper, 2900 Breckenridge, 4912 Basil, 2612 Cheverny) for 11 selections.
