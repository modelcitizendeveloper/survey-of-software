# Library Analysis: SALib (Sensitivity Analysis Library)

## Overview

**Package:** SALib
**Current Version:** 1.5+
**Maintenance:** Active (Cornell/Virginia Tech research group)
**License:** MIT
**Primary Use Case:** Global sensitivity analysis for computational models
**GitHub:** https://github.com/SALib/SALib

## Core Philosophy

SALib is designed to facilitate global sensitivity analysis (GSA) by providing a comprehensive
suite of methods for evaluating how model inputs affect outputs. Unlike local sensitivity
methods (derivatives at a point), SALib focuses on global methods that explore the entire
parameter space.

## Sensitivity Analysis Methods

### 1. Sobol Sensitivity Analysis

**Method:** Variance-based decomposition
**Sampling:** Saltelli's scheme with Sobol sequences (quasi-Monte Carlo)

**What It Provides:**
- First-order indices (S1): Direct effect of each parameter
- Total-order indices (ST): Total effect including interactions
- Second-order indices (S2): Pairwise interaction effects

**Sample Requirements:**
- N(2D + 2) where N = base sample size, D = number of parameters
- Typical: N=1024 for D=10 → 22,528 model evaluations

**Implementation:**
```python
from SALib.sample import saltelli
from SALib.analyze import sobol

problem = {
    'num_vars': 3,
    'names': ['num_elevators', 'capacity', 'speed'],
    'bounds': [[2, 10], [8, 20], [1.0, 3.0]]
}

# Generate samples using Sobol sequence
param_values = saltelli.sample(problem, 1024, calc_second_order=True)
# Shape: (22528, 3) for 3 parameters

# Run model
Y = np.array([elevator_model(x) for x in param_values])

# Analyze sensitivity
Si = sobol.analyze(problem, Y, calc_second_order=True)
# Si['S1']: [0.62, 0.23, 0.08]  # First-order indices
# Si['ST']: [0.68, 0.31, 0.12]  # Total-order indices
# Si['S2']: [[0, 0.04, 0.01], ...]  # Second-order interactions
```

**Advantages:**
- Quantifies variance contribution precisely
- Captures interaction effects
- Model-agnostic (black box)

**Limitations:**
- Computationally expensive (large N required)
- Assumes output variance is meaningful measure
- May be unreliable for highly-skewed or multi-modal outputs

### 2. Morris Method (Elementary Effects)

**Method:** One-at-a-time (OAT) screening with randomized trajectories
**Purpose:** Identify important parameters with minimal computational cost

**What It Provides:**
- μ (mu): Average sensitivity (main effect size)
- μ* (mu_star): Average absolute sensitivity (monotonicity-free)
- σ (sigma): Standard deviation of effects (interaction/non-linearity indicator)

**Sample Requirements:**
- r × (D + 1) where r = number of trajectories (typically 10-50), D = parameters
- Example: r=20, D=10 → 220 model evaluations (100× less than Sobol)

**Implementation:**
```python
from SALib.sample import morris as morris_sampler
from SALib.analyze import morris

problem = {
    'num_vars': 3,
    'names': ['num_elevators', 'capacity', 'speed'],
    'bounds': [[2, 10], [8, 20], [1.0, 3.0]]
}

# Generate Morris samples (trajectories)
param_values = morris_sampler.sample(problem, N=100, num_levels=4)
# N=100 trajectories, 4 grid levels

# Run model
Y = np.array([elevator_model(x) for x in param_values])

# Analyze
Si = morris.analyze(problem, param_values, Y)
# Si['mu_star']: [0.85, 0.32, 0.12]  # Importance ranking
# Si['sigma']: [0.15, 0.08, 0.02]    # Non-linearity indicator
```

**Advantages:**
- Extremely efficient for screening (10-100 samples per parameter)
- Good for models with many parameters (20+)
- Identifies both main effects and interactions

**Limitations:**
- Qualitative ranking, not quantitative variance decomposition
- Less precise than Sobol for final sensitivity estimates
- Grid-based sampling may miss continuous effects

### 3. FAST (Fourier Amplitude Sensitivity Test)

**Method:** Fourier decomposition of model output variance

**Variants in SALib:**
- **eFAST (Extended FAST):** First and total-order indices
- **RBD-FAST:** Random Balanced Design (more efficient)

**Sample Requirements:**
- eFAST: N × D where N ≈ 1000 (often less than Sobol)
- RBD-FAST: Even fewer samples with comparable accuracy

**Implementation:**
```python
from SALib.sample import fast_sampler
from SALib.analyze import fast

problem = {
    'num_vars': 3,
    'names': ['num_elevators', 'capacity', 'speed'],
    'bounds': [[2, 10], [8, 20], [1.0, 3.0]]
}

# Generate samples
param_values = fast_sampler.sample(problem, N=1000)

# Run model
Y = np.array([elevator_model(x) for x in param_values])

# Analyze
Si = fast.analyze(problem, Y)
# Si['S1']: First-order indices
# Si['ST']: Total-order indices
```

**Advantages:**
- More efficient than Sobol for first/total-order indices
- Based on solid mathematical foundation (Fourier analysis)
- RBD-FAST variant exploits sample structure better

**Limitations:**
- No second-order indices
- Less widely used than Sobol (fewer validation studies)

### 4. PAWN Method

**Method:** Moment-independent, CDF-based sensitivity

**When to Use:**
- Outputs are highly skewed
- Outputs are multi-modal
- Variance-based methods give unreliable results

**Implementation:**
```python
from SALib.sample import latin
from SALib.analyze import pawn

problem = {
    'num_vars': 3,
    'names': ['num_elevators', 'capacity', 'speed'],
    'bounds': [[2, 10], [8, 20], [1.0, 3.0]]
}

param_values = latin.sample(problem, 1000)
Y = np.array([elevator_model(x) for x in param_values])

Si = pawn.analyze(problem, param_values, Y, S=10)
# S: number of conditioning slices
```

**Advantages:**
- Robust to output distribution shape
- Works for non-normal, non-unimodal outputs
- Lower sample requirements for screening

**Limitations:**
- Less interpretable than variance-based indices
- Requires choosing number of slices (S parameter)

### 5. DGSM (Derivative-based Global Sensitivity Measure)

**Method:** Approximates variance-based indices using finite differences

**Implementation:**
```python
from SALib.sample import finite_diff
from SALib.analyze import dgsm

param_values = finite_diff.sample(problem, 1000, delta=0.01)
Y = np.array([elevator_model(x) for x in param_values])

Si = dgsm.analyze(problem, param_values, Y)
```

**Advantages:**
- Can be more efficient than Sobol for smooth models
- Provides variance-based interpretation

**Limitations:**
- Requires smooth model response
- Finite difference step size (delta) affects accuracy

## Integration with SciPy/NumPy

### Sampling Integration

SALib uses scipy.stats.qmc internally for quasi-Monte Carlo:
```python
# SALib's Sobol sampler uses scipy.stats.qmc.Sobol
# with scrambling and seed support
param_values = saltelli.sample(problem, 1024, scramble=True, seed=42)
```

### Distribution Support

SALib operates in [0, 1] normalized space, then scales to bounds:
```python
# For custom distributions, transform samples:
from scipy.stats import norm, lognorm

# Get uniform samples from SALib
samples_uniform = saltelli.sample(problem, 1024)

# Transform to desired distributions
samples_transformed = np.column_stack([
    norm.ppf(samples_uniform[:, 0], loc=5, scale=2),      # Normal
    lognorm.ppf(samples_uniform[:, 1], s=0.5, scale=10),  # Lognormal
    samples_uniform[:, 2] * 10 + 2                         # Uniform [2, 12]
])
```

### Parallel Execution

SALib provides no built-in parallelization, but easily integrates:
```python
from multiprocessing import Pool

def run_model_wrapper(params):
    return elevator_model(params)

with Pool(8) as pool:
    Y = pool.map(run_model_wrapper, param_values)

Si = sobol.analyze(problem, np.array(Y))
```

## Performance Characteristics

### Computational Costs (D=10 parameters)

| Method      | Samples Required | Model Evaluations | Relative Cost |
|-------------|------------------|-------------------|---------------|
| Morris      | 220 (r=20)       | 220              | 1×           |
| RBD-FAST    | 2,000            | 2,000            | 9×           |
| eFAST       | 10,000           | 10,000           | 45×          |
| Sobol (1st) | 12,288 (N=1024)  | 12,288           | 56×          |
| Sobol (2nd) | 22,528 (N=1024)  | 22,528           | 102×         |

### Processing Overhead

SALib analysis functions are fast (Python-based but vectorized):
- Sobol.analyze: ~100 ms for 20,000 samples
- Morris.analyze: ~10 ms for 220 samples
- Bottleneck is always model evaluation, not SALib processing

### Memory Efficiency

- Stores only sample matrix and output vector
- Memory: O(N × D) for samples + O(N) for outputs
- Example: N=20,000, D=10 → ~1.6 MB for float64 arrays

## API Quality

### Strengths

1. **Consistent Interface:** All methods follow sample → run → analyze pattern
2. **Clear Problem Definition:** Dictionary-based problem specification
3. **Minimal Dependencies:** NumPy, SciPy, matplotlib, pandas
4. **Well-Documented:** Examples for each method, mathematical descriptions

### Example Workflow

```python
# 1. Define problem (consistent across all methods)
problem = {
    'num_vars': 3,
    'names': ['x1', 'x2', 'x3'],
    'bounds': [[0, 1], [0, 1], [0, 1]]
}

# 2. Sample (method-specific)
from SALib.sample import saltelli
param_values = saltelli.sample(problem, 1024)

# 3. Evaluate model (user-provided)
Y = evaluate_model(param_values)

# 4. Analyze (method-specific)
from SALib.analyze import sobol
Si = sobol.analyze(problem, Y)

# 5. Interpret results
print(f"First-order indices: {Si['S1']}")
print(f"Total-order indices: {Si['ST']}")
print(f"Parameter ranking: {problem['names'][np.argsort(Si['ST'])[::-1]]}")
```

### Learning Curve

**Easy for Basic Use:**
- Problem definition is intuitive
- Sample/analyze separation is clean
- Good examples in documentation

**Requires SA Background:**
- Understanding which method to use requires statistical knowledge
- Interpreting indices needs care (especially interactions)
- Convergence analysis is manual

## Limitations

### What's Missing

**No Uncertainty Propagation:**
- Only sensitivity analysis, not full uncertainty quantification
- No confidence intervals on model predictions
- No error propagation through calculations

**No Correlation Handling:**
- Assumes independent parameters
- For correlated inputs, must manually transform samples or use copulas

**No Built-in Visualization:**
- Provides matplotlib examples but no automatic plotting
- Must create custom visualizations for results

**Limited Distribution Support:**
- Sampling in [0, 1] uniform space
- User must transform for non-uniform distributions
- No built-in copula support

## Maintenance and Community

### Development Activity

**Release Cadence:** 1-2 releases per year
**Contributors:** ~30 (academic research group)
**Issue Response:** Within weeks (smaller team than SciPy)
**Breaking Changes:** Infrequent, stable API

### Community Health

**Citations:** 400+ academic papers cite SALib
**GitHub Stars:** ~800
**Stack Overflow:** ~50 questions (smaller community)
**Documentation:** Comprehensive, with examples for each method

## Production Readiness

### Reliability

**Academic Validation:**
- Methods validated against published benchmarks
- Used in peer-reviewed research
- Comparison studies show good agreement with R/MATLAB implementations

**Stability:**
- Mature codebase (since 2014)
- Good test coverage
- Few reported bugs

### Deployment

**Dependencies:** NumPy, SciPy, matplotlib, pandas (all standard)
**Package Size:** ~500 KB
**Platform Support:** Pure Python, works everywhere NumPy works

## Recommendations

### Best Use Cases

1. **Parameter Screening**
   - Morris method for identifying important parameters among 20+
   - Fast, qualitative ranking

2. **Variance-Based Sensitivity**
   - Sobol method for precise quantification
   - When computational budget allows N(2D+2) evaluations

3. **Efficient Global SA**
   - RBD-FAST for first/total-order indices with fewer samples
   - Good compromise between Morris and Sobol

4. **Non-Normal Outputs**
   - PAWN method for skewed or multi-modal results
   - When variance is not appropriate measure

### Integration Strategy for OR Consulting

**Two-Stage Approach:**
1. **Screening:** Morris method with N=20-50 trajectories
   - Identify 5-10 most important parameters
   - Minimal computational cost

2. **Detailed Analysis:** Sobol on reduced parameter set
   - Quantify variance contribution
   - Analyze interactions
   - Higher computational cost but focused

**Example for Elevator Model:**
```python
# Stage 1: Screen 15 parameters with Morris
problem_full = {'num_vars': 15, 'names': [...], 'bounds': [...]}
morris_samples = morris_sampler.sample(problem_full, N=30)
morris_Y = evaluate_model(morris_samples)
morris_Si = morris.analyze(problem_full, morris_samples, morris_Y)

# Identify top 5 parameters by mu_star
important_params = np.argsort(morris_Si['mu_star'])[-5:]

# Stage 2: Sobol on reduced set
problem_reduced = {
    'num_vars': 5,
    'names': [problem_full['names'][i] for i in important_params],
    'bounds': [problem_full['bounds'][i] for i in important_params]
}
sobol_samples = saltelli.sample(problem_reduced, 1024)
sobol_Y = evaluate_model(sobol_samples)
sobol_Si = sobol.analyze(problem_reduced, sobol_Y, calc_second_order=True)
```

### When to Look Elsewhere

**Need Uncertainty Propagation:** Use uncertainties or PyMC
**Need Correlated Parameters:** Combine with statsmodels.copula
**Need Bayesian Sensitivity:** Use PyMC with Sobol-like analysis
**Need Industrial UQ Suite:** Use OpenTURNS (includes SA + more)

## Summary Assessment

**Strengths:**
- Comprehensive suite of global sensitivity methods
- Efficient methods for screening (Morris) and detailed analysis (Sobol, FAST)
- Clean API, well-documented
- Integrates well with SciPy/NumPy ecosystem
- Production-ready, academically validated

**Weaknesses:**
- Only sensitivity analysis, not full UQ
- No built-in correlation handling
- No automatic visualization
- Smaller community than SciPy

**Verdict:** Essential tool for OR consulting sensitivity analysis. Complements scipy.stats perfectly - use SciPy for sampling and basic statistics, SALib for global sensitivity analysis. The Morris → Sobol workflow is ideal for computationally expensive elevator models.
