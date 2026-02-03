# Library Analysis: PyMC

## Overview

**Package:** pymc (PyMC3/PyMC4+)
**Current Version:** 5.x (PyMC v4/v5, not PyMC3)
**Maintenance:** Very active (PyMC Labs + community)
**License:** Apache 2.0
**Primary Use Case:** Bayesian inference via Markov Chain Monte Carlo (MCMC)
**GitHub:** https://github.com/pymc-devs/pymc

## Core Philosophy

PyMC is a probabilistic programming library for Bayesian statistical modeling and inference.
While it uses Monte Carlo methods, its focus is on **Bayesian inference** (estimating posterior
distributions of model parameters given data) rather than **forward uncertainty propagation**
(simulating system behavior under uncertain inputs).

## Core Capabilities

### Probabilistic Programming

**Model Specification:**
```python
import pymc as pm
import numpy as np

# Example: Estimating elevator wait time distribution from observations
wait_time_data = np.array([28, 32, 30, 35, 29, 31, 27, 34])

with pm.Model() as model:
    # Priors on distribution parameters
    mu = pm.Normal('mu', mu=30, sigma=10)
    sigma = pm.HalfNormal('sigma', sigma=5)

    # Likelihood of observations
    wait_times = pm.Normal('wait_times', mu=mu, sigma=sigma, observed=wait_time_data)

    # Sample posterior distributions
    trace = pm.sample(2000, tune=1000, chains=4)

# Extract posterior statistics
print(pm.summary(trace))
# mu: 30.75 ± 0.95 (credible interval)
# sigma: 2.8 ± 0.7
```

### Sampling Algorithms

**NUTS (No-U-Turn Sampler):**
- Default sampler for continuous parameters
- Hamiltonian Monte Carlo variant (gradient-based)
- Self-tuning step size and trajectory length
- Highly efficient for high-dimensional posteriors

**Other Samplers:**
- Metropolis-Hastings: Classic MCMC, slower but robust
- SMC (Sequential Monte Carlo): For complex posteriors
- ADVI (Automatic Differentiation Variational Inference): Fast approximation

**Performance (from benchmarks):**
- PyMC with JAX backend: ~12 minutes for large dataset
- PyMC on GPU (JAX): ~2.7 minutes (4× speedup vs CPU)
- Stan comparison: PyMC slightly faster with JAX

### Automatic Differentiation

**Backend Options:**
- **PyTensor** (default): NumPy-compatible, symbolic computation
- **JAX**: JIT compilation, GPU support, 2-4× faster
- **NumPyro NUTS**: JAX-based sampler (fastest option)

**Gradient Computation:**
- Automatic differentiation for all built-in distributions
- Enables efficient NUTS sampling
- Custom gradients supported for user-defined functions

## Integration with OR Consulting Needs

### Mismatch with Forward Simulation

**PyMC is designed for:**
- Inferring parameters from observed data (inverse problem)
- Quantifying parameter uncertainty given observations
- Comparing model hypotheses (model selection)

**OR consulting typically needs:**
- Forward propagation of input uncertainties
- Sensitivity analysis (which inputs matter most)
- Risk quantification for unobserved scenarios
- Fast sampling from known distributions

**Example Mismatch:**
```python
# OR consulting task: "Given ±20% uncertainty on arrival_rate,
# what is the distribution of wait times?"

# PyMC approach (inverse, Bayesian):
with pm.Model() as model:
    arrival_rate = pm.Normal('arrival_rate', mu=2.5, sigma=0.5)  # Prior
    # ... complex model ...
    wait_time = pm.Deterministic('wait_time', some_function(arrival_rate))
    observed_waits = pm.Normal('obs', mu=wait_time, sigma=noise, observed=data)
    trace = pm.sample(2000)  # Slow, needs observed data

# Better approach for OR (forward, frequentist):
from scipy.stats import norm, qmc
arrival_rates = norm.rvs(loc=2.5, scale=0.5, size=1000)
wait_times = [simulate_elevator(ar) for ar in arrival_rates]
# Fast, no observed data needed, direct simulation
```

### When PyMC is Useful for OR

**1. Parameter Estimation from Field Data:**
```python
# You have observed wait times, want to infer system parameters
observed_wait_times = [32, 28, 35, 30, ...]

with pm.Model() as model:
    # Unknown parameters
    num_elevators = pm.DiscreteUniform('n_elev', lower=3, upper=8)
    arrival_rate = pm.Gamma('λ', alpha=2, beta=0.5)

    # Elevator model (simplified)
    service_rate = num_elevators * 4.0  # trips/min
    expected_wait = 1 / (service_rate - arrival_rate)

    # Likelihood
    wait_times = pm.Normal('waits', mu=expected_wait, sigma=2,
                           observed=observed_wait_times)

    trace = pm.sample(2000)

# Result: Posterior distributions of num_elevators and arrival_rate
# Useful for: "Given observed performance, what's the likely system state?"
```

**2. Bayesian Calibration:**
- Updating parameter beliefs as new data arrives
- Incorporating expert knowledge via informative priors
- Quantifying epistemic uncertainty (parameter knowledge)

**3. Model Comparison:**
```python
# Compare different queuing models using observed data
with pm.Model() as model_1:
    # M/M/c queue
    ...

with pm.Model() as model_2:
    # M/G/c queue with gamma service times
    ...

# Compare via WAIC or LOO (information criteria)
pm.compare([trace_1, trace_2])
```

## Performance Characteristics

### Computational Cost

**Sampling Speed (NUTS with JAX):**
- Simple model (5 parameters): ~100 samples/second
- Complex model (50 parameters): ~10 samples/second
- GPU acceleration: 2-4× speedup

**Typical Workflow:**
- Burn-in (tuning): 1,000-2,000 samples
- Posterior sampling: 2,000-4,000 samples
- Total: 3,000-6,000 model evaluations
- Much slower than forward Monte Carlo (10,000 samples in seconds)

**Comparison to Forward MC:**
| Method              | Samples | Time (typical) | Use Case                    |
|---------------------|---------|----------------|-----------------------------|
| Forward MC (scipy)  | 10,000  | 10 seconds     | Propagate known inputs      |
| PyMC NUTS (CPU)     | 4,000   | 5-20 minutes   | Infer unknown parameters    |
| PyMC NUTS (GPU/JAX) | 4,000   | 1-5 minutes    | Infer parameters (faster)   |

### Memory Requirements

**Trace Storage:**
- 4,000 samples × 10 parameters × 8 bytes = 320 KB per chain
- 4 chains (recommended): ~1.3 MB
- Large models or long chains: GBs possible

**Graph Compilation:**
- PyTensor builds symbolic computation graph
- JAX JIT compilation: initial overhead, then fast
- GPU memory: Model + gradients + sampler state

## API Quality

### Strengths

1. **Declarative Syntax:** Model specification is clean and readable
2. **Comprehensive Distribution Library:** 100+ distributions
3. **Automatic Inference:** Default settings often work well
4. **Excellent Diagnostics:** Built-in convergence checks, trace plots

### Learning Curve

**Steep for Non-Bayesians:**
- Requires understanding of Bayesian inference
- Prior specification is non-trivial
- Interpreting posterior distributions needs care
- Diagnosing convergence issues requires expertise

**Example Pitfalls:**
```python
# Common mistake: Using PyMC for forward simulation
with pm.Model() as model:
    x = pm.Normal('x', mu=5, sigma=1)
    y = pm.Deterministic('y', x**2)
    trace = pm.sample(1000)  # SLOW

# Better (for forward MC):
x_samples = np.random.normal(5, 1, 10000)
y_samples = x_samples**2  # 100× faster
```

## Limitations for OR Consulting

### Not Designed for Forward Uncertainty Propagation

**No Direct Support for:**
- Latin Hypercube Sampling
- Sobol sequences (quasi-Monte Carlo)
- Variance reduction techniques (antithetic variates, control variates)
- Efficient forward sampling from parameter distributions

**Workaround (clunky):**
```python
# Generate samples from prior (not posterior)
with pm.Model() as model:
    arrival_rate = pm.Normal('λ', mu=2.5, sigma=0.5)
    prior_samples = pm.sample_prior_predictive(samples=1000)

# Use samples in forward simulation
wait_times = [simulate(ar) for ar in prior_samples['λ']]

# Problem: No sensitivity analysis, no variance-based methods
```

### No Sensitivity Analysis Tools

**Missing:**
- Sobol indices (variance decomposition)
- Morris method (screening)
- FAST (Fourier-based)
- Derivative-based global sensitivity

**PyMC provides:**
- Posterior sensitivity to priors (not same as parameter sensitivity)
- Can manually compute ∂y/∂x from gradients, but not global SA

### Computational Overhead

**MCMC Overhead:**
- Gradient computation (automatic differentiation)
- Metropolis acceptance step
- Adaptation during tuning
- Result: 10-100× slower than forward sampling

**When Overhead is Justified:**
- Need Bayesian inference (inverse problem)
- Need credible intervals on parameters
- Have limited data, want to incorporate prior knowledge

**When Overhead is Not Justified:**
- Just propagating input uncertainties (use scipy.stats)
- Need quick sensitivity analysis (use SALib)
- Forward simulation only (use NumPy/SciPy)

## Maintenance and Community

### Development Activity

**Release Cadence:** ~4 releases per year
**Contributors:** 200+ (very active)
**Issue Response:** Within days (PyMC Labs backing)
**Breaking Changes:** Occasional, but well-documented migrations

### Community Health

**PyMC Discourse:** Very active forum, 5,000+ users
**GitHub Stars:** ~8,000
**Stack Overflow:** 1,000+ questions
**Books:** Multiple textbooks (Bayesian Analysis with Python, etc.)

## Production Readiness

### Reliability

**Mature for Bayesian Inference:**
- Extensive test suite
- Validated against Stan, BUGS
- Used in production by companies and research labs

**Edge Cases:**
- Non-identifiable models can fail to converge
- High-dimensional posteriors require expertise
- Multimodal posteriors need specialized samplers

### Deployment

**Dependencies:** Heavy (PyTensor/JAX, ArviZ, NumPy, SciPy, matplotlib)
**Package Size:** ~100 MB+ with dependencies
**GPU Support:** Excellent with JAX backend

## Recommendations

### When to Use PyMC for OR Consulting

**1. Parameter Inference from Data:**
- Have observed system performance, want to estimate hidden parameters
- Example: Infer arrival rates from wait time observations

**2. Bayesian Decision Analysis:**
- Incorporate prior beliefs about parameters
- Update beliefs as new data arrives
- Quantify epistemic uncertainty (what we don't know about parameters)

**3. Model Calibration and Validation:**
- Fit complex models to real-world data
- Compare alternative models (queuing theories)
- Uncertainty quantification on model parameters

### When NOT to Use PyMC for OR Consulting

**1. Forward Uncertainty Propagation:**
- Use scipy.stats for sampling
- Use NumPy for simulation
- 10-100× faster than PyMC

**2. Sensitivity Analysis:**
- Use SALib for global methods (Sobol, Morris, FAST)
- Use uncertainties for derivative-based local sensitivity

**3. Risk Quantification (Forward):**
- Use Monte Carlo with scipy.stats
- Use quasi-Monte Carlo (scipy.stats.qmc)
- Much more efficient than MCMC

**4. Quick Exploratory Analysis:**
- PyMC is too slow for rapid iteration
- Use NumPy/SciPy for prototyping

### Integration Strategy (Limited)

**Rare Use Cases:**
```python
# 1. Infer parameters from field data (Bayesian calibration)
with pm.Model() as calibration:
    # Priors on unknown parameters
    true_arrival_rate = pm.Gamma('λ', alpha=2, beta=1)
    # ... model ...
    trace = pm.sample(2000)

# 2. Use inferred posterior as input to forward MC
posterior_samples = trace.posterior['λ'].values.flatten()[:1000]
forward_results = [simulate_elevator(λ) for λ in posterior_samples]

# 3. Perform sensitivity analysis with SALib on forward model
# (Separate workflow, no PyMC involvement)
```

**Verdict:** Minimal overlap with typical OR consulting needs. PyMC excels at Bayesian inference (inverse problems), while OR consulting primarily needs forward uncertainty propagation and sensitivity analysis.

## Summary Assessment

**Strengths (for Bayesian Inference):**
- Powerful probabilistic programming
- State-of-the-art MCMC samplers (NUTS)
- GPU acceleration available
- Excellent diagnostics and visualization

**Weaknesses (for OR Consulting):**
- Not designed for forward uncertainty propagation
- No sensitivity analysis tools (Sobol, Morris, etc.)
- Computational overhead (10-100× slower than forward MC)
- Steep learning curve for Bayesian methods

**Verdict for OR Consulting:**
**Low Priority** - PyMC is a world-class Bayesian inference library, but most OR consulting tasks require forward Monte Carlo simulation and sensitivity analysis, not Bayesian parameter estimation. Use PyMC only when you genuinely need to infer unknown parameters from observed data (calibration) or perform Bayesian decision analysis.

**Recommended Role in Toolkit:**
- **Primary:** None for typical OR work
- **Secondary:** Parameter calibration from field data
- **Tertiary:** Bayesian model comparison

**Better Alternatives for OR Consulting:**
- **Forward MC:** scipy.stats + NumPy (10-100× faster)
- **Sensitivity Analysis:** SALib (designed for this)
- **Error Propagation:** uncertainties (efficient, analytical)
- **Comprehensive UQ:** OpenTURNS (includes forward + sensitivity + more)
