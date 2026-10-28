
# Matrix Comp Search — Memory

## Confirmed working flow (as of 2026-09-26)
- Reset (broom icon, top-left of criteria panel) clears prior filters but leaves the top speedbar "Residential" category label chip — that's just the search category, not an actual Property Type filter; ignore it.
- Status "Closed" defaults its date range sub-field to "0-90" after selecting — always overwrite to "0-365" (or the correct value) after applying the Closed status.
- Zip Code field: clicking directly at the input coordinate and typing works, but the first attempt after scrolling can land on the wrong element/miss focus — verify the top speedbar area shows the zip echoed and the criteria chip "Zip Code is 'XXXXX'" appears after running search.
- The magnifying-glass Search button next to the speedbar is the ONLY search-submit control (there is no separate "Search" button at the bottom of the left criteria panel) — clicking it submits both the speedbar text AND all panel criteria (with "Include other criteria" checked, which is the default).
- After running, click the chevron/dropdown toggle next to Print (top right of criteria bar) to expand truncated criteria chips (shows "+3" etc. when many filters are active) to verify every filter actually landed, since the sidebar/live grid can update before the formal chip list does.
- Property SubType vs Property Type: confirmed these are two distinct fields further down the panel (Housing Type, Property Type, Property SubType in that order near the bottom). Only set SubType = "Single Family Residence"; leave Property Type untouched/blank.

## Example run
- Subject: <subject-address>, Keller, TX 76248 (GLA 1,981; 0.1924 acres; built 1986; no pool)
- Ranges used: SqFt 1585-2377, Acres 0.15-0.23, Year Built 1976-1996, Pool=No, Photo Count 4-999, SubType=SFR, Zip=76248, Closed 0-365
- Result: 14 matches (zip-code area filter, not radius draw — user didn't request radius this run).

## Area filter preference update (2026-09-26)
- User asked to switch the default area-filter fallback from Zip Code to the subject's City/town (e.g. "Keller" instead of "76248"). SKILL.md updated accordingly — City field is now the primary fallback, Zip Code is secondary/backup only.
- Confirmed the City field in the criteria panel accepts a plain city name (e.g. "Keller") and produces a chip like "Keller" (shown as a city filter, similar UI position to Zip Code, likely via State/County/City "Or" selectors section). Use this field going forward instead of Zip Code by default.
- City field UI: click the "Select" box under City, a modal opens with a Filter textbox + checkbox list; type the city name to filter the list down to one match, check it, click Apply. Same pattern as Property SubType modal.

## Second example run (Carrollton, 2026-09-26)
- Subject: <subject-address>, Carrollton, TX 75007 (GLA 2,096; 0.1928 acres; built 1983; no pool).
- Ranges used: SqFt 1677-2515, Acres 0.15-0.23, Year Built 1973-1993, Pool=No, Photo Count 4-999, SubType=SFR, City=Carrollton, Closed 0-365.
- Result: 219 matches — city-filter area searches for a whole (larger) city can return much higher counts than zip code did previously (14 for Keller zip vs 219 for Carrollton city). This is expected/acceptable per user's explicit preference change; no action needed, but worth flagging to the user when counts are very high in case they want to further narrow (e.g. by subdivision) themselves.

## Third example run (The Colony, 2026-09-27)
- Subject: <subject-address>, The Colony, TX 75056 (from Realist tax PDF; GLA/MLS Sq Ft 1,667; Estimated Lot Acres 0.1779; built 1990; no pool [Pool field blank in PDF]).
- Ranges used: SqFt 1334-2000, Acres 0.14-0.21, Year Built 1980-2000, Pool=No, Photo Count 4-999, SubType=SFR, City=The Colony, Closed 0-365.
- Result: 43 matches — city-filter area search.
- Note: subject PDF was a Realist/CoreLogic tax report (not MLS-formatted); used "MLS Sq Ft" field for GLA and "Estimated Lot Acres" for land size since no direct MLS acres field was present.

## Fifth example run (Frisco, 2026-09-28)
- Subject: <subject-address>, Frisco, TX 75033 (CoreLogic/Realist Property Details PDF; MLS Sq Ft 2,235; Estimated Lot Acres 0.14; MLS Yr Built 2007; Pool field blank -> assumed No).
- Ranges used: SqFt 1788-2682, Acres 0.11-0.17, Year Built 1997-2017, Pool=No, Photo Count 4-999, SubType=SFR, City=Frisco, Closed 0-365.
- Result: 187 matches — city-filter area search.
- Bug encountered: after filling all criteria fields fully in one long session and expanding the criteria-chip chevron (top-right toggle next to Print), the search got stuck in a broken state — speedbar showed "Sorry, criteria not understood" persistently, match count froze at "?", and re-clicking the search/magnifying-glass icon repeatedly did nothing (grid kept showing stale unfiltered rows). Clearing/retyping the speedbar text, pressing Enter, and clicking elsewhere on the page did not fix it.
- Fix: reloaded the whole page (browser refresh) — Matrix preserved Closed 0-365 and Total Square Feet through the reload — then redid Acres/Year Built/Pool/Photo Count/City/SubType from scratch. After reload, the search auto-ran after just adding City (before SubType was even set), landing on the correct 187-match Frisco result immediately, then adding SubType after and re-running kept the same 187 count with "RES SFR" in the speedbar. So if the UI ever gets stuck like this again, don't keep retrying the search button — reload the page and re-enter the criteria (it's fast since most panel fields are simple text entry).
- Note: expanding the chip-summary chevron itself may not be the root cause (did it safely on a different run before), but avoid combining that click with a following search-button click in quick succession — space them out or reload if a "criteria not understood" toast appears.

## Sixth example run (Wylie, 2026-09-28)
- Subject: <subject-address>, Wylie, TX 75098 (CoreLogic/Realist Property Details PDF; MLS Sq Ft 1,777; Estimated Lot Acres 0.184; MLS Yr Built 1983; no Pool field present anywhere in PDF -> assumed No).
- Ranges used: SqFt 1422-2132, Acres 0.15-0.22, Year Built 1973-1993, Pool=No, Photo Count 4-999, SubType=SFR, City=Wylie, Closed 0-365.
- Result: 32 matches — city-filter area search.
- Bug recurred: after applying City (last field entered), clicking the "+3" collapsed-criteria-chip to expand/verify all chips triggered the same "criteria not understood" stuck state as the Fifth run (speedbar froze, match count reverted to 5000+, map/grid reverted to unfiltered). Reload fixed it again, and this time ALL fields (Total Square Feet, Acres, Year Built, Pool=No) survived the reload except Photo Count, which had to be re-entered. City/SubType also had to be redone post-reload.
- Updated rule: do NOT click the "+3"/chevron chip-expansion control after all criteria are entered and the search has already run successfully with the correct match count and map/grid reflecting the filters. It's an unnecessary verification step that has now triggered the bug twice. Instead, verify success by (a) the match count being reasonable/non-5000+, (b) speedbar showing category+subtype abbreviation (e.g. "RES SFR"), and (c) map/grid visibly reflecting the city filter. Only expand chips if truly needed, and if so, do it BEFORE running the final search rather than after.

## Fourth example run (McKinney, 2026-09-27)
- Subject: <subject-address>, Mckinney, TX 75072 (Realist tax PDF; MLS Sq Ft 2,689; Estimated Lot Acres 0.12; built 2005; pool field absent from PDF entirely -> assumed No/no pool).
- Ranges used: SqFt 2151-3227, Acres 0.10-0.14, Year Built 1995-2015, Pool=No, Photo Count 4-999, SubType=SFR, City=McKinney, Closed 0-365.
- Result: 139 matches — city-filter area search.
- Note: some Realist PDFs omit the Pool field row entirely (not just blank) when the property has no pool recorded; treat absence of a Pool field the same as a blank Pool field (assume No) unless another field indicates a pool.
- Note: prior selections (checked rows) from an earlier search in the same tab/session can persist visually into a new search's grid ("3 Selected of N matches") — this is just leftover UI checkbox state, not a filter; doesn't affect actual results. Not worth clearing but worth being aware it can look confusing when reviewing screenshots.

## Seventh example run (Keller, 2026-09-29)
- Subject: <subject-address>, Keller, TX 76248 (GLA 3,041; 0.2121 ac; built 1997; Pool blank -> No).
- Ranges: SqFt 2433-3649, Acres 0.17-0.25, Year 1987-2007, Pool=No, Photo 4-999, SFR, City=Keller, Closed 0-365. Result: 41 matches. Ran smoothly, no stuck bug (did not expand chips). Note: in City modal, must click the Filter box before typing.

## Eighth example run (Allen, 2026-09-30)
- Subject: <subject-address>, Allen, TX 75002 (Realist PDF; Bldg Sq Ft 1,326 used as GLA [Total Bldg Sq Ft 1,770 includes 444 sf garage]; 0.17 ac [7,476 sf]; built 1989; no pool field -> No).
- Ranges: SqFt 1061-1591, Acres 0.14-0.21, Year 1979-1999, Pool=No, Photo 4-999, SFR, City=Allen, Closed 0-365. Result: 46 matches.
- Stale-state bug (chips missing, 5000+ matches) hit again after clicking search; a page reload applied everything correctly (RES SFR, 46 matches). Reload is the fix.

## Ninth example run (McKinney, 2026-10-01)
- Subject: <subject-address>, McKinney, TX 75071 (Realist PDF; GLA 1,595; 0.25 ac [10,744 sf]; built 2003; Pool blank -> No).
- Ranges: SqFt 1276-1914, Acres 0.20-0.30, Year 1993-2013, Pool=No, Photo 4-999, SFR, City=McKinney, Closed 0-365. Result: 23 matches. Smooth run, no stuck bug (did not expand chips).

## Tenth example run (McKinney, 2026-10-01)
- Subject: 5712 Broken Spur, McKinney 75070 (GLA 1,779; 0.13 ac; built 2007; no pool). Ranges: SqFt 1423-2135, Acres 0.10-0.16, Year 1997-2017, Pool=No, Photo 4-999, SFR, City=McKinney, Closed 0-365. Result: 289 matches.
- UI variant: navigating to /Matrix/Search/Residential/Detailed gave a classic form where Total Sqft/Acres/Year Built/Photo Count are SINGLE boxes accepting "min-max" (e.g. "4-999" worked fine), City is an autocomplete (type, click suggestion), Pool is a native select (click, type "N", Tab), and the bottom "Results" button submits. Page viewport resized mid-run — re-screenshot before clicking to avoid mis-clicks (a stray click selected Adobe in Flooring -> 0 matches; reload fixed it).

## Eleventh run (Wylie, 2026-10-02)
- Subject: <subject-address>, Wylie 75098 (GLA 1,331; 0.18 ac; built 1994; no pool). Ranges: SqFt 1065-1597, Acres 0.14-0.22, Year 1984-2004, Pool=No, Photo 4-999, SFR, City=Wylie, Closed 0-365. Result: 31 matches.
- Attached PDF was a wrong/empty Matrix dashboard screenshot. Found real data on OneDrive: Appraisal-Mirror/{{WORKFILES_ROOT}}/by_address/<address_slug>/subject/ (subject_realist_tax_pdf__<slug>.pdf, and __2.pdf is the real Realist report) and metadata/ (artifact_matrix_saved_search__<slug>.json, artifact_intake). If the attached PDF is bad, search OneDrive for the address.
- The new-style panel ("Cross All Property Types") has NO City field. Use /Matrix/Search/Residential/Detailed (classic): click Clear (bottom bar), tick Closed, date box keeps default text so select-all before typing "0-365"; City autocomplete (type, click suggestion); Photo Count single box "4-999" (verify it stuck); Pool select "N"; bottom "Results" link submits. Smooth, no stuck bug.

## Follow-up: 3 as-is / 3 as-renovated picks (1309 London, 2026-10-02)
- User method. AS-IS: sort by $/LivSqFt ascending, match the subject's PURCHASE ppsf (price/GLA; here $225k/1331=$169), check photos, reject anything with nicer materials. AS-RENOVATED: sort ppsf descending (proxy for quality), inspect photos for FULL recent renovation (partial = reject, e.g. original oak cabinets kept), if none move up in price; if still none relax filters. Defaults for this stage: 2-mile radius ON, city filter OFF, acres min 0.05. Marked comps are lost if criteria change (export Spark first or re-mark).
- Workflow tips: set radius in classic Detailed form, then click "Try Our New Search" to convert; collapse left panel (<<) and expand grid to see $/LivSqFt column; clicking MLS# opens a popup tab (Photos tab at ~157,44); check boxes at x~17 to mark.
- Subject scope (OneDrive artifact_renovation_scope json): C4 as-is -> C2 ARV, rehab ~$67k (kitchen quartz/SS, baths, vinyl flooring, paint, HVAC, foundation). LOE: purchase $225k, ARV $300k.

## Spark export + OneDrive filing (2026-10-02)
- Spark export (3 dots -> Export -> Spark) downloads into the sandbox (/home/user/downloads/Spark.csv), not the user's PC. Filed to OneDrive comps/ as comps_matrix_spark_export_csv__1309_london_dr_wylie_tx_75098__4.csv via the OneDrive web UI (no upload connector). SKILL.md rewritten to include the whole narrowing + export + filing flow.
- Picks for 1309 London: as-is <subject-address>, <subject-address>, <subject-address>; renovated <subject-address>, <subject-address>, <subject-address> (weakest).

## User feedback on picks (2026-10-02)
- User agreed with as-is picks and 1300 Wyndham, but replaced 1112 Old Knoll + 1211 Sheppard (flip-grade materials despite top ppsf/proximity) with <subject-address> (21129146) and <subject-address> (21172388), citing higher-quality materials; told me to use listing descriptions too. Final 6: 405 W Oak, 110 Eastridge, 1402 Sheppard, 1300 Wyndham, 1111 Sheppard, 211 Piccadilly. Re-exported -> OneDrive comps/...__5.csv (__4 is the superseded first set; left in place).
- Lesson: my "partial renovation" rejection of 1111 Sheppard (kept old hardwood, mixed baths) was too strict; user weighs material quality of what WAS renovated. Weight quality > ppsf rank > distance.
- 2026-10-02: User wants superseded exports cleaned up ("create clarity"). Deleted my superseded __4.csv (recycle bin) after uploading __5. Left older pipeline files (base, __2, __3, JSONs) untouched. Do this proactively next time.
- 2026-10-02: My uploaded __5.csv vanished once from OneDrive (recycle bin: "Deleted by {{OPERATOR_NAME}}", cause unknown, not me). Re-uploaded; always re-list the comps folder after upload to confirm it persisted. User then explicitly approved deleting the older pipeline comp CSVs (base, __2, __3) so only this run's export remains; JSONs (selected_comps, adjustments*, reconciliation*) left untouched. Only delete older pipeline files when the user says so.

## Revised as-is logic (<subject-address>, Carrollton, 2026-10-04)
- Problem: the old as-is method ("sort ppsf ascending, take the lowest") picked investor/distress sales ($240-275k, $141-151/sf) for a $375k contract ($206/sf). User flagged a ~$100k gap.
- Fix (now in SKILL.md section 3): purchase-ppsf target + +/-15% price band, recency (<=6 months) and distance, read remarks (export shortlist to Spark CSV and read descriptions), reject both too-nice and too-distressed, exclude garage conversions and two-story if subject is single-story, sanity-check that picks sit within ~10-15% of contract before export.
- Shortlist trick: type several MLS#s comma-separated into the Matrix speedbar to get a small result set, Select All, Export > Spark, then read Property Description/Private Remarks in the CSV.
- Matrix results: set per-page to 100 (ref via find) and pull all rows with execute_javascript (tr/td innerText); dedupe by MLS#.
- Popup listing tab: must take a screenshot before clicking in it; Photos thumbnails need ~8-10s to load.

## <subject-address>, Carrollton 75010 (2026-10-05)
- No PDF attached; subject data from OneDrive workfile metadata (artifact_matrix_comp_filter_context_presubmit json: GLA 1,518, 0.1217 ac, built 1989, no pool). LOE: purchase $345k ($227/sf), ARV $420k, rehab $68k, C4->C2. Titan showed site 8,368 sf but Realist/MLS comps (~0.1 ac) match 0.1217, so used 0.05-0.15.
- Filters: SqFt 1214-1822, Acres 0.05-0.15, Yr 1979-1999, Pool N, SFR, Closed 0-365, 2 mi radius -> 26 matches. Pool select: click, type N, Enter submits the form (fine).
- Sign-in: NTREIS login redirects; use sign_in then click Password Login, then re-navigate to the Detailed URL.
- Fetching listing pages in-page with fetch(ToFull?recordId=..) works for remarks; listing popup via navigate to ToFull URL + Photos tab (~157,44) works in a second tab.
- Spark export of 25 listings failed to sync to sandbox (HTTP 400, probably size); 6-listing export synced fine. Keep exports small.
- OneDrive was OVER STORAGE LIMIT (upload blocked). Could not file __3.csv; file left at /home/user/upload/. Do not delete user files to free space without permission.
- Picks: as-is 1108 Creekstone, 1328 Dallshan, 1527 Ranchview; reno <subject-address>, 1528 Raleigh, 1104 Heather.
- 2026-10-06: After the user reset the OneDrive connection storage showed 12.2 GB of 1 TB; uploads worked. Filed comps/...__3.csv (24,163 B) and metadata/stage_log__<slug>.md (first stage log) for <subject-address>. Both verified via LIST_FOLDER_CHILDREN. Re-uploading the log under the same name: choose Replace.

## <subject-address> (2026-10-06)
- Subject GLA 2,171 (MLS) vs Realist tax 1,693; 0.1872 ac; 1991; contract $<amount>; ARV $330k. 101 matches (2mi, no city).
- Picks: as-is 21213832, 21217980, 21188710 (all >6 mo old, flagged); reno 21290000, 21349792, 21328457. Filed as __3.csv.
- Lessons: for 12+ finalists, export ~12 via speedbar MLS# list, read remarks in CSV, then photo-check only top 3. Close export dialog with Close button after export. Existing comps/ already held base and __2 exports from earlier pipeline.

## <subject-address>, Plano 75023 (2026-10-06) - "AS-IS" order (NOT subject-to), as-is comp selection logic
- Order: Renters Warehouse "as-is" appraisal (vacant, purchase $<amount>, due 10/13/26). User wants ONLY as-is comps (no ARV set): best CLOSED comps + 2 LISTINGS (active), reflecting the subject's CURRENT as-is value and condition.
- KEY LESSON: "as-is" = condition TODAY, which is not always the old/dated C4 state. Read the subject's own MLS listing first (include the subject MLS# in the shortlist export). 6729 Macintosh is listed ACTIVE ($475k, 21375438) as fully renovated (white cabinets, quartz-style, wood-look floors, renovated primary bath, painted brick fireplace, two-story, 4bd/2.5ba, 2,328 sf, 1990). So as-is comps = comps in comparable renovated/flip-grade condition, two-story, NOT dated ones and NOT luxury ones.
- Subject data came from OneDrive metadata artifact_matrix_comp_filter_context_presubmit (no PDF): GLA 2,328, 0.13 ac, 1990, no pool. Filters: SqFt 1862-2794, Acres 0.05-0.16, Yr 1980-2000, Pool N, SFR, Closed 0-365 PLUS Active/ActiveCont/KO/Option statuses left checked (so listings show in same grid), 2 mi radius, no city -> 43 matches. Targets: $460k/2,328 = $197.6/sf, band $391k-$529k.
- Logic used: (1) pull all rows, filter to band + ppsf near target; (2) export ~14-row shortlists via speedbar MLS# list (twice) and read remarks; (3) reject dated (oak cabinets/wallpaper: 6900 Barbican, 6841 Douglas Creek, 785 Antoine), too nice (6812 Huntly $250k remodel, 2014 Fox Glen $200k upgrades, 6725 Macintosh $577k full gut remodel w/ new roof/HVAC = alternate only), one-story (2413 Trophy, 1825 Walters, 2037 Cumberland); (4) photo-check finalists; prefer two-story, close in distance/date.
- Picks (5 marked, exported Spark): closed 21197846 7720 Radford ($470k, 04/28/26, 1.1mi, fully remodeled, LVP, new baths), 21210223 6805 Carrington ($440k, 04/30/26, 0.9mi, white cabinets/LVP/quartz, some dated paint+carpet), 21200512 6728 Saddletree ($465k, 05/21/26, 1.7mi, full remodel, 2,031 sf); listings 21211361 6712 Mantissa ($459k, 0.1mi same subdivision, white cabinets/granite/hardwood, carpet up) and 21340883 6817 Wickliff ($425k, 0.6mi, flip-grade LVP/white kitchen, 1986, 3bd). Filed as comps/...__3.csv (base and __2 existed from earlier pipeline).
- Tips: the speedbar MLS# search drops straight into the new UI; checkboxes at x=416 in new grid; Actions = 3 dots (1247,170) -> Export; select Spark then Export then Close. Record IDs via a.href ToFull?recordId; open ToFull in a 2nd tab then Photos tab (157,44). OneDrive deep link needs /personal/bd23459b22a7306d/Documents/ prefix.

## 2026-10-07 lessons (5105 Avery)
- Photo contact sheets: first 12 photos are mostly exteriors; sample 12 evenly spaced from index 3 (photo_sheet.js). Size=4 URLs with their own exk only; do not rewrite Size/Number. Downloading the pool does not speed anything; photos were the slow part.
- User challenges remarks-only grading. Always photo-verify materials; label unverified grades.
- Avery finding: true C4 as-is comps in the $217-293k band are scarce (Walker is the only clearly dated one); light-refresh comps (Treese 5616, Keys 4205, Ragan 5549) sit at $285-347k.

## <subject-address> re-run with full-pool accounting (2026-10-07)
- User asked for "more info on the comps + report as precedent". Rebuilt search (101 matches: 1737-2605, 0.05-0.22 ac, 1981-2001, pool N, 2 mi) and ran the mandatory accounting. 50 comps photo-verified, 51 labeled remarks/rows only. Filed comps/comp_pool_accounting__<slug>.md and __3.csv (earlier __3 from 10-06 did not exist in OneDrive; base + __2 only).
- GLA conflict: Realist 'Building Sq Ft Tax: 1,693 MLS: 2,171' (garage 661, porch 434). Used 2,171 (MLS); flagged. Single-story, 1991, 0.1872 ac, no pool.
- Picks: as-is River Birch 21188710, Salmon Run 21217980, Indiana 21213832; reno Bentley 21251281, Orland Park 21290000, Marigold 21349792 (dropped 4512 Angelina: photos show custom wood cabinets/travertine, not quartz/new-cabinet scope).
- Speed notes: fetch ToFull for 100 comps in background (window.__rem = getRem().then) then poll; execute_javascript has a 30s cap, so start long fetch/photo batches without awaiting and poll. 13 comps/batch photo sheets, 2 batches in parallel took ~60s. Per-page select via find ref + form_input "100"; 101st row appears only after sorting.
- New-UI speedbar MLS# list: select-all checkbox at (416,287), Actions dots (1172,170), Export at ~(830,294), format select: click, type Spark, Enter, then Export (800,241), Close (724,241).
- 2026-10-07: User CONFIRMED 7413 Crosswicks GLA = 2,171 (MLS), not the 1,693 tax figure. Filters and picks stand as filed.
- 7413 Crosswicks follow-up (2026-10-07): user asked to compare comps to SUBJECT photos. Real current-condition photos are in the initial-scope PDF (224 pages, photos from p19+; render with pdftoppm -r 40 and montage): floral wallpaper kitchen/baths, oak cabinets (some open shelves), laminate counters, tile floor, stained blue carpet, damaged front door = C4-/C5 original. The subject/artifact_photo_*.jpg set in OneDrive shows a renovated-looking staged interior (LVP, white cabinets) that does NOT match the scope photos (unresolved; likely other state/listing). LESSON: check subject photos from the scope PDF BEFORE grading as-is comps. More subject-like comps found: 8104 Berkshire 21366518, 6601 Longleaf 21122352, 8008 Paloverde 21275509, 4117 Chelan 21253437, 7321 Briarwyck 21014267 (foundation repair). Comps this dated sell $265-312k vs the $<amount> contract, so the contract is a discount for condition. NTREIS session expired mid-run: sign_in then re-navigate to Detailed URL.

## 7413 Crosswicks follow-up (2026-10-07)
- Brittany Place 21055343 imported alone into TrueTracts session <report-uuid> (Spark: Tarrant, parcel 05845718). Comp 1, no cleanup yet. Other 5 comps still not imported; final set pending user swap decisions.
- Pipeline's `subject/artifact_photo_*.jpg` (38) are actually Brittany Place listing photos, not the subject.
- 7413 Crosswicks (10/07): user's final subject-to comps = Daren 21217003, Keechi Creek 21246602, Seneca 21165479 (TrueTracts session <report-uuid>; as-is comps River Birch/Salmon Run/Indiana kept). Park-view paired analysis (Park Glen Add, 46 no-pool sales since 12/25): regression park premium ~$13.4k (SE 9.4k), 1-story pairs ~0; applied -$<amount> to Keechi (park view across street).

## <subject-address> run (2026-10-07)
- Pool 69 matches (1150-1726 sf, 0.05-0.27 ac, 1970-1990, no pool, 2 mi). Remarks fetched for all via ToFull in 870-char chunks, 16 photo sheets. Picks as-is 21349209/21240147/21234335, reno 21292398/21185938/21257625. Factory had already built a 57-row city-wide Spark CSV; ours is the curated 6.
- Export CSV lands in /home/user/downloads/Spark.csv. Reorder rows (reno ascending price first) before Spark upload so grid comps 1-3 = ARV.

- USER PREFERENCE (2026-10-08): after each /matrix-comp-search run, LEAVE OPEN a Matrix tab with the full candidate pool (type all pool MLS#s comma-separated in the speedbar) so the user can review/check rows; user's checked rows get moved to TrueTracts.

## <subject-address> (2026-10-11)
- Pool 35 (2mi, pool N). Photo contact sheets for 27 (batch all 27 in one non-awaited loop, poll __phd; ~60s total, saved 1.7MB via file_path). Picks: as-is 21180182 (C4), 21350073, 21221685 (C3); reno 21271536, 21085703, 21229778. Filed as __4.csv + comp_pool_accounting md (existing __1-__3 from earlier pipeline run).
- Left tab on the original 35-row search with 6 picks checked (better than speedbar retype, which would drop the marks).
- Pool had few true C4 two-story sales; most sales were C3/mid refresh. NEVER navigate the user's Gmail tab; use create_tab for OneDrive.

## <subject-address>, Coppell (2026-10-13)
- Pool 26 matches (2 mi, GLA 1,138-1,706, 0.05-0.19 ac, 1973-1993, pool N). Contract $<amount> = $216.5/sf; only 3 non-duplex sales in the +/-15% band; every C4 SFR sale was $352-385k.
- My picks (309, 306, 448 as-is; 102, 935, 900 reno) were corrected by user: reno should be 336 Lakewood + 150 Edgewood (fullest renos, distance ignored), 900 Tupelo partial = out; as-is should be 309 Pepperwood + 508 Grace + 224 Willow (near purchase $/sf, C4 not C5/C6). 306/448/900 unchecked as rejects.
- Final checked set exported (7): reno 336 Lakewood, 150 Edgewood, 102 Pinyon, 935 Mapleleaf; as-is 309 Pepperwood, 508 Grace (duplex-remarked, confirm fee simple), 224 Willow.
- Matrix viewport flips 1280x720 / 1324x892: batched clicks abort; re-screenshot. Grid row order can change when the user re-sorts; use JS to read checked rows.
- FINAL 312 Timber Ridge (user): 6 comps = reno 900 Tupelo, 150 Edgewood, 336 Lakewood; as-is 508 Grace, 224 Willow, 309 Pepperwood. User kept Tupelo (close, solid reno) and dropped 102 Pinyon (lowest-cost reno, below bracket); 935 Mapleleaf also dropped. Exported as __4 (reno asc by price, as-is asc by price).

## <subject-address>, Plano 75093 (2026-10-15)
- Subject from OneDrive Realist PDF (1,993 sf, 1 story, 0.18 ac, 1979, no pool). Pipeline's own presubmit filter had null GLA/acres (800-2000 sf, zip scope), so re-ran: 1594-2392 sf, 0.05-0.21 ac, 1969-1989, pool N, 2 mi radius -> 67 matches. Factory-selected comps were never user-reviewed.
- Subject was itself listed (21393131 AOC $425k, renovated-looking); scope PDF photos show dated C4-ish (gray cabs/granite kit, carpet). Rendering scope PDF with pdftoppm -r 30 and sampling pages is a quick condition check.
- execute_javascript: display truncates strings at ~1000 chars but file_path saves FULL output (3.4MB photo sheets worked); no need to chunk if using file_path.
- Picks: as-is 21041622 Cromwell, 21263127 Leameadow, 21347000 Canterbury (+alt 21262971 Boston); reno 21334146 Emerson, 21197798 Atlanta, 21204718 Fremont (+alt 21270121 Lynbrook). Left checked in 67-row grid for user review; not yet exported/filed.

## <subject-address>, Richardson 75081 (2026-10-16)
- As-is order, subject already renovated and listed (MLS 21397266 $410k, "completely renovated"). Purchase $370k = $192.31/sf, pool 195 (2 mi, 1,539-2,309 sf, 0.05-0.25 ac, 1962-1982, pool N, photos 4+, Active+Closed 0-365).
- My picks: closed 1812 Baylor, 3317 Janwood, 3402 Blueridge; active 3029 Burning Tree, 1607 Centenary. User corrections: 1812 Baylor NOT updated (master bath original; I only saw 12 photos), and 1803 Baylor (flip resale $455k) was a clear choice I missed because of the price band and remarks-only grading. Full-photo recheck: Janwood full, Centenary full, Burning Tree full (2 carpeted BRs), Blueridge mid (carpet BRs), 3534 Post Oak full, 3429 Post Oak mostly full, 1311 Edgewood full but small, 803 Edgewood custom/carpet (no).
- User added 1803 Baylor, 1203 Edgewood ($525k), 1309 Northpark ($495k). Logic fixed in SKILL.md section "AS-IS ORDER WHERE THE SUBJECT IS ALREADY RENOVATED".
- sheet2(recordId,30) returns up to 30 photos; one call for 7 comps fits in the 30s limit; save with file_path.
- USER CORRECTION (2026-10-16): as-is-only is a REFI-style assignment: relevance of comps to the subject's current condition matters, price does NOT. Drop the +/-15% price band and purchase-ppsf targeting for as-is-only orders. Purchase-ppsf alignment is only for the dual as-is + subject-to assignment. 1503 Richland (active, 0.3 mi, full reno) was the best active; also flips 1803 Baylor, 1705 Morningstar. Re-review previously rejected comps whenever the rules change.

## <subject-address>, Flower Mound 75028 (2026-10-16) - Mode B
- Realist PDF in OneDrive subject/ (subject_realist_tax_pdf__<slug>.pdf; pipeline presubmit json had null GLA). GLA MLS 2,154 (tax 2,038), 0.1437 ac, 1988, 2-story, no pool. Purchase $405k ($188/sf), ARV $520k, rehab $73.5k, C4->C2. Existing exports base,__2,__3 -> next is __4.
- Filters: 1723-2585 sf, 0.05-0.17 ac, 1978-1998, pool N, SFR, 2 mi, closed 0-365 -> 59 matches ($345-590k).
- Matrix login: sign_in on clareity then navigate to Detailed URL worked directly. js export of 12 photo sheets must be saved in chunks of 12 (file_path truncates ~700KB when one big string; 1.4MB chunks ok).
- Picks left checked for review: as-is 21046241 Newton, 21286293 Bershire, 21315251 Robin; reno 21299256 Pioneer Park, 21351019 Whitman, 21358431 Highdale.

## <subject-address>, Plano 75093 (2026-10-16) - Mode B
- Workfile file names differ from the skill list: subject/realist_tax.pdf, metadata/renovation_scope.json + stage0_loe_scope.json, comps/ has selected_comps.json, spark_export.csv, selected_spark_export.csv (pipeline), no comps_matrix_spark_export_csv__N yet. Realist: 1,993 sf, 0.18 ac, 1979, 1-story, no pool (identical to neighbor 4416). Purchase $<amount> ($197.3/sf), ARV $500k, rehab $87k email / $91.7k scope, C4->C2.
- Same filters as 4416 -> same 67-match pool. Fetching ToFull for 67 comps (6 parallel) took ~40s; photo sheets (24 photos, 4 parallel) for 62 comps ~2.5 min; ph keys are numeric so order = MLS# ascending. Decode to 2 comps/JPEG labeled, 31 images.
- Picks left checked (6 of 67): as-is 21263127 Leameadow ($360k, $197.8/sf, C4), 21041622 Cromwell ($377k, $192.7, C4, 02/2026), 21347000 3301 Canterbury ($430k, $213.5, C4, 10/2026); reno 21136094 Florence, 21193083 Meadowbrook, 21197798 Atlanta. Alternates as-is: 21296956 Big Horn, 21263180 4100 Emerson; reno: 21334146, 21204718, 21113139, 21270121, 21362448.
- Row checkbox click: JS scrollIntoView block center then click (16,483) works every time.
- 4404 Cleveland follow-up (2026-10-16): User ticked 4524 Boston 21318140 (0.3 mi, 08/27/26, full reno, $589k vs $500k ARV) themselves after I passed it over for price; USER RULE: price never demotes an as-renovated comp (added to mode_as_is_subject_to.md). Final checked set = 7 (reno Atlanta, Meadowbrook, Florence, Boston; as-is Leameadow, Cromwell, 3301 Canterbury); filed comps/...__3.csv (7 rows, reno ascending then as-is ascending; base and __2 were pipeline files). Spark import used a 6-row CSV (dropped Florence, oldest reno) -> flag to user.
- TrueTracts session for 4404 Cleveland: <report-uuid>. Polygon Preston/Coit/Parker/Plano Pkwy = 566 props, 257 filtered. Cost approach: Q4.5, eff age 6, land $<amount> (assessed), garage 466 sf Q4 -> $<amount> (Q4.0 = $<amount>). Not exported from Spark yet.
- Matrix/TrueTracts sign-in: TrueTracts session expired -> sign_in then Continue. Matrix viewport flips 1280x720/1205x892 abort batched clicks.

## <subject-address>, Lewisville 75077 (2026-10-16) - Mode A
- Subject: already renovated + listed (MLS 21402645 $485k, full reno, LVP/quartz/new baths), 2-story, MLS 2,863 sf, 0.228 ac, 1976, no pool. Purchase $<amount>. Workfile has Realist PDF (subject_realist_tax_pdf__...pdf) but no LOE; Gmail email said as-is.
- Pool N 2 mi 1966-1986 2290-3436 sf = only 10 matches (1 reno). Dropped pool + 4 mi radius = 22 matches. Closed comps with 1 photo (3303 Cottonwood, 1301 River Oaks, 2312 Channing) cannot be photo-graded (sheet2 n=1); Photo Count 4+ in new UI left panel is two Min/Max boxes.
- Picks left checked (5 of 22): closed 21373731 Glenhill, 21204082 Havencreek, 21098324 Lake Vista N, 21032140 Claremont (10/2025, old); active 21398311 Wisteria. Alt: 21199003 Gregory. Not exported yet.

## <subject-address>, Plano 75023 (2026-10-17) - Mode B
- No OneDrive workfile yet (order email 29 min old); subject data from public listings (MLS 21292534 / Redfin): GLA 1,873, 8,276 sf lot (0.19 ac), 1977, 1-story, no pool assumed. LOE (Gmail): purchase $<amount> ($197.55/sf), ARV $<amount>, rehab $<amount>, occupied. Unverified vs Realist.
- Filters: 1498-2248 sf, 0.05-0.23 ac, 1967-1987, pool N, SFR, 2 mi, closed 0-365 -> 175 matches (all pool=No). Remarks fetch for 175 in ~60s; 76 comps photo-sheeted (24 photos).
- Lesson: keyword prefilter on remarks MISSED 1700 Throwbridge (0.1 mi, full custom reno, $515k). Always photo-check top-ppsf rows too, not just keyword hits.
- Checked: as-is 21263127 Leameadow, 21186655 909 Harvest Glen, 21211376 1512 Windy Meadow; reno 21204589 1700 Throwbridge, 21322505 2201 Parkhaven, 21285442 2713 Bengal, 21355155 <subject-address>. Not exported yet.

## <subject-address>, McKinney 75070 (2026-10-19) - Mode B
- Workfile existed (pipeline comps base,__2,__3 from 10/14 automated run, never user-reviewed, no stage log) so ran the skill; thread/stage-log check showed no prior matrix-comp-search run. User said "if already done, TrueTracts" -> not done, so search first.
- Realist PDF in subject/ (subject_realist_tax_pdf__<slug>.pdf, find via ONE_DRIVE_SEARCH_ITEMS "<address> realist"): GLA 1,857 (MLS; tax 2,272 incl garage), 0.14 ac, 1996, 1-story, no pool. LOE: purchase $300k ($161.5/sf), rehab $80k (scope $84.4k: roof damage/water intrusion, new HVAC, kitchen/baths, LVP). "subject to repair" + "as-is".
- Filters: 1486-2228 sf, 0.05-0.17 ac, 1986-2006, pool N, SFR, closed 0-365, 2 mi, photos 4+ -> 95 matches. Remarks for 95 in ~20s, 73 photo sheets (closed >= 1/15/26, 24 photos, 5 workers) ~3 min; ph1-3.json in 25-comp chunks worked.
- Picks left checked (6 of 95), not exported: as-is 21349949 4424 Santa Fe ($165/sf), 21322730 4910 Silverweed ($163), 21337465 4404 San Fernando ($190); reno 21227702 4405 San Mateo, 21206576 <subject-address>, 21250108 4427 San Fernando. Next: user review, then export as __4, then /truetracts.

## <subject-address> (McKinney, 2026-10-19), Mode B
- Final set 10 comps (7 renovated incl. 4 user additions + 3 as-is), filed as comps_matrix_spark_export_csv__...__4.csv. TrueTracts session <report-uuid>. ARV pass Q4.0 $<amount> exported; as-is pass Q1.8 $<amount>. Range $413k-$453k with as-is comps rated 0.
