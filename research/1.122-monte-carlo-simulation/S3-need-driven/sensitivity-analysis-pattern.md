# Sensitivity Analysis Pattern

## Pattern Definition

**Generic Use Case**: "System with D input parameters, need to identify which inputs most affect output"

**Core Question**: If I could measure/control only a subset of my input parameters more precisely, which ones would have the biggest impact on my output?

**Parameterization**:
- **D**: Number of input parameters (typical range: 5-50)
- **N**: Monte Carlo samples required (typical range: 1000-100000)
- **evaluation_time**: Time per model evaluation (ranges from microseconds to hours)
- **output_type**: Scalar, vector, or multivariate output
- **correlation**: Are inputs independent or correlated?

## Requirements Breakdown

### Functional Requirements

**FR1: Sensitivity Metric Calculation**
- Must calculate sensitivity indices showing input importance
- Common metrics: Sobol indices, Morris screening, correlation ratios
- Must handle both first-order (individual) and total-order (with interactions) effects

**FR2: Sampling Strategy**
- Must generate samples that efficiently explore parameter space
- Support for: random sampling, Latin hypercube, quasi-random sequences
- Must handle correlated input parameters

**FR3: Model Integration**
- Must work with arbitrary black-box model functions
- No restriction on model internal structure
- Support for expensive evaluations (caching, parallelization)

**FR4: Statistical Validation**
- Must provide confidence intervals on sensitivity estimates
- Bootstrap or analytical methods for uncertainty quantification
- Convergence diagnostics

### Performance Requirements

**PR1: Computational Efficiency**
- For D < 10: Should complete in minutes on standard hardware
- For 10 ≤ D ≤ 50: Should complete in hours, not days
- For D > 50: Should provide screening methods requiring O(D) evaluations

**PR2: Sample Efficiency**
- Should minimize N relative to D
- Best methods: O(D) to O(D²) evaluations
- Avoid methods requiring O(D!) evaluations

### Usability Requirements

**UR1: Developer Experience**
- Should require minimal boilerplate code
- Clear separation of: parameter definition, model definition, analysis
- Interpretable output (rankings, charts)

**UR2: Flexibility**
- Support arbitrary probability distributions
- Support bounded, unbounded, discrete parameters
- Easy to add custom sensitivity metrics

## Library Fit Analysis

### NumPy/SciPy (Foundation Tier)

**Fit Score**: ○ Partial Support

**Capabilities**:
- ✓ Parameter distribution sampling (scipy.stats)
- ✓ Basic correlation analysis (numpy.corrcoef, scipy.stats.spearmanr)
- ○ Variance decomposition (manual implementation required)
- ✗ No Sobol index calculation
- ✗ No Morris screening

**Best For**:
- Simple correlation-based sensitivity (D < 10)
- Quick exploration before rigorous analysis
- When you need full control over the analysis method

**Limitations**:
- Requires manual implementation of advanced methods
- No built-in sampling strategies (LHS, quasi-random)
- No statistical validation of sensitivity estimates

### SALib (Specialized Tier)

**Fit Score**: ✓ Perfect Fit

**Capabilities**:
- ✓ Multiple sensitivity methods (Sobol, Morris, FAST, Delta, DGSM)
- ✓ Efficient sampling strategies (Saltelli, Morris, Sobol sequences)
- ✓ Statistical confidence intervals
- ✓ Handles correlated inputs
- ✓ Convergence analysis tools
- ✓ Visualization utilities

**Best For**:
- Global sensitivity analysis (any D)
- Rigorous variance-based methods (Sobol indices)
- Screening large parameter spaces (Morris method for D > 20)
- Publication-quality sensitivity analysis

**Limitations**:
- Focused on sensitivity analysis only (not general Monte Carlo)
- Learning curve for understanding different methods
- Some methods require specific sample sizes

### Chaospy (Specialized Tier)

**Fit Score**: ○ Good Fit

**Capabilities**:
- ✓ Advanced sampling (LHS, Hammersley, Sobol sequences)
- ✓ Polynomial chaos expansion for sensitivity
- ✓ Sophisticated distribution handling
- ○ Sensitivity via variance decomposition (indirect method)
- ✗ No Morris screening

**Best For**:
- When combining sensitivity with surrogate modeling
- Problems with smooth response surfaces
- Need for both sensitivity and uncertainty quantification

**Limitations**:
- Indirect sensitivity calculation (via PCE)
- Assumes sufficient smoothness for polynomial approximation
- More complex API than SALib

### OpenTURNS (Domain-Specific Tier)

**Fit Score**: ✓ Perfect Fit (Engineering Focus)

**Capabilities**:
- ✓ Comprehensive sensitivity methods (Sobol, ANCOVA, HSIC)
- ✓ Advanced sampling (LHS, QMC sequences)
- ✓ Handles dependencies via copulas
- ✓ Integration with reliability analysis
- ✓ Parallel evaluation support

**Best For**:
- Engineering/reliability applications
- Complex dependency structures
- Large-scale problems (D > 50) with parallel computing
- When combining sensitivity with reliability analysis

**Limitations**:
- Heavy dependency (large installation)
- Steeper learning curve
- More verbose API

## Recommendation by Problem Scale

### Small Problems (D < 10, Fast Evaluation < 1ms)

**Recommended**: NumPy/SciPy + Manual Implementation
- Use simple correlation-based methods
- N = 1000-5000 samples sufficient
- Rapid prototyping without dependencies

**Alternative**: SALib (if rigorous metrics needed)

### Medium Problems (10 ≤ D ≤ 30, Medium Evaluation 1ms-1s)

**Recommended**: SALib
- Use Sobol method for rigorous variance-based sensitivity
- N ≈ 5000-20000 samples (depends on D)
- Well-tested, widely-used methods

### Large Problems (D > 30, Any Evaluation Speed)

**Recommended**: SALib (Morris screening first, then targeted Sobol)
- Morris screening: O(D) evaluations, identifies key parameters
- Sobol on screened subset: Rigorous analysis of important parameters only
- N ≈ 1000 for Morris, then 10000+ for Sobol on subset

### Expensive Evaluations (> 1 second per evaluation)

**Recommended**: SALib Morris + Surrogate Model
1. Use Morris screening with N = 50-100
2. Build surrogate (Gaussian process, polynomial)
3. Run Sobol on surrogate model
4. Validate key findings on original model

## Generic Code Template

```python
"""
GENERIC SENSITIVITY ANALYSIS TEMPLATE

Replace placeholders with your problem parameters and model.
"""

import numpy as np
from SALib.sample import saltelli
from SALib.analyze import sobol
import matplotlib.pyplot as plt

# =============================================================================
# STEP 1: Define Your Problem (USER CONFIGURABLE)
# =============================================================================

problem = {
    'num_vars': 5,  # D: Number of input parameters
    'names': ['param_1', 'param_2', 'param_3', 'param_4', 'param_5'],
    'bounds': [
        [0.5, 1.5],    # param_1 range: [lower, upper]
        [10, 50],      # param_2 range
        [0.0, 1.0],    # param_3 range
        [100, 500],    # param_4 range
        [0.1, 10.0]    # param_5 range
    ]
}

# For correlated inputs, define correlation matrix (optional)
# correlation_matrix = np.array([
#     [1.0, 0.7, 0.0, 0.0, 0.0],
#     [0.7, 1.0, 0.0, 0.0, 0.0],
#     ...
# ])

# =============================================================================
# STEP 2: Define Your Model Function (REPLACE WITH YOUR MODEL)
# =============================================================================

def model_function(X):
    """
    Your system model.

    Args:
        X: numpy array of shape (N, D) where N is samples, D is parameters
           Each row is [param_1, param_2, ..., param_D]

    Returns:
        Y: numpy array of shape (N,) with model outputs
    """
    # EXAMPLE: Ishigami function (replace with your model)
    # X[:, 0] is param_1, X[:, 1] is param_2, etc.

    # Simple example: weighted sum with nonlinear terms
    Y = (X[:, 0] * 2.0 +                    # Linear term
         X[:, 1] ** 2 * 0.5 +               # Quadratic term
         np.sin(X[:, 2]) * X[:, 3] +        # Interaction term
         np.exp(X[:, 4] / 10.0))            # Exponential term

    return Y

# =============================================================================
# STEP 3: Generate Samples (REUSABLE PATTERN)
# =============================================================================

# Calculate required samples for Sobol analysis
# Rule of thumb: N = 1000 * D for convergence
N_BASE = 1000  # Base sample size (increase for accuracy)
param_values = saltelli.sample(problem, N_BASE)

print(f"Generated {param_values.shape[0]} parameter sets for {problem['num_vars']} parameters")
print(f"Expected evaluations: {N_BASE * (2 * problem['num_vars'] + 2)}")

# =============================================================================
# STEP 4: Evaluate Model (MODIFY FOR PARALLEL/CACHING IF NEEDED)
# =============================================================================

Y = model_function(param_values)

print(f"Model evaluations complete. Output range: [{Y.min():.3f}, {Y.max():.3f}]")

# =============================================================================
# STEP 5: Analyze Sensitivity (REUSABLE PATTERN)
# =============================================================================

Si = sobol.analyze(problem, Y, print_to_console=False)

# Extract sensitivity indices
S1 = Si['S1']        # First-order indices (individual effect)
ST = Si['ST']        # Total-order indices (individual + interactions)
S1_conf = Si['S1_conf']  # 95% confidence intervals
ST_conf = Si['ST_conf']

# =============================================================================
# STEP 6: Interpret Results (REUSABLE PATTERN)
# =============================================================================

print("\nSENSITIVITY ANALYSIS RESULTS")
print("=" * 70)
print(f"{'Parameter':<15} {'S1 (Individual)':<20} {'ST (Total)':<20}")
print("-" * 70)

for i, name in enumerate(problem['names']):
    print(f"{name:<15} {S1[i]:>6.3f} ± {S1_conf[i]:>5.3f}      "
          f"{ST[i]:>6.3f} ± {ST_conf[i]:>5.3f}")

print("\nINTERPRETATION:")
print("- S1 (First-order): Direct effect of this parameter alone")
print("- ST (Total-order): Total effect including interactions with other parameters")
print("- ST - S1: Interaction effects with other parameters")
print("\nPrioritize parameters with high ST values for further investigation.")

# =============================================================================
# STEP 7: Visualize (OPTIONAL)
# =============================================================================

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: First-order sensitivity indices
indices = np.arange(len(problem['names']))
ax1.bar(indices, S1, yerr=S1_conf, capsize=5, alpha=0.7, color='steelblue')
ax1.set_xlabel('Parameter')
ax1.set_ylabel('First-Order Sensitivity (S1)')
ax1.set_title('Individual Parameter Effects')
ax1.set_xticks(indices)
ax1.set_xticklabels(problem['names'], rotation=45, ha='right')
ax1.grid(axis='y', alpha=0.3)

# Plot 2: Total-order sensitivity indices
ax2.bar(indices, ST, yerr=ST_conf, capsize=5, alpha=0.7, color='coral')
ax2.set_xlabel('Parameter')
ax2.set_ylabel('Total-Order Sensitivity (ST)')
ax2.set_title('Total Parameter Effects (Including Interactions)')
ax2.set_xticks(indices)
ax2.set_xticklabels(problem['names'], rotation=45, ha='right')
ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('sensitivity_analysis.png', dpi=300, bbox_inches='tight')
print("\nVisualization saved to 'sensitivity_analysis.png'")

# =============================================================================
# STEP 8: Screening Method for Large D (ALTERNATIVE FOR D > 30)
# =============================================================================

"""
For large parameter spaces (D > 30), use Morris screening first:

from SALib.sample import morris as morris_sampler
from SALib.analyze import morris

# Generate Morris samples (much fewer required)
param_values_morris = morris_sampler.sample(problem, N=100, num_levels=4)

# Evaluate model
Y_morris = model_function(param_values_morris)

# Analyze with Morris method
Si_morris = morris.analyze(problem, param_values_morris, Y_morris,
                           print_to_console=False)

# Identify important parameters (μ* > threshold)
important_params = [problem['names'][i]
                   for i in range(len(problem['names']))
                   if Si_morris['mu_star'][i] > threshold_value]

# Then run detailed Sobol analysis on important_params subset only
"""
```

## Multi-Domain Examples

### Example 1: Manufacturing - Production Line Throughput

**Problem**: Manufacturing line with 8 parameters affecting throughput.

**Parameters** (D=8):
- `machine_speed_1` through `machine_speed_4`: Processing rates (parts/hour)
- `failure_rate_1` through `failure_rate_3`: Machine breakdown rates (failures/day)
- `buffer_capacity`: Queue size between stations

**Model**: Discrete-event simulation of production line

**Analysis Approach**:
- Use SALib Morris screening (N=200 evaluations, ~1 hour runtime)
- Expected finding: Buffer capacity typically has low S1 but high ST (interactions)
- Machine speeds usually have high S1 (direct effects dominate)

### Example 2: Finance - Portfolio Value at Risk

**Problem**: Portfolio with 15 asset return assumptions.

**Parameters** (D=15):
- `expected_return_asset_i`: Mean returns for 10 assets
- `volatility_asset_i`: Standard deviations for 5 key assets
- `correlation_coeff_1_2`: Correlation between asset pairs (selected pairs)

**Model**: Monte Carlo portfolio simulation over time horizon

**Analysis Approach**:
- Use SALib Sobol method (N=10000, fast evaluation)
- Expected finding: Correlations have high ST-S1 (strong interactions)
- Volatilities of large positions dominate individual effects

### Example 3: Healthcare - Emergency Department Wait Time

**Problem**: ER with 6 patient flow parameters.

**Parameters** (D=6):
- `arrival_rate`: Patients per hour
- `triage_time`: Mean triage duration (minutes)
- `treatment_time_minor`: Mean treatment for minor cases
- `treatment_time_major`: Mean treatment for major cases
- `num_doctors`: Staffing level
- `acuity_distribution`: Fraction of major vs minor cases

**Model**: Queueing simulation (SimPy) over 24-hour period

**Analysis Approach**:
- Use SALib Sobol method (N=5000, medium evaluation time)
- Expected finding: `num_doctors` and `arrival_rate` high ST values
- Interaction between `acuity_distribution` and treatment times

### Example 4: Logistics - Delivery Time Prediction

**Problem**: Delivery network with 10 uncertainty factors.

**Parameters** (D=10):
- `base_travel_time`: Distance-based travel time
- `traffic_factor`: Traffic congestion multiplier
- `weather_delay`: Weather-related delays
- `loading_time`: Warehouse loading duration
- `driver_efficiency`: Driver experience factor
- `vehicle_reliability`: Breakdown probability
- `demand_volume`: Number of stops
- `route_complexity`: Urban vs rural routing
- `time_of_day`: Peak vs off-peak traffic
- `seasonal_factor`: Holiday season effects

**Model**: Network simulation with stochastic routing

**Analysis Approach**:
- Use SALib Morris first (D large, N=300)
- Screen to 4-5 key parameters
- Run Sobol on screened subset (N=8000)
- Expected finding: `traffic_factor` and `demand_volume` dominate
- Strong interactions between `time_of_day` and `traffic_factor`

### Example 5: Scientific Research - Chemical Reaction Yield

**Problem**: Lab experiment with 7 controllable conditions.

**Parameters** (D=7):
- `temperature`: Reaction temperature (°C)
- `pressure`: System pressure (atm)
- `concentration_reactant_A`: Molarity
- `concentration_reactant_B`: Molarity
- `catalyst_amount`: Catalyst loading (%)
- `reaction_time`: Duration (minutes)
- `mixing_speed`: Stirring rate (RPM)

**Model**: Kinetic model or surrogate from experimental data

**Analysis Approach**:
- Use SALib Sobol method (N=5000)
- Run on surrogate model (Gaussian process fit to experimental data)
- Expected finding: `temperature` and `catalyst_amount` high S1
- Interaction between `concentration_A` and `concentration_B`
- Use results to design factorial experiments for validation

## Integration Patterns

### Combining with Other Patterns

**Sensitivity + Confidence Intervals**:
- Run sensitivity analysis first to identify key parameters
- Focus uncertainty quantification on high-ST parameters only
- Reduces computational cost of full uncertainty propagation

**Sensitivity + Risk Quantification**:
- Sensitivity shows which parameters to measure more precisely
- Risk analysis quantifies how precision improvements affect success probability

**Sensitivity + Model Calibration**:
- Parameters with low ST can be fixed at nominal values
- Calibrate only high-ST parameters against data
- Reduces calibration dimensionality

## Common Pitfalls

1. **Insufficient Sample Size**: Sobol indices require N × (2D + 2) evaluations minimum
2. **Ignoring Correlations**: Independent assumption when inputs are correlated biases results
3. **Wrong Method for Scale**: Using Sobol for D > 50 is computationally prohibitive
4. **Misinterpreting ST - S1**: Large difference indicates interactions, not measurement error
5. **Single Output Focus**: Sensitivity can differ for multiple output metrics

## Gap Identification

**Current Limitations**:
- Time-dependent sensitivity (how sensitivity changes over time) requires custom implementation
- Sensitivity with categorical/discrete parameters poorly supported
- Real-time sensitivity (updating as new data arrives) not well addressed
- Sensitivity under model uncertainty (epistemic uncertainty in model form) limited tools
