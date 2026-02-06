# scipy.optimize: Python's Built-In Optimization

## Overview

`scipy.optimize` is part of SciPy, the foundational scientific computing library for Python. It provides optimization algorithms for **continuous** problems, both constrained and unconstrained. Part of the scipy package which has millions of downloads per year (>13M from PyPI in 2019, likely much higher now as part of scientific Python stack).

**Key insight**: scipy.optimize is ubiquitous but limited to smaller-scale problems and lacks mixed-integer programming capability.

## Installation

```bash
pip install scipy
```

scipy is typically pre-installed in scientific Python distributions (Anaconda, etc.) and has no external dependencies beyond NumPy.

## Problem Types Supported

| Problem Type | Supported | Notes |
|--------------|-----------|-------|
| Unconstrained minimization | ✅ Yes | `minimize` with methods BFGS, Nelder-Mead, etc. |
| Bound-constrained | ✅ Yes | `minimize` with `bounds` parameter, L-BFGS-B |
| Linearly constrained | ✅ Yes | `minimize` with LinearConstraint |
| Nonlinearly constrained | ✅ Yes | `minimize` with NonlinearConstraint, SLSQP, trust-constr |
| Least-squares | ✅ Yes | `least_squares` (Levenberg-Marquardt, trust-region) |
| Curve fitting | ✅ Yes | `curve_fit` wrapper around least-squares |
| Root finding | ✅ Yes | `root`, `fsolve` |
| Linear programming | ✅ Yes | `linprog` (HiGHS backend since SciPy 1.6.0) |
| Integer variables | ❌ No | Cannot handle MILP |
| Global optimization | ⚠️ Limited | `differential_evolution`, `basinhopping` (metaheuristics) |

## Basic Example: Unconstrained Optimization

```python
import numpy as np
from scipy.optimize import minimize

# Define Rosenbrock function (classic test problem)
def rosenbrock(x):
    return sum(100.0 * (x[1:] - x[:-1]**2)**2 + (1 - x[:-1])**2)

# Initial guess
x0 = np.array([1.3, 0.7, 0.8, 1.9, 1.2])

# Optimize with BFGS (gradient-based)
result = minimize(rosenbrock, x0, method='BFGS')

print(f"Optimal solution: {result.x}")
print(f"Optimal value: {result.fun}")
print(f"Success: {result.success}")
```

## Basic Example: Constrained Optimization

```python
from scipy.optimize import minimize, LinearConstraint, NonlinearConstraint

# Minimize x^2 + y^2 subject to x + y >= 1, x >= 0, y >= 0
def objective(x):
    return x[0]**2 + x[1]**2

# Linear constraint: x + y >= 1  →  -x - y <= -1
linear_constraint = LinearConstraint([[1, 1]], [1], [np.inf])

# Bounds: x >= 0, y >= 0
bounds = [(0, None), (0, None)]

# Optimize with SLSQP (Sequential Least Squares Programming)
result = minimize(objective, x0=[0, 0], method='SLSQP',
                  constraints=linear_constraint, bounds=bounds)

print(f"Optimal solution: {result.x}")  # Should be approximately [0.5, 0.5]
print(f"Optimal value: {result.fun}")   # Should be approximately 0.5
```

## Basic Example: Linear Programming

```python
from scipy.optimize import linprog

# Minimize: c^T x
c = [-1, -2]  # Coefficients (negative because linprog minimizes)

# Subject to: A_ub @ x <= b_ub
A_ub = [[2, 1],   # 2x + y <= 20
        [1, 2]]   # x + 2y <= 20

b_ub = [20, 20]

# Bounds: x >= 0, y >= 0
bounds = [(0, None), (0, None)]

# Solve with HiGHS (default since SciPy 1.6.0)
result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

print(f"Optimal solution: {result.x}")
print(f"Optimal value: {-result.fun}")  # Negate because we minimized negative
```

## Available Optimization Methods

### Unconstrained Minimization (`minimize`)

| Method | Type | Derivatives | Characteristics |
|--------|------|-------------|-----------------|
| `'BFGS'` | Quasi-Newton | First | Fast, requires gradient (auto-computed if not provided) |
| `'L-BFGS-B'` | Quasi-Newton | First | Memory-efficient, handles bounds |
| `'Nelder-Mead'` | Simplex | None | Derivative-free, robust but slower |
| `'Powell'` | Direction set | None | Derivative-free |
| `'CG'` | Conjugate gradient | First | Good for large problems |
| `'Newton-CG'` | Newton | Second | Uses Hessian, very fast convergence |
| `'trust-constr'` | Trust region | First/Second | Handles constraints, state-of-art |

### Constrained Minimization

| Method | Constraints | Derivatives | Notes |
|--------|-------------|-------------|-------|
| `'SLSQP'` | Linear, nonlinear | First | Sequential Least Squares, mature |
| `'trust-constr'` | Linear, nonlinear | First/Second | Modern, recommended for constrained |
| `'COBYLA'` | Nonlinear | None | Derivative-free, slower |

### Global Optimization

| Function | Method | Notes |
|----------|--------|-------|
| `differential_evolution` | Genetic algorithm | Derivative-free, population-based |
| `basinhopping` | Random + local | Combines global search with local refinement |
| `dual_annealing` | Simulated annealing | Probabilistic global search |
| `shgo` | Simplicial homology | Deterministic global search (convex problems) |
| `brute` | Grid search | Exhaustive evaluation on grid |

### Linear Programming

| Method | Algorithm | Notes |
|--------|-----------|-------|
| `'highs'` | Dual simplex, IPM | Default since 1.6.0, fastest |
| `'highs-ds'` | Dual simplex | Simplex variant |
| `'highs-ipm'` | Interior point | Interior point variant |
| `'interior-point'` | Legacy IPM | Deprecated, use HiGHS |
| `'revised simplex'` | Simplex | Deprecated, use HiGHS |

## API Design Philosophy

**Functional interface**: Pass objective function and constraints as Python functions. Solver calls them during optimization.

**Advantages**:
- Quick to get started
- Flexible (any Python code in objective)
- No need to learn modeling language

**Disadvantages**:
- No symbolic differentiation (relies on numerical gradients unless you provide analytical)
- Difficult to inspect or modify model structure
- Less efficient for large-scale problems
- Cannot export model to other solvers

## Solver Backends

scipy.optimize is **both library and solver**:
- Implements algorithms directly in Python/Cython (BFGS, Nelder-Mead, etc.)
- Wraps external solvers (HiGHS for LP since 1.6.0)

**Cannot interface with external MILP or NLP solvers** (Gurobi, CPLEX, IPOPT). For multi-solver support, use Pyomo or PuLP.

## When to Use scipy.optimize

### ✅ Good fit when:
- **Already using scipy/numpy**: Zero additional dependencies
- **Small to medium scale**: Hundreds to thousands of variables
- **Continuous variables**: No integer decisions
- **Rapid prototyping**: Quick experiments, research code
- **Function-based objective**: Simulation output, machine learning model, complex calculation
- **Scientific computing context**: Parameter estimation, curve fitting, model calibration

### ❌ Not suitable when:
- **Integer variables required**: No MILP capability → use PuLP, Pyomo, OR-Tools
- **Large-scale LP/MILP**: Thousands of constraints → use dedicated solvers
- **Need solver flexibility**: Cannot swap solvers (Gurobi vs CBC) → use Pyomo
- **Complex model structure**: Many constraints, reusable model → use algebraic modeling
- **Production performance critical**: Direct solver APIs (gurobipy) may be faster

## Community and Maturity

| Metric | Value/Status |
|--------|--------------|
| **Maturity** | Mature (20+ years, scipy 0.x era) |
| **Downloads** | Millions (part of scipy package) |
| **Maintenance** | Very active (scipy core team) |
| **Documentation** | Excellent (scipy.org/docs) |
| **License** | BSD (permissive) |
| **Python versions** | 3.9+ (scipy 1.11+) |

scipy is the **foundation** of scientific Python. Extremely stable, well-tested, and maintained.

## Key Findings from Research

1. **HiGHS adoption (2021)**: SciPy 1.6.0 switched to HiGHS for `linprog`, providing competitive LP performance with open-source solver.

2. **No MILP support**: This is the biggest limitation. For integer variables, must use other libraries.

3. **Gradient computation**: If you don't provide analytical gradients, scipy uses finite differences (slow, inaccurate). Consider automatic differentiation (JAX, autograd).

4. **Trust-region methods**: `trust-constr` (added 2018) is modern, robust method for constrained optimization. Recommended over older SLSQP for difficult problems.

5. **Global optimization limited**: Metaheuristics (`differential_evolution`) can escape local optima but no guarantee of global optimum. For convex problems, local methods sufficient.

## Comparison with Alternatives

| Feature | scipy.optimize | Pyomo | CVXPY | PuLP |
|---------|----------------|-------|-------|------|
| Installation | Built-in (scipy) | pip install | pip install | pip install |
| MILP support | ❌ No | ✅ Yes | ❌ No | ✅ Yes |
| NLP support | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| Modeling style | Functional | Algebraic | Algebraic | Algebraic |
| Solver backends | Few (HiGHS for LP) | 20+ | 10+ | 10+ |
| Learning curve | Easy | Moderate | Moderate | Easy |
| Best for | Quick prototypes, NLP | Multi-solver flexibility | Convex optimization | Simple LP/MILP |

## Example Use Cases (Generic)

### Parameter Estimation
Fit model parameters to data by minimizing prediction error.

```python
def model_prediction(params, inputs):
    # Your model here
    return predictions

def objective(params):
    predictions = model_prediction(params, training_data)
    return np.sum((predictions - observations)**2)

result = minimize(objective, initial_params, method='L-BFGS-B')
```

### Optimal Resource Allocation (Continuous)
Allocate continuous quantities (e.g., budget, energy) across options to maximize utility.

```python
def utility(allocation):
    # Compute total utility from allocation
    return -np.sum(utility_functions(allocation))  # Negative for minimization

constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - total_budget}
bounds = [(0, None)] * n_options

result = minimize(utility, initial_allocation, method='SLSQP',
                  constraints=constraints, bounds=bounds)
```

### Calibration Against Simulation
Find input parameters that make simulation output match observed data.

```python
def simulation_error(params):
    # Run simulation with params
    sim_output = run_simulation(params)
    return np.sum((sim_output - target_output)**2)

result = minimize(simulation_error, initial_params, method='Nelder-Mead')
```

## References

- SciPy documentation: https://docs.scipy.org/doc/scipy/reference/optimize.html
- SciPy 1.0 paper: Virtanen et al., Nature Methods 2020
- HiGHS integration: SciPy 1.6.0 release notes (2021)

## Summary

**scipy.optimize** is the default starting point for **continuous optimization** in Python. Excellent for:
- Research and prototyping
- Parameter estimation and curve fitting
- Small to medium problems
- Users already in scipy/numpy ecosystem

For production MILP, multi-solver support, or large-scale problems, consider Pyomo, PuLP, or OR-Tools instead.
