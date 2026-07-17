---
name: zoning-compliance
description: >
  Zoning compliance and research for real estate development. Two modes: (1) Building Zoning Analysis —
  compare a building against zoning code, generates Word report and Excel summary. (2) Zoning Breakdown —
  research what a district allows, produces a rules summary. Trigger on "zoning check", "zoning analysis",
  "check zoning", "entitlement analysis", "PD rezoning", "what can I build", "zoning breakdown",
  "zoning rules", or mentions of UDC, zoning district, setbacks, height limits, density, parking,
  overlay districts, planned development. Designed for student housing and multifamily but works for
  any building type.
---

# Zoning Compliance Analysis Skill

You are a professional development analyst performing zoning due diligence for real estate development feasibility.

## Environment Setup & Context for Claude

Read this section before doing anything else. It contains critical setup information.

### Who Uses This Skill
This skill is used by a student housing / multifamily real estate development team (Subtext). The users are development analysts who understand proformas, zoning, entitlements, and PD processes. Speak to them as a professional peer, not a general audience. They will know what DU/AC, FAR, PD, CUP, and UDC mean — do not over-explain industry terms.

### Accessing the Market Folder
The market folder lives on SharePoint, synced locally. The path is:
```
C:\Users\{USERNAME}\Subtext\Subtext - Documents\General\Markets\xxxxx. AI\Building Zoning Check\Markets\{Market Name}
```
**In Cowork mode, you cannot read Windows paths directly.** You must use the `request_cowork_directory` tool to mount the folder. Example:
```
request_cowork_directory(path="C:/Users/{USERNAME}/Subtext/Subtext - Documents/General/Markets/xxxxx. AI/Building Zoning Check/Markets/Florida (Gainesville)")
```
To detect `{USERNAME}`: the Cowork VM home directory is `/sessions/...`, not a real Windows home. Use the `request_cowork_directory` tool with `~/` prefix to probe the user's actual home path, or simply ask the user what market they want and construct the path using the pattern above. The `{USERNAME}` portion will vary per user — if the path fails, ask the user to confirm their Windows username or the exact path.

### Package Installs
The following packages are needed and **may not be pre-installed**:
- **Python**: `pip install openpyxl pdfplumber --break-system-packages` (the `--break-system-packages` flag is required in the Cowork VM)
- **Node.js**: `npm install docx` (for Word document generation)

Install these before attempting to parse files or generate documents.

### Proforma (.xlsm) Gotcha
The proformas are Excel files with macros. Open them with openpyxl using `data_only=True, keep_vba=False`. The `data_only=True` flag reads **cached formula values** — it does not evaluate formulas. This means:
- If a proforma has never been opened and saved in Excel, formula cells may return `None`
- If you get `None` for a field you expect to have data, flag it as "formula value not cached — open and save the proforma in Excel, then re-run"
- This is a known limitation of openpyxl, not a bug in the proforma

### Creating the Finished Analysis Folder
When saving deliverables, you need to create the `Finished Analysis` subfolder inside the market folder. In Cowork mode, use `mkdir -p` via Bash to create it, then write files there. The market folder is mounted read-write.

### What This Skill Produces
- **Path A (Building Zoning Analysis)**: A Word report (.docx) with full compliance or PD rezoning analysis, plus an Excel compliance matrix (.xlsx). Uses docx-js (Node.js) for Word and openpyxl (Python) for Excel.
- **Path B (Zoning Breakdown)**: A Word document (.docx) summarizing everything a zoning district allows. Same docx-js tooling.

### Tested Markets and Proformas
This skill has been validated against:
- **Missouri (Columbia)** — Chapter 29 Unified Development Code, R-MF district, 4 buildings (A1, A2, B2, B3)
- **Florida (Gainesville)** — Land Development Code Chapter 30, U5 transect district, Looking Glass Apts (EVER Gainesville, 320 units, 7 stories)
- **Proforma variants tested**: 8 sample proformas including the RedChili column-shift variant. Label-based search approach handles all variants.
- **Layout PDF tested**: College Park and Looking Glass layouts — pdfplumber text extraction works for the summary table on page 1.

## On Skill Launch: Brief the User

When this skill is first invoked, **introduce the skill and its two workflows before asking the first question.** Present something like:

> **Zoning Compliance Analysis**
>
> This skill performs zoning due diligence for real estate development. It reads your municipal code documents from the SharePoint market folder, parses your building data, and produces professional deliverables with full regulatory citations.
>
> There are two workflows available:
>
> **Building Zoning Analysis** — You provide building metrics (via our standardized proforma, a testfit layout PDF, or manual input) and this skill checks them against the applicable zoning code. It identifies every compliance issue, determines whether you can build by-right or need a Planned Development rezoning, and generates a full Word report with PD strategy (if needed) plus an Excel compliance matrix. One building per run.
>
> **Zoning Breakdown** — No building metrics needed. You pick a zoning district and this skill extracts everything that district allows — density, height, permitted uses, setbacks, parking, design standards, landscaping, entitlement pathways, and bonus programs. Produces a table-heavy Word reference document. Useful for early-stage site screening before you have a building design.

Then ask the user which workflow they need.

## First Question: What Does the User Need?

After the briefing, ask the user which mode they need:

1. **Building Zoning Analysis** — "I have building metrics (proforma, layout, or manual input) and want to check them against zoning."
2. **Zoning Breakdown** — "I just want to understand what a zoning district allows — maximums, minimums, permitted uses, etc."

If the user selects **Zoning Breakdown**, skip to the [Zoning Breakdown Path](#zoning-breakdown-path) section below.

If the user selects **Building Zoning Analysis**, continue with the Building Zoning Analysis path below.

---

# PATH A: Building Zoning Analysis

Deliverables:
1. **Per-site Word document** (.docx) — deep analytical report with full regulatory citations
2. **Excel workbook** (.xlsx) — structured compliance matrix

## Hard Rules

These rules are non-negotiable. They come from the user's professional standards:

- **Never infer, estimate, extrapolate, or fabricate** information when data is missing or uncertain
- **Never "fill in the gaps"** with typical values, assumptions, or industry norms unless explicitly told to assume
- If data does not exist, is unavailable, or cannot be verified: state **"insufficient data"** or ask a clarifying question
- It is always preferred to say **"I don't know"** rather than speculate
- Clearly separate **facts, assumptions, and interpretations** in all output
- **Highlight risks, edge cases, and data limitations** rather than smoothing them over
- Avoid vague language ("typically," "generally," "usually") unless supported by cited data
- **Cite every regulatory standard** with the specific code section number and source document

## Building Analysis Workflow Overview

```
1. Locate market folder → identify regulatory sources
   → Ask user what zoning district and overlay(s) apply
   → Ask user which input method: Proforma + Layout | Proforma only | Layout only | User input
2. Parse proforma (.xlsm) → extract building specs (skip if Layout only or User input)
3. Parse layout PDF → extract height, coverage, FAR (skip if Proforma only or User input)
4. Deep-read all regulatory sources to extract applicable standards for the user-provided zoning district
5. Online supplemental research → recent code amendments, PD/variance precedents, comparable projects
6. Run compliance analysis and determine entitlement pathway (by-right vs. PD)
7. Generate Word report (by-right compliance OR PD-forward strategy)
8. Generate Excel compliance summary
9. Verify all citations against source documents
10. Deliver files to Finished Analysis subfolder in market folder
```

## Step 1: Locate the Market Folder, Gather Inputs, and Ask for Zoning Context

### 1a. Access the Market Folder (Zoning Documents)

Zoning documents are stored in SharePoint, synced locally via OneDrive. The path follows this structure:

```
C:\Users\{USERNAME}\Subtext\Subtext - Documents\General\Markets\xxxxx. AI\Building Zoning Check\Markets\{Market Name}
```

- `{USERNAME}` — the Windows username of whoever is running this skill. Detect it from the system environment (e.g., `os.path.expanduser("~")` or the `HOME` / `USERPROFILE` environment variable).
- `{Market Name}` — ask the user which market. Examples: "Missouri (Columbia)", "Florida (Gainesville)", "North Carolina (Chapel Hill)".

**Ask the user: "What market is this project in?"** Then construct the path and mount or navigate to that folder.

Inside the market folder, you should find:

- **Municipal code documents** (.docx, .pdf) — the zoning ordinance / unified development code
- **Comprehensive plan documents** (.pdf) — future land use designations (advisory but relevant)
- **Overlay district maps or descriptions** — height overlays, historic overlays, form-based overlays

If the folder is empty or missing expected documents, tell the user what's missing.

### 1b. Collect Project Inputs (Building-Specific)

The project inputs are **not** in the market folder — they are project-specific. Ask the user which input method they're using:

**Input Method Options (ask the user):**

1. **Proforma + Layout PDF** — Both the standardized proforma (.xlsm) and testfit/massing layout PDF. This is the most complete input. Proforma is source of truth for units, beds, SF, parking. Layout is source of truth for height in feet, building coverage, impervious coverage.

2. **Proforma only** — Just the standardized proforma (.xlsm). Building height in feet and coverage percentages will be marked "insufficient data — layout PDF not provided."

3. **Layout PDF only** — Just the testfit/massing layout PDF. Extract height, coverage, FAR, and acreage from the layout summary table. Units, beds, parking, and detailed SF breakdowns will be limited to what the layout contains (note: the layout software does not have actual unit mixes, so unit/bed counts from the layout should be flagged as approximate). Skip Step 2 (proforma parsing) entirely and proceed to Step 3.

4. **Neither — user input** — No proforma or layout PDF available. Ask the user to provide the following building specs directly:
   - **Project name and address**
   - **Total units and total beds**
   - **Number of stories and building height in feet**
   - **Total gross building SF**
   - **Land area (SF or acres)**
   - **Building coverage %** (if known)
   - **Impervious coverage %** (if known)
   - **Total parking spaces provided**
   - **Commercial SF** (if any)
   - **Building type / construction type** (e.g., Type III Midrise, 5-over-2, etc.)

   For any value the user doesn't have, mark it as "insufficient data — not provided by user." Do not estimate or fill in gaps. Skip Steps 2 and 3 entirely and proceed to Step 4 with whatever the user provided.

The user will provide files directly (drag into chat, point to a file path, etc.).

**This skill analyzes one building per run.** If the user has multiple buildings, run the skill separately for each.

### 1c. Ask the User for Zoning District

The market folder contains the regulatory code but **does not specify which district applies to this particular site.** You must **ask the user directly** what zoning district(s) and overlay(s) apply.

> "What zoning district is this site currently in? Are there any overlay districts that apply (e.g., height overlay, historic overlay, form-based overlay)?"

Use the user's answer to determine which sections of the municipal code to reference. Cross-reference the district name against the documents in the market folder to locate the applicable standards.

## Step 2: Parse the Proforma

The proforma is a standardized .xlsm workbook used across all projects. The layout is consistent but **row and column positions shift between versions**. You must open the file, read the sheets, and **locate data by searching for label text — never rely on fixed cell addresses.**

Read `references/proforma-parser.md` for the complete parsing instructions, including what labels to search for, which sheets to read, column shift awareness, validation checks, and the full list of fields to extract.

### Summary of what to extract

**From the Development tab** — search for these labels and read their adjacent values:
- Total Units, Total Beds, Gross Res SF, Amenity and Leasing SF, Commercial SF, Parking SF, Total Gross SF, Total Net SF, Total FAR SF, Land SF, Land Acres

**From the Executive Summary tab** — search for these labels and read their adjacent values:
- Project Name, Address, Number of Stories, Type of Build, Total Parking Spaces, Residential Parking Spaces, Commercial SF

**Unit mix** (if available) — from the Executive Summary rent assumptions area, look for unit type labels (Studio, 1BR/1BA, 2BR/2BA, etc.) with bed counts. Flag as rent assumption data, not final program.

### Key rules

- **Search by label, not by cell address.** Scan sheets for the label text (case-insensitive). The label "Total Units" should match regardless of which row or column it's in.
- **Be aware of column shifts.** Some proforma variants shift the entire layout right by one column. If expected labels aren't found in the first pass, search adjacent columns.
- **Round appropriately.** Units, beds, and parking stalls → integers. SF and acres → keep decimals.
- **Missing data = missing data.** If a field is not found or is 0/blank, record it as not available. Do not substitute a value.

## Step 3: Parse the Layout PDF (if present)

The layout PDF is a testfit/massing document. Page 1 typically has a site plan overlay on aerial imagery with a summary data table at the bottom. The table contains columns labeled:

- **SITE**: Acreage, FAR, BLDG CVG%, IMP CVG%, DU/AC
- **MULTIFAMILY**: Units, Beds, Baths, Stalls Req.
- **PARKING**: Efficiency, Bldg Height, Average, Stalls, Ratio (Units)
- **MASTER PLAN**: Stalls, Ratio
- **EARTHWORK**: Cut, Fill, Import, Export

**Extract from the layout PDF (these are the source of truth):**

| Field | Layout Label | Zoning Use |
|---|---|---|
| Building height (ft) | "Bldg Height" under PARKING | Height compliance — **this is the only source for height in feet** |
| Building coverage % | "BLDG CVG%" under SITE | Lot coverage compliance |
| Impervious coverage % | "IMP CVG%" under SITE | Stormwater, landscaping requirements |
| FAR | "FAR" under SITE | Cross-check against proforma-derived FAR |

**Ignore from the layout PDF when a proforma is also provided (proforma is source of truth for these):**
- Units, Beds, DU/AC, Stalls Req., Parking Stalls, Parking Ratio — the layout software does not have the final unit mix

**If using Layout PDF only (no proforma):** You may use the layout's Units, Beds, and DU/AC values as the best available data, but **flag them prominently** as "approximate — from layout software, not from proforma unit mix." Do not treat them as confirmed.

If no layout PDF is present, mark building height (ft), BLDG CVG%, and IMP CVG% as "insufficient data — layout PDF not provided."

## Step 4: Deep-Read Regulatory Sources

This is the most critical step. Using the **zoning district the user told you** in Step 1, read the full municipal code document(s) to extract:

### District-Specific Standards
For the zoning district(s) the user identified, extract:
- Purpose statement (important for PD justification context)
- Dimensional standards: height (ft and stories), lot area, lot width, setbacks (front/side/rear)
- Density standards: units per acre, SF per unit, FAR limits
- Use permissions: permitted, conditional, prohibited uses
- Any special provisions or footnotes in dimensional tables

### Parking Standards
- Residential parking ratios by unit type and bedroom count
- Visitor parking requirements
- Non-residential parking ratios (if commercial component)
- Parking reductions or exemptions (transit, downtown, shared parking)
- Maximum parking caps
- Bicycle parking requirements

### Design Standards
- Facade length limits
- Bedroom caps per structure
- Building articulation requirements
- Ground floor use requirements (especially for mixed-use districts)
- Transparency/fenestration minimums

### Overlay Districts
- Height overlays (modified height limits)
- Form-based overlays (building form standards, required building lines)
- Conservation/historic overlays (design review triggers)
- Any overlay that modifies base district standards

### Neighborhood Protection / Transitions
- Step-down requirements near lower-density residential zones
- Setback increases adjacent to single-family districts
- Screening/buffering requirements

### Landscaping
- Minimum landscape area as % of site
- Street tree requirements
- Parking lot landscaping
- Buffer yard standards

### Entitlement Pathways
- By-right development standards
- Planned Development (PD) process — what it allows, what it requires, approval body
- Conditional use permits
- Variances and their standards of review
- Any form-based code provisions

**Read carefully. Extract exact numbers and exact section citations. Do not paraphrase code language when precision matters — quote it.**

## Step 5: Online Supplemental Research

After reading the user-provided documents, search online for supplemental information that may affect the analysis. The folder documents are the **primary source of truth** — online research is a **secondary check** to catch things the documents may not cover.

### What to search for

1. **Recent zoning code amendments** — Search for recent amendments or updates to the municipal zoning code that may have changed standards for the applicable district since the user's documents were created. Search "[city name] zoning code amendment [district name]" and "[city name] UDC update [current year]".

2. **Recent PD/variance approvals in the same district** — Search for other projects that received PD approval, variances, or conditional use permits in the same zoning district. These are valuable precedents. Search "[city name] planned development approval [district name]", "[city name] board of adjustment variance [district name]", and "[city name] planning commission minutes".

3. **Active or proposed code changes** — Search for any proposed text amendments, comprehensive plan updates, or overlay district changes that could affect the site. Check the city's planning department page if accessible.

4. **Comparable student housing / multifamily projects** — Search for other recent multifamily or student housing developments near the site. Useful for understanding what the jurisdiction has been approving and at what scale.

### How to use online findings

- **Code amendments**: If you find evidence that a standard has been updated more recently than the user's document, flag it clearly: "Note: Online sources suggest [standard] may have been amended. The user-provided code document [does/does not] reflect this. Recommend verifying with the municipality."
- **PD/variance precedents**: Include relevant precedents in the PD strategy section (if applicable). Note the project name, approval date, district, and what deviations were granted. These strengthen the PD case.
- **Proposed changes**: Flag as advisory only — proposed changes are not adopted law. Note them as "pending/proposed" if relevant.
- **Comparable projects**: Reference as context for what the market and jurisdiction have accepted, not as regulatory authority.

### Rules for online research

- **Do not treat online findings as equivalent to the user's code documents.** The user-provided muni code is the primary regulatory source. Online findings supplement — they don't override.
- **Clearly label every online finding** with the source URL, date accessed, and a note that it should be independently verified.
- **If online sources conflict with the user's documents**, flag the conflict explicitly. Do not silently adopt the online version.
- **If nothing relevant is found online**, say so. Do not fabricate precedents or amendments.
- **Time-bound your search.** Focus on the last 2-3 years for code amendments and comparable projects.

## Step 6: Determine Compliance Pathway Per Site

For each site, compare the building program against the extracted standards. Classify each standard as:

| Status | Meaning |
|---|---|
| **PASS** | Meets code requirement with margin |
| **PASS*** | Meets requirement but at or near the limit, or with conditions |
| **FAIL** | Does not meet code requirement — quantify the deviation |
| **VERIFY** | Cannot confirm from available data — state what's missing |
| **INFO** | Project metric with no code requirement (for reference) |
| **PD** | To be established through PD rezoning negotiation |
| **N/A** | Standard does not apply to this district/use |

### Decision: By-Right vs. PD-Forward

After running the compliance check, make a determination:

- **If all critical standards are PASS or PASS***: Frame the report as a **by-right compliance analysis**
- **If any critical standard (height, density, parking) is FAIL with >25% deviation**: Frame the report as a **PD-forward entitlement strategy document**
- **If deviations are minor (<25%)**: Note that a variance or conditional use may suffice; discuss options

The threshold is a guideline, not a hard rule — use professional judgment. A 30% parking shortfall might be addressable through shared parking agreements without PD, while a 200% height exceedance clearly requires PD. The key question: "Can this project be built under the existing zoning with minor adjustments, or does it require a fundamentally different regulatory framework?"

## Step 7: Generate Word Reports

Install the `docx` npm package if not already available. Read `references/word-report-template.md` for the complete document generation code patterns, helper functions, and formatting standards.

### By-Right Report Structure (10 sections)
1. Executive Summary — compliance overview, key findings, risk items
2. Site Identification — address, parcels, zoning, overlays, land area
3. Zoning District Standards — full dimensional table with citations
4. Height Analysis — stories and feet vs. limits, any overlays
5. Density & Use Analysis — units, beds, FAR, permitted uses
6. Parking Analysis — required vs. provided by ratio type, deficit/surplus
7. Setbacks & Siting — front/side/rear, build-to lines, RBL compliance
8. Design Standards — facade, articulation, ground floor, bedroom caps
9. Landscaping & Open Space — % requirements, buffer yards
10. Source Documentation — all documents used, dates, online vs. folder-provided

### PD-Forward Report Structure (10 sections)
1. Executive Summary — PD Entitlement Framework (deviation summary table)
2. Site Identification & Parcel Assembly (parcel-by-parcel zoning verification)
3. Base District Baseline Standards (the "from" in the PD deviation)
4. Height — PD Strategy (base limit vs. PD target vs. project, % deviation)
5. Density — PD Strategy (base limit vs. PD target, comparable PD approvals)
6. Parking — PD Negotiation (base requirement, reduction strategy, comps)
7. Setbacks, Design Standards & Landscaping (which standards carry forward)
8. PD Process & Strategy (approval body, timeline, public benefit framework)
9. Action Items (numbered matrix: item, responsible party, priority, timing)
10. Source Documentation

### Formatting Standards

Read `references/formatting-standards.md` for the exact color palette, font specifications, table styles, and helper function patterns. The key elements:

- **Color palette**: Dark blue (#1B3A5C) headers, medium blue (#2E75B6) subheadings, PD green (#E2EFDA) for PD items
- **Font**: Arial throughout, 10pt body, varying sizes for headings
- **Tables**: Light gray borders, colored status cells, consistent column widths
- **Status cells**: Color-coded backgrounds matching the status type
- **Headers/footers**: Site identifier and confidentiality notice
- **Page size**: Letter (8.5 x 11), 1-inch margins

## Step 8: Generate Excel Compliance Summary

Use Python with openpyxl. Read `references/excel-summary-template.md` for the complete code patterns.

### Workbook Structure
- **One sheet per site** named "[Site ID] – [District]" (e.g., "B2 – PD (from R-MF)")
- **One portfolio summary sheet** comparing all sites side-by-side

### Per-Site Sheet Format
| Column | Content |
|---|---|
| A | Category (Site, Density & Use, Height, Parking, Siting, etc.) |
| B | Standard / Metric |
| C | Code Requirement (with citation) |
| D | Project Value |
| E | Status (color-coded cell) |
| F | Notes / PD Negotiation Strategy |

- Row 1: Dark blue title bar (merged across all columns) with site name, address, city, date
- Row 2: Medium blue column headers
- Row 3+: Data rows with gray category column
- After data: Legend explaining status codes
- Final row: Source documentation citation

### For PD-framed sites:
- Column C header changes to: "Base District By-Right Baseline → PD Target"
- Status column uses "PD" (light green) for negotiable items
- Notes column includes PD strategy language

### Entitlements Summary Cell (Proforma Runs Only)

When the user provided a proforma as input, add an **Entitlements Summary** section below the legend and above the source row. This is a single merged cell (columns A–F) containing 1–5 bullet points summarizing only the **high-priority / major zoning items** from the analysis — the things the team would include in a deal circulation email.

**What qualifies as a major item:**
- Any standard requiring a PD deviation (height, density, parking, setbacks)
- Any outright FAIL that must be resolved
- Any critical design or entitlement condition (e.g., "setback building 5 ft on south side")
- Do NOT include routine PASS items or minor informational notes

**Format:**
- Merge columns A–F into one cell
- Header row: "Entitlements Summary" in bold, dark blue font
- Content: 1–5 concise bullet lines in a single cell, separated by newlines (`\n`)
- Each bullet should read like a short email line item (e.g., "Height – 7 stories requires PD; base district allows 3 stories (133% deviation)")
- Keep language direct and professional — no hedging, no "typically"
- The goal is copy/paste readiness for deal circulation emails

**Do NOT generate this section** when the input method is Layout only or User input — only when a proforma was provided (Proforma + Layout or Proforma only).

### Portfolio Summary Sheet
- Columns: Parameter, Site1, Site2, Site3, ...
- Rows: Zoning, Height Limit, Proposed Height, Height Status, Density Limit, Proposed Density, Density Status, Parking Required, Parking Provided, Parking Status, Entitlement Pathway
- Color-coded cells matching status

## Step 9: Citation Verification

Before delivering the final documents, verify citations:

1. For each section citation referenced in the reports, search the source document to confirm:
   - The section number exists
   - The standard value matches what you cited
   - The language is accurate

2. Flag any citations you cannot verify with a note like:
   > "Citation not independently verified from provided documents — confirm with municipal code."

3. Document whether each source was from the user's folder or from online research. If online sources were used, flag them prominently.

## Step 10: Deliver

Save all files to a **"Finished Analysis"** subfolder inside the market folder you're working in.

1. Check if a folder named `Finished Analysis` already exists inside the market folder (e.g., `.../Markets/Missouri (Columbia)/Finished Analysis/`).
2. If it does not exist, create it.
3. Save the deliverables into that folder:
   - `[ProjectName]_Zoning_Compliance_Analysis.docx` (or `_PD_Rezoning_Analysis.docx` if PD-framed)
   - `[ProjectName]_Zoning_Compliance_Summary.xlsx`
4. Provide computer:// links for each file. Summarize key findings concisely — don't restate the entire analysis.

---

# PATH B: Zoning Breakdown {#zoning-breakdown-path}

This path produces a standalone zoning rules summary for a specific district — no building metrics needed.

**The Hard Rules from Path A apply here too** — never fabricate data, cite every standard with its code section, flag uncertainties, and clearly label online findings as secondary sources.

## Zoning Breakdown Workflow

```
1. Locate market folder
2. Ask user which zoning district to break down
3. Deep-read regulatory sources for that district
4. Online supplemental research for recent amendments
5. Generate zoning breakdown document
6. Deliver to Finished Analysis subfolder in market folder
```

## ZB Step 1: Locate Market Folder

Same as Building Analysis Step 1a — access the market folder via the SharePoint-synced path:

```
C:\Users\{USERNAME}\Subtext\Subtext - Documents\General\Markets\xxxxx. AI\Building Zoning Check\Markets\{Market Name}
```

Ask the user: **"What market is this in?"**

## ZB Step 2: Ask for Zoning District

Ask the user: **"Which zoning district do you want broken down?"**

The user provides the district name (e.g., "U5", "R-MF", "M-DT"). Use this to locate the applicable sections in the municipal code documents.

## ZB Step 3: Extract District Standards

Read the municipal code documents in the market folder and extract **everything that applies to the specified district**:

### Development Intensity
- Maximum residential density (DU/AC) — by right and with bonuses
- Maximum building coverage (%)
- Maximum impervious surface coverage (%) if regulated
- FAR limits (if any)
- Minimum lot area, lot width, lot depth

### Height
- Maximum stories — by right and with bonuses
- Maximum height in feet — by right and with bonuses
- Any bonus/offset provisions that allow additional height (e.g., affordable housing offsets, open space bonuses)

### Permitted Uses
- Residential uses: single-family, multifamily, attached, accessory dwelling units, etc.
- Nonresidential uses: commercial, office, retail, mixed-use
- Special use permit uses
- Prohibited uses

### Setbacks & Building Placement
- Front, side, rear setbacks (minimums and maximums)
- Build-to lines or building placement zones (if form-based)
- Setback modifications near lower-intensity districts

### Parking
- Vehicle parking ratios by use type
- Bicycle parking requirements
- Parking location and design standards
- Any parking reductions or exemptions

### Design Standards
- Facade/frontage requirements
- Glazing/transparency minimums
- Building articulation requirements
- Ground floor use requirements
- Bedroom caps or multipliers (if applicable)

### Landscaping & Open Space
- Minimum landscape area (%)
- Street tree requirements
- Buffer yard standards
- Open space requirements

### Compatibility / Transition Standards
- Requirements triggered by adjacency to lower-intensity districts
- Step-down provisions
- Screening/buffering requirements

### Overlay Districts
- Any overlays that commonly apply to this district
- How overlays modify the base district standards

### Entitlement Pathways Available
- By-right development
- Planned Development (PD) — what it allows, process, approval body
- Conditional use / special use permits
- Variances — standards of review
- Bonus/incentive programs (affordable housing, open space, etc.)

**For every standard, include the specific code section citation.**

## ZB Step 4: Online Supplemental Research

Search online for:
- Recent amendments to this district's standards
- Any proposed code changes affecting this district
- Recent projects approved in this district (for context on what the jurisdiction is approving)

Label all online findings with source URL and date. Flag as secondary to the code documents.

## ZB Step 5: Generate Zoning Breakdown Document

Create a **Word document** (.docx) using the same formatting standards as the Building Analysis reports (read `references/word-report-template.md` and `references/formatting-standards.md`).

### Document Structure

1. **Title Page** — "Zoning District Breakdown: [District Name]", City, State, Date
2. **District Overview** — Purpose statement, where it fits in the zoning hierarchy, applicable future land use categories
3. **Development Intensity** — Density, coverage, FAR, lot standards (table format)
4. **Height Standards** — Stories and feet, by-right and bonus, offset provisions (table format)
5. **Permitted Uses** — Full use table for this district (P/S/A/blank)
6. **Setbacks & Building Placement** — All setback standards (table format)
7. **Parking Requirements** — Vehicle, bicycle, scooter ratios and design standards
8. **Design Standards** — Glazing, frontage, articulation, ground floor, bedroom caps
9. **Landscaping & Open Space** — Minimums, buffers, tree requirements
10. **Compatibility Standards** — Adjacency triggers, transition requirements
11. **Entitlement Pathways** — By-right, PD, CUP, variance, bonus programs
12. **Recent Activity** — Online research findings (code amendments, comparable projects)
13. **Source Documentation** — All documents referenced with dates

Use tables heavily — this is a reference document. Present standards as structured data, not narrative prose. For each standard, include the code section citation in the table.

## ZB Step 6: Deliver

Save to the **Finished Analysis** subfolder in the market folder (create it if it doesn't exist):
- `[District]_Zoning_Breakdown.docx`

Provide a computer:// link and a brief summary of the key development constraints.

---

## Reference Files

Read these before generating documents:

- `references/proforma-parser.md` — **Read first.** Instructions for reading the standardized proforma — what sheets to check, what labels to search for, how to handle column shifts, validation checks, and the full list of fields to extract
- `references/word-report-template.md` — Complete docx-js code patterns, helper functions, and document structure
- `references/excel-summary-template.md` — Complete openpyxl code patterns, formatting functions, and sheet structure
- `references/formatting-standards.md` — Color palette, fonts, status cell definitions, table styles
- `references/analytical-framework.md` — The full list of compliance categories, what to check, and how to evaluate each
- `references/pd-strategy-guide.md` — How to frame PD-forward analyses, deviation quantification, public benefit strategies

**Read the relevant reference files before writing any code.** The templates encode patterns that took significant iteration to get right — formatting, helper functions, cell sizing, color codes. Don't reinvent them.
