# permit-history — SPEC (pilot in progress)

**Scope.** Given a project (name + address + jurisdiction), pull its public permit record from the
jurisdiction's online portal: building permits, demo/site/grading permits, trade permits, COs, and
planning/zoning case numbers — with type, status, key dates, valuation, and contractor where exposed.

**Two use cases:**
1. **Past-project benchmarking** — pull permit histories for Subtext's delivered/under-construction
   projects to build a reference set: what permits each jurisdiction actually required, fee amounts
   actually paid (calibrates the fees skill), and issue-date sequences (calibrates entitlement/permit
   timelines in the run loop).
2. **Comp intelligence** — pull competitors' permits on live deals (e.g., HUB/Rambler status informs
   VERVE Clemson's supply timing).

**Method.** Portal-first, registry-driven:
- Look up (or discover and record) the market's permit portal in `data/market-sources.json` —
  system type (Accela, Tyler EnerGov CSS, CitizenServe, OpenGov, SmartGov, custom) determines the
  access pattern. EnerGov CSS and Accela CitizenAccess often expose JSON search endpoints usable
  without login; others are JS walls where the fallback is agenda attachments, monthly permit-report
  PDFs (many cities publish them), or state contractor-license databases.
- Address-first search, then parcel number, then project/applicant name. Capture every permit on the
  parcel, not just the headline building permit — demo/site permits date the real construction start.
- House rules apply: only records actually retrieved; portal-blocked = documented as blocked with the
  fallback evidence used; never reconstruct permit data from news.

**Output.** Per project: a permit table (number, type, description, status, dates, valuation,
contractor) + portal-access notes feeding back into the registry. Batch mode: one Excel workbook per
run (xlsx-author pattern; one sheet per project + summary sheet).

**Pilot results (July 17, 2026) — capability proven, portal-class-dependent:**
- **Accela ACA (LFUCG/Lexington): production-ready today.** No-login GET keyword search
  (`/LEXKY/Cap/GlobalSearchResults.aspx?QueryText=`); row links are ASP.NET `__doPostBack` — replay
  with `__VIEWSTATE` (no cookies/`__EVENTVALIDATION`) to mint **permanently GET-able
  `CapDetail.aspx` URLs**. Full pull achieved for VERVE Lexington: 12 records — building permit
  (BLD-CNC-25-00122: $68,690,050 project cost, 381,355 SF, 7 stories, 275 units, GC Southern
  Building Group), fire suppression, land disturbance (Issued 5/2/2026), demolition (Complete),
  zone change PLN-MAR-25-00005 (Complete 3/2/2025), two major development plans, minor plat.
  ~30 lines of Python to script.
- **Tyler EnerGov CSS (Clemson): the hard class.** Angular SPA; its JSON search endpoint exists but
  500s on synthetic payloads — needs a one-time headless-browser (Playwright) capture of the real
  search POST body, then likely scriptable; version-fragile. Fallback that worked: PD ordinances on
  CivicPlus DocumentCenter (stable `/DocumentCenter/View/{id}` GETs) + news/agenda trail.
- **Estimate: ~60–70% of permit history is pullable unattended**; the rest needs browser automation.

**Registry fields per market** (now being captured in `data/market-sources.json` notes): portal
vendor + version; canonical search URL and GET-ability; auth/session requirements; record-numbering
scheme; fallback evidence sources (DocumentCenter/AgendaCenter paths); known data quirks (e.g.,
LFUCG future-dated File Date fields — quote portal data as shown, flag anomalies).

**Open design questions (settle before the 47-project sweep):**
- Batch cadence: one-time sweep vs. monitored (permits change status; a quarterly refresh cron may
  be worth it — statuses like "Awaiting Payment" → "Issued" are the signal).
- Where results live: repo (no — project data), SharePoint per-project folders vs. one master
  workbook in the Development tracking folder.
- Whether to stand up Playwright for the EnerGov-class portals now or triage those markets to
  fallback-evidence mode.
