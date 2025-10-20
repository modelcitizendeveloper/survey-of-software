# Alternative Libraries - Not Recommended for Rapid Development

## Quick Assessment of Other Options

### PyMC

**What**: Probabilistic programming, Bayesian MCMC
**GitHub**: ~8K stars, very popular IN ITS NICHE
**Why skip**:
- Wrong use case (Bayesian inference, not Monte Carlo simulation)
- Heavy learning curve (days to proficiency)
- Overkill for parameter sensitivity
- Specialized for probabilistic modeling
**Verdict**: Use if you need Bayesian inference, not for basic Monte Carlo

### Chaospy

**What**: Polynomial chaos expansion for uncertainty quantification
**GitHub**: Unknown (search didn't provide stars)
**Why skip**:
- Niche method (polynomial chaos vs Monte Carlo)
- Requires deep theoretical understanding
- Less intuitive than direct sampling
- Smaller community than SciPy
**Verdict**: Academic tool, skip for practical work

### pyDOE / pyDOE2

**What**: Design of experiments, Latin Hypercube sampling
**GitHub**: Multiple forks, fragmented community
**Why skip**:
- Original pyDOE is deprecated/unmaintained
- pyDOE2 is a community fork (maintenance uncertainty)
- scipy.stats.qmc now provides same functionality
- Ecosystem is moving to SciPy
**Verdict**: Deprecated. Use scipy.stats.qmc.LatinHypercube instead

### monaco

**What**: Monte Carlo simulation wrapper
**PyPI**: Available but low adoption
**Why skip**:
- Very small user base
- Adds abstraction layer over SciPy
- Not needed if you know NumPy/SciPy
- Minimal advantage over direct use
**Verdict**: Unnecessary abstraction layer

### pandas-montecarlo

**What**: Monte Carlo on Pandas Series
**GitHub**: Low stars, specific use case
**Why skip**:
- Very narrow focus (financial time series)
- Small community
- Can do same with pandas + NumPy directly
- Not general-purpose
**Verdict**: Too specialized

### Uncertainpy

**What**: UQ toolkit for computational neuroscience
**Focus**: Neural models, polynomial chaos
**Why skip**:
- Domain-specific (neuroscience)
- Not general-purpose engineering
- Steep learning curve
- Based on Chaospy (adds another layer)
**Verdict**: Wrong domain, skip

### OpenTURNS

**What**: C++ library with Python bindings for UQ
**Why skip**:
- Heavy dependency (C++ library)
- Complex installation
- Over-engineered for simple Monte Carlo
- Better alternatives in pure Python
**Verdict**: Too heavy

### QMCPy

**What**: Quasi-Monte Carlo in Python
**Why skip**:
- scipy.stats.qmc already exists
- Smaller community than SciPy
- No significant advantage
- Redundant with standard stack
**Verdict**: Use scipy.stats.qmc instead

## S1 Rapid Library Search Pattern Recognition

**Winners**: NumPy, SciPy, SALib
- Millions/thousands of users
- Part of standard stack
- <30 min to first example
- Excellent documentation

**Losers**: Everything else
- Niche adoption
- Specialized use cases
- Steep learning curves
- Redundant with standard stack

## Key Insight

The Python scientific ecosystem has consolidated around NumPy/SciPy. Specialized packages from 2010-2015 era are being deprecated as SciPy absorbs their functionality. For rapid development, stick to the standard stack + SALib for sensitivity analysis.

## S1 Decision Rule

If it's not:
1. Part of NumPy/SciPy, OR
2. The dominant library in its niche (like SALib), OR
3. Providing unique functionality (like uncertainties)

Then skip it. Use the popular solution.
