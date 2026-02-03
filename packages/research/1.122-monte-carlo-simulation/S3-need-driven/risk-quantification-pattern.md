# Risk Quantification Pattern

## Pattern Definition

**Generic Use Case**: "Decision between alternatives, quantify probability of meeting goals"

**Core Question**: What is the probability that my system meets performance targets? Which decision alternative has highest success probability?

**Parameterization**:
- **N_alternatives**: Number of decision options to compare
- **success_criteria**: Threshold or goal to achieve
- **risk_tolerance**: Acceptable failure probability
- **N_samples**: Monte Carlo replications per alternative
- **decision_horizon**: Short-term (single period) vs. long-term (multi-period)

## Requirements Breakdown

### Functional Requirements

**FR1: Success Probability Estimation**
- Must calculate P(output ≥ target) or P(output ≤ threshold)
- Handle multiple success criteria (e.g., cost AND time constraints)
- Provide confidence intervals on probability estimates

**FR2: Alternative Comparison**
- Rank alternatives by success probability
- Statistical testing: Are differences significant?
- Handle trade-offs (Alternative A better on metric 1, Alternative B on metric 2)

**FR3: Risk Metrics**
- Probability of failure
- Expected shortfall (average deficit when target missed)
- Value at Risk (VaR): X-percentile loss
- Conditional Value at Risk (CVaR): Expected loss beyond VaR

**FR4: Decision Support**
- Dominance analysis (Alternative A always better than B)
- Pareto frontier (efficient alternatives)
- Expected utility calculation with risk preferences

### Performance Requirements

**PR1: Sample Efficiency**
- Rare event simulation (when P(success) < 1%)
- Importance sampling for tail events
- Variance reduction techniques

**PR2: Multi-Alternative Scaling**
- Efficient when comparing N_alternatives > 10
- Common random numbers for fair comparison
- Parallel evaluation across alternatives

### Usability Requirements

**UR1: Interpretable Output**
- Clear probability statements (avoiding statistical jargon)
- Visual comparisons (bar charts, cumulative distributions)
- Decision recommendations with rationale

**UR2: Sensitivity to Criteria**
- How does success probability change with threshold?
- Trade-off curves (success probability vs. cost)

## Library Fit Analysis

### NumPy/SciPy (Foundation Tier)

**Fit Score**: ✓ Excellent Fit

**Capabilities**:
- ✓ Count success fraction: np.mean(results >= target)
- ✓ Percentile-based VaR: np.percentile(results, 5)
- ✓ Statistical testing: scipy.stats.ttest_ind for comparing alternatives
- ✓ Bootstrap CIs on probabilities: scipy.stats.bootstrap
- ○ No built-in importance sampling
- ✗ No CVaR direct calculation (easy to implement)

**Best For**:
- Straightforward success probability estimation
- Comparing small number of alternatives (N < 10)
- When failure probability > 1% (not rare events)

**Limitations**:
- Rare event simulation inefficient (need importance sampling)
- No decision theory utilities built-in
- Manual implementation of advanced risk metrics

### SciPy.stats (Foundation Tier)

**Fit Score**: ✓ Perfect Fit (Statistical Testing)

**Capabilities**:
- ✓ Hypothesis testing for alternative comparison
- ✓ Distribution fitting for risk assessment
- ✓ Statistical power analysis (sample size for detecting differences)
- ✓ Parametric risk metrics if distribution known

**Best For**:
- Rigorous statistical comparison of alternatives
- When you can assume distribution family (normal, lognormal)
- Combining simulation with analytical methods

**Limitations**:
- Focus on statistical inference, not decision theory
- No multi-criteria decision analysis tools

### Pandas (Data Tier)

**Fit Score**: ○ Good Fit (Organization)

**Capabilities**:
- ✓ Organize simulation results by alternative
- ✓ Group-by analysis for stratified risk metrics
- ✓ Easy calculation of conditional probabilities
- ✓ Integration with visualization (seaborn)

**Best For**:
- Managing results from multiple alternatives/scenarios
- Exploratory analysis and reporting
- When you have many simulation outputs to organize

**Limitations**:
- Not Monte Carlo specific (general data tool)
- Performance overhead for very large N

### Arch (Finance-Specific Tier)

**Fit Score**: ○ Good Fit (Financial Risk)

**Capabilities**:
- ✓ VaR and CVaR calculation
- ✓ Volatility modeling (GARCH)
- ✓ Bootstrap methods for financial risk
- ○ Focused on financial applications
- ✗ Not designed for general decision analysis

**Best For**:
- Financial risk management (portfolio VaR)
- When you need industry-standard risk metrics
- Integration with time series models

**Limitations**:
- Financial domain specificity
- Overkill for simple success probability estimation

### PyMC (Bayesian Tier)

**Fit Score**: ○ Good Fit (Prior Knowledge)

**Capabilities**:
- ✓ Bayesian decision theory
- ✓ Update risk estimates with new data
- ✓ Prior distributions on model parameters
- ○ Steep learning curve
- ✗ Slower than direct Monte Carlo for simple cases

**Best For**:
- When you have prior expert knowledge about risks
- Sequential decision making (update beliefs)
- Small data + strong theory

**Limitations**:
- Complexity overhead for simple risk quantification
- Longer computation time than frequentist MC

## Recommendation by Use Case

### Single Alternative, Single Criterion

**Recommended**: NumPy
```python
success_prob = np.mean(results >= target)
ci = scipy.stats.bootstrap((results >= target,), np.mean, confidence_level=0.95)
```

**Why**: Direct, fast, interpretable.

### Multiple Alternatives (N < 10), Single Criterion

**Recommended**: NumPy + SciPy hypothesis testing
```python
# Calculate success probabilities
probs = {alt: np.mean(results[alt] >= target) for alt in alternatives}

# Test if differences significant
stat, pval = scipy.stats.ttest_ind(results['A'], results['B'])
```

**Why**: Statistical rigor for comparison.

### Multiple Criteria (Cost AND Time AND Quality)

**Recommended**: Pandas + Custom Multi-Criteria Logic
```python
import pandas as pd

df = pd.DataFrame(results)
success = (df['cost'] <= cost_target) & \
          (df['time'] <= time_target) & \
          (df['quality'] >= quality_target)
success_prob = success.mean()
```

**Why**: Clean boolean logic for complex criteria.

### Rare Events (P < 1%)

**Recommended**: Custom Importance Sampling (NumPy/SciPy base)
```python
# Shift distribution to oversample failures
# Then reweight results
```

**Why**: Standard MC requires N >> 1/P samples for rare events.

### Financial Risk Metrics

**Recommended**: NumPy for VaR, Custom for CVaR
```python
VaR_95 = np.percentile(losses, 95)
CVaR_95 = losses[losses >= VaR_95].mean()  # Expected loss beyond VaR
```

**Alternative**: Arch library if doing extensive financial risk.

## Generic Code Template

```python
"""
GENERIC RISK QUANTIFICATION TEMPLATE

Compare decision alternatives and quantify probability of meeting goals.
"""

import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt

# =============================================================================
# STEP 1: Define Decision Problem (USER CONFIGURABLE)
# =============================================================================

# Decision alternatives to compare
ALTERNATIVES = ['Alternative_A', 'Alternative_B', 'Alternative_C']

# Success criteria
SUCCESS_TARGET = 1000  # Target output value to achieve
MAXIMIZE = True        # True if higher is better, False if lower is better

# Risk tolerance
ACCEPTABLE_FAILURE_RATE = 0.10  # 10% failure acceptable

# Simulation parameters
N_SAMPLES = 10000
RANDOM_SEED = 42

# =============================================================================
# STEP 2: Define Models for Each Alternative (REPLACE WITH YOUR MODELS)
# =============================================================================

def model_alternative_A():
    """Model for Alternative A with its specific uncertainties."""
    # EXAMPLE: Higher mean, lower variance (safe choice)
    base_value = np.random.normal(loc=1050, scale=100)
    noise = np.random.normal(loc=0, scale=20)
    return base_value + noise

def model_alternative_B():
    """Model for Alternative B with its specific uncertainties."""
    # EXAMPLE: Lower mean, higher variance (risky choice)
    base_value = np.random.normal(loc=1000, scale=150)
    risk_event = np.random.binomial(n=1, p=0.2)  # 20% chance of boost
    boost = risk_event * np.random.normal(loc=200, scale=50)
    return base_value + boost

def model_alternative_C():
    """Model for Alternative C with its specific uncertainties."""
    # EXAMPLE: Medium mean, medium variance (balanced choice)
    base_value = np.random.lognormal(mean=np.log(1020), sigma=0.12)
    return base_value

# Map alternative names to model functions
ALTERNATIVE_MODELS = {
    'Alternative_A': model_alternative_A,
    'Alternative_B': model_alternative_B,
    'Alternative_C': model_alternative_C
}

# =============================================================================
# STEP 3: Run Monte Carlo for All Alternatives (REUSABLE PATTERN)
# =============================================================================

np.random.seed(RANDOM_SEED)

results = {}
for alt_name, model_func in ALTERNATIVE_MODELS.items():
    print(f"Simulating {alt_name}...")
    results[alt_name] = np.array([model_func() for _ in range(N_SAMPLES)])

print(f"\nCompleted {N_SAMPLES} replications for {len(ALTERNATIVES)} alternatives")

# =============================================================================
# STEP 4: Calculate Risk Metrics (REUSABLE PATTERN)
# =============================================================================

risk_metrics = {}

for alt_name, outcomes in results.items():
    # Success probability
    if MAXIMIZE:
        successes = outcomes >= SUCCESS_TARGET
    else:
        successes = outcomes <= SUCCESS_TARGET

    success_prob = successes.mean()
    failure_prob = 1 - success_prob

    # Confidence interval on success probability (bootstrap)
    bootstrap_result = stats.bootstrap(
        (successes,),
        statistic=np.mean,
        confidence_level=0.95,
        n_resamples=1000
    )
    success_prob_ci = (bootstrap_result.confidence_interval.low,
                       bootstrap_result.confidence_interval.high)

    # Expected shortfall (average deficit when target missed)
    if MAXIMIZE:
        failures = outcomes < SUCCESS_TARGET
        shortfall = SUCCESS_TARGET - outcomes[failures]
    else:
        failures = outcomes > SUCCESS_TARGET
        shortfall = outcomes[failures] - SUCCESS_TARGET

    expected_shortfall = shortfall.mean() if failures.any() else 0.0

    # Value at Risk (VaR) - 5th percentile for downside risk
    if MAXIMIZE:
        VaR_5 = np.percentile(outcomes, 5)  # 5% chance of being below this
    else:
        VaR_5 = np.percentile(outcomes, 95)  # 5% chance of being above this

    # Conditional Value at Risk (CVaR) - expected loss beyond VaR
    if MAXIMIZE:
        tail_losses = outcomes[outcomes <= VaR_5]
    else:
        tail_losses = outcomes[outcomes >= VaR_5]

    CVaR = tail_losses.mean() if len(tail_losses) > 0 else VaR_5

    # Store metrics
    risk_metrics[alt_name] = {
        'mean': outcomes.mean(),
        'median': np.median(outcomes),
        'std': outcomes.std(),
        'success_prob': success_prob,
        'success_prob_ci': success_prob_ci,
        'failure_prob': failure_prob,
        'expected_shortfall': expected_shortfall,
        'VaR_5': VaR_5,
        'CVaR_5': CVaR
    }

# =============================================================================
# STEP 5: Compare Alternatives (REUSABLE PATTERN)
# =============================================================================

print("\nRISK QUANTIFICATION RESULTS")
print("=" * 90)
print(f"Success Target: {'≥' if MAXIMIZE else '≤'} {SUCCESS_TARGET}")
print(f"Acceptable Failure Rate: {ACCEPTABLE_FAILURE_RATE * 100}%")
print()

# Create comparison table
df = pd.DataFrame(risk_metrics).T
df = df.sort_values('success_prob', ascending=False)

print("ALTERNATIVE COMPARISON:")
print("-" * 90)
print(f"{'Alternative':<20} {'Mean':<10} {'Success %':<15} {'Failure %':<15} {'VaR 5%':<10}")
print("-" * 90)
for alt in df.index:
    m = risk_metrics[alt]
    print(f"{alt:<20} {m['mean']:>9.1f} "
          f"{m['success_prob']*100:>7.1f}% "
          f"({m['success_prob_ci'][0]*100:.1f}-{m['success_prob_ci'][1]*100:.1f})%    "
          f"{m['failure_prob']*100:>6.1f}%        "
          f"{m['VaR_5']:>9.1f}")

print()

# Statistical comparison (is best significantly better than second-best?)
best_alt = df.index[0]
second_alt = df.index[1] if len(df) > 1 else None

if second_alt:
    # T-test comparing distributions
    stat, pval = stats.ttest_ind(results[best_alt], results[second_alt])
    print(f"Statistical Comparison: {best_alt} vs {second_alt}")
    print(f"  t-statistic: {stat:.3f}")
    print(f"  p-value: {pval:.4f}")
    print(f"  Conclusion: {'Significantly different' if pval < 0.05 else 'Not significantly different'} (α=0.05)")
    print()

# =============================================================================
# STEP 6: Decision Recommendation (REUSABLE PATTERN)
# =============================================================================

print("DECISION RECOMMENDATION:")
print("-" * 90)

# Check if any alternative meets risk tolerance
acceptable_alternatives = [
    alt for alt, metrics in risk_metrics.items()
    if metrics['failure_prob'] <= ACCEPTABLE_FAILURE_RATE
]

if acceptable_alternatives:
    # Among acceptable, choose highest expected value
    recommended = max(acceptable_alternatives,
                     key=lambda alt: risk_metrics[alt]['mean'])

    print(f"✓ Recommended: {recommended}")
    print(f"  Success Probability: {risk_metrics[recommended]['success_prob']*100:.1f}%")
    print(f"  Expected Value: {risk_metrics[recommended]['mean']:.1f}")
    print(f"  Failure Rate: {risk_metrics[recommended]['failure_prob']*100:.1f}% "
          f"(within {ACCEPTABLE_FAILURE_RATE*100}% tolerance)")

    # Show why rejected others
    for alt in ALTERNATIVES:
        if alt != recommended:
            if alt in acceptable_alternatives:
                print(f"  - {alt}: Also acceptable but lower expected value "
                      f"({risk_metrics[alt]['mean']:.1f})")
            else:
                print(f"  - {alt}: Rejected due to high failure rate "
                      f"({risk_metrics[alt]['failure_prob']*100:.1f}%)")
else:
    # No alternative meets criteria - show least-bad option
    least_risky = min(ALTERNATIVES, key=lambda alt: risk_metrics[alt]['failure_prob'])
    print(f"⚠ Warning: No alternative meets risk tolerance of {ACCEPTABLE_FAILURE_RATE*100}%")
    print(f"  Least risky option: {least_risky}")
    print(f"  Failure Rate: {risk_metrics[least_risky]['failure_prob']*100:.1f}%")
    print(f"  Recommendation: Consider redesign or accept higher risk")

# =============================================================================
# STEP 7: Visualize Risk Profiles (REUSABLE PATTERN)
# =============================================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Distribution comparison
for alt_name, outcomes in results.items():
    axes[0, 0].hist(outcomes, bins=50, alpha=0.5, label=alt_name, density=True)

axes[0, 0].axvline(SUCCESS_TARGET, color='red', linestyle='--', linewidth=2,
                   label=f'Target: {SUCCESS_TARGET}')
axes[0, 0].set_xlabel('Outcome Value')
axes[0, 0].set_ylabel('Probability Density')
axes[0, 0].set_title('Outcome Distributions')
axes[0, 0].legend()
axes[0, 0].grid(alpha=0.3)

# Plot 2: Success probability comparison
success_probs = [risk_metrics[alt]['success_prob'] for alt in ALTERNATIVES]
colors = ['green' if risk_metrics[alt]['failure_prob'] <= ACCEPTABLE_FAILURE_RATE
          else 'orange' for alt in ALTERNATIVES]

axes[0, 1].bar(range(len(ALTERNATIVES)), success_probs, color=colors, alpha=0.7)
axes[0, 1].axhline(1 - ACCEPTABLE_FAILURE_RATE, color='red', linestyle='--',
                   label=f'Min Acceptable ({(1-ACCEPTABLE_FAILURE_RATE)*100}%)')
axes[0, 1].set_xticks(range(len(ALTERNATIVES)))
axes[0, 1].set_xticklabels(ALTERNATIVES, rotation=45, ha='right')
axes[0, 1].set_ylabel('Success Probability')
axes[0, 1].set_title('Success Probability by Alternative')
axes[0, 1].legend()
axes[0, 1].grid(axis='y', alpha=0.3)
axes[0, 1].set_ylim([0, 1])

# Plot 3: Cumulative distribution (for risk curve)
for alt_name, outcomes in results.items():
    sorted_outcomes = np.sort(outcomes)
    cumulative_prob = np.arange(1, len(sorted_outcomes) + 1) / len(sorted_outcomes)
    axes[1, 0].plot(sorted_outcomes, cumulative_prob, label=alt_name, linewidth=2)

axes[1, 0].axvline(SUCCESS_TARGET, color='red', linestyle='--',
                   label=f'Target: {SUCCESS_TARGET}')
axes[1, 0].set_xlabel('Outcome Value')
axes[1, 0].set_ylabel('Cumulative Probability')
axes[1, 0].set_title('Cumulative Distribution Functions')
axes[1, 0].legend()
axes[1, 0].grid(alpha=0.3)

# Plot 4: Risk-Return scatter
means = [risk_metrics[alt]['mean'] for alt in ALTERNATIVES]
stds = [risk_metrics[alt]['std'] for alt in ALTERNATIVES]

axes[1, 1].scatter(stds, means, s=200, alpha=0.6, c=colors)
for i, alt in enumerate(ALTERNATIVES):
    axes[1, 1].annotate(alt, (stds[i], means[i]),
                        xytext=(5, 5), textcoords='offset points')

axes[1, 1].axhline(SUCCESS_TARGET, color='red', linestyle='--', alpha=0.5,
                   label=f'Target: {SUCCESS_TARGET}')
axes[1, 1].set_xlabel('Risk (Standard Deviation)')
axes[1, 1].set_ylabel('Expected Return (Mean)')
axes[1, 1].set_title('Risk-Return Trade-off')
axes[1, 1].legend()
axes[1, 1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('risk_quantification_analysis.png', dpi=300, bbox_inches='tight')
print("\nVisualization saved to 'risk_quantification_analysis.png'")

# =============================================================================
# STEP 8: Sensitivity to Success Criteria (OPTIONAL)
# =============================================================================

"""
How does success probability change with different targets?

targets = np.linspace(900, 1200, 20)
success_curves = {alt: [] for alt in ALTERNATIVES}

for target in targets:
    for alt in ALTERNATIVES:
        if MAXIMIZE:
            success_prob = np.mean(results[alt] >= target)
        else:
            success_prob = np.mean(results[alt] <= target)
        success_curves[alt].append(success_prob)

# Plot trade-off curves
for alt in ALTERNATIVES:
    plt.plot(targets, success_curves[alt], label=alt, linewidth=2)

plt.xlabel('Success Target')
plt.ylabel('Success Probability')
plt.title('Success Probability vs. Target Level')
plt.legend()
plt.grid(alpha=0.3)
"""
```

## Multi-Domain Examples

### Example 1: Manufacturing - Process Selection

**Problem**: Choose between 3 manufacturing processes for new product.

**Alternatives**:
- Process A: Established (low risk, moderate cost)
- Process B: Automated (high risk, low cost if successful)
- Process C: Hybrid (medium risk, medium cost)

**Success Criteria**:
- Unit cost ≤ $50
- Defect rate ≤ 2%
- Throughput ≥ 1000 units/day

**Analysis**:
- N = 10,000 production day simulations per process
- Multi-criteria success: All three criteria must be met
- Risk metric: Probability of meeting all criteria simultaneously
- Trade-off: Process B has 65% success rate but lowest cost when successful

**Decision**: Choose Process A (85% success, acceptable cost) for initial production.

### Example 2: Finance - Investment Strategy

**Problem**: Select portfolio allocation strategy.

**Alternatives**:
- Strategy 1: 60/40 stocks/bonds (conservative)
- Strategy 2: 80/20 stocks/bonds (moderate)
- Strategy 3: 100% stocks (aggressive)

**Success Criteria**:
- 5-year return ≥ 30% (target wealth)
- Maximum drawdown ≤ 20% (downside protection)

**Analysis**:
- N = 50,000 market scenario simulations (5 years each)
- VaR and CVaR calculation for downside risk
- Success probability vs. expected return trade-off
- Scenario analysis: Different market regimes

**Decision**: Strategy 2 (70% success probability, 42% expected return, acceptable VaR).

### Example 3: Healthcare - Treatment Protocol

**Problem**: Choose treatment protocol for patient population.

**Alternatives**:
- Protocol A: Standard care
- Protocol B: Aggressive intervention
- Protocol C: Personalized (risk-stratified)

**Success Criteria**:
- Patient survival rate ≥ 90%
- Adverse event rate ≤ 5%
- Cost per patient ≤ $100,000

**Analysis**:
- N = 20,000 patient cohort simulations
- Stratified analysis by patient risk group
- Multi-criteria: Safety AND efficacy AND cost
- Ethical consideration: Maximize survival probability primary

**Decision**: Protocol C (92% survival, 3% adverse events, but cost variance high).

### Example 4: Infrastructure - Bridge Design

**Problem**: Select structural design for bridge.

**Alternatives**:
- Design A: Steel truss (proven, expensive)
- Design B: Concrete arch (economical, weight limit)
- Design C: Cable-stayed (modern, wind sensitive)

**Success Criteria**:
- 100-year load capacity (safety)
- Construction cost ≤ $50M
- 75-year lifespan without major maintenance

**Analysis**:
- N = 100,000 load scenario simulations (rare events critical)
- Importance sampling for extreme weather/earthquake events
- Failure probability must be < 0.01% (safety critical)
- CVaR on construction cost overruns

**Decision**: Design A (99.998% safety, deterministic cost, proven reliability).

### Example 5: Supply Chain - Supplier Selection

**Problem**: Choose supplier for critical component.

**Alternatives**:
- Supplier 1: Domestic (reliable, expensive)
- Supplier 2: International (cheap, lead time risk)
- Supplier 3: Dual-sourcing (redundant, complex)

**Success Criteria**:
- On-time delivery ≥ 95%
- Cost per unit ≤ $10
- Quality defect rate ≤ 1%

**Analysis**:
- N = 10,000 annual operation simulations
- Geopolitical risk scenarios (tariffs, disruptions)
- Expected shortfall: Cost of stockouts when delivery fails
- Robust decision: Performance across worst-case scenarios

**Decision**: Supplier 3 (88% success, higher cost, but resilient to disruptions).

## Integration Patterns

### Combining with Sensitivity Analysis

1. Identify which input parameters most affect success probability
2. Focus uncertainty reduction efforts on high-sensitivity parameters
3. Recalculate risk after improved measurements
4. Quantify value of information (EVPI)

### Combining with Confidence Intervals

- Report risk metrics with uncertainty: "Success probability 75% (95% CI: [72%, 78%])"
- Decision robustness: Choose alternative whose CI doesn't overlap failure threshold

### Combining with Optimization

- Risk-constrained optimization: Maximize expected return subject to P(success) ≥ 0.9
- Efficient frontier: Pareto-optimal alternatives (no alternative dominates)

## Common Pitfalls

1. **Ignoring Statistical Uncertainty**: Reporting success probability without CI
2. **Sample Size Too Small**: Rare events require N >> 1/P(failure)
3. **Unfair Comparison**: Not using common random numbers across alternatives
4. **Single-Criterion Focus**: Ignoring multi-dimensional trade-offs
5. **Threshold Sensitivity**: Small change in target drastically changes ranking

## Gap Identification

**Current Limitations**:
- Sequential decision making (decision trees with MC at nodes) requires custom framework
- Multi-objective optimization with risk (Pareto frontier generation) manual
- Robust optimization (minimize worst-case regret) not standardized
- Real options (value of flexibility) requires specialized modeling
- Ambiguity aversion (Knightian uncertainty) limited library support
