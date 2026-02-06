# Model Calibration Pattern

## Pattern Definition

**Generic Use Case**: "Model has unknown parameters, fit to observed data while quantifying parameter uncertainty"

**Core Question**: What parameter values make my model match observed data? How certain am I about those parameters?

**Parameterization**:
- **N_parameters**: Number of unknown parameters to calibrate
- **N_observations**: Amount of data available
- **model_complexity**: Simple (analytic) vs. complex (simulation)
- **observation_noise**: Measurement error in data
- **prior_knowledge**: Strong priors vs. uninformative

## Requirements Breakdown

### Functional Requirements

**FR1: Parameter Estimation**
- Must find parameter values that minimize model-data mismatch
- Handle likelihood functions (Bayesian) or loss functions (frequentist)
- Support constraints on parameters (bounds, physical constraints)

**FR2: Uncertainty Quantification**
- Must provide uncertainty estimates on calibrated parameters
- Posterior distributions (Bayesian) or confidence regions (frequentist)
- Distinguish identifiability: Can all parameters be estimated from data?

**FR3: Prior Integration**
- Incorporate expert knowledge as priors (Bayesian)
- Regularization (frequentist equivalent)
- Informative vs. weakly-informative vs. uniform priors

**FR4: Model Validation**
- Posterior predictive checks: Does calibrated model fit data?
- Out-of-sample validation
- Residual analysis for model adequacy

### Performance Requirements

**PR1: Computational Efficiency**
- Adaptive sampling (focus on high-likelihood regions)
- Parallel evaluation for expensive models
- Gradient-free methods (when model is black-box)

**PR2: Convergence Diagnostics**
- MCMC convergence (Gelman-Rubin, effective sample size)
- Optimization convergence (loss function stabilization)
- Identifiability assessment

### Usability Requirements

**UR1: Prior Specification**
- Easy definition of parameter priors
- Automatic prior sensitivity analysis
- Default weakly-informative priors

**UR2: Output Interpretation**
- Posterior summaries (mean, median, credible intervals)
- Pairwise parameter correlations
- Prediction uncertainty from parameter uncertainty

## Library Fit Analysis

### SciPy.optimize (Foundation Tier)

**Fit Score**: ○ Good Fit (Point Estimates)

**Capabilities**:
- ✓ Parameter optimization (minimize, least_squares)
- ✓ Handles constraints and bounds
- ✓ Multiple algorithms (Nelder-Mead, L-BFGS-B, differential evolution)
- ○ Confidence intervals via Hessian approximation
- ✗ No full uncertainty quantification (point estimates only)

**Best For**:
- Frequentist parameter estimation (MLE, least squares)
- When you only need point estimates + basic CIs
- Fast models where full Bayesian overkill

**Limitations**:
- No posterior distributions
- Confidence intervals assume asymptotic normality
- No prior integration

### PyMC (Bayesian Tier)

**Fit Score**: ✓ Perfect Fit (Bayesian Calibration)

**Capabilities**:
- ✓ Full Bayesian inference (MCMC, NUTS sampler)
- ✓ Flexible prior specification
- ✓ Posterior distributions for parameters
- ✓ Excellent diagnostics (convergence, divergences)
- ✓ Posterior predictive sampling
- ✓ Model comparison (WAIC, LOO)
- ✓ Hierarchical models

**Best For**:
- Bayesian calibration with uncertainty quantification
- Incorporating prior knowledge
- Complex models with multiple parameter levels
- When you need full posterior distributions

**Limitations**:
- Steeper learning curve than optimization
- Slower than point estimation (MCMC sampling)
- Requires understanding of Bayesian concepts

### emcee (MCMC Tier)

**Fit Score**: ✓ Excellent Fit (Affine-Invariant MCMC)

**Capabilities**:
- ✓ Efficient MCMC sampling (ensemble sampler)
- ✓ Good for moderate dimensions (N_parameters < 50)
- ✓ Simple API (just define log-probability)
- ✓ Parallel evaluation
- ○ Manual prior/likelihood specification
- ✗ Less automation than PyMC

**Best For**:
- Bayesian calibration with custom likelihood functions
- When you want control over MCMC details
- Astrophysics, physics applications (where it originated)

**Limitations**:
- Less high-level than PyMC (more manual work)
- No automatic model comparison tools
- Requires tuning for optimal performance

### lmfit (Specialized Tier)

**Fit Score**: ✓ Excellent Fit (Curve Fitting Focus)

**Capabilities**:
- ✓ High-level curve fitting interface
- ✓ Parameter bounds, constraints, expressions
- ✓ Uncertainty estimation via covariance matrix
- ✓ Bootstrap and MCMC options for CI
- ✓ Excellent for 1D/2D curve fitting problems
- ○ Less suited for complex simulation models

**Best For**:
- Fitting standard functions to data (exponentials, Gaussians, etc.)
- Experimental data analysis
- When you want simple syntax for common fitting tasks

**Limitations**:
- Focused on curve fitting (not general simulation calibration)
- Less flexible than PyMC for complex models

### Statsmodels (Statistical Models Tier)

**Fit Score**: ○ Good Fit (Statistical Models)

**Capabilities**:
- ✓ Regression model calibration (GLM, OLS, etc.)
- ✓ Rigorous statistical inference (p-values, CIs)
- ✓ Model diagnostics (residuals, influence, etc.)
- ○ Less suited for custom simulation models
- ✗ Limited to statistical model families

**Best For**:
- Calibrating regression models, time series (ARIMA, etc.)
- When your model is a standard statistical model
- Publication-quality statistical tables

**Limitations**:
- Not designed for arbitrary simulation models
- Assumes specific model structures

## Recommendation by Use Case

### Simple Model, Lots of Data (N_obs >> N_params)

**Recommended**: SciPy.optimize (least squares)
```python
from scipy.optimize import least_squares

def residuals(params, x_data, y_data):
    return model(x_data, params) - y_data

result = least_squares(residuals, initial_params, args=(x_data, y_data))
fitted_params = result.x
```

**Why**: Fast, simple, sufficient when data abundant.

### Moderate Data, Want Full Uncertainty

**Recommended**: PyMC (Bayesian)
```python
import pymc as pm

with pm.Model() as model:
    # Priors
    param1 = pm.Normal('param1', mu=0, sigma=10)
    param2 = pm.Uniform('param2', lower=0, upper=1)

    # Model
    predictions = custom_model(param1, param2, x_data)

    # Likelihood
    pm.Normal('obs', mu=predictions, sigma=obs_noise, observed=y_data)

    # Sample
    trace = pm.sample(2000)
```

**Why**: Full posterior, incorporates priors, rigorous UQ.

### Expensive Model (> 10 sec per evaluation)

**Recommended**: PyMC with surrogate or emcee with careful tuning
- Build surrogate (Gaussian process) from limited model runs
- Calibrate surrogate parameters
- Validate on original model

**Why**: Reduce evaluations from millions (MCMC) to thousands (surrogate fitting).

### Prior Knowledge Available

**Recommended**: PyMC (natural prior specification)
- Use informative priors from literature, expert elicitation
- Regularizes parameter estimates when data sparse

### Custom Likelihood (Non-Standard)

**Recommended**: emcee (flexible log-probability)
```python
import emcee

def log_probability(params, x_data, y_data):
    # Custom likelihood + prior
    lp = log_prior(params)
    if not np.isfinite(lp):
        return -np.inf
    return lp + log_likelihood(params, x_data, y_data)

sampler = emcee.EnsembleSampler(nwalkers, ndim, log_probability, args=(x_data, y_data))
sampler.run_mcmc(initial_positions, nsteps)
```

**Why**: Full control over probability function.

## Generic Code Template

```python
"""
GENERIC MODEL CALIBRATION TEMPLATE

Calibrate model parameters to observed data with uncertainty quantification.
"""

import numpy as np
import pymc as pm
import arviz as az
import matplotlib.pyplot as plt
from scipy import stats

# =============================================================================
# STEP 1: Load or Generate Observed Data (USER PROVIDES DATA)
# =============================================================================

# EXAMPLE DATA (replace with your real observations)
np.random.seed(42)

# True parameters (unknown in real calibration)
TRUE_PARAMS = {'param_a': 2.5, 'param_b': 1.2}

# Generate synthetic observations (replace with real data)
N_OBS = 50
x_observed = np.linspace(0, 10, N_OBS)

# True model with noise
def true_model(x, param_a, param_b):
    return param_a * x + param_b * x**2

y_true = true_model(x_observed, TRUE_PARAMS['param_a'], TRUE_PARAMS['param_b'])
observation_noise = 5.0
y_observed = y_true + np.random.normal(0, observation_noise, size=N_OBS)

print(f"Loaded {N_OBS} observations")
print(f"Data range: x=[{x_observed.min():.2f}, {x_observed.max():.2f}], "
      f"y=[{y_observed.min():.2f}, {y_observed.max():.2f}]")

# =============================================================================
# STEP 2: Define Model to Calibrate (REPLACE WITH YOUR MODEL)
# =============================================================================

def simulation_model(x, param_a, param_b):
    """
    Your simulation or analytical model.

    Args:
        x: Input conditions (array)
        param_a, param_b: Parameters to calibrate

    Returns:
        predictions: Model output (array)
    """
    # EXAMPLE: Quadratic model (replace with your model)
    return param_a * x + param_b * x**2

# =============================================================================
# STEP 3: Specify Prior Knowledge (USER CONFIGURABLE)
# =============================================================================

# Define priors based on:
# 1. Physical constraints (e.g., rate constants > 0)
# 2. Literature values
# 3. Expert judgment
# 4. Weakly informative if no knowledge

PRIORS = {
    'param_a': {
        'distribution': 'normal',
        'mu': 0.0,          # Prior mean (use literature value if known)
        'sigma': 10.0       # Prior std (large = weakly informative)
    },
    'param_b': {
        'distribution': 'normal',
        'mu': 0.0,
        'sigma': 5.0
    },
    'obs_noise': {
        'distribution': 'halfnormal',  # Noise must be positive
        'sigma': 10.0
    }
}

# =============================================================================
# STEP 4: Bayesian Calibration with PyMC (REUSABLE PATTERN)
# =============================================================================

with pm.Model() as calibration_model:

    # Prior distributions
    param_a = pm.Normal('param_a',
                       mu=PRIORS['param_a']['mu'],
                       sigma=PRIORS['param_a']['sigma'])

    param_b = pm.Normal('param_b',
                       mu=PRIORS['param_b']['mu'],
                       sigma=PRIORS['param_b']['sigma'])

    obs_noise = pm.HalfNormal('obs_noise',
                             sigma=PRIORS['obs_noise']['sigma'])

    # Model predictions
    model_predictions = simulation_model(x_observed, param_a, param_b)

    # Likelihood (how well model matches data)
    likelihood = pm.Normal('observations',
                          mu=model_predictions,
                          sigma=obs_noise,
                          observed=y_observed)

    # Sample from posterior
    print("\nRunning MCMC sampling...")
    trace = pm.sample(
        draws=2000,           # Number of posterior samples
        tune=1000,            # Burn-in samples (discarded)
        chains=4,             # Number of independent chains (for convergence check)
        return_inferencedata=True,
        random_seed=42
    )

print("Sampling complete!")

# =============================================================================
# STEP 5: Check Convergence (REUSABLE PATTERN)
# =============================================================================

print("\nCONVERGENCE DIAGNOSTICS:")

# R-hat (should be close to 1.0, ideally < 1.01)
rhat = az.rhat(trace)
print(f"R-hat values (want < 1.01):")
for var in ['param_a', 'param_b', 'obs_noise']:
    print(f"  {var}: {rhat[var].values:.4f}")

# Effective sample size (should be > 400 for reliable inference)
ess = az.ess(trace)
print(f"\nEffective sample size (want > 400):")
for var in ['param_a', 'param_b', 'obs_noise']:
    print(f"  {var}: {ess[var].values:.0f}")

# Check for divergences (should be 0)
divergences = trace.sample_stats.diverging.sum().item()
print(f"\nNumber of divergent transitions: {divergences}")
if divergences > 0:
    print("  Warning: Divergences detected. Model may be misspecified or need reparameterization.")

# =============================================================================
# STEP 6: Analyze Posterior (REUSABLE PATTERN)
# =============================================================================

# Extract posterior samples
posterior = trace.posterior

# Summary statistics
summary = az.summary(trace, var_names=['param_a', 'param_b', 'obs_noise'])

print("\nPOSTERIOR SUMMARY:")
print("=" * 70)
print(summary)

# Get point estimates (posterior means)
param_a_posterior = posterior['param_a'].values.flatten()
param_b_posterior = posterior['param_b'].values.flatten()
obs_noise_posterior = posterior['obs_noise'].values.flatten()

param_a_mean = param_a_posterior.mean()
param_b_mean = param_b_posterior.mean()
obs_noise_mean = obs_noise_posterior.mean()

print(f"\nCalibrated Parameters (Posterior Means):")
print(f"  param_a: {param_a_mean:.3f} (true: {TRUE_PARAMS['param_a']:.3f})")
print(f"  param_b: {param_b_mean:.3f} (true: {TRUE_PARAMS['param_b']:.3f})")
print(f"  obs_noise: {obs_noise_mean:.3f} (true: {observation_noise:.3f})")

# Credible intervals (Bayesian equivalent of confidence intervals)
print(f"\n95% Credible Intervals:")
for var in ['param_a', 'param_b', 'obs_noise']:
    low, high = az.hdi(trace, var_names=[var], hdi_prob=0.95)[var].values
    print(f"  {var}: [{low:.3f}, {high:.3f}]")

# =============================================================================
# STEP 7: Posterior Predictive Check (Model Validation)
# =============================================================================

with calibration_model:
    # Sample from posterior predictive distribution
    posterior_predictive = pm.sample_posterior_predictive(trace, random_seed=42)

# Extract predictions
y_pred_samples = posterior_predictive.posterior_predictive['observations'].values
y_pred_samples = y_pred_samples.reshape(-1, N_OBS)  # Flatten chains

# Calculate prediction intervals
y_pred_mean = y_pred_samples.mean(axis=0)
y_pred_lower = np.percentile(y_pred_samples, 2.5, axis=0)
y_pred_upper = np.percentile(y_pred_samples, 97.5, axis=0)

# Check fit quality
residuals = y_observed - y_pred_mean
rmse = np.sqrt(np.mean(residuals**2))

print(f"\nMODEL FIT QUALITY:")
print(f"  RMSE: {rmse:.3f}")
print(f"  Mean residual: {residuals.mean():.3f}")
print(f"  Std residual: {residuals.std():.3f}")

# Fraction of observations within 95% prediction interval
in_interval = np.sum((y_observed >= y_pred_lower) & (y_observed <= y_pred_upper))
coverage = in_interval / N_OBS

print(f"  95% prediction interval coverage: {coverage:.1%} (expect ~95%)")

# =============================================================================
# STEP 8: Visualize Results (REUSABLE PATTERN)
# =============================================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Data and fitted model
x_plot = np.linspace(x_observed.min(), x_observed.max(), 100)
y_plot_mean = simulation_model(x_plot, param_a_mean, param_b_mean)

# Plot uncertainty band (sample from posterior)
y_plot_samples = []
for i in range(500):
    idx = np.random.randint(len(param_a_posterior))
    y_sample = simulation_model(x_plot, param_a_posterior[idx], param_b_posterior[idx])
    y_plot_samples.append(y_sample)

y_plot_samples = np.array(y_plot_samples)
y_plot_lower = np.percentile(y_plot_samples, 2.5, axis=0)
y_plot_upper = np.percentile(y_plot_samples, 97.5, axis=0)

axes[0, 0].scatter(x_observed, y_observed, alpha=0.5, label='Observed data', s=30)
axes[0, 0].plot(x_plot, y_plot_mean, 'r-', linewidth=2, label='Posterior mean fit')
axes[0, 0].fill_between(x_plot, y_plot_lower, y_plot_upper,
                        alpha=0.3, color='red', label='95% credible band')
axes[0, 0].set_xlabel('x')
axes[0, 0].set_ylabel('y')
axes[0, 0].set_title('Calibrated Model Fit')
axes[0, 0].legend()
axes[0, 0].grid(alpha=0.3)

# Plot 2: Posterior distributions
axes[0, 1].hist(param_a_posterior, bins=50, alpha=0.7, color='blue', density=True, label='param_a')
axes[0, 1].axvline(param_a_mean, color='blue', linestyle='--', linewidth=2, label='Posterior mean')
axes[0, 1].axvline(TRUE_PARAMS['param_a'], color='blue', linestyle=':', linewidth=2, label='True value')
axes[0, 1].set_xlabel('param_a')
axes[0, 1].set_ylabel('Posterior Density')
axes[0, 1].set_title('Posterior Distribution: param_a')
axes[0, 1].legend()
axes[0, 1].grid(alpha=0.3)

# Plot 3: Parameter correlation
axes[1, 0].scatter(param_a_posterior, param_b_posterior, alpha=0.2, s=5)
axes[1, 0].axvline(TRUE_PARAMS['param_a'], color='red', linestyle=':', alpha=0.5)
axes[1, 0].axhline(TRUE_PARAMS['param_b'], color='red', linestyle=':', alpha=0.5)
axes[1, 0].set_xlabel('param_a')
axes[1, 0].set_ylabel('param_b')
axes[1, 0].set_title('Parameter Correlation (Posterior)')
axes[1, 0].grid(alpha=0.3)

corr = np.corrcoef(param_a_posterior, param_b_posterior)[0, 1]
axes[1, 0].text(0.05, 0.95, f'Correlation: {corr:.3f}',
               transform=axes[1, 0].transAxes, verticalalignment='top')

# Plot 4: Residuals
axes[1, 1].scatter(y_pred_mean, residuals, alpha=0.5)
axes[1, 1].axhline(0, color='red', linestyle='--', linewidth=2)
axes[1, 1].set_xlabel('Predicted value')
axes[1, 1].set_ylabel('Residual (observed - predicted)')
axes[1, 1].set_title('Residual Plot')
axes[1, 1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('model_calibration_results.png', dpi=300, bbox_inches='tight')
print("\nVisualization saved to 'model_calibration_results.png'")

# =============================================================================
# STEP 9: Make Predictions with Uncertainty (REUSABLE PATTERN)
# =============================================================================

# New prediction points
x_new = np.array([2.5, 5.0, 7.5])

print(f"\nPREDICTIONS AT NEW POINTS:")
print("-" * 70)

for x_val in x_new:
    # Predict using posterior samples
    predictions = []
    for i in range(len(param_a_posterior)):
        pred = simulation_model(x_val, param_a_posterior[i], param_b_posterior[i])
        predictions.append(pred)

    predictions = np.array(predictions)
    pred_mean = predictions.mean()
    pred_lower, pred_upper = np.percentile(predictions, [2.5, 97.5])

    print(f"x = {x_val:.1f}:")
    print(f"  Prediction: {pred_mean:.2f}")
    print(f"  95% CI: [{pred_lower:.2f}, {pred_upper:.2f}]")

# =============================================================================
# STEP 10: Alternative - Frequentist Calibration (SciPy)
# =============================================================================

"""
For simpler use cases, use frequentist optimization:

from scipy.optimize import curve_fit

# Define model for curve_fit
def model_for_fit(x, param_a, param_b):
    return simulation_model(x, param_a, param_b)

# Fit parameters
fitted_params, param_cov = curve_fit(
    model_for_fit,
    x_observed,
    y_observed,
    p0=[1.0, 1.0]  # Initial guess
)

# Extract results
param_a_fit, param_b_fit = fitted_params
param_a_std, param_b_std = np.sqrt(np.diag(param_cov))

print(f"param_a: {param_a_fit:.3f} ± {param_a_std:.3f}")
print(f"param_b: {param_b_fit:.3f} ± {param_b_std:.3f}")

# Note: This gives point estimates + asymptotic CIs
# Less rigorous than full Bayesian, but faster
"""
```

## Multi-Domain Examples

### Example 1: Epidemiology - Disease Transmission Model

**Problem**: Calibrate SIR model parameters to COVID-19 case data.

**Parameters** (N=3):
- `beta`: Transmission rate (unknown)
- `gamma`: Recovery rate (unknown)
- `R0`: Basic reproduction number (derived = beta/gamma)

**Data**: Daily new cases over 90 days (N_obs=90)

**Analysis**:
- PyMC Bayesian calibration
- Priors: Literature values from similar diseases (informative)
- Likelihood: Poisson (count data)
- Challenge: Reporting delays, testing changes (time-varying bias)

**Result**: beta posterior [0.25, 0.35], gamma [0.08, 0.12], R0 [2.3, 3.8]

### Example 2: Chemical Engineering - Reaction Kinetics

**Problem**: Calibrate Arrhenius parameters for catalytic reaction.

**Parameters** (N=4):
- `A`: Pre-exponential factor (unknown, wide range)
- `Ea`: Activation energy (unknown)
- `k_adsorption`: Adsorption rate constant
- `K_eq`: Equilibrium constant

**Data**: Conversion rate at 20 different temperatures (N_obs=20)

**Analysis**:
- PyMC with log-transformed parameters (physical positivity)
- Hierarchical model: Batch-to-batch catalyst variability
- Informative prior on Ea from quantum chemistry calculations

**Result**: Ea = 85 ± 7 kJ/mol, A = 10^(12.3±0.5) s^-1

### Example 3: Ecology - Population Dynamics

**Problem**: Calibrate Lotka-Volterra predator-prey model.

**Parameters** (N=4):
- `alpha`: Prey growth rate
- `beta`: Predation rate
- `gamma`: Predator efficiency
- `delta`: Predator death rate

**Data**: Monthly predator and prey counts over 10 years (N_obs=120 × 2)

**Analysis**:
- PyMC with multivariate observations
- Observation noise differs for predator vs. prey (count variability)
- Ecological constraints: alpha, delta > 0
- Initial population sizes also uncertain (estimate jointly)

**Result**: Model captures cycles, but residual periodicity suggests missing migration term.

### Example 4: Finance - Stochastic Volatility Model

**Problem**: Calibrate Heston model parameters to options prices.

**Parameters** (N=5):
- `kappa`: Mean reversion speed
- `theta`: Long-term variance
- `sigma_v`: Volatility of volatility
- `rho`: Stock-volatility correlation
- `v0`: Initial variance

**Data**: European call option prices for 50 strikes/maturities (N_obs=50)

**Analysis**:
- emcee MCMC (custom likelihood for options pricing)
- Model evaluation expensive (Monte Carlo path simulation)
- Use surrogate (Gaussian process) for MCMC proposals
- Priors from implied volatility surface

**Result**: Parameters well-identified except sigma_v (weak sensitivity in data).

### Example 5: Hydrology - Rainfall-Runoff Model

**Problem**: Calibrate conceptual hydrological model.

**Parameters** (N=8):
- `field_capacity`: Soil moisture threshold
- `percolation_rate`: Deep drainage
- `base_flow_coefficient`: Groundwater contribution
- `routing_delay`: Channel lag
- 4 more parameters controlling quick flow

**Data**: Daily streamflow measurements for 5 years (N_obs=1826)

**Analysis**:
- PyMC with autocorrelated errors (AR(1) residuals)
- Equifinality problem: Multiple parameter sets fit equally well
- Use regularization: Prefer parameters giving physical water balance
- Split data: Calibrate on 3 years, validate on 2 years

**Result**: Good fit (NSE=0.82) but posterior correlations high (identifiability issues).

## Integration Patterns

### Combining with Sensitivity Analysis

1. Run sensitivity analysis BEFORE calibration (parameter screening)
2. Calibrate only identifiable/sensitive parameters
3. Fix insensitive parameters at nominal values
4. Reduces dimensionality, improves identifiability

### Combining with Uncertainty Propagation

1. Calibrate parameters → posterior distributions
2. Propagate parameter uncertainty through model
3. Get prediction uncertainty (aleatoric + epistemic)
4. Decompose: How much uncertainty from parameters vs. stochasticity?

### Combining with Model Validation

1. Calibrate on training data
2. Posterior predictive check on training data (fit quality)
3. Validate on held-out test data (generalization)
4. If poor test performance → model structural inadequacy

## Common Pitfalls

1. **Overfitting**: Too many parameters for limited data (N_params ≈ N_obs)
2. **Identifiability**: Parameters correlated, cannot distinguish effects
3. **Prior-Data Conflict**: Informative prior contradicts data (check prior predictive)
4. **Ignoring Model Error**: Assuming model perfect, all mismatch is noise
5. **Convergence Failure**: Insufficent MCMC samples or divergences
6. **Local Optima**: Optimization stuck (use global methods or multiple starts)

## Gap Identification

**Current Limitations**:
- Expensive models (hours per evaluation) require surrogate-based calibration (not standardized)
- Time-varying parameters (change over time) require state-space methods (pymc partially supports)
- Model selection + calibration jointly (which model structure best?) requires advanced methods
- Multi-fidelity calibration (calibrate cheap surrogate, then refine with expensive) emerging area
- Robust calibration (outlier-resistant) requires manual implementation
- Calibration under model misspecification (all models wrong, some useful) theoretical gap
