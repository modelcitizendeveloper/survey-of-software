# S1 Rapid Library Search - Final Recommendation

## Primary Recommendation: The Standard Stack

**Confidence Level**: Very High (95%)

Use the combination:
1. **NumPy random** (np.random.default_rng) - Random number generation
2. **scipy.stats** - Statistical distributions and analysis
3. **scipy.stats.qmc** - Latin Hypercube and Sobol sequences
4. **SALib** - Sensitivity analysis
5. **uncertainties** - Error propagation (optional, but useful)

## Why This Combination Wins

### 1. Popularity = Reliability

**NumPy/SciPy**:
- 100+ million downloads per month
- 25K+ GitHub stars (NumPy), 11K+ (SciPy)
- Universal adoption in scientific Python
- If it's broken, millions would have noticed

**SALib**:
- 60K weekly downloads
- THE library for sensitivity analysis
- No viable alternative with similar adoption
- Published research backing

### 2. Speed to Value

**Time to first working example**: 15-20 minutes total

```python
# 5 minutes: Basic Monte Carlo
import numpy as np
rng = np.random.default_rng(42)
samples = rng.normal(100, 20, size=10000)

# 5 minutes: Latin Hypercube
from scipy.stats import qmc
lhs = qmc.LatinHypercube(d=3)
param_samples = lhs.random(n=100)

# 10 minutes: Sensitivity analysis
from SALib.sample import saltelli
from SALib.analyze import sobol
problem = {'num_vars': 3, 'names': ['a','b','c'],
           'bounds': [[0,1]]*3}
X = saltelli.sample(problem, 1024)
# Run your model...
Si = sobol.analyze(problem, Y)
```

Total: 20 minutes from zero to sensitivity analysis results.

### 3. Zero Installation Friction

- NumPy/SciPy: Already installed (core dependencies)
- SALib: `pip install SALib` (one command, no complications)
- uncertainties: `pip install uncertainties` (optional)

No compilation, no C++ dependencies, no configuration.

### 4. Ecosystem Integration

All libraries work together seamlessly:
- NumPy arrays pass directly to SciPy functions
- SciPy qmc integrates with NumPy random
- SALib consumes NumPy arrays
- uncertainties wraps NumPy functions

No impedance mismatch, no conversion overhead.

## Coverage of Requirements

**Fast random number generation**: NumPy (PCG64, state-of-the-art)
**Quality guarantees**: NumPy (100M users, decades of testing)
**Multiple distributions**: scipy.stats (100+ built-in)
**Simple Monte Carlo**: NumPy random
**Latin Hypercube**: scipy.stats.qmc.LatinHypercube
**Sobol sequences**: scipy.stats.qmc.Sobol
**Variance-based sensitivity**: SALib (Sobol indices)
**Morris method**: SALib
**Uncertainty propagation**: uncertainties package
**NumPy/SciPy integration**: Native (same stack)
**Production-ready**: Millions of users
**Documentation**: Excellent (official tutorials, examples)

**Coverage**: 100% of requirements met

## Alternative Options (If Primary Fails)

### Option 2: Standard Stack + Custom Code

If SALib doesn't fit:
- Use NumPy + SciPy for everything
- Implement basic sensitivity analysis manually
- Still <30 min to first result
- Confidence: Medium (70%)

### Option 3: Add UQpy for Advanced Methods

If you need specialized UQ methods:
- Keep NumPy/SciPy base
- Add UQpy for specific advanced features
- Accept longer learning curve
- Confidence: Low (40%) - only if forced

## What NOT to Do

1. **Don't use pyDOE/pyDOE2**: Deprecated, use scipy.stats.qmc
2. **Don't use PyMC**: Wrong tool (Bayesian inference, not Monte Carlo)
3. **Don't use Chaospy**: Academic focus, steep curve
4. **Don't use monaco/pandas-montecarlo**: Unnecessary abstractions
5. **Don't use old NumPy API**: No np.random.seed(), use default_rng()

## Implementation Next Steps

### Phase 1: Basic Monte Carlo (Day 1, 2 hours)

```python
import numpy as np
from scipy import stats

# Setup RNG
rng = np.random.default_rng(42)

# Define parameter distributions
wait_time = stats.norm(45, 10)
arrival_rate = stats.expon(30)

# Run Monte Carlo
n_trials = 10000
results = []
for _ in range(n_trials):
    wt = wait_time.rvs(random_state=rng)
    ar = arrival_rate.rvs(random_state=rng)
    results.append(your_model(wt, ar))

# Analyze
results = np.array(results)
print(f"Mean: {results.mean():.2f}")
print(f"95% CI: {np.percentile(results, [2.5, 97.5])}")
```

### Phase 2: Latin Hypercube Sampling (Day 1, 1 hour)

```python
from scipy.stats import qmc

# LHS for parameter space exploration
sampler = qmc.LatinHypercube(d=3)
samples = sampler.random(n=100)

# Scale to your bounds
l_bounds = [0.8, 0.8, 0.8]  # -20%
u_bounds = [1.2, 1.2, 1.2]  # +20%
scaled = qmc.scale(samples, l_bounds, u_bounds)
```

### Phase 3: Sensitivity Analysis (Day 2, 3 hours)

```python
from SALib.sample import saltelli
from SALib.analyze import sobol

# Define problem
problem = {
    'num_vars': 3,
    'names': ['wait_time', 'arrival_rate', 'capacity'],
    'bounds': [[36, 54],    # ±20% around 45
               [24, 36],    # ±20% around 30
               [8, 12]]     # ±20% around 10
}

# Generate samples (Saltelli scheme)
param_values = saltelli.sample(problem, 1024)

# Run model
Y = np.array([your_model(*params) for params in param_values])

# Analyze sensitivity
Si = sobol.analyze(problem, Y)

print("First-order indices:", Si['S1'])
print("Total-order indices:", Si['ST'])
```

### Phase 4: Error Propagation (Day 2, 1 hour)

```python
from uncertainties import ufloat

# Values with uncertainties
mean_wait = ufloat(45.2, 3.1)
mean_arrival = ufloat(30.5, 2.8)

# Automatic propagation
result = your_formula(mean_wait, mean_arrival)
print(f"Result: {result:.1f}")  # Shows: 123.4 +/- 5.6
```

## Success Metrics

After 1 day (8 hours):
- Running Monte Carlo simulations: DONE
- Generating Latin Hypercube samples: DONE
- Calculating confidence intervals: DONE

After 2 days (16 hours):
- Sensitivity analysis working: DONE
- Understanding parameter importance: DONE
- Ready for production use: DONE

## Why This Recommendation is Confident

1. **Battle-tested**: Billions of simulations run with these tools
2. **Standard practice**: Every scientific Python user knows this stack
3. **Minimal risk**: If millions of users have success, you will too
4. **Fast learning**: Excellent documentation and examples everywhere
5. **Future-proof**: NumPy/SciPy aren't going anywhere
6. **Hiring-friendly**: Any Python data scientist knows these tools

## S1 Methodology Validation

This recommendation embodies S1 principles:
- **Popular**: Most downloaded Python scientific packages
- **Fast**: <30 minutes to first working example
- **Low-risk**: Millions of users validate reliability
- **Standard**: Part of accepted scientific Python stack
- **Documented**: Comprehensive official documentation

Popular solutions exist for a reason. This is the reason.
