# Rapid Discovery: What is Mathematical Optimization?

## Technical Overview

Mathematical optimization (mathematical programming) is the discipline of finding the **best element** from a feasible set with respect to an objective criterion. Formally:

```
minimize (or maximize)    f(x)
subject to                g_i(x) ≤ 0,  i = 1,...,m
                          h_j(x) = 0,  j = 1,...,p
                          x ∈ X
```

Where:
- **f(x)**: Objective function to minimize/maximize
- **x**: Decision variables (what we control)
- **g_i(x)**: Inequality constraints
- **h_j(x)**: Equality constraints
- **X**: Domain of variables (e.g., real numbers, integers)

## Problem Type Taxonomy

The structure of f(x), g_i(x), h_j(x), and X determines problem **type**, which drives solver selection.

### Linear Programming (LP)

**Definition**: Linear objective, linear constraints, continuous variables.

```
minimize    c^T x
subject to  Ax ≤ b
            x ≥ 0
```

**Example**: Maximize profit from production of multiple products with resource constraints.

**Characteristics**:
- Polynomial-time solvable (simplex, interior point methods)
- Global optimum guaranteed
- Well-understood theory
- Efficient solvers (HiGHS, GLPK, commercial)

**When to use**: Resource allocation, blending problems, network flows, diet problems, transportation problems.

### Mixed-Integer Linear Programming (MILP/MIP)

**Definition**: LP where some/all variables must be integers.

```
minimize    c^T x
subject to  Ax ≤ b
            x_i ∈ {0,1} or x_i ∈ ℤ for some i
```

**Example**: Select which facilities to open (binary decisions) to minimize total cost.

**Characteristics**:
- NP-hard (computationally difficult)
- Branch-and-bound, branch-and-cut algorithms
- Modern solvers extremely effective for practical instances
- Special structure (e.g., network flows) helps

**When to use**: Yes/no decisions (selection, assignment), scheduling with discrete time periods, facility location, cutting stock, bin packing.

### Quadratic Programming (QP)

**Definition**: Quadratic objective, linear constraints.

```
minimize    (1/2) x^T Q x + c^T x
subject to  Ax ≤ b
```

**Example**: Portfolio optimization minimizing variance (quadratic) subject to return requirements.

**Characteristics**:
- If Q is positive semidefinite (convex), efficiently solvable
- If Q is indefinite (non-convex), NP-hard
- Interior point methods effective for convex case

**When to use**: Portfolio optimization, least-squares problems, model predictive control.

### Nonlinear Programming (NLP)

**Definition**: Nonlinear objective or constraints.

```
minimize    f(x)
subject to  g_i(x) ≤ 0
```

**Example**: Minimize chemical reactor cost (nonlinear engineering equations) subject to safety constraints.

**Characteristics**:
- Wide range of difficulty depending on problem structure
- Local optimum vs global optimum distinction critical
- Gradient-based methods (BFGS, SQP, interior point)
- Derivative-free methods for non-smooth functions

**When to use**: Engineering design, parameter estimation, fitting nonlinear models, physical system optimization.

### Convex Optimization

**Definition**: Convex objective function, convex feasible region.

A function f is **convex** if:
```
f(αx + (1-α)y) ≤ αf(x) + (1-α)f(y)  for all α ∈ [0,1]
```

**Example**: Minimize convex loss function subject to norm constraints.

**Characteristics**:
- **Any local optimum is global optimum**
- Polynomial-time solvable for many subclasses
- LP and convex QP are special cases
- Includes conic programming (SOCP, SDP)

**When to use**: Machine learning (SVM, logistic regression), signal processing, control systems, robust optimization.

### Constraint Programming (CP)

**Definition**: Logical and combinatorial constraints, often with discrete variables.

**Example**: Scheduling tasks with precedence constraints, resource limits, and no-overlap requirements.

**Characteristics**:
- Domain propagation and constraint inference
- Effective for scheduling, timetabling, configuration
- Different paradigm from mathematical programming

**When to use**: Scheduling with complex logical rules, rostering, configuration problems, puzzles.

### Multi-Objective Optimization

**Definition**: Multiple objective functions simultaneously.

```
minimize    [f_1(x), f_2(x), ..., f_k(x)]
subject to  g_i(x) ≤ 0
```

**Example**: Minimize cost AND minimize emissions (competing objectives).

**Characteristics**:
- No single "optimal" solution
- Find **Pareto frontier** (solutions where improving one objective worsens another)
- Requires preference specification or generate full frontier

**When to use**: Trade-off analysis, multi-criteria decision making, design optimization with competing goals.

## Solver vs Modeling Language Distinction

### Solver
The **engine** that implements optimization algorithms and computes solutions.

**Examples**:
- **Open-source**: HiGHS, CBC, GLPK, SCIP, IPOPT, OSQP
- **Commercial**: Gurobi, CPLEX, MOSEK, XPRESS

**Role**: Takes problem in standard form (MPS, LP file, or direct API) and returns solution.

### Modeling Language
The **interface** for expressing optimization problems in human-readable form.

**Examples**:
- **Python**: Pyomo, CVXPY, PuLP, OR-Tools
- **Others**: AMPL, GAMS, JuMP (Julia)

**Role**: Translates user model to solver input format, manages data, retrieves results.

**Analogy**: Modeling language is like SQL (express what you want), solver is like database engine (compute the result).

## Optimization Algorithm Approaches

### Gradient-Based Methods

**Principle**: Use derivatives to determine descent direction.

**Algorithms**:
- **Gradient descent**: Move in direction of negative gradient
- **Newton's method**: Use second derivatives (Hessian) for faster convergence
- **Quasi-Newton (BFGS)**: Approximate Hessian efficiently
- **Sequential Quadratic Programming (SQP)**: Solve sequence of QP subproblems
- **Interior point methods**: Move through interior of feasible region

**Requirements**: Objective and constraints must be differentiable.

**Advantages**:
- Fast convergence for smooth problems
- Efficient for large-scale problems
- Mature theory and implementations

**Limitations**:
- May converge to local optima (non-convex problems)
- Requires gradient computation (analytical or automatic differentiation)

**When to use**: Continuous optimization, smooth functions, large scale.

### Derivative-Free Methods

**Principle**: Optimize without computing gradients.

**Algorithms**:
- **Nelder-Mead simplex**: Geometric search using simplex shape
- **Powell's method**: Sequential line searches
- **Pattern search**: Evaluate on geometric patterns
- **Trust region methods**: Sample within trusted radius

**Advantages**:
- Handle non-smooth, noisy objectives
- Simple to implement
- No derivative computation needed

**Limitations**:
- Slower convergence than gradient-based
- Struggle with high dimensions
- No guarantee of global optimum

**When to use**: Black-box objectives (simulation-based), non-smooth functions, small to medium dimension.

### Combinatorial/Discrete Optimization

**Principle**: Systematically search discrete solution space.

**Algorithms**:
- **Branch-and-bound**: Partition space, bound subproblem solutions
- **Branch-and-cut**: Branch-and-bound with cutting planes
- **Dynamic programming**: Solve subproblems recursively
- **Constraint propagation**: Eliminate infeasible values

**Characteristics**:
- Exact methods guarantee optimal solution
- Computational complexity often exponential
- Modern implementations highly optimized

**When to use**: Integer variables, combinatorial structure.

### Metaheuristics

**Principle**: Heuristic search strategies inspired by natural processes.

**Algorithms**:
- **Genetic algorithms**: Evolutionary selection and crossover
- **Simulated annealing**: Probabilistic acceptance of worse solutions
- **Particle swarm optimization**: Population-based search
- **Tabu search**: Guided local search with memory

**Advantages**:
- Applicable to any problem type
- Can escape local optima
- Handle large, complex, black-box problems

**Limitations**:
- No optimality guarantee
- Many parameters to tune
- Computational cost (many evaluations)

**When to use**: Complex, non-convex problems where exact methods too slow, multi-objective optimization, robust optimization.

## Key Insights for Solver Selection

1. **Problem type drives solver choice**: LP solvers can't handle integers, MILP solvers can't handle nonlinearity. Know your problem type.

2. **Convexity is gold**: Convex problems have global optima and efficient algorithms. Test if your problem is convex.

3. **Size matters differently**: LP scales to millions of variables. MILP scales to thousands to hundreds of thousands. NLP scaling depends heavily on structure.

4. **Modeling language adds convenience**: For rapid development, algebraic modeling (Pyomo, CVXPY) beats direct API coding.

5. **Commercial vs open-source gap narrowing**: Open-source solvers (HiGHS, SCIP) competitive for many problems. Commercial edge on largest MILP instances.

6. **Solver backend matters more than frontend**: For production performance, solver (Gurobi vs CBC) dominates modeling language choice (Pyomo vs PuLP).

## Problem Type Decision Tree

```
Is objective and constraints linear?
├─ YES, all continuous → LP
│  └─ Solvers: HiGHS, GLPK, Gurobi, CPLEX
├─ YES, some integer → MILP
│  └─ Solvers: CBC, SCIP, HiGHS, Gurobi, CPLEX
└─ NO (nonlinear)
   ├─ Is problem convex?
   │  ├─ YES → Convex optimization
   │  │  └─ Solvers: ECOS, SCS, MOSEK, Clarabel
   │  └─ NO → General NLP
   │     └─ Solvers: IPOPT, SNOPT, Knitro
   └─ Logical constraints, scheduling? → Constraint Programming
      └─ Solvers: OR-Tools CP-SAT, Gecode

Multiple objectives?
└─ Multi-objective optimization (pymoo, weighted sum, epsilon-constraint)

Dynamic over time with differential equations?
└─ Dynamic optimization (GEKKO, Pyomo.DAE)
```

## Next Steps in S1-Rapid

The following pages investigate specific Python libraries:
- **scipy.optimize**: Built-in Python scientific computing
- **OR-Tools**: Google's operations research toolkit
- **Pyomo**: Algebraic modeling language
- **CVXPY**: Convex optimization specialist
- **PuLP**: Simple LP/MILP modeling

Each library page documents:
- Problem types supported
- Installation and basic example
- API approach and design philosophy
- Solver backends available
- Maturity and community indicators
- When to choose this library
