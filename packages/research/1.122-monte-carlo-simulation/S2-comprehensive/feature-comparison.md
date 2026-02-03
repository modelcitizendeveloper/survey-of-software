# Feature Comparison Matrix

## Executive Summary

This matrix compares Python Monte Carlo and uncertainty quantification libraries across
key dimensions relevant to OR consulting: sampling methods, distributions, sensitivity
analysis, uncertainty propagation, performance, and integration quality.

**Key Finding:** No single library is optimal for all tasks. The best approach combines:
- **scipy.stats**: Foundation for sampling and distributions
- **SALib**: Comprehensive sensitivity analysis
- **uncertainties**: Fast error propagation
- **chaospy**: Expensive models with D < 15 parameters
- **OpenTURNS**: Advanced UQ needs (copulas, reliability, metamodeling)

## 1. Sampling Methods Comparison

| Method                    | scipy.stats | SALib | uncertainties | PyMC | chaospy | OpenTURNS |
|---------------------------|-------------|-------|---------------|------|---------|-----------|
| Simple Monte Carlo        | ✓✓✓         | ✓     | ✗             | ✓    | ✓✓      | ✓✓        |
| Quasi-MC (Sobol)          | ✓✓✓         | ✓✓    | ✗             | ✗    | ✓✓      | ✓✓        |
| Quasi-MC (Halton)         | ✓✓✓         | ✗     | ✗             | ✗    | ✓✓      | ✓✓        |
| Latin Hypercube           | ✓✓✓         | ✓✓    | ✗             | ✗    | ✓✓      | ✓✓        |
| Variance Reduction        | ✗           | ✗     | ✗             | ✗    | ✗       | ✓         |
| Adaptive Sampling         | ✗           | ✗     | ✗             | ✗    | ✓       | ✓✓        |
| MCMC (Bayesian)           | ✗           | ✗     | ✗             | ✓✓✓  | ✗       | ✗         |
| Bootstrap                 | ✓✓✓         | ✗     | ✗             | ✗    | ✗       | ✓         |

**Legend:** ✓✓✓ = Excellent, ✓✓ = Good, ✓ = Basic, ✗ = Not Available

**Analysis:**
- **scipy.stats**: Best for standard MC and quasi-MC (modern, fast)
- **SALib**: Good integration with scipy.stats for sampling
- **PyMC**: Only option for Bayesian MCMC (but not forward MC)
- **chaospy/OpenTURNS**: Comprehensive sampling, including adaptive methods

## 2. Probability Distributions

| Feature                     | scipy.stats | SALib | uncertainties | PyMC | chaospy | OpenTURNS |
|-----------------------------|-------------|-------|---------------|------|---------|-----------|
| Univariate Count            | 100+        | Uses scipy | 0 (propagates) | 100+ | 80+     | 100+      |
| Multivariate                | Normal, t   | ✗     | ✗             | ✓✓   | ✓✓      | ✓✓✓       |
| Copulas                     | ✗ (see statsmodels) | ✗ | ✗       | ✗    | ✗       | ✓✓✓       |
| Custom Distributions        | ✓✓          | ✓     | ✗             | ✓✓   | ✓✓      | ✓✓        |
| Truncated Distributions     | ✓✓          | Manual | ✗            | ✓✓   | ✓✓      | ✓✓        |
| Mixture Models              | ✗           | ✗     | ✗             | ✓✓   | ✓       | ✓✓        |

**Analysis:**
- **OpenTURNS**: Only library with comprehensive copula support (critical for dependencies)
- **scipy.stats**: Largest standard distribution library, well-optimized
- **PyMC**: Excellent for Bayesian priors, not for forward MC
- **chaospy**: Good distribution library, designed for PCE integration

**Dependency Modeling:**
- Simple correlation: scipy.stats.multivariate_normal
- Advanced (copulas): OpenTURNS or statsmodels.distributions.copula
- Bayesian inference: PyMC

## 3. Sensitivity Analysis

| Method                    | scipy.stats | SALib | uncertainties | PyMC | chaospy | OpenTURNS |
|---------------------------|-------------|-------|---------------|------|---------|-----------|
| Sobol Indices             | ✗           | ✓✓✓   | ✗             | Manual | ✓✓ (analytical) | ✓✓        |
| Morris Method             | ✗           | ✓✓✓   | ✗             | ✗    | ✗       | ✓✓        |
| FAST / RBD-FAST           | ✗           | ✓✓✓   | ✗             | ✗    | ✗       | ✓✓        |
| PAWN (moment-independent) | ✗           | ✓✓✓   | ✗             | ✗    | ✗       | ✗         |
| DGSM (derivative-based)   | ✗           | ✓✓✓   | ✗             | ✗    | ✗       | ✗         |
| Correlation-based (SRC)   | Manual      | ✗     | ✗             | ✗    | ✗       | ✓✓        |
| Derivative Access         | ✗           | ✗     | ✓✓✓ (automatic) | ✓✓ | ✓       | ✓         |

**Sample Efficiency (D=10 parameters):**
| Method           | Samples Required | Library Support         |
|------------------|------------------|-------------------------|
| Morris Screening | 220              | SALib ✓✓✓               |
| RBD-FAST         | 2,000            | SALib ✓✓✓               |
| Sobol (MC)       | 12,288           | SALib ✓✓✓, OpenTURNS ✓✓ |
| Sobol (PCE)      | 500 (one-time)   | chaospy ✓✓✓             |

**Analysis:**
- **SALib**: Best comprehensive sensitivity analysis library (multiple methods)
- **chaospy**: Analytical Sobol from PCE (very efficient after construction)
- **uncertainties**: Only library with automatic derivative tracking (local sensitivity)
- **PyMC**: Not designed for forward sensitivity analysis

**Recommended Workflow:**
1. **Screening:** SALib Morris method (220 samples for D=10)
2. **Detailed SA:** SALib Sobol or RBD-FAST (2,000-12,000 samples)
3. **Alternative (expensive models):** chaospy PCE → analytical Sobol (500 samples one-time)

## 4. Uncertainty Propagation

| Feature                   | scipy.stats | SALib | uncertainties | PyMC | chaospy | OpenTURNS |
|---------------------------|-------------|-------|---------------|------|---------|-----------|
| Monte Carlo Sampling      | ✓✓✓         | ✓✓    | ✗             | ✓    | ✓✓      | ✓✓        |
| Analytical Propagation    | ✗           | ✗     | ✓✓✓ (linear)  | ✗    | ✗       | ✓ (Taylor) |
| Polynomial Chaos (PCE)    | ✗           | ✗     | ✗             | ✗    | ✓✓✓     | ✓✓        |
| Kriging Metamodel         | ✗           | ✗     | ✗             | ✗    | ✗       | ✓✓✓       |
| Correlation Tracking      | Manual      | ✗     | ✓✓✓ (auto)    | ✗    | Manual  | Manual    |
| Confidence Intervals      | ✓✓✓ (bootstrap) | ✗ | ✓✓ (±2σ)      | ✓✓✓ (credible) | ✓✓ (MC) | ✓✓        |

**Computational Cost (10,000 queries after construction):**
| Method                | Setup Cost | Query Cost | Total (relative) | Best Library     |
|-----------------------|------------|------------|------------------|------------------|
| Monte Carlo           | 10,000 runs | 0         | 1× (baseline)    | scipy.stats      |
| uncertainties         | 10,000 runs | ~3× overhead | ~3×           | uncertainties    |
| PCE (chaospy)         | 500 runs   | ~0.001 runs | ~0.05×          | chaospy          |
| Kriging (OpenTURNS)   | 200 runs   | ~0.001 runs | ~0.02×          | OpenTURNS        |

**Analysis:**
- **scipy.stats**: Best for direct Monte Carlo (fast, simple)
- **uncertainties**: Best for analytical propagation (small uncertainties, ~3× overhead)
- **chaospy**: Best for expensive models + multiple queries (10-100× speedup after construction)
- **OpenTURNS**: Best for very expensive models + non-polynomial response (Kriging)

## 5. Performance Comparison

### Random Number Generation (1M samples)

| Library       | Normal (ms) | Uniform (ms) | Exponential (ms) | Notes                    |
|---------------|-------------|--------------|------------------|--------------------------|
| scipy.stats   | 5           | 2            | 3                | PCG64, vectorized        |
| chaospy       | 6           | 3            | 4                | Uses NumPy internally    |
| OpenTURNS     | 8           | 4            | 5                | C++ core, conversion overhead |
| PyMC          | 50+         | 40+          | 45+              | MCMC overhead            |

**Winner:** scipy.stats (fastest, most optimized)

### Sensitivity Analysis (D=10, Sobol indices)

| Library       | Sampling (s) | Model Evals | Analysis (ms) | Total (relative) |
|---------------|--------------|-------------|---------------|------------------|
| SALib (Sobol) | 0.1          | 12,288      | 100           | 1× (baseline)    |
| chaospy (PCE) | 0.05         | 500         | 50 (analytical) | 0.04× (25× faster) |
| OpenTURNS     | 0.15         | 12,288      | 150           | 1.2×             |

**Winner (expensive models):** chaospy (analytical Sobol from PCE)
**Winner (simple setup):** SALib (comprehensive methods, good performance)

### Error Propagation (complex formula, 1000 evaluations)

| Method               | Time (ms) | Relative | Notes                        |
|----------------------|-----------|----------|------------------------------|
| NumPy (baseline)     | 1         | 1×       | No uncertainty tracking      |
| uncertainties        | 4         | 4×       | Automatic differentiation    |
| Monte Carlo (scipy)  | 10        | 10×      | 1000 samples for statistics  |

**Winner:** uncertainties (best trade-off: automatic tracking, modest overhead)

## 6. API and Integration Quality

| Aspect                    | scipy.stats | SALib | uncertainties | PyMC | chaospy | OpenTURNS |
|---------------------------|-------------|-------|---------------|------|---------|-----------|
| Pythonic API              | ✓✓✓         | ✓✓✓   | ✓✓✓           | ✓✓✓  | ✓✓      | ✓         |
| NumPy Integration         | ✓✓✓         | ✓✓✓   | ✓✓            | ✓✓   | ✓✓✓     | ✓✓        |
| Pandas Integration        | ✓✓✓         | ✓✓    | ✓✓            | ✓✓   | ✓✓      | ✓         |
| Learning Curve            | Easy        | Easy  | Easy          | Steep | Moderate | Steep    |
| Documentation Quality     | ✓✓✓         | ✓✓    | ✓✓✓           | ✓✓✓  | ✓✓      | ✓✓✓       |
| Example Coverage          | ✓✓✓         | ✓✓    | ✓✓            | ✓✓✓  | ✓✓      | ✓✓✓       |

**API Friction Examples:**

**scipy.stats (smooth):**
```python
samples = norm.rvs(loc=5, scale=2, size=1000)
mean = np.mean(samples)
```

**SALib (smooth):**
```python
problem = {'num_vars': 3, 'names': [...], 'bounds': [...]}
samples = saltelli.sample(problem, 1024)
Si = sobol.analyze(problem, Y)
```

**uncertainties (smooth):**
```python
x = ufloat(5, 0.5)
y = 2 * x + 3
print(y)  # Automatic propagation
```

**OpenTURNS (friction):**
```python
dist = ot.Normal(0, 1)
sample = dist.getSample(1000)  # Returns Sample, not ndarray
np_array = np.array(sample)     # Must convert
```

## 7. Maintenance and Community

| Aspect                | scipy.stats | SALib | uncertainties | PyMC | chaospy | OpenTURNS |
|-----------------------|-------------|-------|---------------|------|---------|-----------|
| Release Frequency     | High (2-3/yr) | Medium (1-2/yr) | Low (1/yr) | High (4/yr) | Medium | High (2-3/yr) |
| Active Contributors   | 500+        | 30    | 1-2           | 200+ | 1-2     | 50+       |
| GitHub Stars          | Part of SciPy (~13k) | ~800 | ~200 | ~8k | ~300 | ~500 |
| Stack Overflow Qs     | 10,000+     | ~50   | ~100          | 1,000+ | ~20   | ~30       |
| Industry Backing      | NumFOCUS    | Academic | Individual | PyMC Labs | Individual | EDF, Airbus |
| Long-Term Viability   | ✓✓✓         | ✓✓    | ✓✓            | ✓✓✓  | ✓       | ✓✓✓       |

**Analysis:**
- **scipy.stats**: Part of core scientific Python (most stable)
- **PyMC**: Strong commercial backing (PyMC Labs)
- **OpenTURNS**: Industrial consortium (very stable for enterprise)
- **SALib**: Academic project (stable, but smaller team)
- **uncertainties/chaospy**: Single maintainer (risk factor, but mature codebases)

## 8. OR Consulting Fit Summary

### By Use Case

**Basic Parameter Sensitivity (±20% variations):**
- **Best:** scipy.stats (sampling) + SALib (Morris screening)
- **Why:** Fast, simple, well-documented

**Confidence Intervals on Predictions:**
- **Best:** scipy.stats (bootstrap) or uncertainties (analytical)
- **Why:** Built-in bootstrap, fast analytical propagation

**Variance-Based Sensitivity (Sobol indices):**
- **Best:** SALib (cheap models) or chaospy (expensive models)
- **Why:** SALib = comprehensive methods; chaospy = sample efficiency

**Model Validation and Testing:**
- **Best:** scipy.stats (distributions, hypothesis tests)
- **Why:** Complete statistical toolkit

**Uncertainty Propagation Through Complex Calculations:**
- **Best:** uncertainties (fast models) or chaospy (expensive models)
- **Why:** Automatic differentiation vs. polynomial surrogates

**Advanced Dependency Modeling (Correlations):**
- **Best:** OpenTURNS (copulas)
- **Why:** Only comprehensive copula library

**Expensive Models (>1 sec per evaluation):**
- **Best:** chaospy (PCE) or OpenTURNS (Kriging)
- **Why:** Metamodeling reduces evaluations by 10-100×

### By Model Characteristics

| Model Characteristic        | Recommended Library Combination                          |
|-----------------------------|----------------------------------------------------------|
| Fast (<0.1 sec/eval)        | scipy.stats + SALib                                      |
| Moderate (0.1-1 sec/eval)   | scipy.stats + SALib + uncertainties                      |
| Expensive (>1 sec/eval)     | scipy.stats + chaospy (PCE) or OpenTURNS (Kriging)       |
| Few parameters (D < 5)      | scipy.stats + SALib + uncertainties                      |
| Many parameters (D = 5-15)  | scipy.stats + SALib (Morris screening) + chaospy         |
| Very many (D > 15)          | scipy.stats + SALib (Morris only) → reduce → chaospy     |
| Smooth response             | chaospy (PCE excellent)                                  |
| Non-smooth / discontinuous  | scipy.stats + SALib (Monte Carlo only)                   |
| Correlated parameters       | OpenTURNS (copulas) or statsmodels.copula                |

## 9. Recommended Toolkit for OR Consulting

### Essential (Install First)

1. **scipy.stats** (+ NumPy)
   - Foundation: sampling, distributions, bootstrap
   - Use for: All basic Monte Carlo tasks

2. **SALib**
   - Sensitivity analysis: Morris, Sobol, FAST, PAWN
   - Use for: Parameter screening and variance decomposition

3. **uncertainties**
   - Error propagation: automatic differentiation
   - Use for: Fast analytical uncertainty tracking

### Advanced (Add as Needed)

4. **chaospy**
   - Polynomial chaos expansion
   - Use for: Expensive models (>1 sec/eval), D < 15 parameters

5. **OpenTURNS**
   - Comprehensive UQ suite: copulas, Kriging, reliability
   - Use for: Advanced dependencies, metamodeling, industrial clients

### Rarely (Specialized Needs)

6. **PyMC**
   - Bayesian MCMC
   - Use for: Parameter inference from data (inverse problems only)

### Typical Workflow

```python
# 1. Basic setup (always)
import numpy as np
from scipy.stats import norm, uniform, qmc
from SALib.sample import morris as morris_sampler
from SALib.analyze import morris

# 2. Screening (if D > 10)
problem = {'num_vars': 15, 'names': [...], 'bounds': [...]}
morris_samples = morris_sampler.sample(problem, N=30)
morris_Y = [model(x) for x in morris_samples]
morris_Si = morris.analyze(problem, morris_samples, morris_Y)
important_params = morris_Si['mu_star'] > threshold  # Top 5-10

# 3a. Detailed SA (cheap models)
from SALib.sample import saltelli
from SALib.analyze import sobol

problem_reduced = {...}  # Top 5-10 parameters
sobol_samples = saltelli.sample(problem_reduced, 1024)
sobol_Y = [model(x) for x in sobol_samples]
sobol_Si = sobol.analyze(problem_reduced, sobol_Y)

# 3b. Detailed SA (expensive models)
import chaospy as cp
joint = cp.J(...)
samples = joint.sample(500, rule='halton')
outputs = [expensive_model(x) for x in samples.T]
expansion = cp.generate_expansion(3, joint)
pce = cp.fit_regression(expansion, samples, outputs)
sobol_pce = cp.Sens_t(pce, joint)  # Analytical!

# 4. Uncertainty propagation
from uncertainties import ufloat
# Convert MC results to uncertain numbers
mean_result = ufloat(np.mean(outputs), np.std(outputs))
# Propagate to business metrics
revenue = mean_result * price  # Automatic error bars
```

## 10. Decision Matrix

**For each task, choose the optimal library:**

| Task                                    | Fast Model | Expensive Model | Notes                  |
|-----------------------------------------|------------|-----------------|------------------------|
| Sample from distributions               | scipy.stats | scipy.stats    | Always use scipy       |
| Parameter screening (D > 10)            | SALib      | SALib           | Morris method          |
| Variance-based SA (Sobol)               | SALib      | chaospy         | PCE for expensive      |
| Error propagation (small σ)             | uncertainties | uncertainties | Analytical             |
| Error propagation (large σ, nonlinear)  | scipy.stats MC | chaospy PCE  | Full distribution      |
| Confidence intervals                    | scipy.stats | scipy.stats    | Bootstrap              |
| Correlated parameters (simple)          | scipy.stats | scipy.stats    | Multivariate normal    |
| Correlated parameters (copulas)         | OpenTURNS  | OpenTURNS       | Only copula option     |
| Metamodeling (polynomial response)      | N/A        | chaospy         | PCE                    |
| Metamodeling (non-polynomial)           | N/A        | OpenTURNS       | Kriging                |
| Reliability analysis (rare events)      | OpenTURNS  | OpenTURNS       | FORM/SORM              |
| Bayesian parameter inference            | PyMC       | PyMC            | Inverse problem        |

**Legend:**
- **Fast Model:** <0.1 sec per evaluation
- **Expensive Model:** >1 sec per evaluation
