# Confidence Interval Pattern

## Pattern Definition

**Generic Use Case**: "Stochastic model produces variable outputs, need statistical bounds on predictions"

**Core Question**: Given my model has randomness/uncertainty, what range of outputs can I expect with X% confidence?

**Parameterization**:
- **N**: Number of Monte Carlo replications needed
- **confidence_level**: Desired confidence (e.g., 90%, 95%, 99%)
- **output_type**: Scalar, vector, time series, or multivariate
- **distribution_type**: Known (e.g., normal) or unknown/empirical
- **tail_behavior**: Interest in mean, median, extreme percentiles

## Requirements Breakdown

### Functional Requirements

**FR1: Confidence Interval Calculation**
- Must calculate percentile-based intervals for any distribution
- Support parametric methods (when distribution known)
- Support non-parametric/empirical methods (bootstrap, percentile)
- Handle multiple output metrics simultaneously

**FR2: Sample Size Determination**
- Must estimate N required for desired precision
- Convergence diagnostics (has N been reached?)
- Adaptive sampling (add more samples if needed)

**FR3: Multiple Comparison Correction**
- When estimating intervals for K outputs, adjust confidence levels
- Bonferroni, Benjamini-Hochberg, or simultaneous intervals

**FR4: Bootstrap Support**
- Resample existing simulation output for CI on statistics
- Bootstrap for derived quantities (ratios, percentiles)
- Bias correction methods

### Performance Requirements

**PR1: Memory Efficiency**
- For N > 1M samples, should not require storing all values
- Streaming/online algorithms for percentiles
- Incremental updates as samples arrive

**PR2: Computational Efficiency**
- Fast percentile calculation (O(N log N) acceptable, O(N) preferred)
- Parallel sample generation
- Vectorized operations over samples

### Usability Requirements

**UR1: Output Formats**
- Standard interval notation: [lower, upper]
- Graphical output: histograms with CI bands, box plots
- Structured output for reporting (mean ± CI, median [IQR])

**UR2: Interpretation Support**
- Clear distinction: confidence interval vs. prediction interval
- Context for interval width (is this precise enough?)
- Relationship between N and CI width

## Library Fit Analysis

### NumPy/SciPy (Foundation Tier)

**Fit Score**: ✓ Perfect Fit (Basic Use Cases)

**Capabilities**:
- ✓ Percentile calculation (numpy.percentile, numpy.quantile)
- ✓ Bootstrap sampling (numpy.random.choice with replacement)
- ✓ Parametric CIs if distribution known (scipy.stats distributions)
- ✓ Fast, memory-efficient for moderate N
- ○ No built-in convergence diagnostics
- ✗ No automatic multiple comparison correction

**Best For**:
- Standard confidence intervals on scalar outputs
- When N < 1M and fits in memory
- Quick analysis without dependencies
- Educational/teaching contexts

**Limitations**:
- Manual implementation of bootstrap bias correction
- No streaming percentile algorithms
- No built-in CI width prediction

### SciPy.stats (Foundation Tier)

**Fit Score**: ✓ Excellent Fit

**Capabilities**:
- ✓ Parametric CIs via distribution fitting (fit() + interval())
- ✓ Non-parametric tests and CIs
- ✓ Bootstrap module (scipy.stats.bootstrap) since v1.7
- ✓ Multiple comparison methods (Bonferroni via manual calculation)
- ✓ Statistical tests for distribution assumptions

**Best For**:
- When you want parametric efficiency (assume normal/lognormal/etc)
- Bootstrap CIs on arbitrary statistics
- Combined hypothesis testing and interval estimation

**Limitations**:
- Bootstrap can be slow for large N or complex statistics
- Limited streaming/online capabilities

### Bootstrapped (Specialized Tier)

**Fit Score**: ○ Good Fit (Bootstrap-Specific)

**Capabilities**:
- ✓ Advanced bootstrap methods (percentile, BCa, ABC)
- ✓ Bias-corrected accelerated intervals
- ✓ Parallel bootstrap execution
- ○ Focused only on bootstrap (not general MC)
- ✗ Less maintained than SciPy

**Best For**:
- Advanced bootstrap methods (BCa when sample size small)
- Legacy code using this library
- When you need specific bootstrap variant

**Limitations**:
- SciPy.stats.bootstrap now provides similar functionality
- Smaller community, less active development

### Statsmodels (Domain-Specific Tier)

**Fit Score**: ○ Good Fit (Regression/Time Series Focus)

**Capabilities**:
- ✓ CIs for regression coefficients (extensive)
- ✓ Prediction intervals vs confidence intervals distinction
- ✓ Time series forecasting intervals (ARIMA, etc.)
- ○ Monte Carlo less central (focused on statistical models)
- ✓ Excellent for comparison with analytical methods

**Best For**:
- When MC is validating/extending regression analysis
- Time series prediction intervals
- Publication-quality statistical tables with CIs

**Limitations**:
- Overkill if you only need basic percentile CIs
- Heavy dependency for simple MC applications

### Pingouin (Specialized Tier)

**Fit Score**: ○ Good Fit (Statistical Testing Focus)

**Capabilities**:
- ✓ Clean API for confidence intervals
- ✓ Bootstrap CIs with simple syntax
- ✓ Parametric and non-parametric methods
- ✓ Excellent documentation and examples
- ○ Smaller scope than SciPy

**Best For**:
- Research/academic settings
- When you want simpler API than SciPy
- Combining MC with statistical testing

**Limitations**:
- Less comprehensive than SciPy
- Smaller community

## Recommendation by Use Case

### Scalar Output, Unknown Distribution, N < 100k

**Recommended**: NumPy percentile method
```python
lower = np.percentile(results, 2.5)   # 95% CI lower
upper = np.percentile(results, 97.5)  # 95% CI upper
```

**Why**: Simple, fast, no assumptions about distribution.

### Scalar Output, Known Distribution (e.g., Normal)

**Recommended**: SciPy parametric CI
```python
from scipy import stats
mean, std = results.mean(), results.std()
ci = stats.norm.interval(0.95, loc=mean, scale=std/np.sqrt(len(results)))
```

**Why**: More efficient (narrower CI) if distribution assumption valid.

### Complex Statistics (median, ratio, percentile)

**Recommended**: SciPy bootstrap
```python
from scipy.stats import bootstrap
res = bootstrap((data,), statistic=np.median, confidence_level=0.95)
```

**Why**: Bootstrap handles any statistic, doesn't assume distribution.

### Multiple Outputs (K > 10 metrics)

**Recommended**: NumPy percentile + Bonferroni correction
```python
adjusted_alpha = 0.05 / K  # Bonferroni
lower = np.percentile(results, adjusted_alpha/2 * 100, axis=0)
upper = np.percentile(results, (1 - adjusted_alpha/2) * 100, axis=0)
```

**Why**: Controls family-wise error rate across multiple CIs.

### Time Series or Functional Data

**Recommended**: Statsmodels (if ARIMA/regression) or NumPy percentile bands
```python
# Percentile bands over time
lower_band = np.percentile(timeseries_samples, 2.5, axis=0)
upper_band = np.percentile(timeseries_samples, 97.5, axis=0)
```

**Why**: Captures uncertainty evolution over time.

## Generic Code Template

```python
"""
GENERIC CONFIDENCE INTERVAL TEMPLATE

Calculate confidence intervals for Monte Carlo simulation results.
"""

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# =============================================================================
# STEP 1: Configure Analysis (USER CONFIGURABLE)
# =============================================================================

CONFIDENCE_LEVEL = 0.95  # 95% confidence interval
N_SAMPLES = 10000        # Number of Monte Carlo replications
RANDOM_SEED = 42         # For reproducibility

# =============================================================================
# STEP 2: Define Model with Uncertainty (REPLACE WITH YOUR MODEL)
# =============================================================================

def stochastic_model():
    """
    Your model with random inputs/processes.

    Returns:
        output: scalar or array of model outputs
    """
    # EXAMPLE: Project cost estimation with uncertainties
    base_cost = np.random.normal(loc=100000, scale=10000)  # Base cost uncertainty
    risk_event = np.random.binomial(n=1, p=0.15)           # 15% chance of risk
    risk_cost = risk_event * np.random.lognormal(mean=10, sigma=0.5)
    efficiency_factor = np.random.uniform(0.9, 1.1)

    total_cost = (base_cost + risk_cost) * efficiency_factor

    return total_cost

# =============================================================================
# STEP 3: Run Monte Carlo Simulation (REUSABLE PATTERN)
# =============================================================================

np.random.seed(RANDOM_SEED)

results = np.array([stochastic_model() for _ in range(N_SAMPLES)])

print(f"Completed {N_SAMPLES} Monte Carlo replications")
print(f"Output range: [{results.min():.2f}, {results.max():.2f}]")

# =============================================================================
# STEP 4: Calculate Confidence Intervals (REUSABLE PATTERN)
# =============================================================================

# Method 1: Percentile-based (non-parametric, most general)
alpha = 1 - CONFIDENCE_LEVEL
lower_percentile = (alpha / 2) * 100
upper_percentile = (1 - alpha / 2) * 100

ci_lower = np.percentile(results, lower_percentile)
ci_upper = np.percentile(results, upper_percentile)

# Method 2: Parametric (assumes normal distribution - faster but requires assumption)
mean = results.mean()
std_error = results.std() / np.sqrt(N_SAMPLES)
ci_parametric = stats.norm.interval(CONFIDENCE_LEVEL, loc=mean, scale=std_error)

# Method 3: Bootstrap (for derived statistics like median, percentiles)
# Useful when you want CI on median, IQR, or custom statistics
def my_statistic(data):
    return np.median(data)  # Replace with any statistic

bootstrap_result = stats.bootstrap(
    (results,),
    statistic=my_statistic,
    confidence_level=CONFIDENCE_LEVEL,
    n_resamples=1000,
    method='percentile'
)
ci_bootstrap = (bootstrap_result.confidence_interval.low,
                bootstrap_result.confidence_interval.high)

# =============================================================================
# STEP 5: Summary Statistics (REUSABLE PATTERN)
# =============================================================================

print("\nCONFIDENCE INTERVAL RESULTS")
print("=" * 70)
print(f"Sample size (N): {N_SAMPLES}")
print(f"Confidence level: {CONFIDENCE_LEVEL * 100}%")
print()
print(f"Mean: {mean:.2f}")
print(f"Median: {np.median(results):.2f}")
print(f"Std Dev: {results.std():.2f}")
print()
print("CONFIDENCE INTERVALS:")
print(f"  Percentile method: [{ci_lower:.2f}, {ci_upper:.2f}]")
print(f"  Parametric (normal): [{ci_parametric[0]:.2f}, {ci_parametric[1]:.2f}]")
print(f"  Bootstrap (on median): [{ci_bootstrap[0]:.2f}, {ci_bootstrap[1]:.2f}]")
print()
print(f"CI Width: {ci_upper - ci_lower:.2f}")
print(f"Relative Precision: ±{(ci_upper - ci_lower) / (2 * mean) * 100:.1f}%")

# =============================================================================
# STEP 6: Interpret Percentiles (REUSABLE PATTERN)
# =============================================================================

percentiles = [5, 25, 50, 75, 95]
percentile_values = np.percentile(results, percentiles)

print("\nPERCENTILE SUMMARY:")
for p, v in zip(percentiles, percentile_values):
    print(f"  {p}th percentile: {v:.2f}")

# Common interpretation:
# - [5th, 95th]: 90% prediction interval
# - [25th, 75th]: Interquartile range (IQR)
# - 50th: Median (robust to outliers)

# =============================================================================
# STEP 7: Assess Convergence (Check if N sufficient)
# =============================================================================

# Split samples into chunks and calculate CI width for each chunk size
chunk_sizes = [100, 500, 1000, 5000, N_SAMPLES]
ci_widths = []

for n in chunk_sizes:
    if n <= N_SAMPLES:
        sample = results[:n]
        lower = np.percentile(sample, lower_percentile)
        upper = np.percentile(sample, upper_percentile)
        ci_widths.append(upper - lower)

print("\nCONVERGENCE ANALYSIS:")
print(f"{'Sample Size':<15} {'CI Width':<15} {'% Change':<15}")
print("-" * 45)
for i, (n, width) in enumerate(zip(chunk_sizes[:len(ci_widths)], ci_widths)):
    pct_change = "" if i == 0 else f"{(ci_widths[i] - ci_widths[i-1]) / ci_widths[i-1] * 100:+.1f}%"
    print(f"{n:<15} {width:<15.2f} {pct_change:<15}")

print("\nCI width should stabilize as N increases. If still changing >5%, increase N.")

# =============================================================================
# STEP 8: Visualize (REUSABLE PATTERN)
# =============================================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Histogram with confidence interval
axes[0].hist(results, bins=50, density=True, alpha=0.7, color='steelblue', edgecolor='black')
axes[0].axvline(ci_lower, color='red', linestyle='--', linewidth=2, label=f'{CONFIDENCE_LEVEL*100}% CI')
axes[0].axvline(ci_upper, color='red', linestyle='--', linewidth=2)
axes[0].axvline(mean, color='green', linestyle='-', linewidth=2, label='Mean')
axes[0].axvline(np.median(results), color='orange', linestyle='-', linewidth=2, label='Median')
axes[0].set_xlabel('Output Value')
axes[0].set_ylabel('Probability Density')
axes[0].set_title(f'Distribution with {CONFIDENCE_LEVEL*100}% Confidence Interval')
axes[0].legend()
axes[0].grid(alpha=0.3)

# Plot 2: Box plot with percentiles
axes[1].boxplot(results, vert=True, widths=0.5)
axes[1].axhline(ci_lower, color='red', linestyle='--', linewidth=1.5, label=f'{CONFIDENCE_LEVEL*100}% CI')
axes[1].axhline(ci_upper, color='red', linestyle='--', linewidth=1.5)
axes[1].set_ylabel('Output Value')
axes[1].set_title('Box Plot with Confidence Interval')
axes[1].legend()
axes[1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('confidence_interval_analysis.png', dpi=300, bbox_inches='tight')
print("\nVisualization saved to 'confidence_interval_analysis.png'")

# =============================================================================
# STEP 9: Sample Size Planning (How much N is needed?)
# =============================================================================

def required_sample_size(desired_width, confidence_level, estimated_std):
    """
    Estimate required sample size for desired CI width.

    For normal approximation: width = 2 * z * (std / sqrt(N))
    Solving for N: N = (2 * z * std / width)^2

    Args:
        desired_width: Target CI width
        confidence_level: e.g., 0.95
        estimated_std: Estimated standard deviation (from pilot run)

    Returns:
        Required sample size
    """
    z = stats.norm.ppf(1 - (1 - confidence_level) / 2)
    N_required = ((2 * z * estimated_std) / desired_width) ** 2
    return int(np.ceil(N_required))

# Example: What N needed for CI width of 5000?
desired_ci_width = 5000
estimated_std = results.std()
N_required = required_sample_size(desired_ci_width, CONFIDENCE_LEVEL, estimated_std)

print(f"\nSAMPLE SIZE PLANNING:")
print(f"To achieve CI width of {desired_ci_width:.0f}:")
print(f"  Required N ≈ {N_required:,}")
print(f"  Current N = {N_SAMPLES:,}")
print(f"  {'Sufficient' if N_SAMPLES >= N_required else 'Need more samples'}")

# =============================================================================
# STEP 10: Multiple Output Extension
# =============================================================================

"""
For models with multiple outputs (e.g., cost AND duration AND quality):

def multioutput_model():
    # Returns dictionary or array
    return {
        'cost': ...,
        'duration': ...,
        'quality': ...
    }

# Run simulation
results_dict = {key: [] for key in ['cost', 'duration', 'quality']}
for _ in range(N_SAMPLES):
    outputs = multioutput_model()
    for key, value in outputs.items():
        results_dict[key].append(value)

# Calculate CI for each output
for metric, values in results_dict.items():
    values_array = np.array(values)
    ci_low = np.percentile(values_array, lower_percentile)
    ci_high = np.percentile(values_array, upper_percentile)
    print(f"{metric}: [{ci_low:.2f}, {ci_high:.2f}]")

# Apply Bonferroni correction if testing multiple hypotheses
K = len(results_dict)
bonferroni_alpha = (1 - CONFIDENCE_LEVEL) / K
bonferroni_lower = (bonferroni_alpha / 2) * 100
bonferroni_upper = (1 - bonferroni_alpha / 2) * 100
# Use bonferroni_lower/upper with np.percentile for conservative CIs
"""
```

## Multi-Domain Examples

### Example 1: Manufacturing - Production Capacity Planning

**Problem**: Estimate monthly production capacity with 95% confidence.

**Uncertainty Sources**:
- Machine uptime variability (random breakdowns)
- Worker productivity variation
- Material delivery delays
- Quality rejection rates

**Model Output**: Total units produced per month

**Analysis Approach**:
- N = 10,000 monthly simulations
- Percentile-based CI (distribution right-skewed from breakdowns)
- Key metric: 5th percentile (pessimistic planning scenario)
- Decision: Size inventory buffer to cover gap between mean and 5th percentile

**Expected Results**:
- Mean production: 10,000 units
- 95% CI: [8,200, 11,500]
- 5th percentile: 8,200 units (plan buffer for 1,800 units)

### Example 2: Finance - Portfolio Return Forecasting

**Problem**: Estimate 1-year portfolio return with 90% confidence.

**Uncertainty Sources**:
- Asset return distributions (fat-tailed)
- Correlation uncertainty
- Trading costs
- Market regime changes

**Model Output**: Portfolio value after 1 year

**Analysis Approach**:
- N = 50,000 price path simulations
- Both percentile and parametric CIs (compare to check normality)
- Focus on downside: 5th percentile (Value at Risk concept)
- Bootstrap CI on Sharpe ratio (derived statistic)

**Expected Results**:
- Mean return: +7.5%
- 90% CI: [-12%, +28%]
- 5th percentile: -12% (VaR threshold)
- Sharpe ratio 95% CI: [0.45, 0.72]

### Example 3: Healthcare - Surgery Duration Estimation

**Problem**: Predict surgery duration for scheduling with 80% confidence.

**Uncertainty Sources**:
- Patient-specific factors (age, comorbidities)
- Surgeon experience variability
- Complication probability
- Equipment availability

**Model Output**: Surgery duration (minutes)

**Analysis Approach**:
- N = 5,000 procedure simulations
- Parametric CI (assume lognormal distribution after log-transform)
- Upper 90th percentile critical for scheduling (avoid overtime)
- Separate CIs by patient risk category

**Expected Results**:
- Median duration: 120 minutes
- 80% CI: [95, 160]
- 90th percentile: 180 minutes (schedule 3-hour blocks)
- High-risk patients: 80% CI [110, 200]

### Example 4: Logistics - Delivery Time Promise

**Problem**: What delivery time can we promise with 99% reliability?

**Uncertainty Sources**:
- Traffic variability
- Weather delays
- Vehicle breakdowns
- Customer unavailability

**Model Output**: Door-to-door delivery time (hours)

**Analysis Approach**:
- N = 20,000 delivery simulations
- Focus on upper tail: 99th percentile
- Separate CIs by route type (urban, rural, highway)
- Time-of-day stratification (rush hour vs. off-peak)

**Expected Results**:
- Median delivery: 3.2 hours
- Mean delivery: 3.5 hours
- 99th percentile: 8.5 hours (promise "within 9 hours")
- 95% CI on 99th percentile: [7.8, 9.2] hours

### Example 5: Environmental Science - Pollutant Concentration

**Problem**: Estimate annual average pollutant concentration with confidence.

**Uncertainty Sources**:
- Emission rate variability
- Meteorological conditions (wind, temperature)
- Measurement error
- Seasonal patterns

**Model Output**: Annual mean concentration (μg/m³)

**Analysis Approach**:
- N = 10,000 annual simulations
- Parametric CI (concentration often lognormal)
- Compliance metric: 95th percentile vs. regulatory threshold
- Bootstrap CI on exceedance probability

**Expected Results**:
- Mean concentration: 35 μg/m³
- 95% CI: [28, 44]
- 95th percentile: 52 μg/m³ (vs. 55 threshold = compliant)
- P(exceed threshold) 95% CI: [2%, 8%]

## Integration Patterns

### Combining with Sensitivity Analysis

1. Run sensitivity analysis first to identify key parameters
2. Focus uncertainty reduction on high-sensitivity parameters
3. Recalculate CIs after improving input precision
4. Quantify CI width reduction per parameter precision improvement

### Combining with Risk Quantification

- Confidence intervals on success probability estimates
- Example: "We estimate 75% success probability (95% CI: [68%, 82%])"
- Helps distinguish "probably successful" from "probably unsuccessful"

### Combining with Distribution Characterization

- CIs on percentiles, not just mean
- Full characterization: CIs on 5th, 25th, 50th, 75th, 95th percentiles
- Captures uncertainty about entire distribution shape

## Common Pitfalls

1. **Confusion: CI vs. Prediction Interval**
   - CI: Uncertainty about mean/statistic (width ~ 1/√N)
   - Prediction Interval: Range for next observation (width ~ constant)

2. **Insufficient Sample Size**
   - Rule of thumb: N ≥ 1000 for 95% CI on median
   - N ≥ 10,000 for extreme percentiles (1st, 99th)

3. **Multiple Comparison Issue**
   - Reporting 20 CIs without correction: expect 1 false coverage
   - Apply Bonferroni or false discovery rate control

4. **Assuming Normality**
   - Parametric CIs invalid for skewed distributions
   - Always check histogram before using parametric methods

5. **Ignoring Autocorrelation**
   - If samples correlated (time series), effective N is smaller
   - Need more samples or use batch means method

## Gap Identification

**Current Limitations**:
- Streaming CIs (update as samples arrive) require manual implementation
- CIs for complex nested structures (confidence region for multivariate) limited
- Adaptive sample size (stop when precision reached) not standardized
- CIs under model misspecification (robust CIs) underdeveloped
- Spatial CIs (confidence bands for spatial fields) require specialized tools
