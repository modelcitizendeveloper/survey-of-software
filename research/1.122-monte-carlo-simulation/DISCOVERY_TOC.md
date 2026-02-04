# 1.122 Monte Carlo Simulation Libraries - Discovery Table of Contents

**Date Compiled**: 2025-10-19
**Status**: Complete (S1-S4 methodologies executed)
**Category**: 1.120-129 Simulation & Modeling Libraries
**Libraries Analyzed**: NumPy, SciPy, SALib, uncertainties, chaospy, OpenTURNS, PyMC

---

## Executive Summary

**What is Monte Carlo Simulation?**
Monte Carlo simulation uses repeated random sampling to model uncertainty and variability in complex systems, enabling quantitative analysis of risk, confidence intervals, and parameter sensitivity.

**What This Research Covers**
This comprehensive discovery analyzed 6 core Python libraries for Monte Carlo simulation across four distinct methodologies (S1-S4), evaluating:
- Random number generation and statistical distributions
- Quasi-Monte Carlo and Latin Hypercube sampling
- Sensitivity analysis (Sobol, Morris, FAST methods)
- Uncertainty propagation and error analysis
- Bayesian inference and model calibration

**Key Finding**
All four methodologies converge on **NumPy + scipy.stats** as the universal foundation for Monte Carlo work. Specialized tools (SALib, uncertainties, PyMC, OpenTURNS) should be added only when specific needs justify the complexity, with careful attention to long-term strategic risk (maintenance, governance, institutional backing).

**Universal Recommendation**
Start with scipy.stats (covers 90% of use cases), add SALib for sensitivity analysis if D ≥ 10 parameters, and consider uncertainties for convenient error propagation. Avoid chaospy (declining academic project). Use OpenTURNS for industrial/enterprise applications requiring comprehensive UQ workflows.

---

## Quick Recommendations by Methodology

### S1 Rapid Discovery
**Primary Recommendation**: The Standard Stack (NumPy + scipy.stats + SALib + uncertainties)
**Confidence**: Very High (95%)
**Rationale**: Popularity = reliability. 100M+ monthly downloads, universal adoption, fastest time-to-value (<30 min to working Monte Carlo). SALib provides best-in-class sensitivity analysis with 60K weekly downloads and no viable alternative.

**Time to First Result**: 15-20 minutes total
**Coverage**: 100% of typical OR consulting requirements met

**Key Insight**: Popular solutions exist for a reason. The standard scientific Python stack (NumPy/SciPy) is battle-tested by billions of simulations and millions of users.

---

### S2 Comprehensive Discovery
**Primary Recommendation**: Layered Toolkit (scipy.stats + SALib + uncertainties as core, add chaospy/OpenTURNS as needed)
**Confidence**: High (90%)
**Rationale**: No single library is optimal for all use cases. Best-of-breed combination provides superior performance and usability compared to monolithic frameworks. scipy.stats offers fastest RNG (PCG64) and vectorized operations, SALib delivers comprehensive sensitivity analysis (Morris, Sobol, FAST, PAWN), uncertainties enables elegant analytical error propagation.

**Decision Framework**:
- **Fast models (< 0.1s/eval)**: scipy.stats standard Monte Carlo
- **Medium models (0.1-1s)**: scipy.stats.qmc Latin Hypercube Sampling
- **Expensive models (> 1s)**: chaospy PCE for 10-100× sample reduction
- **Industrial UQ**: OpenTURNS for copulas, reliability analysis, regulatory compliance

**Key Trade-off**: Specialist approach (multiple lightweight libraries) vs. Generalist approach (comprehensive suite like OpenTURNS). Specialist wins on learning curve and performance for typical OR tasks.

---

### S3 Need-Driven Discovery
**Recommendations by Pattern**:

**Sensitivity Analysis** (Which inputs matter most?)
- D < 10: NumPy/SciPy correlation analysis
- 10 ≤ D ≤ 50: SALib Sobol indices (variance-based sensitivity)
- D > 50: SALib Morris screening → Sobol on reduced set

**Confidence Intervals** (Statistical bounds on predictions)
- Scalar output: NumPy percentiles (simple, fast)
- Complex statistics: scipy.stats.bootstrap (gold standard, no distributional assumptions)
- Analytical approximation: uncertainties (3-4× overhead, assumes small uncertainties)

**Risk Quantification** (Probability of meeting goals)
- Basic: NumPy (np.mean(results >= target) for success probability)
- Alternative comparison: scipy.stats hypothesis testing
- Financial risk: NumPy + custom VaR/CVaR calculations

**Uncertainty Propagation** (Input uncertainty → output uncertainty)
- Fast models, D < 10: NumPy/SciPy standard Monte Carlo
- Fast models, D ≥ 10: scipy.stats.qmc Latin Hypercube
- Expensive models: chaospy polynomial chaos expansion
- Complex dependencies: OpenTURNS (copula support)

**Model Calibration** (Fit parameters to data)
- Point estimates: scipy.optimize least squares
- Full Bayesian uncertainty: PyMC (posterior distributions)
- Custom likelihood: emcee MCMC sampler

**Distribution Characterization** (Describe output distribution)
- Quick summary: NumPy + pandas (df.describe())
- Identify best-fit distribution: scipy.stats fitting + GOF tests
- Visualization: Seaborn (histplot, kdeplot, Q-Q plots)

**Key Insight**: Match requirements to library capabilities, don't force-fit a library to your problem. Start simple (NumPy/SciPy), add specialized tools as needed.

---

### S4 Strategic Discovery
**Recommendations by User Type**:

**Academic Researchers**
- **Core**: NumPy + scipy.stats (universal peer acceptance, permanent citations)
- **Add if needed**: SALib (pin version, archive with paper), PyMC (Bayesian inference)
- **Avoid**: chaospy (reproducibility risk by 2027)
- **Risk Level**: LOW (with version pinning and archival)

**Startup CTOs**
- **MVP Stack**: NumPy + scipy.stats (zero cost, fastest learning, universal talent pool)
- **Production**: Add SALib/uncertainties only if core value proposition
- **Avoid**: PyMC (too heavy for forward MC), OpenTURNS (overkill for MVP), chaospy (abandonment risk)
- **Risk Level**: LOW (Tier 1-2 stack), MEDIUM (Tier 3)

**Enterprise Architects**
- **Foundation**: NumPy + scipy.stats (NumFOCUS backing, commercial support available via Tidelift/Quansight)
- **Comprehensive UQ**: OpenTURNS (EDF/Airbus backing, regulatory validation, Phimeca support)
- **Bayesian**: PyMC (NumFOCUS, PyMC Labs support)
- **Use with caution**: SALib (succession risk, maintain fork capability)
- **Avoid**: uncertainties (solo maintainer), chaospy (unacceptable risk)
- **Risk Level**: LOW (Tier 1-2 with commercial support)

**Data Scientists**
- **Daily driver**: NumPy + scipy.stats + pandas + matplotlib
- **Exploratory SA**: SALib (acceptable risk for analysis work)
- **Bayesian inference**: PyMC + ArviZ (growing demand skill)
- **Avoid**: chaospy (declining), OpenTURNS (API friction with pandas/Jupyter)
- **Risk Level**: LOW (Tier 1 for production, Tier 3 acceptable for exploration)

**Hobbyists/Learners**
- **Start here**: NumPy + scipy.stats + matplotlib + Jupyter (best documented, largest community)
- **Add when ready**: SALib (teaches SA concepts), uncertainties (error propagation)
- **Advanced**: PyMC + ArviZ (valuable skill, steep learning curve)
- **Avoid**: chaospy (poor docs, minimal community), OpenTURNS (overwhelming for beginners)
- **Risk Level**: LOW (learning context tolerates library changes)

**Strategic Risk Tiers** (Long-term viability):
- **Tier 1 (10+ years)**: NumPy, scipy.stats - UNIVERSAL SAFE BETS
- **Tier 2 (7-10 years)**: PyMC, OpenTURNS - INSTITUTIONAL-BACKED SPECIALISTS
- **Tier 3 (3-5 years)**: SALib, uncertainties - NICHE LEADERS WITH SUCCESSION RISK
- **Tier 4 (2-4 years)**: chaospy - HIGH RISK, AVOID OR MIGRATE

---

## Convergence Analysis

### Complete Agreement (All 4 Methodologies)

**NumPy + scipy.stats as Universal Foundation**
All methodologies (S1-S4) independently converged on NumPy's random number generation and scipy.stats as the essential starting point for Monte Carlo work:

- **S1 Rapid**: "100M+ downloads/month, if millions succeed, you will too"
- **S2 Comprehensive**: "Fastest RNG (PCG64), foundation for all Monte Carlo work"
- **S3 Need-Driven**: "Foundation Tier - ALWAYS NEEDED for all patterns"
- **S4 Strategic**: "10/10 confidence, 10+ year horizon, zero strategic risk"

**Convergence reasoning**: Popularity (S1), performance (S2), versatility (S3), and long-term viability (S4) all point to the same answer. This is the rarest and strongest form of recommendation convergence.

---

### Strong Agreement (3/4 Methodologies)

**SALib for Sensitivity Analysis**
S1, S2, and S3 recommend SALib as the best Python sensitivity analysis library, with S4 acknowledging it while flagging strategic risk:

- **S1**: "THE library for sensitivity analysis, 60K weekly downloads, no viable alternative"
- **S2**: "Best comprehensive sensitivity analysis library (Morris + Sobol + FAST + PAWN)"
- **S3**: "Gold-standard variance-based sensitivity for D ≥ 10"
- **S4**: "Best tool, but Tier 3 risk (succession concerns, use with monitoring)"

**Divergence reasoning**: S1-S3 focus on current capability (SALib is objectively the best), while S4 adds temporal dimension (small maintainer team, 3-5 year horizon, succession risk).

**Resolution**: Use SALib for now, but enterprise users should maintain fork capability and monitor quarterly.

---

**uncertainties for Error Propagation**
S1, S2, and S3 recommend uncertainties for convenient analytical error propagation, while S4 flags solo-maintainer risk:

- **S1**: "Optional but useful for error propagation"
- **S2**: "Elegant for fast analytical propagation (3-4× overhead, automatic differentiation)"
- **S3**: "Simple, integrates with NumPy workflow"
- **S4**: "Tier 3 risk (solo maintainer), acceptable for analysis, not production-critical systems"

**Divergence reasoning**: Convenience (S1-S3) vs. long-term support risk (S4).

**Resolution**: Use for exploratory work and non-critical calculations. Enterprise users should document algorithms (manual error propagation is simple math, ~200 lines to reimplement).

---

### Moderate Agreement (2/4 Methodologies)

**OpenTURNS for Comprehensive UQ**
S2 and S4 recommend OpenTURNS for industrial/enterprise applications, while S1 and S3 suggest it's overkill for typical use cases:

- **S2**: "Add when needed for copulas, Kriging, reliability analysis, regulatory compliance"
- **S4**: "Tier 2 (9/10 confidence), industrial consortium backing, 7-10 year horizon"
- **S1**: "Not recommended (steep learning curve) unless forced by advanced requirements"
- **S3**: "Only for engineering applications, comprehensive UQ workflow"

**Divergence reasoning**: S1 optimizes for speed-to-value (OpenTURNS has steeper learning curve). S3 focuses on specific patterns (OpenTURNS is overkill for simple MC). S2 and S4 consider long-term capability and strategic safety.

**Resolution**: Context-dependent. Use scipy.stats for typical OR consulting (90% of cases). Use OpenTURNS for enterprise/industrial applications requiring comprehensive UQ, regulatory validation, or commercial support.

---

### Strong Disagreement (Opposite Recommendations)

**chaospy for Expensive Models**
The four methodologies sharply disagree on chaospy:

- **S1**: "Don't use (academic focus, steep learning curve)" - 40% confidence if forced
- **S2**: "Tier 2 Advanced - Add for expensive models >1 sec/eval, D < 15, 10-100× sample efficiency"
- **S3**: "Use for surrogate modeling when model evaluation is expensive"
- **S4**: "Tier 4 HIGH RISK - 2/10 confidence, declining academic project, AVOID OR MIGRATE"

**Divergence reasoning**:
- S1 (Rapid): Focuses on current popularity → chaospy has low adoption
- S2 (Comprehensive): Focuses on current capability → chaospy PCE is technically excellent
- S3 (Need-Driven): Focuses on fit → chaospy solves expensive model pattern well
- S4 (Strategic): Focuses on long-term viability → chaospy shows declining activity, succession risk

**This is the MOST IMPORTANT divergence** - it reveals the difference between "what works now" vs. "what's safe long-term."

**Resolution**:
- **If project timeline < 2 years AND model is expensive**: chaospy's PCE is technically superior
- **If project timeline > 2 years OR strategic stability matters**: migrate to OpenTURNS or use more samples with scipy.stats
- **Enterprise users**: Avoid chaospy entirely (unacceptable strategic risk)

---

### Why Methodologies Diverge

**S1 Rapid** → Optimizes for **speed-to-value** (popularity, fast learning, low risk)
**S2 Comprehensive** → Optimizes for **current technical capability** (performance, features, completeness)
**S3 Need-Driven** → Optimizes for **requirement fit** (does it solve my specific pattern?)
**S4 Strategic** → Optimizes for **long-term viability** (governance, maintenance, 10-year horizon)

**These are different lenses on the same libraries**, and the "right" answer depends on your priorities:
- Fast prototype? → Follow S1
- Complex technical requirements? → Follow S2
- Specific use case pattern? → Follow S3
- Building infrastructure for 10 years? → Follow S4

**The strongest recommendations** (NumPy/scipy.stats) are where all four lenses align.

---

## Complete File Index

### S1 Rapid Discovery (`S1-rapid/`)
- `README.md` - Overview of S1 methodology: popularity-driven, fast time-to-value approach
- `approach.md` - S1 principles: popular = reliable, battle-tested, fast learning curve
- `numpy-random.md` - NumPy random number generation (PCG64, default_rng API)
- `scipy-stats.md` - SciPy statistical distributions (100+ distributions, parametric methods)
- `scipy-stats-qmc.md` - Quasi-Monte Carlo (Latin Hypercube, Sobol sequences)
- `salib.md` - Sensitivity analysis library (Sobol, Morris, FAST methods)
- `uncertainties.md` - Automatic error propagation (analytical differentiation)
- `uqpy.md` - UQpy evaluation (advanced UQ, not recommended for rapid start)
- `alternatives-not-recommended.md` - Libraries to avoid (pyDOE, PyMC for forward MC, chaospy, monaco)
- `recommendation.md` - **FINAL S1 RECOMMENDATION** (NumPy + scipy.stats + SALib stack)

### S2 Comprehensive Discovery (`S2-comprehensive/`)
- `README.md` - Overview of S2 methodology: exhaustive analysis across all dimensions
- `approach.md` - S2 evaluation framework (performance, features, maintainability, OR fit)
- `scipy-stats.md` - Deep dive: performance benchmarks, distribution coverage, QMC methods
- `salib.md` - Deep dive: sensitivity analysis methods comparison, sample requirements
- `uncertainties.md` - Deep dive: error propagation mechanics, automatic differentiation
- `chaospy.md` - Deep dive: polynomial chaos expansion, sample efficiency analysis
- `openturns.md` - Deep dive: comprehensive UQ suite, industrial backing, regulatory use
- `pymc.md` - Deep dive: Bayesian inference (NOT for forward MC, inverse problems only)
- `feature-comparison.md` - Side-by-side feature matrix across all 6 libraries
- `recommendation.md` - **FINAL S2 RECOMMENDATION** (layered toolkit by use case)

### S3 Need-Driven Discovery (`S3-need-driven/`)
- `approach.md` - S3 methodology: requirements first, then find exact fits
- `sensitivity-analysis-pattern.md` - Use case: "Which inputs matter most?" (SALib, NumPy)
- `confidence-interval-pattern.md` - Use case: "Statistical bounds?" (scipy.bootstrap, NumPy)
- `risk-quantification-pattern.md` - Use case: "Probability of success?" (NumPy, scipy.stats)
- `uncertainty-propagation-pattern.md` - Use case: "Propagate uncertainty?" (scipy.qmc, chaospy, OpenTURNS)
- `model-calibration-pattern.md` - Use case: "Fit parameters to data?" (PyMC, scipy.optimize, emcee)
- `distribution-characterization-pattern.md` - Use case: "Describe output distribution?" (scipy.stats, Seaborn)
- `recommendation.md` - **FINAL S3 RECOMMENDATION** (decision tree by pattern and parameters)

### S4 Strategic Discovery (`S4-strategic/`)
- `README.md` - Overview of S4 methodology: long-term viability, governance health
- `approach.md` - S4 evaluation framework (3-5 year strategic planning, risk tiers)
- `numpy-random-maturity.md` - Strategic assessment: Tier 1 (10/10 confidence, critical infrastructure)
- `scipy-stats-maturity.md` - Strategic assessment: Tier 1 (10/10 confidence, NumFOCUS flagship)
- `salib-maturity.md` - Strategic assessment: Tier 3 (6/10 confidence, succession risk)
- `uncertainties-maturity.md` - Strategic assessment: Tier 3 (6/10 confidence, solo-maintained)
- `chaospy-maturity.md` - Strategic assessment: Tier 4 (2/10 confidence, declining project)
- `openturns-maturity.md` - Strategic assessment: Tier 2 (9/10 confidence, industrial consortium)
- `pymc-maturity.md` - Strategic assessment: Tier 2 (9/10 confidence, NumFOCUS + commercial support)
- `ecosystem-positioning.md` - Python scientific ecosystem analysis, consolidation trends
- `recommendation.md` - **FINAL S4 RECOMMENDATION** (strategic stack by user type)

---

## Quick Start Guide

### For Rapid Decision (< 10 minutes)
**Goal**: Get a library recommendation fast, start coding immediately
**Read**: `/S1-rapid/recommendation.md`
**Outcome**: Install NumPy + scipy.stats + SALib, run first Monte Carlo in 20 minutes
**Best for**: Prototypes, tight deadlines, proven solutions, low-risk choices

---

### For Comprehensive Understanding (2-3 hours)
**Goal**: Understand all options, make informed trade-offs, deep technical details
**Read**:
1. `/S2-comprehensive/recommendation.md` (main recommendation)
2. `/S2-comprehensive/feature-comparison.md` (side-by-side library comparison)
3. Individual library deep-dives as needed (scipy-stats.md, salib.md, etc.)

**Outcome**: Complete picture of Python MC ecosystem, performance benchmarks, use-case-specific recommendations
**Best for**: Complex projects, technical evaluation, architecture decisions

---

### For Specific Use Case (30-60 minutes)
**Goal**: Solve a specific pattern (sensitivity, confidence intervals, risk quantification)
**Read**:
1. `/S3-need-driven/recommendation.md` (decision tree by pattern)
2. Your specific pattern file:
   - Sensitivity analysis → `sensitivity-analysis-pattern.md`
   - Confidence intervals → `confidence-interval-pattern.md`
   - Risk quantification → `risk-quantification-pattern.md`
   - Uncertainty propagation → `uncertainty-propagation-pattern.md`
   - Model calibration → `model-calibration-pattern.md`
   - Distribution characterization → `distribution-characterization-pattern.md`

**Outcome**: Exact library stack for your pattern, working code templates, parameter-based guidance (D, N, model complexity)
**Best for**: Focused problems, clear requirements, pattern-matching scenarios

---

### For Long-Term Strategy (1-2 hours)
**Goal**: Build infrastructure for 3-10 years, minimize strategic risk, ensure long-term support
**Read**:
1. `/S4-strategic/recommendation.md` (recommendations by user type)
2. `/S4-strategic/ecosystem-positioning.md` (ecosystem trends, consolidation analysis)
3. Individual maturity assessments for libraries you're considering

**Outcome**: Risk-adjusted library stack, monitoring strategy, migration planning, vendor relationships
**Best for**: Enterprise architecture, academic reproducibility, startup foundations, long-term projects

---

### Decision Tree: Which Methodology to Follow?

```
START: What's your primary constraint?

├─ TIME (need answer in < 1 day)
│  └─ Follow S1 Rapid → recommendation.md
│     Outcome: Proven stack, fast learning, low risk
│
├─ TECHNICAL REQUIREMENTS (complex performance/feature needs)
│  └─ Follow S2 Comprehensive → recommendation.md + feature-comparison.md
│     Outcome: Optimal performance, complete feature coverage
│
├─ SPECIFIC PATTERN (clear use case: SA, CI, risk, etc.)
│  └─ Follow S3 Need-Driven → your-pattern.md
│     Outcome: Exact fit for your requirements
│
└─ STRATEGIC RISK (10+ year planning, governance matters)
   └─ Follow S4 Strategic → recommendation.md (your user type)
      Outcome: Long-term viability, minimal succession risk
```

---

## Libraries Analyzed

| Library | Primary Use Case | S4 Maturity Tier | Key Strength | Recommendation Level |
|---------|------------------|------------------|--------------|---------------------|
| **NumPy** | Random number generation | Tier 1 (10/10) | Universal foundation, PCG64 RNG | ESSENTIAL (all users) |
| **scipy.stats** | Distributions, QMC, bootstrap | Tier 1 (10/10) | 100+ distributions, NumFOCUS flagship | ESSENTIAL (all users) |
| **SALib** | Sensitivity analysis | Tier 3 (6/10) | Best Python SA library (Sobol, Morris) | RECOMMENDED (D ≥ 10) |
| **uncertainties** | Error propagation | Tier 3 (6/10) | Automatic differentiation, minimal code | OPTIONAL (convenience) |
| **chaospy** | Polynomial chaos, expensive models | Tier 4 (2/10) | 10-100× sample efficiency (PCE) | AVOID (declining) |
| **OpenTURNS** | Industrial UQ, regulatory | Tier 2 (9/10) | Comprehensive suite, EDF/Airbus backing | ENTERPRISE (as needed) |
| **PyMC** | Bayesian inference | Tier 2 (9/10) | Best Python Bayesian framework | SPECIALIZED (inverse problems) |

**Notes**:
- **NumPy + scipy.stats**: Start here (90% of use cases covered)
- **SALib**: Add if sensitivity analysis is core requirement (D ≥ 10 parameters)
- **uncertainties**: Add for convenient error propagation (or implement manually)
- **chaospy**: Strategic risk too high (migrate to OpenTURNS if using PCE)
- **OpenTURNS**: Enterprise/industrial only (comprehensive UQ, commercial support)
- **PyMC**: Bayesian inference only (NOT for forward Monte Carlo simulation)

---

## Navigation

### By Methodology
- [S1 Rapid Discovery](S1-rapid/README.md) - Fast, popularity-driven recommendations
- [S2 Comprehensive Discovery](S2-comprehensive/README.md) - Exhaustive technical analysis
- [S3 Need-Driven Discovery](S3-need-driven/README.md) - Pattern-based recommendations
- [S4 Strategic Discovery](S4-strategic/README.md) - Long-term viability assessment

### By Use Case (S3 Patterns)
- [Sensitivity Analysis](S3-need-driven/sensitivity-analysis-pattern.md) - Which parameters matter most?
- [Confidence Intervals](S3-need-driven/confidence-interval-pattern.md) - Statistical bounds on predictions
- [Risk Quantification](S3-need-driven/risk-quantification-pattern.md) - Probability of meeting goals
- [Uncertainty Propagation](S3-need-driven/uncertainty-propagation-pattern.md) - Input → output uncertainty
- [Model Calibration](S3-need-driven/model-calibration-pattern.md) - Fit parameters to data
- [Distribution Characterization](S3-need-driven/distribution-characterization-pattern.md) - Describe outputs

### By Library (Deep Dives)
**S2 Comprehensive Analyses**:
- [scipy.stats Deep Dive](S2-comprehensive/scipy-stats.md)
- [SALib Deep Dive](S2-comprehensive/salib.md)
- [uncertainties Deep Dive](S2-comprehensive/uncertainties.md)
- [chaospy Deep Dive](S2-comprehensive/chaospy.md)
- [OpenTURNS Deep Dive](S2-comprehensive/openturns.md)
- [PyMC Deep Dive](S2-comprehensive/pymc.md)

**S4 Strategic Assessments**:
- [NumPy Maturity Assessment](S4-strategic/numpy-random-maturity.md)
- [scipy.stats Maturity Assessment](S4-strategic/scipy-stats-maturity.md)
- [SALib Maturity Assessment](S4-strategic/salib-maturity.md)
- [uncertainties Maturity Assessment](S4-strategic/uncertainties-maturity.md)
- [chaospy Maturity Assessment](S4-strategic/chaospy-maturity.md)
- [OpenTURNS Maturity Assessment](S4-strategic/openturns-maturity.md)
- [PyMC Maturity Assessment](S4-strategic/pymc-maturity.md)

### By User Type (S4 Strategic)
- [Academic Researchers](S4-strategic/recommendation.md#1-academic-researchers) - Reproducibility, peer acceptance
- [Startup CTOs](S4-strategic/recommendation.md#2-startup-ctos) - Rapid prototyping, minimal dependencies
- [Enterprise Architects](S4-strategic/recommendation.md#3-enterprise-architects) - Long-term support, compliance
- [Data Scientists](S4-strategic/recommendation.md#4-data-scientists) - Jupyter integration, workflow fit
- [Hobbyists/Learners](S4-strategic/recommendation.md#5-hobbyistslearners) - Documentation, community support

---

## Meta-Analysis: The Four Methodologies

**S1 Rapid**: Popularity-driven, fast time-to-value (< 1 day to recommendation)
**S2 Comprehensive**: Feature-driven, exhaustive technical analysis (performance, completeness)
**S3 Need-Driven**: Pattern-driven, requirements-first matching (6 generic use case patterns)
**S4 Strategic**: Viability-driven, long-term risk assessment (3-10 year planning horizon)

**When they AGREE** (NumPy/scipy.stats) → Highest confidence recommendation
**When they DIVERGE** (chaospy) → Context matters, choose methodology matching your constraints

**This multi-methodology approach** provides orthogonal perspectives on the same libraries, revealing trade-offs between current capability (S2), strategic safety (S4), learning speed (S1), and requirement fit (S3).

---

**Document Generation**: Auto-generated from S1-S4 recommendation.md files on 2025-10-19
**Research Category**: 1.122 Monte Carlo Simulation Libraries (part of 1.120-129 Simulation & Modeling)
**Total Analysis Depth**: 4 methodologies × 6 libraries × 27 files = comprehensive ecosystem coverage

---

**For Questions or Updates**: Review individual methodology READMEs for detailed rationale and evaluation criteria.
