# Library Analysis: scipy.stats and scipy.stats.qmc

## Overview

**Package:** scipy.stats + scipy.stats.qmc
**Version Range:** ≥1.7 (qmc added), ≥1.17 recommended (PCG64 default)
**Maintenance:** Active (core SciPy project)
**License:** BSD-3-Clause
**Primary Use Case:** General-purpose statistical distributions and quasi-Monte Carlo sampling

## Core Capabilities

### Random Number Generation (numpy.random.Generator)

**Modern RNG (NumPy 1.17+):**
- PCG64 bit generator (default since 1.17)
- 40% faster than Mersenne Twister (MT19937)
- Superior statistical properties (passes TestU01)
- Smaller state size (vs. MT's 2.5 kB)

**Performance Characteristics:**
- Ziggurat methods for normal/exponential/gamma: 2-10× faster than legacy
- Vectorized generation: 100 integers in 1.91 μs (0.019 μs/integer)
- 3× faster than Python's random.random() for bulk generation
- Single value generation slower (amortizes cost over arrays)

**Quality Guarantees:**
- Cryptographically secure seeding
- Independent streams via SeedSequence
- Reproducibility across platforms

### Probability Distributions (scipy.stats)

**Distribution Library:**
- 100+ continuous distributions
- 20+ discrete distributions
- Multivariate: multivariate_normal, multivariate_t
- Custom distributions via rv_continuous/rv_discrete base classes

**Key Methods:**
- rvs(): Random variate sampling (vectorized)
- pdf()/pmf(): Probability density/mass functions
- cdf()/ppf(): Cumulative distribution and inverse
- stats(): Mean, variance, skewness, kurtosis
- fit(): Maximum likelihood parameter estimation

**Performance:**
- Based on compiled C/Fortran code
- Self-implemented samplers ~41× slower than SciPy built-ins
- Excellent numerical stability

### Quasi-Monte Carlo (scipy.stats.qmc)

**Low-Discrepancy Sequences:**
- Sobol: Best for 2^m samples, extensible in n and d, scrambling support
- Halton: Arbitrary sample sizes, earlier dimensions better, slower convergence
- LatinHypercube: Strength 1/2/3 support, optimization schemes (random-cd, lloyd)

**Convergence Advantage:**
- QMC error: O(1/n) vs. Monte Carlo O(1/√n)
- Scrambling improves convergence, prevents patterns in high dimensions
- Discrepancy measures available for quality assessment

**API Design:**
```python
from scipy.stats import qmc

# Sobol sequence (recommended for 2^m samples)
sampler = qmc.Sobol(d=3, scramble=True, seed=42)
sample = sampler.random(n=128)  # [0,1)^3

# Latin Hypercube (arbitrary sample sizes)
lhs = qmc.LatinHypercube(d=3, strength=2, optimization='random-cd')
sample_lhs = lhs.random(n=100)

# Scale to parameter bounds
l_bounds = [50, 1, 5]
u_bounds = [300, 10, 30]
scaled = qmc.scale(sample, l_bounds, u_bounds)
```

### Resampling and Bootstrap (scipy.stats)

**scipy.stats.bootstrap:**
- Methods: 'percentile', 'basic', 'BCa' (bias-corrected accelerated)
- Default BCa for better coverage properties
- Vectorized for performance
- Automatic confidence interval construction

**Example:**
```python
from scipy.stats import bootstrap

result = bootstrap(
    (data,),
    np.median,
    confidence_level=0.95,
    method='BCa',
    n_resamples=10000,
    random_state=42
)
# result.confidence_interval: ConfidenceInterval(low=..., high=...)
```

## Integration Patterns

### With NumPy

**Seamless Array Operations:**
- All outputs are NumPy arrays
- Broadcasting support for vectorized operations
- Memory-efficient views where possible

**Example - Parameter Sweep:**
```python
import numpy as np
from scipy.stats import norm, qmc

# Generate LHS samples for 3 parameters
sampler = qmc.LatinHypercube(d=3)
samples = sampler.random(n=1000)

# Scale to parameter ranges
params = qmc.scale(samples, [50, 1, 5], [300, 10, 30])

# Run model (vectorized)
results = elevator_model(
    num_elevators=params[:, 0],
    capacity=params[:, 1],
    speed=params[:, 2]
)

# Statistical analysis
mean_wait = np.mean(results)
ci_low, ci_high = np.percentile(results, [2.5, 97.5])
```

### With Pandas

**Distribution Fitting:**
```python
import pandas as pd
from scipy.stats import norm

df = pd.DataFrame({'wait_time': simulation_results})
mu, sigma = norm.fit(df['wait_time'])
df['probability'] = norm.pdf(df['wait_time'], mu, sigma)
```

### Custom Distributions

**Creating Domain-Specific Distributions:**
```python
from scipy.stats import rv_continuous

class truncated_exponential_gen(rv_continuous):
    def _pdf(self, x, lam, upper):
        normalization = 1 - np.exp(-lam * upper)
        return lam * np.exp(-lam * x) / normalization

truncated_exp = truncated_exponential_gen(name='truncated_exp', a=0)
```

## Performance Characteristics

### Benchmark Data

**Random Number Generation (PCG64):**
- 1M normal samples: ~5 ms
- 1M uniform samples: ~2 ms
- 1M exponential samples: ~3 ms

**Quasi-Monte Carlo Sampling:**
- Sobol 1024 points, d=10: ~0.5 ms
- LHS 1000 points, d=10: ~2 ms (with optimization)

**Bootstrap Confidence Intervals:**
- 10,000 resamples, n=1000, median: ~200 ms
- BCa method overhead: ~20% vs. percentile

### Scalability

**Vectorization Benefits:**
- Single RNG call for array >> multiple scalar calls
- SIMD optimizations in modern NumPy
- Multithreading support via numba/cython extensions

**Memory Efficiency:**
- PCG64 state: 32 bytes
- Minimal overhead for distribution objects
- Generator reuse recommended

## API Quality

### Strengths

1. **Consistent Design:** Follows SciPy conventions (rvs, pdf, cdf pattern)
2. **Well-Documented:** Comprehensive API reference, mathematical descriptions
3. **Type Safety:** NumPy arrays with predictable dtypes
4. **Composability:** Easy to chain operations (sample → transform → analyze)

### Learning Curve

**Beginner-Friendly:**
- Simple API for common tasks
- Good error messages
- Extensive examples in documentation

**Advanced Features:**
- Custom distributions require understanding rv_continuous
- QMC methods need statistical background
- Performance tuning requires NumPy expertise

## Limitations

### What's Missing

**No Built-in Sensitivity Analysis:**
- Requires external library (SALib) or manual implementation
- No Sobol indices, Morris method, FAST
- Must combine with other tools for global SA

**No Variance Reduction Techniques:**
- No antithetic variates support
- No control variates framework
- No importance sampling helpers

**Limited Uncertainty Propagation:**
- No automatic error propagation
- No correlation tracking through calculations
- Must manually implement or use uncertainties package

**No Copula Support:**
- Multivariate distributions limited (normal, t)
- No Archimedean copulas
- Use statsmodels.distributions.copula for advanced needs

## Maintenance and Community

### Development Activity

**Release Cadence:** 2-3 major releases per year
**Contributors:** 500+ (SciPy project)
**Issue Response:** Typically within days
**Breaking Changes:** Rare, well-documented deprecation cycle

### Community Health

**Stack Overflow:** 10,000+ scipy.stats questions
**Documentation:** Excellent tutorials, user guide, API reference
**Books:** Multiple textbooks use SciPy examples
**Industry Adoption:** Ubiquitous in scientific Python

## Production Readiness

### Reliability

**Battle-Tested:**
- In production since 2001
- Used by major scientific institutions
- Extensive test suite (90%+ coverage)

**Numerical Stability:**
- Careful handling of edge cases
- Validated against statistical reference implementations
- Continuous benchmarking against R, MATLAB

### Deployment

**Dependencies:** NumPy (required), minimal additional
**Package Size:** ~40 MB (full SciPy)
**Platform Support:** Linux, macOS, Windows (pre-built wheels)

## Recommendations

### Best Use Cases

1. **Baseline Monte Carlo Simulations**
   - Standard parameter sampling
   - Confidence interval construction
   - Distribution fitting and hypothesis testing

2. **Quasi-Monte Carlo Studies**
   - When sample efficiency matters
   - High-dimensional parameter spaces
   - Convergence guarantees needed

3. **Integration with Broader SciPy Ecosystem**
   - Optimization (scipy.optimize)
   - Interpolation (scipy.interpolate)
   - Linear algebra (scipy.linalg)

### When to Look Elsewhere

**Need Global Sensitivity Analysis:** Use SALib
**Need Error Propagation:** Use uncertainties package
**Need Bayesian MCMC:** Use PyMC
**Need Polynomial Chaos:** Use chaospy
**Need Industrial UQ Suite:** Use OpenTURNS

## Summary Assessment

**Strengths:**
- Fast, reliable random number generation (PCG64)
- Comprehensive distribution library
- Modern QMC methods (Sobol, Halton, LHS)
- Excellent integration with NumPy ecosystem
- Production-grade stability

**Weaknesses:**
- No built-in sensitivity analysis
- Limited to sampling and basic statistics
- Requires combination with other libraries for advanced UQ

**Verdict:** Essential foundation for any Monte Carlo work in Python, but insufficient alone for comprehensive OR consulting needs. Best used as the sampling engine combined with specialized libraries for sensitivity analysis and uncertainty propagation.
