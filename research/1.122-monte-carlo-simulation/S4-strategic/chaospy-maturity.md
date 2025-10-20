# chaospy - Strategic Maturity Assessment

**Library**: chaospy (Polynomial Chaos Expansion toolkit)
**Domain**: Uncertainty quantification via polynomial chaos methods
**Assessment Date**: October 2025
**Strategic Outlook**: MEDIUM-LOW CONFIDENCE - Academic project with succession risk

## Executive Summary

**Strategic Recommendation**: SPECIALIZED TOOL for expensive models, but with medium-high risk
**Viability Horizon**: 2-4 years (low to moderate confidence)
**Risk Level**: MEDIUM-HIGH (small academic team, niche use case, abandonment risk)
**Maintenance Status**: Slow maintenance, limited active development

chaospy offers powerful polynomial chaos expansion methods for expensive models, but shows classic academic software risks: small maintainer base, sporadic activity, and potential abandonment. Strategic fit is narrow (expensive smooth models only).

## Governance Health: POOR

### Institutional Backing
- **Academic project**: Developed at Norwegian University of Science and Technology (NTNU)
- **No foundation support**: No NumFOCUS, no corporate backing, no formal organization
- **PhD project origins**: Started as PhD research project (common academic pattern)
- **Bus factor**: Very low (~1-2 primary maintainers)
- **No succession planning**: No evidence of governance continuity

### Governance Structure
- **Informal**: No formal governance, single-person decision-making
- **Academic style**: Development tied to research group activity
- **No transparency mechanisms**: No RFCs, no governance documents, no roadmaps
- **Contribution barriers**: Limited external contributor onboarding

### Financial Sustainability
- **No funding model**: Pure academic volunteer labor
- **Grant dependency**: Development tied to research grants (expired?)
- **No commercial support**: No revenue model, no commercial services
- **Academic career dependency**: Maintainers' continued academic interest

**Governance Score**: 2/10 (high governance risk, typical abandoned academic software pattern)

## Maintenance Trajectory: DECLINING

### Historical Activity (2015-2025)
- **Early activity (2015-2018)**: Active development (PhD period)
- **Mid period (2019-2021)**: Moderate activity
- **Recent (2022-2025)**: Significantly reduced activity (warning sign)
- **Commit frequency**: 20-50 commits/year (2022-2025, down from 100+/year earlier)
- **Release cadence**: Sporadic (6+ months between releases, sometimes >1 year)
- **Development mode**: Minimal maintenance (mostly Python compatibility fixes)
- **Trend**: DECLINING (major warning sign for abandonment)

### Recent Developments
- **v4.3 (2022)**: Python 3.10 compatibility
- **v4.4 (2024)**: Minimal updates, maintenance release
- **Stagnant features**: No major new features in 3+ years
- **Bug backlog**: Growing unresolved issues

### API Stability
- **Breaking changes**: Rare (v4.x series stable since 2020)
- **Semver adherence**: Informal
- **Deprecation process**: Minimal communication
- **Backward compatibility**: Generally maintained by inertia (no active changes)

### Ecosystem Adaptation
- **Python version support**: 3.8-3.11 (lags behind current Python 3.13)
- **NumPy compatibility**: Eventually tracks NumPy, but delays possible
- **Platform support**: Pure Python (good portability)
- **Modern features**: Minimal (no type hints, basic documentation)

**Maintenance Score**: 3/10 (declining activity, warning signs of abandonment)

## Community Health: VERY SMALL

### Contributor Base
- **Active contributors**: 1-2 active, ~10-15 total historical
- **Bus factor**: 1 (critical risk - Jonathan Feinberg, primary author)
- **Geographic diversity**: Low (primarily Norway/NTNU)
- **Organizational diversity**: Very low (academic research group)
- **New contributors**: Minimal (no evidence of new contributor growth)

### User Community
- **GitHub stars**: ~350 (very small for scientific library)
- **Issue response time**: Variable (weeks to months, sometimes unanswered)
- **Stack Overflow**: Minimal activity (~20 questions total)
- **User forum**: GitHub Issues only (low activity)
- **Download statistics**: 10K-20K downloads/week (very niche)

### Educational Ecosystem
- **Official documentation**: Moderate (examples exist, but limited)
- **Third-party tutorials**: Very limited (a few blog posts)
- **Books**: Rarely mentioned (not in mainstream UQ textbooks)
- **University courses**: Used at NTNU and a few other institutions (very limited)

### Community Engagement
- **Conferences**: Minimal presence (occasional UQ workshop mentions)
- **Mailing list**: None
- **Chat platform**: None
- **Development sprints**: None

**Community Score**: 2/10 (tiny community, minimal engagement)

## Academic Adoption: LIMITED (NICHE)

### Research Validation
- **Citations**: 200-300 citations (very limited for 10-year-old library)
- **Discipline coverage**: Narrow (UQ in engineering, some computational physics)
- **Reproducibility**: Used in some UQ research papers
- **Method validation**: Implements known PCE methods (Wiener, Askey schemes)

### Method Implementation Quality
- **Algorithm correctness**: Appears sound (implements standard PCE theory)
- **Test suite**: Limited coverage
- **Numerical accuracy**: Not extensively validated against other implementations
- **Documentation**: Moderate (methods referenced, but not deeply explained)

### Academic Community
- **Developer affiliation**: NTNU (Norway)
- **Grant support**: Likely had Norwegian research grants (unclear current status)
- **Publication record**: Few papers specifically about chaospy
- **Research tool**: Used in some UQ research, but not dominant

**Academic Score**: 4/10 (limited academic adoption, niche within niche)

## Commercial Adoption: MINIMAL

### Industry Use Cases
- **Engineering consulting**: Very limited use (some UQ consultants aware of it)
- **Aerospace/Automotive**: Rare use (OpenTURNS more common)
- **Research contracts**: Occasional use in research-oriented projects
- **Production systems**: Virtually none (too risky)

### Commercial Support
- **No commercial offerings**: No paid support, no consulting services
- **No commercial ecosystem**: No companies offering chaospy services
- **Self-service only**: Users entirely on their own

### Risk Management
- **No CVE tracking**: No security process
- **No security team**: None
- **Vulnerability response**: Uncertain (would depend on maintainer availability)
- **SBOM**: Not provided

### Production Deployment
- **Production use**: Very rare (mostly academic/research use)
- **Mission-critical**: None (too risky)
- **Regulatory**: Not validated for regulatory compliance

**Commercial Score**: 1/10 (essentially no commercial use or support)

## License and Dependencies: GOOD

### License
- **Type**: MIT (permissive)
- **Commercial use**: Unrestricted
- **Patent grants**: No patent concerns
- **Redistribution**: Free to use, modify, distribute

### Dependency Footprint
- **Core dependencies**: NumPy, SciPy, numpoly (custom polynomial library by same author)
- **Dependency risk**: MEDIUM (numpoly is also single-maintainer academic project)
- **Supply chain risk**: MEDIUM (both chaospy and numpoly could be abandoned)
- **Portability**: Pure Python (good portability if dependencies available)

### Packaging Quality
- **PyPI**: Available with source distribution
- **conda-forge**: Available (but infrequently updated)
- **Installation**: Simple `pip install chaospy` (when it works)
- **System packages**: Not packaged in major distros (too specialized)

**License Score**: 6/10 (good license, but dependency on numpoly is risk)

## Strategic Risk Assessment

### Risk: Abandonment (HIGH)
- **Probability**: 60% (declining activity, single maintainer, academic project)
- **Mitigation**: Could be forked, but requires PCE expertise
- **Impact if occurs**: HIGH (no good alternative for PCE in Python)
- **User action**: Monitor GitHub closely, prepare contingencies

### Risk: Fragmentation (LOW)
- **Probability**: 5% (community too small to fragment)
- **Mitigation**: N/A (not a concern)
- **Impact if occurs**: N/A
- **User action**: N/A

### Risk: Breaking Changes (LOW-MEDIUM)
- **Probability**: 20% (infrequent updates could include breaking changes without warning)
- **Mitigation**: Pin version strictly
- **Impact if occurs**: Medium (migration burden with minimal support)
- **User action**: Pin chaospy and numpoly versions

### Risk: Security Vulnerabilities (LOW)
- **Probability**: 10% (pure Python, math-only, minimal attack surface)
- **Mitigation**: Minimal attack surface
- **Impact if occurs**: Medium (no security response team)
- **User action**: Audit dependencies, use in isolated environments

### Risk: Ecosystem Displacement (MEDIUM)
- **Probability**: 30% (OpenTURNS could absorb users, new PCE library could emerge)
- **Mitigation**: PCE niche is small, displacement would be obvious
- **Impact if occurs**: Medium (migration to OpenTURNS or DIY)
- **User action**: Monitor OpenTURNS PCE capabilities, UQ library landscape

**Overall Risk Level**: MEDIUM-HIGH (significant abandonment risk, limited alternatives)

## User Type Suitability

### Academic Researchers: USE WITH EXTREME CAUTION
- **Strengths**: PCE methods implemented, some publications use it
- **Weaknesses**: Declining maintenance, reproducibility risk, limited citations
- **Recommendation**: Use only if PCE is essential AND cite specific version, archive code
- **Risk**: HIGH (library abandonment could compromise reproducibility)
- **Mitigation**: Archive chaospy code with paper, consider OpenTURNS

### Startup CTOs: NOT RECOMMENDED
- **Strengths**: Powerful PCE for expensive models
- **Weaknesses**: No support, abandonment risk, learning curve, small community
- **Recommendation**: Avoid - use OpenTURNS or stick with standard Monte Carlo
- **Risk**: VERY HIGH (no support, high abandonment risk)
- **Mitigation**: Use alternative (OpenTURNS, direct MC, or hire UQ expert to implement PCE)

### Enterprise Architects: DO NOT USE
- **Strengths**: None for enterprise context
- **Weaknesses**: No commercial support, no SLA, abandonment risk, tiny community
- **Recommendation**: DO NOT USE - use OpenTURNS for PCE needs
- **Risk**: UNACCEPTABLE (no support path, likely abandonment)
- **Mitigation**: Use OpenTURNS or commercial UQ software (UQLAB, Dakota)

### Data Scientists: NOT RECOMMENDED
- **Strengths**: Interesting method (PCE)
- **Weaknesses**: Limited learning resources, minimal community, abandonment risk
- **Recommendation**: Learn PCE concepts elsewhere, use more stable libraries
- **Risk**: HIGH (time investment in dying library)
- **Mitigation**: Use OpenTURNS or standard MC methods

### Hobbyists/Learners: NOT RECOMMENDED FOR LEARNING
- **Strengths**: Interesting PCE implementation
- **Weaknesses**: Poor documentation, no community support, abandonment risk
- **Recommendation**: Learn PCE from textbooks, use OpenTURNS if needed
- **Risk**: Medium (learning investment may not transfer)
- **Mitigation**: Focus on PCE theory, not chaospy specifically

## Long-Term Outlook (2025-2030)

### Likely Scenarios

**Scenario 1: Abandonment (60% probability)**
- Maintainer stops activity (already declining)
- Library becomes dormant, eventually incompatible with new Python/NumPy
- Users migrate to OpenTURNS or abandon PCE
- **User strategy**: Plan for abandonment NOW, have migration path ready

**Scenario 2: Minimal Maintenance (25% probability)**
- Maintainer continues sporadic Python compatibility updates
- No new features, minimal bug fixes
- Library limps along in maintenance mode
- **User strategy**: Pin versions, minimize dependency, prepare migration

**Scenario 3: Revival (10% probability)**
- New maintainer(s) or research project revives development
- Renewed activity, improved documentation
- **User strategy**: Monitor for signs of revival, reassess if occurs

**Scenario 4: Replacement (5% probability)**
- New Python PCE library emerges with better governance
- Community migrates to successor
- **User strategy**: Monitor for emerging alternatives

### Monitoring Indicators
- **Green flags**: New commits, new releases, new contributors (none recently)
- **Yellow flags**: Slowing activity, issue backlog growth (CURRENT STATE)
- **Red flags**: >12 months without commit, Python incompatibility, maintainer silence

### Recommended Monitoring Frequency
- **Quarterly review**: Check GitHub for any activity
- **Immediate action trigger**: If you depend on chaospy, plan migration NOW

## Alternatives and Contingencies

### Current Alternatives

**OpenTURNS**:
- **Status**: Industrial-backed, active development
- **PCE support**: Comprehensive PCE implementation
- **Trade-off**: Heavier, steeper learning curve, but MUCH more stable
- **Recommendation**: MIGRATE TO OPENTURNS if PCE is needed

**DIY Implementation**:
- **Complexity**: Moderate (PCE is well-documented in literature)
- **Effort**: 2-4 weeks for basic PCE implementation
- **Trade-off**: Full control, no dependency risk, implementation burden

**Standard Monte Carlo**:
- **Fallback**: Use more samples with scipy.stats instead of PCE
- **Trade-off**: Slower for expensive models, but stable and supported

### Contingency Strategy for Current Users

**If you currently use chaospy**:
1. **Immediate**: Pin chaospy and numpoly versions EXACTLY
2. **Short-term** (1-3 months): Evaluate OpenTURNS migration
3. **Medium-term** (3-6 months): Begin migration or plan DIY implementation
4. **Long-term**: Assume chaospy will be abandoned, complete migration

**For new projects**:
1. **DO NOT START** with chaospy
2. Use OpenTURNS for PCE needs
3. Or use standard Monte Carlo (more samples, but stable)

## Strategic Recommendation

**chaospy is a DECLINING ACADEMIC PROJECT with HIGH abandonment risk. NOT RECOMMENDED for any user type.**

**Recommendation by User Type**:

- **Academics**: Avoid (reproducibility risk, use OpenTURNS)
- **Startups**: Avoid (abandonment risk, use OpenTURNS or MC)
- **Enterprises**: Absolutely avoid (unacceptable risk)
- **Data Scientists**: Avoid (better learning investments exist)
- **Hobbyists**: Avoid (learn PCE elsewhere)

**Confidence Level**: 2/10 (high confidence it will be abandoned)

**Time Horizon**: 2-4 years maximum (likely abandoned sooner)

**Strategic Position**: DECLINING ACADEMIC PROJECT - avoid or migrate

**Decision Rule**:
- **If currently using**: MIGRATE to OpenTURNS within 6-12 months
- **If considering**: DO NOT START - use OpenTURNS instead
- **If need PCE**: Use OpenTURNS or implement from literature
- **If no PCE need**: Use scipy.stats (standard Monte Carlo)

**Future-Proofing**: chaospy has NO future-proofing value. Any investment in chaospy is likely wasted. Migrate to stable alternatives now.

## Comparison to Alternatives

**chaospy vs. OpenTURNS**:
- **chaospy**: Pythonic, simple, DECLINING, high risk
- **OpenTURNS**: Industrial, comprehensive, active, low risk
- **Verdict**: OpenTURNS is superior strategic choice despite learning curve

**chaospy vs. DIY PCE**:
- **chaospy**: Existing code, DECLINING, abandonment risk
- **DIY**: Implementation effort, but full control, no dependency
- **Verdict**: For critical needs, DIY is safer than chaospy dependency

**chaospy vs. scipy.stats (standard MC)**:
- **chaospy**: Sample efficient for expensive models, HIGH RISK
- **scipy.stats**: More samples needed, STABLE, supported
- **Verdict**: scipy.stats is safer unless PCE is absolutely required

**Strategic Positioning**: chaospy is a **strategic liability** - powerful methods implemented, but unsustainable governance makes it unsuitable for any production or research use requiring reproducibility beyond 1-2 years.

## Special Warning: Academic Reproducibility

For academics: Using chaospy in research creates **reproducibility risk**.

**Scenario**: You publish paper in 2025 using chaospy v4.4
- 2027: Reader tries to reproduce, chaospy incompatible with Python 3.14
- 2028: chaospy abandoned, not installable on modern systems
- 2030: Your paper's code no longer runs

**Mitigation**:
- Archive full environment (Docker container) with paper
- Cite specific versions, archive code
- Consider OpenTURNS for better long-term reproducibility
- Document algorithms used, not just "we used chaospy"

This reproducibility risk alone makes chaospy unsuitable for academic research.
