# Subtext Product Profile — What the Skills Are Analyzing For

Grounded in a read-only survey of the SharePoint Projects area (July 2026). Skills should speak this
vocabulary when deriving programs, checking massings against zoning envelopes, and framing
entitlement asks. Items marked `[To confirm]` are observed labels whose internal definition should be
confirmed with the dev team before a skill asserts them.

## Product

Ground-up purpose-built student housing (multifamily, leased by the bed), Class-A, typically with
ground-floor retail/amenity on urban campus-edge sites; VERVE and EVER brands. ~47 active projects
across university markets (Ann Arbor, Chapel Hill, Clemson, Boone, Charlottesville, Columbia,
Fayetteville, West Lafayette, State College, Knoxville, Lexington, Madison, Oxford, Pittsburgh,
Gainesville, Tampa, College Station, Fort Collins, Boise, and others).

## Construction typologies (the massing vocabulary)

Proformas are run **per construction type** — filenames follow
`Proforma_<Project>_<Type>_<date>.xlsm` — meaning a site is normally evaluated against more than one
typology, and the zoning/entitlement question is which typologies the envelope and the path can carry:

| Observed label | Reading | Skill-relevant breakpoint |
|---|---|---|
| Type I | High-rise-capable noncombustible construction — the 12-story Chapel Hill product | Needed above wood-frame limits; usually implies the tallest zoning ask (height + often a discretionary path) |
| Type II | Mid-rise product `[To confirm internal definition vs. IBC label]` | Mid-rise envelope |
| 5-over-2 / podium | 5 wood-frame residential stories over 2-level concrete podium (parking/retail) | The workhorse; fits ~75–85 ft envelopes; podium levels interact with ground-floor-use and parking rules |
| 6-story configurations | Evaluated alongside 5-over-2 (e.g., Phoenix-Osborne) | The marginal-story question: does one more story force a different construction type, height relief, or path? |
| "w LL" variants (Type I w LL, Type II w LL) | `[To confirm — unverified; do not expand the acronym in deliverables]` | — |

**Implication for skills:** when a massing is provided, state which typology it implies and check that
typology's height/story needs against the envelope; when no massing is provided (program derivation),
present the viable typology options for the envelope rather than a single guess — that mirrors how
the dev team actually underwrites (multiple type runs per site).

## Standard instruments the skills will encounter

- **Proforma:** `SH Template Model w P3 Screener` (.xlsm) — the standardized student-housing model the
  zoning-compliance proforma parser targets; an `MF Template Model` exists for conventional
  multifamily. Label-search parsing, never fixed cells (versions shift).
- **Program templates:** `Program_Template`, `PreCon Program_Template` (.xlsx); a **Unit Mix
  Optimizer** exists — program/unit-mix data may arrive from these rather than a proforma.
- **IC process:** staged approvals (Market Approval → Initial Project Approval → Project Approval
  Update) with `Checklist_IC.xlsx`; tracked enterprise-wide in `Development/IC Tracking.xlsx`.
  Feasibility-memo outputs should slot into this cadence — the memo's verdict language
  (PROCEED / REVISE / ABANDON) maps to IC stage gates.
- **Project folder taxonomy:** every project folder carries an **Entitlements** area (Market Research,
  Land docs, Permits, Zoning studies) — per-project skill outputs (memos, trackers) belong there,
  alongside the market-folder `Finished Analysis` convention.

## Where things live

- Projects: `Subtext - Documents\General\Projects\<Market>-<Street>` (master folder template
  standardizes subfolders)
- Enterprise templates: `Subtext - Documents\General\Templates`
- Muni codes for skills: `Subtext - Documents\General\Markets\xxxxx. AI\Building Zoning Check\Markets\{Market}`
