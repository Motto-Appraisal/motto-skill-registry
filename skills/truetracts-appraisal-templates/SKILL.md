---
name: truetracts-appraisal-templates
description: Reads the TrueTracts export/preview page for a session and updates the user's three standard appraisal comment templates (Adjustments/Search Parameters/Sales Comparison/Market Analysis block, Neighborhood Boundaries, and Market Conditions) with the latest figures, without changing wording or length. Use when the user wants to update their appraisal templates from a TrueTracts export/preview page, or asks to "run the TrueTracts template update."
---

# TrueTracts Appraisal Template Updater

Goal: At the end of a TrueTracts session, harvest the data on the export/preview tab and use it to refresh the numeric details in the user's three standard appraisal comment templates, keeping sentence structure and overall length essentially unchanged. Output the updated text directly in chat (no file destination, no email/Slack/spreadsheet).

This workflow is run manually by the user (they will say something like "run the TrueTracts template update" or paste a new export URL). It is not on a schedule.

## Step 1: Get the export/preview page
1. The user will typically already have the TrueTracts export/preview tab open (last stage of a TrueTracts session), e.g. a URL like `https://truetracts.truefootage.tech/truetracts/<session-id>/export`. If a relevant tab is already open, use it directly.
2. If no tab is open, ask the user for the TrueTracts export URL for this session, then navigate to it.
3. Extract ALL harvestable data points from the page, including but not limited to:
   - GLA $/sqft adjustment, GAM indication, credible interval (e.g. 90% CI low/high), and the sqft threshold for applying the adjustment
   - Lot size $/sqft adjustment and threshold
   - Bathroom adjustments (full bath / half bath $ amounts)
   - Garage space adjustment ($/space) — note: this figure does not always appear in the extractable page text; if absent, leave the template value unchanged and flag it
   - Bedroom count treatment (whether an adjustment was applied or not)
   - Search/filter parameters: bedroom range, bathroom range, garage range, GLA range, lot size range, stories, year built range, sold price range used to remove outliers
   - Submarket / market area / competing submarket (green-coded) methodology notes and any named submarket/market area
   - Market analysis stats over the trailing ~12 months: average adjusted sale price (before/after, % change), months of housing supply (before/after), average days on market (before/after), sale-to-final-list ratio (before/after), sale-to-original-list ratio (before/after), distressed sales % (before/after), % of sales with concessions (before/after), average concession contribution (before/after)
   - Any age/quality/condition treatment notes
   - Anything else numeric or methodology-specific visible on the export page that maps to the template language below
   - If page text extraction truncates on long pages, search the full saved text for keywords like "average", "GAM", "credible", "per square foot", "Garage", "Months", "Days on Market", "Distressed", "Concession" rather than re-fetching repeatedly.

## Step 2: Read the neighborhood boundary streets off the heatmap (visual-only data)
The four boundary streets for Template 2 are NOT present anywhere in the page's extractable text — they only exist visually as a gold/black outlined polygon drawn on the map. You must read them off the map:

1. Scroll to the **Market Area Heatmap** (or Comps Heatmap — both show the same polygon) section on the export page.
2. The subject's Submarket/Neighborhood boundary is the gold-and-black outlined polygon surrounding the orange subject pin ("S" marker). This is distinct from the thin green Market Area polygon and the individual comp markers.
3. **Map interaction gotchas (learned from experience):**
   - The map's Leaflet zoom (+/-) buttons and mouse-wheel-over-map scrolling recenter/pan unpredictably, easily sending the subject pin and polygon out of view. To scroll the page itself, use a point outside the map (e.g. over the Export Settings panel) — never scroll with the cursor over the map unless you intend to zoom it.
   - Zoom the map itself only via the on-map "+" button, one click at a time, taking a screenshot after each click to confirm the polygon and subject pin are still in view before zooming further.
   - If the map view is lost/panned away and you can't relocate the polygon, reload the export page (accept the ~8-10s "Loading session... / Loading Adjustments..." recalculation delay) to reset the map to its default centered view, then retry zooming carefully.
4. Zoom in until street name labels are legible along all four edges of the polygon. You may need to check each edge (top/north, bottom/south, left/west, right/east) separately, since one zoom level rarely shows all four edges' labels clearly at once — take a screenshot (or a cropped region) centered on each edge as needed.
5. Identify the feature running along each of the four edges: West, North, East, South. Watch for streets that change N/S or E/W prefix along their length (e.g. "N Jupiter Rd" vs "S Jupiter Rd") — use the label that appears directly adjacent to the polygon edge itself, not labels further away outside the polygon's span.
6. **Not every edge borders a street.** Some polygons run along a natural feature (a lake, pond, or creek) instead of a road for one or more sides — the edge will visually hug a body of water with no street line directly on it. When this happens:
   - Zoom out and pan to find a name label for the water body itself (lakes are often unlabeled at the immediate zoom level but named at a wider regional zoom, e.g. "Lewisville Lake"/"Lake Lewisville"). A web search for "<nearby city/community> lake name" can confirm/disambiguate if the on-map label is abbreviated or missing.
   - Use that water body's name in place of a street name for that edge (see Step 4 phrasing).
   - Two adjacent edges bordering the same lake can be combined into one clause (e.g. "Lake Lewisville to the West and South") rather than repeating the name twice — see Step 4.
7. If an edge borders neither a legible street nor an identifiable named natural feature after a reasonable attempt (reload + careful zoom + regional zoom-out + web search), leave that specific direction's value unchanged from the base template and flag it to the user — do not guess. Only fall back to "leave Template 2 entirely as-is" if the polygon itself cannot be located at all.

## Step 3: Update Template 1 — Adjustments / Search Parameters / Sales Comparison / Market Analysis
Base template (reuse this exact structure and wording, only swapping numbers/figures that changed):

"Adjustments
All comparables are located within the subject's data-defined submarket and broader market area, as identified by the TrueTracts ML heatmap, with no market division or locational barrier noted within the competitive polygons; green-coded competing areas were considered similar, and no separate location adjustment was indicated. The sales were selected to bracket the subject's key features within the appraiser-defined filters for similar properties, including 3-4 bedrooms, 2-3.5 baths, up to 3 garage spaces, 1,620-2,700 square feet of GLA, 5,000-12,000 square foot lots, 1-2 stories, and year built 1976-2000. Adjustments for GLA were developed using GAM and peer-supported rates, with the selected adjustment of $79 per square foot supported by a GAM indication of $79 with a 90% credible interval from $76 to $82, and applied only for differences greater than 100 square feet. No additional adjustment was considered necessary for bedroom count within the filtered range because the applied filters and market modeling indicate a consistent buyer preference across 3-4 bedrooms in this competitive segment. Other feature adjustments follow directly from data-supported rates in the grid, including lot size at $3 per square foot for differences greater than 1,000 square feet, bathrooms at $11,000 per full bath and $5,500 per half bath, garage spaces at $9,000 per space, and listing status adjustments for actives and pendings based on supported sale-to-list ratios to estimate probable sale price. Adjustments to the comparables are supported by a combination of generalized additive modeling, peer adjustments, depreciated cost, and sensitivity analysis, with the appraiser reconciling to market-aligned figures within the indicated ranges. Quality and condition differences were analyzed using UAD ratings with internal plus/minus refinements, with quality and condition conclusions interpreted through GAM, depreciated cost, and corroborating methods to reflect market reaction to observed differences.

Exceeds Guidelines
It is noted that there is a difference in age among some comparables; however, the applied search parameters already limited the competitive data set to homes built from 1976-2000, and the market analysis indicates buyers in this segment primarily differentiate on condition and quality rather than chronological age. Accordingly, no direct age adjustment was applied, and any age-related influence is reflected through condition, quality, and contributory depreciation rather than as a separate line-item adjustment.

Search Parameters
A search for comparable properties was completed using TrueTracts to define the subject's submarket, market area, and competing submarkets, then applying feature filters for competitive homes within the market area, including 3-4 bedrooms, 2-3.5 baths, up to 3 garage spaces, 1,620-2,700 square feet of GLA, 5,000-12,000 square foot lots, 1-2 stories, year built 1976-2000, and a sold price range of $310,000-$512,000 used only to remove extreme outliers. The tool trained a GAM model on the past 5 years of competing sales within the subject submarket and then identified green-coded competing submarkets within the broader market area, ensuring selected comparables are both locationally and physically competitive. Every effort was made to include the most appropriate comparables within this data-defined neighborhood and submarket structure, and the cited sales were deemed the most reliable indicators of value based on similarity and overall competitive appeal.

Sales Comparison Analysis
Texas is a non-disclosure state; therefore, MLS and public record data, as accessed through TrueTracts, serve as the primary source of closed sale and listing information. Market-area modeling identified competitive properties within the subject's submarket and green competing submarkets, and the sales comparison grid incorporates closed sales and, where relevant, active, pending, and contingent listings with supported sale-to-list adjustments to estimate probable closing prices. Weighted reconciliation is based on similarity ratings, with higher weights assigned to the most similar properties and lower or zero weights assigned to less comparable sales, while other sales and listings were considered qualitatively and not directly weighted in the statistical reconciliation.

Market Analysis
Market analysis for similar homes within the subject's market area over at least the past 12 months indicates overall property values are relatively stable, with the average adjusted sale price decreasing from about $415,200 to $412,000, an implied change of -0.8%. Months of housing supply decreased from 3.3 to 2.9 months and remain in shortage, while average days on market decreased from 40 to 27 days, reflecting marketing times under three months. The average sale-to-final list price ratio decreased from 97.5% to 97.0%, while the average sale-to-original list price ratio increased from 95.8% to 96.3%, indicating generally stable pricing relative to list levels. Distressed sales increased slightly from 0.8% to 1.0% and were reconciled as relatively stable and not a significant market factor. Seller concessions remain common, with the share of sales with concessions increasing from 57.7% to 62.3% and the average concession contribution increasing from 1.7% to 1.9%, reconciled as relatively stable and market-typical."

Replace every number, range, $ amount, percentage, and directional word (increase/decrease/stable/shortage/etc.) with the corresponding value found on the current export page. If a data point isn't present on the export page, leave the original template value in place and flag it in your summary to the user rather than guessing. Do not change sentence structure, add new sentences, or lengthen the template — only substitute figures/values in place. If a ratio/percentage is unchanged between before/after, rephrase that clause minimally (e.g. "remained unchanged at X%" instead of "decreased from X% to X%") rather than forcing a false direction word.

## Step 4: Update Template 2 — Neighborhood Boundaries
Base template: "S Jupiter Rd to the West, E Bethany Rd to the North, S Allen Heights Dr to the East, Chaparral Rd to the South."

Using the four boundary features read off the gold/black polygon in Step 2, update the four directional entries accordingly (West/North/East/South), keeping the exact same phrasing pattern ("[Feature] to the [Direction]"):
- For edges bordering a street, use "[Street Name] to the [Direction]" as before.
- For edges bordering a named natural feature (lake/pond/creek) instead of a street, substitute the feature's name in the same slot, e.g. "Lake Lewisville to the West".
- If two adjacent directions border the same water body, combine them into a single clause instead of repeating the name: "Lake Lewisville to the West and South" replacing what would otherwise be two separate clauses — then join with the remaining street clauses, e.g. "Fishtrap Rd to the North, Union Park Blvd to the East, Lake Lewisville to the West and South."
- If a specific direction has no legible street AND no identifiable named feature after a reasonable attempt, leave just that direction's original template value in place and flag it — don't block the other three directions from updating.
- Only skip the entire template (leave fully as-is) if the polygon itself can't be located on the map at all.

## Step 5: Update Template 3 — Market Conditions
Base template: "Financing on sales is similar to conventional financing for homes in the metroplex and where appropriate is adjusted to cash equivalency. Analysis of MLS data indicates property values are declining with demand exceeding supply. The marketing time for properties is relatively stable and is estimated to be under 3 months."

Use the export page's market analysis data to determine:
- Whether values are increasing/declining/stable (based on the average adjusted sale price % change and its reconciled trend label)
- Whether demand exceeds supply, supply exceeds demand, or they're balanced (based on months of housing supply / absorption trend and its reconciled label, e.g. "In Shortage")
- Whether marketing time (average days on market) is under 3 months, 3-6 months, or over 6 months, and whether it's stable/increasing/decreasing

Update only the words describing direction/magnitude (e.g., "declining" vs "increasing" vs "stable", "demand exceeding supply" vs "supply exceeding demand" vs "supply and demand in balance", the DOM threshold), keeping the rest of the sentence structure unchanged.

## Step 6: Deliver output
Present all three updated templates back to the user in the chat, clearly labeled ("Adjustments/Search Parameters/Market Analysis template", "Neighborhood Boundaries template", "Market Conditions template"), ready to copy into Total Alamode. Call out any figure you could not find on the export page and therefore left unchanged (e.g. garage adjustment $/space is commonly missing from the extractable text).

## Notes
- The user pastes the final text into Total Alamode themselves — this workflow does not write to Total Alamode.
- Always ground every figure in what's actually visible on the TrueTracts export page for that session; never invent or carry over numbers from a previous run.
- The gold/black polygon boundary features must be read visually (screenshots/zoom) every session — they are not retrievable via plain text extraction and are specific to that session's subject property location. Not all four edges are guaranteed to be streets; some border a lake/pond/creek instead, in which case use the water body's name for that edge rather than leaving it unchanged.
