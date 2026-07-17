# Political & Precedent Research Protocol

The political layer is researched, not intuited. Every statement about what a council or commission
"will" do is grounded in what it **did** — named projects, dates, votes, margins, stated reasons.
This file defines where to look, what to extract, and how to turn it into a defensible risk rating.

## Where to look (in priority order)

1. **Planning commission and council agendas, minutes, and staff reports** — the primary record.
   Most jurisdictions publish through a portal (Legistar, Granicus, CivicClerk, Municode Meetings) or
   the clerk's page. Staff reports show the use classification applied, the findings framework, and
   staff's recommendation; minutes show votes and conditions; video/transcripts show reasoning.
2. **Hearing video / transcripts** — where a decision was close or contested, the transcript is where
   member-by-member logic lives. If the user has run the city-council-transcript-analysis skill,
   ingest its output here (votes, reasoning, conditions, dos/don'ts) rather than re-deriving.
3. **Local news and civic media** — search "[city] student housing rezoning", "[city] council rejects
   apartments", "[university] purpose-built student housing approval", project names from the
   pipeline. News is the pointer; follow it back to the primary record and cite both.
4. **Organized-opposition footprints** — neighborhood-association pages, preservation trusts,
   change.org petitions, "Save [neighborhood]" groups. These reveal trigger issues and mobilization
   capacity before they show up at your hearing.
5. **The jurisdiction's own signals** — adopted moratoria (on anything: a council willing to use
   moratoria is a datapoint), pending ZOTAs, comp-plan update processes, housing-study rhetoric,
   campus-area small-area plans.

Time-bound the sweep: ~5 years back, weighted to the last 2–3. Note council turnover since key votes
— a precedent decided by members no longer serving is weaker evidence either way.

## The precedent table (required in every memo)

One row per comparable entitlement decision (student housing first; large multifamily second; any
project in the same district/corridor third):

| Field | What to capture |
|---|---|
| Project / applicant | Name, developer, site (distance from subject) |
| Year decided | And how long the process ran, if determinable |
| Request | Mechanism (ZMA to what, PD, CUP, development plan) + scale (beds/units/stories) |
| Staff recommendation | Approve / deny / conditions |
| PC vote | Count and margin |
| Council vote | Count and margin (note protest petitions / supermajority triggers) |
| Outcome | Approved / denied / withdrawn / approved-reduced |
| Stated opposition themes | From the record: historic demolition, neighborhood character, parking/traffic, displacement, "too tall," student behavior, infrastructure |
| Conditions imposed | What approval cost: step-downs, parking changes, design conditions, traffic improvements, community benefits |
| Sources | Minutes/news URLs + dates |

Two derived readings matter most:
- **The margin pattern.** An 8–7 denial and a unanimous denial are different markets. Thin margins
  mean individual-member engagement can flip outcomes; blowouts mean the path itself is wrong.
- **The divergence pattern.** Where commission and council split (PC approves 8–2, council denies
  8–7), the commission's findings are not protective — underwrite to the council, and weight paths
  that avoid a legislative vote accordingly.

## Opposition-theme coding (student-housing-specific)

Code every precedent's opposition themes; the subject site's exposure to each theme is the risk map:

| Theme | What triggers it | Subject-site check |
|---|---|---|
| Historic resources | Demolition of listed/eligible structures; H-overlay adjacency | Any on-site or adjacent resources? (Absence is a marketable advantage — say so) |
| Neighborhood character / scale | Height abutting SF residential; "out of scale" | Which edges abut low-density zones? Step-down tools available? |
| Parking & traffic | Low ratios near neighborhoods that absorb overflow | On-street permit regimes nearby? Ratio vs. recent approvals |
| Displacement / affordability | Demolishing occupied housing; "luxury student" framing | Current site use — commercial redevelopment is materially safer ground |
| Student behavior / "studentification" | Proximity to established SF neighborhoods | Distance/buffer to owner-occupied blocks |
| Infrastructure capacity | Sewer/school/traffic capacity claims | Utility capacity confirmations from Site Specifics work |

## The risk rating (evidence-required rubric)

Rate the recommended path's political risk on a four-level scale. The rating sentence must carry its
evidence: *"HIGH — the council denied the last comparable student rezoning 8–7 in Nov 2025 over
historic demolition and neighborhood character (WKYT, minutes 11/20/25), and the subject requires the
same council vote; mitigating: no historic resources on site."*

- **LOW** — path requires no legislative vote; recent comparable approvals were staff/commission-level
  and uncontested; no organized opposition footprint found.
- **MODERATE** — public hearing(s) required; comparable projects approved but with meaningful
  conditions; opposition exists but hasn't defeated a comparable project recently.
- **HIGH** — legislative vote required in a jurisdiction with a recent comparable denial, thin
  approval margins, or organized opposition with a win record; or classification/mechanism ambiguity
  puts the path itself at interpretive risk.
- **SEVERE** — recent comparable denials on the same fact pattern the subject presents (same corridor,
  same objection profile), active hostile ZOTA/moratorium activity, or a required supermajority the
  precedent record says is unreachable.

State the rating **per path**, not just overall — the whole point of path selection is that a
development-plan route and a rezoning route on the same site can sit two levels apart.

## Conditions forecasting

From the precedent table's conditions column, list what this jurisdiction actually extracts as the
price of approval, and pre-price the ones the subject should expect. This feeds underwriting (cost,
program) and the engagement strategy (offer proactively what will be extracted anyway, on your own
terms). Do not invent conditions with no local precedent — the forecast is an extrapolation from the
table, labeled as such.

## Engagement strategy notes

Close the political section with the practical read: which council district the site sits in and who
represents it; whether early neighbor engagement is expected practice (some jurisdictions require a
neighborhood meeting — that's Step 3 mechanics; here, note whether *voluntary* early engagement has
correlated with outcomes in the precedent record); and the two or three messages the record suggests
land (e.g., "no historic demolition, no rezoning required, replaces a parking lot") versus the ones
that don't. Keep it evidence-tied and short — this is analyst support, not a lobbying plan.
