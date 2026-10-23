---
name: appraisal-review-check
description: Acts as an independent appraisal reviewer (like a lender QC/underwriting reviewer). Use whenever the user attaches or references appraisal PDFs for review. Expects 2 PDFs per property (the completed appraisal report + an Initial Scope/renovation scoping PDF). Cross-references bed/bath counts in the scope doc's room labels (Bedroom 1/2/3, Bathroom 1/2, etc.) against the appraisal's stated counts as the primary check, then also scans for AS-IS vs Subject-To value inconsistencies (including a missing value when comps are split into two valuation groups), GLA/room-count math errors, adjustment $ mismatches vs narrative, Cost Approach site value mismatches, and certification/boilerplate contradictions. Outputs a flagged-issues list only.
---

# Appraisal Revision Check (Reviewer Simulation)

## When this runs
Whenever the user attaches or references appraisal PDFs and wants them reviewed. Treat any newly attached appraisal PDF(s) as a trigger to run this review.

## Expected inputs — 2 PDFs per property
Each run should have **two PDFs for the same property**:
1. The completed appraisal report (a la mode "TOTAL" software Residential Appraisal Report / Exterior-Only Inspection Report format, Texas non-disclosure market, TrueTracts-sourced comps).
2. An "Initial Scope" / "Guided Capture Scoping" renovation scope document (e.g. filename like "<address> Initial Scope.pdf") — a room-by-room renovation line-item estimate (likely from a scoping tool used by the property owner/investor, e.g. Renters Warehouse) that lists named room sections such as "Bedroom 1", "Bedroom 2", "Bedroom 3", "Bathroom 1", "Bathroom 2", "Kitchen", "Living Room 1", "Living Room 2", "Garage", "Hallway", "Entry", "Exterior front/side/back", etc.

If only one PDF is attached, still run the review on it, but explicitly note in the reply that the Initial Scope PDF was not provided so the bed/bath cross-reference step (below) could not be performed — ask the user to attach it for full coverage next time rather than skipping the note silently.

## Bed/Bath Cross-Reference (primary check against the Scope doc)
This is the main purpose of requiring the second PDF:
1. Extract text from the Initial Scope PDF and find every distinct numbered room label of the form "Bedroom N" and "Bathroom N" (grep-style: room labels appear as a column/tag next to each line item, e.g. `grep -oE "(Bedroom|Bathroom) ?[0-9]+" file.txt | sort -u`). Count the highest N for each to get the scope document's implied bedroom count and bathroom count (half-baths may appear as a distinct "Bathroom N" without further label — treat each numbered Bathroom as a full bath unless line items inside it clearly describe a half-bath/powder room, e.g. no shower/tub line items).
2. Compare this count against the appraisal report's stated bedroom/bathroom counts (the "Finished area above grade contains: X Rooms, Y Bedrooms, Z Bath(s)" line, and the Room Count row in the sales comparison grid's Subject column).
3. Flag any mismatch — e.g. scope doc shows "Bedroom 1/2/3" (3 bedrooms) but appraisal states 2 bedrooms, or scope doc has no "Bathroom 2" but appraisal states 2.0 baths. This is a primary, high-priority flag category — call it out first in the output, before the other checks below.
4. If the two documents agree, state that bed/bath counts were cross-checked against the Initial Scope document and are consistent — don't skip mentioning that this check was performed.

## Role
Act as an independent appraisal reviewer (like a lender QC/underwriting reviewer) scanning the report for internal inconsistencies and errors before it goes out — NOT re-deriving value, just catching things a human reviewer would flag.

## Steps

1. Extract text from the PDF(s) for review:
   ```bash
   pdftotext -layout "<file>.pdf" "<file>.txt"
   ```
   If pdftotext yields little/garbled text (scanned image PDF), fall back to converting pages to images and read them visually, focusing on the subject data section, sales comparison grid, and reconciliation/addendum pages.

2. Pull out these fields/sections for cross-checking:
   - Subject property: address, bedrooms, bathrooms (full.half format, e.g. "3.1" = 3 full, 1 half), GLA, room count total, site/lot size, year built.
   - Sales Comparison Grid ("Room Count" row): Bdrms/Baths for Subject vs. each Comp, and any bed/bath adjustment dollar amounts shown when counts differ.
   - Which comps are labeled "Subject To" vs "As Is" (per the "Summary of Sales Comparison Approach" line, e.g. "Comparables 1 thru 3 are based on 'Subject To' and Comparables 5 thru 6 are based on 'As Is'").
   - Adjustment narrative text (e.g. "$X per bedroom", "$Y per full bath / $Z per half bath", "$ per sq ft for GLA", garage space $ amounts, lot size $/sf) vs. the actual dollar adjustments applied in the grid for each comp — these must match.
   - Reconciliation / Reconciliation Addendum page: "ESTIMATED INDICATED 'SUBJECT-TO' VALUE" and "ESTIMATED INDICATED 'AS-IS' VALUE" figures, and the final "Opinion of Value" on the cover page and in the reconciliation section — confirm which value type the final opinion of value matches, and that a report using both hypothetical conditions (Subject To / As Is) clearly discloses both values and doesn't accidentally state only one where the report logic implies both should appear (or vice versa).
   - **Missing As-Is/Subject-To split is itself a major flag.** This appraiser frequently splits comps into two groups intentionally to derive TWO separate indicated values from one report: e.g. Comparables 1-3 valued "Subject To" and Comparables 4-6 (or 5-6) valued "As Is". Signs of this split: (a) an explicit disclosure sentence like "Comparables 1 thru 3 are based on 'Subject To' and Comparables 4 thru 6 are based on 'As Is'" in the Summary of Sales Comparison Approach, and/or (b) the two comp groups being adjusted with different methodology/logic (e.g. one group's condition/GLA/age adjustments follow different assumptions than the other group) because they represent different valuation bases, not an error. **Whenever the report's comps appear split into two groups like this, verify the Reconciliation Addendum actually shows two separately labeled indicated values — "ESTIMATED INDICATED 'SUBJECT-TO' VALUE OF THE SUBJECT" and "ESTIMATED INDICATED 'AS-IS' VALUE OF THE SUBJECT" — each derived from its own comp group's weighting table. If only one unlabeled "ESTIMATED INDICATED VALUE OF THE SUBJECT" appears (comps from both groups blended into a single weighted value, or no As-Is/Subject-To label at all despite the split existing in the grid), flag this as a missing value — the report is very likely supposed to present both an As-Is and a Subject-To value but only produced one, or blended them incorrectly.**
   - Do NOT flag differing adjustment treatment (e.g. condition, GLA, age logic) between the two comp groups themselves as an inconsistency — this is expected/intentional since each group supports a different value conclusion. Only flag inconsistency in adjustment logic WITHIN the same comp group (e.g. two comps in the same As-Is group where a worse-condition comp gets a smaller adjustment than a better-condition comp).
   - "As-is" Value of Site Improvements line, if present, vs. overall as-is value logic.
   - **Cost Approach land/site value narrative match.** Confirm the "Opinion of Site Value" dollar figure in the Cost Approach grid matches the number stated in the "Support for the opinion of site value" narrative sentence (e.g. "Based on allocation, the opinion of site value is $X"), and that the stated valuation method (allocation, extraction, comparable land sales, etc.) is consistent with how the number was actually derived. Also sanity check this site value isn't contradicted by other land/site references elsewhere in the report (e.g. site size adjustments in the sales grid, "As-is" Value of Site Improvements).
   - GLA math: Total Rooms / Bedrooms / Bathrooms above grade stated in the narrow "Finished area above grade contains: X Rooms, Y Bedrooms, Z Bath(s), N sf GLA" line vs. the Room Count row for the Subject column in the grid, vs. any per-comp GLA-derived sf figures — flag any mismatch.
   - Certification / USPAP boilerplate (the numbered certification paragraphs, hypothetical conditions / extraordinary assumptions statements, "as is" / "subject to" checkbox in the Reconciliation section) — flag contradictions, e.g. the checkbox says one condition but the narrative or value sections describe another, or a hypothetical condition is invoked in the text but not disclosed in the certification.
   - Comp distance/date/sale status sanity: flag comps that are unusually far away, stale (sale date far from effective date), or whose status (Active/Pending/Closed) doesn't match how they're described in the narrative.

3. Compare and flag discrepancies. Common categories seen in this appraiser's reports:
   - Bed/bath count mismatches between Subject and comps that aren't reflected with a corresponding adjustment (or an adjustment applied where counts actually match).
   - Room count row inconsistencies between the two grids often present in these reports (main grid vs. an addendum/second grid) — same comp should show the same bed/bath count in both places.
   - As-Is vs Subject-To value confusion: final Opinion of Value doesn't clearly state which value type it is, or doesn't match either the As-Is or Subject-To figure computed in the Reconciliation Addendum.
   - Missing As-Is or Subject-To value: comps are clearly split into two groups (by narrative disclosure or by differing adjustment methodology) but the Reconciliation Addendum only shows one blended/unlabeled indicated value instead of two labeled ones.
   - Cost Approach site/land value narrative not matching the grid figure or stated method.
   - Adjustment $ amount stated in the narrative doesn't match the $ amount actually applied in the grid for a given feature (bedroom count, bath count, GLA, lot size, garage).
   - GLA or room-count figures that don't match between the subject summary line, the grid, and any per-unit narrative descriptions.
   - Certification/boilerplate section contradicts the hypothetical condition / as-is-subject-to framing used elsewhere in the report.

4. Output: a **flagged issues list only** (no full pass/fail checklist, no memo). For each issue found, give:
   - A short label for the type of issue (e.g. "Bed/Bath Mismatch", "AS-IS/Subject-To Inconsistency", "Adjustment Math Mismatch", "GLA/Room Count Mismatch", "Certification Contradiction", "Comp Recency/Proximity Flag").
   - The specific location (page/section/comp #) and the conflicting values quoted directly from the report.
   - Why it's a potential problem in one sentence.
   If nothing is found in a category, do not list it — only report actual flags. If the report is completely clean, say so briefly rather than manufacturing issues.
   Reply with the flagged list directly in chat (no separate file needed unless the user asks for one).

## Notes
- This appraiser's reports are Texas non-disclosure market reports built with TrueTracts data, routinely containing both "Subject To" and "As Is" comps/values in the same report — this is expected and not itself a flag; only flag it when the two values or their disclosure are inconsistent with each other.
