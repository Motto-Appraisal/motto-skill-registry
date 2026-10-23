
# MODE A: AS-IS ONLY ORDERS (refi-style)
Use when the LOE asks for an as-is value only: no ARV, no "subject-to", no renovation scope. This is a REFI-style appraisal: find the most RELEVANT comparables that represent the subject as it actually is today. This file is independent of `mode_as_is_subject_to.md`: edit one without touching the other. Shared setup, tooling, review, export and filing steps live in SKILL.md. (user correction 2026-10-16, 1713 Baylor Dr)

## A0. Hard rules
- PRICE DOES NOT MATTER. No price band. No purchase-price or purchase-$/sf target. No sanity check against the contract. Price and $/sf are shown in tables for information only and must never reject, rank, sort-gate or skip a comp. Do not sort by $/sf to find candidates.
- Relevance = (1) condition/quality match to the subject's CURRENT state, (2) style/story count/GLA/lot/age/garage, (3) distance, (4) recency (closed <=6 months preferred, up to ~9 if needed).
- There is no "renovated" side vs "as-is" side. One comp set, all chosen to represent the subject's current condition.

## A1. Establish the subject's CURRENT condition first
1. Include the subject's own MLS# in the first shortlist export and read its remarks; look at ALL its photos (sheet2(recordId,30)). Check Realist condition and any scope PDF/photos.
2. Classify the subject: already renovated/listed (flip-grade: new kitchen/baths/flooring) vs dated C4 vs light refresh vs distressed. Write the subject's quality tier and key materials down (cabinets, counters, flooring, baths).
3. The comps must be the same tier. Renovated subject => renovated comps equal or above in scope (mid refreshes are alternates at best). Dated subject => dated C4 comps (reject only C5/C6).

## A2. Candidates
1. Pull ALL pool rows and fetch every ToFull page for remarks (MEMORY.md bulk method). Account for every comp: candidate / reject + one-line reason. Allowed reject reasons: condition mismatch vs subject, story/GLA/lot mismatch, garage conversion, non-arms-length/auction, recency, distance, C5/C6. NEVER price or $/sf.
2. Photo-verify with ALL photos (sheet2(recordId,24..30)), not 12: check every bath, bedroom flooring, kitchen. 12 photos hid an original master bath (1812 Baylor) and carpeted bedrooms (3402 Blueridge). Verify every closed comp within ~9 months and every active listing that is within about 1 mi of the subject or has update language, whatever its price. Label anything not fully photo-viewed "partial look".
3. FLIP DETECTION: find the same address twice in the pool (prior low sale then high resale, e.g. 1803 Baylor $252k then $455k; 1705 Morningstar $300k then $443.9k). For a renovated subject these are the best evidence: surface and verify first.
4. Tier by materials: D / C4 dated / C3 light refresh / mid refresh / full reno / upscale-custom. Record C-rating.
5. If the rules or criteria change mid-run, RE-REVIEW every comp previously rejected, including ones already photo-viewed (1503 Richland was missed this way).

## A3. Pick
- Best closed comps (typically 3-4) plus 2 active LISTINGS (keep Active/Contingent/KO/Option checked with Closed 0-365). Leave a 4th closed or alternates checked if useful; the user trims.
- Bracket the subject's quality: at least one slightly above and one slightly below/equal where the pool allows, none far below.
- Prefer one-story if the subject is one-story; skip two-story and converted garages.

## A4. Report
Subject current condition (source), pool size and filters, each pick with distance, GLA, date, condition note and why it beat near-misses (condition match, size, closeness, recency); rejected near-misses with allowed-reason; alternates; flips found; uncertainties. Price/$/sf shown for information only. Then follow USER REVIEW in SKILL.md.

## A4b. Subject Spark export (user request 2026-10-21, 1922 Camden Way) - EVERY MODE A RUN
When the subject has an MLS listing (active, pending, or recently closed/expired; MLS# known), export the SUBJECT as its own Spark CSV in addition to the comps:
1. In the final export step, after exporting the user's checked comps, uncheck all (check-list dropdown > Clear Selected), type the subject MLS# in the shorthand box (or use a fresh check on its row if it is in the pool), check it, Actions > Export > Spark, verify the dialog says "Export 1 Listings". NOTE: the shorthand search replaces the pool, so do this ONLY AFTER the user approves the comps and the comps export is done.
2. File it in the OneDrive comps folder as `comps_matrix_spark_export_csv__<slug>__subject.csv` (next unused name, never overwrite).
3. Tell /truetracts to upload it in Spark under Add Subject (together with the comps CSV) instead of typing county/parcel.
4. If the subject has no MLS listing, skip and use the county + parcel ID fallback in /truetracts.

## A5. History
- 1713 Baylor Dr (2026-10-16): subject already renovated and listed (full reno, navy cabinets/quartz/LVP/new baths). First pass used dual logic (price band) and missed 1803 Baylor, 1503 Richland, 1203 Edgewood. Rerun under Mode A (price ignored; photo-screened 106 pool comps incl. low-priced ones): closed 1803 Baylor, 1705 Morningstar (flip pair), 3317 Janwood, 2112 Cornell, 1203 Edgewood; active 1503 Richland, 1607 Centenary. Alternates: 3429 and 3534 Post Oak, 4009 Sweetbriar, 1705 Bobbie, 4709 Princeton, 1311 Edgewood, 1715 Baltimore (carpet BRs), 3029 Burning Tree, 909 Maydelle (active flip).
- Low-priced pool rows can be full renovations (4009 Sweetbriar $308k, 1705 Bobbie $320k): in Mode A photo-screen them too.
