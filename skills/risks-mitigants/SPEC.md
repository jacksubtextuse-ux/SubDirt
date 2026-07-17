# risks-mitigants — SPEC (not yet built)

**Scope.** The synthesis layer — §9 of the example feasibility memo. Consumes the outputs of the other
modules (zoning-compliance, student-housing-entitlements, student-housing-dev-fees, site-specifics,
market/comp data) and produces:

1. **Risk & mitigant table across four dimensions** — Market, Physical, Legal/Regulatory, Financial
   (+ Seller/transaction where relevant). Each row: Dimension | Risk | Mitigant. Risks must trace to
   a finding in an upstream module — this skill does not discover new risks, it consolidates and
   ranks them.
2. **Consolidated data-needed list** — every `[Data needed: …]` and `[To be verified: …]` item from
   upstream outputs, deduplicated, each with where/how to resolve it (study, agency, document).
3. **Recommended next steps, in order** — sequenced by what most cheaply de-risks the verdict first
   (the example's pattern: pre-app meeting → rent study → seller intent/price → geotech + Phase I →
   re-underwrite).

**Key design question (resolve before building).** Is this a standalone skill or a section-generator
inside the feasibility-memo orchestrator? Leaning: build as a small standalone skill with a defined
input contract (a folder of upstream outputs), so it can also run on partial analyses; the
orchestrator then calls it last.

**House rules.** No new facts. Every risk cites its upstream source. Rank by verdict-criticality, not
category. Student-specific risks to always check for presence upstream: pre-lease-cycle timing (the
August cliff), competitive bed pipeline concentration, per-bed rent confirmation, enrollment-trend
dependence, unrelated-persons/occupancy caps.
