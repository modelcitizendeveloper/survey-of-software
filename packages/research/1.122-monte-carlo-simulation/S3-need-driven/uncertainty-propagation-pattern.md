# Uncertainty Propagation Pattern

## Pattern Definition

**Generic Use Case**: "Input variables have measurement uncertainty, propagate through model to understand output uncertainty"

**Core Question**: Given my input parameters are uncertain (measurement error, natural variability), how uncertain is my model output?

**Parameterization**:
- **D**: Number of uncertain input parameters
- **input_distributions**: Type of uncertainty (normal, uniform, empirical)
- **correlation_structure**: Independent vs. correlated inputs
- **model_complexity**: Linear, nonlinear, black-box
- **output_statistics**: Mean, variance, full distribution needed

## Requirements Breakdown

### Functional Requirements

**FR1: Distribution Propagation**
- Must propagate input probability distributions through arbitrary models
- Support for common distributions (normal, lognormal, uniform, triangular, beta)
- Handle empirical/data-driven distributions
- Preserve correlation structure between inputs

**FR2: Output Characterization**
- Calculate output mean, variance, percentiles
- Full output distribution (histogram, KDE)
- Uncertainty decomposition: Which inputs contribute most to output uncertainty?

**FR3: Correlation Handling**
- Support independent inputs
- Support correlated inputs (correlation matrix, copulas)
- Maintain physical constraints (e.g., sum of fractions = 1)

**FR4: Computational Methods**
- Direct Monte Carlo sampling
- Advanced methods: Latin Hypercube Sampling (LHS), Quasi-Monte Carlo
- Surrogate modeling for expensive models (Polynomial Chaos, Gaussian Process)

### Performance Requirements

**PR1: Sample Efficiency**
- LHS: Better space-filling than random sampling
- QMC: Faster convergence for smooth models
- Surrogate: Drastically reduce evaluations for expensive models

**PR2: Dimensionality Scaling**
- Efficient for D < 10 (standard MC fine)
- Scalable for 10 ≤ D ≤ 100 (need LHS or QMC)
- Tractable for D > 100 (require dimensionality reduction)

### Usability Requirements

**UR1: Input Specification**
- Easy definition of parameter distributions
- Import from data (fit distribution to measurements)
- Expert elicitation support (min, most-likely, max → triangular/PERT)

**UR2: Output Interpretation**
- Variance contribution by input
- Confidence bands on outputs
- Comparison: deterministic vs. uncertain predictions

## Library Fit Analysis

### NumPy/SciPy (Foundation Tier)

**Fit Score**: ✓ Perfect Fit (Basic Propagation)

**Capabilities**:
- ✓ Distribution sampling (scipy.stats rich distribution library)
- ✓ Random sampling for direct MC
- ✓ Correlation via multivariate_normal for correlated inputs
- ○ No built-in LHS (need external or manual)
- ✗ No automatic surrogate modeling

**Best For**:
- Straightforward uncertainty propagation
- Fast models (can afford 10k+ evaluations)
- Independent or multivariate normal inputs

**Limitations**:
- No advanced sampling (LHS built-in)
- Correlation limited to multivariate normal
- No automatic variance decomposition

### SciPy.stats.qmc (Foundation Tier - Quasi-Monte Carlo)

**Fit Score**: ✓ Excellent Fit (Added v1.7)

**Capabilities**:
- ✓ Latin Hypercube Sampling (qmc.LatinHypercube)
- ✓ Sobol sequences (qmc.Sobol)
- ✓ Halton sequences (qmc.Halton)
- ✓ Better convergence than random MC
- ○ Requires transformation to match distributions

**Best For**:
- When you want better sample efficiency than random MC
- Smooth model functions
- Medium dimensionality (D = 10-50)

**Limitations**:
- QMC advantages diminish for very nonsmooth models
- Transformation to arbitrary distributions requires care

### Chaospy (Specialized Tier - Polynomial Chaos)

**Fit Score**: ✓ Perfect Fit (Surrogate-Based)

**Capabilities**:
- ✓ Polynomial chaos expansion (PCE) for surrogates
- ✓ Sophisticated distribution handling (any scipy.stats distribution)
- ✓ Automatic variance decomposition (Sobol indices via PCE)
- ✓ Copula support for complex dependencies
- ✓ LHS and advanced sampling built-in

**Best For**:
- Expensive models (reduce evaluations via surrogate)
- Smooth response surfaces (polynomial approximation valid)
- Need both propagation AND sensitivity analysis
- Complex input dependencies

**Limitations**:
- Assumes sufficient smoothness for polynomial approximation
- PCE degree selection requires expertise
- Slower for very cheap models (overhead not worth it)

### OpenTURNS (Specialized Tier - Comprehensive UQ)

**Fit Score**: ✓ Perfect Fit (Industrial-Grade UQ)

**Capabilities**:
- ✓ Comprehensive distribution library + custom distributions
- ✓ Advanced sampling (LHS, QMC, importance sampling)
- ✓ Sophisticated correlation (copulas, nataf transformation)
- ✓ Multiple surrogate methods (PCE, Kriging, neural nets)
- ✓ Sensitivity analysis integration
- ✓ Rare event simulation
- ✓ Calibration and validation tools

**Best For**:
- Industrial/engineering applications (aerospace, civil, nuclear)
- Complex dependency structures
- Large-scale studies requiring multiple UQ methods
- When you need comprehensive UQ workflow

**Limitations**:
- Heavy installation (many dependencies)
- Steeper learning curve
- Verbose API (more code for simple tasks)

### UncertaintyQuantification / UQpy (Specialized Tier)

**Fit Score**: ○ Good Fit (Research-Oriented)

**Capabilities**:
- ✓ Modern Python UQ implementations
- ✓ Subset simulation for rare events
- ✓ Reliability analysis tools
- ○ Smaller community than OpenTURNS
- ○ Less comprehensive documentation

**Best For**:
- Research applications
- When you want lighter-weight than OpenTURNS
- Specific advanced methods (subset simulation)

**Limitations**:
- Less mature than OpenTURNS or Chaospy
- Fewer examples and tutorials

## Recommendation by Problem Type

### Fast Model, Independent Inputs, D < 10

**Recommended**: NumPy/SciPy standard Monte Carlo
```python
# Sample inputs
x1 = np.random.normal(loc=100, scale=10, size=N)
x2 = np.random.uniform(low=0, high=1, size=N)

# Evaluate model
y = model(x1, x2)

# Characterize output
mean_y, std_y = y.mean(), y.std()
percentiles = np.percentile(y, [5, 50, 95])
```

**Why**: Simple, fast, no overhead.

### Fast Model, Want Better Efficiency, D = 10-50

**Recommended**: SciPy QMC (Latin Hypercube)
```python
from scipy.stats import qmc

sampler = qmc.LatinHypercube(d=D)
samples = sampler.random(n=N)

# Transform to desired distributions
x1 = scipy.stats.norm.ppf(samples[:, 0], loc=100, scale=10)
x2 = scipy.stats.uniform.ppf(samples[:, 1], loc=0, scale=1)

y = model(x1, x2)
```

**Why**: 10-100x faster convergence than random MC.

### Expensive Model (> 1 sec per evaluation)

**Recommended**: Chaospy (Polynomial Chaos Expansion)
```python
import chaospy as cp

# Define distributions
dist = cp.J(cp.Normal(100, 10), cp.Uniform(0, 1))

# Generate PCE
expansion = cp.generate_expansion(order=3, dist=dist)
nodes, weights = cp.generate_quadrature(order=4, dist=dist)

# Evaluate model at quadrature points (few evaluations)
evaluations = [model(x[0], x[1]) for x in nodes.T]

# Fit surrogate
surrogate = cp.fit_quadrature(expansion, nodes, weights, evaluations)

# Propagate uncertainty via surrogate (instant)
mean_y = cp.E(surrogate, dist)
std_y = cp.Std(surrogate, dist)
```

**Why**: Reduces evaluations from 10k+ to ~100 for 2D problem.

### Correlated Inputs (Complex Dependencies)

**Recommended**: Chaospy (copulas) or OpenTURNS
```python
# Chaospy example with dependency
import chaospy as cp

# Marginal distributions
marginal1 = cp.Normal(100, 10)
marginal2 = cp.Uniform(0, 1)

# Create correlated joint distribution (Gaussian copula)
correlation_matrix = [[1.0, 0.7], [0.7, 1.0]]
joint_dist = cp.MvNormal([100, 0.5], correlation_matrix)  # Simplified example

# Sample and propagate
samples = joint_dist.sample(N)
y = model(samples[0, :], samples[1, :])
```

**Why**: Handles correlations beyond multivariate normal.

### Industrial Application (Need Comprehensive UQ)

**Recommended**: OpenTURNS
- Full UQ workflow: distribution fitting → sampling → propagation → sensitivity → calibration
- Industry-standard methods and documentation

## Generic Code Template

```python
"""
GENERIC UNCERTAINTY PROPAGATION TEMPLATE

Propagate input uncertainties through model to quantify output uncertainty.
"""

import numpy as np
from scipy import stats
from scipy.stats import qmc
import matplotlib.pyplot as plt

# =============================================================================
# STEP 1: Define Input Uncertainties (USER CONFIGURABLE)
# =============================================================================

# Number of uncertain inputs
D = 3

# Define input distributions (MODIFY FOR YOUR PROBLEM)
input_distributions = {
    'param_1': stats.norm(loc=100, scale=10),      # Normal: mean=100, std=10
    'param_2': stats.uniform(loc=0, scale=1),      # Uniform: [0, 1]
    'param_3': stats.lognorm(s=0.3, scale=50),     # Lognormal: median≈50, CV=0.3
}

# Correlation matrix (optional - for independent inputs, use identity)
# Set to None for independent inputs
correlation_matrix = None  # No correlation

# Alternative: Specify correlations
# correlation_matrix = np.array([
#     [1.0, 0.5, 0.2],
#     [0.5, 1.0, 0.3],
#     [0.2, 0.3, 1.0]
# ])

# Simulation parameters
N_SAMPLES = 10000
RANDOM_SEED = 42
USE_LHS = True  # Use Latin Hypercube Sampling for efficiency

# =============================================================================
# STEP 2: Define Model (REPLACE WITH YOUR MODEL)
# =============================================================================

def model_function(param_1, param_2, param_3):
    """
    Your system model that transforms inputs to output.

    Args:
        param_1, param_2, param_3: Input parameters (scalars or arrays)

    Returns:
        output: Model prediction (scalar or array)
    """
    # EXAMPLE: Nonlinear model with interactions
    output = (param_1 * param_2 +
              np.sqrt(param_3) * 10 +
              param_1 * param_3 / 100)

    return output

# =============================================================================
# STEP 3: Generate Samples (REUSABLE PATTERN)
# =============================================================================

np.random.seed(RANDOM_SEED)

if USE_LHS:
    # Latin Hypercube Sampling (better space-filling than random)
    sampler = qmc.LatinHypercube(d=D, seed=RANDOM_SEED)
    unit_samples = sampler.random(n=N_SAMPLES)  # Uniform [0,1]^D samples

    # Transform to desired distributions
    param_names = list(input_distributions.keys())
    samples = {}
    for i, name in enumerate(param_names):
        # Use inverse CDF (PPF) to transform uniform [0,1] to target distribution
        samples[name] = input_distributions[name].ppf(unit_samples[:, i])

else:
    # Standard Monte Carlo sampling
    samples = {}
    for name, dist in input_distributions.items():
        samples[name] = dist.rvs(size=N_SAMPLES)

# Handle correlations if specified
if correlation_matrix is not None:
    # Transform to correlated using Gaussian copula approach
    # (Advanced - for simplicity, shown without implementation)
    # Typically use: scipy.stats.multivariate_normal or OpenTURNS/Chaospy
    print("Warning: Correlation specified but not implemented in basic template.")
    print("Use OpenTURNS or Chaospy for complex correlations.")

print(f"Generated {N_SAMPLES} samples using {'LHS' if USE_LHS else 'Random MC'}")

# =============================================================================
# STEP 4: Propagate Uncertainty (REUSABLE PATTERN)
# =============================================================================

# Evaluate model for all samples
outputs = model_function(samples['param_1'], samples['param_2'], samples['param_3'])

print(f"Model evaluations complete. Output range: [{outputs.min():.2f}, {outputs.max():.2f}]")

# =============================================================================
# STEP 5: Characterize Output Uncertainty (REUSABLE PATTERN)
# =============================================================================

# Summary statistics
mean_output = outputs.mean()
median_output = np.median(outputs)
std_output = outputs.std()
cv_output = std_output / mean_output  # Coefficient of variation

# Percentiles
percentiles = [5, 25, 50, 75, 95]
percentile_values = np.percentile(outputs, percentiles)

# Prediction interval (e.g., 90%)
pi_lower = np.percentile(outputs, 5)
pi_upper = np.percentile(outputs, 95)

print("\nOUTPUT UNCERTAINTY CHARACTERIZATION")
print("=" * 70)
print(f"Mean: {mean_output:.2f}")
print(f"Median: {median_output:.2f}")
print(f"Std Dev: {std_output:.2f}")
print(f"Coefficient of Variation: {cv_output:.2%}")
print()
print(f"90% Prediction Interval: [{pi_lower:.2f}, {pi_upper:.2f}]")
print()
print("Percentiles:")
for p, v in zip(percentiles, percentile_values):
    print(f"  {p}th: {v:.2f}")

# =============================================================================
# STEP 6: Variance Decomposition (OPTIONAL - Input Contribution)
# =============================================================================

# Simple correlation-based attribution (for linear models)
# For nonlinear models, use sensitivity analysis (see sensitivity-analysis-pattern.md)

correlations = {}
for name in input_distributions.keys():
    corr = np.corrcoef(samples[name], outputs)[0, 1]
    correlations[name] = corr

print("\nINPUT-OUTPUT CORRELATIONS:")
print("(Approximate measure of input contribution to output uncertainty)")
for name, corr in sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {name}: {corr:+.3f}")

print("\nNote: For nonlinear models, use Sobol indices for accurate variance decomposition.")

# =============================================================================
# STEP 7: Compare Deterministic vs. Uncertain Predictions
# =============================================================================

# Deterministic prediction (using mean inputs)
deterministic_inputs = {name: dist.mean() for name, dist in input_distributions.items()}
deterministic_output = model_function(
    deterministic_inputs['param_1'],
    deterministic_inputs['param_2'],
    deterministic_inputs['param_3']
)

print("\nDETERMINISTIC vs. UNCERTAIN PREDICTIONS:")
print(f"Deterministic (mean inputs): {deterministic_output:.2f}")
print(f"Uncertain (mean output): {mean_output:.2f}")
print(f"Difference: {mean_output - deterministic_output:.2f}")
print(f"Uncertainty range: ±{std_output:.2f} (1 std dev)")

# =============================================================================
# STEP 8: Visualize Uncertainty Propagation (REUSABLE PATTERN)
# =============================================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Output distribution
axes[0, 0].hist(outputs, bins=50, density=True, alpha=0.7, color='steelblue', edgecolor='black')
axes[0, 0].axvline(mean_output, color='red', linestyle='--', linewidth=2, label='Mean')
axes[0, 0].axvline(median_output, color='orange', linestyle='--', linewidth=2, label='Median')
axes[0, 0].axvline(pi_lower, color='green', linestyle=':', linewidth=2, label='90% PI')
axes[0, 0].axvline(pi_upper, color='green', linestyle=':', linewidth=2)
axes[0, 0].set_xlabel('Output Value')
axes[0, 0].set_ylabel('Probability Density')
axes[0, 0].set_title('Output Distribution (Uncertainty Propagation)')
axes[0, 0].legend()
axes[0, 0].grid(alpha=0.3)

# Plot 2: Input-output scatter (for first input)
first_param = list(input_distributions.keys())[0]
axes[0, 1].scatter(samples[first_param], outputs, alpha=0.3, s=10)
axes[0, 1].set_xlabel(f'{first_param} (Input)')
axes[0, 1].set_ylabel('Output')
axes[0, 1].set_title(f'Output vs. {first_param}')
axes[0, 1].grid(alpha=0.3)

# Plot 3: Cumulative distribution
sorted_outputs = np.sort(outputs)
cumulative = np.arange(1, len(sorted_outputs) + 1) / len(sorted_outputs)
axes[1, 0].plot(sorted_outputs, cumulative, linewidth=2, color='navy')
axes[1, 0].axhline(0.5, color='orange', linestyle='--', alpha=0.5, label='Median')
axes[1, 0].axhline(0.05, color='green', linestyle=':', alpha=0.5, label='5th/95th percentile')
axes[1, 0].axhline(0.95, color='green', linestyle=':', alpha=0.5)
axes[1, 0].set_xlabel('Output Value')
axes[1, 0].set_ylabel('Cumulative Probability')
axes[1, 0].set_title('Cumulative Distribution Function')
axes[1, 0].legend()
axes[1, 0].grid(alpha=0.3)

# Plot 4: Correlation bar chart
param_names = list(correlations.keys())
corr_values = [abs(correlations[name]) for name in param_names]
colors_corr = ['red' if correlations[name] < 0 else 'blue' for name in param_names]

axes[1, 1].barh(param_names, corr_values, color=colors_corr, alpha=0.7)
axes[1, 1].set_xlabel('|Correlation| with Output')
axes[1, 1].set_title('Input Contribution to Output Uncertainty')
axes[1, 1].grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('uncertainty_propagation.png', dpi=300, bbox_inches='tight')
print("\nVisualization saved to 'uncertainty_propagation.png'")

# =============================================================================
# STEP 9: Convergence Check
# =============================================================================

# Check if N_SAMPLES is sufficient
sample_sizes = [100, 500, 1000, 5000, N_SAMPLES]
means_by_n = []
stds_by_n = []

for n in sample_sizes:
    if n <= N_SAMPLES:
        subset = outputs[:n]
        means_by_n.append(subset.mean())
        stds_by_n.append(subset.std())

print("\nCONVERGENCE ANALYSIS:")
print(f"{'N Samples':<12} {'Mean':<12} {'Std Dev':<12}")
print("-" * 36)
for n, m, s in zip(sample_sizes[:len(means_by_n)], means_by_n, stds_by_n):
    print(f"{n:<12} {m:<12.2f} {s:<12.2f}")

print("\nStatistics should stabilize. If still changing >1%, increase N_SAMPLES.")

# =============================================================================
# STEP 10: Advanced - Surrogate Modeling for Expensive Models
# =============================================================================

"""
For expensive models (evaluation time > 1 second), use surrogate:

import chaospy as cp

# Define joint distribution
dist = cp.J(
    cp.Normal(100, 10),
    cp.Uniform(0, 1),
    cp.LogNormal(mu=np.log(50), sigma=0.3)
)

# Generate polynomial chaos expansion
expansion = cp.generate_expansion(order=3, dist=dist)

# Generate quadrature points (few model evaluations needed)
nodes, weights = cp.generate_quadrature(order=4, dist=dist)

# Evaluate expensive model at quadrature points only
evaluations = []
for i in range(nodes.shape[1]):
    eval_point = model_function(nodes[0, i], nodes[1, i], nodes[2, i])
    evaluations.append(eval_point)

# Fit surrogate model
surrogate = cp.fit_quadrature(expansion, nodes, weights, evaluations)

# Now use surrogate for instant predictions
mean_surrogate = cp.E(surrogate, dist)
std_surrogate = cp.Std(surrogate, dist)

print(f"Surrogate mean: {mean_surrogate:.2f}")
print(f"Surrogate std: {std_surrogate:.2f}")
print(f"Model evaluations: {nodes.shape[1]} instead of {N_SAMPLES}")

# Sample from surrogate for distribution
surrogate_samples = surrogate(*dist.sample(N_SAMPLES))
"""
```

## Multi-Domain Examples

### Example 1: Structural Engineering - Bridge Load Capacity

**Problem**: Propagate material property uncertainties through stress calculation.

**Uncertain Inputs** (D=4):
- `steel_yield_strength`: Normal(250 MPa, 15 MPa) - material testing variability
- `concrete_compressive_strength`: Lognormal(median=30 MPa, CV=0.15) - batch variation
- `applied_load`: Gumbel distribution - extreme value for wind/traffic
- `geometric_tolerance`: Uniform(±2mm) - construction precision

**Model**: Finite element stress analysis (expensive: 10 min per run)

**Analysis**:
- Use Chaospy PCE with order=3 polynomial (requires ~50 evaluations)
- Output: Maximum stress under load
- Compare to deterministic: Mean inputs give stress=180 MPa (safe)
- Uncertain: 95th percentile stress=220 MPa (closer to limit)

**Result**: Uncertainty propagation reveals 8% probability of exceeding design limit.

### Example 2: Pharmaceutical - Drug Dosing

**Problem**: Propagate patient variability through pharmacokinetic model.

**Uncertain Inputs** (D=5):
- `body_weight`: Normal(70 kg, 15 kg) - patient population
- `liver_clearance_rate`: Lognormal - metabolic variability
- `kidney_function`: Truncated normal - age-related decline
- `absorption_rate`: Uniform - food effects
- `volume_of_distribution`: Correlated with body_weight

**Model**: PK/PD model (differential equations, fast evaluation)

**Analysis**:
- Standard MC with N=20,000 (fast model allows large N)
- Handle weight-volume correlation with multivariate normal
- Output: Plasma concentration at 4 hours
- Therapeutic window: [5, 20] mg/L

**Result**: 85% of population within window; 12% underdosed, 3% overdosed.

### Example 3: Climate Science - Temperature Projection

**Problem**: Propagate climate model parameter uncertainties to 2100 temperature.

**Uncertain Inputs** (D=8):
- `climate_sensitivity`: Lognormal(median=3°C, 5th-95th: 2-4.5°C) - key uncertainty
- `ocean_heat_uptake`: Uniform - poorly constrained
- `aerosol_forcing`: Normal with large uncertainty
- `carbon_cycle_feedback`: Triangular(min, mode, max) from expert elicitation
- `emission_scenario_parameters`: Multiple correlated variables

**Model**: Earth system model (very expensive: hours per run)

**Analysis**:
- Use ensemble of N=300 runs from international project
- Treat as empirical distribution (no surrogate needed, already sampled)
- Propagate through simple energy balance model for regional projections

**Result**: Global mean warming 2.5-4.5°C (66% range), but regional uncertainty much larger.

### Example 4: Manufacturing - Process Yield

**Problem**: Propagate process parameter uncertainties through yield calculation.

**Uncertain Inputs** (D=6):
- `temperature`: Normal(350°C, 5°C) - thermostat precision
- `pressure`: Normal(2.0 atm, 0.1 atm) - pressure control
- `feed_composition`: Dirichlet distribution - mixture fractions must sum to 1
- `catalyst_activity`: Lognormal - batch-to-batch variation
- `residence_time`: Uniform - flow rate fluctuations
- `moisture_content`: Beta distribution - bounded [0, 1]

**Model**: Kinetic rate equations (fast evaluation)

**Analysis**:
- LHS with N=5,000 for efficiency
- Constrained sampling for composition (sum=1 constraint)
- Output: Product yield (%)

**Result**: Mean yield 87% (vs. deterministic 90%); high sensitivity to catalyst activity.

### Example 5: Finance - Option Pricing

**Problem**: Propagate volatility and rate uncertainties through option pricing model.

**Uncertain Inputs** (D=3):
- `volatility`: Lognormal(median=0.25, CV=0.20) - implied volatility uncertainty
- `risk_free_rate`: Normal(0.03, 0.005) - term structure uncertainty
- `dividend_yield`: Uniform(0.01, 0.03) - company policy uncertainty

**Model**: Black-Scholes with Monte Carlo path simulation

**Analysis**:
- QMC (Sobol sequence) with N=10,000 for efficiency
- Nested MC: Outer loop for parameters, inner loop for price paths
- Output: Option value

**Result**: Option value $12.50 ± $1.80 (1 std dev); parametric uncertainty dominates path variability.

## Integration Patterns

### Combining with Sensitivity Analysis

1. Propagate uncertainty first to get output distribution
2. Run sensitivity analysis to decompose output variance by input
3. Focus uncertainty reduction on high-sensitivity inputs
4. Iterate: Reduce input uncertainty → re-propagate → measure improvement

### Combining with Confidence Intervals

- Propagation gives prediction interval (uncertainty in outcome)
- Add epistemic uncertainty → confidence interval on prediction interval
- Distinguish: aleatory (irreducible randomness) vs. epistemic (model uncertainty)

### Combining with Model Calibration

- Propagate parameter uncertainties post-calibration
- Posterior predictive distribution (Bayesian)
- Assess: Is output uncertainty acceptable given calibrated parameters?

## Common Pitfalls

1. **Ignoring Correlations**: Assuming independence when inputs are correlated biases results
2. **Wrong Distribution**: Using normal when lognormal appropriate (physical quantities > 0)
3. **Insufficient Samples**: N too small for tail percentiles (need N > 1000 for 95th percentile)
4. **Deterministic Fallacy**: Mean inputs ≠ mean output for nonlinear models
5. **Confusing Aleatory and Epistemic**: Natural variability vs. knowledge uncertainty

## Gap Identification

**Current Limitations**:
- Time-dependent uncertainty (propagating over time with autocorrelation) requires custom implementation
- High-dimensional UQ (D > 100) needs dimensionality reduction (active subspaces) - limited tools
- Robust UQ (distribution on distributions, ambiguity sets) emerging research area
- Real-time UQ (online updating as data arrives) not standardized
- Multi-fidelity UQ (combining cheap/expensive models) requires specialized frameworks
