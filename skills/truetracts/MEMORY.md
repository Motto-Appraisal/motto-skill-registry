

## Learnings from <subject-address> run (2026-10)
- Spark Cost Data "+" unresponsive to clicks: use execute_javascript `document.getElementById('costplusbutton').click()` then click `.costuploaditem` "Import Subject From Spark Grid" via JS.
- TrueTracts grid header drag-reorder doesn't work: reorder CSV rows (ARV asc by price first, then as-is), trash comps, re-import via Spark (needs subject + Cost Data again).
- Grid Cleanup text cells: type then Tab, never Enter.
- Set subject quality equal to ARV comps (Q4), not Factory default Q4+, else spurious $22.5k quality adj.
- Export downloads (workfiles.zip, Report.tdcx) go to user's machine; sandbox sync can fail HTTP 400 - ask user to file them.
- Heatmap boundary: scroll page via right panel, then wheel-zoom on each edge; whole polygon visible at default after ~16 ticks.

## <subject-address> run (2026-10-06)
- Create Report form had EMPTY prefill (no APN/GLA): type year built, GLA, lot sf, acres, beds, baths, stories, garage, then Quality/Condition dropdowns; Create stays disabled until bedrooms filled.
- Subject polygon "The Colony central" gave 703 SS props with no tuning. 1004MC box coords (after scrolling to bottom, then up): see screenshot method; Add 1004MC row order differs by row.
- Spark: Subject Type defaults County to Tarrant; retype county (Denton) and APN as "R00673" worked. Comps CSV was pre-ordered (ARV asc price, then as-is) so grid order is right with no drag.
- Cost: Q4.0 age6 land(assessed) -> $382.6k; Q4.5 -> $420.1k (step is ~$37k here, bigger than London's $25k). Left at Q4.0 pending user.

## <subject-address> re-run (2026-10-06 evening)
- CSV ORDER CAN BE AS-IS FIRST: the 6-row Spark CSV had as-is comps in rows 1-3 and ARV in rows 4-6. Identify ARV comps from submarket_thesis.md / reconciliation_arv.json (the "Subject-to (ARV)" set), then reorder CSV (ARV asc price, then as-is) BEFORE importing. Fixing later needs: trash all 6 comps (trash icon, confirm), Import Comps with Spark again, subject Type + Cost Data + Export again.
- Grid Cleanup: TAB moves DOWN the column in some rows and RIGHT in others; it overwrote bedrooms/baths/GLA once. Safer: click cell, type, then click a row label (works for most) or press Tab only once and verify. Always re-read get_page_text after edits.
- Viewport was 1512x804 this run: cost-form coords differ (Quality 287,228; Garage SF 306,424; Garage Q 388,424; Eff Age 306,506; Site 491,520; Export button 1390,26; Get Cost Data 1257,26). Reconciliation: Rating "0" option at y~444; cell edit = triple_click + type + Enter.
- Reconciliation concessions/time/rooms zero rules applied; photo check showed pergola (not covered) on comp 1 and front covered porch only on comp 3.
- Export templates: boundaries from heatmap: N edge runs through backyards (used Lebanon Rd), S edge parallels Memorial Dr, E=Southern Hills Dr, W=Main St.

## <subject-address> run (2026-10-08)
- Session was created by hand (detached, 2055) with polygon + 1004MC already set; Import Comps with Spark ran directly from Grid Cleanup. Spark Subject Type: County Dallas + Parcel ID "28201610030130000" (account number from CAD) worked.
- Spark cost form at 1512x804: Quality (287,228), Garage SF (306,424), Garage Q (388,424), Eff age (306,506), Site (491,520), Get Cost Data (1257,26), Export (1390,26), Go (755,426), Open Updated Session (773,179). Q4.0/age 6/land $<amount>/484sf garage = $<amount>.
- Built-in features: "Selected Adjustment" box may stay blank after clicking a cost-table cell (text shows $[MISSING SELECTED ADJUSTMENT]); type the value in the box + Tab. Carport built-in default now $<amount> per carport.
- Grid Cleanup subject Condition dropdown: click field then option; comps/subject cells editable at same row y with triple_click + type + click row label. Garage adjustment is per space ($<amount> GAM) so a carport comp gets +14,200 garage and -4,000 carport.
- Reconciliation rating dropdown: "0" is last item (~380px below field); setting comps 4-6 to 0 moved the range to $293k-$315k.

## 2521 High Pointe (8-comp run, 10/11/2026) learnings
- Grid edit cells: after each Enter wait ~3 s before the next triple_click+type, otherwise edits silently drop (batched edits lost 2 of 4). Enter moves focus down a row; verify with JS (inputs are all in DOM; read rows by label y and input x).
- Reconciliation Rating dropdown "0" is ~380 px below the field; the rating box sits to the RIGHT of its "Comp N" label.
- Realist lists a detached carport (400 sf) and "Garage Type Enclosed 462 sf" for converted-garage subjects: ARV (scope reconverts garage) vs as-is garage adjustment is a judgment call; I zeroed garage on ARV comps 1-4 only and flagged it.
- MLS "CvPat" labels can be wrong: photo check (viewer, Down key per comp) showed comp 2 had only a slab, comp 5 (as-is) a big covered patio, comp 3 a bedroom fireplace despite MLS "none".
- Feature Adjustment peer cells: Fireplace median $<amount>; Covered Patio small ~$<amount>; Carport $<amount>.
- Held the Export step because flagged adjustments remained (skill rule).

## <subject-address>, Coppell (Oct 2026) learnings
- Pipeline had already created the TrueTracts session (2055, polygon drawn); resume it instead of creating a new one.
- Grid dropdown option lists are viewport-fixed: screenshot then click. Browser zoom/zoom action do not work.
- Photo check fast path: in Matrix tab fetch last 12 photos per comp (sheetTail via ToFull PHOTOS tab), stitch with PIL; backyard shots are at the end of the photo list.
- Grid defaults to fix: subject Porch "Deck" and Pool "None/Spa" unsupported by photos; subject Quality Q4+ -> Q4.
- GLA: peer median $80 typed (GAM said $120, cost $125) - flag. C4 to C2- card zeroed (-0 Locked). Added Covered Patio $<amount> (Small/Good) and Shed $<amount> (Small/Average).
- Reconciliation: after Rating 0 on comps 4-6 the range is renovated-only ($445k-$467k). The page scrolls itself after each cell edit; re-scroll right+down before each edit. A cell left highlighted after a prior Enter is already in edit mode.
- Time-adjustment rule: zero when closed within 6 months of today (>= ~04/13 when today is 10/13); only Edgewood (01/26) kept 12,300.

## <subject-address>, Carrollton (10/13/2026)
- A TrueTracts session already existed (pipeline-created, polygon with only 69 SS). Redrew: zoom OUT one tick (+/- at 75,180), corners (585,295),(835,295),(835,520),(570,520),(528,430), close on first -> 110 SS / 964 CS. Draw corners under y~560 are hidden by the bottom banner; chat widget pops up if you click near bottom-right.
- 1004MC for this market (13/9/5 sales etc.): sales Declining, absorption Declining, active listings Increasing, months supply Increasing, sale price Stable, sales DOM Declining, list price Stable, listing DOM Increasing, sale/list Stable, concessions Yes+Increasing, REO No.
- Spark accepted an 8-row CSV (4 ARV + 4 as-is). Subject: County Denton + Parcel "R117445". Spark subject GLA = Realist 1303 vs MLS 1307; set cost GLA to 1307.
- Cost: Q4.0, age 6, garage 420 sf Q4.0, land $<amount> -> total $<amount> (below ARV comps 349-415k; user likely nudges quality up).

## <subject-address>, Arlington (10/13/2026)
- Factory session existed (<report-uuid>) but was form type 1004, Q4+/C3+, no polygon: fixed via Market Definition > Modify Property Info (set 2055, Q4, C3), then drew polygon (355 SS) with corners (380,280),(1000,240),(1000,550),(530,550) after Draw Market Area.
- Spark subject: County Tarrant + Parcel "04817559" worked; 7-row CSV accepted (4 ARV + 3 as-is). Cost: GLA 1484, garage 437 sf, age 6, land $<amount> (Realist assessed): Q4.0 = $<amount>; Q4.5 = ~$309k (kept 4.5 to approach ARV comps).
- Spark JS: click costplusbutton and the "Import Subject" item in ONE execute_javascript call (menu closes between calls).
- Grid Cleanup dropdown options for Quality sit left of the field arrow (Q4 ~ (arrow_x-194, 482)). Imported Spark subject had lot 6,795 (set 6,778), garage 0, no energy value; comp 1 garage 0, comp 2 heating blank.

## <subject-address> learnings (10/13/2026)
- Always grep pool.json remarks for patio/porch/fireplace/shed/carport BEFORE Grid Cleanup labels; Silver Maple's "covered patio" was only found late (needed Grid Cleanup fix + -3,800 in Reconciliation).
- Reconciliation edits: after each recalculation re-scroll (left 40, right 6/30, down 20; Total Rooms row = then up 7, y~481; Porch y~537, Fireplace y~573). Analysis Mode is the default on entry; click Full Grid View (325,113), wait, then scroll.
- Grid Cleanup edit: triple_click cell, type, click row label (x=110) to commit.
- 8 comps (4 ARV + 4 as-is) were accepted by Spark/TrueTracts; flag to user.

## Yorkford 2026-10-13 (Reconciliation lessons)
- Reconciliation grid cell edit: triple_click adj cell, type, Enter, wait 3s, Escape. Enter moves focus down a row, Escape closes. If the page auto-scrolls mid-batch, later edits land in wrong rows (put -3,600 in Financing, 4,000 in Concessions); do ONE edit per call + screenshot, and fix strays by typing 0.
- A white (not red/green) adj value = default/unchanged, NOT counted in Adj. Price. Retype a different number then the real one (e.g. -1500 then -1600).
- Feature Adjustments: Fireplace peer median was 4,000 (not 5,000); Deck peer median 2,000 (Selected box needs ctrl+a before typing); Covered Patio S/Good 3,600; Shed S/Avg 1,600; Carport 3,800. GLA peer median 70 typed -> Locked. Garage default 8,100/space applies automatically.
- Bedrooms card has no include box when counts match; Stories box at card top, uncheck.
- Reconciliation Analysis Mode: rating dropdown "0" option ~380px below field; page text can be read with get_page_text (subject first).

## <subject-address>, Plano (10/15/2026)
- Pipeline session d118d001 had polygon of only 40 SS (tiny box), Q4+/C3+, lot 7,840. Fixed via Modify Property Info (lot 7753 per Realist, Q4, C3); Redraw polygon Preston Rd (W) to Independence Pkwy (E), y 215-540 => 119 SS / 522 CS (min met, under 150 target).
- Grid Cleanup showed Option 1/2 chooser (clean slate). Spark accepted 10-row CSV (6 ARV + 4 as-is); Subject Type: County Collin + Parcel "R018200801201" worked.
- Cost: Q4.0, age 6, garage 451 sf Q4.0, land $<amount>, site 7753 => $<amount>.
- 1004MC for this market: sales Declining, absorption Declining, active Increasing, supply Increasing, sale price Increasing, sales DOM Declining, list price Stable, listing DOM Increasing, sale/list Stable, concessions Yes+Increasing, REO No.
- Stopped after Cost Data (no Export from Spark yet).
- 4416 Cleveland (cont.): user pared to 9 comps (5 ARV: Atlanta, Florence, Boston, Lynbrook, Emerson; 4 as-is) and exported Spark -> TT; the Spark export tab opens a NEW TT tab (old one closed). Grid Cleanup Design first field is a dropdown (pick Detached); Spark subject came in with blank Design/Energy/Porch/Pool/Exterior/Ownership/Total Rooms.
- Reconciliation Full Grid View: page jumps to top after each cell edit, so scroll down 30 before each edit; cell edit = triple_click+type+Enter+wait 4+Escape worked (porch y709, fireplace y745, exterior y817 at bottom scroll; concessions/time rows at top scroll y667/y703). Rating "0" option is 381px below field.
- Back photos: /home/user/work/tail.js (tail2/runTail) fetches last 12 photos per comp in Matrix tab; good for patio check.
- Result: ARV-only supported range $504k-$543k (5 comps) after as-is rated 0. Stopped before export for user review.

## User expectations (2026-10-16, 3300 Stone Bridge)
- COST APPROACH for as-is + subject-to: the ONLY lever is subject Quality. Manipulate Quality (decimals OK, e.g. 4.9) so the cost-approach Total emulates the as-renovated (ARV) value as closely as possible (target = order ARV / adjusted ARV-comp value). Everything else is standard: GLA fixed to MLS, garage SF from Realist, garage quality = subject quality, effective age 6, assessed land value, site improvements $<amount> default. Do not stop at Q4.0 and ask.
- Import ALL checked comps the user leaves selected in Matrix (user additions are picks, not "alternates"); ARV comps ascending first, then as-is. Don't reinterpret user additions; ask if unclear BEFORE filing.
- Spark/Cost Data layout glitch with odd window size: click Grid, then Cost Data so it resizes to the window.

## 3300 Stone Bridge (2026-10-16) learnings
- Housing Trends checkboxes on Market Analysis p1 are auto-set; no manual action needed.
- Export tab: click Export, wait ~60s; dialog gives Work File Zip + Total TDCX; clicking both syncs downloads to sandbox /home/user/downloads (a few seconds).
- Template boundaries: pan map by left_click_drag on the map; south edge may run along the street just below the polygon.
- Garage $/space is not on the export page; Template 1 value left unchanged (flag it).

## <subject-address>, Coppell (2026-10-18) - partial run
- Session <report-uuid> (2055, Q4/C3, lot 7,174). Polygon 4 corners (500,422)(905,422)(905,600)(500,600) at 1205x892 after Draw Market Area, no zoom: 246 SS / 506 CS. 1004MC: sales Declining? (19/11/12 -> Stable chosen via clicks; verify), concessions Yes+Increasing, REO No.
- Spark: County Dallas + parcel 18007000070120000 (APN digits, no dashes) worked; 6-row CSV (__3, reno asc then as-is) gave correct grid order. Cost: GLA 1711, garage 440, land $<amount> (2025 assessed), age 6. Q4.0=$<amount>; Q5.0=$<amount>; Q5.4=$<amount> (exported, targets ARV $475k); as-is probe Q4.2=$<amount> (purchase $382k).
- Grid after import: comp1 2 fireplaces, comps Q4+/C2-/blank heating on comp4, porch labels CvPch etc still need Pc/ cleanup. Stopped before Grid Cleanup edits.

## Subject Spark export (user correction 2026-10-21, <subject-address>)
- In /matrix-comp-search, ALSO export the SUBJECT listing (when it is in MLS, e.g. active/just-closed; type its MLS# in the shorthand box or check its row) as its own Spark CSV, named like the comps file with `__subject`. Upload it in Spark "Add Subject" alongside the comps CSV when starting /truetracts, instead of typing county/parcel by hand. Subject GLA/lot/rooms/garage then come from MLS.
- Parcel/county entry (Denton, R47879) worked as a fallback but gave a cost-form half-bath of 0 until corrected.
