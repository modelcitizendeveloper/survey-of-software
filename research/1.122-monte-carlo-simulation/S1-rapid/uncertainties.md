# Library Assessment: uncertainties

## Quick Overview

**Package**: uncertainties
**Repository**: https://github.com/lmfit/uncertainties
**Domain**: Automatic error propagation and uncertainty calculations

## Popularity Metrics

**PyPI Downloads**: High (exact numbers not available, but well-established)
**GitHub**: lmfit/uncertainties (ownership transferred to lmfit org in 2024)
**Maintenance**: Active - part of lmfit ecosystem
**Documentation**: https://uncertainties-python-package.readthedocs.io/

## What It Does

Transparent uncertainty propagation:
- Automatic error propagation through calculations
- Linear error propagation theory
- Correlation tracking between variables
- Works with NumPy arrays
- Uncertainty-aware math functions

## Quick "Does It Work" Validation

**Time to first working example**: 5 minutes

```python
from uncertainties import ufloat
from uncertainties.umath import sin, sqrt

# Create value with uncertainty
wait_time = ufloat(45.2, 3.1)  # 45.2 ± 3.1 seconds

# Operations propagate errors automatically
doubled = 2 * wait_time  # 90.4 ± 6.2
squared = wait_time**2   # 2043 ± 280

# Complex calculations
result = sqrt(wait_time) + sin(wait_time)
print(result)  # Shows value ± uncertainty
```

Works immediately, very intuitive.

## Learning Curve

**Estimate**: Very low (<1 hour)

- Simple, pythonic interface
- Works like regular numbers
- Automatic everything (no manual derivatives)
- Natural syntax: `(2 +/- 0.1) * 2 = 4 +/- 0.2`

## Strengths (S1 Perspective)

1. **Unique capability**: Only major library for automatic error propagation
2. **Zero friction**: Numbers with uncertainties work like normal numbers
3. **Correlation handling**: Automatically tracks dependencies
4. **NumPy integration**: Works with arrays
5. **Well-documented**: Clear examples and API docs
6. **Mature**: Been around for years, stable API

## Limitations

- Linear error propagation only (not full Monte Carlo)
- Can't handle complex statistical distributions
- Not designed for sensitivity analysis
- Performance overhead for large arrays

## Use Case Fit

**Perfect for**:
- Confidence intervals on predictions (wait time ranges)
- Error bars through calculations
- Uncertainty propagation through formulas
- Quick "what's my error?" questions
- Reporting results with ± notation

**Not sufficient for**:
- Sensitivity analysis (use SALib)
- Advanced Monte Carlo (use NumPy + SciPy)
- Non-linear uncertainty propagation

## When to Use

Use when you want error bars on calculated results without writing:
```python
# Manual error propagation (tedious)
y_error = sqrt((dy_dx * x_error)**2 + (dy_db * b_error)**2)

# With uncertainties (automatic)
y = f(x, b)  # errors propagate automatically
```

## Integration Points

- Works with NumPy functions via uncertainties.unumpy
- Compatible with standard math operations
- Can extract nominal values and errors: `value.n`, `value.s`
- Converts to/from NumPy arrays easily

## Quick Start Resources

1. Official docs: https://uncertainties-python-package.readthedocs.io/
2. GitHub: https://github.com/lmfit/uncertainties
3. Quick guide: https://pythonhosted.org/uncertainties/
4. PDF manual: Available on readthedocs

## S1 Verdict

**Adoption Score**: 8/10 (widely used in physics/engineering)
**Ease of Use**: 10/10 (trivial to use)
**Time to Value**: 10/10 (instant results)

**Overall**: Perfect for adding error bars to results. Unique capability, no real alternative.
