# site-specifics — SPEC (not yet built)

**Scope.** The physical/environmental layer of a site analysis — §4.2 ("Physical fitness to carry the
program") and the utilities/concurrency content of the example memos. Given a site (parcels), produce
a sourced physical-conditions assessment:

- FEMA flood zone, streams/wetlands, hydric soils
- Geotechnical flags (karst/sinkhole, bedrock depth, water table) → diligence triggers
- Radon zone, wildfire, other environmental screens
- Environmental red flags from current/prior uses (UST risk on fuel/convenience parcels → Phase I ESA trigger)
- Utilities: provider per service (water, sewer, electric, gas, fiber, stormwater), availability,
  tap/connection mechanics (fee side belongs to student-housing-dev-fees), capacity confirmations needed
- Access/frontage, adjacency map (what abuts each edge — drives buffers and opposition exposure;
  feeds entitlements skill)
- Historic/cultural resources on-site and adjacent (feeds entitlements political layer)

**Output.** A "Site Specifics" Word section/memo + a findings table (Attribute | Finding | Implication
| Source & vintage), with a per-dimension GO / GO-conditioned / FLAG verdict and a diligence-items
list ([Data needed: geotech opinion] etc.).

**House rules.** Same as siblings: primary sources only, source-and-vintage on every table, no
inferred conditions, `[To be verified]` for anything not determinable. Findings are screens, not
engineering — every physical flag maps to the professional study that resolves it (geotech, Phase I,
ALTA, capacity letter).

**Design notes.** Much of this data comes from the platform (DirtAI-style parcel data) or public
sources (FEMA NFHL, NRCS soils, state radon maps, USGS karst). Decide per-market what's scriptable vs.
research. Keep the diligence-trigger mapping table as a reference file.
