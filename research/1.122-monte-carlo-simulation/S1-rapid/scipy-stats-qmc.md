# Library Assessment: scipy.stats.qmc

## Quick Overview

**Package**: scipy.stats.qmc (Quasi-Monte Carlo submodule)
**Part of**: SciPy (standard scientific Python stack)
**Available since**: SciPy 1.7 (2021), actively maintained

## Popularity Metrics

**PyPI Downloads**: Millions (SciPy is a core dependency for scientific Python)
**GitHub**: Part of scipy/scipy repository (11K+ stars for entire SciPy project)
**Maintenance**: Official SciPy project, highly active development
**Last Update**: SciPy 1.16.2 (January 2025)

## What It Does

Provides quasi-Monte Carlo methods and sampling strategies:
- Sobol' sequences (scrambled and unscrambled)
- Halton sequences
- Latin Hypercube Sampling (LHS)
- Discrepancy measures (quality metrics)
- Sample scaling and transformation

## Quick "Does It Work" Validation

**Time to first working example**: 5 minutes

```python
from scipy.stats import qmc
import numpy as np

# Latin Hypercube Sampling
sampler = qmc.LatinHypercube(d=3)
sample = sampler.random(n=100)

# Sobol sequence
engine = qmc.Sobol(d=3, scramble=True)
sobol_sample = engine.random(n=256)
```

Works immediately, no configuration needed.

## Learning Curve

**Estimate**: Low (1-2 hours to proficiency)

- Clear official documentation with examples
- Integrates seamlessly with NumPy arrays
- Consistent API across different samplers
- Official tutorial: https://docs.scipy.org/doc/scipy/tutorial/stats/quasi_monte_carlo.html

## Strengths (S1 Perspective)

1. **Already installed**: Part of SciPy, zero installation friction
2. **Standard library**: If you know NumPy, you know this
3. **Battle-tested**: Used by millions of scientists/engineers
4. **Great docs**: Official SciPy tutorials and examples
5. **Active maintenance**: Receives updates with every SciPy release

## Limitations

- Only covers sampling methods (not sensitivity analysis)
- Requires understanding of QMC theory for optimal use
- Sample sizes need to be powers of 2 for some methods (Sobol')

## Use Case Fit

**Perfect for**:
- Latin Hypercube sampling for parameter variations
- Sobol sequences for efficient space-filling designs
- Quality assessment via discrepancy measures

**Not sufficient for**:
- Sensitivity analysis (use SALib)
- Error propagation (use uncertainties package)
- Complex Bayesian inference (use PyMC)

## Quick Start Resources

1. Official tutorial: https://docs.scipy.org/doc/scipy/tutorial/stats/quasi_monte_carlo.html
2. Blog post: https://blog.scientific-python.org/scipy/qmc-basics/
3. API reference: https://docs.scipy.org/doc/scipy/reference/stats.qmc.html

## S1 Verdict

**Adoption Score**: 10/10 (part of standard stack)
**Ease of Use**: 9/10 (simple API, excellent docs)
**Time to Value**: 10/10 (works immediately)

**Overall**: Essential component, use as primary sampling engine.
