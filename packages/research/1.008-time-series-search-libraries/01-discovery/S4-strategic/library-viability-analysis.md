# Library Viability Analysis (5-Year Outlook)

## Methodology

Each library evaluated on three dimensions:
- **Technical**: Commit activity, test coverage, documentation quality
- **Community**: GitHub stars, StackOverflow presence, adoption signals
- **Organizational**: Funding, governance, bus factor

**Risk Rating**:
- 🟢 **Low Risk**: Production-ready, long-term viable
- 🟡 **Medium Risk**: Viable but monitor for changes
- 🔴 **High Risk**: Use with caution, have backup plan

---

## STUMPY: Matrix Profile Specialists

### Viability: 🟢 LOW RISK

**Technical Health** (as of Jan 2025):
- **Age**: 5+ years (first release 2019)
- **Commits**: 800+ commits, active monthly
- **Contributors**: 15+ contributors
- **Test coverage**: 95%+
- **Documentation**: Excellent (tutorials, API docs, use case guides)
- **Python support**: 3.8-3.12 (modern)

**Community Health**:
- **GitHub**: 3.3K stars, 320 forks
- **PyPI downloads**: 100K+/month
- **StackOverflow**: 150+ questions
- **Academic citations**: 500+ (Yeh et al. matrix profile papers)
- **Production deployments**: Finance (JPMorgan), healthcare (monitoring)

**Organizational**:
- **Backing**: UC Riverside research + community (no single commercial sponsor)
- **Governance**: Open governance, no CLA required
- **Bus factor**: Medium (3-4 core maintainers)
- **License**: BSD-3-Clause (permissive)
- **Roadmap**: Public roadmap, responsive to community

**5-Year Outlook**: **STABLE**
- Matrix profile is fundamental algorithm (not a trend)
- Academic foundation ensures longevity
- No commercial competitor (niche enough to avoid disruption)
- Risk: Bus factor if key maintainers leave academia

**TCO (5 years, medium scale)**:
- Implementation: $100K (Year 1)
- Maintenance: $20K/year × 4 = $80K
- Infrastructure: $10K/year × 5 = $50K
- **Total**: $230K

---

## sktime: Unified Time Series ML

### Viability: 🟢 LOW RISK

**Technical Health**:
- **Age**: 6+ years (first release 2019)
- **Commits**: 4000+ commits
- **Contributors**: 100+ contributors (highly collaborative)
- **Test coverage**: 90%+
- **Documentation**: Excellent (scikit-learn-style docs)
- **Python support**: 3.8-3.12

**Community Health**:
- **GitHub**: 7.8K stars, 1.3K forks
- **PyPI downloads**: 500K+/month (fastest growing TS library)
- **StackOverflow**: 300+ questions
- **Academic citations**: 200+ (framework paper + ROCKET paper)
- **Production**: Wide adoption (tech companies, research labs)

**Organizational**:
- **Backing**: Alan Turing Institute (UK national AI institute) + community
- **Governance**: NumFOCUS fiscal sponsorship (mature open source governance)
- **Bus factor**: Low risk (large contributor base)
- **License**: BSD-3-Clause
- **Roadmap**: Quarterly releases, transparent planning

**5-Year Outlook**: **GROWING**
- Scikit-learn API ensures long-term compatibility
- Turing Institute backing provides stability
- Active research community (new algorithms added regularly)
- NumFOCUS sponsorship = credible long-term project
- Risk: Complexity growth (40+ classifiers, may become bloated)

**TCO (5 years, medium scale)**:
- Implementation: $75K (Year 1)
- Maintenance: $15K/year × 4 = $60K
- Infrastructure: $5K/year × 5 = $25K (CPU-only)
- **Total**: $160K

---

## tslearn: DTW & Clustering Specialists

### Viability: 🟡 MEDIUM RISK

**Technical Health**:
- **Age**: 7+ years (first release 2017)
- **Commits**: 600+ commits
- **Contributors**: 20+ contributors
- **Test coverage**: 85%
- **Documentation**: Good (examples, API docs)
- **Python support**: 3.7-3.12

**Community Health**:
- **GitHub**: 2.9K stars, 650 forks
- **PyPI downloads**: 200K+/month
- **StackOverflow**: 200+ questions
- **Academic citations**: 100+ (DTW is well-established)
- **Production**: Finance, healthcare (DTW use cases)

**Organizational**:
- **Backing**: Research project (no major institution)
- **Governance**: Small core team (2-3 maintainers)
- **Bus factor**: Medium-high risk (dependent on key maintainers)
- **License**: BSD-2-Clause
- **Roadmap**: Ad-hoc releases

**5-Year Outlook**: **STABLE BUT NICHE**
- DTW is fundamental algorithm (won't disappear)
- Slower growth than sktime (competition for same use cases)
- Risk: If sktime improves DTW support, tslearn becomes redundant
- Risk: Maintenance may slow if key contributors move on
- Recommendation: Use for DTW-specific needs, but monitor sktime as alternative

**TCO (5 years, medium scale)**:
- Implementation: $60K (Year 1)
- Maintenance: $12K/year × 4 = $48K
- Infrastructure: $5K/year × 5 = $25K
- **Total**: $133K

---

## tsfresh: Feature Extraction Specialists

### Viability: 🟢 LOW RISK

**Technical Health**:
- **Age**: 8+ years (first release 2016)
- **Commits**: 500+ commits
- **Contributors**: 40+ contributors
- **Test coverage**: 90%+
- **Documentation**: Excellent (detailed feature catalog)
- **Python support**: 3.7-3.11

**Community Health**:
- **GitHub**: 8.4K stars, 1.2K forks
- **PyPI downloads**: 150K+/month
- **StackOverflow**: 250+ questions
- **Academic citations**: 400+ (feature extraction is canonical)
- **Production**: Wide adoption (manufacturing, IoT)

**Organizational**:
- **Backing**: Blue Yonder (commercial sponsor) + academic (TU Munich)
- **Governance**: Core team from Blue Yonder
- **Bus factor**: Low risk (commercial backing)
- **License**: MIT (permissive)
- **Roadmap**: Stable, incremental improvements

**5-Year Outlook**: **MATURE & STABLE**
- Commercial backing ensures maintenance
- 794 features are comprehensive (no major gaps)
- Mature codebase (few breaking changes)
- Risk: Newer methods (ROCKET) may reduce tsfresh usage
- Risk: Slow to adopt new Python features (conservative approach)
- Recommendation: Solid choice for feature extraction, but consider ROCKET for pure classification

**TCO (5 years, medium scale)**:
- Implementation: $50K (Year 1)
- Maintenance: $10K/year × 4 = $40K
- Infrastructure: $20K/year × 5 = $100K (compute-heavy feature extraction)
- **Total**: $190K

---

## dtaidistance: Performance-Focused DTW

### Viability: 🟡 MEDIUM RISK

**Technical Health**:
- **Age**: 6+ years (first release 2018)
- **Commits**: 200+ commits
- **Contributors**: 10+ contributors
- **Test coverage**: 80%
- **Documentation**: Good (C API integration examples)
- **Python support**: 3.7-3.11

**Community Health**:
- **GitHub**: 1.2K stars, 200 forks
- **PyPI downloads**: 50K+/month
- **StackOverflow**: 50+ questions
- **Academic citations**: 50+ (DTW is well-known)
- **Production**: Manufacturing, IoT (high-frequency needs)

**Organizational**:
- **Backing**: KU Leuven research project
- **Governance**: Small team (2-3 maintainers)
- **Bus factor**: Medium-high risk (academic project dependency)
- **License**: Apache 2.0
- **Roadmap**: Maintenance mode (stable, few new features)

**5-Year Outlook**: **MAINTENANCE MODE**
- DTW is mature algorithm (no new research needed)
- Library is "feature complete" (performance optimization done)
- Risk: If maintainers leave academia, project could stagnate
- Risk: Newer libraries (STUMPY, sktime) may absorb use cases
- Recommendation: Use if DTW speed is critical, but have migration plan to tslearn/sktime

**TCO (5 years, medium scale)**:
- Implementation: $40K (Year 1, simple API)
- Maintenance: $8K/year × 4 = $32K
- Infrastructure: $5K/year × 5 = $25K
- **Total**: $97K (lowest TCO)

---

## pyts: Imaging & Symbolic Methods

### Viability: 🔴 HIGH RISK

**Technical Health**:
- **Age**: 6+ years (first release 2018)
- **Commits**: 200+ commits
- **Contributors**: 10+ contributors
- **Test coverage**: 75%
- **Documentation**: Good (examples for each method)
- **Python support**: 3.7-3.10 (lagging)

**Community Health**:
- **GitHub**: 1.8K stars, 400 forks
- **PyPI downloads**: 30K+/month (lowest among libraries)
- **StackOverflow**: 30+ questions
- **Academic citations**: 80+ (imaging methods are niche)
- **Production**: Limited (mostly research)

**Organizational**:
- **Backing**: PhD research project
- **Governance**: Single primary maintainer
- **Bus factor**: HIGH RISK (single maintainer)
- **License**: BSD-3-Clause
- **Roadmap**: Infrequent releases

**5-Year Outlook**: **UNCERTAIN**
- Imaging methods (GAF, MTF) are niche (CNNs not dominant in TS classification)
- Single maintainer is bottleneck (slow issue response)
- ROCKET has largely replaced imaging methods for classification
- Risk: Abandonment if maintainer moves on
- Recommendation: Avoid for production, use sktime instead unless specific imaging need

**TCO (5 years, medium scale)**:
- Implementation: $50K (Year 1)
- Maintenance: $15K/year × 4 = $60K (higher risk = more monitoring)
- Infrastructure: $5K/year × 5 = $25K
- **Migration risk**: $50K (if library abandoned, rewrite to sktime)
- **Total**: $185K (high risk-adjusted TCO)

---

## Risk Summary Matrix

| Library | Technical | Community | Organizational | Overall Risk | 5-Year Outlook |
|---------|-----------|-----------|----------------|--------------|----------------|
| **STUMPY** | 🟢 Excellent | 🟢 Strong | 🟡 Academic | 🟢 **LOW** | Stable |
| **sktime** | 🟢 Excellent | 🟢 Very Strong | 🟢 Institutional | 🟢 **LOW** | Growing |
| **tslearn** | 🟡 Good | 🟡 Moderate | 🟡 Small Team | 🟡 **MEDIUM** | Niche |
| **tsfresh** | 🟢 Excellent | 🟢 Strong | 🟢 Commercial | 🟢 **LOW** | Mature |
| **dtaidistance** | 🟡 Good | 🟡 Moderate | 🟡 Academic | 🟡 **MEDIUM** | Maintenance |
| **pyts** | 🟡 Fair | 🔴 Weak | 🔴 Single Maintainer | 🔴 **HIGH** | Uncertain |

## Strategic Recommendations

### Tier 1: Safe Long-Term Bets
- **sktime**: Best overall choice for classification/regression (Turing Institute backing)
- **STUMPY**: Best for unsupervised pattern discovery (strong academic foundation)
- **tsfresh**: Best for feature extraction (commercial backing)

### Tier 2: Use with Monitoring
- **tslearn**: Good for DTW-specific needs, but watch sktime's DTW improvements
- **dtaidistance**: Good for performance-critical DTW, but have migration plan

### Tier 3: Avoid for Production
- **pyts**: Too high bus factor risk, use sktime instead unless imaging methods critical

### Migration Strategy

If dependent on medium/high risk libraries:
1. **Quarterly health check**: Monitor GitHub activity, maintainer status
2. **Abstraction layer**: Wrap library calls (easier to swap implementations)
3. **Alternative POC**: Have proof-of-concept with safer alternative (e.g., tslearn → sktime)
4. **Trigger threshold**: If no commits in 6 months or maintainer announces departure, execute migration
