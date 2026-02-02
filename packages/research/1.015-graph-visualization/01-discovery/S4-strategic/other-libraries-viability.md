# Other Libraries - Strategic Viability Assessment

## PyVis

### Verdict: ⚠️ **CAUTION** - Maintenance risk due to vis.js
**Risk Level:** Medium-High
**3-Year Outlook:** Uncertain (dependent on vis.js revival or replacement)

### Key Risk: vis.js Abandonment
- **vis.js status:** Community-maintained since 2021, no active core development
- **Security:** No recent security patches (CVE risk)
- **PyVis dependency:** Thin wrapper around vis.js (tied to its fate)

### Ecosystem Health
- **Downloads:** 1.5M/month (moderate adoption)
- **Maintenance:** Slow (updates every 3-6 months)
- **Community:** Small (1K GitHub stars)
- **Corporate backing:** None

### Strategic Recommendation
**Use case:** ✅ Internal tools, prototypes, education
**Avoid:** ❌ Production applications, client-facing dashboards, long-term projects

**Mitigation:** Plan migration path to Plotly or Cytoscape.js if PyVis stagnates.

**3-Year Outlook:** Likely to be replaced by Plotly or custom Cytoscape.js for serious projects. Acceptable for short-term use only.

---

## Graphviz

### Verdict: ✅ **LEGACY STABLE** - Ancient but reliable
**Risk Level:** Very Low
**3-Year Outlook:** Stable (30+ years of history)

### Ecosystem Health
- **Heritage:** AT&T Research (1991), now open-source
- **Adoption:** Embedded in countless tools (Doxygen, Sphinx, PlantUML)
- **Python bindings:** 25M downloads/month (actively maintained)
- **Community:** Small but dedicated

### Strategic Strengths
- **Proven:** 30+ years in production systems
- **Standards-based:** DOT language is a de facto standard
- **Minimal changes:** API stable for decades
- **Wide integration:** Ecosystem momentum protects it

### Strategic Risks
- **C dependency:** System installation required (Docker complexity)
- **No interactivity:** Static output only (web trends favor interactive)
- **Learning curve:** DOT language is niche skill

### Long-Term Outlook
**Stability:** Excellent (survived multiple technology shifts)
**Growth:** Flat (not growing, but not declining)
**Replacement risk:** Low (too embedded in existing infrastructure)

**3-Year Outlook:** Safe bet for documentation, unlikely to change significantly. May lose ground to interactive tools for new projects, but existing use cases secure.

**Recommendation:** Commit with confidence for documentation, automated diagram generation. Avoid for interactive visualization.

---

## py4cytoscape

### Verdict: ✅ **NICHE SPECIALIST** - Safe for biology, risky outside
**Risk Level:** Low (for bioinformatics), High (for general use)
**3-Year Outlook:** Stable within bioinformatics domain

### Ecosystem Health
- **Cytoscape backing:** Cytoscape Consortium, NRNB funding
- **Biological community:** Strong (bioinformatics standard)
- **Python wrapper:** Active development (20K downloads/month)
- **General adoption:** Very low (domain-specific)

### Strategic Strengths
- **Domain dominance:** THE tool for biological networks
- **Funding:** NIH grants, academic support
- **App ecosystem:** 1000+ Cytoscape apps (pathway enrichment, etc.)
- **Publication acceptance:** Reviewers expect Cytoscape figures

### Strategic Risks
- **Desktop dependency:** Requires Cytoscape running (not cloud-native)
- **Narrow focus:** Biological only (general graphs better served elsewhere)
- **Skill availability:** Bioinformaticians only (hiring constraint outside domain)

### Long-Term Outlook
**Within biology:** Excellent (entrenched, funded, peer-accepted)
**Outside biology:** Poor (better alternatives exist)

**3-Year Outlook:** Will remain biology standard. Growth in bioinformatics, irrelevant elsewhere.

**Recommendation:**
- **Bioinformatics:** Commit with confidence (safe long-term)
- **Other domains:** Avoid (Plotly, NetworkX, Graphviz better choices)

---

## Gephi (Desktop)

### Verdict: ⚠️ **DESKTOP TOOL** - Excellent for exploration, poor for automation
**Risk Level:** Medium
**3-Year Outlook:** Stable for desktop use, Python integration unlikely to improve

### Ecosystem Health
- **Consortium backing:** Gephi Consortium (academic/corporate members)
- **Adoption:** 5.5K GitHub stars, widely used in social network analysis
- **Release cadence:** 1-2 releases/year
- **Python integration:** Community wrappers only (no official support)

### Strategic Strengths
- **Force Atlas 2:** Best-in-class layout for large graphs
- **Proven:** 15+ years, used in research, journalism, education
- **Plugin ecosystem:** 100+ plugins for specialized analysis
- **Massive scale:** Tested on 1M+ node graphs

### Strategic Risks
- **Python gap:** No official Python API (integration is hacky)
- **Desktop requirement:** Cannot deploy as web service
- **Manual workflow:** Automation is difficult
- **Java dependency:** JVM requirement (heavy)

### Python Integration Reality
**File-based workflow only:** Export GEXF from Python → manual Gephi → export images

**Programmatic control:** Fragmented community wrappers, not production-ready

### Long-Term Outlook
**Desktop tool:** Stable and excellent
**Python automation:** No improvement expected (not a priority for Gephi team)

**3-Year Outlook:** Remain a desktop exploration tool. Python users should treat it as manual supplement, not programmatic library.

**Recommendation:**
- **Exploratory analysis (>100K nodes):** Use Gephi desktop, export from Python
- **Automated pipelines:** Avoid (use Graphviz or NetworkX instead)
- **Web applications:** Not viable (desktop-only)

---

## Summary Comparison

| Library | Risk Level | 3-Year Outlook | Best For |
|---------|-----------|----------------|----------|
| **NetworkX** | Very Low | ✅ Stable, growing | Algorithms, research, Python ecosystem |
| **Plotly** | Low-Medium | ✅ Stable (commercial) | Production dashboards, interactivity |
| **PyVis** | Medium-High | ⚠️ Uncertain (vis.js) | Prototypes only, plan migration |
| **Graphviz** | Very Low | ✅ Legacy stable | Documentation, hierarchical diagrams |
| **py4cytoscape** | Low (biology) | ✅ Safe (niche) | Biological networks only |
| **Gephi** | Medium | ⚠️ Desktop-only | Large graph exploration (manual) |

## Strategic Recommendations by Risk Tolerance

### Conservative (Minimize Risk)
1. **NetworkX** - Safest bet for analysis
2. **Graphviz** - Safest bet for static diagrams
3. **Plotly** - Safest bet for interactivity (with enterprise support)

**Avoid:** PyVis (production), Gephi (automation)

### Moderate (Accept Some Risk)
1. **NetworkX + Plotly** - Analysis + dashboards
2. **py4cytoscape** - If biological domain
3. **PyVis** - For prototypes (plan migration)

**Avoid:** Gephi programmatic control (too fragile)

### Aggressive (Early Adoption)
- None applicable - all libraries are mature or declining
- For cutting-edge, consider emerging libraries (e.g., Rust-based graph viz)

## Bottom Line

**Safest 3-5 year bets:**
1. NetworkX (analysis foundation)
2. Graphviz (documentation automation)
3. Plotly + Dash (interactive dashboards, with enterprise support)

**Domain specialists (safe within niche):**
- py4cytoscape (bioinformatics)

**Use with caution:**
- PyVis (maintenance risk, plan migration)
- Gephi (desktop-only, not automatable)

**General rule:** Favor foundation-backed (NetworkX) or commercially-backed (Plotly) over community-only projects (PyVis) for long-term commitments.
