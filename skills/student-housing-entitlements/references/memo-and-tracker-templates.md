# Deliverable Templates — Entitlement Path Memorandum (.docx) + Entitlement Tracker (.xlsx)

Generation is Python: `python-docx` for the memo, `openpyxl` for the tracker
(`pip install python-docx openpyxl --break-system-packages`). Formatting follows the house standard
shared with the zoning-compliance skill (see its `references/formatting-standards.md` for the full
palette rationale).

## House formatting constants

```python
DARK_BLUE  = "1B3A5C"   # section headers, title bars
MED_BLUE   = "2E75B6"   # subheadings, table header rows
LIGHT_GRAY = "D9D9D9"   # table borders, category cells
RISK_RED   = "C00000"   # HIGH/SEVERE risk text
COND_AMBER = "FFF2CC"   # conditional / verify cells
OK_GREEN   = "E2EFDA"   # cleared / by-right cells
FONT       = "Arial"    # throughout; 10pt body, 16pt title, 13pt H1, 11pt H2
# Letter page, 1" margins. Footer: site identifier + "Internal — not a legal opinion" + date.
```

Status vocabulary for path/step tables: `VIABLE`, `VIABLE*` (with conditions/ambiguity — footnote it),
`KILLED` (with the citation that kills it), `[To be verified]`.

---

## Entitlement Path Memorandum — 10 sections

Front matter: title block (To / From / Date / Re / Classification: "Internal — prepared for
planning/underwriting. Not a legal opinion."), then a **BLUF box** — a single bordered paragraph
giving: recommended path and mechanism, months (base / contested), political risk rating with its
strongest evidence, and the top three open items. A reader who stops after the BLUF has the answer.

1. **Property & Proposal Identification** — parcel table (APN, address, acreage, current zoning,
   owner/tenure, existing use), jurisdiction and governing code (name, effective date, host URL),
   proposed use and scale as analyzed. Note split zoning and split ownership here.
2. **Executive Summary** — numbered findings (5–7): districts; classification conclusion; by-right
   answer; the viable paths in one line each; recommended path + timeline; risk rating; conditions
   forecast headline. Each finding ≤3 sentences.
3. **Use Classification — the threshold question** — candidate definitions quoted, the reading this
   memo proceeds on, reasoning, and the confirmation plan (verification letter / pre-app). Occupancy
   traps (unrelated-persons caps, bedroom caps) surfaced here if present.
4. **Permission Under Current Zoning & Path Enumeration** — per-parcel use-table findings with quoted
   operative language; then the full path table (every candidate from the taxonomy: mechanism,
   citation, delivers, body, discretion, status VIABLE/KILLED + why). Killed paths stay visible.
5. **Recommended Path — Mechanics & Timeline** — sequence table: Step | Action | Approving body |
   Public hearing? | Statutory clock (cited) or typical range (labeled) | Dependencies/concurrency.
   Follow with the critical-path statement: base months, contested months, and the academic-calendar
   tie ("a development-plan approval by <month> keeps an August <year> delivery alive; slipping past
   <month> pushes lease-up a full cycle"). State the fallback path and its switch trigger.
6. **Comprehensive Plan & Policy Conformance** — the governing designation/placetype (quoted), the
   conformance argument, the state findings statute where a rezoning is in play, and the
   current-use-code-vs-plan-designation trap check (state explicitly which source the designation came
   from). Pending plan/code changes flagged as pending.
7. **Political Environment & Precedent Analysis** — the precedent table (see research protocol for
   columns), margin/divergence readings, opposition-theme exposure map for the subject site, council
   composition and district representative, and the per-path risk ratings with evidence sentences.
8. **Anticipated Conditions, Exactions & Commitments** — what this jurisdiction's record says approval
   will cost (from the precedent conditions column), each item tagged: program impact / cost impact /
   schedule impact. Labeled as extrapolation from cited precedent.
9. **Risks & Open Items** — risk register (Risk | Likelihood | Impact | Mitigant | Owner), then the
   ordered open-items list, each with resolver and method ("[To be verified with LFUCG Planning —
   pre-application conference]"). The #1 item is whatever the recommendation most depends on.
10. **Sources & Limitations** — every code section, plan document, meeting record, and URL with access
    dates; the standard limitations paragraph: internal planning document, not a legal opinion,
    jurisdiction-defined terms, confirm with the municipality and land-use counsel before committing
    capital.

Style rules: **source-and-vintage line under every table**; assumptions and interpretations labeled
in-line; no "typically/generally/usually" without a citation or an "industry-typical, labeled" tag;
quote code text where a conclusion turns on it.

### python-docx patterns

```python
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def shade(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:fill"), hex_fill)
    tcPr.append(shd)

def h1(doc, text):
    p = doc.add_paragraph(); r = p.add_run(text)
    r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True
    r.font.color.rgb = RGBColor.from_string("1B3A5C")
    return p

def std_table(doc, headers, rows, widths=None):
    t = doc.add_table(rows=1, cols=len(headers)); t.style = "Table Grid"
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]; c.text = ""
        r = c.paragraphs[0].add_run(h)
        r.font.name = "Arial"; r.font.size = Pt(9); r.font.bold = True
        r.font.color.rgb = RGBColor.from_string("FFFFFF"); shade(c, "2E75B6")
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            r = cells[i].paragraphs[0].add_run(str(v)); r.font.name = "Arial"; r.font.size = Pt(9)
    return t

def source_line(doc, text):   # the source-and-vintage line under every table
    p = doc.add_paragraph(); r = p.add_run("Source & vintage: " + text)
    r.font.name = "Arial"; r.font.size = Pt(8); r.font.italic = True
```

Build the BLUF box as a 1×1 `Table Grid` table with a light-gray shade and the run bolded lead-in
("Bottom line up front."). Set document defaults once via `doc.styles["Normal"]`
(Arial, 10pt) rather than styling every run.

---

## Entitlement Tracker — 4 sheets

Named `[Site]_Entitlement_Tracker.xlsx`. Row 1 of every sheet: dark-blue merged title bar (site,
jurisdiction, date). Row 2: medium-blue headers, white bold text. Freeze panes at the data row.

1. **Path Steps** — the living schedule. Columns: `# | Step | Mechanism / citation | Approving body |
   Hearing? | Statutory clock | Typical duration | Depends on | Status | Actual date | Notes`.
   Status values with fills: `Not started` (no fill) / `In progress` (amber FFF2CC) / `Complete`
   (green E2EFDA) / `Blocked` (red text C00000). One block of rows per path if a fallback is being
   tracked in parallel; label blocks with a merged gray band row.
2. **Precedents** — the precedent table verbatim from the memo (columns per the research protocol),
   so the deal team can extend it as new decisions land.
3. **Risk Register** — `Risk | Dimension (Classification/Path/Political/Schedule) | Likelihood |
   Impact | Mitigant | Owner | Status`. Likelihood/Impact as Low/Med/High text with amber/red fills
   on High.
4. **Open Items** — `# | Item | Resolves via | Owner | Priority | Status | Date resolved | Answer`.
   Priority 1 = the item the recommendation most depends on. This sheet is the pre-application
   meeting agenda, ready to print.

### openpyxl pattern

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

DARK = PatternFill("solid", fgColor="1B3A5C"); MED = PatternFill("solid", fgColor="2E75B6")
HDR  = Font(name="Arial", size=10, bold=True, color="FFFFFF")
BODY = Font(name="Arial", size=10)
THIN = Border(*[Side(style="thin", color="D9D9D9")]*4)

def sheet_with_title(wb, name, title, headers, col_widths):
    ws = wb.create_sheet(name)
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(headers))
    c = ws.cell(1, 1, title); c.fill = DARK; c.font = Font(name="Arial", size=12, bold=True, color="FFFFFF")
    for i, h in enumerate(headers, 1):
        c = ws.cell(2, i, h); c.fill = MED; c.font = HDR; c.alignment = Alignment(wrap_text=True, vertical="center")
        ws.column_dimensions[c.column_letter].width = col_widths[i-1]
    ws.freeze_panes = "A3"
    return ws
```

After writing, reopen the workbook with `openpyxl.load_workbook` to confirm it loads cleanly before
delivering (house verification habit — same as the fees skill's script does).
