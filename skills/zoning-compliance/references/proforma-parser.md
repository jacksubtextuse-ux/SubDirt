# Proforma Parser — Instructions for Claude

## What You're Working With

The proforma is a standardized .xlsm workbook (Excel with macros). The structure is consistent across all projects, but **row positions and sometimes column positions shift between versions**. You cannot rely on hard-coded cell addresses. You must open the file, read the sheets, and locate data by searching for label text.

Since you only need to read calculated values (not run macros), open with `data_only=True, keep_vba=False` in openpyxl.

## Sheets to Read

The proforma has 20+ sheets. Focus on these three:

- **Development** — Area measures, cost breakdowns, parcel details. This is your **primary source for square footage and land data**.
- **Executive Summary** — Project summary, stories, build type, parking stalls, unit rents. This is your **primary source for building description and parking counts**.
- **Building Program** — Testfit metrics, parking breakdowns, resi metrics by construction type. Use as a **backup/cross-check source**.

## How to Find Data

Do NOT assume any field is at a specific row or column. Instead:

1. Open the sheet
2. Scan through the cells looking for the label text you need
3. When you find the label, the corresponding value is in the adjacent value column on the same row

Use **case-insensitive matching**. Try an exact match first, then fall back to partial match (e.g., searching for "Total Units" should match a cell that says "Total Units" or "Total Units (All Types)").

### Column Shift Awareness

In most proformas, the Development tab has labels in one column and values a few columns to the right. However, in some variants (notably the "RedChili" proforma family), the entire layout shifts right by one column. If you don't find expected labels in the columns where they first appear, shift your search one column to the right.

The same applies to the Building Program tab if you use it.

**Bottom line: read the sheet, find the labels, read the values. Don't assume column letters or numbers.**

## What to Extract from the Development Tab

The Development tab has a section called "FACTOR CALCULATION METRICS" (or similar heading). Within it, look for these labels and extract their corresponding values:

| Label to Search For | Field Name | What It's Used For |
|---|---|---|
| Total Units | `total_units` | Density compliance (round to integer) |
| Total Beds | `total_beds` | Parking calcs, bedroom cap triggers (round to integer) |
| Gross Res SF | `gross_res_sf` | FAR, general reference |
| Amenity and Leasing SF | `amenity_sf` | General reference |
| Commercial SF | `commercial_sf` | Use compliance, ground floor requirements |
| Parking SF | `parking_sf` | General reference |
| Total Gross SF | `total_gross_sf` | FAR calculations |
| Total Net SF | `total_net_sf` | General reference |
| Total FAR SF | `total_far_sf` | FAR (may be 0 or blank in some versions) |
| Land SF | `land_sf` | Density, coverage, landscaping calcs |
| Land Acres | `land_acres` | Density calculations |

**Notes:**
- Numeric values from formulas often appear as floats (e.g., 277.04 units). Round units, beds, and parking stalls to integers. Keep decimals for SF and acres.
- If a field is not found or is 0/blank, record it as missing — do not substitute a value.

## What to Extract from the Executive Summary Tab

The Executive Summary has a "PROJECT SUMMARY" section (or similar). Look for these labels and extract their values:

| Label to Search For | Field Name | What It's Used For |
|---|---|---|
| Project Name | `project_name` | Report labeling |
| Address | `address` | Site identification |
| Number of Stories | `stories` | Height compliance (may read as "6 Stories" or "5-Over-2") |
| Type of Build | `build_type` | Construction type context (e.g., "Type III Midrise / 6 over 1 Podium") |
| Total Parking Spaces | `total_parking` | Parking compliance (round to integer) |
| Residential Parking Spaces | `resi_parking` | Parking compliance (round to integer) |
| Commercial SF | `commercial_sf_check` | Cross-check against Development tab value |

### Unit Mix (from Executive Summary)

The Executive Summary also has a rent assumptions area. It contains unit type labels like "Studio", "1BR/1BA", "2BR/2BA", "3BR/3BA", "4BR/2BA", "4BR/4BA", "5BR/5BA" with corresponding bed counts.

Scan through the rows in the rent assumption area and look for labels matching unit type patterns (Studio, or XBR/XBA format). The bed count for each unit type will be in the adjacent column.

**Important caveat:** These bed counts come from the proforma's rent model. They may not represent the final program unit mix. If you use this data, flag it as "proforma rent assumption unit mix, not final program."

If you can't find unit mix data, that's fine — record it as not available.

## Building Program Tab (Backup Only)

If the Building Program tab exists, you can use it to cross-check values from the Development tab. Look for:
- Total Units
- Total Beds
- Acres / Site Square Footage
- FAR

If there's a discrepancy between the Development tab and Building Program tab (more than 1 unit difference), flag it in your output.

## Calculated Fields

After extraction, compute:
- **Calculated FAR** = Total Gross SF ÷ Land SF (if both values are available)
- **Calculated DU/AC** = Total Units ÷ Land Acres (if both values are available)

## Validation Checks

Run these sanity checks on your extracted data:

1. **Land area consistency**: Land Acres × 43,560 should approximately equal Land SF. If the difference exceeds 500 SF, flag it.
2. **Gross SF logic**: Total Gross SF should be ≥ Gross Res SF. If not, flag it.
3. **Commercial SF cross-check**: Commercial SF from the Development tab should match Commercial SF from the Executive Summary. If they differ, flag it.
4. **Unit count cross-check**: If Building Program tab data is available, units should be within 1 of the Development tab count. If not, flag it.

## Layout PDF Parsing

Layout PDF parsing instructions are in **SKILL.md Step 3**. Refer to that section for what to extract (height, coverage, FAR), what to ignore (units, beds, parking when proforma is available), and how to handle the layout-only input path.

## What You Should Have After Parsing

After reading the proforma (and layout PDF if available), you should have:

**From the proforma:**
- total_units, total_beds, gross_res_sf, amenity_sf, commercial_sf, parking_sf, total_gross_sf, total_net_sf, land_sf, land_acres
- project_name, address, stories, build_type, total_parking, resi_parking
- unit_mix (if available, flagged as rent assumption data)
- calculated_far, calculated_du_ac

**From the layout PDF (if provided):**
- bldg_height_ft, bldg_coverage_pct, imp_coverage_pct, layout_far

**Missing data handling:**
- Any field that could not be extracted: mark as "insufficient data" with a note on which sheet/source was checked
- Never silently skip a failed extraction — always surface what's missing and from where
