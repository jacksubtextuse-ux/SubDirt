# Word Report Generation Template (docx-js)

## Setup

```bash
npm install docx
```

```javascript
const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, LevelFormat,
        HeadingLevel, BorderStyle, WidthType, ShadingType,
        PageNumber, PageBreak, TabStopType, TabStopPosition } = require('docx');
```

## Color Constants

```javascript
const DARK_BLUE = "1B3A5C";
const MED_BLUE = "2E75B6";
const LIGHT_BLUE = "D5E8F0";
const GREEN = "4CAF50";
const YELLOW = "FFC107";
const RED = "F44336";
const LIGHT_GRAY = "F5F5F5";
const WHITE = "FFFFFF";
const PD_GREEN = "E2EFDA";
const PD_DARK = "375623";
```

## Table Infrastructure

```javascript
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
const cellMargins = { top: 60, bottom: 60, left: 100, right: 100 };
```

## Helper Functions

These helper functions are the core building blocks. Use them for every table and paragraph in the document. They ensure consistent formatting throughout.

### Table Cells

```javascript
// Standard header cell — dark blue background, white bold text
function headerCell(text, width) {
  return new TableCell({
    borders, width: { size: width, type: WidthType.DXA },
    shading: { fill: DARK_BLUE, type: ShadingType.CLEAR },
    margins: cellMargins, verticalAlign: "center",
    children: [new Paragraph({
      alignment: AlignmentType.LEFT,
      children: [new TextRun({ text, bold: true, color: WHITE, font: "Arial", size: 20 })]
    })]
  });
}

// Standard data cell — customizable fill, color, bold, alignment
function dataCell(text, width, opts = {}) {
  return new TableCell({
    borders, width: { size: width, type: WidthType.DXA },
    shading: { fill: opts.fill || WHITE, type: ShadingType.CLEAR },
    margins: cellMargins, verticalAlign: "center",
    children: [new Paragraph({
      alignment: opts.align || AlignmentType.LEFT,
      children: [new TextRun({
        text, bold: opts.bold || false, color: opts.color || "333333",
        font: "Arial", size: 20, italics: opts.italic || false
      })]
    })]
  });
}

// PD-specific cell — green background, dark green bold text, centered
function pdCell(text, width) {
  return new TableCell({
    borders, width: { size: width, type: WidthType.DXA },
    shading: { fill: PD_GREEN, type: ShadingType.CLEAR },
    margins: cellMargins, verticalAlign: "center",
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text, bold: true, color: PD_DARK, font: "Arial", size: 18 })]
    })]
  });
}

// Status cell — color-coded based on compliance status
function statusCell(status, width) {
  let fill, color, text;
  if (status === "COMPLIANT") { fill = "E8F5E9"; color = GREEN; text = "COMPLIANT"; }
  else if (status === "PD") { fill = PD_GREEN; color = PD_DARK; text = "PD NEGOTIATION"; }
  else if (status === "FLAG") { fill = "FFF3E0"; color = "E65100"; text = "REQUIRES VERIFICATION"; }
  else if (status === "BASELINE") { fill = LIGHT_GRAY; color = "666666"; text = "R-MF BASELINE"; }
  else if (status === "PASS") { fill = "E8F5E9"; color = GREEN; text = "PASS"; }
  else if (status === "FAIL") { fill = "FFC7CE"; color = RED; text = "FAIL"; }
  else if (status === "NA") { fill = LIGHT_GRAY; color = "666666"; text = "N/A"; }
  else { fill = LIGHT_GRAY; color = "666666"; text = status; }
  return new TableCell({
    borders, width: { size: width, type: WidthType.DXA },
    shading: { fill, type: ShadingType.CLEAR },
    margins: cellMargins, verticalAlign: "center",
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text, bold: true, color, font: "Arial", size: 18 })]
    })]
  });
}
```

### Paragraphs

```javascript
function sectionHeading(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 200 },
    children: [new TextRun({ text, bold: true, font: "Arial", size: 28, color: DARK_BLUE })]
  });
}

function subHeading(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 240, after: 120 },
    children: [new TextRun({ text, bold: true, font: "Arial", size: 24, color: MED_BLUE })]
  });
}

function bodyText(text, opts = {}) {
  return new Paragraph({
    spacing: { before: 80, after: 80 },
    children: [new TextRun({
      text, font: "Arial", size: 20,
      color: opts.color || "333333", bold: opts.bold || false, italics: opts.italic || false
    })]
  });
}

// For paragraphs with mixed formatting (bold + normal in same paragraph)
function multiRunParagraph(runs) {
  return new Paragraph({
    spacing: { before: 80, after: 80 },
    children: runs.map(r => new TextRun({
      font: "Arial", size: 20,
      color: r.color || "333333", bold: r.bold || false, italics: r.italic || false, text: r.text
    }))
  });
}

function bulletItem(text, opts = {}) {
  return new Paragraph({
    bullet: { level: 0 },
    spacing: { before: 40, after: 40 },
    children: [new TextRun({
      text, font: "Arial", size: 20,
      color: opts.color || "333333", bold: opts.bold || false
    })]
  });
}

function pageBreak() {
  return new Paragraph({ children: [new PageBreak()] });
}
```

### PD-Specific Table Rows

```javascript
// 5-column row for PD deviation tables
function pdRow(standard, baseline, pdTarget, projectValue, notes) {
  return new TableRow({ children: [
    dataCell(standard, 2000, { bold: true }),
    dataCell(baseline, 2000, { fill: LIGHT_GRAY, color: "666666" }),
    dataCell(pdTarget, 2000, { fill: PD_GREEN, color: PD_DARK, bold: true }),
    dataCell(projectValue, 2000),
    dataCell(notes, 2200)
  ]});
}
```

## Document Structure

```javascript
const doc = new Document({
  styles: {
    paragraphStyles: [{
      id: "Normal", name: "Normal",
      run: { font: "Arial", size: 20, color: "333333" },
      paragraph: { spacing: { line: 276 } }
    }]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1200, bottom: 1200, left: 1200, right: 1200 }
      }
    },
    headers: {
      default: new Header({ children: [new Paragraph({
        alignment: AlignmentType.RIGHT,
        children: [
          new TextRun({ text: "SITE [ID] — [ANALYSIS TYPE]", font: "Arial", size: 16, color: MED_BLUE, bold: true }),
          new TextRun({ text: "  |  CONFIDENTIAL", font: "Arial", size: 16, color: "999999" })
        ]
      })] })
    },
    footers: {
      default: new Footer({ children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [
          new TextRun({ text: "Page ", font: "Arial", size: 16, color: "999999" }),
          new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 16, color: "999999" }),
          new TextRun({ text: " of ", font: "Arial", size: 16, color: "999999" }),
          new TextRun({ children: [PageNumber.TOTAL_PAGES], font: "Arial", size: 16, color: "999999" })
        ]
      })] })
    },
    children: [
      // Title page elements go here
      // Section content goes here
    ]
  }]
});
```

## Title Page Pattern

### By-Right Report

```javascript
new Paragraph({ spacing: { before: 2400 } }),
new Paragraph({ alignment: AlignmentType.CENTER, children: [
  new TextRun({ text: "ZONING COMPLIANCE ANALYSIS", font: "Arial", size: 44, bold: true, color: DARK_BLUE })
] }),
new Paragraph({ spacing: { before: 200 }, alignment: AlignmentType.CENTER, children: [
  new TextRun({ text: "SITE [ID] — [ADDRESS]", font: "Arial", size: 32, color: MED_BLUE })
] }),
new Paragraph({ spacing: { before: 100 }, alignment: AlignmentType.CENTER, children: [
  new TextRun({ text: "[CITY], [STATE]", font: "Arial", size: 26, color: "666666" })
] }),
new Paragraph({ spacing: { before: 600 }, alignment: AlignmentType.CENTER, children: [
  new TextRun({ text: "Zoning District: [DISTRICT] | Overlay: [OVERLAY]", font: "Arial", size: 24, color: "666666" })
] }),
new Paragraph({ spacing: { before: 800 }, alignment: AlignmentType.CENTER, children: [
  new TextRun({ text: "Prepared: [Month Year]", font: "Arial", size: 20, color: "999999" })
] }),
new Paragraph({ spacing: { before: 100 }, alignment: AlignmentType.CENTER, children: [
  new TextRun({ text: "PRIVILEGED & CONFIDENTIAL — FOR INTERNAL USE ONLY", font: "Arial", size: 18, color: RED, bold: true })
] }),
```

### PD-Forward Report

Same as above but with:
- Title: "PLANNED DEVELOPMENT REZONING ANALYSIS"
- Subtitle: "Current Zoning: [BASE] → Target: PD (Planned Development)"
- PD Context Banner (see PD Strategy Guide reference)

## Saving the Document

```javascript
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync('[output_path]', buffer);
  console.log('Document generated successfully');
});
```

## Common Table Structures

### Key-Value Table (2 columns)
For site data, district parameters, etc.
```javascript
new Table({ rows: [
  new TableRow({ children: [headerCell("Attribute", 3600), headerCell("Value", 6600)] }),
  new TableRow({ children: [dataCell("Address", 3600, { bold: true }), dataCell("123 Main St", 6600)] }),
  // ...more rows
], width: { size: 10200, type: WidthType.DXA } })
```

### Compliance Table (6 columns)
For by-right compliance checks.
```javascript
new Table({ rows: [
  new TableRow({ children: [
    headerCell("Standard", 1800), headerCell("Code Requirement", 2400),
    headerCell("Project Value", 2000), headerCell("Status", 1200),
    headerCell("Citation", 1400), headerCell("Notes", 1400)
  ] }),
  // data rows...
], width: { size: 10200, type: WidthType.DXA } })
```

### PD Deviation Table (5 columns)
For PD analyses. Uses the `pdRow()` helper.
```javascript
new Table({ rows: [
  new TableRow({ children: [
    headerCell("Standard", 2000), headerCell("[District] Baseline", 2000),
    headerCell("PD Target", 2000), headerCell("Project Value", 2000),
    headerCell("Notes", 2200)
  ] }),
  pdRow("Max Height", "35 ft", "~104 ft / 8 stories", "8 stories", "197% deviation"),
  // ...more rows
], width: { size: 10200, type: WidthType.DXA } })
```

### Action Items Table (5 columns)
```javascript
new Table({ rows: [
  new TableRow({ children: [
    headerCell("#", 600), headerCell("Action Item", 3800),
    headerCell("Responsible", 2000), headerCell("Priority", 1400),
    headerCell("Timing", 2400)
  ] }),
  // numbered rows...
], width: { size: 10200, type: WidthType.DXA } })
```
