# Library Analysis: OpenTURNS

## Overview

**Package:** openturns
**Current Version:** 1.25+
**Maintenance:** Very active (industrial consortium: EDF, Airbus, Phimeca, IMACS)
**License:** LGPL
**Primary Use Case:** Industrial-strength uncertainty quantification (comprehensive suite)
**Website:** https://openturns.org
**GitHub:** https://github.com/openturns/openturns

## Core Philosophy

OpenTURNS (Open source Treatment of Uncertainty, Risk 'N Statistics) is a comprehensive,
industrial-grade library for uncertainty quantification. Developed by major engineering
companies (EDF R&D, Airbus), it provides a complete UQ workflow: sampling, uncertainty
propagation, sensitivity analysis, metamodeling, reliability analysis, and stochastic
processes. It is designed for regulatory-compliant engineering applications where
robustness and completeness are paramount.

## Core Capabilities

### Comprehensive UQ Workflow

**Full Coverage:**
1. **Uncertainty Modeling:** Distributions, copulas, dependencies
2. **Sampling:** Monte Carlo, quasi-MC, LHS, experimental designs
3. **Uncertainty Propagation:** Forward simulation, Taylor expansion
4. **Sensitivity Analysis:** Sobol, FAST, Morris, correlation-based
5. **Metamodeling:** Polynomial chaos, Kriging, neural networks
6. **Reliability Analysis:** FORM/SORM, importance sampling, subset simulation
7. **Stochastic Processes:** Gaussian processes, time series

**This Comprehensiveness is Unique:**
- Most libraries focus on 1-2 areas (e.g., SALib = sensitivity only)
- OpenTURNS provides end-to-end UQ pipeline in single package

### Distribution and Copula Library

**Distributions:**
- 100+ univariate distributions (all standard + many specialized)
- Multivariate distributions (normal, Student-t, etc.)
- Custom distributions via Python interface

**Copulas (Advanced Dependency Modeling):**
```python
import openturns as ot

# Marginal distributions
margin1 = ot.Normal(5, 2)
margin2 = ot.Lognormal(1, 0.5)
margin3 = ot.Uniform(0, 10)

# Copula (dependency structure)
copula = ot.NormalCopula(3)  # Gaussian copula
# Or: GumbelCopula, ClaytonCopula, FrankCopula, etc.

# Correlation matrix
correlation = ot.CorrelationMatrix(3)
correlation[0, 1] = 0.5
correlation[0, 2] = 0.3
correlation[1, 2] = 0.2
copula.setParameter(correlation)

# Composed distribution (Sklar's theorem)
distribution = ot.ComposedDistribution([margin1, margin2, margin3], copula)

# Sample
samples = distribution.getSample(1000)
```

**Key Advantage:**
- Explicit copula modeling separates marginals from dependence
- More flexible than multivariate normal assumption
- Critical for complex engineering systems

### Sampling Methods

**Monte Carlo:**
```python
import openturns as ot

# Define distribution
dist = ot.Normal(5, 2)

# Simple Monte Carlo
samples = dist.getSample(10000)

# Low-discrepancy sequences
sobol_exp = ot.SobolSequence(3)
lhs_exp = ot.LHSExperiment(dist, 1000)
lhs_exp.setAlwaysShuffle(True)
lhs_samples = lhs_exp.generate()

# Quasi-Monte Carlo
qmc_exp = ot.LowDiscrepancyExperiment(ot.SobolSequence(), dist, 1024)
qmc_samples = qmc_exp.generate()
```

**Experimental Designs:**
- Factorial designs
- Central composite designs
- Box-Behnken designs
- Optimal designs (D-optimal, A-optimal)

### Sensitivity Analysis

**Methods Available:**
1. **Sobol Indices:** Variance-based (Saltelli, Jansen, Martinez)
2. **FAST:** Fourier amplitude sensitivity test
3. **Morris:** Screening method
4. **Correlation-Based:** SRC, SRRC, PCC, PRCC
5. **ANCOVA:** Analysis of variance

**Example (Sobol):**
```python
import openturns as ot

# Define parameter distributions
params = ot.ComposedDistribution([
    ot.Uniform(50, 300),   # num_elevators
    ot.Uniform(1, 10),     # capacity
    ot.Uniform(5, 30)      # speed
])

# Wrap model as OpenTURNS function
def elevator_model_wrapper(x):
    return [elevator_model(x)]  # Return list

model = ot.PythonFunction(3, 1, elevator_model_wrapper)

# Sobol sensitivity analysis
size = 1024  # Base sample size
sie = ot.SobolIndicesExperiment(params, size)
input_design = sie.generate()
output_design = model(input_design)

# Compute indices
sensitivity = ot.SaltelliSensitivityAlgorithm(input_design, output_design, size)
first_order = sensitivity.getFirstOrderIndices()
total_order = sensitivity.getTotalOrderIndices()

print(f"First-order: {first_order}")
print(f"Total-order: {total_order}")
```

### Metamodeling (Surrogate Models)

**Methods:**
1. **Polynomial Chaos Expansion:** Similar to chaospy
2. **Kriging (Gaussian Process):** For expensive, non-polynomial models
3. **Polynomial Regression:** Linear, quadratic, etc.
4. **Functional Chaos:** For functional outputs

**Example (Kriging):**
```python
import openturns as ot

# Training data (expensive model evaluations)
input_train = lhs_exp.generate()
output_train = model(input_train)

# Build Kriging metamodel
basis = ot.ConstantBasisFactory(3).build()
covarianceModel = ot.SquaredExponential([1.0] * 3, [1.0])
algo = ot.KrigingAlgorithm(input_train, output_train, covarianceModel, basis)
algo.run()
kriging_result = algo.getResult()
kriging_metamodel = kriging_result.getMetaModel()

# Fast predictions
input_test = params.getSample(10000)
output_pred = kriging_metamodel(input_test)

# Validation
validation = ot.MetaModelValidation(input_test, model(input_test),
                                     kriging_metamodel)
print(f"Q2: {validation.computePredictivityFactor()}")  # Leave-one-out R²
```

### Reliability Analysis

**Methods:**
- FORM (First-Order Reliability Method)
- SORM (Second-Order Reliability Method)
- Importance Sampling
- Subset Simulation
- Monte Carlo for probability estimation

**Use Case:**
- Estimate probability of failure P(Y > threshold)
- Example: P(wait_time > 60 seconds) < 0.05

```python
import openturns as ot

# Define limit state function: g(x) = 60 - wait_time(x)
# Failure: g(x) < 0
def limit_state(x):
    wait = elevator_model_wrapper(x)[0]
    return [60 - wait]

limit_state_function = ot.PythonFunction(3, 1, limit_state)

# FORM approximation (fast)
event = ot.ThresholdEvent(limit_state_function, ot.Less(), 0.0)
solver = ot.AbdoRackwitz()
algo = ot.FORM(solver, event, params.getMean())
algo.run()
result = algo.getResult()
pf = result.getEventProbability()

print(f"Probability of excessive wait: {pf:.4f}")
```

## Integration Patterns

### With NumPy/SciPy

**Data Conversion:**
```python
import openturns as ot
import numpy as np

# OpenTURNS Sample to NumPy
ot_sample = dist.getSample(1000)
np_array = np.array(ot_sample)

# NumPy to OpenTURNS Sample
np_array = np.random.normal(0, 1, (1000, 3))
ot_sample = ot.Sample(np_array)

# Works with scipy.stats
from scipy.stats import norm
scipy_samples = norm.rvs(size=1000)
ot_sample = ot.Sample([[x] for x in scipy_samples])
```

**Function Wrapping:**
```python
# Wrap NumPy-based model
def numpy_model(x):
    # x: NumPy array
    # ... use NumPy, SciPy, etc. ...
    return result

# Make OpenTURNS-compatible
def ot_model_wrapper(x):
    return [numpy_model(np.array(x))]

ot_model = ot.PythonFunction(3, 1, ot_model_wrapper)
```

### With Pandas

**Data Analysis:**
```python
import pandas as pd
import openturns as ot

# OpenTURNS Sample to DataFrame
ot_sample = dist.getSample(1000)
df = pd.DataFrame(np.array(ot_sample), columns=['x1', 'x2', 'x3'])

# DataFrame to OpenTURNS
ot_sample = ot.Sample(df.values)
```

## Performance Characteristics

### Computational Cost

**C++ Core:**
- OpenTURNS is written in C++ with Python bindings
- Core algorithms (sampling, distributions) are fast (compiled)
- Comparable to SciPy/NumPy for basic operations

**Benchmarks (relative to scipy.stats):**
- Random number generation: Similar speed (both use efficient RNGs)
- Distribution PDF/CDF: Comparable (compiled implementations)
- Sobol sensitivity: Similar to SALib (both use efficient algorithms)

**Metamodeling:**
- Kriging construction: Moderate cost (O(n³) for n training points)
- PCE construction: Fast (similar to chaospy)
- Evaluation: Very fast (surrogates are cheap to evaluate)

### Memory Efficiency

**Data Structures:**
- OpenTURNS uses its own Sample, Point classes (not NumPy arrays natively)
- Conversion overhead between OpenTURNS and NumPy
- Typical memory: Similar to NumPy for same data

## API Quality

### Strengths

1. **Comprehensive:** Everything UQ-related in one package
2. **Industrial-Grade:** Designed for regulatory compliance
3. **Well-Documented:** Extensive manual, examples, theory guides
4. **Validated:** Benchmarked against commercial UQ software

### Learning Curve

**Steep:**
- Large API surface (100s of classes)
- Different conventions from SciPy/NumPy (Sample vs. array, etc.)
- Requires understanding of UQ theory (metamodeling, reliability, etc.)

**Example Complexity:**
```python
# Simple task: Sample from normal distribution
# SciPy (2 lines):
from scipy.stats import norm
samples = norm.rvs(size=1000)

# OpenTURNS (4 lines, different syntax):
import openturns as ot
dist = ot.Normal(0, 1)
sample = dist.getSample(1000)
np_array = np.array(sample)  # Convert for compatibility
```

### Documentation

**Excellent:**
- Comprehensive user manual (~1000 pages)
- Theory guide (mathematical background)
- 100+ examples
- API reference for all classes

**But:**
- Can be overwhelming for beginners
- Assumes familiarity with UQ terminology

## Limitations

### Non-Pythonic API

**Different Conventions:**
- Uses own data structures (Sample, Point, Matrix)
- Method names are verbose (getSample, setParameter)
- Requires frequent conversion to/from NumPy

**Example Friction:**
```python
# Pythonic (NumPy/SciPy):
samples = dist.rvs(size=1000)
mean = np.mean(samples)

# OpenTURNS:
sample = dist.getSample(1000)
mean = sample.computeMean()[0]  # Returns Point, need to index
```

### Heavy Dependencies

**Large Installation:**
- C++ core + Python bindings
- Dependencies: NumPy, SciPy, matplotlib, etc.
- Package size: ~50 MB
- Compilation required for custom builds (pre-built wheels available)

### Overkill for Simple Tasks

**Comprehensive = Complex:**
- For simple Monte Carlo, scipy.stats is simpler
- For sensitivity analysis only, SALib is lighter
- OpenTURNS best when you need multiple UQ capabilities

## Maintenance and Community

### Development Activity

**Very Active:**
- Release cadence: 2-3 releases per year
- Industrial backing (EDF, Airbus, Phimeca, IMACS)
- 50+ contributors
- Issue response: Within days

### Community Health

**Smaller than SciPy, but strong:**
- Discourse forum: Active
- GitHub stars: ~500
- Academic citations: 100+
- Used in engineering: aerospace, nuclear, civil

## Production Readiness

### Reliability

**Industrial-Strength:**
- Extensive test suite
- Validated against commercial software (e.g., ANSYS UQ)
- Used for regulatory submissions (nuclear safety, aerospace certification)

**Numerical Stability:**
- Careful handling of edge cases
- Validated implementations of UQ algorithms
- Continuous benchmarking

### Deployment

**Dependencies:** C++ runtime, Python, NumPy, SciPy, matplotlib
**Package Size:** ~50 MB
**Platform Support:** Linux, macOS, Windows (pre-built wheels)

## Recommendations

### When to Use OpenTURNS

**1. Comprehensive UQ Workflows:**
- Need multiple UQ capabilities (sampling + sensitivity + metamodeling + reliability)
- Want single package for entire workflow
- Prefer industrial-grade, validated implementations

**2. Advanced Dependency Modeling:**
- Need copulas for complex parameter correlations
- Cannot assume multivariate normal
- Example: Tail dependencies in risk assessment

**3. Reliability Analysis:**
- Need to estimate rare event probabilities (P < 0.01)
- FORM/SORM methods for efficiency
- Importance sampling, subset simulation

**4. Metamodeling for Expensive Models:**
- Kriging for non-polynomial responses
- Polynomial chaos for smooth responses
- Adaptive experimental designs

**5. Regulatory Compliance:**
- Need validated, traceable UQ methods
- Documentation requirements for certification
- Example: Aerospace safety analysis

### When NOT to Use OpenTURNS

**1. Simple Monte Carlo:**
- scipy.stats is simpler, more Pythonic
- No need for comprehensive UQ suite
- Example: Basic parameter sensitivity (±20% variations)

**2. Sensitivity Analysis Only:**
- SALib is lighter, easier to learn
- More methods (PAWN, DGSM, etc.)
- Better integration with NumPy/Pandas

**3. Rapid Prototyping:**
- Learning curve is steep
- API friction with NumPy ecosystem
- Better to start with scipy.stats, add OpenTURNS if needed

**4. Error Propagation Only:**
- uncertainties package is simpler
- Automatic differentiation vs. manual sampling
- Much lighter dependency

### Integration Strategy for OR Consulting

**Use OpenTURNS When:**
- Client requires industrial-grade UQ (e.g., aerospace, nuclear)
- Need multiple UQ capabilities (sensitivity + metamodeling + reliability)
- Advanced dependency modeling (copulas) is critical
- Elevator model is very expensive (metamodeling essential)

**Workflow Example:**
```python
import openturns as ot

# 1. Define correlated parameter distributions (copulas)
margins = [ot.Uniform(50, 300), ot.Uniform(1, 10), ot.Uniform(5, 30)]
copula = ot.NormalCopula(ot.CorrelationMatrix(3))
# ... set correlations ...
params = ot.ComposedDistribution(margins, copula)

# 2. Build Kriging metamodel (expensive model)
lhs_exp = ot.LHSExperiment(params, 200)
input_train = lhs_exp.generate()
output_train = expensive_elevator_model(input_train)
kriging = build_kriging(input_train, output_train)

# 3. Sobol sensitivity on metamodel (fast)
sie = ot.SobolIndicesExperiment(params, 1024)
input_design = sie.generate()
output_design = kriging(input_design)
sensitivity = ot.SaltelliSensitivityAlgorithm(input_design, output_design, 1024)

# 4. Reliability analysis
pf = estimate_failure_probability(kriging, params, threshold=60)

# All in one package, validated, traceable
```

**Avoid OpenTURNS When:**
- Simple tasks (use scipy.stats, SALib, uncertainties instead)
- Need rapid iteration (learning curve too steep)
- Pythonic API is priority (OpenTURNS is more Java-like)

### Comparison to Alternatives

| Task                      | Best Tool       | OpenTURNS Alternative?       |
|---------------------------|-----------------|------------------------------|
| Simple MC sampling        | scipy.stats     | No, overkill                 |
| Sensitivity analysis only | SALib           | No, SALib simpler            |
| Error propagation only    | uncertainties   | No, uncertainties easier     |
| Expensive model + UQ      | **OpenTURNS**   | **Yes, Kriging + Sobol**     |
| Copula modeling           | **OpenTURNS**   | **Yes, best option**         |
| Reliability analysis      | **OpenTURNS**   | **Yes, only option**         |
| Polynomial chaos only     | chaospy         | OpenTURNS also good          |

## Summary Assessment

**Strengths:**
- Comprehensive UQ suite (sampling, sensitivity, metamodeling, reliability)
- Industrial-grade, validated implementations
- Advanced features (copulas, Kriging, FORM/SORM)
- Strong industrial backing (EDF, Airbus)
- Excellent documentation (theory + practice)

**Weaknesses:**
- Steep learning curve (large API, UQ theory required)
- Non-Pythonic API (own data structures, verbose methods)
- Overkill for simple tasks
- Heavier dependencies than alternatives

**Verdict for OR Consulting:**
**High Priority for Advanced UQ** - OpenTURNS is the most comprehensive UQ library in Python, offering capabilities unavailable elsewhere (copulas, Kriging, reliability analysis). However, it is overkill for simple Monte Carlo or sensitivity analysis. Use OpenTURNS when clients require industrial-grade UQ, multiple UQ capabilities, or advanced features like copulas or reliability analysis. For simpler tasks, scipy.stats + SALib + uncertainties is more efficient.

**Recommended Role in Toolkit:**
- **Primary:** Comprehensive UQ projects (multiple capabilities needed)
- **Secondary:** Advanced dependency modeling (copulas)
- **Tertiary:** Reliability analysis (rare event probabilities)

**Best Used When:**
1. Client requires traceable, validated UQ methods
2. Need multiple UQ capabilities (not just one)
3. Model is expensive (metamodeling essential)
4. Parameter dependencies are complex (copulas)

**Avoid When:**
- Simple Monte Carlo suffices (use scipy.stats)
- Sensitivity analysis only (use SALib)
- Need rapid prototyping (learning curve too steep)
