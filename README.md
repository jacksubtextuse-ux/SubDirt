# SubDirt

Subtext's student-housing site-analysis toolkit. Give it a site → it analyzes everything (zoning,
entitlements, fees, physical conditions, market, cost/value). Give it a massing or proforma → it
tells you what you can and can't build. The target deliverables are modeled on the DirtAI-style
Feasibility Memo and Zoning & Entitlement Memorandum (examples live on SharePoint under
`General/Markets/xxxxx. AI/SubDirt AI/Deliverable Example` — deal documents deliberately stay out of
this repo).

## Module map

| Module | Status | What it does |
|---|---|---|
| [`skills/zoning-compliance`](skills/zoning-compliance) | ✅ Built (v1, Cowork-validated) | Building-vs-code compliance matrix (Word + Excel); district breakdowns. Columbia MO + Gainesville tested. |
| [`skills/student-housing-dev-fees`](skills/student-housing-dev-fees) | ✅ Built | Exhaustive, primary-source fee schedule from an address; jurisdiction stack + supremacy resolution; branded Excel workbook via bundled script. |
| [`skills/student-housing-entitlements`](skills/student-housing-entitlements) | 🆕 Built — needs a live-market shakedown | Entitlement path determination: use classification, path enumeration/ranking, bodies + timelines, plan conformance, precedent-based political risk, conditions forecast. Word memo + Excel tracker. |
| [`skills/site-specifics`](skills/site-specifics) | 📋 Spec only | Physical/environmental layer: flood, karst, radon, USTs, utilities, adjacency → diligence triggers. |
| [`skills/risks-mitigants`](skills/risks-mitigants) | 📋 Spec only | Synthesis: 4-dimension risk/mitigant table, consolidated data-needed list, ordered next steps. |
| [`skills/feasibility-memo`](skills/feasibility-memo) | 📋 Spec only — build last | Orchestrator: composes all modules into the 10-section go/no-go memo with the ULI value-vs-cost test. Rent/supply inputs from the Subtext research DB (`subtext-sql` MCP) — the edge over the DirtAI original. |

## House rules (apply to every skill)

- Primary sources only; **never** estimate, infer "typical" values, or carry numbers from memory.
- Cite everything: code section, adopting instrument, or URL + access date. Source-and-vintage line
  under every table.
- Facts, assumptions, and interpretations are explicitly separated; gaps are `[Data needed: …]` /
  `[To be verified with <agency>]`, never smoothed over.
- Timelines labeled statutory (cited) vs. typical (labeled). Section-level verdicts (GO / conditioned
  / FAIL).
- Student-housing framing: beds not units, per-bed rents, academic pre-lease cycle and the August
  delivery cliff, enrollment vs. on-campus capacity, walk-radius trade areas.

## Packaging for Cowork

```
python tools/package_skill.py skills/<name>        # → dist/<name>.skill
```

Install via Cowork → Settings → Skills → Install from file. Claude Code can use the skill folders
directly.

## Data dependencies

- **Muni codes / comp plans**: SharePoint market folders under
  `General/Markets/xxxxx. AI/Building Zoning Check/Markets/{Market}`.
- **Rent & supply data**: Subtext research SQL DB via the `subtext-sql` MCP (see the Unit Reporting
  pipelines on SharePoint for the data model).
- **Council records**: jurisdiction portals (Legistar/Granicus/etc.); pairs with the
  city-council-transcript-analysis skill.
