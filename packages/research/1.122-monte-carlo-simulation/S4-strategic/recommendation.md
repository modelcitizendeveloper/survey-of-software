# S4 Strategic Recommendations: Monte Carlo Library Selection

**Methodology**: S4 Strategic Solution Selection
**Philosophy**: Long-term viability and strategic fit across diverse user communities
**Time Horizon**: 3-5 year strategic planning
**Assessment Date**: October 2025

## Executive Summary

After comprehensive strategic assessment of Monte Carlo libraries in the Python ecosystem, this analysis provides recommendations for five distinct user archetypes, focusing on long-term viability, governance health, and strategic risk management.

**Key Finding**: The Python scientific ecosystem CONSOLIDATES around NumPy/SciPy. Strategic recommendations favor institutional-backed libraries (NumFOCUS, corporate sponsorship) over academic projects, with clear risk assessment for each user type.

**Universal Truth**: NumPy + scipy.stats form the SAFEST long-term foundation for Monte Carlo work across all user types. Specialized tools should be added only when justified by specific needs and with awareness of strategic risks.

## Strategic Risk Tiers

Based on governance health, maintenance trajectory, and long-term viability:

### Tier 1: UNIVERSAL SAFE BETS (10+ year horizon)
- **NumPy (numpy.random)**: 10/10 confidence - Critical infrastructure
- **SciPy (scipy.stats)**: 10/10 confidence - NumFOCUS flagship, expanding scope

### Tier 2: INSTITUTIONAL-BACKED SPECIALISTS (7-10 year horizon)
- **PyMC**: 9/10 confidence - NumFOCUS, commercial support (Bayesian inference only)
- **OpenTURNS**: 9/10 confidence - Industrial consortium, regulatory use (comprehensive UQ)

### Tier 3: NICHE LEADERS WITH SUCCESSION RISK (3-5 year horizon)
- **SALib**: 6/10 confidence - Small academic team, best SA tool, succession risk
- **uncertainties**: 6/10 confidence - Solo-maintained, mature, minimal dependencies

### Tier 4: HIGH RISK - AVOID OR MIGRATE (2-4 year horizon)
- **chaospy**: 2/10 confidence - Declining academic project, abandonment risk

## Strategic Recommendations by User Type

### 1. Academic Researchers

**Primary Need**: Peer-reviewed methods, reproducibility, publication acceptance
**Risk Tolerance**: LOW (career depends on correctness and reproducibility)
**Timeline**: 1-3 years per project, but building long-term expertise

#### Recommended Stack

**Foundation (REQUIRED)**:
```
numpy>=1.24.0
scipy>=1.11.0
```
- **Rationale**: Universal peer acceptance, citations required for reproducibility
- **Risk**: Negligible (journals expect NumPy/SciPy)
- **Long-term**: Permanent (will outlast academic career)

**Sensitivity Analysis (IF NEEDED)**:
```
SALib>=1.4.0  # Pin specific version for reproducibility
```
- **Rationale**: Best Python SA library, peer-reviewed methods
- **Risk**: Medium (cite specific version, archive code with paper)
- **Alternative**: OpenTURNS (more stable, but steeper learning curve)
- **Mitigation**: Archive full environment (Docker) with publication

**Error Propagation (IF NEEDED)**:
```
uncertainties>=3.1.0
```
- **Rationale**: Standard for experimental uncertainty, simple
- **Risk**: Medium (solo maintainer, but cite version and archive)
- **Alternative**: Manual error propagation (first-order Taylor)

**Bayesian Inference (IF NEEDED)**:
```
pymc>=5.0.0
```
- **Rationale**: Leading Python Bayesian framework, well-cited
- **Risk**: Low (NumFOCUS, active development, but pin major version)
- **Alternative**: Stan (more mature, but separate language)

**AVOID**:
- **chaospy**: Declining activity = reproducibility risk (2027: library may not install)
- **Cutting-edge libraries**: No peer review acceptance, reproducibility concerns

#### Strategic Guidance

**Publication strategy**:
1. Always cite library versions (NumPy 1.24.0, SciPy 1.11.0, SALib 1.4.5)
2. Archive code with paper (Zenodo, GitHub release)
3. Document algorithms used, not just "we used Library X"
4. For critical work, include analytical validation alongside MC

**Long-term career investment**:
- **High value**: NumPy/SciPy expertise (transferable, permanent)
- **Medium value**: PyMC (Bayesian skills growing in demand)
- **Low value**: chaospy (declining library, skills may not transfer)

**Monitoring frequency**: Annual review of library health

**Risk Level**: LOW (with version pinning and archival)

---

### 2. Startup CTOs

**Primary Need**: Rapid prototyping, minimal dependencies, quick learning curve, cost-effective
**Risk Tolerance**: MEDIUM (can pivot if needed, but switching costs exist)
**Timeline**: Weeks to MVP, months to production

#### Recommended Stack

**Phase 1: MVP (Week 1-4)**
```
numpy>=1.24.0
scipy>=1.11.0
```
- **Rationale**: Zero cost, minimal dependencies, fastest time-to-value, universal talent pool
- **Risk**: Negligible (won't be abandoned, team can learn quickly)
- **Learning curve**: 1-2 days for basic MC (abundant tutorials)

**Phase 2: Production (Month 2-6)**

*IF sensitivity analysis needed*:
```
SALib>=1.4.0
```
- **Rationale**: Best SA tool, easy to integrate
- **Risk**: Medium (succession risk, but 3-5 year horizon acceptable for startups)
- **Mitigation**: Build internal SA expertise (understand algorithms, not just API)

*IF error propagation needed*:
```
uncertainties>=3.1.0
```
- **Rationale**: Minimal dependencies, simple, does one thing well
- **Risk**: Medium (solo maintainer, but simple to fork or reimplement if needed)
- **Mitigation**: Error propagation is simple math (200 lines to reimplement if necessary)

**AVOID for startups**:
- **PyMC**: Too heavy for forward MC (10-100× slower), steep learning curve, use only for genuine Bayesian needs
- **OpenTURNS**: Steeper learning curve, heavier dependencies, overkill for MVP
- **chaospy**: Abandonment risk too high for startup (no support path)

#### Strategic Guidance

**Hiring strategy**:
- NumPy/SciPy skills are universal (every data scientist knows them)
- PyMC skills are rarer (budget for training or specialized hire)
- OpenTURNS skills are very rare (European UQ specialists)

**Build vs. buy decision**:
- Start with scipy.stats (build on standard stack)
- Add SALib if SA is core value proposition
- Only add OpenTURNS if comprehensive UQ is competitive differentiator

**Technical debt management**:
- NumPy/SciPy = zero tech debt (stable foundation)
- SALib/uncertainties = low tech debt (simple, forkable if needed)
- chaospy = high tech debt (likely abandoned, will require replacement)

**Pivot flexibility**:
- Stick to Tier 1-2 libraries for maximum pivot flexibility
- Avoid deep dependency on Tier 3-4 (switching costs)

**Monitoring frequency**: Quarterly review (check library health)

**Risk Level**: LOW (with Tier 1-2 stack), MEDIUM (if using Tier 3)

---

### 3. Enterprise Architects

**Primary Need**: Long-term support, regulatory compliance, security updates, vendor backing
**Risk Tolerance**: VERY LOW (large switching costs, 10+ year planning horizons)
**Timeline**: Years of planning, decades of maintenance

#### Recommended Stack

**Foundation (MANDATORY)**:
```
numpy>=1.24.0  # NumFOCUS, critical infrastructure
scipy>=1.11.0  # NumFOCUS, expanding, long-term stable
```
- **Rationale**: Institutional backing, 10+ year horizon, commercial support available (Tidelift, Quansight)
- **Risk**: Negligible (safest software dependencies in Python ecosystem)
- **Support**: Tidelift subscriptions, Anaconda enterprise, Quansight consulting

**Comprehensive UQ (IF NEEDED)**:
```
openturns>=1.22  # Industrial backing, regulatory acceptance
```
- **Rationale**: EDF/Airbus backing, regulatory validation (nuclear, aerospace), commercial support (Phimeca Engineering)
- **Risk**: Low (multi-organizational governance, 10+ year horizon)
- **Support**: Phimeca Engineering (paid support, SLAs, training)
- **Regulatory**: Accepted by ASN (French nuclear), EASA (aviation)

**Bayesian Inference (IF NEEDED)**:
```
pymc>=5.0.0  # NumFOCUS, commercial support
```
- **Rationale**: NumFOCUS sponsored, commercial support (PyMC Labs), growing enterprise adoption
- **Risk**: Low (institutional backing), Medium (breaking changes across major versions)
- **Support**: PyMC Labs (consulting, training, custom development)
- **Mitigation**: Pin major versions, budget for migration support

**USE WITH CAUTION (require risk mitigation)**:
```
SALib>=1.4.0  # Best SA tool, but succession risk
```
- **Rationale**: Best available Python SA library, no good alternative
- **Risk**: Medium-High (small maintainer base, no commercial support)
- **Mitigation strategies**:
  1. Maintain internal fork capability
  2. Build internal SA expertise (not just library knowledge)
  3. Budget for re-implementation if abandoned (2-4 week effort)
  4. Monitor GitHub activity quarterly
  5. Consider OpenTURNS migration (has SA methods)

**AVOID for enterprise**:
- **uncertainties**: Solo maintainer, no SLA, acceptable only for non-critical analysis
- **chaospy**: Unacceptable risk (declining, no support, use OpenTURNS for PCE)

#### Strategic Guidance

**Procurement strategy**:
- Require institutional backing (NumFOCUS, corporate sponsor, consortium)
- Require commercial support option (Tidelift, vendor consulting)
- Require security vulnerability disclosure process

**Risk assessment framework**:
```
ACCEPTABLE RISK:
- NumPy/SciPy (critical infrastructure status)
- OpenTURNS (industrial consortium, commercial support)
- PyMC (NumFOCUS, commercial support, major version pinning)

MANAGED RISK (with mitigation):
- SALib (maintain fork capability, monitor quarterly)

UNACCEPTABLE RISK:
- Solo-maintained libraries without commercial backing (uncertainties)
- Declining academic projects (chaospy)
- Libraries without institutional support for 10+ year horizon
```

**Vendor management**:
- Establish relationships with Tidelift, Quansight (NumPy/SciPy support)
- Establish relationship with Phimeca Engineering (OpenTURNS support)
- Establish relationship with PyMC Labs (if using PyMC)

**Security compliance**:
- NumPy/SciPy: CVE tracking, CZI-funded security audits
- OpenTURNS: Industrial QA processes, security team
- PyMC: Active maintenance team, security response
- SALib: NO formal security process (risk factor)

**Regulatory compliance**:
- OpenTURNS: Validated for nuclear (ASN), aerospace (EASA)
- SciPy: Widely accepted for FDA submissions (validated software)
- PyMC: Case-by-case (Bayesian methods acceptance varies)

**Monitoring frequency**: Quarterly security updates, annual strategic review

**Risk Level**: LOW (with Tier 1-2 stack), UNACCEPTABLE (with Tier 3-4)

---

### 4. Data Scientists

**Primary Need**: Jupyter integration, NumPy/pandas compatibility, visualization, interactivity
**Risk Tolerance**: MEDIUM (exploratory work tolerates experimentation)
**Timeline**: Days to analysis, weeks to deployment

#### Recommended Stack

**Daily Driver (ALWAYS)**:
```
numpy>=1.24.0
scipy>=1.11.0
pandas>=2.0.0
matplotlib>=3.7.0
jupyter>=1.0.0
```
- **Rationale**: Standard data science stack, seamless integration, universal skills
- **Risk**: Negligible (ecosystem standard)
- **Learning**: Assumed baseline knowledge for data scientists

**Sensitivity Analysis (WHEN NEEDED)**:
```
SALib>=1.4.0
```
- **Rationale**: Easy to use, outputs pandas DataFrames, good examples
- **Risk**: Medium (succession risk), but acceptable for exploratory work
- **Usage**: Exploratory SA, not production-critical

**Error Propagation (OCCASIONAL)**:
```
uncertainties>=3.1.0
```
- **Rationale**: Simple, integrates with NumPy workflow
- **Risk**: Medium, but suitable for analysis (not production)
- **Usage**: Quick uncertainty estimates, not production calculations

**Bayesian Inference (SPECIALIZED)**:
```
pymc>=5.0.0
arviz>=0.15.0  # Visualization companion
```
- **Rationale**: Powerful Bayesian toolkit, great for inference problems
- **Risk**: Low (well-supported), but learning curve
- **Usage**: Parameter estimation, hierarchical models, NOT for forward MC

**AVOID**:
- **chaospy**: Declining library, limited Jupyter support, use OpenTURNS if PCE needed
- **OpenTURNS**: API friction with pandas/Jupyter workflow, use only if comprehensive UQ required

#### Strategic Guidance

**Workflow integration**:
```python
# Typical data science MC workflow (strategic stack)
import numpy as np
import scipy.stats as stats
import pandas as pd
import matplotlib.pyplot as plt

# 1. Define distributions (scipy.stats - safe, permanent)
revenue_dist = stats.norm(loc=100, scale=10)

# 2. Monte Carlo sampling (NumPy - safe, permanent)
rng = np.random.default_rng(seed=42)
samples = revenue_dist.rvs(size=10000, random_state=rng)

# 3. Results to DataFrame (pandas - safe, permanent)
results = pd.DataFrame({'revenue': samples})

# 4. Visualization (matplotlib - safe, permanent)
results['revenue'].hist(bins=50)
plt.show()

# Strategic: This workflow will work identically in 2030
```

**Skill investment priority**:
1. **High priority**: NumPy/SciPy/pandas (universal, permanent)
2. **Medium priority**: PyMC (Bayesian skills valuable, growing demand)
3. **Low priority**: Specialized libraries (may not transfer to next job)

**Exploratory vs. production**:
- **Exploratory**: Can use Tier 3 libraries (SALib, uncertainties) with awareness
- **Production**: Stick to Tier 1-2 (hand off to engineering with stable stack)

**Collaboration considerations**:
- NumPy/SciPy: Every data scientist knows them (easy collaboration)
- PyMC: Growing knowledge, but not universal (document well)
- SALib/OpenTURNS: Rare knowledge (provide good documentation)

**Monitoring frequency**: Annual review (check for new DA-friendly tools)

**Risk Level**: LOW (Tier 1 stack), LOW-MEDIUM (Tier 3 for exploration)

---

### 5. Hobbyists/Learners

**Primary Need**: Good documentation, active community, educational resources, approachability
**Risk Tolerance**: HIGH (learning experience valuable even if library changes)
**Timeline**: Hours to learning, weeks to first project

#### Recommended Stack

**Start Here (Week 1-2)**:
```
numpy>=1.24.0
scipy>=1.11.0
matplotlib>=3.7.0
jupyter>=1.0.0
```
- **Rationale**: Best documented, most tutorials, largest community (Stack Overflow)
- **Learning curve**: Gentle (abundant free resources)
- **Risk**: Negligible (stable learning investment)
- **Resources**: Official tutorials, YouTube, free courses

**Add When Ready (Week 3-8)**:

*Sensitivity Analysis*:
```
SALib>=1.4.0
```
- **Rationale**: Good documentation, clear examples, interesting methods
- **Learning**: Teaches sensitivity analysis concepts
- **Risk**: Low (learning investment is small, concepts transfer)

*Error Propagation*:
```
uncertainties>=3.1.0
```
- **Rationale**: Simple, well-documented, teaches error propagation
- **Learning**: Good for understanding uncertainty concepts
- **Risk**: Low (simple enough to understand implementation)

**Advanced Topics (Month 3+)**:

*Bayesian Inference*:
```
pymc>=5.0.0
arviz>=0.15.0
```
- **Rationale**: Excellent documentation, active community, valuable skill
- **Learning curve**: Steep (requires Bayesian statistics knowledge)
- **Risk**: Low (good learning investment), but significant time commitment
- **Prerequisite**: Learn Bayesian statistics concepts first (books, courses)

**AVOID for learning**:
- **chaospy**: Poor documentation, minimal community, declining library
- **OpenTURNS**: Steep learning curve, heavy dependencies, overwhelming for beginners

#### Strategic Guidance

**Learning path**:
```
1. NumPy basics (arrays, operations) - 1 week
2. SciPy distributions (scipy.stats) - 1 week
3. Basic Monte Carlo (sampling, histograms) - 1 week
4. Quasi-Monte Carlo (scipy.stats.qmc) - 1 week
5. Sensitivity analysis (SALib) - 2 weeks
6. Error propagation (uncertainties) - 1 week
7. Bayesian inference (PyMC) - optional, 4+ weeks
```

**Resource recommendations**:
- **NumPy/SciPy**: Official tutorials, SciPy lectures, YouTube
- **Monte Carlo**: Online courses, textbooks, blog posts (abundant)
- **PyMC**: "Bayesian Methods for Hackers" (free online book)
- **Avoid**: Libraries with poor documentation (time wasted)

**Community support**:
- **NumPy/SciPy**: 100K+ Stack Overflow questions (instant help)
- **PyMC**: Active Discourse forum (helpful community)
- **SALib/uncertainties**: Limited community (rely on documentation)
- **chaospy**: Minimal community (frustrating for learners)

**Skill transferability**:
- **NumPy/SciPy**: Universal (transfers to any Python data science job)
- **PyMC**: Growing demand (valuable career skill)
- **SALib/uncertainties**: Niche (concepts transfer, API may not)

**Project ideas**:
1. Personal finance MC (retirement planning) - scipy.stats
2. Weather uncertainty (temperature forecasting) - scipy.stats + uncertainties
3. Game outcome simulation (poker, dice) - NumPy
4. A/B testing (Bayesian) - PyMC
5. Sensitivity analysis (which factors matter most?) - SALib

**Monitoring frequency**: None required (learning investment is short-term)

**Risk Level**: LOW (learning context tolerates library changes)

---

## Universal Safe Bets (All User Types)

### Core Foundation (ALWAYS USE)

```python
# install
pip install numpy scipy pandas matplotlib jupyter

# or
conda install numpy scipy pandas matplotlib jupyter
```

**Libraries**:
1. **NumPy (numpy.random)** - RNG foundation
2. **SciPy (scipy.stats)** - Distributions, QMC, bootstrap
3. **pandas** - Results storage and manipulation
4. **matplotlib** - Visualization
5. **Jupyter** - Interactive exploration

**Strategic Rationale**:
- 10+ year viability (NumFOCUS backing, critical infrastructure)
- Universal skills (every Python user knows these)
- Zero strategic risk (won't be abandoned)
- Comprehensive documentation and community
- Industry standard (transferable across jobs, domains)

**When This Stack Is Sufficient**:
- Basic Monte Carlo sampling (90% of use cases)
- Confidence intervals and bootstrap (scipy.stats.bootstrap)
- Quasi-Monte Carlo (scipy.stats.qmc)
- Basic distributions (100+ in scipy.stats)
- Simple uncertainty propagation (manual calculations)

**When to Add Specialized Tools**:
- Sensitivity analysis → SALib (best tool, medium risk) or OpenTURNS (safer, steeper)
- Error propagation → uncertainties (convenient) or manual (safer)
- Bayesian inference → PyMC (best Python tool)
- Comprehensive UQ → OpenTURNS (enterprise) or stay with scipy (simple)
- Advanced metamodeling → OpenTURNS (only option)

### Risk-Adjusted Decision Tree

```
START: Do you need Monte Carlo simulation?
│
├─ YES → Use NumPy + scipy.stats (ALWAYS)
│   │
│   ├─ Need sensitivity analysis?
│   │   ├─ YES, can accept medium risk → SALib
│   │   ├─ YES, need enterprise support → OpenTURNS
│   │   └─ NO → Continue
│   │
│   ├─ Need error propagation?
│   │   ├─ YES, convenience priority → uncertainties (medium risk)
│   │   ├─ YES, safety priority → Manual calculation
│   │   └─ NO → Continue
│   │
│   ├─ Need Bayesian inference?
│   │   ├─ YES → PyMC (good choice)
│   │   └─ NO → Continue (you're doing forward MC, not inverse)
│   │
│   ├─ Need comprehensive UQ (copulas, reliability, metamodeling)?
│   │   ├─ YES, enterprise context → OpenTURNS
│   │   ├─ YES, research context → OpenTURNS or scipy.stats
│   │   └─ NO → Continue
│   │
│   └─ DONE: You have a strategic stack
│
└─ NO → Why are you reading this? :)
```

---

## Strategic Watch List (Monitor, Not Yet Recommended)

These are emerging or evolving libraries to MONITOR but NOT yet adopt for production use:

### 1. JAX Ecosystem (NumPyro, JAX-based MC)
**Why watching**: GPU acceleration via JAX, Array API standard
**Current status**: Growing, but less mature than NumPy/SciPy
**When to reconsider**: If Array API becomes mainstream (2027-2030?)
**Risk**: Ecosystem fragmentation, less stable than NumPy
**Action**: Monitor annually, experiment with non-critical projects

### 2. SciPy Sensitivity Analysis Module (hypothetical)
**Why watching**: SciPy may absorb SA functionality (like it did with QMC)
**Current status**: Not yet exists, but plausible
**When to reconsider**: If SciPy announces SA module
**Risk**: None (would be safer than SALib if it happens)
**Action**: Monitor SciPy release notes quarterly

### 3. Dask-Native Monte Carlo Libraries
**Why watching**: Distributed MC for large-scale simulations
**Current status**: Can use Dask + scipy.stats, but not seamless
**When to reconsider**: If dedicated Dask-MC library emerges with institutional backing
**Risk**: Distributed computing adds complexity
**Action**: Monitor for cloud-native MC tools

### 4. Quantum Computing Monte Carlo
**Why watching**: Quantum RNG, potential speedups
**Current status**: Research phase, not practical (2025)
**When to reconsider**: When quantum computers become accessible (2030+?)
**Risk**: Very speculative, may never be practical for typical MC
**Action**: Passive monitoring (follow quantum computing news)

### 5. Julia Language UQ Tools
**Why watching**: Julia may attract performance-critical users
**Current status**: Growing ecosystem (Distributions.jl, Turing.jl)
**When to reconsider**: If Julia ecosystem matures significantly
**Risk**: Python has too much ecosystem inertia to be displaced soon
**Action**: Monitor Julia adoption in scientific computing

**Strategic Guidance**: Do NOT adopt watch list items for production use. These are for AWARENESS only. Stick to recommended tiers for actual work.

---

## Long-Term Strategic Planning (2025-2030)

### Scenario Planning

#### Scenario 1: Status Quo (60% probability)
**What happens**:
- NumPy/SciPy continue dominating
- SciPy gradually expands MC functionality
- PyMC and OpenTURNS remain stable in niches
- SALib continues with small team
- chaospy is abandoned

**User strategy**:
- Continue with Tier 1-2 recommendations
- Monitor SciPy for functionality absorption
- Plan chaospy migration (if using)

#### Scenario 2: Ecosystem Consolidation (25% probability)
**What happens**:
- SciPy absorbs sensitivity analysis (displaces SALib)
- SciPy adds error propagation utilities
- Specialized libraries become legacy wrappers

**User strategy**:
- Excellent outcome (more functionality in stable library)
- Gradual migration from SALib → scipy.stats.sensitivity
- Reduced dependency count, increased stability

#### Scenario 3: GPU Acceleration Mainstream (10% probability)
**What happens**:
- Array API becomes standard
- NumPy/SciPy gain transparent GPU support
- JAX-based libraries gain adoption

**User strategy**:
- Benefit from GPU speedup with minimal code changes
- NumPy/SciPy code automatically faster
- May experiment with JAX for custom kernels

#### Scenario 4: Disruption (5% probability)
**What happens**:
- Python 4 with major breaking changes
- New array library displaces NumPy (very unlikely)
- Major ecosystem shift

**User strategy**:
- Institutional-backed libraries (Tier 1-2) will adapt
- Solo-maintained libraries (Tier 3-4) may not
- Vindication of conservative strategy

### Strategic Hedging

**To hedge against uncertainty**:
1. **Build on Tier 1 foundation** (NumPy/SciPy - will adapt to any change)
2. **Favor institutional backing** (NumFOCUS, corporate - have resources to adapt)
3. **Avoid deep lock-in** to Tier 3-4 (maintain migration capability)
4. **Monitor ecosystem** quarterly (early warning of shifts)
5. **Invest in concepts** (MC theory), not just library APIs

---

## Migration Strategies

### From chaospy (URGENT)
**Timeline**: 6-12 months
**Target**: OpenTURNS (comprehensive UQ) or scipy.stats (simple MC)

**Steps**:
1. Audit current chaospy usage (where, why, how critical)
2. Evaluate alternatives:
   - OpenTURNS for PCE needs (more stable)
   - scipy.stats for simple MC (more samples, but stable)
3. Pilot migration on non-critical project
4. Gradual rollout (project by project)
5. Archive chaospy environment (Docker) for legacy reproducibility

**Risk**: chaospy may become incompatible with Python 3.14+ (2027)

### From uncertainties (if needed)
**Timeline**: 12+ months (not urgent unless maintainer abandons)
**Target**: Manual error propagation or scipy (if added)

**Steps**:
1. Assess criticality (production systems vs. analysis scripts)
2. For critical systems: Implement error propagation (200 lines)
3. For analysis: Continue using, but monitor maintainer activity
4. Document algorithms (not just "we use uncertainties")

**Risk**: Solo maintainer succession, but library is mature and simple

### From SALib (if needed)
**Timeline**: 12+ months (monitor for signs of abandonment)
**Target**: OpenTURNS (comprehensive) or scipy (if added)

**Steps**:
1. Build internal SA expertise (understand Sobol, Morris algorithms)
2. Monitor SciPy for SA additions (may happen 2026-2028)
3. If SALib shows abandonment signs:
   - Migrate to OpenTURNS (enterprise)
   - Implement key methods (Sobol, Morris) from literature (2-4 weeks)
4. Gradual migration testing

**Risk**: Succession risk, but 3-5 year horizon is reasonable

---

## Cost-Benefit Analysis by User Type

### Academic Researchers
**Recommended stack cost**: $0 (all open source)
**Time investment**: 2-4 weeks (learning NumPy/SciPy/SALib)
**Risk cost**: Medium (reproducibility risk with Tier 3, mitigated by archival)
**Benefit**: Peer acceptance, reproducibility, low financial barrier
**ROI**: Excellent (zero cost, universal academic acceptance)

### Startup CTOs
**Recommended stack cost**: $0 (Tier 1-2 open source)
**Optional support cost**: $0-$5K/year (Tidelift, if enterprise customers require)
**Time investment**: 1-2 weeks (team learning)
**Risk cost**: Low-Medium (Tier 1 = zero, Tier 2 = succession risk)
**Benefit**: Fast prototyping, universal hiring, low financial burn
**ROI**: Excellent (zero upfront cost, fast time-to-market)

### Enterprise Architects
**Recommended stack cost**: $0 (core libraries open source)
**Support cost**: $2K-20K/year (Tidelift, Quansight, Phimeca, PyMC Labs)
**Migration cost**: $0 (building on stable foundation)
**Time investment**: 4-8 weeks (enterprise process, validation)
**Risk cost**: Very Low (Tier 1-2 with commercial support = minimal)
**Benefit**: 10+ year stability, regulatory acceptance, vendor support
**ROI**: Excellent (low cost vs. commercial UQ software: $50K-500K/year)

### Data Scientists
**Recommended stack cost**: $0 (all open source)
**Time investment**: 1 week (if familiar with NumPy/pandas)
**Risk cost**: Low (Tier 1 for production, Tier 3 acceptable for exploration)
**Benefit**: Seamless workflow integration, universal skills
**ROI**: Excellent (productivity boost, zero cost)

### Hobbyists/Learners
**Recommended stack cost**: $0 (all open source)
**Time investment**: 4-8 weeks (learning from scratch)
**Risk cost**: Zero (learning investment is short-term)
**Benefit**: Transferable skills, free education, large community
**ROI**: Excellent (free learning, high skill value)

---

## Final Strategic Recommendations

### Universal Principles (All Users)

1. **Build on NumPy/SciPy foundation** (10/10 strategic safety)
2. **Favor institutional backing** over academic projects (NumFOCUS, corporate)
3. **Accept medium risk only for best-in-class tools** (SALib, uncertainties)
4. **Avoid declining academic projects** (chaospy - migrate now)
5. **Monitor ecosystem quarterly** (early warning system)
6. **Invest in concepts, not APIs** (Monte Carlo theory > specific library knowledge)

### Decision Framework Summary

```
TIER 1 (USE ALWAYS):
├─ NumPy (numpy.random) - RNG foundation
└─ SciPy (scipy.stats) - Distributions, QMC, bootstrap
   → 10+ year horizon, negligible risk, universal choice

TIER 2 (ADD WHEN NEEDED):
├─ PyMC - Bayesian inference only (NOT for forward MC)
└─ OpenTURNS - Comprehensive UQ, enterprise, regulatory
   → 7-10 year horizon, low risk, institutional backing

TIER 3 (USE WITH CAUTION):
├─ SALib - Sensitivity analysis (best available, succession risk)
└─ uncertainties - Error propagation (solo-maintained, mature)
   → 3-5 year horizon, medium risk, niche leaders

TIER 4 (AVOID OR MIGRATE):
└─ chaospy - Declining academic project
   → 2-4 year horizon, high risk, migrate to OpenTURNS
```

### Strategic Confidence Levels

- **Highest confidence (10/10)**: NumPy + scipy.stats for ALL users
- **High confidence (9/10)**: +PyMC for Bayesian, +OpenTURNS for enterprise UQ
- **Medium confidence (6/10)**: +SALib for SA, +uncertainties for error propagation
- **Low confidence (2/10)**: chaospy (avoid or migrate)

### Time Horizon Guidance

**10+ year planning** (Enterprise):
- ONLY Tier 1 (NumPy/SciPy)
- ONLY Tier 2 with commercial support (OpenTURNS, PyMC)
- AVOID Tier 3-4 entirely

**5-7 year planning** (Academic, established startups):
- Tier 1 foundation
- Tier 2 for specialized needs
- Tier 3 with caution and monitoring

**3-5 year planning** (Startups, data scientists):
- Tier 1 foundation
- Tier 2-3 acceptable with risk awareness
- Monitor Tier 3 quarterly

**1-3 year planning** (Hobbyists, short projects):
- All tiers acceptable (learning context)
- Prefer Tier 1-2 for transferable skills

---

## Conclusion

The strategic landscape for Monte Carlo libraries strongly favors **conservative choices**: NumPy and scipy.stats provide the safest long-term foundation across all user types. Specialized tools should be added only when specific needs justify the increased strategic risk.

**The ecosystem is consolidating** - functionality is moving INTO scipy.stats (QMC was added, SA may follow). This trend rewards users who build on the standard stack and avoid dependency on declining academic projects.

**For maximum strategic safety**:
- Start with NumPy + scipy.stats (works for 90% of use cases)
- Add institutional-backed specialists only when needed (PyMC, OpenTURNS)
- Use niche leaders with caution (SALib, uncertainties) and monitoring
- Avoid or migrate from declining projects (chaospy)

**Strategic positioning**: The Python scientific ecosystem provides a rare situation where the SAFEST choice (scipy.stats) is also FREE, WELL-DOCUMENTED, and UNIVERSALLY KNOWN. This makes conservative strategy both low-risk and high-value across all user types.

Choose stability. Build on the foundation. Add complexity only when proven necessary.
