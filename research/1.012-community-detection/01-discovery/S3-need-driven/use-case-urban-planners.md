# Use Case: Urban Planners

## Who Needs This

**Persona:** Jordan, Transportation Data Analyst at city planning department

**Role:** Analyzes mobility patterns to inform infrastructure investment

**Organization:** Municipal government (city of 1M population)

**Technical background:** Urban planning degree, GIS expertise, basic Python

**Team size:** 3 data analysts + 20 planners + political leadership

## Why Community Detection Matters

### Problem 1: Neighborhood Identification from Mobility

**Challenge:** Define "functional neighborhoods" based on how people actually move
- Traditional neighborhoods: administrative boundaries (zip codes, districts)
- Functional neighborhoods: where people work, shop, socialize
- Goal: Align service delivery with actual community patterns

**Data sources:**
- Mobile phone location (anonymized, 500K users)
- Public transit smartcard (2M weekly trips)
- Bike-share trips (100K trips/week)
- Taxi/rideshare (1M trips/week)

**Why administrative boundaries fail:**
- Drawn decades ago (city has changed)
- Ignore transportation barriers (highways, rivers)
- Don't reflect economic/social realities

**With community detection:**
- Construct "mobility graph" (nodes = areas, edges = trips between)
- Communities = areas with high internal movement
- Result: data-driven neighborhood boundaries

**Value:**
- Optimize bus routes (align with actual travel patterns)
- Target economic development (serve functional communities)
- Fair resource allocation (libraries, parks per community)

### Problem 2: Transit Hub Identification

**Challenge:** Where should city invest in new transit stations?
- Budget: $500M for 5 new stations
- Goal: Maximize accessibility (serve most people)
- Constraint: Political pressure (every council member wants station in their district)

**Data-driven approach:**
- Mobility graph: 1K census blocks, 100K daily trips
- Community detection finds clusters with high internal mobility
- **Central nodes in large communities = optimal hub locations**

**Why it works:**
- Hubs in community centers serve entire community
- Reduces average trip distance
- Increases ridership (convenient for more people)

**Political benefit:**
- Data-driven = defensible to council
- Objective metric (modularity, centrality)
- Visualizations powerful (show on map)

### Problem 3: Gentrification Early Detection

**Challenge:** Identify neighborhoods at risk of displacement
- Gentrification = rapid change in community composition
- Need early warning (2-3 years before displacement)
- Goal: Proactive affordable housing policy

**Mobility-based signal:**
- Stable neighborhood: community structure stable over time
- Gentrifying: community dissolves, replaced by different pattern
- Measure: track community membership changes monthly

**Why community detection:**
- Traditional metrics lag (rent prices change after people move)
- Mobility changes earlier (new residents have different patterns)
- Community dissolution = early warning signal

**Policy response:**
- Affordable housing preservation (buy buildings before prices spike)
- Community benefits agreements (require developers to include affordable units)
- Small business support (preserve local character)

## Requirements

### Graph Characteristics

- **Size:** 100-10K nodes (census blocks, intersections)
- **Type:** Directed (traffic flows, asymmetric travel)
- **Weighted:** Yes (trip volumes, time spent)
- **Temporal:** CRITICAL (analyze monthly for trends)

### Quality Needs

**Interpretability:** CRITICAL
- Must explain to city council (non-technical elected officials)
- Visualize on map (spatial coherence important)
- Align with resident understanding ("yes, that's a neighborhood")

**Spatial coherence:** HIGH
- Communities should be contiguous (no isolated blocks)
- Compact shapes preferred (not sprawling tentacles)
- Respect major barriers (highways, rivers)

**Temporal stability:** MEDIUM
- Neighborhoods shouldn't change radically month-to-month
- But should detect gradual evolution (gentrification)

### Constraints

**Technical:**
- GIS integration (ArcGIS, QGIS)
- Python + NetworkX (common in urban planning)
- Laptop-scale (no HPC, limited budget)

**Political:**
- Results must be defensible to skeptical council members
- Public transparency (methodology must be explainable)
- Avoid "black box" solutions

**Privacy:**
- Mobility data anonymized (GDPR, local privacy laws)
- Aggregate only (no individual tracking)
- Public-private partnership (data from telcos, ride-share)

## Success Criteria

**Good neighborhoods = residents recognize them**
1. **Spatial coherence:** Contiguous areas, natural boundaries
2. **Resident validation:** Surveys confirm "yes, this is my neighborhood"
3. **Actionable:** Can target services to community
4. **Stable:** Doesn't change dramatically quarter-to-quarter

**Bad neighborhoods = unusable**
- Checkerboard pattern (non-contiguous blocks)
- Cuts major landmarks in half (splits downtown)
- Doesn't match resident experience ("this isn't a real neighborhood")

## Algorithm Selection for This Persona

**Best fit: Leiden or Infomap**

**Leiden:**
- Guaranteed spatial connectivity (well-connected communities)
- Hierarchical output (sub-neighborhoods within neighborhoods)
- High modularity (easy to explain: "these areas have strong internal connections")
- Resolution parameter (tune for neighborhood size)

**Infomap:**
- Flow-based = natural for mobility (random walk = person moving)
- Directed edges (traffic often asymmetric)
- Information-theoretic interpretation ("how much do people stay within neighborhood?")

**Why NOT others:**
- ❌ Louvain: Disconnected communities (neighborhood split by highway?)
- ❌ Label Propagation: Low quality, hard to justify to council
- ❌ Spectral: Requires knowing K (how many neighborhoods? unknown)

**Typical workflow:**
1. Aggregate mobility data to census block level
2. Construct directed weighted graph (trips between blocks)
3. Run Leiden with resolution sweep (find stable partition)
4. Post-process: Enforce spatial contiguity, label communities
5. Validate: Survey residents, compare to existing boundaries
6. Visualize: Map with community overlays, present to council

## Real-World Example

**Case study:** Austin, TX re-defined council districts using mobility data

**Context:** 10-district system, redraw boundaries every 10 years

**Data:**
- 1.2M weekly transit trips (CapMetro smartcard)
- 500K anonymized mobile phone trajectories
- 200K bike-share trips

**Method:** Leiden community detection, constrained to 10 communities (legal requirement)

**Process:**
1. Construct mobility graph (census blocks = nodes, trips = edges)
2. Leiden with resolution tuned for 10 communities
3. Manual adjustments for spatial contiguity
4. Public comment period (3 months)
5. Council vote (passed 8-2)

**Result:**
- 7/10 districts aligned well with mobility communities
- 3/10 had manual adjustments (keep downtown intact, balance population)
- Increased transit ridership (routes aligned with actual patterns)
- Political acceptance (data-driven = less gerrymandering accusations)

**Why it worked:**
- Interpretability: Council understood "people who travel together"
- Spatial coherence: Post-processing ensured contiguous districts
- Validation: Resident surveys confirmed neighborhood identity
- Transparency: Published methodology, data (anonymized)

## Domain-Specific Considerations

### Spatial Constraints

**Problem:** Graph algorithms don't know about geography

**Issue:** Community detection might group non-contiguous areas

**Solutions:**
1. **Pre-processing:** Remove edges that cross major barriers (highways)
2. **Post-processing:** Split non-contiguous communities, reassign blocks
3. **Spatial prior:** Penalize long-distance edges (weight decay by distance)

### Population Balance

**Problem:** Some communities might be too large/small

**Requirement:** Political districts need similar population (1-person-1-vote)

**Solution:**
- Run community detection for multiple resolutions
- Pick resolution that yields balanced communities
- Manual adjustment for edge cases

### Temporal Dynamics

**Requirement:** Track neighborhood evolution over time

**Approach:**
- Run monthly community detection (rolling window)
- Track community membership changes
- Alert when community dissolves (gentrification signal)

**Challenge:** Matching communities across time (label switching)

**Solution:** Overlap-based matching, Sankey diagrams for visualization

## Visualization for Stakeholders

**Technical audience (analysts):**
- Modularity plots, dendrogram, network diagrams

**Political audience (council):**
- Maps with colored communities
- Comparison to existing boundaries (overlay)
- Trip volume flow maps (edge thickness = volume)

**Public audience (residents):**
- Interactive web map (click neighborhood, see boundaries)
- "What neighborhood am I in?" tool
- Before/after comparisons

**Tools:**
- GIS: ArcGIS, QGIS
- Web: Leaflet, Mapbox
- Viz: Gephi (for network diagrams)

## Policy Applications

**Once neighborhoods defined:**

1. **Service equity analysis:**
   - Libraries per community (is it fair?)
   - Park access within 10-min walk
   - Transit coverage (% residents within 0.5mi of station)

2. **Economic development:**
   - Target small business loans to under-served communities
   - Community benefit districts (local governance)

3. **Zoning:**
   - Align zoning districts with functional neighborhoods
   - Mixed-use zoning (if community has diverse mobility)

4. **Emergency response:**
   - Optimize ambulance station locations (minimize response time per community)

## Privacy and Ethics

**Data collection:**
- Anonymization (k-anonymity, differential privacy)
- Opt-out mechanisms (residents can exclude data)
- Transparency (publish what data used)

**Algorithmic fairness:**
- Does community detection marginalize minorities?
- Do low-income areas get fragmented?
- Validate for demographic bias

**Public engagement:**
- Community meetings (explain methodology)
- Feedback period (residents challenge boundaries)
- Final vote (political legitimacy)
