# Excel Summary Workbook Template (openpyxl)

## Setup

```bash
pip install openpyxl --break-system-packages
```

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
```

## Style Definitions

```python
# ─── Colors ───
DARK_BLUE_FILL = PatternFill(start_color="1F3864", end_color="1F3864", fill_type="solid")
MED_BLUE_FILL  = PatternFill(start_color="2E5090", end_color="2E5090", fill_type="solid")
GRAY_FILL      = PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid")
WHITE_FILL     = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
PASS_FILL      = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
FAIL_FILL      = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
VERIFY_FILL    = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")
INFO_FILL      = PatternFill(start_color="BDD7EE", end_color="BDD7EE", fill_type="solid")
PD_FILL        = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")

# ─── Fonts ───
WHITE_FONT       = Font(name="Arial", size=10, bold=True, color="FFFFFF")
WHITE_FONT_TITLE = Font(name="Arial", size=13, bold=True, color="FFFFFF")
HEADER_FONT      = Font(name="Arial", size=10, bold=True, color="FFFFFF")
CAT_FONT         = Font(name="Arial", size=9, bold=True, color="000000")
DATA_FONT        = Font(name="Arial", size=9, color="333333")
BOLD_DATA        = Font(name="Arial", size=9, bold=True, color="333333")
STATUS_FONT      = Font(name="Arial", size=9, bold=True)
NOTE_FONT        = Font(name="Arial", size=9, color="333333")
SOURCE_FONT      = Font(name="Arial", size=8, color="595959")

# ─── Borders ───
thin_border = Border(
    left=Side(style='thin', color='CCCCCC'),
    right=Side(style='thin', color='CCCCCC'),
    top=Side(style='thin', color='CCCCCC'),
    bottom=Side(style='thin', color='CCCCCC')
)
```

## Helper Functions

```python
def set_cell(ws, row, col, value, font=DATA_FONT, fill=WHITE_FILL, alignment=None, border=thin_border):
    """Write a value to a cell with full formatting."""
    cell = ws.cell(row=row, column=col, value=value)
    cell.font = font
    cell.fill = fill
    cell.border = border
    cell.alignment = alignment or Alignment(vertical='center', wrap_text=True)
    return cell

def status_cell(ws, row, col, status):
    """Write a color-coded status cell."""
    fills = {
        "PASS": PASS_FILL, "FAIL": FAIL_FILL, "VERIFY": VERIFY_FILL,
        "INFO": INFO_FILL, "PASS*": VERIFY_FILL, "PD": PD_FILL,
        "N/A": PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
    }
    fill = fills.get(status, VERIFY_FILL)
    set_cell(ws, row, col, status, font=STATUS_FONT, fill=fill,
             alignment=Alignment(horizontal='center', vertical='center'))

def write_header_row(ws, row, cols):
    """Write column header row with blue background."""
    for i, text in enumerate(cols, 1):
        set_cell(ws, row, i, text, font=HEADER_FONT, fill=MED_BLUE_FILL,
                 alignment=Alignment(horizontal='left', vertical='center', wrap_text=True))

def write_data_row(ws, row, category, standard, requirement, project_val, status, notes=""):
    """Write a standard 6-column data row."""
    set_cell(ws, row, 1, category, font=CAT_FONT, fill=GRAY_FILL)
    set_cell(ws, row, 2, standard, font=DATA_FONT)
    set_cell(ws, row, 3, requirement, font=DATA_FONT)
    set_cell(ws, row, 4, project_val, font=DATA_FONT)
    status_cell(ws, row, 5, status)
    set_cell(ws, row, 6, notes, font=NOTE_FONT)

def setup_sheet(ws, title_text, col_widths=None):
    """Set column widths and create title row."""
    widths = col_widths or [18, 28, 38, 28, 10, 48]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    # Title row — dark blue bar merged across all columns
    num_cols = len(widths)
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=num_cols)
    c = ws.cell(row=1, column=1, value=title_text)
    c.font = WHITE_FONT_TITLE
    c.fill = DARK_BLUE_FILL
    c.alignment = Alignment(horizontal='left', vertical='center')
    for col in range(2, num_cols + 1):
        ws.cell(row=1, column=col).fill = DARK_BLUE_FILL

def write_legend(ws, start_row):
    """Write status code legend below data rows."""
    r = start_row + 1
    set_cell(ws, r, 1, "Legend", font=Font(name="Arial", size=9, bold=True))
    r += 1
    items = [
        ("PASS", PASS_FILL, "Meets code requirement"),
        ("FAIL", FAIL_FILL, "Does not meet code requirement"),
        ("PASS*", VERIFY_FILL, "Passes with conditions (e.g., PD approval, design modification)"),
        ("VERIFY", VERIFY_FILL, "Cannot confirm from available data — requires site plan or City verification"),
        ("INFO", INFO_FILL, "Project metric — no code requirement applies"),
        ("PD", PD_FILL, "To be established through PD rezoning negotiation"),
    ]
    for label, fill, desc in items:
        set_cell(ws, r, 1, label, font=STATUS_FONT, fill=fill,
                 alignment=Alignment(horizontal='center', vertical='center'))
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=6)
        set_cell(ws, r, 2, desc, font=NOTE_FONT)
        r += 1
    return r

def write_source_row(ws, row, source_text):
    """Write the source citation row at the bottom of a sheet."""
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=6)
    set_cell(ws, row, 1, source_text, font=SOURCE_FONT, fill=PatternFill())
```

## Per-Site Sheet Pattern

```python
# Create sheet
ws = wb.create_sheet("[SiteID] – [District]")

# Setup with title
setup_sheet(ws, "[District] Zoning Compliance  |  Site [ID] – [Address]  |  [City], [State]  |  [Date]")

# Column headers (row 2)
# For by-right sites:
write_header_row(ws, 2, ["Category", "Standard / Metric", "Code Requirement ([District])", "Project Value", "Status", "Notes"])

# For PD sites:
write_header_row(ws, 2, ["Category", "Standard / Metric", "[Base District] By-Right Baseline → PD Target", "Project Value", "Status", "Notes / PD Negotiation Strategy"])

# Data rows (starting row 3)
rows = [
    # (category, standard, requirement, project_value, status, notes)
    ("Site", "Site Area", "No minimum in [District]", "XX,XXX SF (X.XX ac)", "PASS", ""),
    ("Site", "Zoning District", "Current: [District]", "[District] / [Overlay]", "PASS", "Citation"),
    # ... more rows organized by category
]

for i, (cat, std, req, val, stat, note) in enumerate(rows, 3):
    write_data_row(ws, i, cat, std, req, val, stat, note)

# Legend and source
r = 3 + len(rows)
r = write_legend(ws, r)
r += 1
write_source_row(ws, r, "Sources: [list all documents with dates]. [Online/folder statement].")
```

## Portfolio Summary Sheet Pattern

```python
ws_sum = wb.create_sheet("Portfolio Summary")
setup_sheet(ws_sum, "Portfolio Zoning Summary  |  [Market]  |  [Date]",
            col_widths=[24] + [22] * num_sites)  # Adjust for number of sites

# Headers
write_header_row(ws_sum, 2, ["Parameter"] + site_names)

# Data rows — each parameter compared across sites
summary_rows = [
    ("Zoning District", site1_zoning, site2_zoning, ...),
    ("Overlay", site1_overlay, site2_overlay, ...),
    ("Height Limit", site1_limit, site2_limit, ...),
    ("Proposed Height", site1_proposed, site2_proposed, ...),
    ("Height Status", "PASS", "PD", ...),  # color-coded
    # ... more parameters
]

# For status rows, use status_cell() for color coding
# For data rows, use set_cell() with appropriate fonts
```

## Entitlements Summary Cell (Proforma Runs Only)

Add this section below the legend and above the source row **only when a proforma was provided**.

```python
def write_entitlements_summary(ws, start_row, bullets):
    """Write 1-5 bullet entitlements summary in a single merged cell.
    
    Args:
        ws: worksheet
        start_row: first available row after legend
        bullets: list of 1-5 short strings (no bullet chars — they're added here)
    """
    r = start_row + 1  # blank spacer row
    r += 1
    # Header row
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
    set_cell(ws, r, 1, "Entitlements Summary",
             font=Font(name="Arial", size=11, bold=True, color="1F3864"),
             fill=WHITE_FILL,
             alignment=Alignment(horizontal='left', vertical='center'))
    r += 1
    # Content cell — all bullets in one merged cell, newline-separated
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
    bullet_text = "\n".join(f"• {b}" for b in bullets)
    cell = set_cell(ws, r, 1, bullet_text, font=DATA_FONT, fill=WHITE_FILL,
                    alignment=Alignment(horizontal='left', vertical='top', wrap_text=True))
    ws.row_dimensions[r].height = max(30, 16 * len(bullets))  # auto-ish height
    r += 1
    return r

# Usage:
# entitlement_bullets = [
#     "Height – 7 stories requires PD; base district allows 3 stories (133% deviation)",
#     "Density – 222 DU/AC proposed vs. 43 DU/AC max (416% over); PD required",
#     "Parking – 0.35/bed provided vs. 0.50/bed required (30% deficit); negotiate reduction",
# ]
# r = write_entitlements_summary(ws, legend_end_row, entitlement_bullets)
# write_source_row(ws, r, "Sources: ...")
```

## Saving the Workbook

```python
output_path = "[workspace_folder]/Zoning_Compliance_Summary_All_Sites.xlsx"
wb.save(output_path)
print(f"Workbook saved to {output_path}")
```

## Data Row Categories (Standard Order)

Organize rows in this consistent order across all sheets:

1. **Site** — Site area, zoning district, overlay, comprehensive plan, parcel assembly
2. **Density & Use** — Density, total units, total beds, unit mix, FAR, use, ground floor use, bedroom cap
3. **Height** — Stories, feet, overlay-modified limit, bonus height, minimum height, ground floor height
4. **Parking** — Residential ratio, visitor parking, non-residential, maximum cap, bicycle, reductions
5. **Siting** — Front setback, side setback, rear setback, build-to line, RBL, footprint
6. **Design** — Facade length, articulation, transparency, material standards
7. **Landscaping** — Landscape area %, open space per unit, street trees, buffer yards
8. **Transitions** — Height step-down, setback increase, screening
9. **Unit Metrics** — Total beds, beds/unit, commercial SF, total gross SF, construction type (all INFO status)
