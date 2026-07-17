# Planned Development (PD) Strategy Guide

## When to Use PD Framing

A PD-forward analysis replaces the standard compliance report when the building program cannot be built under the existing zoning. Instead of documenting a series of FAIL statuses, the report reframes the analysis as an entitlement strategy document — the base district standards become the "deviation baseline" and the report focuses on what needs to be negotiated through the PD process.

## PD Report vs. By-Right Report — Key Differences

| Element | By-Right Report | PD-Forward Report |
|---|---|---|
| Executive summary | "This building complies/doesn't comply" | "This building requires PD — here's the deviation framework" |
| Status cells | PASS / FAIL / VERIFY | PASS / PD / VERIFY / BASELINE / COMPLIANT |
| Table structure | Standard / Requirement / Project Value / Status | Standard / Base District Baseline / PD Target / Project Value / Notes |
| Parking section | "Required: X, Provided: Y, Deficit: Z" | "Base requirement: X, PD reduction target: Y, strategy for negotiation" |
| Tone | Audit/compliance | Strategy/entitlement advisory |
| Action items | "Verify X, confirm Y" | "File PD application, prepare traffic study, negotiate parking, etc." |

## PD Deviation Summary Table

Every PD report opens with a deviation summary table immediately after the executive summary. This is the single most important table in the document — it gives the reader an instant picture of what needs to be negotiated.

### Column Structure (5 columns, full table width)

| Column | Width | Content |
|---|---|---|
| Standard | 2000 DXA | The zoning parameter |
| [District] Baseline | 2000 DXA | The by-right limit (gray background, gray text) |
| PD Target | 2000 DXA | What the PD needs to establish (PD green background, dark green text) |
| Project Value | 2000 DXA | What the building proposes |
| Notes | 2200 DXA | Deviation %, strategy notes |

### Typical PD Deviations by Building Type

For **student housing** projects specifically, the most common PD deviations are:

1. **Height** — Student housing buildings are almost always taller than surrounding residential zoning allows. 4-12 story buildings in 35-45 ft districts are common.

2. **Density** — Student housing operates at much higher density than conventional multifamily. 200-400 units on 1-2 acres is typical for university-proximate sites, while conventional zoning may allow 15-40 units.

3. **Parking** — Student housing provides less parking per bed than conventional multifamily codes require. Ratios of 0.3-0.5 spaces/bed are common in the industry, while codes often require 1.0-2.5 spaces/unit.

4. **Bedroom Cap** — Many jurisdictions limit bedrooms per structure (often 200) specifically targeting student housing. PD can override this.

5. **Facade Length** — Large student housing buildings frequently exceed 200 ft facade limits. Architectural articulation is the typical PD mitigation.

## PD Banner

Every PD-forward report includes a prominent banner on the title page, immediately below the title block. This banner uses the PD green background with a 3pt dark green border and contains:

1. **Bold header line**: "PD REZONING REQUIRED — THIS ANALYSIS IS FRAMED FOR PD ENTITLEMENT STRATEGY"
2. **Context paragraph**: 1-2 sentences explaining why PD is required and what the key deviations are

This is implemented as a single-cell table for consistent formatting:

```javascript
new Table({ rows: [new TableRow({ children: [new TableCell({
  borders: { /* 3pt PD_DARK borders all sides */ },
  width: { size: 10200, type: WidthType.DXA },
  shading: { fill: PD_GREEN, type: ShadingType.CLEAR },
  margins: { top: 200, bottom: 200, left: 300, right: 300 },
  children: [
    // Bold header paragraph
    // Context paragraph
  ]
})]})], width: { size: 10200, type: WidthType.DXA } })
```

## PD Process Section Content

Section 8 of every PD-forward report covers the PD process itself. Pull this information from the municipal code. Typical elements:

### What the Code Says About PD
- Which section governs PD? (e.g., "Section 29-2.4")
- What properties are eligible? (usually any except those in certain districts)
- What's the approval body? (usually City Council, with P&Z recommendation)
- Is it a legislative action? (yes — gives Council discretion)
- What must the development plan include?

### PD Application Requirements (typical)
1. Pre-application meeting with planning staff
2. Neighborhood meeting (often required or strongly recommended)
3. Development plan submission showing all deviations from base district
4. Traffic impact study (usually triggered above a threshold)
5. Public hearing before Planning & Zoning Commission
6. City Council vote (legislative action — subject to political dynamics)

### Public Benefit Framework
PD approvals often hinge on demonstrating public benefit. For student housing, common public benefit arguments include:

- **Housing supply**: Addresses student housing shortage near campus
- **Tax revenue**: Higher assessed value than existing low-density residential
- **Infrastructure investment**: Developer-funded improvements (sidewalks, utilities, streetscape)
- **Urban design**: Better-designed building than what by-right zoning would produce
- **Reduced sprawl**: Concentrating student housing near campus reduces car dependence
- **Employment**: Construction jobs and ongoing property management employment

**Never fabricate public benefit claims.** Only include benefits that are genuinely supportable for the specific project and context.

## Action Items Matrix

Every PD-forward report ends with a numbered action items matrix. Organize by priority:

### Structure

| # | Action Item | Responsible Party | Priority | Timing |
|---|---|---|---|---|
| 1 | Verify zoning of all assembled parcels | Development team / Title company | Critical | Pre-application |
| 2 | Engage Columbia planning staff — pre-application conference | Development team | Critical | Immediate |
| 3 | Commission traffic impact study | Traffic engineer | High | Pre-filing |
| ... | ... | ... | ... | ... |

### Typical Action Items for Student Housing PD

1. Parcel zoning verification (all assemblage parcels)
2. Pre-application meeting with planning staff
3. Traffic impact study
4. Parking demand study (to support reduced ratio)
5. Neighborhood outreach / community meeting
6. Height/massing study showing transitions to adjacent properties
7. Public benefit package development
8. PD development plan preparation (architect/planner)
9. Legal review of PD ordinance requirements
10. Timeline analysis (Council meeting schedule, election cycles)
11. Confirm comprehensive plan alignment
12. Utility capacity verification
13. Environmental review (if applicable)
14. Financial proforma sensitivity to PD conditions

## Comparing Multiple PD Sites

When analyzing multiple sites in the same market that both require PD, include a comparison noting:

- Which site has fewer deviations (may be easier to entitle)
- Which site has larger deviations (more negotiation needed)
- Whether filing simultaneously creates strategic advantages or risks
- Whether one site's PD precedent could help or hurt the other
- Different base districts create different negotiation dynamics (e.g., R-MF density cap vs. M-OF no density cap)
