# CVXPY: Convex Optimization in Python

## Overview

CVXPY is a Python-embedded modeling language for **convex optimization** problems. It provides automatic verification of problem convexity through Disciplined Convex Programming (DCP) analysis, ensuring that your problem can be solved globally and efficiently.

**Key finding**: CVXPY is the specialist for convex optimization, with Stanford academic origins and JMLR publication (2016). Unlike general-purpose tools, CVXPY **verifies convexity** at modeling time, preventing common errors.

## Installation

```bash
pip install cvxpy
```

CVXPY includes open-source solvers (Clarabel, SCS, OSQP, ECOS) by default. Additional solvers (MOSEK, Gurobi, CPLEX) can be used if installed.

## Problem Types Supported

CVXPY is specialized for **convex optimization**:

| Problem Type | Supported | Notes |
|--------------|-----------|-------|
| Linear Programming (LP) | ✅ Yes | Special case of convex |
| Quadratic Programming (QP) | ✅ Yes (if convex) | Positive semidefinite Q |
| Second-Order Cone (SOCP) | ✅ Yes | Norm constraints |
| Semidefinite Programming (SDP) | ✅ Yes | Matrix constraints |
| General Convex | ✅ Yes | If DCP-compliant |
| Mixed-Integer Convex | ⚠️ Limited | Via branch-and-bound (slow) |
| Nonconvex (general NLP) | ❌ No | Use scipy or Pyomo+IPOPT |
| Mixed-Integer LP (MILP) | ❌ No | Use PuLP, Pyomo, OR-Tools |

**Core insight**: If your problem is convex, CVXPY is likely the best choice. DCP analysis catches modeling errors early.

## What is Convex Optimization?

A problem is **convex** if:
1. Objective function is convex (for minimization)
2. Feasible region is convex

**Why convexity matters**:
- Any local optimum is a **global optimum**
- Polynomial-time algorithms available
- No initialization sensitivity
- Reliable, predictable solving

**Common convex problems**:
- Linear programming
- Least-squares regression
- Lasso, ridge regression
- Support vector machines (SVM)
- Portfolio optimization (mean-variance)
- Signal processing (filter design)
- Control systems (LQR, MPC)

## Disciplined Convex Programming (DCP)

DCP is a ruleset for constructing convex optimization problems. CVXPY automatically checks DCP compliance.

**DCP rules**:
- Convex functions can only be minimized or bounded above
- Concave functions can only be maximized or bounded below
- Affine functions can be used anywhere
- Composition rules ensure convexity is preserved

**Example of DCP violation**:
```python
import cvxpy as cp

x = cp.Variable()
# ERROR: Cannot minimize a concave function
objective = cp.Minimize(-cp.sqrt(x))  # sqrt is concave
```

CVXPY raises an error immediately, preventing silent failures.

## Basic Example: Linear Programming

```python
import cvxpy as cp

# Variables
x = cp.Variable()
y = cp.Variable()

# Objective: minimize -x - 2y (equivalent to maximize x + 2y)
objective = cp.Minimize(-x - 2*y)

# Constraints
constraints = [
    2*x + y <= 20,
    x + 2*y <= 20,
    x >= 0,
    y >= 0
]

# Create and solve problem
problem = cp.Problem(objective, constraints)
problem.solve(solver=cp.CLARABEL)

print(f"Status: {problem.status}")
print(f"Optimal value: {-problem.value}")  # Negate for maximization
print(f"x = {x.value}")
print(f"y = {y.value}")
```

## Basic Example: Quadratic Programming (Portfolio Optimization)

```python
import cvxpy as cp
import numpy as np

# Portfolio optimization: minimize risk subject to return target
n_assets = 4
returns = np.array([0.10, 0.15, 0.12, 0.08])  # Expected returns
cov_matrix = np.array([  # Covariance matrix (risk)
    [0.04, 0.01, 0.02, 0.01],
    [0.01, 0.06, 0.01, 0.02],
    [0.02, 0.01, 0.05, 0.01],
    [0.01, 0.02, 0.01, 0.03]
])

# Variables: portfolio weights
w = cp.Variable(n_assets)

# Objective: minimize portfolio variance (risk)
risk = cp.quad_form(w, cov_matrix)
objective = cp.Minimize(risk)

# Constraints
constraints = [
    cp.sum(w) == 1,           # Weights sum to 1
    w >= 0,                    # No short selling
    returns @ w >= 0.11        # Target return of 11%
]

problem = cp.Problem(objective, constraints)
problem.solve()

print(f"Optimal portfolio: {w.value}")
print(f"Expected return: {returns @ w.value:.2%}")
print(f"Portfolio variance: {problem.value:.4f}")
print(f"Portfolio std dev: {np.sqrt(problem.value):.2%}")
```

## Basic Example: L1 Regression (Lasso)

```python
import cvxpy as cp
import numpy as np

# Generate synthetic data
np.random.seed(1)
n, p = 100, 20
X = np.random.randn(n, p)
beta_true = np.zeros(p)
beta_true[:5] = np.array([1, -2, 0.5, -1, 3])  # Sparse true coefficients
y = X @ beta_true + 0.1 * np.random.randn(n)

# Lasso regression: minimize ||Xβ - y||² + λ||β||₁
beta = cp.Variable(p)
lambda_reg = 0.1

objective = cp.Minimize(cp.sum_squares(X @ beta - y) + lambda_reg * cp.norm(beta, 1))
problem = cp.Problem(objective)
problem.solve()

print(f"True coefficients: {beta_true[:5]}")
print(f"Estimated coefficients: {beta.value[:5]}")
print(f"Number of non-zero: {np.sum(np.abs(beta.value) > 0.01)}")
```

## Basic Example: Constraint with Norms (SOCP)

```python
import cvxpy as cp

# Minimize ||x - center||₂ subject to linear constraints
x = cp.Variable(3)
center = np.array([1, 2, 3])

objective = cp.Minimize(cp.norm(x - center, 2))

constraints = [
    cp.sum(x) == 9,
    x >= 0
]

problem = cp.Problem(objective, constraints)
problem.solve()

print(f"Closest point: {x.value}")
print(f"Distance: {problem.value}")
```

## API Design Philosophy

**Algebraic modeling with DCP verification**: Express problems naturally while CVXPY ensures convexity.

**Advantages**:
- **Automatic convexity verification**: Catch modeling errors at construction time
- **Readable code**: Mathematical notation
- **Solver abstraction**: CVXPY reformulates problem for solver capabilities
- **Parameters**: Separate data from structure, enable rapid re-solves

**Disadvantages**:
- **Limited to convex problems**: Cannot handle general nonlinear
- **No integer variables** (or very limited support via MI-CVXPY)
- **DCP learning curve**: Must understand convexity rules

## Solver Backends

CVXPY automatically selects appropriate solver based on problem type.

### Bundled (Free):
- **Clarabel**: Rust-based interior point (default for many problems)
- **SCS**: Splitting Conic Solver (robust, medium accuracy)
- **OSQP**: Operator Splitting QP (fast for QP)
- **ECOS**: Embedded Conic Solver (small to medium SOCP)
- **CVXOPT**: Python convex optimization

### Commercial (if installed):
- **MOSEK**: High-performance conic (SOCP, SDP)
- **Gurobi**: QP and conic support
- **CPLEX**: QP support

### Specialized:
- **GLPK**, **CBC**: LP/MILP via Pyomo interface
- **NAG**: Numerical Algorithms Group

Specify solver with `problem.solve(solver=cp.MOSEK)`.

## When to Use CVXPY

### ✅ Good fit when:
- **Problem is convex**: LP, convex QP, SOCP, SDP, convex constraints
- **Want convexity verification**: Prevent modeling errors with DCP
- **Machine learning**: Lasso, ridge, SVM, logistic regression
- **Portfolio optimization**: Mean-variance, risk parity
- **Signal processing**: Filter design, compressed sensing
- **Control theory**: LQR, MPC with convex constraints
- **Parameter tuning**: Rapid re-solves with different data (cp.Parameter)

### ❌ Not suitable when:
- **Integer variables**: No MILP support → use PuLP, Pyomo, OR-Tools
- **Nonconvex NLP**: Non-convex objectives/constraints → use scipy, Pyomo+IPOPT
- **Combinatorial optimization**: Scheduling, routing → use OR-Tools
- **Large-scale MILP**: Commercial solvers faster → Gurobi, CPLEX directly

## Community and Maturity

| Metric | Value/Status |
|--------|--------------|
| **GitHub stars** | Not directly checked (cvxpy/cvxpy) |
| **Maturity** | Mature (10+ years) |
| **Academic roots** | Stanford (Stephen Boyd group) |
| **Publication** | JMLR 2016 (Vol 17, No 83) |
| **Maintenance** | Active |
| **Documentation** | Excellent (cvxpy.org) |
| **License** | Apache 2.0 |
| **Courses** | Used in Stanford CVX101 (Convex Optimization) |

CVXPY is the **standard tool** for convex optimization in Python, widely used in academia and industry.

## Key Findings from Research

1. **DCP verification is killer feature**: Automatically checks convexity at modeling time. No other Python library does this.

2. **Academic pedigree**: Developed by Stephen Boyd's group at Stanford, based on CVX (MATLAB). Used in teaching convex optimization.

3. **Automatic reformulation**: CVXPY transforms your problem into standard conic form for solvers. You model naturally, CVXPY handles the details.

4. **Parameters enable fast re-solves**: Declare `cp.Parameter` for data that changes, dramatically faster than rebuilding model.

5. **Disciplined Convex Programming (DCP)**: Ruleset ensures convexity. Learning curve, but catches errors early.

## Comparison with Alternatives

| Feature | CVXPY | Pyomo | scipy.optimize | PuLP |
|---------|-------|-------|----------------|------|
| Convex optimization | ✅ Best | ✅ Yes | ✅ Yes | ⚠️ LP only |
| DCP verification | ✅ Yes | ❌ No | ❌ No | ❌ No |
| MILP | ❌ No | ✅ Yes | ❌ No | ✅ Yes |
| General NLP | ❌ No | ✅ Yes | ✅ Yes | ❌ No |
| Learning curve | Moderate | Moderate | Easy | Easy |
| Best for | Convex problems | Multi-solver | Prototyping | Simple LP/MILP |

## Example Use Cases (Generic)

### Resource Allocation with Quadratic Cost
Allocate resources to minimize quadratic cost (diminishing returns).

```python
import cvxpy as cp

# Allocate budget across N options with diminishing returns
x = cp.Variable(n_options)

# Quadratic cost (diminishing returns modeled as x^2)
objective = cp.Minimize(cp.sum_squares(x))

constraints = [
    cp.sum(x) == total_budget,
    x >= min_allocation,
    x <= max_allocation
]

problem = cp.Problem(objective, constraints)
problem.solve()
```

### Robust Optimization
Minimize worst-case cost under uncertainty.

```python
import cvxpy as cp

# Worst-case cost over uncertain parameters
x = cp.Variable(n)
u = cp.Variable(m)  # Uncertain parameters

# Minimize worst-case objective
objective = cp.Minimize(cp.max(cost_scenarios @ x))

constraints = [
    A @ x + B @ u <= b,
    cp.norm(u, 2) <= uncertainty_radius,  # Uncertainty set
    x >= 0
]

problem = cp.Problem(objective, constraints)
problem.solve()
```

### Fair Resource Allocation
Maximize minimum allocation (max-min fairness).

```python
import cvxpy as cp

# Allocate resources fairly (maximize minimum share)
x = cp.Variable(n_users)
min_share = cp.Variable()

objective = cp.Maximize(min_share)

constraints = [
    x >= min_share,  # Each user gets at least min_share
    cp.sum(x) <= total_capacity,
    x >= 0
]

problem = cp.Problem(objective, constraints)
problem.solve()
```

## Advanced Features

### Parameters for Fast Re-solving
```python
# Define parameter (data that changes)
lambda_param = cp.Parameter(nonneg=True)
beta = cp.Variable(p)

objective = cp.Minimize(cp.sum_squares(X @ beta - y) + lambda_param * cp.norm(beta, 1))
problem = cp.Problem(objective)

# Solve for different lambda values (fast!)
for lam in [0.01, 0.1, 1.0]:
    lambda_param.value = lam
    problem.solve(warm_start=True)
    print(f"Lambda={lam}: objective={problem.value}")
```

### Constraints as Objects
```python
# Store constraint for later modification
budget_constraint = cp.sum(x) <= budget_param
problem = cp.Problem(objective, [budget_constraint, ...])

# Later, change budget and re-solve
budget_param.value = new_budget
problem.solve()
```

### Dual Variables
```python
# Access dual variables (shadow prices)
problem.solve()
print(f"Dual value: {constraints[0].dual_value}")
```

## Problem Classes CVXPY Recognizes

CVXPY automatically classifies problems for solver selection:

- **LP**: Linear Programming
- **QP**: Quadratic Programming
- **SOCP**: Second-Order Cone Programming (norm constraints)
- **SDP**: Semidefinite Programming (matrix constraints)
- **ExpCone**: Exponential cone (entropy, log)
- **PowCone**: Power cone (geometric programming)

Check with: `print(problem.classification)`

## References

- Official documentation: https://www.cvxpy.org
- GitHub: https://github.com/cvxpy/cvxpy
- Paper: Diamond & Boyd, "CVXPY: A Python-Embedded Modeling Language for Convex Optimization", JMLR 2016
- Tutorial: https://www.cvxpy.org/tutorial/
- Book: Boyd & Vandenberghe, "Convex Optimization" (free online)

## Summary

**CVXPY** is the specialist for convex optimization:
- Automatic convexity verification (DCP analysis)
- Natural mathematical notation
- Excellent for machine learning, portfolio optimization, signal processing
- Stanford academic origins, widely used in education and research

**Choose CVXPY** when:
- Your problem is convex (or you want to verify it is)
- Machine learning applications (Lasso, SVM, logistic regression)
- Portfolio optimization, control theory, signal processing
- You want to catch modeling errors early with DCP

**Look elsewhere** for:
- Integer variables (PuLP, Pyomo, OR-Tools)
- General nonlinear (scipy, Pyomo)
- Large-scale MILP (Gurobi, CPLEX)

If your problem is convex, start with CVXPY. The DCP verification alone is worth it.
