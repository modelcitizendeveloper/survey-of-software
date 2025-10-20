# S1: Rapid Library Search - Approach

## Methodology: Popular Solutions Exist for a Reason

**Time Budget**: 60 minutes maximum
**Discovery Tools**: Web search, PyPI downloads, GitHub stars, Stack Overflow mentions
**Philosophy**: Find widely-adopted, battle-tested libraries quickly

## Discovery Process

### Phase 1: Initial Web Search (15 minutes)

Started with three parallel searches to get a quick landscape view:
1. "Python Monte Carlo simulation library PyPI downloads 2024"
2. "best Python libraries uncertainty quantification sensitivity analysis"
3. "Python Latin Hypercube sampling Sobol sequences library"

This rapid scan revealed:
- SciPy has built-in QMC capabilities (since v1.7)
- SALib is the dominant sensitivity analysis library
- Multiple specialized Monte Carlo packages exist but with limited adoption

### Phase 2: Focused Discovery (20 minutes)

Investigated the most promising candidates based on mentions:
- **SALib**: Found ~60K weekly PyPI downloads, healthy maintenance
- **scipy.stats + scipy.stats.qmc**: Part of standard scientific stack (millions of users)
- **uncertainties**: Popular for error propagation
- **NumPy random**: Modern generator API (np.random.default_rng)

### Phase 3: Quick Validation (15 minutes)

Checked:
- Official documentation quality and examples
- Recent activity (2024 updates)
- Integration with NumPy/SciPy ecosystem
- Learning curve estimates from tutorials

### Phase 4: Alternative Scanning (10 minutes)

Reviewed specialized options:
- UQpy: 272 GitHub stars, academic focus
- Chaospy: Polynomial chaos expansion specialist
- PyMC: Bayesian MCMC focus (different use case)
- pyDOE2: Design of experiments (deprecated in favor of SciPy)

## Key Popularity Metrics Checked

1. **PyPI weekly downloads**
   - SALib: ~60,000/week
   - uncertainties: High (exact numbers not available)
   - scipy/numpy: Millions (standard library)

2. **GitHub stars** (attempted but API limited)
   - UQpy: 272 stars
   - SALib/uncertainties: Repository exists with active maintenance

3. **Documentation quality**
   - SciPy: Official tutorials, comprehensive
   - SALib: Complete API docs, research papers
   - NumPy: Best practices guides published 2024

4. **Stack Overflow mentions**
   - Heavy recommendation for scipy.stats.qmc over pyDOE
   - Multiple tutorials using NumPy random generator
   - SALib consistently recommended for sensitivity analysis

## Time Spent Breakdown

- Initial search: 15 min
- SALib investigation: 8 min
- SciPy/NumPy investigation: 12 min
- uncertainties package: 5 min
- Alternative libraries: 10 min
- Documentation writing: 10 min

**Total**: ~60 minutes

## Quick Validation Method

For each library:
1. Check if it has recent releases (2024 activity)
2. Look for "quick start" or "getting started" examples
3. Estimate time-to-first-working-example
4. Verify NumPy/SciPy compatibility

## Discovery Philosophy Applied

Following S1 methodology:
- **Speed over depth**: Focused on what's popular NOW
- **Popularity = reliability**: If millions use SciPy, it works
- **Ecosystem matters**: Prioritized libraries that play well with NumPy/SciPy
- **Documentation as proxy**: Good docs = mature library = popular
- **Avoid reinventing**: If it's built into SciPy, use that first

## Key Insights

1. **SciPy consolidation**: Many specialized packages are being deprecated in favor of scipy.stats.qmc
2. **Standard stack wins**: NumPy + SciPy + SALib covers 90% of use cases
3. **Niche vs general**: Specialized packages (PyMC, Chaospy) have steep learning curves
4. **Modern APIs**: Recent best practices emphasize np.random.default_rng() over old methods

## Recommendation Preview

Primary: **SciPy + NumPy + SALib combination**
- SciPy is already in the environment
- Time to first example: <30 minutes
- Covers all stated requirements
- Battle-tested by millions of users
