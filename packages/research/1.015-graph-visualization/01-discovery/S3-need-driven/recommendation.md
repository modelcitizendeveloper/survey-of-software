# S3 Recommendation: Use Case-Driven Library Selection

## Quick Reference: Who Needs What

| Persona | Primary Tool | Secondary Tool | Why |
|---------|-------------|----------------|-----|
| **Academic Researcher** | NetworkX + matplotlib | Graphviz (hierarchical) | Publication quality, SciPy integration |
| **Software Architect** | Graphviz | NetworkX + Graphviz | Automated docs, hierarchical layouts |
| **Data Scientist** | Plotly + Dash | PyVis (prototypes) | Interactive dashboards, stakeholder exploration |
| **Bioinformatician** | py4cytoscape | NetworkX + Cytoscape | Domain standard, pathway tools, omics integration |
| **Security Analyst** | NetworkX + Plotly | PyVis (ad-hoc) | Rapid analysis, SIEM integration, incident response |

## Decision Matrix by Priority

### Priority 1: Domain Standards

**If you work in biology/bioinformatics:**
→ **py4cytoscape** (non-negotiable)
- Reviewers expect Cytoscape
- Pathway databases integrated
- Omics data overlay built-in
- Publication standards

**Why not others:** Generic tools lack biological conventions, pathway enrichment, domain-specific apps.

### Priority 2: Output Format

**Static publication figures:**
→ **NetworkX + matplotlib** (academia) or **Graphviz** (documentation)

**Interactive dashboards:**
→ **Plotly + Dash** (professional) or **PyVis** (quick demos)

**Automated documentation:**
→ **Graphviz** (CI/CD integration, deterministic output)

### Priority 3: Scale

**Small (<5K nodes):**
→ Any tool works, choose by output format

**Medium (5K-50K):**
→ **Plotly** (interactive) or **Graphviz** (static)

**Large (50K-500K):**
→ **Graphviz** (static) or **Gephi desktop** (interactive exploration)

**Massive (>500K):**
→ **Gephi** (Force Atlas 2) or **Graph database** (Neo4j + visualization layer)

### Priority 4: Team Context

**Scientific Python stack:**
→ **NetworkX** (integrates with Pandas, NumPy, SciPy)

**Web development team:**
→ **Plotly + Dash** (React-based, familiar patterns)

**DevOps/Documentation:**
→ **Graphviz** (scriptable, Git-friendly)

**Non-programmers as stakeholders:**
→ **Plotly** (browser-based, no install) or **PyVis** (standalone HTML)

## Use Case Patterns

### Pattern 1: Research Publication
**Workflow:**
1. Data collection → Pandas
2. Network analysis → NetworkX (centrality, communities)
3. Visualization → matplotlib (or Graphviz for hierarchical)
4. Export → PDF/SVG for LaTeX

**Tools:** NetworkX + matplotlib
**Time to first figure:** 30 minutes (after data cleaning)

### Pattern 2: Automated Documentation
**Workflow:**
1. Parse codebase/config → Python scripts
2. Extract dependencies → NetworkX or direct Graphviz
3. Generate diagrams → Graphviz DOT
4. Commit to repo → CI/CD auto-updates

**Tools:** Graphviz (+ NetworkX for complex parsing)
**Time to setup:** 2-3 hours (one-time investment)

### Pattern 3: Interactive Dashboard
**Workflow:**
1. Data pipeline → Pandas from database
2. Build graph → NetworkX
3. Compute layout → NetworkX (positions)
4. Render → Plotly
5. Deploy → Dash app

**Tools:** NetworkX + Plotly + Dash
**Time to MVP:** 1-2 days

### Pattern 4: Biological Analysis
**Workflow:**
1. Query pathway database → STRING, Reactome
2. Integrate omics → RNA-seq, proteomics
3. Import to Cytoscape → py4cytoscape
4. Enrichment analysis → ClueGO, ReactomeFI apps
5. Export figures → High-res PNG/PDF

**Tools:** py4cytoscape
**Time to publication figure:** 2-4 hours

### Pattern 5: Security Incident Response
**Workflow:**
1. Ingest logs → SIEM query
2. Build network → NetworkX (IPs, connections)
3. Detect anomalies → Graph algorithms
4. Visualize → Plotly (interactive) or PyVis (quick HTML)
5. Report → Screenshots + findings

**Tools:** NetworkX + Plotly (or PyVis for speed)
**Time to insights:** 15-30 minutes (during active incident)

## Common Mistakes

### Mistake 1: Choosing by Features Instead of Use Case
**Wrong:** "Plotly has more features, I'll use that"
**Right:** "My users need static PDFs → Graphviz or matplotlib"

### Mistake 2: Ignoring Domain Standards
**Wrong:** Using Plotly for biological pathways
**Right:** Using py4cytoscape (what reviewers expect)

### Mistake 3: Over-Engineering Quick Tasks
**Wrong:** Setting up Dash for one-time analysis
**Right:** Use PyVis for quick HTML demo

### Mistake 4: Under-Engineering Production Systems
**Wrong:** Using PyVis for production dashboard (vis.js unmaintained)
**Right:** Use Plotly + Dash for long-term stability

### Mistake 5: Fighting the Ecosystem
**Wrong:** Trying to script Gephi Toolkit from Python
**Right:** Export GEXF from Python, use Gephi desktop manually

## Validation Checklist

Before committing to a library, verify:

**✅ Output format matches need:**
- [ ] Static images → matplotlib, Graphviz
- [ ] Interactive web → Plotly, PyVis
- [ ] Desktop exploration → Gephi, Cytoscape

**✅ Scale is appropriate:**
- [ ] <5K nodes → Any tool
- [ ] 5K-50K → Plotly, Graphviz, NetworkX
- [ ] >50K → Graphviz, Gephi, graph databases

**✅ Integration with existing stack:**
- [ ] Scientific Python → NetworkX
- [ ] Web apps → Plotly + Dash
- [ ] Documentation → Graphviz
- [ ] Biological → py4cytoscape

**✅ Team skills match:**
- [ ] Python developers → Any Python library
- [ ] Non-programmers → Desktop tools (Gephi, Cytoscape)
- [ ] DevOps → Graphviz (CI/CD friendly)

**✅ Long-term maintenance:**
- [ ] Production → Avoid PyVis (vis.js unmaintained)
- [ ] Research → Prefer mature projects (NetworkX, Graphviz)
- [ ] Commercial → Consider Plotly Enterprise

## When to Combine Tools

**Common combinations:**

### NetworkX + [Visualization Library]
**Pattern:** Analyze with NetworkX, visualize with specialized tool
**Why:** NetworkX has best algorithms, visualization is separate concern

**Examples:**
- NetworkX + matplotlib (research)
- NetworkX + Plotly (dashboards)
- NetworkX + Graphviz (documentation)
- NetworkX + py4cytoscape (biology)

### Plotly for Web + Graphviz for Reports
**Pattern:** Interactive dashboard + static executive summary
**Why:** Different audiences, different needs

**Example:** Data science team explores in Plotly, management gets PDF from Graphviz

### PyVis for Prototyping → Plotly for Production
**Pattern:** Quick demo with PyVis, migrate to Plotly if successful
**Why:** PyVis is faster to set up, Plotly is more maintainable

**Migration path:** Save NetworkX graph, rebuild with Plotly

## Anti-Patterns (What NOT to Do)

### ❌ Using NetworkX matplotlib for final deliverables
**Problem:** Basic aesthetics, no interactivity
**Fix:** Use for exploration only, switch to Plotly/Graphviz for deliverables

### ❌ Manual diagram updates
**Problem:** Docs fall out of sync with reality
**Fix:** Automate with Graphviz in CI/CD pipeline

### ❌ Interactive dashboards for static reports
**Problem:** Overengineered, hard to maintain
**Fix:** Use matplotlib or Graphviz for static output

### ❌ Static images for exploratory analysis
**Problem:** Can't zoom, filter, explore
**Fix:** Use Plotly or PyVis for interactive exploration

### ❌ Desktop tools for automated pipelines
**Problem:** Require manual intervention
**Fix:** Use scriptable libraries (NetworkX, Graphviz)

## Bottom Line by Persona

**Researcher:** NetworkX + matplotlib (or Graphviz for hierarchical)
**Architect:** Graphviz (automated documentation)
**Data Scientist:** Plotly + Dash (stakeholder dashboards)
**Bioinformatician:** py4cytoscape (domain standard)
**Security Analyst:** NetworkX + Plotly (rapid incident response)

**General rule:** Let your use case (not library features) drive the decision.
