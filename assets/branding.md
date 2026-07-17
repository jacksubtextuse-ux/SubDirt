# SubDirt AI Branding

Applies to every deliverable the toolkit generates (Word memos, Excel workbooks, trackers).

## Logo

**Official mark: `assets/subdirt_logo.png`** (= Option D) — rounded lowercase wordmark, "subdirt" in
a sage→Everest gradient, "ai" in Lime. Rebuilt from the DirtAI mark's styling in Arial Rounded MT
Bold. Options A–C are archived in this folder; don't use them in deliverables. Title pages: logo
centered, ~2.8 in wide, on white.

## Palette (source of truth — matches the fee-workbook constants)

| Name | Hex | Use |
|---|---|---|
| Everest Green | `16352E` | Primary — H1/title bars, table header fills, footer rules |
| Sage | `4EA57E` | Secondary — H2/H3, accents (the logo gradient top) |
| Lime | `C1D100` | Highlight only — sparingly (subtotals, the "ai" in the mark) |
| Birch | `A95818` | Accent for section labels in Excel (fees workbook precedent) |
| Beige | `F7F1E3` | Callout/BLUF boxes, alternating rows, category cells |
| Ink | `2B2B2B` | Body text |
| Muted | `595959` | Source-and-vintage lines, footnotes |

Status semantics (independent of brand accents): pass/viable `E2EFDA` · verify/conditional `FFF2CC`
· fail/killed/high-risk text `C00000` on `F8E1E1`.

## Type

Arial throughout documents (10pt body; 9pt tables; 8pt italic source lines; headings 16/13/11pt in
Everest/Sage). The logo face is Arial Rounded MT Bold — logo only, never for document text.

## Document conventions

- Title page: logo, document title, project line, "Opportunity Intelligence for Land Development",
  "Prepared by SubDirt AI · <date>".
- Footer: project identifier · "Internal — not a legal opinion" · page number.
- Closing disclosure page: SubDirt AI informational-purposes paragraph (see the renderer's default).
- Source-and-vintage line under every table, muted italic.

## Where it's implemented

`skills/student-housing-entitlements/scripts/build_branded_memo.py` — the generic branded Word
renderer (JSON spec → memo). Reuse it for any SubDirt deliverable rather than re-implementing
formatting; it owns these constants.
