# Library Assessment: SALib

## Quick Overview

**Package**: SALib (Sensitivity Analysis Library in Python)
**Repository**: https://github.com/SALib/SALib
**Domain**: Global sensitivity analysis methods

## Popularity Metrics

**PyPI Downloads**: ~60,000 per week
**GitHub Stars**: 800+ (estimated from search results)
**Maintenance**: Healthy - positive release cadence
**Last Update**: Active in 2024
**Community**: 50+ open source contributors

## What It Does

Implements global sensitivity analysis methods:
- Sobol' indices (variance-based)
- Morris method (screening)
- FAST (Fourier Amplitude Sensitivity Test)
- DGSM, PAWN, HDMR methods
- Fractional factorial designs

## Quick "Does It Work" Validation

**Time to first working example**: 15 minutes

```python
from SALib.sample import saltelli
from SALib.analyze import sobol

# Define problem
problem = {
    'num_vars': 3,
    'names': ['x1', 'x2', 'x3'],
    'bounds': [[0, 1], [0, 1], [0, 1]]
}

# Generate samples
param_values = saltelli.sample(problem, 1024)

# Run model (your function)
Y = evaluate_model(param_values)

# Analyze
Si = sobol.analyze(problem, Y)
print(Si['S1'])  # First-order indices
print(Si['ST'])  # Total-order indices
```

Straightforward workflow, well-documented.

## Learning Curve

**Estimate**: Medium (2-4 hours to proficiency)

- Requires understanding of sensitivity analysis concepts
- Clear examples in documentation
- Two-step process: sample generation, then analysis
- Need to integrate with your own model code

## Strengths (S1 Perspective)

1. **Domain leader**: THE library for sensitivity analysis in Python
2. **Published research**: Academic paper in Journal of Open Source Software
3. **Multiple methods**: 7+ sensitivity analysis techniques
4. **Active community**: 50+ contributors, regular updates
5. **Good documentation**: https://salib.readthedocs.io/
6. **Production ready**: Used in research and industry

## Limitations

- Requires more setup than basic Monte Carlo
- Need to understand which method to use (Sobol vs Morris vs FAST)
- Sample generation can be computationally expensive
- Doesn't do random number generation (use NumPy for that)

## Use Case Fit

**Perfect for**:
- Parameter sensitivity analysis (±20% variations)
- Identifying important parameters in elevator models
- Variance decomposition
- Screening many parameters (Morris method)
- Risk quantification decisions

**Not sufficient for**:
- Random number generation (use NumPy)
- Sampling strategies (use scipy.stats.qmc)
- Error propagation (use uncertainties)

## Integration Points

Works well with:
- NumPy arrays (input/output)
- SciPy distributions
- Your existing simulation code
- Pandas for results analysis

## Quick Start Resources

1. Official docs: https://salib.readthedocs.io/
2. GitHub: https://github.com/SALib/SALib
3. Paper: Herman & Usher (2017), Journal of Open Source Software
4. Examples: https://salib.readthedocs.io/en/latest/basics.html

## S1 Verdict

**Adoption Score**: 9/10 (dominant in its niche)
**Ease of Use**: 7/10 (requires SA knowledge)
**Time to Value**: 7/10 (15-30 min for first result)

**Overall**: Essential for sensitivity analysis. No viable alternative with similar adoption.
