---
name: titan-appraisal-prep
description: Preps one Renters Warehouse exterior-only (2055 UAD) appraisal in Titan Appraisal from the OneDrive workfile and LOE email. Validated flow (1110 Emily Ln, 2026-10-04) - new no-merge report from the address, generate Flood and Aerial maps there and save images + FEMA, merge the filled template (ZZ TEMPLATE TEST, Forms AND data) over the same report, fix form order, upload images, overwrite only in-scope fields. Stops before comps/adjustments (TrueTracts), Location Map, certification, signing, delivery.
---

## Factory execution adapter (read first)
Read [FACTORY_ADAPTER.md](FACTORY_ADAPTER.md) and [MEMORY.md](MEMORY.md) before following the procedure below. The adapter maps Polar paths/tools to Factory and resolves dated corrections without changing the supplied source. For this installation, do not start a live appraisal unless an active order and the correct browser are available.



# Titan Appraisal prep (Renters Warehouse, Exterior-Only 2055 UAD)

Input: property address (or next starred order). Output: a prepared Titan report left OPEN in the user's tab, plus a flag list. Old experiments and failed approaches: `reference/old-skill-full-history-2026-10-04.md` and `reference/lessons-log-2026-10-02.md` (read only if something below fails).

Status: reproduced end to end on two different orders (1110 Emily Ln, then 2905 Furlong Dr W on 2026-10-04). Still not a guarantee; watch for the differences listed under REPRODUCTION NOTES. If a step misbehaves, stop, screenshot, and tell the user instead of improvising a different merge.

## Hard rules (user-set, binding)
1. NEVER sign, deliver, eSign, or fill CERTIF/certification. NEVER touch comps GC1-3, adjustment grid, market-context fields, neighborhood boundaries/description, market conditions text, Market Conditions Analysis / Adjustment Support pages, Reconciliation, Location Map (TrueTracts owns them; list as "pending TrueTracts").
2. Never edit a signed report (signed ones are only merge sources). Never read /Appraisal-Mirror/Appraisal-Creds/. No fabricated data; flag conflicts and unknowns (leave unknown fields blank).
3. Titan allows ONE login session: work only in the user's Titan tab, sequentially. Login page -> notify_user. Switch reports via File > New Report / Drive > Open, never by pasting a second report URL while one is open.
4. ONE data merge per report, and it must be done AFTER the maps are generated (a data merge overwrites the geocode; the generated map forms and FEMA/census values survive it). Never merge a second time.
5. Manage (add/remove/reorder forms): one change at a time, screenshot to verify the highlighted row and count before each removal; never click the left Available list while removing; arrows lag, so click once per second.
6. Do NOT close the report while the user watches. Leave it open and saved.
7. Never click map zoom (+/-) before Add Map. Never send email without confirmation.
8. Never edit the template report "ZZ TEMPLATE TEST" (clone of 8009 Chesham Dr). It is only a merge source.
9. Before reporting done, verify the FINAL FORM ORDER in Manage against the list in step 7 (the user caught a misplaced Building Sketch once).

## Inputs (OneDrive connector; ToolSearch select ONE_DRIVE_LIST_FOLDER_CHILDREN and ONE_DRIVE_DOWNLOAD_FILE first)
Folder `/Appraisal-Mirror/Motto-Workfiles/by_address/<slug>/`, slug = `<street>_<city>_<st>_<zip>` lower-case with underscores (list by_address ordered by lastModifiedDateTime desc to find it). Use `subject/` listing (orderby name desc; large, results save to a file, grep it for ids). Download via DOWNLOAD_FILE (returns s3url; curl into `/home/user/work/<slug>/`). Staged files do NOT persist across chats: always re-download.
- `subject_realist_tax_pdf__*.pdf` (3 pages; run `pdftoppm -r 130 -png realist.pdf up/pd` -> pd-1..3; `pdftotext -layout` for owner, legal, APN, taxes, zoning, lot, garage). GATE: if missing, STOP and report.
- `subject_improvement_sketch_image__*.png` (missing sketch alone is not a stop).
- `artifact_<slug>_initial_scope__*.pdf` = scope (sharepoint_scout may be empty). `pdftotext -layout` for condition, amenities, structural flags; `pdfimages -f 1 -l 1 -j scope.pdf sc/cover` -> cover-00N.jpg = best FRONT PHOTO (view it; MLS photo_001 and artifact_front_photo.jpg may be the wrong house or an interior).
- Order folder root: `order.json`, e2e_result json, LOE txt in `subject/loe_emails/`. `sfrep/payload.json` is OK for gla/beds/baths/year built; `sfrep/narratives.json` is boilerplate, do not use.
- Gmail connector (lkmotto@gmail.com, `is:starred`) for Purchase Price, ARV, Rehab, Occupancy, Option Ends, order email date.

## Conventions
- Entry method: click the field, Ctrl+A, type (clearing: Ctrl+A, Delete, then Escape to dismiss QuickList popups). Click each field; do not rely on Tab. Screenshot after each batch; layout shifts ~50 px after popups.
- File/invoice number = `M` + street number + MMDD + 2026 (run date), e.g. M111010042026. Invoice date = run date. Due date = Option Ends if no due date exists (flag).
- Image slots (Cover, Subject Photos, Building Sketch, map slots): double-click the dropzone -> file chooser -> `file_upload` with the `filechooser_N` ref. Slots that already hold an old image (Property Data 1, 2, [Scanned Page] Addendum): double-click the image, scroll up 3, click the Image Tools folder icon (first icon in the blue panel), then file_upload.
- "Report is out of sync" popup appears intermittently after Ctrl+S or an edit. Edits were NOT lost: click OK, navigate to the same Forms URL (tab's current report), check, continue. Save (Ctrl+S, wait 15-20 s) after each section.
- Text-overflow prompt ("move to overflow addenda?") can trigger on long entries: keep entries short.
- Checkbox clicks: click the box center, ~15 px LEFT of its label; screenshot first.

## Procedure
1. **Stage inputs** (above). Facts to collect: owner, APN, legal, subdivision, county, tax year/taxes, year built, GLA, beds/baths, lot size/dimensions, zoning, garage, occupancy, purchase price, list price/date/status, order date, option ends.
2. **New no-merge report.** Ctrl+S, then File > New Report. SmartStart: Street, City, State TX, ZIP, description = `<address> vN` (unique). Keep the first radio (Favorite form URAR). OK, wait 30 s. Census tract auto-fills (record it).
3. **Generate maps in this report** (before any merge).
   - Flood: Add Map dropdown arrow (650,48) > Flood Map Only (626,105); the preview MUST center on the subject; Add Map (1088,870); wait 30 s.
   - Aerial: Add Map main button (602,48); Map Type (149,49) > Subject Only (139,100); confirm Yes (768,224); wait 8 s; Page Title (473,49) > Aerial Map (358,99); Add Map (1190,84); wait ~70 s. The aerial is tightly zoomed; that is normal.
   - Save images: execute_javascript, collect `<img>` srcs matching /NetX/ (FLD = flood, LOC = aerial), fetch each with quality=90, credentials include, base64, `file_path` /home/user/work/<slug>/maps.json; decode with python to flood.jpg / aerial.jpg.
   - FEMA: Page 1 Site row (scroll 9 ticks down then 4 up): SFHA, zone, map #, map date. Write to fema.md. Ctrl+S.
4. **The merge.** Toolbar Merge (245,48): Entire report + Forms AND data (defaults). Click the row whose description is exactly "ZZ TEMPLATE TEST" (list reorders: screenshot and verify highlighted row). Merge (1063,829), wait 40 s. Expect: standing fields come in, FEMA/census and the typed address keep the correct values, the generated Flood/Aerial forms are still present, template data (county, owner, legal, APN, taxes, neighborhood, comps, appraised value) is stale until overwritten.
5. **Fix form order in Manage** (File contents: left Manage button ~50,316; wait ~10 s for it to load). Expect 36+ forms starting URAR, Flood Map, Aerial Map, Invoice, Cover Page, ...
   a. Select generated Flood Map (row 2), left arrow (742,441); the next row (generated Aerial Map) becomes highlighted: screenshot to confirm, left arrow again.
   b. Select Invoice, up arrow (742,472) once. Select Cover Page, up arrow once. Order: Invoice, Cover Page, URAR.
   c. Search "building sketch" in Available forms, select "[Digital] Building Sketch" (Most Common), right arrow (742,411). It lands right after Invoice.
   d. Select Building Sketch (highlighted after add), then down arrow (742,503) ONE click per second, 13 times from position 2, until it sits right after "[Scanned Page] Addendum" and before Subject Photos. Screenshot to verify. OK (1066,836), wait 20 s, Ctrl+S.
   FINAL ORDER (36 forms): Invoice, Cover Page, URAR 1-6, USPAP Compliance Addendum, Additional Comparables 4-6, Market Conditions Addendum, UAD Definitions 1-3, Supplemental Addendum, Location Map, Aerial Map, Flood Map, Property Data 1, Property Data 2, [Scanned Page] Addendum, Building Sketch, Subject Photos, Comparable Photos 1-3, 4-6, Reconciliation Addendum, Market Conditions Analysis 1-9, Adjustment Support pages... (Verify the first 17 against this list.)
6. **Order Form** (top menu Assignment > Order Form [Page 1]). Field coordinates (page unscrolled, banner closed): Order Date (532,242), Due Date (793,242), Job Type (532,277) `AS - IS + SUBJECT TO`, Property Type (532,295) `SFR`, Form Type (532,330) `2055`, Sale Price (793,277), Internal order # (1105,182), Main file # (1105,260), Invoice # (1105,323), Invoice date (1105,340), Ordered By (1085,372), Bill To (1085,389), Ship To (1085,475) all `Renters Warehouse`, Base Fee 450 (already). Property block: County (540,404), APN (785,404), Legal (650,422, one wrapped field), Neighborhood = Realist subdivision (760,438), Tax yr (640,456), Taxes (760,456), Year built (437,473), Rooms (543,473; unknown -> flag), Beds (640,473), Baths (745,473), GLA (850,473; MLS/payload GLA, NOT Realist total incl. garage). Owner (590,645). Occupancy checkboxes: Owner Occupied (795,707) uncheck, Vacant (795,742) per email. Then Invoice tab (left list): Due Date (1070,605), TO lines: click line 3 (620,713) Ctrl+A Delete `3701 Wayzata Blvd, Suite 500`, line 4 (620,734) `Minneapolis, MN 55416`. Ctrl+S.
7. **Images.** Contents list (scroll it) or Jump to Forms. Building Sketch dropzone: sketch png. Cover Page: scope cover jpg (double-click "Double click to browse"). Aerial Map and Flood Map slots (template's empty dropzones, titles already correct): aerial.jpg / flood.jpg. Property Data - Page 1, Page 2, [Scanned Page] Addendum: replace old images with pd-1.png, pd-2.png, pd-3.png via Image Tools. Subject Photos: Subject Front dropzone: cover jpg. Wait for "Photo uploading..." to finish (~8 s) each time. Location Map slot stays empty for TrueTracts.
8. **URAR Page 1** (Contents > URAR Page 1; a submenu pops up: click Subject, then scroll). Fix:
   - Assignment Type: LEAVE Other (describe) checked with `Ascertain Market Value` (USER 2026-10-16: RW requests are not purchase transactions; do NOT tick Purchase Transaction). Contract Price is filled from the order form. Contract Analysis popup: Select transaction type must stay `-None Selected-` (clear any template 'Arms length sale'). Financial Assistance popup: the amount field must be EMPTY (template held 2000; delete it, leave Yes/No boxes untouched).
   - Offered for sale Yes (~1067,419) opens "Subject Sale & Listing History": DOM field (~836,336) = days from list date to run date; data line (~780,373): `Per NTREIS, listed MM/DD/YYYY at $X, currently Active.` Click outside to close.
   - Site: Dimensions (~540,845), Area (~770,845, `5,300 sf`), Specific Zoning Classification (~580,863) from Realist, clear Zoning Description (~900,863). FEMA/census come from the geocode (verify they match fema.md).
   - Improvements: Effective Age = 2026 - year built; Roof (e.g. `Comp Shingle` from Realist); clear Chesham leftovers not supported by scope/Realist (gutters, window type, fence, porch, pool, microwave, "Other" appliance text). Keep supported items: fireplace, garage + cars, central air, patio (back door), ceiling fans, appliances in scope. Garage cars inferred from MLS/Realist.
   - Condition: click Additional-features line (~900,744 in scrolled view), Tab; popup: dropdown arrow (~806,590) > Overall C3 (~650,671) (C3 for heavy renovation scope; adjust if the scope says otherwise and flag); comment box Ctrl+A BackSpace then type once: `Per RW scoping visit <date> (est. $<total>): <trades>. Source: RW scope of work; exterior viewed via photographs only (no inspection by appraiser).` Never write that the appraiser inspected the property. Click elsewhere to close.
   - Physical deficiencies: if the scope flags structure (eaves, foundation, brick cracking), type a short note into the describe line (box ticks Yes automatically); flag the judgment.
   Ctrl+S after each section.
9. **Verify and save.** Re-open Page 1 values, Order Form, Invoice, maps, photos, sketch, Realist pages; open Manage and check the FINAL ORDER (rule 9); Ctrl+S; leave the report open. Update `/home/user/work/<slug>/status.md`.

## Report back (always)
Fields filled and sources. Flags: due date source (Option Ends), cover photo identity, sketch vs "no record", garage count inferred, structural Yes judgment, DOM, rehab email vs scope total, Realist-vs-MLS GLA, total rooms (template value if unknown), aerial tightly zoomed, unknown fields left blank. Pending TrueTracts (stale template content): neighborhood boundaries/description, market conditions text, comps grid and Additional Comparables, Appraised Value, Supplemental Addendum narrative, Reconciliation, Market Conditions Analysis / Adjustment Support pages, Location Map. Manual: certification, signing, delivery. Cleanup owed: test reports in Drive (delete lock is time-based).

## UI reference
- Top menu: File (119,15), Forms (533,15), Assignment (~458,15). Toolbar y=48: Merge 245, Contents ~345, Add Map 602, dropdown arrow 650. Orange "Link your TOTAL" banner (close X at 1214,15) shifts coordinates ~30 px when shown.
- Manage ("Add or Remove Forms"): left arrow (742,441), right arrow (742,411), up (742,472), down (742,503), search box (172,172), OK (1066,836), Cancel (1125,836) then Yes (826,188). Forms-in-report list region x 772-1172, y 150-760; first row y~213.
- File menu: New Report (178,44), Close (157,258).
- Drive: https://titanappraisal.com/Desktop; search ~(350,92), Open ~(155,63), Delete ~(496,63).
- Failed approaches (do not retry): Forms-only merge (empty fields); merge BEFORE maps (wrong geocode); separate scratch map report; any second merge; pin drag on Reposition map; USPS re-standardize to fix geocode; zoom before Add Map; batched Manage removals; Photos library import; Street View screenshots (black).

## REPRODUCTION NOTES (2905 Furlong Dr W, 2026-10-04, second run, confirmed the flow)
- Everything in the procedure worked: no-merge report, maps centered correctly (FEMA 48121C0540G Zone X, tract 48121-0217.52 kept after the merge), merge gave 37 forms, same Manage fixes, images, Page 1.
- Differences to expect:
  - Building Sketch inserts AFTER THE CURRENTLY SELECTED ROW. Run 2 it landed at position 3 (after Cover Page) so it needed 12 down-clicks, run 1 it needed 13. Count by watching the list: stop when it is directly after "Addendum" and before "Subject Photos".
  - No sketch image in the workfile (no subject_improvement_sketch file): add the empty Building Sketch form anyway and flag it.
  - Generated forms land in order Flood Map then Aerial Map (rows 2 and 3): remove row 2, row 3 becomes highlighted, remove again.
  - Invoice TO lines sit at different y (street ~441, city ~462, due date field ~1070,332) than run 1; screenshot the Invoice before typing.
  - The left panel layout toggles between a QuickList panel (Report Contents list starts y~353) and a tall one; take a screenshot before clicking Contents items.
  - Template leftover on URAR: stories showed 1, effective age 6, roof "Comp/Good", gutters/window text, fence/porch/pool/microwave/Other appliance, "Offered for sale = No / no known listings", Assignment Type "Other: Ascertain Market Value", zoning description. All must be overwritten (done on Furlong). Occupant Vacant and contract price came through from the Order Form.
  - Condition popup positions differ per scroll: dropdown arrow (806,533) with Overall C3 at (648,614) and the comment line ~ (700,639) in the Furlong layout; screenshot the popup first.
  - Deficiency "Yes" box does not always tick when typing the note: click the Yes box and verify the X.
  - Irregular lot: Realist page 3 map gives side lengths; used `45X109X56X116` and Shape Irregular (flag).
  - Dimensions/Area/Shape/Zoning positions change after Zoning Description is cleared: re-screenshot before editing roof/gutters (a value landed in the wrong field once).
- Out-of-sync popup appeared once (Invoice save); reload the same Forms URL and continue.

## FORM TYPE FIX - VERIFIED (1110 Emily Ln v4, 2026-10-05)
Choosing **Exterior-Only [UAD Version]** as SmartStart Favorite form WORKS. Starter shows "Exterior-Only [Page 1-6]" (`2055UAD_`). After the single template merge the main form is ONE row (no URAR duplicate); 36-37 forms. Manage fixes reduce to: (1) remove generated Flood Map with left arrow (742,441), (2) remove generated Aerial Map (highlighted after first removal), (3) select Invoice, up arrow once, (4) select Cover Page, up arrow once.
- **Building Sketch shortcut (replaces 12-13 down-clicks):** first select the "[Scanned Page] Addendum" row in the right list, THEN search "building sketch", pick "[Digital] Building Sketch", right arrow (742,411). It lands right after Addendum, before Subject Photos. Verify, OK, wait 20 s, Ctrl+S.
- The merge brings stale template data (county Dallas, owner, legal, neighborhood, comps, value) - overwrite everything; Order Form coordinates in step 6 verified again. Order Form "Sale Price" etc. are blank after merge; Invoice TO city line already has a stray "," that can't be removed by typing at (500,733).
- Steps 5/7/9 labels: read "Exterior-Only [Page n]" instead of "URAR [Page n]".

## Stage log checkpoints (see /appraisal-end-to-end "Stage log"; stage id S2-titan-prep)
Read `metadata/stage_log__<slug>.md` first and resume at the last DONE checkpoint. Append a line at: `report-created` (Titan report id/name, no merge), `maps-fema` (Flood+Aerial added, FEMA values saved), `template-merged` (the ONE merge done; never repeat it), `manage-fixed` (form order verified), `order-form-page1` (order form, images, Page 1 done), `saved-open` (Ctrl+S, report left open). Include the Titan report URL/id in the first line so a later stage can find the same report.

## USER CORRECTION (1213 Marcus Ct, 2026-10-09): do NOT overwrite Effective Age or Window Type
- The template's Effective Age (6) and Window Type (`DblePane/Good`) are CORRECT standing values for these orders. LEAVE THEM ALONE.
- Remove "Effective Age = 2026 - year built" and "clear window type" from step 8 Improvements. Same for Gutters & Downspouts unless the user says otherwise (it was cleared on Marcus; ask before clearing standing template values).
- The Window Type field caps typed text at 12 characters, so retyping `DblePane/Good` (13) truncates it. Never retype it; if a value is lost it cannot be restored exactly by typing (Marcus now holds `DblPane/Good`, restored by hand).
- General rule: only overwrite fields that are subject-specific (address, owner, APN, legal, taxes, GLA, beds/baths, year built, lot, zoning, listing, price, dates). Treat template-wide style/condition fields as standing values.
- Titan text fields: Ctrl+A+Delete is unreliable (sometimes removes one character); use click, End, then repeated BackSpace. After closing a popup, do not click blank form space (opens Condition/Contract popups); click the gray margin instead.

## FRONT PHOTO FALLBACK (user-approved 2026-10-09, 1213 Marcus Ct)
When the workfile has no scope PDF/front photo, extract the MLS photo embedded on Realist page 1: `pdfimages -f 1 -l 1 -all realist.pdf img` -> img-000.jpg (900x594, full resolution; better than cropping/enlarging the rendered page). Use it for Cover Page and Subject Front and flag it as the MLS listing photo.

## INCOMPLETE WORKFILE FALLBACKS (user-approved 2026-10-09; use whenever an expected input is missing)
Observed on 1213 Marcus Ct, 2607 Buckskin Dr, 2707 Mountain View Dr: the OneDrive workfile `subject/` folder can hold ONLY `realist_tax.pdf`, `property_detail_report_*.pdf`, `improvement_sketch_*.png` and truetracts json, with NO scope PDF, NO LOE email and NO front photo. Names differ from the list in "Inputs": the Realist file is `realist_tax.pdf` (not `subject_realist_tax_pdf__*`), the sketch is `improvement_sketch_<COUNTY>-<id>.png`. List `subject/` before assuming anything is missing. Do NOT stop for a missing scope or photo; use these fallbacks and flag them in the report:
1. **Order details (price, occupancy, due/option date, ARV, rehab, scope link):** Gmail connector (lkmotto@gmail.com), search the street name (search `"<street name>"`, not is:starred only). Orders from Verni Reyes are "subject to repair" + "as-is"; orders from Dennis Fernandez are "as-is" only (Job Type `AS - IS`, no scope, due date given as Report Due Date). Several orders can sit in ONE thread; read the whole thread (FETCH_MESSAGE_BY_THREAD_ID). No attachments: the scope is a SharePoint link.
2. **Renovation scope PDF (missing from workfile, link in email):** open the link in a SEPARATE new tab (never the Titan tab); links open without login. The folder holds `<address> initial scope.pdf`. Get the bytes with in-page fetch (browser proxy curl fails): `fetch(location.origin+"/personal/<owner>/_api/web/GetFileByServerRelativePath(decodedurl='<server relative path>')/$value",{credentials:'include'})`, keep the blob in `window.__b`, then read it in 2.5 MB slices (`blob.slice(a,b).arrayBuffer()` -> base64) using execute_javascript with `file_path` (each output ~3.3 MB, cap is ~4 MB), rejoin with python (`json.load` each chunk, take `['d']` or `['result']['d']`, b64decode, concatenate). Then `pdftotext -layout`; total est. cost and AI summary are on page 1-2; structural flags are in the AI summary. Compare total with the email Rehab and flag differences.
3. **Front photo (no photo in workfile):** first choice = cover image in the scope PDF (`pdfimages -f 1 -l 1 -j scope.pdf sc/cover`, view it to confirm it is the exterior of the right house). Second choice = the MLS photo embedded in Realist page 1: `pdfimages -f 1 -l 1 -all realist.pdf img` -> img-000.jpg (900x594). Use for Cover Page and Subject Front; flag the source.
4. **Property Data images:** Realist PDF has 4 pages: p1 -> Property Data Page 1, p2 -> Property Data Page 2, p4 (property map) -> [Scanned Page] Addendum. Page 3 (sales history) has no slot; do NOT stitch it into page 2 (renders tiny). Flag the sales history (recent flips) in the report.
5. **Condition / structural note without scope:** leave the template condition text and flag it; with a scope, follow step 8.
6. **Standing template values:** never overwrite Effective Age, Window Type or Gutters; see the USER CORRECTION section.
7. **Unknown fields:** Rooms, zoning, date of contract stay blank and are flagged.

## RUN NOTES (2026-10-09, Buckskin + Mountain View)
- Realist PDF can be 3 pages (not 4): p1 -> Property Data 1, p2 (includes sales history) -> Property Data 2, p3 (mortgage tail + Property Map) -> [Scanned Page] Addendum. Check page count with `pdftoppm` before mapping.
- SharePoint scope folders can also hold a foundation estimate PDF (e.g. Pier Pressure Foundation Repair "Project Proposal"). Read it: "No repairs will be necessary" means Physical deficiencies = No and mention the evaluation in the condition text; the scope AI summary alone may only say "possible movement concerns".
- Scope cover photo can be blocked by a mailbox/vehicle; if the house is hard to see, prefer the Realist MLS photo (img-000.jpg) and flag the source.
- Subject Photos: double-click the FIRST dropzone only after a fresh screenshot of that page (page shifts after save/upload; a photo once landed in Subject Rear). Delete a misplaced photo via Image Tools trash then OK.
- Page 1 section jump: Contents > Exterior-Only [Page 1] > Site (336,478) lands with Dimensions y~807, Zoning y~825. Offered = Yes popup: DOM field (845,298), data line (1000,334) with ~100 BackSpaces before typing; close popup by clicking (1222,500), then re-jump via Contents.
- Invoice page after merge: Due Date (1067,332), TO street line (620,441), city line (700,463, End + 5 BackSpace).

## USER CORRECTION (2026-10-09, Meadowbrook): DO NOT CLEAR FIELDS YOU CANNOT REPLACE
- Do not blank Zoning / Zoning Description (or any other field) just because the template value looks stale or belongs to another property. If the true value is unknown, LEAVE the existing template value in place and FLAG it in the report ("zoning left as template Z236 / Single Family Residential District, unverified"). Clearing creates a blank the user then has to fill and hides that the value was never checked.
- Only overwrite a field when you have a verified replacement value. Clearing is allowed only for text that is plainly wrong and is being replaced in the same step (e.g. the "Ascertain Market Value" Other text when Purchase Transaction is ticked).

## LESSONS FROM PHOENIX (10/09/2026)
- Page 1 checkbox cells need a focus click first and then a toggle click, and display lags; after clicking verify with a full screenshot after clicking elsewhere. Do not click margin (1222,500) on Page 1: it jumped the view and my following clicks hit the adverse-conditions text (restored to "No apparent adverse easements or encroachments.  No adjustment will be made."). Always screenshot before typing after any jump.
- Realist photo is often a stock placeholder; use scope cover and flag.
- Manage order after merge can be Exterior-Only, Flood, Aerial, Invoice, Cover: remove the two maps one at a time then move Invoice, Cover up.

## FEE SCHEDULE (user-set 2026-10-16) - RENTERS WAREHOUSE ORDERS ONLY
Applies only to Renters Warehouse appraisals; do NOT apply to orders from other clients/sources (leave their fees as given).
- Base fee: 450 (line item named for the job type, e.g. `AS - IS + SUBJECT TO`, already on the Invoice).
- Rush Fee 200: add when the due date / "Option Ends" is 1 or 2 days after the order email date (run date). Add as the next Invoice FEES line: description `Rush Fee`, amount `200.00`.
- Measurement Fee 150: add when the LOE/order email alludes to measuring the property (e.g. "measure", "measurements", "sq ft verification"). Add as next FEES line: description `Measurement Fee`, amount `150.00`.
- Same nomenclature/layout: one line per fee under the base line (line 2 = Rush Fee, next = Measurement Fee). Both can apply (total 800).
- In step 6 (Invoice tab) add these lines; compute days from order email date to due date/option ends and flag the fees added (and why) in the report. If the email wording about measuring is ambiguous, add nothing and flag it.


## USER CORRECTION 2026-10-16 (template flaws)
- Assignment Type = Other / `Ascertain Market Value` (not Purchase). Contract transaction type = None Selected. Financial assistance amount = blank (was 2000). FIXED IN THE TEMPLATE 2026-10-16 (ZZ TEMPLATE TEST edited at user's request, verified after reload): transaction type None Selected, financial assistance amount blank (was 2,000), Other/Ascertain Market Value already ticked. Reports merged after this need no edit; just spot-check all three on Page 1 and do NOT tick Purchase Transaction. (Exception to hard rule 8, user-authorized for these three fields only.)

## USER CORRECTION 2026-10-16 (no inspection claims; addendum condition comments)
- We do NOT inspect; the exterior is seen through photographs. Never write 'inspection/inspected/visit' as something the appraiser did, in any typed text.
- ZZ TEMPLATE TEST Supplemental Addendum (Addenda button, editor) was edited and verified after reload: removed the variable end bullet 'Exterior-Only: Improvements - Condition of the Property' (renovation narrative); Scope of Work now 'reviewed photographs of the exterior'; comps 'reviewed using MLS photos'; Inspection Comments now says 'The appraiser did not visit the property. The exterior was observed through photographs...'; 'via photographs' for data sources; Effective Date 'reviewed photographs of the subject property'. Merged reports now need no addendum edit; do NOT add a condition narrative to the addendum.
- NOT editable by us / left as is, FLAG to user: pre-printed form text on Exterior-Only Page 2/4 ('Based on a visual inspection of the exterior areas ... from at least the street', 'date of inspection') and the Certification ('I performed a visual inspection of the exterior areas'). Also Page 1 condition comment in the template still reads 'See attached addenda.' (now points at nothing; step 8 overwrites it per report).
- Titan addenda editor typing quirk: typed text with spaces garbles (spaces land late). Use clipboard write_file + ctrl+v instead (a paste can insert TWICE: check and delete the duplicate with BackSpace). Select text by double-click a word then shift+click the end.
