# The Run Loop — Standard Protocol for a Zoning & Entitlement Memo Run

Formalized from the VERVE Clemson live run (July 2026). A run takes a site (program workbook,
address list, or platform export) and produces the branded Z&E Memorandum + Entitlement Tracker in
one pass. Follow the phases in order; Phases 1's two research tracks run **in parallel**.

## Phase 0 — Intake (~15 min)

1. **Parse the input.** Program workbook (design program / proforma / testfit), address list, or a
   verbal site description. Extract: parcels/addresses, acreage, program (units/beds/stories/
   typology/parking/retail), and every zoning assumption the input carries (district targets, fee
   figures, ratios, height basis). **Record each assumption with its stated basis — these get
   re-verified in Phase 2, never trusted.**
2. **Check for internal contradictions** in the input (two program versions, a conformance sheet run
   against a different testfit, N/A-vs-included fee cells). Log them now; they go in §5/§8 of the memo.
3. **Extract exhibits** — aerials, zoning-map crops, parcel maps embedded in the workbook
   (`zipfile` → `xl/media/`). Re-encode via PIL to PNG (python-docx rejects exotic encodings). Stage
   in the output folder.
4. **Sources check — online-first.** `data/market-sources.json` in the SubDirt repo is the source
   map: code host + fetchable route, ArcGIS REST zoning services, parcel GIS, permit and agenda
   portals, with fetchability warnings. Muni code is read from the **live online host**, never from
   memory and not from curated document folders (the legacy zoning skill's market-folder workflow is
   dead — its analysis structure survives in Phase 2, its sourcing doesn't). If the market has no
   registry entry, the Phase 1 code agent also captures registry fields; merge them back after the
   run. If a user hands you code documents directly, use them, but date-check them against the live
   host — local copies go stale.
5. Create the output folder next to the input (`<input folder>\Finished Analysis\`), or the market
   folder's `Finished Analysis` when running from a market-folder context.

## Phase 1 — Parallel research (agents; ~15–20 min wall clock)

Dispatch **two background research agents** with the briefs below. Both carry the same hard rules —
paste them verbatim into every brief:

> HARD RULE: report ONLY what you actually verified at a URL you fetched — never from general
> knowledge or memory. For every fact: citation (code section), source URL, verified /
> could-not-verify. Anything unverified goes in an explicit COULD NOT VERIFY list — an honest gap is
> required output, a guess is failure. Distinguish adopted law from drafts/pending items.

**Agent 1 — Code verification.** Parameterize with: jurisdiction, parcels/addresses, the target
district(s), and **every zoning assumption from Phase 0 stated as a verification target** ("the
program assumes X — verify against live text"). Task list: district purpose + use permissions;
dimensional table + endnotes (quote verbatim where money/height turns on them); parking basis;
fees/contributions tied to zoning; overlays (architectural review, historic, flood); amendment/
rezoning process mechanics with statutory clocks; comprehensive-plan status and designation;
pending amendments/moratoria; current per-parcel zoning from map/GIS. Include the access tactics
(SKILL.md "Research tactics"): print endpoints on JS-blocked hosts, stale-snapshot detection,
qPublic 403 handling. If the market registry lacks an entry, ask for the registry JSON fields too.

**Agent 2 — Political precedent.** Parameterize with: jurisdiction, project scale, corridor/
neighborhood. Task list per `political-precedent-research.md`: the precedent table (~5 years,
comparable PBSH/multifamily decisions with PC votes, council votes, margins, opposition themes,
conditions imposed); regulatory-posture history (moratoria, lawsuits, ordinance changes); council
composition and member-level voting patterns; organized opposition; demand context (enrollment,
pipeline); timing factors (elections, plan updates, observed application-to-decision durations).

Cap each brief's requested output (~1,200 words) and require source URLs + access dates throughout.

## Phase 2 — Reconcile (~20 min)

The analytical core. Build the **input-basis vs. live-code discrepancy table**: one row per Phase 0
assumption — program basis | live code (verified, cited) | impact (PASS / VERIFY / FAIL). In the
Clemson run this table surfaced a 3x fee understatement, an unsourced parking ratio, and an
unresolved height cap — expect it to be the memo's most valuable section. Then:
- Determine the **path recommendation** per `entitlement-pathways.md` ranking — and check it against
  *practice*, not just code: if every recent comparable went PD, say so and recommend accordingly.
- Rate risks per the `political-precedent-research.md` rubric, evidence sentence per rating.
- Sequence the open items (resolver + method); #1 is whatever the verdict most depends on.

## Phase 3 — Author the spec (~30 min)

Write the JSON spec for `build_branded_memo.py` (schema at top of script), combined Z&E memo shape
per `memo-and-tracker-templates.md`. Conventions that made the Clemson memo land:
- BLUF carries the three most decision-relevant findings and the recommendation — nothing else.
- Quote ordinance text verbatim where a conclusion turns on it; give every table a `source` line
  with access dates; mark unverifiable cells `[To be verified]` (they auto-color amber).
- Labeled illustrations are allowed for exposure math ("illustrative — basis undefined in ordinance")
  but must carry the caveat in the same sentence.
- Statutory clocks cite their section; everything else is "typical (labeled)".
- Appendix: precedent table + demand context.

## Phase 4 — Render & verify (~10 min)

1. `python build_branded_memo.py spec.json out.docx` — check the JSON summary (status ok, counts).
2. Word COM pass: update fields/TOC, export PDF (`SaveAs …, 17`).
3. Visual spot-check 1–2 rendered PDF pages (pymupdf → PNG) — status colors, table widths, images.
4. Build the tracker (4 sheets per `memo-and-tracker-templates.md`) with the run's actual content:
   Path Steps (with statutory clocks from Phase 1), Precedents, Risk Register, Open Items.

## Phase 5 — Deliver & report

Files: memo .docx + .pdf, tracker .xlsx, the spec .json (reusable), staged exhibits — all in
`Finished Analysis`. Chat report: BLUF-level only — recommended path, months, risk rating with its
strongest evidence, the top three open items, and any input-integrity flags. Do not restate the memo.

## Phase 6 — Retro (5 min, mandatory)

Push learnings back to the repo the same day: new research tactics → SKILL.md; renderer gaps → the
script; market infrastructure discovered → `data/market-sources.json`. The loop improves only if
every run feeds it.

**Cross-workstream handoff:** the memo's classification, path, months, and risk rating are the
inputs the feasibility memo consumes (HANDOFF.md) — keep them stated crisply enough to lift verbatim.
