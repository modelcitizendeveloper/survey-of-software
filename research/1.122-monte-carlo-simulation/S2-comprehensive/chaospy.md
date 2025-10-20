# Library Analysis: chaospy

## Overview

**Package:** chaospy
**Current Version:** 4.3+
**Maintenance:** Active (Jonathan Feinberg)
**License:** MIT
**Primary Use Case:** Uncertainty quantification via polynomial chaos expansions (PCE)
**GitHub:** https://github.com/jonathf/chaospy
**Documentation:** https://chaospy.readthedocs.io/

## Core Philosophy

Chaospy implements **polynomial chaos expansion** (PCE) methods for uncertainty quantification.
PCE represents model outputs as polynomial series in random inputs, enabling efficient uncertainty
propagation and sensitivity analysis with far fewer samples than Monte Carlo (typically 10-100×
fewer for models with <20 uncertain parameters).

## Core Capabilities

### Polynomial Chaos Expansion

**Concept:**
- Approximate model output Y = f(X) as polynomial series: Y ≈ Σᵢ cᵢΨᵢ(X)
- Ψᵢ: Orthogonal polynomials (basis functions)
- cᵢ: Coefficients determined by sparse sampling + regression/quadrature
- Once built, PCE is cheap to evaluate (polynomial, not full model)

**Advantages over Monte Carlo:**
- Sample efficiency: O(100) samples vs. O(10,000) for similar accuracy
- Analytical sensitivity analysis (derivatives of polynomial)
- Fast uncertainty propagation (evaluate polynomial, not model)

**Limitations:**
- Assumes smooth model response (polynomial-approximable)
- Curse of dimensionality: Exponential growth with parameters (works for D < ~20)
- Requires careful basis selection and sample strategy

### Distribution Library

**Comprehensive Distributions:**
```python
import chaospy as cp

# Built-in distributions
uniform = cp.Uniform(0, 10)
normal = cp.Normal(5, 2)
exponential = cp.Exponential(1.5)
lognormal = cp.LogNormal(0, 1)

# Multivariate with dependencies
joint = cp.J(
    cp.Uniform(0, 1),
    cp.Normal(0, 1),
    cp.Exponential(2)
)

# Copulas for correlation
correlation = [[1, 0.5], [0.5, 1]]
copula = cp.Nataf(joint, correlation)
```

**Custom Distributions:**
```python
# User-defined distribution
class TruncatedExponential(cp.Distribution):
    def __init__(self, rate, upper):
        self.rate = rate
        self.upper = upper
        super().__init__()

    def _cdf(self, x):
        norm = 1 - np.exp(-self.rate * self.upper)
        return (1 - np.exp(-self.rate * x)) / norm

    def _ppf(self, q):
        norm = 1 - np.exp(-self.rate * self.upper)
        return -np.log(1 - q * norm) / self.rate
```

### Sampling Methods

**Low-Discrepancy Sequences:**
```python
# Sobol sequence
samples = joint.sample(1024, rule='sobol')

# Halton sequence
samples = joint.sample(512, rule='halton')

# Latin Hypercube
samples = joint.sample(100, rule='latin_hypercube')

# Random (standard Monte Carlo)
samples = joint.sample(10000, rule='random')
```

**Advanced Sampling (for PCE construction):**
```python
# Quadrature nodes (for numerical integration)
nodes, weights = cp.generate_quadrature(3, joint, rule='gaussian')

# Sparse grid (efficient for high dimensions)
nodes, weights = cp.generate_quadrature(3, joint, rule='clenshaw_curtis',
                                         sparse=True)
```

### Polynomial Chaos Expansion Construction

**Point Collocation Method (Regression):**
```python
import chaospy as cp
import numpy as np

# 1. Define parameter distributions
joint = cp.J(
    cp.Uniform(50, 300),   # num_elevators (continuous approx)
    cp.Uniform(1, 10),     # capacity
    cp.Uniform(5, 30)      # speed
)

# 2. Generate samples (typically 2-3× polynomial terms)
polynomial_order = 3
samples = joint.sample(100, rule='halton')  # Smart sampling

# 3. Evaluate model at sample points
def elevator_model(params):
    # ... simulation ...
    return wait_time

model_output = np.array([elevator_model(s) for s in samples.T])

# 4. Create orthogonal polynomial basis
expansion = cp.generate_expansion(polynomial_order, joint)

# 5. Fit PCE via regression (point collocation)
pce_approx = cp.fit_regression(expansion, samples, model_output)

# 6. Use PCE for fast uncertainty propagation
# Generate new samples
mc_samples = joint.sample(10000, rule='sobol')
# Evaluate PCE (fast, no model calls!)
mc_results = pce_approx(*mc_samples)

# Statistics from PCE
mean = cp.E(pce_approx, joint)
variance = cp.Var(pce_approx, joint)
std = cp.Std(pce_approx, joint)

print(f"Wait time: {mean:.2f} ± {std:.2f} seconds")
```

**Spectral Projection (Quadrature):**
```python
# More accurate but requires quadrature rule
# (expensive for high dimensions)

# 1. Generate quadrature nodes and weights
nodes, weights = cp.generate_quadrature(3, joint, rule='gaussian')

# 2. Evaluate model at nodes
model_output = np.array([elevator_model(n) for n in nodes.T])

# 3. Fit PCE via spectral projection
expansion = cp.generate_expansion(3, joint)
pce_approx = cp.fit_quadrature(expansion, nodes, weights, model_output)

# Rest same as point collocation
```

### Sensitivity Analysis

**Sobol Indices from PCE (Analytical):**
```python
# After constructing PCE (pce_approx)

# First-order Sobol indices
sobol_first = cp.Sens_m(pce_approx, joint)
# [0.62, 0.23, 0.08] - variance contribution of each parameter

# Total-order Sobol indices
sobol_total = cp.Sens_t(pce_approx, joint)
# [0.68, 0.31, 0.12] - total effect including interactions

# Second-order interaction indices
sobol_second = cp.Sens_m2(pce_approx, joint)
# [[0, 0.04, 0.01], ...] - pairwise interactions

# Advantages:
# - Analytical (no additional sampling)
# - Exact for PCE approximation
# - Much faster than SALib Monte Carlo methods
```

### Uncertainty Propagation

**Statistics from PCE:**
```python
# Moments (analytical from PCE)
mean = cp.E(pce_approx, joint)
variance = cp.Var(pce_approx, joint)
skewness = cp.Skew(pce_approx, joint)
kurtosis = cp.Kurt(pce_approx, joint)

# Percentiles (via sampling PCE)
samples_pce = pce_approx(*joint.sample(10000))
percentiles = np.percentile(samples_pce, [2.5, 50, 97.5])

# Correlation between inputs and output
# (via sensitivity analysis)
```

## Integration Patterns

### With NumPy/SciPy

**Seamless Array Operations:**
```python
# Chaospy distributions work like scipy.stats
dist = cp.Normal(0, 1)

# Generate samples (NumPy arrays)
samples = dist.sample(1000)  # shape: (1000,)

# PDF, CDF, PPF
pdf_vals = dist.pdf(samples)
cdf_vals = dist.cdf(samples)
quantiles = dist.inv(cdf_vals)  # PPF equivalent

# Integration with scipy.stats
from scipy.stats import norm
scipy_samples = norm.rvs(size=1000)
# Use in chaospy PCE construction
```

### With SALib (Comparison/Validation)

**PCE Sensitivity vs. SALib:**
```python
# 1. Build PCE and compute Sobol analytically
pce_sobol = cp.Sens_t(pce_approx, joint)

# 2. Validate with SALib Monte Carlo
from SALib.sample import saltelli
from SALib.analyze import sobol

problem = {
    'num_vars': 3,
    'names': ['x1', 'x2', 'x3'],
    'bounds': [[50, 300], [1, 10], [5, 30]]
}

saltelli_samples = saltelli.sample(problem, 1024)
saltelli_output = np.array([elevator_model(s) for s in saltelli_samples])
salib_sobol = sobol.analyze(problem, saltelli_output)

# Compare
print(f"PCE Sobol: {pce_sobol}")
print(f"SALib Sobol: {salib_sobol['ST']}")
# Should agree closely if PCE is accurate
```

## Performance Characteristics

### Sample Efficiency

**Polynomial Chaos vs. Monte Carlo:**
| Method                 | Samples Required | Model Evals | Notes                        |
|------------------------|------------------|-------------|------------------------------|
| Monte Carlo (crude)    | 10,000           | 10,000      | Baseline                     |
| Quasi-MC (Sobol)       | 1,000            | 1,000       | 10× fewer                    |
| PCE (order 3, D=10)    | 200-500          | 200-500     | 20-50× fewer                 |
| PCE (order 4, D=10)    | 500-1,000        | 500-1,000   | Still ~10× fewer             |

**Dimensionality Limit:**
- D ≤ 10: Excellent (order 3-5 feasible)
- D = 10-20: Good (order 2-3, sparse grids help)
- D > 20: Challenging (curse of dimensionality, consider screening first)

### Computational Cost

**PCE Construction (one-time):**
- Sampling: Negligible (~1 ms for 1000 samples)
- Model evaluations: Dominates (depends on model)
- Regression: Fast (~10 ms for 1000 samples, order 3)
- Total: Approximately N × t_model where N = 100-1000

**PCE Evaluation (amortized):**
- 10,000 evaluations of PCE: ~1 ms (polynomial evaluation)
- 10,000 evaluations of model: seconds to hours
- Speedup: 1000-1,000,000× for uncertainty propagation

**Example:**
```python
# Model: 1 second per evaluation
# PCE construction: 500 samples × 1 sec = 500 seconds (~8 min)

# After construction:
# Monte Carlo (model): 10,000 × 1 sec = 10,000 sec (~3 hours)
# Monte Carlo (PCE): 10,000 × 0.0001 sec = 1 sec

# For multiple UQ queries: PCE amortizes construction cost
```

### Accuracy

**Error Sources:**
- Polynomial approximation error (smooth models → low error)
- Sampling error (regression) or quadrature error (spectral)
- Typically <5% relative error for smooth models with order 3-5

**Validation:**
```python
# Cross-validation
from sklearn.model_selection import KFold

kf = KFold(n_splits=5)
errors = []

for train_idx, test_idx in kf.split(samples.T):
    train_samples = samples[:, train_idx]
    train_output = model_output[train_idx]
    test_samples = samples[:, test_idx]
    test_output = model_output[test_idx]

    pce_train = cp.fit_regression(expansion, train_samples, train_output)
    pce_pred = pce_train(*test_samples)

    error = np.mean((pce_pred - test_output)**2)
    errors.append(error)

print(f"Mean CV error: {np.mean(errors):.3f}")
```

## API Quality

### Strengths

1. **Composable Design:** Distributions, sampling, PCE construction modular
2. **NumPy-Compatible:** Arrays throughout, easy integration
3. **Comprehensive:** Distributions, sampling, PCE, sensitivity all in one package

### Learning Curve

**Moderate to Steep:**
- Requires understanding of polynomial chaos theory
- Choosing polynomial order, sampling strategy non-trivial
- Validating PCE accuracy requires statistical knowledge

**Example Complexity:**
```python
# Simple task: propagate uncertainty
# Chaospy: ~20 lines (define dist, sample, build PCE, evaluate)
# scipy.stats: ~5 lines (sample, evaluate model, summarize)

# But chaospy amortizes for multiple queries
```

## Limitations

### Curse of Dimensionality

**Polynomial Terms Grow Exponentially:**
- Order p, dimension D: ~(p+D)! / (p! D!) terms
- Example: p=3, D=5 → 56 terms (manageable)
- Example: p=3, D=15 → 816 terms (requires 1,600+ samples)

**Mitigation:**
- Use screening (Morris method) to reduce D
- Sparse grids for quadrature
- Adaptive sparse PCE methods

### Smoothness Requirement

**PCE Assumes Polynomial-Approximable Functions:**
- Works well: Smooth, continuous model responses
- Struggles with: Discontinuities, sharp transitions, threshold effects

**Example Failure:**
```python
# Model with threshold
def model_with_threshold(x):
    return 10 if x < 5 else 100

# PCE will smooth out the jump, losing accuracy
```

### No Built-in Parallelization

**Manual Parallelization Needed:**
```python
from multiprocessing import Pool

def evaluate_model_wrapper(sample):
    return elevator_model(sample)

with Pool(8) as pool:
    model_output = pool.map(evaluate_model_wrapper, samples.T)

# Then build PCE
pce_approx = cp.fit_regression(expansion, samples, np.array(model_output))
```

## Maintenance and Community

### Development Activity

**Release Cadence:** 1-2 releases per year
**Maintainer:** Primarily Jonathan Feinberg (single maintainer)
**Issue Response:** Within weeks
**Breaking Changes:** Rare, stable API

### Community Health

**Citations:** ~100 academic papers
**GitHub Stars:** ~300
**Documentation:** Comprehensive, with tutorials
**Smaller Community:** Less Stack Overflow activity than scipy/numpy

## Production Readiness

### Reliability

**Academic Validation:**
- Published in Journal of Computational Science
- Benchmarked against other PCE implementations
- Used in engineering research

**Stability:**
- Mature codebase (since 2015)
- Test suite covers core functionality
- Few critical bugs reported

### Deployment

**Dependencies:** NumPy, SciPy, numpoly (polynomial library)
**Package Size:** ~2 MB
**Platform Support:** Pure Python, cross-platform

## Recommendations

### When to Use Chaospy

**1. Expensive Models (>1 second per evaluation):**
- PCE construction cost (500 evals) amortizes quickly
- Subsequent UQ queries are nearly free

**2. Multiple UQ Queries:**
- Build PCE once, use for many scenarios
- Example: Vary parameter ranges, compute statistics repeatedly

**3. Moderate Dimensionality (D < 20):**
- PCE sample efficiency shines
- Analytical Sobol indices are bonus

**4. Smooth Model Response:**
- Polynomial approximation accurate
- Validate with cross-validation

### When NOT to Use Chaospy

**1. Fast Models (<0.1 sec per evaluation):**
- Monte Carlo with 10,000 samples takes ~10 seconds
- PCE construction overhead not justified
- Use scipy.stats directly

**2. High Dimensionality (D > 20):**
- Curse of dimensionality limits PCE
- Use screening (Morris) + reduced model
- Or stick with Monte Carlo / quasi-MC

**3. Discontinuous or Non-Smooth Models:**
- PCE will be inaccurate
- Use Monte Carlo instead
- Example: Threshold-based logic, if-else chains

**4. Quick Exploratory Analysis:**
- Setting up PCE properly takes time
- Use scipy.stats for rapid prototyping

### Integration Strategy for OR Consulting

**Use Chaospy When:**
- Elevator simulation is computationally expensive (>5 sec/eval)
- Need to perform many UQ queries (vary distributions, compute stats)
- Have <15 uncertain parameters
- Model response is smooth

**Workflow:**
```python
# 1. Define parameter distributions
params = cp.J(
    cp.Uniform(50, 300),   # num_elevators
    cp.Uniform(1, 10),     # capacity
    cp.Uniform(5, 30),     # speed
    # ... up to ~15 parameters
)

# 2. Build PCE (one-time cost: 500 model evaluations)
samples = params.sample(500, rule='halton')
outputs = [expensive_elevator_simulation(s) for s in samples.T]
expansion = cp.generate_expansion(3, params)
pce = cp.fit_regression(expansion, samples, outputs)

# 3. Fast UQ queries (no additional model calls)
mean_wait = cp.E(pce, params)
std_wait = cp.Std(pce, params)
percentiles = pce(*params.sample(10000, rule='sobol'))
sobol_indices = cp.Sens_t(pce, params)

# 4. What-if scenarios (instant)
# Change parameter distributions, recompute stats from PCE
params_optimistic = cp.J(cp.Uniform(60, 300), ...)
mean_optimistic = cp.E(pce, params_optimistic)
```

**Combine with SALib for Validation:**
```python
# Validate PCE Sobol indices with SALib
# (If PCE Sobol ≈ SALib Sobol, PCE is accurate)
```

## Summary Assessment

**Strengths:**
- Extreme sample efficiency (10-100× fewer than MC)
- Analytical sensitivity analysis (Sobol indices)
- Fast uncertainty propagation after construction
- Comprehensive distribution library

**Weaknesses:**
- Curse of dimensionality (D < ~20)
- Requires smooth model response
- Steeper learning curve than direct MC
- Smaller community, single maintainer

**Verdict for OR Consulting:**
**High Priority for Expensive Models** - If elevator simulations are computationally expensive (>1 sec per evaluation) and model response is smooth, chaospy can reduce UQ costs by 10-100×. The analytical Sobol indices are a significant bonus. However, for fast models or high-dimensional problems, stick with scipy.stats + SALib.

**Recommended Role in Toolkit:**
- **Primary:** Expensive models (>1 sec/eval) with D < 15 parameters
- **Secondary:** Multiple UQ queries on same model (amortizes construction)
- **Tertiary:** Academic validation (compare PCE vs. MC results)

**Best Used In Combination:**
1. **Screening:** SALib Morris method to reduce D from 20 → 10
2. **PCE Construction:** Chaospy on reduced parameter set
3. **Validation:** SALib Sobol on small sample to verify PCE accuracy
4. **Production:** Use PCE for fast UQ in client deliverables
