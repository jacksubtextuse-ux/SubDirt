#!/usr/bin/env python3
"""
build_fee_workbook.py — Render a development fee schedule into a branded Subtext Excel workbook.

USAGE
    python build_fee_workbook.py <spec.json> <output.xlsx>

WHY A SCRIPT
    The formatting is identical every run; only the data changes. Generating the workbook from a JSON
    spec keeps each invocation focused on the research (the hard part) instead of re-deriving openpyxl
    styling. The output is a *static research record* — a fee schedule analysts read and extend in
    their own models — so amounts and the mandatory subtotal are written as computed values, not live
    formulas. That makes the file display correctly everywhere immediately and carry zero formula-error
    risk; no recalc step is required.

JSON SPEC SCHEMA
    All sections are optional except `project`. Empty sections render a "none identified" note so the
    reader can see the section was considered, not skipped.

    {
      "project": {
        "name":     "Project name or working name",        # optional
        "address":  "123 Main St, City, ST 00000",          # REQUIRED
        "type":     "Ground-up student housing",            # optional, defaults to this
        "units":    300,        # optional ints/floats — shown on cover for context only
        "beds":     900,
        "gsf":      350000,
        "prepared": "2026-06-17"  # optional ISO date; defaults to today
      },

      # STEP 0 — each charging/permitting authority and what it may levy
      "jurisdiction_stack": [
        {"entity": "City of X", "authority_type": "Home-rule municipality",
         "fees_allowed": "Permitting, plan review, city impact fees, inclusionary in-lieu"}
      ],

      # STEP 1 — geographic layers that affect fees
      "fee_layers": [
        {"layer": "Transportation impact-fee District 2", "authority": "County",
         "fee_power": "Road/transportation impact fee", "city_supersedes": "No",
         "county_applies": "Yes", "notes": "Citywide county fee collected at permit"}
      ],

      # STEP 3 — the master table; ONE functional charge per row
      "master_fees": [
        {
          "fee_name":      "Building permit fee (a.k.a. construction permit)",  # include aliases
          "authority":     "City of X Building Dept.",
          "level":         "City",          # City / County / State / Utility / School / Special District / Regional
          "supremacy":     "City charges; county building dept. has no jurisdiction intra-city per Charter §4.2",
          "applies":       "Y",             # Y / N / Conditional  (drives row color)
          "applies_reason":"Required for all new construction",
          "basis":         "Valuation table (ICC-derived)",
          "rate":          "$X per $1,000 valuation, see Table 3-A",  # or "Not published — contact agency"
          "amount_value":  None,            # optional float: extended dollars, feeds the subtotal
          "timing":        "At permit issuance",
          "mandatory":     "Mandatory",     # Mandatory / Conditional
          "exemptions":    "None",
          "citation":      "Master Fee Schedule Res. 2025-14, Table 3-A",
          "source_url":    "https://city.gov/fees"
        }
      ],

      # STEP 4 — non-line-item cost drivers
      "cost_triggers": [
        {"trigger": "Traffic impact study", "detail": "Required if >100 PM peak trips; ~$25-40k third-party"}
      ],

      # STEP 5 — certification
      "completeness": {
        "checklist": [
          {"item": "City fees checked",  "status": "Yes", "note": ""},
          {"item": "County fees checked","status": "Yes", "note": ""}
        ],
        "uncertainties": [
          "Sewer capacity fee rate not published online — confirm with X Water Authority (555-1234)"
        ]
      }
    }
"""

import json
import sys
from datetime import date

try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.comments import Comment
    from openpyxl.utils import get_column_letter
except ImportError:
    sys.exit("openpyxl is required. Install it with:  pip install openpyxl --break-system-packages")

# ─── Subtext brand palette (swap these six lines to re-skin the whole workbook) ───
EVEREST_GREEN = "16352E"   # primary — title bars, column headers
BIRCH         = "A95818"   # accent — section labels, conditional tint base
BEIGE         = "F7F1E3"   # neutral — alternating rows, category fills
LIME          = "C1D100"   # highlight — subtotal / emphasis
# Derived tints for the applies-to-project status column
APPLIES_Y     = "E4ECD4"   # light lime — applies
APPLIES_N     = "ECECEC"   # light gray — does not apply
APPLIES_COND  = "F2E2CE"   # light birch — conditional
WHITE         = "FFFFFF"
INK           = "2B2B2B"   # body text
MUTED         = "595959"   # source / footnote text

def fill(hex_):
    return PatternFill(start_color=hex_, end_color=hex_, fill_type="solid")

TITLE_FONT  = Font(name="Arial", size=14, bold=True, color=WHITE)
HEADER_FONT = Font(name="Arial", size=10, bold=True, color=WHITE)
LABEL_FONT  = Font(name="Arial", size=10, bold=True, color=WHITE)      # birch section labels
CAT_FONT    = Font(name="Arial", size=9,  bold=True, color=INK)
DATA_FONT   = Font(name="Arial", size=9,  color=INK)
BOLD_DATA   = Font(name="Arial", size=9,  bold=True, color=INK)
LINK_FONT   = Font(name="Arial", size=9,  color="1155CC", underline="single")
SOURCE_FONT = Font(name="Arial", size=8,  color=MUTED)
SUBTOTAL_FONT = Font(name="Arial", size=10, bold=True, color=EVEREST_GREEN)

THIN = Side(style="thin", color="CCCCCC")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP_TOP = Alignment(vertical="top", wrap_text=True)
WRAP_MID = Alignment(vertical="center", wrap_text=True)
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)

MONEY_FMT = '$#,##0;($#,##0);"—"'


def cell(ws, r, c, value, font=DATA_FONT, fillc=None, align=WRAP_TOP, border=BORDER, num_fmt=None):
    cl = ws.cell(row=r, column=c, value=value)
    cl.font = font
    if fillc:
        cl.fill = fill(fillc)
    cl.alignment = align
    cl.border = border
    if num_fmt:
        cl.number_format = num_fmt
    return cl


def title_bar(ws, ncols, text):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=ncols)
    c = ws.cell(row=1, column=1, value=text)
    c.font = TITLE_FONT
    c.fill = fill(EVEREST_GREEN)
    c.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[1].height = 26
    for col in range(2, ncols + 1):
        ws.cell(row=1, column=col).fill = fill(EVEREST_GREEN)


def header_row(ws, r, headers):
    for i, h in enumerate(headers, 1):
        c = cell(ws, r, i, h, font=HEADER_FONT, fillc=EVEREST_GREEN,
                 align=Alignment(horizontal="left", vertical="center", wrap_text=True))
    ws.row_dimensions[r].height = 30


def widths(ws, ws_widths):
    for i, w in enumerate(ws_widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w


def note_row(ws, r, ncols, text):
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=ncols)
    cell(ws, r, 1, text, font=Font(name="Arial", size=9, italic=True, color=MUTED), align=WRAP_MID)


def applies_fillcolor(applies):
    a = (applies or "").strip().lower()
    if a.startswith("y"):
        return APPLIES_Y
    if a.startswith("n"):
        return APPLIES_N
    if a.startswith("c"):
        return APPLIES_COND
    return None


# ─────────────────────────── Sheets ───────────────────────────

def build_cover(wb, spec):
    p = spec.get("project", {})
    ws = wb.active
    ws.title = "Cover"
    widths(ws, [26, 80])
    title_bar(ws, 2, "Development Fee Schedule")
    rows = [
        ("Project", p.get("name", "—")),
        ("Address", p.get("address", "—")),
        ("Project type", p.get("type", "Ground-up student housing")),
        ("Prepared", p.get("prepared") or date.today().isoformat()),
    ]
    for label in ("units", "beds", "gsf"):
        if p.get(label) is not None:
            pretty = {"units": "Units", "beds": "Beds", "gsf": "Gross sq ft"}[label]
            rows.append((pretty, f"{p[label]:,}"))
    r = 3
    for label, val in rows:
        cell(ws, r, 1, label, font=CAT_FONT, fillc=BEIGE)
        cell(ws, r, 2, val, font=DATA_FONT, align=WRAP_MID)
        r += 1
    r += 1
    cell(ws, r, 1, "Source discipline", font=LABEL_FONT, fillc=BIRCH)
    cell(ws, r, 2, "Every line is verified to an official primary source (adopted ordinance, fee "
                   "resolution, rate sheet, or impact-fee study) and cited. Unverifiable amounts are "
                   "marked \u201cNot published \u2014 contact agency\u201d rather than estimated. No "
                   "figure on this schedule is approximated or carried from memory.",
         font=DATA_FONT, fillc=BIRCH if False else None, align=WRAP_TOP)
    ws.row_dimensions[r].height = 60
    r += 1
    cell(ws, r, 1, "Confidential", font=SOURCE_FONT)
    cell(ws, r, 2, "Prepared for internal underwriting use. Confirm open items before relying at risk.",
         font=SOURCE_FONT, align=WRAP_MID)
    ws.sheet_view.showGridLines = False


def build_jurisdiction(wb, spec):
    ws = wb.create_sheet("Jurisdiction Stack")
    cols = ["Entity / Authority", "Legal Authority Type", "Fees Legally Allowed to Impose"]
    widths(ws, [30, 28, 70])
    title_bar(ws, len(cols), "Step 0 \u2014 Jurisdiction Stack")
    header_row(ws, 2, cols)
    data = spec.get("jurisdiction_stack", [])
    if not data:
        note_row(ws, 3, len(cols), "No jurisdiction stack provided in spec.")
    r = 3
    for i, e in enumerate(data):
        fillc = BEIGE if i % 2 else None
        cell(ws, r, 1, e.get("entity", ""), font=CAT_FONT, fillc=fillc or BEIGE)
        cell(ws, r, 2, e.get("authority_type", ""), fillc=fillc)
        cell(ws, r, 3, e.get("fees_allowed", ""), fillc=fillc)
        r += 1
    ws.freeze_panes = "A3"
    ws.sheet_view.showGridLines = False


def build_layers(wb, spec):
    ws = wb.create_sheet("Fee Layers")
    cols = ["Geographic Layer", "Governing Authority", "Fee Power Type",
            "City Supersedes?", "County Still Applies?", "Notes"]
    widths(ws, [30, 24, 26, 16, 18, 44])
    title_bar(ws, len(cols), "Step 1 \u2014 Geographic Fee Layers")
    header_row(ws, 2, cols)
    data = spec.get("fee_layers", [])
    if not data:
        note_row(ws, 3, len(cols), "No fee layers provided in spec.")
    r = 3
    for i, e in enumerate(data):
        fillc = BEIGE if i % 2 else None
        cell(ws, r, 1, e.get("layer", ""), font=CAT_FONT, fillc=fillc or BEIGE)
        cell(ws, r, 2, e.get("authority", ""), fillc=fillc)
        cell(ws, r, 3, e.get("fee_power", ""), fillc=fillc)
        cell(ws, r, 4, e.get("city_supersedes", ""), fillc=fillc, align=CENTER)
        cell(ws, r, 5, e.get("county_applies", ""), fillc=fillc, align=CENTER)
        cell(ws, r, 6, e.get("notes", ""), fillc=fillc)
        r += 1
    ws.freeze_panes = "A3"
    ws.sheet_view.showGridLines = False


MASTER_HEADERS = [
    "Fee Name (incl. aliases)", "Charging Authority", "Jurisdiction Level",
    "Supremacy Analysis", "Applies to Project?", "Calculation Basis",
    "Rate / Amount", "Extended ($)", "Timing", "Mandatory / Conditional",
    "Exemptions / Reductions", "Citation", "Source",
]
MASTER_WIDTHS = [30, 22, 14, 34, 14, 22, 22, 14, 16, 16, 26, 28, 30]


def build_master(wb, spec):
    ws = wb.create_sheet("Master Fee Schedule")
    widths(ws, MASTER_WIDTHS)
    title_bar(ws, len(MASTER_HEADERS), "Step 3 \u2014 Master Fee Schedule  (one functional charge per row)")
    header_row(ws, 2, MASTER_HEADERS)
    fees = spec.get("master_fees", [])
    if not fees:
        note_row(ws, 3, len(MASTER_HEADERS), "No fee rows provided in spec.")
    r = 3
    subtotal = 0.0
    subtotal_has = False
    for i, f in enumerate(fees):
        zebra = BEIGE if i % 2 else None
        cell(ws, r, 1, f.get("fee_name", ""), font=CAT_FONT, fillc=zebra or BEIGE)
        cell(ws, r, 2, f.get("authority", ""), fillc=zebra)
        cell(ws, r, 3, f.get("level", ""), fillc=zebra, align=CENTER)
        cell(ws, r, 4, f.get("supremacy", ""), fillc=zebra)
        # applies column — color coded, reason appended
        applies = f.get("applies", "")
        reason = f.get("applies_reason", "")
        applies_text = applies if not reason else f"{applies} \u2014 {reason}"
        cell(ws, r, 5, applies_text, fillc=applies_fillcolor(applies), align=WRAP_TOP)
        cell(ws, r, 6, f.get("basis", ""), fillc=zebra)
        cell(ws, r, 7, f.get("rate", ""), fillc=zebra)
        # extended amount
        amt = f.get("amount_value")
        if isinstance(amt, (int, float)):
            cell(ws, r, 8, float(amt), fillc=zebra, align=Alignment(horizontal="right", vertical="top"),
                 num_fmt=MONEY_FMT)
            if str(f.get("mandatory", "")).strip().lower().startswith("mand") and \
               (applies or "").strip().lower().startswith("y"):
                subtotal += float(amt)
                subtotal_has = True
        else:
            cell(ws, r, 8, "", fillc=zebra)
        cell(ws, r, 9, f.get("timing", ""), fillc=zebra)
        cell(ws, r, 10, f.get("mandatory", ""), fillc=zebra, align=CENTER)
        cell(ws, r, 11, f.get("exemptions", ""), fillc=zebra)
        cell(ws, r, 12, f.get("citation", ""), fillc=zebra)
        url = f.get("source_url", "")
        sc = cell(ws, r, 13, url or "", font=LINK_FONT if url else DATA_FONT, fillc=zebra)
        if url:
            sc.hyperlink = url
        r += 1

    # subtotal row (computed value, documented) — only if we had numeric mandatory amounts
    if subtotal_has:
        r += 0
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=7)
        lab = cell(ws, r, 1,
                   "Subtotal \u2014 verified mandatory fees with computed amounts "
                   "(excludes conditional and \u201cnot published\u201d items)",
                   font=SUBTOTAL_FONT, fillc=LIME, align=Alignment(horizontal="right", vertical="center"))
        for col in range(2, 8):
            ws.cell(row=r, column=col).fill = fill(LIME)
        sc = cell(ws, r, 8, subtotal, font=SUBTOTAL_FONT, fillc=LIME,
                  align=Alignment(horizontal="right", vertical="center"), num_fmt=MONEY_FMT)
        sc.comment = Comment("Computed sum of Extended ($) over rows flagged Mandatory and Applies=Y. "
                             "Static research value, not a live formula.", "student-housing-dev-fees")
        for col in range(9, len(MASTER_HEADERS) + 1):
            ws.cell(row=r, column=col).fill = fill(LIME)

    ws.freeze_panes = "A3"
    last_col = get_column_letter(len(MASTER_HEADERS))
    ws.auto_filter.ref = f"A2:{last_col}2"
    ws.sheet_view.showGridLines = False


def build_triggers(wb, spec):
    ws = wb.create_sheet("Cost Triggers")
    cols = ["Cost Trigger", "Detail / Threshold / Estimated Magnitude"]
    widths(ws, [34, 86])
    title_bar(ws, len(cols), "Step 4 \u2014 Additional Cost Triggers")
    header_row(ws, 2, cols)
    data = spec.get("cost_triggers", [])
    if not data:
        note_row(ws, 3, len(cols), "No additional cost triggers identified.")
    r = 3
    for i, e in enumerate(data):
        fillc = BEIGE if i % 2 else None
        cell(ws, r, 1, e.get("trigger", ""), font=CAT_FONT, fillc=fillc or BEIGE)
        cell(ws, r, 2, e.get("detail", ""), fillc=fillc)
        r += 1
    ws.freeze_panes = "A3"
    ws.sheet_view.showGridLines = False


def build_completeness(wb, spec):
    ws = wb.create_sheet("Completeness")
    widths(ws, [40, 14, 70])
    title_bar(ws, 3, "Step 5 \u2014 Completeness Certification")
    comp = spec.get("completeness", {})
    checklist = comp.get("checklist", [])
    uncertainties = comp.get("uncertainties", [])

    cell(ws, 2, 1, "Checklist Item", font=HEADER_FONT, fillc=EVEREST_GREEN)
    cell(ws, 2, 2, "Status", font=HEADER_FONT, fillc=EVEREST_GREEN, align=CENTER)
    cell(ws, 2, 3, "Note", font=HEADER_FONT, fillc=EVEREST_GREEN)
    ws.row_dimensions[2].height = 26
    default_items = ["City fees checked", "County fees checked", "All special districts checked",
                     "Utilities checked", "Schools checked", "State checked",
                     "No estimated values used", "All sources cited"]
    if not checklist:
        checklist = [{"item": it, "status": "", "note": ""} for it in default_items]
    r = 3
    for i, e in enumerate(checklist):
        zebra = BEIGE if i % 2 else None
        cell(ws, r, 1, e.get("item", ""), font=CAT_FONT, fillc=zebra or BEIGE)
        st = e.get("status", "")
        st_fill = APPLIES_Y if st.strip().lower().startswith("y") else (
            APPLIES_N if st.strip().lower() in ("n", "no", "n/a", "na") else None)
        cell(ws, r, 2, st, fillc=st_fill, align=CENTER)
        cell(ws, r, 3, e.get("note", ""), fillc=zebra)
        r += 1

    r += 1
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
    cell(ws, r, 1, "Known Uncertainties / Manual Confirmation Needed", font=LABEL_FONT, fillc=BIRCH)
    for col in (2, 3):
        ws.cell(row=r, column=col).fill = fill(BIRCH)
    r += 1
    if not uncertainties:
        note_row(ws, r, 3, "None flagged \u2014 all categories verified to primary sources.")
        r += 1
    else:
        for u in uncertainties:
            ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
            cell(ws, r, 1, f"\u2022  {u}", font=DATA_FONT, align=WRAP_TOP)
            r += 1
    ws.sheet_view.showGridLines = False


def verify(out_path):
    """Reopen the workbook, confirm it loads and no cell holds an Excel error string."""
    errs = []
    wb = openpyxl.load_workbook(out_path)
    error_tokens = ("#REF!", "#DIV/0!", "#VALUE!", "#NAME?", "#N/A", "#NULL!", "#NUM!")
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str) and c.value in error_tokens:
                    errs.append(f"{ws.title}!{c.coordinate}={c.value}")
    return wb.sheetnames, errs


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python build_fee_workbook.py <spec.json> <output.xlsx>")
    spec_path, out_path = sys.argv[1], sys.argv[2]
    with open(spec_path, "r", encoding="utf-8") as fh:
        spec = json.load(fh)

    wb = openpyxl.Workbook()
    build_cover(wb, spec)
    build_jurisdiction(wb, spec)
    build_layers(wb, spec)
    build_master(wb, spec)
    build_triggers(wb, spec)
    build_completeness(wb, spec)
    wb.save(out_path)

    sheets, errs = verify(out_path)
    summary = {
        "status": "errors_found" if errs else "ok",
        "output": out_path,
        "sheets": sheets,
        "fee_rows": len(spec.get("master_fees", [])),
        "jurisdiction_entities": len(spec.get("jurisdiction_stack", [])),
        "cost_triggers": len(spec.get("cost_triggers", [])),
        "open_uncertainties": len(spec.get("completeness", {}).get("uncertainties", [])),
        "cell_errors": errs,
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
