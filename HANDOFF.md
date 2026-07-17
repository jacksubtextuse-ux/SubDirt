# Handoff — Feasibility Memo Workstream

Ownership split (July 2026): **Jack → Zoning & Entitlement Memorandum** ·
**you → Feasibility Memo**. This doc is everything the feasibility side needs to run independently.

## Start here

1. **Read `skills/feasibility-memo/SPEC.md`** — the 10-section structure, module sequencing, and the
   design rules already settled (one shared program, one shared zoning determination, per-typology
   program derivation).
2. **Read the example deliverable** on SharePoint (`.../SubDirt AI/Deliverable Example/Feasibility
   Memo - UK Assemblage...docx`) — that's the target, student-housing-first. Deal documents stay out
   of this repo (it's public unless/until flipped private).
3. **Look at the working demo** in `.../SubDirt AI/Demo Output/` — the Lexington Zoning & Entitlement
   memo rendered end-to-end through the shared pipeline, plus the JSON spec that produced it. Your
   memo should come off the same rails.

## What the zoning/entitlement side hands you

The feasibility memo's §5 (Legal & Regulatory) does **not** re-derive anything — it condenses the
Zoning & Entitlement Memorandum's determinations verbatim:

| You consume | Where it lives in the Z&E memo |
|---|---|
| Use classification the analysis proceeds on | §4.1 |
| By-right vs. discretionary determination, per parcel | §4.2 |
| Recommended path + fallback, with mechanism citations | §4.3 / §7 |
| Entitlement months (base / contested) → carry cost & schedule scenarios | §7 |
| Political risk rating + evidence → risk register | §8 |
| Open items / [To be verified] list → §9 data-needed list | §8.2 |

**The one rule that matters:** the two memos must never disagree on entitlement posture. The original
DirtAI examples contradicted each other (feasibility said "no rezoning needed," zoning memo said
"rezoning required") — the whole point of the shared determination is preventing that. If your
underwriting wants a different posture than the Z&E memo states, that's a conversation, not an edit.

## Shared infrastructure (don't rebuild these)

- **Branded Word renderer**: `skills/student-housing-entitlements/scripts/build_branded_memo.py` —
  JSON spec → SubDirt-branded .docx (logo title page, TOC, Everest/Sage palette, status-colored
  tables, source-and-vintage lines, footers, disclosure). Schema at the top of the script. It's
  generic — author your feasibility spec against it. If it needs a new block type (e.g., a
  sensitivity-matrix table style), extend the script rather than forking it.
- **Branding**: `assets/branding.md` (palette/type/conventions) + `assets/subdirt_logo.png` (official
  mark — Option D; A–C are archived alternates).
- **House rules**: README "House rules" section — primary sources, labeled assumptions,
  `[Data needed:]` placeholders, section verdicts, statutory-vs-typical timeline labeling.
- **Excel**: follow the fees skill's pattern (`skills/student-housing-dev-fees/scripts/
  build_fee_workbook.py`) — JSON spec in, branded workbook out, self-verification pass, JSON summary.

## Data sources for your sections

- **§3 Market / §7 Value — rent and supply**: the Subtext research SQL DB via the `subtext-sql` MCP.
  Data model notes live in the Unit Reporting pipelines on SharePoint
  (`.../SubDirt AI/Unit Reporting Using Database/Clemson/SKILL.md` documents the key view:
  `dbo.YoYPropertyRentGrowth_CH`; `dbo.MonthlyPropertyData_CH` for property/beds resolution). Rent is
  an advertised per-bed proxy — label it as such. This is the edge over the DirtAI original: their #1
  data gap (confirmed per-bed rent) is our strongest input.
- **§6 Cost — fees lines**: run `student-housing-dev-fees` for the permits/taps/impact stack rather
  than estimating.
- **§4 Program**: derive per construction typology — see `docs/subtext-product-profile.md`. The
  standardized proforma, when one exists, is the `SH Template Model w P3 Screener` (.xlsm; parse by
  label search, never fixed cells — see `skills/zoning-compliance/references/proforma-parser.md`).

## Repo workflow

Feature branches + PRs into `main` (direct pushes to main are gated). Current open branch:
`branding-logo` (logo assets + renderer + branding). Keep skill folders self-contained — Cowork
packaging (`python tools/package_skill.py skills/<name>`) zips one folder.
