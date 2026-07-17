# feasibility-memo — SPEC (not yet built; the orchestrator)

**Scope.** Recreates the "Feasibility Memo" example deliverable, student-housing-first: give it a site
(± a massing/program) → a 10-section desktop go/no-go:

1. Executive Summary & Recommendation (PROCEED / REVISE-PROCEED WITH CONDITIONS / ABANDON, with the
   conditions that flip the verdict each way)
2. Subject Property & Proposed Development
3. Market Feasibility (demand drivers: enrollment vs. on-campus beds; supply: bed pipeline in the
   walk-radius trade area; what the market supports → feeds §4 and §7)
4. Proposed Program & Physical Feasibility ("the one program" used consistently everywhere;
   site-specifics module feeds 4.2)
5. Legal & Regulatory Feasibility (zoning-compliance + entitlements modules, condensed — **one shared
   zoning determination**; the two example memos contradicted each other on by-right status, which is
   the failure mode this orchestrator exists to prevent)
6. Development Cost Estimate (planning-level stack; fees module feeds permits/taps line)
7. Value & Revenue Analysis (stabilized NOI → cap rate → completed value; residual land value
   cross-check; absorption-timing carry)
8. Feasibility Determination (the ULI value-vs-cost test + one-variable sensitivity table + "which
   single variable flips the verdict")
9. Risks, Data Gaps & Next Steps (risks-mitigants module)
10. Sources & Limitations

**The differentiator vs. the DirtAI example:** §7's rent assumption comes from the Subtext research
SQL DB (`subtext-sql` MCP — per-bed comps, YoY growth, pre-lease velocity) instead of a labeled guess.
The example's #1 data gap ("confirmed per-bed rent") is our strongest input. Supply (§3.2) similarly
draws bed inventory/pipeline from the DB where covered.

**Sequencing contract.** Modules run in dependency order: site-specifics + zoning → entitlements →
program derivation → fees + cost → DB-driven market/rent → value → determination → risks-mitigants.
The "one program" (beds/units/stories/GSF/parking) is fixed once in §4 and every later section uses
it — no section-local program drift.

**Program derivation speaks Subtext typologies.** The dev team underwrites each site against multiple
construction types (5-over-2 podium, mid-rise, Type I high-rise — see
`docs/subtext-product-profile.md`), so §4 should derive the program per viable typology for the
envelope (or take the typology from a provided massing/proforma — the standardized proforma is the
`SH Template Model w P3 Screener` .xlsm), pick one for "the one program," and show the rejected
typologies with the reason (envelope, path, or cost). Cost stack in §6 is typology-dependent —
podium vs. Type I is a different $/SF world.

**House rules.** Every figure is platform data, cited public source, or a labeled assumption. Section
verdicts (GO / GO-with-conditions / FAIL) per dimension. Sensitivities recompute the margin, one
variable at a time. Student framing throughout: beds not units, per-bed rents, August delivery cliff,
academic pre-lease absorption (step function, not linear ramp).

**Build last** — it composes the other modules and its design should follow their settled output
contracts.
