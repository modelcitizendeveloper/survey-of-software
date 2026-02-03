# S3 Need-Driven Discovery: Recommendations

## Executive Summary

This document synthesizes library recommendations for six generic Monte Carlo use case patterns. Recommendations are organized by **pattern first, then library fit**, following the S3 methodology's "requirements first, then find exact fits" philosophy.

**Key Finding**: No single library solves all patterns. The optimal toolkit depends on your specific pattern parameters (D, N, model complexity).

## Quick Decision Tree

```
START: What is your primary need?
│
├─ "Which inputs matter most?" → SENSITIVITY ANALYSIS PATTERN
│  ├─ D < 10, fast model → NumPy/SciPy (correlation)
│  ├─ 10 ≤ D ≤ 50 → SALib (Sobol indices)
│  └─ D > 50 → SALib (Morris screening first)
│
├─ "What are statistical bounds?" → CONFIDENCE INTERVAL PATTERN
│  ├─ Simple scalar output → NumPy (percentiles)
│  ├─ Complex statistics (median, ratios) → SciPy.stats.bootstrap
│  └─ Time series → Statsmodels
│
├─ "Probability of success?" → RISK QUANTIFICATION PATTERN
│  ├─ Single alternative → NumPy (fraction > target)
│  ├─ Multiple alternatives → NumPy + SciPy (hypothesis testing)
│  └─ Financial risk (VaR/CVaR) → NumPy + Custom (or Arch)
│
├─ "Propagate input uncertainty?" → UNCERTAINTY PROPAGATION PATTERN
│  ├─ Fast model, D < 10 → NumPy/SciPy (standard MC)
│  ├─ Fast model, D ≥ 10 → SciPy.stats.qmc (LHS)
│  ├─ Expensive model → Chaospy (PCE surrogate)
│  └─ Complex dependencies → OpenTURNS or Chaospy
│
├─ "Calibrate parameters to data?" → MODEL CALIBRATION PATTERN
│  ├─ Point estimates only → SciPy.optimize
│  ├─ Full uncertainty → PyMC (Bayesian)
│  ├─ Custom likelihood → emcee (MCMC)
│  └─ Curve fitting → lmfit
│
└─ "Characterize output distribution?" → DISTRIBUTION CHARACTERIZATION PATTERN
   ├─ Quick summary → NumPy + Pandas
   ├─ Identify best distribution → SciPy.stats (fitting + GOF)
   ├─ Visualize → Seaborn
   └─ Test normality → SciPy + Statsmodels (Q-Q plots)
```

## Pattern-by-Pattern Recommendations

### 1. Sensitivity Analysis Pattern

**Use Case**: "System with D input parameters, need to identify which inputs most affect output"

#### Recommended Libraries by Problem Scale

| Problem Scale | Library | Rationale |
|--------------|---------|-----------|
| D < 10, exploration | NumPy/SciPy | Simple correlation, fast prototyping |
| 10 ≤ D ≤ 30 | SALib (Sobol) | Gold-standard variance-based sensitivity |
| D > 30 | SALib (Morris → Sobol) | Screen first, then targeted analysis |
| Expensive model | SALib Morris + Surrogate | Minimize evaluations |
| Engineering focus | OpenTURNS | Comprehensive UQ + reliability |

#### Implementation Strategy

**Beginner (D < 10)**:
```python
import numpy as np
from scipy import stats

# Simple correlation-based sensitivity
correlations = {param: np.corrcoef(inputs[param], outputs)[0,1]
                for param in input_names}
```

**Recommended (10 ≤ D ≤ 50)**:
```python
from SALib.sample import saltelli
from SALib.analyze import sobol

# Define problem, sample, evaluate, analyze
Si = sobol.analyze(problem, Y)
# Si['ST'] gives total-order indices (include interactions)
```

**Advanced (D > 50 or expensive model)**:
```python
from SALib.sample import morris as morris_sampler
from SALib.analyze import morris

# Screen with Morris (O(D) evaluations)
# Then run Sobol on subset of important parameters
```

#### Gap Identification

- **Time-dependent sensitivity**: How sensitivity changes over time (requires custom implementation)
- **Categorical parameters**: Sensitivity for discrete/categorical inputs (limited support)
- **Model uncertainty sensitivity**: Sensitivity to model form, not just parameters

---

### 2. Confidence Interval Pattern

**Use Case**: "Stochastic model produces variable outputs, need statistical bounds on predictions"

#### Recommended Libraries by Use Case

| Use Case | Library | Method |
|----------|---------|--------|
| Scalar output, unknown dist | NumPy | `np.percentile(results, [2.5, 97.5])` |
| Scalar output, known dist | SciPy.stats | Parametric CI (normal, etc.) |
| Complex statistics | SciPy.stats.bootstrap | Bootstrap CI on any statistic |
| Multiple outputs | NumPy + Bonferroni | Multiple comparison correction |
| Time series | Statsmodels | Prediction intervals for ARIMA, etc. |

#### Implementation Strategy

**Standard Approach**:
```python
import numpy as np

# 95% confidence interval (percentile method)
alpha = 0.05
ci_lower = np.percentile(results, alpha/2 * 100)
ci_upper = np.percentile(results, (1 - alpha/2) * 100)
```

**For Derived Statistics**:
```python
from scipy.stats import bootstrap

# CI on median, IQR, or any custom statistic
def my_statistic(data):
    return np.median(data)  # Or any function

res = bootstrap((results,), statistic=my_statistic,
                confidence_level=0.95)
ci = (res.confidence_interval.low, res.confidence_interval.high)
```

**Sample Size Planning**:
```python
# How many samples for desired CI width?
from scipy import stats

z = stats.norm.ppf(1 - alpha/2)
N_required = ((2 * z * estimated_std) / desired_width) ** 2
```

#### Gap Identification

- **Streaming CIs**: Online updating as samples arrive (not standardized)
- **Adaptive sampling**: Stop when precision reached (manual implementation)
- **Spatial CIs**: Confidence bands for spatial fields (requires specialized tools)

---

### 3. Risk Quantification Pattern

**Use Case**: "Decision between alternatives, quantify probability of meeting goals"

#### Recommended Libraries by Complexity

| Complexity | Library | Approach |
|------------|---------|----------|
| Single criterion | NumPy | `np.mean(results >= target)` |
| Multiple alternatives | NumPy + SciPy.stats | t-test for comparison |
| Multi-criteria | Pandas + Custom | Boolean logic for complex criteria |
| Financial risk | NumPy + Custom | VaR, CVaR calculations |
| Bayesian decision | PyMC | Decision theory with priors |

#### Implementation Strategy

**Basic Risk Quantification**:
```python
import numpy as np

# Success probability
success_prob = np.mean(results >= target)
failure_prob = 1 - success_prob

# Value at Risk (VaR)
VaR_95 = np.percentile(results, 5)  # 5% chance below this

# Conditional VaR (Expected Shortfall)
tail = results[results <= VaR_95]
CVaR_95 = tail.mean()
```

**Alternative Comparison**:
```python
from scipy import stats

# Statistical test: Is A better than B?
stat, pval = stats.ttest_ind(results_A, results_B)

# Effect size: How much better?
mean_diff = results_A.mean() - results_B.mean()
```

**Multi-Criteria**:
```python
import pandas as pd

df = pd.DataFrame(results)
success = ((df['cost'] <= cost_target) &
           (df['time'] <= time_target) &
           (df['quality'] >= quality_target))
success_prob = success.mean()
```

#### Gap Identification

- **Sequential decisions**: Decision trees with MC at nodes (no standard framework)
- **Robust optimization**: Minimize worst-case regret (limited tools)
- **Real options**: Value of flexibility under uncertainty (specialized modeling)

---

### 4. Uncertainty Propagation Pattern

**Use Case**: "Input variables have measurement uncertainty, propagate through model"

#### Recommended Libraries by Model Type

| Model Type | Library | Reason |
|------------|---------|--------|
| Fast, D < 10 | NumPy/SciPy | Direct MC sampling |
| Fast, 10 ≤ D ≤ 50 | SciPy.stats.qmc | LHS for efficiency |
| Expensive (>1s eval) | Chaospy | PCE surrogate |
| Correlated inputs | Chaospy or OpenTURNS | Copula support |
| Industrial/engineering | OpenTURNS | Comprehensive UQ workflow |

#### Implementation Strategy

**Standard Monte Carlo**:
```python
import numpy as np
from scipy import stats

# Define input distributions
x1 = stats.norm(loc=100, scale=10).rvs(N)
x2 = stats.uniform(loc=0, scale=1).rvs(N)

# Propagate
outputs = model(x1, x2)

# Characterize output uncertainty
mean_output = outputs.mean()
std_output = outputs.std()
percentiles = np.percentile(outputs, [5, 50, 95])
```

**Efficient Sampling (LHS)**:
```python
from scipy.stats import qmc

# Latin Hypercube Sampling
sampler = qmc.LatinHypercube(d=D)
unit_samples = sampler.random(n=N)

# Transform to target distributions
x1 = stats.norm.ppf(unit_samples[:, 0], loc=100, scale=10)
x2 = stats.uniform.ppf(unit_samples[:, 1], loc=0, scale=1)

outputs = model(x1, x2)
```

**Surrogate Modeling (Expensive Models)**:
```python
import chaospy as cp

# Define joint distribution
dist = cp.J(cp.Normal(100, 10), cp.Uniform(0, 1))

# Polynomial chaos expansion
expansion = cp.generate_expansion(order=3, dist=dist)
nodes, weights = cp.generate_quadrature(order=4, dist=dist)

# Evaluate at quadrature points (few evaluations)
evals = [model(x[0], x[1]) for x in nodes.T]

# Fit surrogate
surrogate = cp.fit_quadrature(expansion, nodes, weights, evals)

# Propagate via surrogate (instant)
mean = cp.E(surrogate, dist)
std = cp.Std(surrogate, dist)
```

#### Gap Identification

- **High-dimensional UQ** (D > 100): Dimensionality reduction (active subspaces) limited
- **Time-dependent UQ**: Autocorrelation over time (custom implementation)
- **Multi-fidelity**: Combining cheap/expensive models (specialized frameworks)

---

### 5. Model Calibration Pattern

**Use Case**: "Model has unknown parameters, fit to observed data with uncertainty"

#### Recommended Libraries by Approach

| Approach | Library | When to Use |
|----------|---------|-------------|
| Point estimates | SciPy.optimize | Fast, no full UQ needed |
| Bayesian UQ | PyMC | Want posterior distributions |
| Custom likelihood | emcee | Full control over probability |
| Curve fitting | lmfit | Standard function fitting |
| Statistical models | Statsmodels | Regression, time series |

#### Implementation Strategy

**Frequentist (Point Estimates)**:
```python
from scipy.optimize import least_squares

def residuals(params, x_data, y_data):
    return model(x_data, params) - y_data

result = least_squares(residuals, initial_params,
                       args=(x_data, y_data))
fitted_params = result.x

# Confidence intervals from Hessian (asymptotic)
```

**Bayesian (Full Uncertainty)**:
```python
import pymc as pm

with pm.Model() as calibration:
    # Priors
    param_a = pm.Normal('param_a', mu=0, sigma=10)
    param_b = pm.Uniform('param_b', lower=0, upper=1)

    # Model
    predictions = model(x_data, param_a, param_b)

    # Likelihood
    pm.Normal('obs', mu=predictions, sigma=obs_noise,
              observed=y_data)

    # Sample posterior
    trace = pm.sample(2000)

# Posterior distributions for parameters
```

**Custom Likelihood (emcee)**:
```python
import emcee

def log_probability(params, x_data, y_data):
    lp = log_prior(params)
    if not np.isfinite(lp):
        return -np.inf
    return lp + log_likelihood(params, x_data, y_data)

sampler = emcee.EnsembleSampler(nwalkers, ndim, log_probability,
                                args=(x_data, y_data))
sampler.run_mcmc(initial_pos, nsteps)
```

#### Gap Identification

- **Expensive models**: Surrogate-based calibration (not standardized)
- **Model selection + calibration**: Joint inference (advanced methods)
- **Time-varying parameters**: State-space methods (partial PyMC support)

---

### 6. Distribution Characterization Pattern

**Use Case**: "Complex system output distribution, need percentiles and distributional properties"

#### Recommended Libraries by Task

| Task | Library | Method |
|------|---------|--------|
| Quick summary | NumPy + Pandas | `df.describe()` |
| Identify distribution | SciPy.stats | Fitting + GOF tests |
| Visualize | Seaborn | histplot, kdeplot, ecdfplot |
| Test normality | SciPy + Statsmodels | Shapiro test + Q-Q plots |
| Tail analysis | NumPy | VaR, CVaR calculations |
| Multivariate | Seaborn + NumPy | Joint plots, correlation |

#### Implementation Strategy

**Basic Characterization**:
```python
import numpy as np
from scipy import stats
import pandas as pd

# Summary statistics
df = pd.DataFrame({'output': results})
summary = df.describe()  # Mean, std, percentiles

# Shape
skew = stats.skew(results)
kurt = stats.kurtosis(results)
```

**Distribution Fitting**:
```python
from scipy import stats

# Test multiple distributions
distributions = [stats.norm, stats.lognorm, stats.gamma]

best_fit = None
best_aic = np.inf

for dist in distributions:
    params = dist.fit(results)
    log_lik = np.sum(dist.logpdf(results, *params))
    aic = 2*len(params) - 2*log_lik

    if aic < best_aic:
        best_aic = aic
        best_fit = (dist, params)

# Goodness-of-fit test
ks_stat, pval = stats.kstest(results,
                             lambda x: best_fit[0].cdf(x, *best_fit[1]))
```

**Visualization**:
```python
import seaborn as sns
import matplotlib.pyplot as plt

# Histogram + KDE
sns.histplot(results, kde=True)

# Box plot
sns.boxplot(y=results)

# Empirical CDF
sns.ecdfplot(results)

# Q-Q plot
stats.probplot(results, dist='norm', plot=plt)
```

**Tail Analysis**:
```python
# VaR and CVaR
VaR_95 = np.percentile(results, 95)
tail = results[results >= VaR_95]
CVaR_95 = tail.mean()

# Tail heaviness indicator
q75, q25 = np.percentile(results, [75, 25])
q95, q5 = np.percentile(results, [95, 5])
tail_ratio = (q95 - q5) / (q75 - q25)
# Normal ≈ 2.91, heavy-tailed > 3.0
```

#### Gap Identification

- **Mixture distributions**: Automated component selection (manual iteration)
- **Copula estimation**: Beyond correlation (specialized libraries)
- **Extreme value theory**: Peaks-over-threshold methods (careful application)

---

## Cross-Pattern Integration Strategies

### Pattern Combination 1: Sensitivity → Uncertainty → Risk

**Workflow**:
1. **Sensitivity Analysis**: Identify which inputs drive output variance
2. **Uncertainty Propagation**: Focus measurement on high-sensitivity inputs
3. **Risk Quantification**: Recalculate success probability after reducing key uncertainties

**Libraries**: SALib → SciPy.stats.qmc → NumPy

**Value**: Optimal resource allocation (reduce uncertainty where it matters most)

---

### Pattern Combination 2: Calibration → Propagation → Confidence

**Workflow**:
1. **Calibration**: Fit model parameters to data (get posterior distributions)
2. **Propagation**: Propagate parameter uncertainty through model
3. **Confidence Intervals**: Quantify prediction uncertainty

**Libraries**: PyMC → Chaospy → SciPy.stats.bootstrap

**Value**: Distinguish aleatory (inherent randomness) vs. epistemic (parameter) uncertainty

---

### Pattern Combination 3: Distribution → Sensitivity → Calibration

**Workflow**:
1. **Distribution Characterization**: Understand current output distribution
2. **Sensitivity Analysis**: Identify which parameters affect distribution shape
3. **Calibration**: Fit those parameters to match target distribution

**Libraries**: SciPy.stats → SALib → PyMC

**Value**: Inverse problem (design inputs to achieve desired output distribution)

---

## Library Ecosystem Overview

### Foundation Tier (Always Needed)

**NumPy** (required):
- Array operations, basic statistics
- Percentiles, means, standard deviations
- Foundation for all other libraries

**SciPy** (highly recommended):
- `scipy.stats`: Distributions, statistical tests, bootstrap
- `scipy.stats.qmc`: Latin Hypercube, Sobol sequences
- `scipy.optimize`: Parameter fitting

**Pandas** (recommended for organization):
- Data organization and manipulation
- Multi-variable output management
- Quick summary statistics (`describe()`)

### Specialized Monte Carlo Tier

**SALib** (sensitivity analysis):
- When: D ≥ 10 parameters
- Methods: Sobol, Morris, FAST
- Strength: Gold-standard sensitivity metrics

**Chaospy** (uncertainty quantification):
- When: Expensive models or complex dependencies
- Methods: Polynomial chaos expansion, advanced sampling
- Strength: Surrogate modeling for expensive models

**OpenTURNS** (industrial UQ):
- When: Engineering applications, comprehensive UQ workflow
- Methods: Everything (distributions, sampling, sensitivity, reliability)
- Strength: Industrial-grade, comprehensive

### Bayesian/Calibration Tier

**PyMC** (Bayesian inference):
- When: Need full posterior distributions
- Methods: MCMC (NUTS), prior specification
- Strength: User-friendly Bayesian modeling

**emcee** (MCMC sampler):
- When: Custom likelihoods, need MCMC control
- Methods: Affine-invariant ensemble sampler
- Strength: Simple API, good for moderate dimensions

**lmfit** (curve fitting):
- When: Standard function fitting to data
- Methods: Least squares, constraints
- Strength: High-level API for common tasks

### Visualization Tier

**Matplotlib** (required):
- Base plotting functionality
- All other viz libraries build on this

**Seaborn** (highly recommended):
- Beautiful statistical visualizations
- Distribution plots, joint plots
- Strength: Publication-quality with minimal code

### Domain-Specific Tier

**Statsmodels** (statistical models):
- When: Regression, time series, hypothesis testing
- Strength: Statistical rigor, model diagnostics

**Arch** (financial risk):
- When: Financial applications (VaR, volatility modeling)
- Strength: Industry-standard financial metrics

---

## Parameter-Based Decision Matrix

### By Number of Parameters (D)

| D Range | Sensitivity | Uncertainty Prop | Calibration |
|---------|-------------|------------------|-------------|
| D < 5 | Correlation (NumPy) | Standard MC (NumPy) | Least squares (SciPy) |
| 5 ≤ D < 10 | Sobol (SALib) | Standard MC or LHS | Bayesian (PyMC) |
| 10 ≤ D < 30 | Sobol (SALib) | LHS (SciPy.qmc) | Bayesian (PyMC) |
| 30 ≤ D < 100 | Morris+Sobol (SALib) | LHS or Surrogate | Screening + PyMC |
| D ≥ 100 | Morris (SALib) | Dimensionality reduction | Regularization |

### By Sample Size (N)

| N Range | When Appropriate | Confidence on |
|---------|------------------|---------------|
| N < 1,000 | Mean/median estimates | Mean ± 10% |
| 1,000 ≤ N < 10,000 | 95th percentile | Percentiles ± 5% |
| 10,000 ≤ N < 100,000 | 99th percentile | Tail metrics ± 10% |
| N ≥ 100,000 | Rare events (P < 1%) | Extreme quantiles |

### By Model Evaluation Time

| Eval Time | Strategy | Libraries |
|-----------|----------|-----------|
| < 0.001s | Direct MC, large N | NumPy (N=100k+) |
| 0.001-0.1s | Efficient sampling (LHS) | SciPy.qmc (N=10k) |
| 0.1-1s | Careful sample size | SciPy.qmc (N=5k) |
| 1-10s | Surrogate or screening | Chaospy PCE (N=100s) |
| > 10s | Surrogate mandatory | Chaospy/GP (N=50-200) |

---

## Common Workflow Templates

### Template 1: Basic Uncertainty Analysis

**Goal**: Understand output uncertainty from input uncertainty

```python
# 1. Sample inputs (LHS for efficiency)
from scipy.stats import qmc
sampler = qmc.LatinHypercube(d=D)
samples = sampler.random(n=5000)
# Transform to distributions...

# 2. Evaluate model
outputs = [model(*sample) for sample in samples]

# 3. Characterize output
import numpy as np
mean = np.mean(outputs)
ci_95 = np.percentile(outputs, [2.5, 97.5])

# 4. Visualize
import seaborn as sns
sns.histplot(outputs, kde=True)
```

**Time**: 1 hour setup, depends on model evaluation time

---

### Template 2: Comprehensive Sensitivity Study

**Goal**: Identify key parameters for targeted investigation

```python
# 1. Define problem
from SALib.analyze import sobol
from SALib.sample import saltelli

problem = {
    'num_vars': D,
    'names': ['param1', 'param2', ...],
    'bounds': [[low1, high1], [low2, high2], ...]
}

# 2. Sample (Saltelli for Sobol)
param_values = saltelli.sample(problem, N=1000)

# 3. Evaluate
Y = np.array([model(*params) for params in param_values])

# 4. Analyze
Si = sobol.analyze(problem, Y)

# 5. Identify key parameters
important = [problem['names'][i] for i in range(D)
             if Si['ST'][i] > 0.05]  # Total effect > 5%
```

**Time**: Setup 30 min, depends on D × N × eval_time

---

### Template 3: Bayesian Calibration with Predictions

**Goal**: Calibrate model and make uncertainty-aware predictions

```python
import pymc as pm
import arviz as az

# 1. Define Bayesian model
with pm.Model() as model:
    # Priors
    params = pm.Normal('params', mu=0, sigma=10, shape=D)

    # Model predictions
    predictions = model_function(x_obs, params)

    # Likelihood
    pm.Normal('obs', mu=predictions, sigma=obs_noise,
              observed=y_obs)

    # Sample
    trace = pm.sample(2000)

# 2. Check convergence
print(az.summary(trace))

# 3. Posterior predictive (with uncertainty)
with model:
    post_pred = pm.sample_posterior_predictive(trace)

# 4. Make predictions at new points
# (sample from posterior, evaluate model, aggregate)
```

**Time**: 1-2 hours setup, hours to days for MCMC

---

### Template 4: Multi-Criteria Decision Analysis

**Goal**: Compare alternatives across multiple objectives

```python
import pandas as pd
import numpy as np

# 1. Run MC for each alternative
results = {}
for alt in alternatives:
    outputs = run_mc_simulation(alt, N=10000)
    results[alt] = pd.DataFrame(outputs)  # columns = criteria

# 2. Calculate success probabilities
for alt, df in results.items():
    success = ((df['cost'] <= cost_target) &
               (df['time'] <= time_target) &
               (df['quality'] >= quality_target))
    print(f"{alt}: {success.mean():.1%} success")

# 3. Visualize trade-offs
means = {alt: df.mean() for alt, df in results.items()}
stds = {alt: df.std() for alt, df in results.items()}
# Plot risk-return scatter...
```

**Time**: 2-4 hours, depends on N_alternatives

---

## Minimum Viable Library Stack

### Beginner (Getting Started)

**Required**:
- NumPy: Basic statistics and arrays
- Matplotlib: Visualization

**Recommended**:
- SciPy: Statistical distributions and tests
- Pandas: Data organization

**Capability**: Basic MC simulation, confidence intervals, simple comparisons

---

### Intermediate (Most Use Cases)

**Add to Beginner Stack**:
- Seaborn: Better visualization
- SALib: Sensitivity analysis
- SciPy.stats.qmc: Efficient sampling (LHS)

**Capability**: Sensitivity analysis, efficient uncertainty propagation, publication-quality plots

---

### Advanced (Comprehensive UQ)

**Add to Intermediate Stack**:
- PyMC: Bayesian calibration
- Chaospy or OpenTURNS: Advanced UQ methods

**Capability**: Full Bayesian workflow, expensive model handling, complex dependencies

---

## Installation Recommendations

### Minimal Install (Beginner)
```bash
pip install numpy scipy pandas matplotlib seaborn
```

### Standard Install (Intermediate)
```bash
pip install numpy scipy pandas matplotlib seaborn SALib
```

### Full Install (Advanced)
```bash
pip install numpy scipy pandas matplotlib seaborn SALib pymc arviz chaospy
# OpenTURNS requires: pip install openturns (large package, optional)
```

### Dependency Considerations

- **PyMC**: Large installation (includes Theano/Aesara backend), but essential for Bayesian
- **OpenTURNS**: Very large, only install if needed for industrial UQ
- **Chaospy**: Moderate size, good for surrogate modeling
- **SALib**: Lightweight, highly recommended for sensitivity

---

## Performance Optimization Guidelines

### Memory Efficiency

**Problem**: N > 1M samples, running out of RAM

**Solutions**:
1. Streaming statistics (update mean/variance incrementally)
2. Chunked processing (process batches, combine results)
3. Use NumPy memmap for disk-based arrays

```python
# Streaming mean and variance
n = 0
mean = 0.0
M2 = 0.0  # Sum of squared differences

for sample in generate_samples():
    n += 1
    delta = sample - mean
    mean += delta / n
    M2 += delta * (sample - mean)

variance = M2 / (n - 1)
```

### Computational Efficiency

**Problem**: Model evaluation is slow

**Solutions**:
1. Vectorize model (evaluate N samples at once)
2. Parallelize (use multiprocessing)
3. Build surrogate (Gaussian process, PCE)
4. Use compiled code (Numba, Cython)

```python
# Parallel evaluation
from multiprocessing import Pool

with Pool(processes=8) as pool:
    results = pool.map(model_function, parameter_samples)
```

### Sample Size Optimization

**Problem**: Uncertainty whether N is sufficient

**Solutions**:
1. Convergence plots (mean/CI width vs. N)
2. Adaptive sampling (add samples until criteria met)
3. Sample size formulas (for specific confidence)

```python
# Convergence check
ns = [100, 500, 1000, 5000, 10000]
means = [results[:n].mean() for n in ns]

# Plot means vs. n (should stabilize)
# If still changing >1%, increase N
```

---

## Validation and Verification

### Validate Your MC Implementation

**Checklist**:
1. Test on known distributions (normal → should get μ, σ)
2. Verify percentiles (95th percentile should have 5% exceedance)
3. Check random seed reproducibility
4. Compare to analytical solutions (when available)
5. Independence check (no autocorrelation in samples)

```python
# Verification test: Sample from normal, check recovery
test_samples = np.random.normal(loc=100, scale=15, size=10000)
assert 98 < test_samples.mean() < 102  # Within ±2 of true mean
assert 14 < test_samples.std() < 16    # Within ±1 of true std
```

### Common Implementation Errors

1. **Off-by-one in percentiles**: `percentile(90)` is 90th, not top 10%
2. **Forgetting ddof=1**: Use `std(ddof=1)` for sample std dev
3. **Correlation in samples**: Check for autocorrelation if using pseudo-random
4. **Wrong distribution**: Using normal when lognormal appropriate
5. **Insufficient burn-in**: MCMC chains need warm-up period

---

## Future-Proofing Your Analysis

### Documentation Standards

**For Reproducibility**, document:
1. Library versions (`pip freeze > requirements.txt`)
2. Random seeds used
3. Sample sizes (N) and why chosen
4. Distribution assumptions and justification
5. Any data preprocessing steps

### Extending Your Analysis

**When to Upgrade Methods**:
- Simple MC → LHS: When N × eval_time becomes significant
- Correlation → Sobol: When interaction effects suspected
- Point estimates → Bayesian: When parameter uncertainty matters
- Direct MC → Surrogate: When eval_time > 1 second

### Emerging Methods (Not Yet Standardized)

- **Multi-fidelity UQ**: Combining cheap/expensive models
- **Active learning**: Adaptive sampling for efficient exploration
- **Deep learning surrogates**: Neural networks for complex models
- **Robust UQ**: Optimization under distributional ambiguity

---

## Summary: The S3 Philosophy Applied

**S3 Methodology**: Requirements first, then find exact fits

This document organized recommendations by **use case pattern**, not by library. This is intentional:

1. **Start with your need** (which pattern matches your problem?)
2. **Check parameters** (D, N, model complexity)
3. **Select library** (based on fit analysis in pattern file)
4. **Implement** (using generic template)
5. **Validate** (convergence, verification)

**No single library does everything**. The optimal stack depends on your specific combination of patterns and parameters. Start simple (NumPy/SciPy), add specialized tools as needed (SALib, PyMC), and only adopt comprehensive frameworks (OpenTURNS) when genuinely required.

**Key Takeaway**: Match your requirements to library capabilities, don't force-fit a library to your problem.
