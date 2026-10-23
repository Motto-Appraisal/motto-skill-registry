
# Memory (titan-appraisal-prep)
- 2026-10-06 5105 Avery Ln run: flow worked unchanged. Viewport 1280x720 here; Manage arrows at (785,321 add / 352 remove / 383 up / 414 down), OK (1108,655), Cancel (1167,655). Merge dialog: search "ZZ TEMPLATE" in Source File, Merge (1106,667).
- File chooser coords vary; double-click dropzone then file_upload with the filechooser_N ref from the result.
- In Titan editor, Ctrl+A sometimes only selects a word; End then shift+Home then Delete/type clears a field reliably.
- Opening Drive "New" with a row selected opens that existing report; use File > New Report instead.
- No subject MLS listing data in workfile: left "offered for sale" boxes/data line blank and flagged rather than keep template "no known listings".
- Scope json (metadata/artifact_renovation_scope) has as_is_condition (C4 here); payload said C3. Foundation estimate PDF in subject/ can imply structural Yes.
- Order Form edits to Bill To overwrite Invoice TO lines; re-type invoice street/city lines after.
- 2026-10-07 1110 Emily Ln v4 resumed (open tab had merge+Manage+Order Form done, images/Page 1 not): finished steps 7-8. No stage log existed in OneDrive. Generated Flood/Aerial images were never saved before the Manage removal, so Aerial/Flood slots stayed empty: ALWAYS save maps.json images right after generating (step 3) before anything else.
- Condition: scope json as_is_condition C4 (ARV C2) -> used Overall C4. Clearing text fields: click, End, BackSpace xN works; deficiency Yes box shows yellow until you click another field, then X.
- Out-of-sync popup hit again on Page 1 edit; edits persisted after navigating to same Forms URL.

## 809 Frances Dr run (2026-10-07) learnings
- Workfile can be NON-STANDARD: `/Appraisal-Mirror/Motto-Workfiles/renterswarehouse-<slug>-full/` (made by Factory) instead of by_address. realist_tax.pdf may be a Matrix dashboard screenshot and sketch.png a watermarked TaxNet screenshot: check images before use. Real tax data was `property_detail_report_*.pdf` (Dallas CAD). No scope PDF there: get it from the SharePoint link in the order email via the browser viewer (bash proxy download fails on size).
- Order Form Neighborhood/Tax Yr/Taxes won't accept typed edits (linked to Page 1): edit them on Page 1.
- SmartStart OK may land on Drive without opening the report: search Drive for the description and open.
- Deficiency Yes: click once, click another field, verify the X.
- Rerun after new artifacts (809 Frances v2, 10/08): artifacts land later in `by_address/<slug>/subject/` (realist_tax.pdf, improvement_sketch_*.png) + `artifact_manifest.json` (status verified/failed); recheck by_address after a workfile-only run. A rerun = new report (v2) since only ONE merge is allowed per report. Order Form Tax Yr/Taxes link to Page 1 and fill from the Order Form once typed there this time (taxes 6,171.79 took). "Report is out of sync" popup hit after the deficiency note: OK, reload the Forms URL, re-check microwave/note.

- Workfile artifacts can be replaced repeatedly: re-list, compare size/md5, and swap images in place via Image Tools (no new report). If an upload sticks on "Photo uploading..." the image is NOT saved: reload loses it. Upload ONE image, wait ~15 s, Ctrl+S, confirm, then the next. After a reload, Contents clicks may not scroll the pane; scroll with the mouse wheel instead.

## 4230 Phoenix Dr (2026-10-10)
- Titan Drive already held "4230 Phoenix Dr v1" from a 10/09 run (merge, Manage, maps, order form, images, Page 1 all done). Search Drive for the street FIRST and resume instead of starting a new report. Only fixed Condition C3->C4 (scope json as_is C4) and scope date 10/07.
- Workfile here: /Appraisal-Mirror/Motto-Workfiles/renosy-<slug>-full/ with subject/sharepoint_scout/ holding scope, CompanyCam, foundation PDFs (OneDrive connector can download them; curl the s3url).

## 2521 High Pointe Blvd (2026-10-11)
- Flow worked unchanged; viewport flips 1280x720/1205x892 mid-run (batch actions abort, re-screenshot). Titan Drive login needed notify_user (no saved login); then navigate to /Desktop.
- SmartStart favorite select: click it, type "Exterior", Enter. Merge-source search "ZZ TEMPLATE" = one row. 1280x720 coords: Manage arrows right (785,321) left (785,352) up (785,383); OK (1108,655), Cancel (1167,655).
- Order Form layout shifts after Legal Description edit (rows move up ~20px): screenshot between batches; Map Ref got a stray value, cleared. Neighborhood/Tax/Taxes on Order Form are linked: edit on Page 1.
- Condition popup closes by clicking another Page 1 field (e.g. deficiency describe line), not the margin. Offered-for-sale popup: left No ticked with blank source, flagged.
- Workfile had scope PDF + foundation proposal PDF in subject/ (page 2 of listing); get listing via next_page_token.

## 3304 Sedona Ln (2026-10-13)
- Titan Drive already held "3304 Sedona Ln v1" (10/09 run; reportId 800ac3a9-...). Audited on 10/13: maps, FEMA, order form, invoice, Page 1, cover, Property Data, sketch, Subject Photos, form order all done; only saved and left open. Search Drive by street first.
- Workfile is by_address/<slug>/ with subject/{realist_tax.pdf, property_detail_report, improvement_sketch_*.png, sharepoint_scout/<addr> initial scope.pdf}; comps/ already has Factory spark_export.csv. Background curl of several s3urls lost files: curl sequentially.
- A `task` subagent call aborted when issued together with a browser action in the same batch; call task alone.

## 312 Timber Ridge Ln (2026-10-13)
- Flow worked unchanged (v1, Exterior-Only starter). Titan login needed notify_user. Viewport 1280x720: Manage arrows right (785,321) left (785,352) up (785,383), OK (1108,655), Cancel (1167,655) (no confirm). Merge search "ZZ TEMPLATE", Merge (1106,667). Order Form fields (1280 layout): Order Date (540,246), Due (808,246), JobType (540,283), PropType (540,301), FormType (540,337), SalePrice (808,283), file nos (1130,184/266), Invoice # (1100,329), date (1100,348); Bill Due Date is on Order Form [Page 2] (1110,362). Out-of-sync popup hit after switching to Invoice; reload same URL, edits persisted.
- Workfile: by_address/<slug>/subject/{realist_tax.pdf (3 pp), improvement_sketch_DALLAS-unknown.png, sharepoint_scout/scope+foundation PDFs}; scope cover = pdfimages jpg cover-002.jpg (the ppm files are small thumbs). Subject Photos "Site" size pulls from Page 1 Area.
- No subject listing data in workfile; left Offered=No + template "no known listings" text and flagged.

## 1713 Baylor Dr (2026-10-13)
- Flow worked unchanged (v1, Exterior-Only starter, reportId 33475ac7-...). Titan was already logged in (no notify needed). 1280x720: toolbar Add Map (608,48) arrow (648,48), Merge (245,48), Manage (60,316); Manage arrows right (785,321) left (785,352) up (785,383), OK (1108,655), Cancel (1167,655). Map Type dd (145,48), Page Title dd (470,48), Add Map (1234,84) in map editor; flood preview Add Map (1134,688).
- Workfile by_address had realist pdf (3 pp, MLS photo = real front), sketch, LOE txt, but empty sharepoint_scout/loe_emails (no scope). As-is only order: Job Type `AS - IS`; left template condition C2 text, zoning Z236, rooms 6, effective age/window untouched and flagged.
- Image slot order that worked: Cover, Aerial, Flood, Property Data 1/2/Addendum (Image Tools folder icon, y shifts per form), Building Sketch, Subject Photos; Ctrl+S after each. Saving popup blocks clicks ~15 s after Subject Photos upload.
- Invoice TO lines blank after Order Form Bill To edit: street (620,453), city (700,475) End+3 BackSpace.

## 325 Kirby Dr (2026-10-13)
- Flow worked unchanged (v1, reportId d0ebf736-..., Exterior-Only starter). Titan login needed notify_user. Workfile by_address/<slug>/ had realist_tax.pdf (3pp), sketch, scope in subject/sharepoint_scout (14MB; curl s3url fine), metadata/renovation_scope.json (as_is C4). Realist had MLS listing (Active Option Contract) -> filled Offered=Yes, DOM, data line.
- 1280x720 layout: left panel is short, Order Form fields at: OrderDate (540,246), Due (808,246), JobType (540,283), PropType (540,301), FormType (540,337), SalePrice (808,283), file nos (1130,184/266), Invoice#(1100,329)/date(1100,348), Ordered/Bill/Ship (1100,382)/(1085,398)/(1085,486), County (540,413), APN (800,413), Legal (650,432), Year (440,486), Beds (654,486), Baths (756,486), GLA (860,486). Invoice: due (1100,341), TO street (620,453), city (700,475).
- Order Form Neighborhood/Tax Yr are linked: typing Tax Yr overwrote Neighborhood with "2025". Fix both on Page 1 (Neighborhood (600,298), Taxes (1170,280) End+BackSpace).
- Page 1 Improvements: click on right edge (1230,440) opens Condition popup by accident; popup closes by clicking deficiency line. Fence/patio/microwave/Other appliance "Tile Back Splash" left as template and flagged.

## 4416 Cleveland Dr (2026-10-14)
- Flow worked unchanged (v1, reportId 5336611d-..., Exterior-Only starter). Titan login needed notify_user (no saved login). Viewport 1205x892 layout: Add Map main (608,48)/arrow (648,48); map editor Map Type (145,48), Page Title (470,48), Add Map (1159,84); flood preview Add Map (1058,860); Merge search (500,397), Merge (1035,822); Manage arrows right (714,407) left (714,437) up (714,468), OK (1038,827), Manage button (60,316).
- Workfile by_address/<slug>/ had realist pdf (3pp), sketch, scope in subject/sharepoint_scout (cover-002.jpg 1920x1080 is real front); scope json as_is C4 (rehab_total 72,705 vs email 73,000). Realist has no zoning: left template Z236 and flagged. Lot dims from Realist p3 map (69x111).
- Order Form 1205 layout: OrderDate (540,246) Due (808,246) JobType (540,283) PropType (540,301) FormType (540,337) Sale (808,283) file nos (1120,185/267) Invoice# (1090,329) date (1090,348) Ordered/Bill/Ship (1090,380/399/487) County (540,413) APN (800,413) Year (440,487) Beds (654,487) Baths (756,487) GLA (860,487) Owner (600,664); Legal (650,433). Invoice: due (1100,341), TO street (620,453), city (700,475) End+4 BackSpace.
- Image slots: Image Tools folder icon y shifts (PD1/PD2 at (978,367), Addendum (968,491)). Deficiency Yes: click another field, click Yes (1056,651), click elsewhere.

## 3300 Stone Bridge Dr (2026-10-16)
- Flow worked unchanged (v1, reportId 053e7f5e-..., Exterior-Only starter). Titan login needed notify_user. Viewport flipped 1205x892 -> 1280x720 mid-run. Page 1 checkboxes: click the BOX (e.g. Purchase box x~453), not the label (537 did nothing).
- Workfile by_address/<slug>/subject had realist_tax_pdf (3pp), sketch png, scope + CompanyCam + foundation PDFs in subject root (not sharepoint_scout). MLS photo from Realist (pdfimages) was a much clearer front than scope cover (truck blocking): used it for Cover + Subject Front.
- Foundation proposal (12 piers $5,000) -> Physical deficiencies Yes with note. Subject Photos side panel (Site 8368 sf etc.) pulls from Page 1 Area; refresh by reopening.

## 4404 Cleveland Dr (2026-10-16)
- Flow worked unchanged (v1, reportId 4f12c669-5fc5-4d26-91bb-dc76c7653915, Exterior-Only starter). Titan login needed notify_user. Viewport 1280x720: Add Map main (608,48)/arrow (648,48); flood preview Add Map (1134,688); map editor Map Type (145,48), Page Title (470,48), Add Map (1234,84); Merge search (507,397), Merge (1106,667); Manage arrows right (785,321) left (785,352) up (785,383), OK (1108,655).
- Workfile by_address/<slug>/subject had realist_tax.pdf (3pp), improvement_sketch_COLLIN-unknown.png (real TaxNet sketch), scope in sharepoint_scout; cover-002.jpg = real front. OneDrive search "4404 cleveland" found the folder when it was not in the top-15 recent list.
- Order Form (1280 layout): Legal desc clear with ctrl+a Delete worked; occupancy boxes (811,426 owner)/(811,462 vacant) after scrolling 3; Invoice due (1100,341), TO street (620,453), city (700,475) End+3 BackSpace.
- Page 1 after Site jump: Dimensions (560,413), Area (790,413); popup closes by clicking Borrower field (540,245). Condition dropdown arrow (795,347), C4 (646,453).

## 1331 San Antone Ln (2026-10-16)
- Flow worked unchanged (v1, reportId 5be6399d-df41-4bbc-bc26-cf9ce126e7ed, Exterior-Only starter). Titan was already logged in. As-is-only Dennis Fernandez order (Job Type `AS - IS`, Due = Report Due Date, no scope). 1280x720 layout; Manage arrows left (785,352) up (785,383) right (785,321), OK (1108,655), Cancel (1167,655); Building Sketch shortcut (select [Scanned Page] Addendum first) worked.
- Workfile by_address/<slug>/subject had realist pdf (3pp; MLS photo via pdfimages = real front), sketch png, loe txt; no scope. Realist showed Active listing -> Offered=Yes popup (DOM field (848,304), data line: End, shift+Home, type; 70 BackSpace was not enough).
- Order Form 1280 layout: Order Date (540,246) Due (808,246) JobType (540,283) PropType (540,301) FormType (540,337) Sale (808,283); Invoice due (1090,518 after tab opens), TO street (620,632), city (700,652 End+3 BackSpace). Invoice base fee line description was blank; typed `AS - IS`. Out-of-sync popup hit on Invoice save; edits persisted after reload.
- Page 1 after Order Form: Neighborhood/Taxes edited on Page 1 (Neighborhood (650,298), Taxes (1170,280)); Contract Price came through from Order Form Sale Price.

## 1600 Hearthstone Dr (2026-10-17)
- Flow worked unchanged (v1, reportId db2f3e94-d7b7-4666-978d-e0e691ecc2f4, Exterior-Only starter). Titan login needed notify_user. Viewport 1205x892 coords as in 4416 Cleveland run (Add Map (608,48)/(648,48), map Add Map (1159,84), flood Add Map (1058,860), Merge (1035,822), Manage arrows (714,407/437/468), OK (1038,827)).
- Workfile by_address/<slug>/subject: realist pdf (3pp, Pending listing), sketch png, scope + loe in subject root (sharepoint_scout/loe_emails folders empty). OneDrive by_address lastModified list put it first.
- Condition popup and deficiency line DROP characters when a long string is typed in one go (lost "t, HVAC, electrical"; "cracked/settled con"). Type in short chunks (<=40 chars) and re-screenshot.
- Order Form Tax Yr/Taxes/Neighborhood still stale after Order Form edits: fixed on Page 1 (Neighborhood (650,298), Tax Yr (920,280), Taxes (1150,280), End+shift+Home). Contract price flowed from Order Form Sale Price. Drive search 'Hearthstone' before starting: a SmartStart run interrupted mid-click still created the report.
- Rush Fee applied: option ends 10/19, run 10/17 (2 days) though email dated 10/16 (3 days): flagged.

## 450 Woodhurst Dr (2026-10-18)
- Flow worked unchanged (v1, reportId c9873321-bbcc-48a3-9eaf-b3eeb0874071, Exterior-Only starter). Titan was already logged in. 1280x720 coords: Add Map (608,48)/arrow (648,48), flood preview Add Map (1134,688), map editor Map Type (145,48) Yes confirm (792,224), Page Title (470,48), Add Map (1234,84); Merge search (507,397), Merge (1106,667); Manage arrows right (785,321) left (785,352) up (785,383), OK (1108,655). Save icon (93,48).
- Workfile by_address had realist_tax (3pp, Active MLS listing, real MLS front photo), sketch, NO scope in OneDrive: scope PDF via SharePoint link in-page fetch (15 MB, 6 chunks of 2.5 MB worked). Foundation PDF was not present for this address.
- Manage: clicking a row then arrow in one batch can miss; select, screenshot, then click arrow once.
- Order Form (1280 layout, unscrolled): OrderDate (540,246) Due (808,246) JobType (540,283) PropType (540,301) FormType (540,337) Sale (808,283); file nos (1130,184/266); Invoice#/date (1090,329/348); Ordered/Bill/Ship (1085,380/398/486); County (540,413) APN (800,413) Legal (650,432) Year (440,486) Beds (654,486) Baths (756,486) GLA (860,486) Owner (590,664). Invoice tab: due (1100,518), TO street (620,632), city (700,652); scroll 8 ticks for fee lines (base desc (720,331), Rush (720,351), amount (1150,351)).
- Page 1: Taxes (1160,280), Neighborhood (650,298), Offered Yes (1090,389) -> popup DOM (848,304), data line (800,342); close popup by clicking Borrower (540,245). Condition via click (1100,306)+Tab, dropdown (795,163), C4 (622,269).

## 3208 Weeping Willow Ct (2026-10-18)
- Flow worked unchanged (v1, reportId 79654ccb-16ae-4b51-8c06-33739efbc17c, Exterior-Only starter). Titan login needed notify_user. Viewport 1280x720 (flipped once). Same coords as 4404 Cleveland run; Manage arrows left (785,352) up (785,383) right (785,321), OK (1108,655), Cancel (1167,655).
- First aerial Add Map did NOT save (stuck on map editor ~4 min): reload Forms URL, redo aerial (map editor Add Map (1234,84)); second try saved in ~90 s.
- Workfile: scope PDF was NOT in OneDrive (194 pages, 15 MB); fetched from SharePoint link via in-page fetch in 7 slices of 2.5 MB. Cover-002.jpg real front. Realist 3pp, sketch OK, rs.json as_is C4.
- Order Form after merge lets Tax/Neighborhood fill from Page 1 edits directly; Page 1 Subject layout (scroll 6 from top) shows all values. Template cover page value 334,000 is stale (TrueTracts).

## 2015 Sandi Ln (2026-10-19)
- Flow worked unchanged (v1, reportId f5751c0c-9f3e-4f82-8d6a-a4d4d79502a9, Exterior-Only starter). Titan login needed notify_user. Viewport 1259x892: SmartStart fields (628,198) street,(460,269) city,(720,269) st,(889,269) zip,(628,375) desc, OK (875,718); flood preview Add Map (1112,860); map editor Add Map (1213,84); Merge row (620,542), Merge (1086,822); Manage arrows right (766,407) left (766,437) up (766,468), OK (1089,827), Cancel (1147,827).
- Workfile by_address had realist pdf (4pp: p1 PD1, p2 PD2, p4 map -> Addendum), sketch, artifact_renovation_scope json (as_is C4); scope+foundation PDFs only via SharePoint link in email (in-page fetch, 7 chunks; chunk files are raw base64 text). Cover = scope cover-002.jpg real front.
- Order Form (1259 layout) coordinates same as 1280 notes; occupancy boxes (811,727)/(811,763) after unscrolled. Image slot nav in Contents list scrolled: PD1 y842, PD2 y868; Image Tools folder icon (978,367).

## 1922 Camden Way (2026-10-20)
- Flow worked unchanged (v1, reportId 54a14bf8-e042-4a92-a0de-f7a242cd3b1c, Exterior-Only starter). Titan login needed notify_user. Viewport 1259x892 coords as in 2015 Sandi run. Manage: Flood row2 left (766,437) twice removes both maps; Invoice/Cover up (766,468); select [Scanned Page] Addendum (row y577) before adding Building Sketch.
- Workfile by_address had realist pdf (3pp, Active sale listing + a rental listing in same MLS table), sketch png, no scope (as-is, Vincent Kolles). OneDrive LIST_FOLDER_CHILDREN needs use_me_drive=true with folder_path. Front photo = Realist MLS image (pdfimages).
- Order Form legal desc: ctrl+a Delete + type worked; Invoice TO street (620,709), city (700,731), due (1090,596), fee desc (720,710) after scrolling 5.
- Page 1 after jump: Taxes (1160,280), Neighborhood (650,298), Offered Yes (1090,389) popup DOM (848,303), data (800,341); close popup via Borrower (540,245).
