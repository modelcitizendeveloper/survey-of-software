# Distribution Characterization Pattern

## Pattern Definition

**Generic Use Case**: "Complex system output distribution, need percentiles, probabilities, and distributional properties"

**Core Question**: What does my output distribution look like? Beyond mean/variance, what are tails, skewness, multimodality?

**Parameterization**:
- **N_replications**: Monte Carlo samples needed for accuracy
- **output_dimensionality**: Scalar, vector, or multivariate
- **tail_behavior**: Light-tailed (normal-like) vs. heavy-tailed (extreme values)
- **distribution_goals**: Full characterization vs. specific quantiles
- **goodness_of_fit**: Need to test distributional assumptions?

## Requirements Breakdown

### Functional Requirements

**FR1: Distributional Summaries**
- Must calculate: mean, median, mode, variance, std dev
- Higher moments: skewness, kurtosis
- Percentiles/quantiles at arbitrary levels
- Coefficient of variation, interquartile range

**FR2: Tail Characterization**
- Extreme value statistics (min, max)
- Tail probabilities: P(X > threshold)
- Value at Risk (VaR), Expected Shortfall (ES)
- Outlier detection

**FR3: Distribution Identification**
- Fit parametric distributions (normal, lognormal, Weibull, etc.)
- Goodness-of-fit tests (KS test, Anderson-Darling, Q-Q plots)
- Model selection (AIC, BIC for distribution family)
- Non-parametric density estimation (KDE)

**FR4: Multivariate Extensions**
- Joint distributions for multiple outputs
- Marginal distributions
- Correlation structure, copulas
- Principal components (dimensionality reduction)

### Performance Requirements

**PR1: Sample Size Guidelines**
- Mean/median: N ≥ 1,000 typically sufficient
- 95th percentile: N ≥ 2,000
- 99th percentile (tails): N ≥ 10,000
- 99.9th percentile (rare events): N ≥ 100,000

**PR2: Computational Efficiency**
- Fast percentile computation (sorted arrays, online algorithms)
- Efficient KDE (FFT-based methods for large N)
- Parallel sample generation

### Usability Requirements

**UR1: Visualization**
- Histograms with appropriate binning
- Kernel density plots (smooth distribution)
- Box plots, violin plots
- Q-Q plots for distribution assumption checking
- Empirical CDF plots

**UR2: Interpretation Support**
- Classify distribution shape: symmetric, right-skewed, left-skewed, bimodal
- Compare to common distributions (normal, lognormal, exponential)
- Actionable summaries (e.g., "median wait time 5 min, 95th percentile 18 min")

## Library Fit Analysis

### NumPy (Foundation Tier)

**Fit Score**: ✓ Excellent Fit (Basic Statistics)

**Capabilities**:
- ✓ Moments: mean, std, var (numpy.mean, numpy.std, numpy.var)
- ✓ Percentiles: numpy.percentile, numpy.quantile
- ✓ Min/max: numpy.min, numpy.max
- ○ No built-in skewness/kurtosis (use scipy)
- ✗ No distribution fitting

**Best For**:
- Quick summary statistics
- Percentile calculations
- Foundation for other analyses

**Limitations**:
- No higher moments
- No distribution fitting or GOF tests

### SciPy.stats (Foundation Tier)

**Fit Score**: ✓ Perfect Fit (Comprehensive)

**Capabilities**:
- ✓ Extensive distribution library (90+ continuous, 20+ discrete)
- ✓ Distribution fitting: fit() method
- ✓ Goodness-of-fit: kstest, anderson, shapiro tests
- ✓ Higher moments: skew, kurtosis functions
- ✓ Kernel density estimation: gaussian_kde
- ✓ Parametric and non-parametric methods

**Best For**:
- Identifying best-fit distribution family
- Hypothesis testing for distribution assumptions
- Statistical rigor in distribution characterization

**Limitations**:
- KDE can be slow for very large N (> 1M)
- Some distributions require careful parameter initialization for fitting

### Pandas (Data Tier)

**Fit Score**: ○ Good Fit (Descriptive Statistics)

**Capabilities**:
- ✓ describe(): Comprehensive summary (count, mean, std, percentiles)
- ✓ Easy grouping for stratified analysis
- ✓ Integration with plotting (hist, box, kde)
- ○ Less statistical depth than scipy
- ✓ Excellent for organizing multiple output variables

**Best For**:
- Exploratory data analysis
- Multi-variable output organization
- Quick summary tables
- Reporting and visualization

**Limitations**:
- Not specialized for distribution analysis
- No distribution fitting

### Statsmodels (Statistical Models Tier)

**Fit Score**: ○ Good Fit (Statistical Testing)

**Capabilities**:
- ✓ Q-Q plots: qqplot, qqplot_2samples
- ✓ Probability plots
- ✓ Additional GOF tests
- ○ Focus on regression/time series, not general MC
- ✓ Excellent diagnostic plots

**Best For**:
- Visual distribution diagnostics
- Hypothesis testing for normality
- Publication-quality Q-Q plots

**Limitations**:
- Not MC-focused (more statistical modeling)

### Seaborn (Visualization Tier)

**Fit Score**: ✓ Excellent Fit (Visualization)

**Capabilities**:
- ✓ Beautiful distribution plots: histplot, kdeplot, ecdfplot
- ✓ Violin plots, box plots with aesthetic appeal
- ✓ Joint distributions (jointplot) for multivariate
- ✓ Easy faceting for stratified distributions
- ○ Visualization-only (no statistical tests)

**Best For**:
- Publication-quality distribution visualizations
- Exploring multivariate distributions
- Communicating results to non-technical audiences

**Limitations**:
- No statistical inference (pair with scipy)

### Distfit (Specialized Tier)

**Fit Score**: ○ Good Fit (Automated Fitting)

**Capabilities**:
- ✓ Automated distribution selection (tests multiple families)
- ✓ Ranks distributions by GOF
- ✓ Visualization of fitted distribution
- ○ Smaller community, less maintained
- ○ Overlaps with scipy functionality

**Best For**:
- Automated distribution identification
- When you want to test many distributions quickly

**Limitations**:
- Less flexible than scipy.stats
- Potentially overkill for standard distributions

## Recommendation by Use Case

### Quick Summary Statistics

**Recommended**: NumPy + Pandas
```python
import pandas as pd
import numpy as np

df = pd.DataFrame({'output': results})
summary = df.describe()  # Count, mean, std, percentiles
skew = results.skew()
kurt = results.kurt()
```

**Why**: Fast, simple, built-in.

### Identify Best-Fit Distribution

**Recommended**: SciPy.stats
```python
from scipy import stats

# Try multiple distributions
distributions = [stats.norm, stats.lognorm, stats.gamma, stats.weibull_min]
best_fit = None
best_aic = np.inf

for dist in distributions:
    params = dist.fit(results)
    # Calculate AIC
    log_likelihood = np.sum(dist.logpdf(results, *params))
    k = len(params)
    aic = 2*k - 2*log_likelihood

    if aic < best_aic:
        best_aic = aic
        best_fit = (dist, params)

print(f"Best fit: {best_fit[0].name}")
```

**Why**: Rigorous statistical fitting.

### Visualize Distribution

**Recommended**: Seaborn
```python
import seaborn as sns
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Histogram + KDE
sns.histplot(results, kde=True, ax=axes[0])

# Box plot
sns.boxplot(y=results, ax=axes[1])

# Empirical CDF
sns.ecdfplot(results, ax=axes[2])
```

**Why**: Beautiful, publication-ready plots.

### Test Normality Assumption

**Recommended**: SciPy + Statsmodels (Q-Q plot)
```python
from scipy import stats
import statsmodels.api as sm

# Statistical test
stat, pval = stats.shapiro(results)  # Shapiro-Wilk test
print(f"Normality test p-value: {pval:.4f}")

# Visual check
sm.qqplot(results, line='45')
plt.title('Q-Q Plot vs. Normal')
```

**Why**: Rigorous test + visual confirmation.

### Characterize Tails (Risk Analysis)

**Recommended**: NumPy percentiles + Custom metrics
```python
# Tail statistics
var_95 = np.percentile(results, 95)  # Value at Risk
tail_values = results[results >= var_95]
cvar_95 = tail_values.mean()  # Conditional VaR (Expected Shortfall)

# Tail ratio (heavy-tailed indicator)
q75 = np.percentile(results, 75)
q25 = np.percentile(results, 25)
q95 = np.percentile(results, 95)
q5 = np.percentile(results, 5)
tail_ratio = (q95 - q5) / (q75 - q25)  # >2.9 suggests heavy tails
```

**Why**: Domain-specific risk metrics.

### Multivariate Distribution

**Recommended**: Seaborn jointplot + NumPy correlation
```python
import seaborn as sns

# Joint distribution
sns.jointplot(x=output1, y=output2, kind='kde')

# Correlation matrix
corr_matrix = np.corrcoef([output1, output2, output3])
```

**Why**: Visualize relationships, quantify dependence.

## Generic Code Template

```python
"""
GENERIC DISTRIBUTION CHARACTERIZATION TEMPLATE

Comprehensive analysis of Monte Carlo output distributions.
"""

import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =============================================================================
# STEP 1: Collect Monte Carlo Results (USER PROVIDES)
# =============================================================================

# EXAMPLE: Load or generate MC results (replace with your data)
np.random.seed(42)
N_SAMPLES = 10000

# Simulate results (replace with actual MC output)
# Example: Right-skewed distribution (lognormal)
results = np.random.lognormal(mean=3.0, sigma=0.5, size=N_SAMPLES)

print(f"Analyzing {len(results)} Monte Carlo samples")

# =============================================================================
# STEP 2: Basic Summary Statistics (REUSABLE PATTERN)
# =============================================================================

# Central tendency
mean_val = np.mean(results)
median_val = np.median(results)
mode_val = stats.mode(results, keepdims=True).mode[0]  # Most common value (binned)

# Dispersion
std_val = np.std(results, ddof=1)  # Sample std dev
var_val = np.var(results, ddof=1)
cv_val = std_val / mean_val  # Coefficient of variation
iqr_val = stats.iqr(results)  # Interquartile range

# Shape
skew_val = stats.skew(results)
kurt_val = stats.kurtosis(results)  # Excess kurtosis

# Range
min_val = np.min(results)
max_val = np.max(results)
range_val = max_val - min_val

print("\nBASIC SUMMARY STATISTICS")
print("=" * 70)
print(f"{'Statistic':<25} {'Value':<15}")
print("-" * 70)
print(f"{'Sample Size':<25} {len(results):<15}")
print(f"{'Mean':<25} {mean_val:<15.3f}")
print(f"{'Median':<25} {median_val:<15.3f}")
print(f"{'Std Dev':<25} {std_val:<15.3f}")
print(f"{'Coefficient of Variation':<25} {cv_val:<15.2%}")
print(f"{'Interquartile Range':<25} {iqr_val:<15.3f}")
print(f"{'Min':<25} {min_val:<15.3f}")
print(f"{'Max':<25} {max_val:<15.3f}")
print(f"{'Range':<25} {range_val:<15.3f}")
print(f"{'Skewness':<25} {skew_val:<15.3f}")
print(f"{'Kurtosis (excess)':<25} {kurt_val:<15.3f}")

# Interpret shape
if abs(skew_val) < 0.5:
    skew_interp = "Approximately symmetric"
elif skew_val > 0.5:
    skew_interp = "Right-skewed (tail extends right)"
else:
    skew_interp = "Left-skewed (tail extends left)"

if abs(kurt_val) < 0.5:
    kurt_interp = "Normal-like tails"
elif kurt_val > 0.5:
    kurt_interp = "Heavy tails (more outliers than normal)"
else:
    kurt_interp = "Light tails (fewer outliers than normal)"

print(f"\nDISTRIBUTION SHAPE:")
print(f"  Skewness: {skew_interp}")
print(f"  Kurtosis: {kurt_interp}")

# =============================================================================
# STEP 3: Percentile Analysis (REUSABLE PATTERN)
# =============================================================================

percentiles = [1, 5, 10, 25, 50, 75, 90, 95, 99]
percentile_values = np.percentile(results, percentiles)

print(f"\nPERCENTILE ANALYSIS:")
print("-" * 40)
print(f"{'Percentile':<15} {'Value':<15}")
print("-" * 40)
for p, v in zip(percentiles, percentile_values):
    print(f"{p}th{' '*(12-len(str(p)))} {v:<15.3f}")

# Common intervals
p90_range = (np.percentile(results, 5), np.percentile(results, 95))
p80_range = (np.percentile(results, 10), np.percentile(results, 90))
p50_range = (np.percentile(results, 25), np.percentile(results, 75))

print(f"\nCOMMON INTERVALS:")
print(f"  50% of values in: [{p50_range[0]:.2f}, {p50_range[1]:.2f}]")
print(f"  80% of values in: [{p80_range[0]:.2f}, {p80_range[1]:.2f}]")
print(f"  90% of values in: [{p90_range[0]:.2f}, {p90_range[1]:.2f}]")

# =============================================================================
# STEP 4: Distribution Fitting (REUSABLE PATTERN)
# =============================================================================

# Test multiple distribution families
distributions_to_test = {
    'Normal': stats.norm,
    'Lognormal': stats.lognorm,
    'Gamma': stats.gamma,
    'Weibull': stats.weibull_min,
    'Exponential': stats.expon,
}

print(f"\nDISTRIBUTION FITTING:")
print("=" * 70)
print(f"{'Distribution':<15} {'KS Statistic':<15} {'p-value':<15} {'AIC':<15}")
print("-" * 70)

fit_results = {}
for name, dist in distributions_to_test.items():
    # Fit distribution
    params = dist.fit(results)

    # Goodness of fit (Kolmogorov-Smirnov test)
    ks_stat, ks_pval = stats.kstest(results, lambda x: dist.cdf(x, *params))

    # Calculate AIC (lower is better)
    log_likelihood = np.sum(dist.logpdf(results, *params))
    k = len(params)  # Number of parameters
    aic = 2*k - 2*log_likelihood

    fit_results[name] = {
        'params': params,
        'ks_stat': ks_stat,
        'ks_pval': ks_pval,
        'aic': aic,
        'dist': dist
    }

    print(f"{name:<15} {ks_stat:<15.4f} {ks_pval:<15.4f} {aic:<15.1f}")

# Identify best fit (lowest AIC)
best_fit_name = min(fit_results, key=lambda k: fit_results[k]['aic'])
best_fit = fit_results[best_fit_name]

print(f"\nBest fit (by AIC): {best_fit_name}")
print(f"  AIC: {best_fit['aic']:.1f}")
print(f"  KS p-value: {best_fit['ks_pval']:.4f}")
print(f"  {'Cannot reject' if best_fit['ks_pval'] > 0.05 else 'Reject'} null hypothesis (α=0.05)")

# =============================================================================
# STEP 5: Tail Characterization (REUSABLE PATTERN)
# =============================================================================

# Value at Risk (VaR) - common risk metric
var_95 = np.percentile(results, 95)
var_99 = np.percentile(results, 99)

# Conditional Value at Risk (CVaR / Expected Shortfall)
tail_95 = results[results >= var_95]
cvar_95 = tail_95.mean()

tail_99 = results[results >= var_99]
cvar_99 = tail_99.mean()

# Tail ratio (indicator of tail heaviness)
q75 = np.percentile(results, 75)
q25 = np.percentile(results, 25)
q95 = np.percentile(results, 95)
q5 = np.percentile(results, 5)
tail_ratio = (q95 - q5) / (q75 - q25)

print(f"\nTAIL ANALYSIS:")
print("-" * 50)
print(f"VaR 95% (95th percentile): {var_95:.3f}")
print(f"CVaR 95% (expected value above VaR): {cvar_95:.3f}")
print(f"VaR 99% (99th percentile): {var_99:.3f}")
print(f"CVaR 99% (expected value above VaR): {cvar_99:.3f}")
print(f"\nTail Ratio: {tail_ratio:.2f}")
print(f"  (Normal≈2.91, Heavy-tailed>3.0, Light-tailed<2.8)")

if tail_ratio > 3.0:
    tail_interp = "Heavy tails - expect more extreme values than normal"
elif tail_ratio < 2.8:
    tail_interp = "Light tails - fewer extreme values than normal"
else:
    tail_interp = "Normal-like tails"

print(f"  Interpretation: {tail_interp}")

# =============================================================================
# STEP 6: Outlier Detection (REUSABLE PATTERN)
# =============================================================================

# IQR method for outliers
q1 = np.percentile(results, 25)
q3 = np.percentile(results, 75)
iqr = q3 - q1

lower_fence = q1 - 1.5 * iqr
upper_fence = q3 + 1.5 * iqr

outliers_low = results[results < lower_fence]
outliers_high = results[results > upper_fence]
outliers_total = len(outliers_low) + len(outliers_high)

print(f"\nOUTLIER DETECTION (IQR method):")
print(f"  Lower fence: {lower_fence:.3f}")
print(f"  Upper fence: {upper_fence:.3f}")
print(f"  Outliers below: {len(outliers_low)} ({len(outliers_low)/len(results)*100:.1f}%)")
print(f"  Outliers above: {len(outliers_high)} ({len(outliers_high)/len(results)*100:.1f}%)")
print(f"  Total outliers: {outliers_total} ({outliers_total/len(results)*100:.1f}%)")

# =============================================================================
# STEP 7: Visualizations (REUSABLE PATTERN)
# =============================================================================

fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Plot 1: Histogram + KDE + Fitted distribution
ax1 = fig.add_subplot(gs[0, :2])
ax1.hist(results, bins=50, density=True, alpha=0.6, color='steelblue',
         edgecolor='black', label='Empirical')

# KDE
kde = stats.gaussian_kde(results)
x_plot = np.linspace(results.min(), results.max(), 200)
ax1.plot(x_plot, kde(x_plot), 'r-', linewidth=2, label='KDE')

# Best fit distribution
best_dist = fit_results[best_fit_name]['dist']
best_params = fit_results[best_fit_name]['params']
ax1.plot(x_plot, best_dist.pdf(x_plot, *best_params), 'g--',
         linewidth=2, label=f'Fitted {best_fit_name}')

ax1.axvline(mean_val, color='orange', linestyle='--', linewidth=2, label='Mean')
ax1.axvline(median_val, color='purple', linestyle='--', linewidth=2, label='Median')
ax1.set_xlabel('Value')
ax1.set_ylabel('Probability Density')
ax1.set_title('Distribution: Histogram, KDE, and Fitted Model')
ax1.legend()
ax1.grid(alpha=0.3)

# Plot 2: Box plot
ax2 = fig.add_subplot(gs[0, 2])
bp = ax2.boxplot(results, vert=True, widths=0.5, patch_artist=True)
bp['boxes'][0].set_facecolor('lightblue')
ax2.set_ylabel('Value')
ax2.set_title('Box Plot')
ax2.grid(axis='y', alpha=0.3)

# Plot 3: Empirical CDF
ax3 = fig.add_subplot(gs[1, 0])
sorted_results = np.sort(results)
cumulative = np.arange(1, len(sorted_results)+1) / len(sorted_results)
ax3.plot(sorted_results, cumulative, linewidth=2, color='navy')
ax3.set_xlabel('Value')
ax3.set_ylabel('Cumulative Probability')
ax3.set_title('Empirical CDF')
ax3.grid(alpha=0.3)

# Plot 4: Q-Q plot vs Normal
ax4 = fig.add_subplot(gs[1, 1])
stats.probplot(results, dist='norm', plot=ax4)
ax4.set_title('Q-Q Plot vs. Normal Distribution')
ax4.grid(alpha=0.3)

# Plot 5: Q-Q plot vs Best Fit
ax5 = fig.add_subplot(gs[1, 2])
stats.probplot(results, dist=best_dist, sparams=best_params[:-2], plot=ax5)
ax5.set_title(f'Q-Q Plot vs. {best_fit_name}')
ax5.grid(alpha=0.3)

# Plot 6: Percentile comparison
ax6 = fig.add_subplot(gs[2, :])
ax6.bar(range(len(percentiles)), percentile_values, alpha=0.7, color='coral')
ax6.set_xticks(range(len(percentiles)))
ax6.set_xticklabels([f'{p}th' for p in percentiles])
ax6.set_xlabel('Percentile')
ax6.set_ylabel('Value')
ax6.set_title('Percentile Values')
ax6.grid(axis='y', alpha=0.3)

# Add horizontal lines for key percentiles
ax6.axhline(median_val, color='red', linestyle='--', linewidth=1.5,
           alpha=0.7, label='Median')
ax6.axhline(mean_val, color='orange', linestyle='--', linewidth=1.5,
           alpha=0.7, label='Mean')
ax6.legend()

plt.savefig('distribution_characterization.png', dpi=300, bbox_inches='tight')
print("\nVisualization saved to 'distribution_characterization.png'")

# =============================================================================
# STEP 8: Probability Queries (REUSABLE PATTERN)
# =============================================================================

# Answer practical questions
threshold = median_val * 1.5  # Example threshold

prob_exceed = np.mean(results > threshold)
prob_below = np.mean(results < threshold)

print(f"\nPROBABILITY QUERIES:")
print(f"  P(X > {threshold:.2f}): {prob_exceed:.2%}")
print(f"  P(X ≤ {threshold:.2f}): {prob_below:.2%}")

# Inverse query: What value has 80% probability of not being exceeded?
value_80 = np.percentile(results, 80)
print(f"  80% of values are ≤ {value_80:.2f}")

# =============================================================================
# STEP 9: Pandas Summary (OPTIONAL - Alternative Format)
# =============================================================================

df = pd.DataFrame({'output': results})
pandas_summary = df.describe(percentiles=[.01, .05, .10, .25, .50, .75, .90, .95, .99])

print(f"\nPANDAS SUMMARY:")
print(pandas_summary)

# =============================================================================
# STEP 10: Multivariate Extension (If Multiple Outputs)
# =============================================================================

"""
For models with multiple outputs:

results_dict = {
    'output1': results1,
    'output2': results2,
    'output3': results3
}

df_multi = pd.DataFrame(results_dict)

# Summary statistics for all
print(df_multi.describe())

# Correlation matrix
corr_matrix = df_multi.corr()
print("\\nCorrelation Matrix:")
print(corr_matrix)

# Joint distribution visualization
import seaborn as sns
sns.pairplot(df_multi)
plt.savefig('multivariate_distribution.png')

# Marginal distributions
for col in df_multi.columns:
    plt.figure()
    sns.histplot(df_multi[col], kde=True)
    plt.title(f'Distribution of {col}')
    plt.savefig(f'distribution_{col}.png')
    plt.close()
"""
```

## Multi-Domain Examples

### Example 1: Manufacturing - Product Lifetime

**Problem**: Characterize product lifetime distribution for warranty planning.

**MC Output**: Time to failure (hours) for 10,000 simulated products

**Analysis**:
- Fit Weibull distribution (standard for lifetime data)
- Key metrics: Median lifetime, 10th percentile (early failures), 90th percentile
- Shape parameter β: <1 (infant mortality), =1 (random), >1 (wear-out)
- Warranty decision: Cover 95th percentile = 8,000 hours

**Result**: Weibull(β=2.3, η=5000) fits well; 95% survive 8,200 hours.

### Example 2: Finance - Portfolio Returns

**Problem**: Characterize annual return distribution for investor communication.

**MC Output**: 1-year returns (%) for 50,000 market scenarios

**Analysis**:
- Test normality (often rejected - fat tails)
- Fit Student-t distribution (heavier tails than normal)
- Key metrics: VaR 95% (-12%), CVaR 95% (-18%), Sharpe ratio
- Asymmetry: Downside deviation larger than upside
- Communication: "Median return 7.5%, 90% range [-10%, +26%]"

**Result**: Student-t(df=5) better than normal; significant left skew.

### Example 3: Healthcare - ER Wait Times

**Problem**: Characterize patient wait time distribution for performance reporting.

**MC Output**: Wait times (minutes) for 20,000 simulated patient arrivals

**Analysis**:
- Fit Lognormal (right-skewed, bounded below by 0)
- Key metrics: Median (clinical experience), 95th percentile (worst-case planning)
- Stratify by acuity: Minor vs. major cases have different distributions
- Target: 90% of patients seen within 60 minutes

**Result**: Lognormal fits well; median 12 min, 95th percentile 58 min (meets target).

### Example 4: Climate - Precipitation Extremes

**Problem**: Characterize extreme precipitation events for flood risk.

**MC Output**: Annual maximum daily rainfall (mm) for 10,000 simulated years

**Analysis**:
- Fit Generalized Extreme Value (GEV) distribution
- Focus on upper tail: 99th, 99.9th percentiles
- 100-year event: 99th percentile ≈ 150mm
- Shape parameter ξ: Heavy tail (ξ>0) implies extreme events more likely
- Compare historical vs. future climate scenarios

**Result**: GEV(ξ=0.15) indicates heavy tail; 100-year event: 165mm.

### Example 5: Logistics - Delivery Cost

**Problem**: Characterize total delivery cost distribution for budgeting.

**MC Output**: Monthly delivery costs ($) for 5,000 simulated months

**Analysis**:
- Test multiple distributions: Normal, Lognormal, Gamma
- Bimodal detection: Mixture of low-volume and high-volume months
- Key metrics: Mean (budget baseline), 80th percentile (buffer), max (worst-case)
- Seasonality check: Separate distributions for peak vs. off-peak

**Result**: Mixture of two normals fits best; mean $125k, 90th percentile $148k.

## Integration Patterns

### Combining with Sensitivity Analysis

1. Characterize output distribution
2. Run sensitivity analysis to identify key input drivers
3. Decompose output distribution shape: Which inputs cause skewness? Heavy tails?

### Combining with Risk Quantification

1. Characterize distribution to understand full risk profile
2. Set risk thresholds based on percentiles (e.g., VaR 95%)
3. Evaluate decision alternatives on distributional differences (not just means)

### Combining with Confidence Intervals

1. Distribution characterization provides point estimates of percentiles
2. Confidence intervals quantify uncertainty in those percentiles
3. Example: "95th percentile is 120 (95% CI: [115, 127])"

## Common Pitfalls

1. **Assuming Normality**: Many real distributions are skewed, heavy-tailed, or multimodal
2. **Insufficient Sample Size**: Tails require large N (99th percentile needs N ≥ 10,000)
3. **Ignoring Multimodality**: Single distribution fit when mixture is appropriate
4. **Over-interpretation**: Distribution fitting is descriptive, not causal
5. **Outlier Removal**: Removing "outliers" without justification biases tail estimates

## Gap Identification

**Current Limitations**:
- Mixture distribution fitting (automated component selection) requires manual iteration
- Time-varying distributions (non-stationarity) need specialized time series tools
- Copula estimation for multivariate distributions (beyond correlation) requires specialized libraries
- Distribution goodness-of-fit for small samples (N < 100) has low power
- Functional data (distribution over time/space) requires specialized methods (FDA)
- Extreme value theory (block maxima, peaks-over-threshold) requires careful application beyond standard libraries
