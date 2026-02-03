# SALib - Strategic Maturity Assessment

**Library**: SALib (Sensitivity Analysis Library)
**Domain**: Global sensitivity analysis methods
**Assessment Date**: October 2025
**Strategic Outlook**: MEDIUM CONFIDENCE - Niche leader with succession risk

## Executive Summary

**Strategic Recommendation**: BEST-IN-CLASS for sensitivity analysis, but with medium-term risks
**Viability Horizon**: 3-5 years (moderate confidence)
**Risk Level**: MEDIUM (small maintainer base, academic funding dependency)
**Maintenance Status**: Active but resource-constrained

SALib is the dominant Python library for global sensitivity analysis with no viable alternative. However, it shows classic academic software risks: small maintainer base, grant-dependent funding, and potential succession challenges.

## Governance Health: FAIR

### Institutional Backing
- **Organization**: Independent open source project (no foundation support)
- **Academic roots**: Developed by researchers at universities (original: Imperial College London)
- **No formal sponsorship**: No NumFOCUS, no corporate backing, no foundation
- **Grant support**: Some development funded by research grants (sporadic)
- **Bus factor**: Low (~3-5 active maintainers)

### Governance Structure
- **Informal governance**: No formal steering council or governance document
- **Core maintainers**: Small group of academic researchers
- **Decision-making**: Informal consensus among maintainers
- **Transparency**: GitHub-based development, but no formal RFC/PEP process

### Financial Sustainability
- **Funding model**: Volunteer labor + occasional research grants
- **No sustainable revenue**: No commercial support offerings, no donations infrastructure
- **Academic dependency**: Maintainers work on SALib as side project to research
- **Vulnerability**: If maintainers change institutions or research focus, project risks abandonment

**Governance Score**: 4/10 (classic academic software governance risks)

## Maintenance Trajectory: ACTIVE BUT CONSTRAINED

### Historical Activity (2020-2025)
- **Commit frequency**: 100-200 commits/year (modest, but consistent)
- **Release cadence**: 1-2 releases/year (sporadic timing)
- **Development mode**: Maintenance + incremental feature additions
- **Trend**: Stable activity, no major growth or decline

### Recent Developments
- **v1.4 (2022)**: Added PAWN method, improved documentation
- **v1.5 (2024)**: Performance improvements, better NumPy integration
- **Python 3.x support**: Maintains compatibility with modern Python
- **Dependency updates**: Keeps up with NumPy/SciPy evolution

### API Stability
- **Breaking changes**: Rare (mostly additive development)
- **Semver adherence**: Informal (1.x series maintained for years)
- **Deprecation process**: Limited (small user base allows direct changes)
- **Backward compatibility**: Generally maintained, but no formal guarantees

### Ecosystem Adaptation
- **Python version support**: 3.8-3.13 (reasonable support window)
- **NumPy/SciPy compatibility**: Tracks major versions well
- **Platform support**: Pure Python (excellent portability)
- **Modern features**: Limited type hints, no async, basic documentation

**Maintenance Score**: 6/10 (active, but resource-constrained)

## Community Health: MODEST

### Contributor Base
- **Active contributors**: 5-10 contributors/year
- **Total contributors**: ~50 total over project lifetime
- **Bus factor**: 3 (concerning - small core team)
- **Geographic diversity**: Moderate (US, UK, Europe)
- **Organizational diversity**: Low (mostly academic researchers)

### User Community
- **GitHub stars**: ~900 (modest for specialized library)
- **Issue response time**: Variable (days to weeks, depends on maintainer availability)
- **Stack Overflow**: Limited activity (~50 questions tagged SALib)
- **User forum**: GitHub Issues is primary support venue
- **Download statistics**: 60K-100K downloads/week (solid niche adoption)

### Educational Ecosystem
- **Official documentation**: Good (user guide, API reference, examples)
- **Third-party tutorials**: Limited (mostly academic papers using SALib)
- **Books**: Mentioned in UQ/sensitivity analysis textbooks
- **University courses**: Used in specialized UQ courses (not widespread)

### Community Engagement
- **Conferences**: Occasional SciPy conference talks, UQ workshops
- **Mailing list**: None (GitHub only)
- **Chat platform**: None (GitHub Discussions only)
- **Development sprints**: None

**Community Score**: 5/10 (small but engaged niche community)

## Academic Adoption: STRONG (NICHE)

### Research Validation
- **Citations**: 2,000+ citations in academic literature (strong for niche)
- **Discipline coverage**: Engineering, environmental science, economics, epidemiology
- **Reproducibility**: Widely used for reproducible sensitivity analysis
- **Method validation**: Implements peer-reviewed algorithms (Sobol, Morris, FAST)

### Method Implementation Quality
- **Peer-reviewed methods**: All major methods reference academic papers
- **Test suite**: Good coverage with validation against reference implementations
- **Numerical accuracy**: Validated against published results
- **Algorithm correctness**: High confidence (academic scrutiny)

### Academic Community
- **Developer affiliations**: Universities (Imperial College, TU Delft, US universities)
- **Grant support**: Occasional NSF, EU grants for method development
- **Publication standard**: Cited in sensitivity analysis methodology papers
- **Research tool**: Standard tool for SA in many engineering disciplines

**Academic Score**: 8/10 (strong in niche, but niche is small)

## Commercial Adoption: LIMITED

### Industry Use Cases
- **Consulting firms**: Used in engineering consulting (aerospace, automotive)
- **Government agencies**: Environmental modeling, risk assessment
- **Energy sector**: Uncertainty quantification in energy systems
- **Pharmaceuticals**: Limited use in drug development sensitivity studies

### Commercial Support
- **No commercial offerings**: No Tidelift, no paid support, no consultancies
- **Self-service only**: Users must solve problems themselves or file issues
- **Consulting**: Individual maintainers may offer consulting (informal)

### Risk Management
- **CVE tracking**: No formal security process
- **Security team**: None (small project, low attack surface)
- **Vulnerability response**: Informal (would depend on maintainer availability)
- **SBOM**: Not provided

### Production Deployment
- **Production use**: Used in analysis pipelines, not real-time systems
- **Mission-critical**: Rarely (mostly research and one-off studies)
- **Regulatory**: Acceptable for engineering analysis (no formal validation)

**Commercial Score**: 3/10 (limited commercial ecosystem)

## License and Dependencies: GOOD

### License
- **Type**: MIT (permissive)
- **Commercial use**: Unrestricted
- **Patent grants**: No patent concerns
- **Redistribution**: Free to use, modify, distribute

### Dependency Footprint
- **Core dependencies**: NumPy, SciPy, matplotlib, pandas (all standard)
- **Optional dependencies**: None
- **Supply chain risk**: LOW (depends on stable ecosystem libraries)
- **Portability**: Pure Python (excellent - works everywhere)

### Packaging Quality
- **PyPI**: Available with source distribution (no compiled components)
- **conda-forge**: Available in Anaconda ecosystem
- **Installation**: Simple `pip install SALib` (no compilation)
- **System packages**: Not packaged in Debian/Ubuntu (too specialized)

**License Score**: 8/10 (good licensing, minimal dependencies)

## Strategic Risk Assessment

### Risk: Abandonment (MEDIUM)
- **Probability**: 30% (maintainers could leave academia, change research focus)
- **Mitigation**: Methods are well-documented, forkable, pure Python
- **Impact if occurs**: Medium (no direct alternative, but could be forked)
- **User action**: Monitor GitHub activity, maintain internal fork if critical

### Risk: Fragmentation (LOW)
- **Probability**: 10% (small community unlikely to fragment)
- **Mitigation**: Simple codebase, clear method implementations
- **Impact if occurs**: Low (one fork would likely dominate)
- **User action**: None required

### Risk: Breaking Changes (MEDIUM)
- **Probability**: 20% (informal governance could allow breaking changes)
- **Mitigation**: Pin versions in production, maintain internal compatibility layer
- **Impact if occurs**: Medium (migration burden, but library is simple)
- **User action**: Pin SALib version, test updates before deploying

### Risk: Security Vulnerabilities (LOW)
- **Probability**: 5% (pure Python, minimal attack surface, analysis-only use)
- **Mitigation**: No network code, no privileged operations
- **Impact if occurs**: Low (would likely be in dependencies, not SALib itself)
- **User action**: Keep dependencies updated

### Risk: Ecosystem Displacement (MEDIUM)
- **Probability**: 25% (scipy.stats could absorb SA methods in 3-5 years)
- **Mitigation**: SciPy has shown interest in SA (would likely maintain API compatibility)
- **Impact if occurs**: Low-Medium (migration would be straightforward)
- **User action**: Monitor SciPy development for SA additions

**Overall Risk Level**: MEDIUM (viable for 3-5 years, longer-term uncertain)

## User Type Suitability

### Academic Researchers: HIGHLY SUITABLE
- **Strengths**: Peer-reviewed methods, reproducibility, publication acceptance
- **Weaknesses**: Limited commercial support if issues arise
- **Recommendation**: Best available tool for SA research
- **Risk**: Medium (abandonment could affect reproducibility)
- **Mitigation**: Cite specific version, maintain code archive

### Startup CTOs: SUITABLE WITH CAUTION
- **Strengths**: Free, easy to integrate, sufficient for most SA needs
- **Weaknesses**: No commercial support, small maintainer base
- **Recommendation**: Use for analysis, but have contingency plan
- **Risk**: Medium (no support escalation path)
- **Mitigation**: Build internal SA expertise, maintain fork option

### Enterprise Architects: USE WITH CAUTION
- **Strengths**: Best available SA library, permissive license
- **Weaknesses**: No commercial support, no SLA, small maintainer base
- **Recommendation**: Acceptable for non-critical analysis, risky for critical systems
- **Risk**: Medium-High (no support guarantees, succession risk)
- **Mitigation**: Maintain internal fork, budget for re-implementation if abandoned

### Data Scientists: SUITABLE
- **Strengths**: Easy to use, integrates with NumPy/pandas workflow
- **Weaknesses**: Limited learning resources compared to mainstream tools
- **Recommendation**: Use for sensitivity analysis tasks
- **Risk**: Low-Medium (exploratory work can tolerate library changes)
- **Mitigation**: None required (can switch tools if needed)

### Hobbyists/Learners: SUITABLE
- **Strengths**: Good documentation, clear examples, easy installation
- **Weaknesses**: Small community, limited Stack Overflow help
- **Recommendation**: Good for learning SA concepts
- **Risk**: Low (learning investment is small)
- **Mitigation**: None required

## Long-Term Outlook (2025-2030)

### Likely Scenarios

**Scenario 1: Status Quo (40% probability)**
- SALib continues with small maintainer base
- Slow feature development, maintenance-mode primarily
- Continues to serve niche SA community
- **User strategy**: Continue using, monitor for signs of abandonment

**Scenario 2: Ecosystem Absorption (30% probability)**
- SciPy or statsmodels absorbs key SA methods
- SALib becomes legacy wrapper or is deprecated
- Community migrates to scipy.stats.sensitivity
- **User strategy**: Monitor SciPy development, prepare for migration

**Scenario 3: Academic Rejuvenation (20% probability)**
- New research grant brings additional maintainers
- Expanded feature set, improved documentation
- Grows beyond niche into mainstream
- **User strategy**: Benefit from improvements, continue use

**Scenario 4: Abandonment (10% probability)**
- Maintainers leave, project goes dormant
- Community fork emerges or users migrate to alternatives
- **User strategy**: Maintain internal fork or switch to emerging alternative

### Monitoring Indicators
- **Green flags**: New contributors, regular releases, growing download stats
- **Yellow flags**: Slowing commit frequency, delayed issue responses, maintainer turnover
- **Red flags**: >6 months without commit, unresponsive maintainers, growing unresolved issues

### Recommended Monitoring Frequency
- **Quarterly review**: Check GitHub activity, release notes
- **Annual assessment**: Evaluate whether SALib is still best option vs. alternatives
- **Action trigger**: If >6 months without activity, begin contingency planning

## Alternatives and Contingencies

### Current Alternatives (None Ideal)
- **OpenTURNS**: Has SA methods, but heavyweight and non-Pythonic
- **chaospy**: Has analytical Sobol via PCE, but limited to smooth models
- **DIY implementation**: Sobol/Morris are simple enough to implement from papers
- **R packages**: sensitivity, sensobol (requires R bridge)

### Future Alternatives (Possible)
- **scipy.stats.sensitivity**: SciPy could add SA module (would be ideal long-term)
- **statsmodels**: Could add SA methods (similar scope)
- **Emerging libraries**: New academic projects may emerge

### Contingency Strategy
1. **Pin version**: Use SALib==X.Y.Z in requirements
2. **Maintain awareness**: Monitor for SciPy SA development
3. **Internal expertise**: Understand SA algorithms, not just SALib API
4. **Fork readiness**: For critical applications, maintain internal fork capability
5. **Gradual migration**: If SciPy adds SA, migrate gradually over 1-2 years

## Strategic Recommendation

**SALib is the best available tool for sensitivity analysis, but with medium-term risks.**

**Recommendation by User Type**:

- **Academics**: Use SALib (best option, cite version for reproducibility)
- **Startups**: Use SALib (sufficient for MVP, monitor for alternatives)
- **Enterprises**: Use with caution (acceptable for analysis, risky for critical paths)
- **Data Scientists**: Use SALib (good for exploratory SA)
- **Hobbyists**: Use SALib (good learning tool)

**Confidence Level**: 6/10 (best current option, but strategic risks)

**Time Horizon**: 3-5 years (likely viable, but uncertain beyond)

**Strategic Position**: NICHE LEADER with succession risk

**Decision Rule**:
- **Use SALib if**: You need sensitivity analysis and accept medium-term risk
- **Avoid SALib if**: You need guaranteed 5+ year support for mission-critical systems
- **Monitor for**: SciPy sensitivity analysis additions (would be superior long-term choice)

**Future-Proofing Strategy**:
1. Use SALib today (best option)
2. Build internal SA expertise (not just tool knowledge)
3. Monitor SciPy development quarterly
4. Be prepared to migrate if better-supported alternative emerges
5. For critical systems, budget for potential re-implementation

## Comparison to Alternatives

**vs. OpenTURNS**:
- SALib: Easier, Pythonic, narrower scope, smaller community
- OpenTURNS: Industrial backing, comprehensive, steeper learning curve

**vs. DIY implementation**:
- SALib: Validated, tested, documented, maintained (currently)
- DIY: Full control, no dependency risk, implementation burden

**vs. scipy.stats (hypothetical future)**:
- SALib: Available now, specialized, uncertain future
- scipy.stats.sensitivity: Not yet exists, would be superior if developed

**Strategic Positioning**: SALib is a **calculated risk** - best current tool with medium-term uncertainty. Appropriate for users who need SA now and can adapt if the landscape changes.
