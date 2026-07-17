# Formatting Standards

## Color Palette

### Word Documents (docx-js hex values, no # prefix)

```javascript
// Primary palette
const DARK_BLUE = "1B3A5C";   // Section headings, table headers
const MED_BLUE = "2E75B6";    // Subheadings, accents
const LIGHT_BLUE = "D5E8F0";  // Highlight backgrounds

// Status colors
const GREEN = "4CAF50";       // Compliant status text
const YELLOW = "FFC107";      // Verify/warning status
const RED = "F44336";         // Non-compliant, confidentiality notice

// Neutral
const LIGHT_GRAY = "F5F5F5";  // Baseline/reference cells, alternating rows
const WHITE = "FFFFFF";        // Default cell background

// PD-specific
const PD_GREEN = "E2EFDA";    // PD negotiation cell background
const PD_DARK = "375623";     // PD negotiation text color
```

### Excel Documents (openpyxl hex values)

```python
DARK_BLUE_FILL = PatternFill(start_color="1F3864", end_color="1F3864", fill_type="solid")  # Title bar
MED_BLUE_FILL = PatternFill(start_color="2E5090", end_color="2E5090", fill_type="solid")   # Column headers
GRAY_FILL = PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid")       # Category column
WHITE_FILL = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
PASS_FILL = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")       # Green
FAIL_FILL = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")       # Red
VERIFY_FILL = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")     # Yellow
INFO_FILL = PatternFill(start_color="BDD7EE", end_color="BDD7EE", fill_type="solid")       # Blue
PD_FILL = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")         # Light green
```

## Fonts

### Word Documents
- **Body text**: Arial, 10pt (size: 20 in half-points), color #333333
- **Section headings (H1)**: Arial, 14pt (size: 28), bold, color DARK_BLUE
- **Subheadings (H2)**: Arial, 12pt (size: 24), bold, color MED_BLUE
- **Table header text**: Arial, 10pt, bold, white on DARK_BLUE background
- **Table body text**: Arial, 10pt, color #333333
- **Status cell text**: Arial, 9pt (size: 18), bold, color matches status type
- **Bullet items**: Arial, 10pt
- **Header/footer**: Arial, 8pt (size: 16), color MED_BLUE or #999999

### Excel Documents
```python
WHITE_FONT = Font(name="Arial", size=10, bold=True, color="FFFFFF")        # On dark backgrounds
WHITE_FONT_TITLE = Font(name="Arial", size=13, bold=True, color="FFFFFF")  # Title bar
HEADER_FONT = Font(name="Arial", size=10, bold=True, color="FFFFFF")       # Column headers
CAT_FONT = Font(name="Arial", size=9, bold=True, color="000000")          # Category column
DATA_FONT = Font(name="Arial", size=9, color="333333")                    # Data cells
BOLD_DATA = Font(name="Arial", size=9, bold=True, color="333333")         # Emphasized data
STATUS_FONT = Font(name="Arial", size=9, bold=True)                       # Status cells (color varies)
NOTE_FONT = Font(name="Arial", size=9, color="333333")                    # Notes column
SOURCE_FONT = Font(name="Arial", size=8, color="595959")                  # Source citation row
```

## Status Cell Definitions

| Status | Background | Text Color | Meaning |
|---|---|---|---|
| PASS | Green (#C6EFCE / #E8F5E9) | Green (#4CAF50) | Meets code requirement |
| PASS* | Yellow (#FFEB9C / #FFF3E0) | Dark Orange (#E65100) | Passes with conditions |
| FAIL | Red (#FFC7CE) | Red (#F44336 / #B71C1C) | Does not meet requirement |
| VERIFY | Yellow (#FFEB9C / #FFF3E0) | Dark Orange (#E65100) | Cannot confirm from data |
| INFO | Blue (#BDD7EE) | Blue/dark gray | Reference metric, no requirement |
| PD | Light Green (#E2EFDA) | Dark Green (#375623) | PD negotiation item |
| N/A | Light Gray (#F2F2F2) | Gray (#666666) | Not applicable |
| BASELINE | Light Gray (#F5F5F5) | Gray (#666666) | Base district reference value |
| COMPLIANT | Green (#E8F5E9) | Green (#4CAF50) | No PD deviation needed |

## Table Styles

### Word Document Tables
```javascript
// Border style
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };

// Cell margins (in twips)
const cellMargins = { top: 60, bottom: 60, left: 100, right: 100 };

// Table width: 10,200 DXA (full width within 1-inch margins on letter paper)
// Column widths vary by table type — see templates
```

### Excel Sheets
```python
thin_border = Border(
    left=Side(style='thin', color='CCCCCC'),
    right=Side(style='thin', color='CCCCCC'),
    top=Side(style='thin', color='CCCCCC'),
    bottom=Side(style='thin', color='CCCCCC')
)

# Standard column widths for compliance sheets
col_widths = [18, 28, 38, 28, 10, 48]  # Category, Standard, Requirement, Value, Status, Notes
```

## Page Layout (Word)
- **Paper size**: Letter (8.5 x 11) — width: 12240, height: 15840 (in twips)
- **Margins**: 1 inch all sides — top: 1200, bottom: 1200, left: 1200, right: 1200
- **Line spacing**: 1.15 (line: 276)
- **Paragraph spacing**: varies by element (see helper functions)

## Legend Format (Excel)

Every per-site sheet should end with a legend explaining the status codes, followed by a source citation row. The legend is placed 1 blank row after the last data row.

```python
def write_legend(ws, start_row):
    # Row 1: blank spacer
    # Row 2: "Legend" header
    # Row 3+: status label (col A, colored background) + description (cols B-F merged)
    items = [
        ("PASS", PASS_FILL, "Meets code requirement"),
        ("FAIL", FAIL_FILL, "Does not meet code requirement"),
        ("PASS*", VERIFY_FILL, "Passes with conditions"),
        ("VERIFY", VERIFY_FILL, "Cannot confirm from available data"),
        ("INFO", INFO_FILL, "Project metric — no code requirement applies"),
        ("PD", PD_FILL, "To be established through PD rezoning negotiation"),
    ]
```
