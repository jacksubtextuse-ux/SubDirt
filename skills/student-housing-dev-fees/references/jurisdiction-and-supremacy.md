# Jurisdiction Stack & Supremacy Framework

Two questions drive Steps 0–1: **which authorities can charge this site**, and **when two of them
overlap, which one actually does.** Get the first wrong and you miss fees; get the second wrong and you
double-count or omit. This file is how to answer both defensibly.

## Part A — Build the stack (Step 0)

Resolve each layer below from the address. For each, record the **legal authority type** (home-rule
city, general-law city, county, independent special district, state agency, etc.) and **what it is
legally allowed to levy** — its taxing/fee power is bounded by statute or charter, and that boundary is
what makes "this entity cannot charge X" a defensible statement rather than a guess.

| Layer | What to confirm | How to confirm (primary source) |
|---|---|---|
| City vs. county | Is the parcel inside incorporated city limits or in unincorporated county? | County GIS/parcel viewer + city limits layer; the city/county boundary map. This single fact reorders the entire stack. |
| County | Which county | County assessor/GIS |
| State | Which state (sets the enabling statutes for everything below) | — |
| School district(s) | Elementary/unified/HS districts serving the parcel | District boundary locator; state DOE district map |
| Fire protection | City fire dept. vs. independent fire district | County LAFCo/special-district roster; district service-area map |
| Water provider | City utility vs. independent water district/authority | Utility service-area map; "who's my water provider <address>" on the city/utility site |
| Sewer provider | Often a *different* entity than water | Sewer authority service-area map |
| Stormwater / watershed | Municipal MS4 vs. regional watershed/flood-control district | Regional district map; municipal stormwater utility |
| Transportation / mobility | City, county, MPO/RTA, or toll/mobility authority with a fee | Impact-fee district maps; MPO documents |
| Special-assessment / improvement districts | CFD/Mello-Roos, CDD, PID, BID, metro district, downtown district | County assessor parcel detail (shows district tax codes); district administrator |
| Campus / downtown / overlay zones | Any overlay that adds or modifies fees | Municipal zoning map + overlay layer |
| State / regional permitting agencies | Coastal, air, water-quality, environmental-review bodies with permit fees | State agency jurisdiction maps |

Don't move on until every row is resolved or affirmatively marked "none applicable, per <source>."

## Part B — Resolve supremacy (Step 1 and the master table's supremacy column)

When two authorities both look like they could charge, exactly one of four situations is true. Identify
which, and cite the instrument that settles it.

1. **One preempts the other.** Often a city's adopted impact fee preempts a county fee inside city
   limits, or vice-versa — but this is **state- and charter-specific**, never assume the direction.
   Cite the enabling statute or the interlocal/annexation agreement. *Example pattern:* in many states
   a home-rule city inside its limits charges its own transportation impact fee and the county fee does
   not apply intra-city; in others the county collects a countywide fee regardless. Verify which.

2. **Both apply, to different things.** City charges the building permit; the independent water
   authority charges the capacity fee; the school district charges its own fee. No conflict — they fund
   different systems. Say so explicitly so the reader sees it was considered, not missed.

3. **One collects on behalf of the other.** A city or county frequently collects a school, regional
   transportation, or state fee at permit issuance and remits it. The *collector* and the *charging
   authority* differ — record both, and don't double-count the same dollars as two fees.

4. **Genuinely uncertain.** If you cannot determine the direction from primary sources, say so plainly
   in the supremacy cell and **name the governing statute or charter provision** the analyst should
   read or the agency to call. An explicit "governed by §___, direction unconfirmed — confirm with
   <agency>" is a real deliverable; a confident guess is not.

## State shorthand (orientation only — always verify against the live instrument)

These are starting intuitions, not facts to rely on. Use them to know *what to search for*, then
confirm every applicable item against the adopted document.

- **California:** Mitigation Fee Act (AB1600) nexus studies drive impact fees; school developer fees
  under Ed. Code §17620 (Levels 1/2/3); Quimby Act parkland; Mello-Roos CFDs; Title-24 energy and CASp
  accessibility at the state layer; coastal/air/water-quality regional agencies common.
- **Florida:** impact fees governed by the Impact Fee Act (§163.31801); CDDs (Ch. 190) are common and
  recurring; concurrency/proportionate-share; water-management-district permitting.
- **Texas:** impact fees under Local Gov't Code Ch. 395; PIDs and MUDs common; no state income/school
  developer fee, but MUD/PID assessments matter.
- **Colorado:** metro/metropolitan districts are pervasive and recurring; system development fees from
  water/sanitation districts that are independent of the municipality.
- **Pennsylvania:** MPC governs; transportation impact fees require an adopted Act 209 study;
  SALDO-driven parkland dedication/in-lieu.

If the state isn't listed, that changes nothing about the method: resolve the stack, find each
authority's enabling statute, and verify every fee against the adopted instrument.
