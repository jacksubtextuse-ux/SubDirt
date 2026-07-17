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

**Pilot (July 2026, running):** VERVE Lexington (185 E Maxwell St, LFUCG) + HUB Clemson (Keowee
Trail, Clemson SC) — chosen to test two different portal stacks and produce immediately useful data.
Pilot findings will define the registry's `permits` fields and this skill's SKILL.md.

**Open design questions (settle after pilot):**
- Batch cadence for the 47-project back-catalog: one-time sweep vs. monitored (permits change status;
  a quarterly refresh loop may be worth a cron).
- Where results live: repo (no — project data), SharePoint per-project folders vs. one master
  workbook in the Development tracking folder.
