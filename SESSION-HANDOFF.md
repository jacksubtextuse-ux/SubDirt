# Session Handoff — SubDirt AI (through July 20, 2026)

Full context transfer for picking up in a fresh terminal. Read top to bottom once; everything else
is linked. Companion doc: `HANDOFF.md` (the coworker/feasibility interface contract — different
audience, still current).

## The project in one paragraph

SubDirt AI is Subtext's in-house recreation of the DirtAI deliverables (Feasibility Memo + Zoning &
Entitlement Memo), student-housing-first: give it a site → full analysis (zoning, entitlements,
fees, site specifics, market); give it a massing/program → what you can and can't build.
Jack owns the **Zoning & Entitlement Memorandum** workstream; the coworker owns the **Feasibility
Memo** (contract in `HANDOFF.md`; his memo consumes the Z&E memo's determinations verbatim — the
two must never disagree on entitlement posture). Everything so far is explicitly a **dry run with
no tuning** — a tuning/setup phase is planned next, driven by boss redlines on the Clemson memo.

## Repo state

- Repo: https://github.com/jacksubtextuse-ux/SubDirt.git · local clone at
  `C:\Users\JackBranding\repos\SubDirt` (deliberately OUTSIDE OneDrive — git + SharePoint sync
  conflict). **Repo is PUBLIC** — flagged to Jack twice; deal documents deliberately never
  committed. Recommend flipping private.
- **Branch: everything after the first two commits lives on `branding-logo` (unmerged).** Direct
  pushes to `main` get blocked by the permission classifier — use feature branches + PRs. Merge
  the open branch: https://github.com/jacksubtextuse-ux/SubDirt/pull/new/branding-logo
- Git identity is repo-local (Jack Branding / jbranding@subtextliving.com).

## What's built (module map)

| Piece | State | Notes |
|---|---|---|
| `skills/student-housing-entitlements` | **Built + live-run-proven** | SKILL.md + 4 references (pathway taxonomy, use-classification guide, political-precedent protocol, memo/tracker templates) + `references/run-loop.md` (the formalized 6-phase run protocol) + `scripts/build_branded_memo.py` + `assets/subdirt_logo.png` |
| `scripts/build_branded_memo.py` | **Proven** | Generic JSON-spec → branded .docx renderer (logo title page, TOC field, Everest/Sage tables, status-color cells, source-and-vintage lines, footers, disclosure; self-verifies). Schema at top of script. Reuse for ALL Word deliverables incl. feasibility. |
| `skills/student-housing-dev-fees` | Built (Jack's) | Ported as-is; its `build_fee_workbook.py` is the Excel house pattern |
| `skills/zoning-compliance` | **LEGACY — mine, don't run** (Jack's call) | Keep the analysis structure: compliance-matrix vocabulary (PASS/PASS*/FAIL/VERIFY/PD), by-right vs PD-forward framing, `analytical-framework.md`, `pd-strategy-guide.md`, proforma parser. The market-folder/muni-code-document sourcing workflow is dead — online sources via the registry instead. |
| `data/market-sources.json` | **14 jurisdictions / 10 markets verified** | The scaling mechanism for all-markets zoning. Schema in-file. |
| `skills/permit-history` | SPEC + pilot done | Accela class = production-scriptable today; EnerGov class = needs one-time Playwright capture. ~60–70% of the 47-project back-catalog pullable unattended. |
| `skills/site-specifics`, `skills/risks-mitigants`, `skills/feasibility-memo` | SPEC.md stubs | Feasibility = coworker's; build last (composes the rest) |
| `assets/branding.md` + logo | Final | Official mark = **Option D** (sage→Everest gradient "subdirt" + lime "ai", Arial Rounded MT Bold). Palette: Everest `16352E`, Sage `4EA57E`, Lime `C1D100`, Beige `F7F1E3` (matches fees workbook constants). A–C archived. Logo options page (shown to boss): https://claude.ai/code/artifact/84779e50-1be6-4c48-ad10-8889b3ff0173 |
| `tools/package_skill.py` | Works | Zips a skill folder → Cowork-installable `.skill` (`dist/`) |

## Deliverables produced (all on SharePoint, NOT in repo)

Base: `C:\Users\JackBranding\Subtext\Subtext - Documents\General\Markets\xxxxx. AI\SubDirt AI\`

- **`Demo Output\`** — Lexington UK-assemblage Z&E memo re-rendered through the pipeline (docx/pdf +
  spec JSON) — the pipeline validation demo.
- **`Example run\Finished Analysis\`** — **the VERVE Clemson live run** (first original output):
  `VERVE-Clemson_VictoriaSquare_Zoning_Entitlement_Memo.docx/.pdf` (12 pp),
  `VERVE-Clemson_Entitlement_Tracker.xlsx` (Path Steps / Precedents / Risk Register / Open Items),
  `verve_clemson_ze_spec.json`, exhibits. Input was `Example run\Design Program_Clemson
  Site_20260701 JM.xlsx`.
- **`Permit Pilot\VERVE_Lexington_permit_record.md`** — full Accela pull (see below).
- Original DirtAI examples: `Deliverable Example\` (the two target memos — note they CONTRADICT each
  other on by-right status; preventing that is why the feasibility memo must consume the Z&E memo's
  determinations).

## The VERVE Clemson findings (live deal — someone should act on these)

Memo verdict: the design program's zoning basis is stale. Verified against live code
(encodeplus print endpoints, secids 3554/3742/3715/3693):
1. **$30/SF community contribution above 5 stories — not the $10/SF in the workbook** (Sec. 19-405
   verbatim). East side of College Ave "bookended by Strode Circle": **3-story base / 5-story hard
   cap** — whether the site is in that block is unresolved and is **open item #1** (written
   determination from Clemson Planning, 864-653-2050). Illustrative exposure if in-block: ~$3.6M.
2. **Parking: 0.5/bed basis not found in code** — Table 19-802 says 1 space/bedroom; design is short
   even on its own basis (227 residential stalls vs 322 required; 293 total).
3. **Every comparable Clemson project went negotiated PD, not straight CM rezoning** — MODA PD-21
   (1 space/bed, workforce units, bonds, occupancy caps), HUB 4–3 under litigation threat, **Rambler
   5–2 Oct 2025 directly adjacent** (~$9M benefits package; an opponent lives at 100 Strode Circle),
   201 Pine St pending on a knife's edge (final vote was set for mid-July 2026 — CHECK THE OUTCOME,
   it's the live gauge). Recommended path: PD on the Rambler template, 6–9 months, second reading
   done before the **Nov 3, 2026 election** (3 council seats turn over).
4. Workbook contains two conflicting programs (conformance sheet ran 374u/476b; program sheet
   190u/602b) — governing program must be reconciled.

## Permit pilot results

- **LFUCG/Lexington (Accela ACA): full success, no login.** VERVE Lexington complete record — main
  permit BLD-CNC-25-00122 ($68,690,050 project cost, 381,355 SF, 7 stories, 275 units, GC Southern
  Building Group), zone change complete 3/2025, land disturbance issued 5/2026 → **real observed
  LFUCG timeline: zone change → land disturbance ≈ 14 months**. Scripting recipe in the registry
  notes (GET search + one __VIEWSTATE postback → permanent CapDetail URLs).
- **Clemson (Tyler EnerGov CSS): blocked** — JSON endpoint 500s on synthetic payloads; needs a
  one-time headless (Playwright) capture. Fallback that works: CivicPlus DocumentCenter stable GETs
  (HUB PD-22 = View/898, MODA PD-21 = View/896).

## Cross-market doctrine (encoded in registry notes — trust it)

Municode AND eCode360 403 all automated fetches (no workaround found for either). encodeplus has
fetchable print endpoints (`doc-view.aspx?secid=####&print=1`) — but its eReader flipbook pages can
be YEARS-stale snapshots (burned the Clemson workbook). **County/regional ArcGIS REST services are
the reliable machine route to parcel zoning** (verified in Columbia, Fayetteville, Knoxville,
Gainesville, Chapel Hill, Centre Co PA, Washtenaw). Beacon/qPublic/Schneider parcel sites 403.
Ann Arbor publishes its UDC as a directly fetchable official PDF (best case). Watch for
retired-but-live Legistar instances (Gainesville). Strategy flags found: Chapel Hill 4-unrelated-
persons cap; LUMO rewrite (draft ~summer 2026); State College full zoning rewrite in progress;
West Lafayette zoning is county-wide via Tippecanoe APC.

## How to run the next site (the run loop)

`skills/student-housing-entitlements/references/run-loop.md` — 6 phases: intake (log the input's
assumptions AS VERIFICATION TARGETS; catch internal contradictions; extract exhibits via zipfile →
PIL re-encode to PNG) → two parallel background research agents (code-verification + political-
precedent; briefs and hard-rules text are in the doc) → reconcile (the program-basis vs live-code
discrepancy table is the money section) → author spec JSON → render
(`python build_branded_memo.py spec.json out.docx`, then Word COM to update TOC + export PDF, then
pymupdf spot-check) → deliver to `Finished Analysis` + BLUF-only chat report → **mandatory retro**
(push learnings to skill/registry same day).

## Open threads, in priority order

1. **Merge `branding-logo` → main** (PR link above) so the coworker branches off current state.
2. **Boss redlines on the Clemson memo** → drives the tuning pass (deliverable structure/tone).
3. **Clemson pre-app questions** (tracker Open Items sheet is the meeting agenda) + check the
   201 Pine St final vote outcome.
4. **Registry tranche 2** — remaining active-project markets (Boone, Charlottesville, Oxford,
   Pittsburgh, Boise, Tampa, Tempe/Phoenix, College Station, Fort Collins, Miami, STL, Nashville…).
   Reuse the batch-agent brief pattern (in run-loop.md; include the cross-market doctrine above in
   the brief — it speeds agents up).
5. **Permit sweep decisions**: cadence (one-time vs quarterly cron), results location on SharePoint,
   Playwright for the EnerGov class now or later. Then run the 47-project back-catalog.
6. **Feasibility memo build** (coworker; `HANDOFF.md` + `skills/feasibility-memo/SPEC.md`) — DB
   (`subtext-sql` MCP) wiring for rents/supply is the untested differentiator.
7. Site-specifics and risks-mitigants skills (SPEC stubs ready).

## Environment gotchas

- Shell is Windows: PowerShell + Git Bash both available; `gh` CLI NOT installed (bash) — use git +
  API/web for GitHub ops.
- Word/Excel COM automation works (used for TOC update + PDF export; close open workbooks before
  overwriting).
- Images extracted from Office files may be mislabeled formats — always PIL re-encode to PNG before
  python-docx.
- OneDrive files can be cloud-only/locked — copy to scratch before zipfile reads if PermissionError.
- Background research agents can die on session rate limits with zero output — just relaunch the
  same brief.
- The Subtext product vocabulary (typologies: 5-over-2 podium workhorse, Type I high-rise, "w LL"
  variants [unconfirmed meaning]; `SH Template Model w P3 Screener` proforma; IC stage gates) is in
  `docs/subtext-product-profile.md` — memos should speak per-typology envelope answers.
