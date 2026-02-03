# S2-Comprehensive: Optimization Problem Types

## Overview

Optimization problems are classified by the mathematical structure of the objective function, constraints, and variables. This classification determines which algorithms can solve the problem and computational complexity.

**Key principle**: Problem structure determines solvability. Linear problems are polynomial-time; integer programming is NP-hard; general nonlinear can be intractable.

## Taxonomy of Optimization Problems

```
Optimization Problems
│
├── Continuous Variables Only
│   ├── Unconstrained
│   │   ├── Convex → Global optimum guaranteed
│   │   └── Non-convex → Local optima exist
│   │
│   └── Constrained
│       ├── Linear Programming (LP)
│       │   └── Polynomial-time solvable (simplex, interior point)
│       │
│       ├── Convex Optimization
│       │   ├── Quadratic Programming (QP)
│       │   ├── Second-Order Cone Programming (SOCP)
│       │   ├── Semidefinite Programming (SDP)
│       │   └── General Convex → Local = Global optimum
│       │
│       └── Nonlinear Programming (NLP)
│           ├── Convex → Efficient algorithms
│           └── Non-convex → Difficult, local optima
│
└── Discrete/Integer Variables
    ├── Integer Linear Programming (ILP)
    │   └── NP-hard
    │
    ├── Mixed-Integer Linear (MILP)
    │   └── NP-hard, but practical algorithms effective
    │
    ├── Mixed-Integer Nonlinear (MINLP)
    │   └── Very difficult
    │
    ├── Constraint Programming (CP)
    │   └── Logical constraints, domain propagation
    │
    └── Combinatorial Optimization
        └── Graph problems, scheduling, routing
```

---

## 1. Linear Programming (LP)

### Definition

Optimize a linear objective function subject to linear equality and inequality constraints:

```
minimize    c^T x
subject to  Ax ≤ b
            Aeq x = beq
            lb ≤ x ≤ ub
```

Where:
- `x ∈ ℝⁿ`: Decision variables (continuous)
- `c`: Cost coefficients
- `A, b`: Inequality constraints
- `Aeq, beq`: Equality constraints
- `lb, ub`: Variable bounds

### Mathematical Properties

- **Convex feasible region**: Defined by linear constraints (polyhedron)
- **Convex objective**: Linear function is convex
- **Optimal solution**: Occurs at a vertex of the feasible polyhedron
- **Fundamental theorem**: If optimal solution exists, at least one vertex is optimal

### Algorithms

1. **Simplex Method**: Walk along edges of feasible region from vertex to vertex
   - Average-case polynomial, worst-case exponential
   - Very effective in practice

2. **Interior Point Methods**: Move through interior of feasible region
   - Polynomial-time in theory and practice
   - Better for large-scale problems

3. **Dual Simplex**: Operates on dual problem
   - Useful when starting from infeasible solution

### Complexity

**Polynomial-time solvable** in practice. While simplex has worst-case exponential complexity, interior point methods are polynomial, and simplex is extremely effective on practical instances.

### Standard Forms

**Inequality form** (shown above)

**Standard form**: All constraints are equalities with non-negative variables
```
minimize    c^T x
subject to  Ax = b
            x ≥ 0
```

Conversion: Add slack variables to convert inequalities to equalities.

### Special Cases

1. **Network Flow Problems**: LP with network structure
   - Min-cost flow, max-flow, shortest path
   - Special algorithms exploit structure (network simplex)
   - Integer optimal solutions possible with integer data

2. **Transportation Problem**: Ship goods from sources to destinations
   - Bipartite network flow
   - Degenerate structure common

3. **Assignment Problem**: Assign tasks to workers
   - Special case of transportation
   - Hungarian algorithm (combinatorial)

### Applications (Generic)

- Resource allocation with linear costs
- Production planning (continuous quantities)
- Diet/nutrition optimization
- Financial portfolio (without risk minimization)
- Network flow and routing (continuous)
- Blending problems

### Python Libraries

- **scipy.optimize.linprog**: HiGHS backend, good for small-medium
- **PuLP**: Algebraic modeling, CBC bundled
- **Pyomo**: Multi-solver support
- **OR-Tools**: GLOP solver (Google)
- **CVXPY**: Convex optimization framework

---

## 2. Mixed-Integer Linear Programming (MILP/MIP)

### Definition

Linear programming where some or all variables must take integer values:

```
minimize    c^T x
subject to  Ax ≤ b
            x_i ∈ ℤ  for i ∈ I (integer variables)
            x_j ∈ ℝ  for j ∈ C (continuous variables)
            x_i ∈ {0,1}  for i ∈ B (binary variables)
```

### Mathematical Properties

- **NP-hard**: No known polynomial-time algorithm
- **Combinatorial**: Integer variables create discrete decision space
- **Feasible region**: Union of polyhedra (non-convex)
- **Non-convex**: Linear combination of feasible points may be infeasible

### Algorithms

1. **Branch-and-Bound**:
   - Solve LP relaxation (remove integer constraints)
   - Branch on fractional variables
   - Bound: LP relaxation provides lower bound (minimization)
   - Prune branches that cannot improve incumbent solution

2. **Branch-and-Cut**:
   - Branch-and-bound + cutting planes
   - Generate inequalities (cuts) that tighten LP relaxation
   - Cuts remove fractional solutions without removing integer solutions
   - Modern solvers (Gurobi, CPLEX, SCIP) use sophisticated cuts

3. **Branch-and-Price**:
   - Column generation within branch-and-bound
   - For problems with huge numbers of variables
   - Generate variables as needed

### Cutting Planes

Inequalities added to strengthen LP relaxation:

- **Gomory cuts**: General integer cuts
- **Lift-and-project**: Nonlinear inequalities projected to linear
- **Cover cuts**: For knapsack constraints
- **Clique cuts**: For conflict graphs
- **MIR (Mixed-Integer Rounding)**: For mixed-integer problems

### Formulation Quality

**Strong formulation**: LP relaxation tight (close to convex hull of integer solutions)

**Weak formulation**: LP relaxation loose (far from integer hull)

**Impact**: Strong formulations solve much faster. Reformulation techniques:
- Disaggregation
- Symmetry breaking
- Tighter constraints
- Auxiliary variables

### Complexity

- **NP-hard** in general
- **Practical solvability**: Modern solvers (Gurobi, CPLEX, SCIP) solve instances with millions of variables and tens of thousands of integer variables
- **Problem-dependent**: Some structures solve easily (network flow), others intractable

### Special Cases

1. **Pure Integer Programming (ILP)**: All variables integer
2. **Binary Programming**: All variables binary (0/1)
3. **Set Covering/Packing/Partitioning**: Binary variables, specialized structure

### Applications (Generic)

- Facility location (open/close decisions)
- Production planning (batch sizes, setup decisions)
- Scheduling (discrete time periods, binary assignments)
- Routing (visit/don't visit decisions)
- Portfolio selection with cardinality constraints
- Cutting stock and bin packing
- Network design (select edges to include)

### Python Libraries

- **PuLP**: Simple, CBC bundled
- **Pyomo**: Multi-solver (CBC, SCIP, Gurobi, CPLEX)
- **OR-Tools**: SCIP bundled, excellent
- **Gurobi (gurobipy)**: Commercial, fastest
- **CPLEX (docplex)**: IBM commercial

---

## 3. Quadratic Programming (QP)

### Definition

Quadratic objective, linear constraints:

```
minimize    (1/2) x^T Q x + c^T x
subject to  Ax ≤ b
            Aeq x = beq
```

### Convex vs Non-Convex

**Convex QP**: Q is positive semidefinite (Q ⪰ 0)
- Local optimum is global
- Polynomial-time solvable
- Interior point methods effective

**Non-Convex QP**: Q has negative eigenvalues
- Local optima exist
- NP-hard in general
- Much harder to solve

### Algorithms

**Convex QP**:
- Interior point methods (primal-dual)
- Active set methods
- Augmented Lagrangian

**Non-Convex QP**:
- Branch-and-bound (spatial branching)
- SDP relaxations
- Local solvers (may find local optima)

### Applications

- Portfolio optimization (minimize variance)
- Support Vector Machines (SVM)
- Least-squares problems with constraints
- Model Predictive Control (MPC)
- Robust optimization

### Python Libraries

- **CVXPY**: If convex (automatic verification)
- **Pyomo + Gurobi/CPLEX**: Commercial solvers handle QP
- **scipy.optimize.minimize**: For small convex QP
- **OSQP**: Specialized convex QP solver (via CVXPY)

---

## 4. Second-Order Cone Programming (SOCP)

### Definition

Optimization with second-order cone (norm) constraints:

```
minimize    c^T x
subject to  ||A_i x + b_i||_2 ≤ c_i^T x + d_i  for all i
            Fx = g
```

The constraint `||A_i x + b_i||_2 ≤ c_i^T x + d_i` defines a second-order cone (also called Lorentz cone or ice cream cone).

### Properties

- **Convex**: Second-order cone is convex
- **Generalizes QP and LP**: LP (no cones), QP (single quadratic cone)
- **Interior point methods**: Polynomial-time solvable

### Applications

- Robust optimization (worst-case constraints)
- Portfolio optimization with Value-at-Risk (VaR)
- Antenna array design
- Filter design in signal processing
- Structural optimization (engineering)

### Python Libraries

- **CVXPY**: Natural SOCP modeling with `cp.norm`
- **Pyomo + MOSEK**: Commercial solver strong on SOCP
- **SCS, ECOS**: Open-source conic solvers (via CVXPY)

---

## 5. Semidefinite Programming (SDP)

### Definition

Optimization with positive semidefinite matrix constraints:

```
minimize    Trace(CX)
subject to  Trace(A_i X) = b_i
            X ⪰ 0  (positive semidefinite)
```

Where `X` is a matrix variable, and `X ⪰ 0` means all eigenvalues of `X` are non-negative.

### Properties

- **Convex**: Positive semidefinite cone is convex
- **Generalizes LP and SOCP**: LP (diagonal X), SOCP (special structure)
- **Computationally expensive**: Scales poorly with matrix size

### Applications

- Combinatorial optimization relaxations
- Control theory (Lyapunov stability, LQR)
- Matrix completion problems
- Max-cut relaxation
- Quantum information theory

### Python Libraries

- **CVXPY**: `cp.Variable((n, n), PSD=True)` for SDP variables
- **MOSEK**: Commercial, best SDP performance
- **SCS**: Open-source conic solver

---

## 6. Nonlinear Programming (NLP)

### Definition

General nonlinear objective or constraints:

```
minimize    f(x)
subject to  g_i(x) ≤ 0
            h_j(x) = 0
```

Where `f`, `g_i`, `h_j` are nonlinear functions.

### Convex vs Non-Convex

**Convex NLP**: `f` convex, `g_i` convex, `h_j` affine
- Local optimum is global
- Efficient algorithms
- Interior point, SQP methods

**Non-Convex NLP**: General case
- Multiple local optima
- No guarantee of global optimum
- Sensitive to initialization
- Much harder

### Algorithms

1. **Sequential Quadratic Programming (SQP)**:
   - Solve sequence of QP subproblems
   - Approximate objective and constraints with quadratic models
   - Very effective for smooth constrained NLP

2. **Interior Point Methods**:
   - Barrier methods (penalize constraint violations)
   - IPOPT (Interior Point OPTimizer) widely used

3. **Augmented Lagrangian**:
   - Penalty methods with Lagrange multipliers
   - Robust to poor initialization

4. **Trust Region Methods**:
   - Limit step size to region where model is trusted
   - Adapt trust region based on model accuracy

### Derivatives

Most NLP algorithms require:
- **First derivatives** (gradient of objective, Jacobian of constraints)
- **Second derivatives** (Hessian) for faster convergence

**Automatic differentiation**: Compute exact derivatives algorithmically (not finite differences)

### Complexity

- **Convex**: Polynomial-time solvable (similar to LP)
- **Non-convex**: Can be very difficult, no general guarantees

### Applications

- Engineering design optimization (structural, aerodynamic)
- Chemical process optimization (nonlinear kinetics, thermodynamics)
- Parameter estimation (fit nonlinear models to data)
- Optimal control (continuous time, nonlinear dynamics)
- Machine learning (neural networks via gradient descent)

### Python Libraries

- **scipy.optimize**: Good for small-medium NLP (SLSQP, trust-constr)
- **Pyomo + IPOPT**: Large-scale NLP, open-source
- **Pyomo + SNOPT/KNITRO**: Commercial NLP solvers
- **GEKKO**: Dynamic optimization and NLP

---

## 7. Mixed-Integer Nonlinear Programming (MINLP)

### Definition

Nonlinear objective or constraints with integer variables:

```
minimize    f(x, y)
subject to  g_i(x, y) ≤ 0
            h_j(x, y) = 0
            x ∈ ℝⁿ
            y ∈ ℤᵐ
```

### Difficulty

**Very hard**: Combines difficulty of MILP (NP-hard) and NLP (local optima, non-convexity).

### Algorithms

1. **Branch-and-Bound**: Solve NLP relaxations
2. **Outer Approximation**: Linearize nonlinear constraints
3. **Generalized Benders Decomposition**: Decompose into MILP master and NLP subproblem
4. **Hybrid methods**: Combine multiple techniques

### Solvers

- **BARON**: Global MINLP solver (deterministic)
- **SCIP**: Open-source (now Apache 2.0)
- **Couenne**, **Bonmin**: Open-source (EPL)
- **ANTIGONE**: Academic
- **Pyomo.MindtPy**: Decomposition-based MINLP

### Applications

- Process synthesis (select equipment + optimize operating conditions)
- Network design with nonlinear flows
- Discrete optimization with nonlinear physics

---

## 8. Constraint Programming (CP)

### Definition

Solve problems with **logical and combinatorial constraints** using:
- Domain propagation
- Constraint inference
- Backtracking search

### Characteristics

- **Declarative**: Specify what constraints must hold
- **Logical constraints**: All-different, precedence, no-overlap, cumulative
- **Finite domains**: Variables take values from finite sets
- **Different paradigm**: Not mathematical programming

### Algorithms

1. **Domain Propagation**: Remove values inconsistent with constraints
2. **Constraint Propagation**: Infer new constraints from existing
3. **Backtracking Search**: Try variable assignments, backtrack if infeasible

### Applications

- Job shop scheduling
- Employee rostering and timetabling
- Resource-constrained project scheduling
- Configuration problems
- Puzzles (Sudoku, N-queens)

### Python Libraries

- **OR-Tools CP-SAT**: Best-in-class, MiniZinc Challenge winner
- **python-constraint**: Simple CP library
- **Gecode** (via Python bindings): Academic CP solver

---

## 9. Multi-Objective Optimization

### Definition

Multiple objective functions to optimize simultaneously:

```
minimize    [f_1(x), f_2(x), ..., f_k(x)]
subject to  g_i(x) ≤ 0
```

### Pareto Optimality

**Pareto optimal**: Solution where improving one objective worsens another.

**Pareto frontier**: Set of all Pareto optimal solutions.

### Approaches

1. **Weighted Sum**: Minimize `Σ w_i f_i(x)` for weights `w_i`
   - Simple, but cannot find non-convex parts of Pareto frontier

2. **Epsilon-Constraint**: Optimize one objective, constrain others
   - Can find entire Pareto frontier

3. **Evolutionary Algorithms**: Generate population covering Pareto frontier
   - NSGA-II, NSGA-III, MOEAD (in pymoo)

### Applications

- Design optimization (cost vs performance vs weight)
- Portfolio optimization (return vs risk vs liquidity)
- Environmental planning (cost vs emissions vs reliability)
- Engineering trade-offs

### Python Libraries

- **pymoo**: Specialized multi-objective library (NSGA-II, NSGA-III)
- **Pyomo + epsilon-constraint**: Manual implementation
- **CVXPY + weighted sum**: If convex

---

## 10. Stochastic Programming

### Definition

Optimization under uncertainty where uncertain parameters have known probability distributions.

### Two-Stage Formulation

```
minimize    c^T x + E[Q(x, ξ)]
subject to  Ax = b
            x ≥ 0
```

Where:
- **First stage**: Decisions `x` made before uncertainty revealed
- **Second stage**: Recourse decisions after observing random outcome `ξ`
- **Q(x, ξ)**: Optimal value of second-stage problem given `x` and `ξ`

### Solution Methods

- **Sample Average Approximation (SAA)**: Sample scenarios, solve large deterministic problem
- **L-shaped method**: Benders decomposition for two-stage
- **Progressive hedging**: Decomposition by scenario

### Python Libraries

- **Pyomo.PySP**: Stochastic programming extension (deprecated in favor of mpi-sppy)
- **mpi-sppy**: Modern stochastic programming in Pyomo

---

## 11. Robust Optimization

### Definition

Optimize for worst-case performance over uncertain parameters (no probability distribution assumed).

```
minimize    max_{u ∈ U} f(x, u)
subject to  g_i(x, u) ≤ 0  for all u ∈ U
```

Where `U` is uncertainty set (e.g., box, ellipsoid, polyhedron).

### Approaches

1. **Worst-case**: Optimize for worst scenario in uncertainty set
2. **Robust counterpart**: Reformulate as deterministic problem
3. **Affine adaptation**: Decision rules linear in uncertainty

### Python Libraries

- **CVXPY**: Modeling robust constraints with norms
- **Pyomo**: Manual reformulation

---

## 12. Dynamic Optimization / Optimal Control

### Definition

Optimize decisions over time subject to dynamic system equations (differential or difference equations).

**Continuous time**:
```
minimize    ∫ L(x(t), u(t)) dt
subject to  dx/dt = f(x(t), u(t))
            x(0) = x_0
```

**Discrete time**:
```
minimize    Σ L_t(x_t, u_t)
subject to  x_{t+1} = f_t(x_t, u_t)
```

### Methods

1. **Direct Methods**: Discretize time, solve large NLP
2. **Indirect Methods**: Solve optimality conditions (Pontryagin maximum principle)
3. **Dynamic Programming**: Bellman equation (limited to low dimensions)
4. **Model Predictive Control (MPC)**: Solve finite-horizon repeatedly

### Python Libraries

- **GEKKO**: Specialized for dynamic optimization, DAE, MPC
- **Pyomo.DAE**: Differential-algebraic equation extension
- **CasADi** (via Python): Optimal control and NLP

---

## Problem Type Selection Guide

### Decision Questions

1. **Are variables continuous or discrete?**
   - Continuous → LP, QP, NLP, convex
   - Discrete → MILP, CP, combinatorial
   - Mixed → MILP, MINLP

2. **Is objective/constraint nonlinear?**
   - No (all linear) → LP or MILP
   - Yes (nonlinear) → NLP, QP, convex, or MINLP

3. **If nonlinear, is problem convex?**
   - Yes (convex) → Convex optimization (efficient!)
   - No (non-convex) → General NLP (harder)
   - Don't know → Test with CVXPY (DCP analysis)

4. **Are there logical constraints?**
   - Yes (all-different, no-overlap, etc.) → CP
   - No → Mathematical programming

5. **Multiple objectives?**
   - Yes → Multi-objective optimization
   - No → Single-objective

6. **Dynamic system over time?**
   - Yes → Dynamic optimization, optimal control
   - No → Static optimization

7. **Uncertainty?**
   - Stochastic (known distributions) → Stochastic programming
   - Robust (worst-case) → Robust optimization
   - None → Deterministic

### Complexity Hierarchy

```
Easy ← ────────────────────────────────────────────────────────── → Hard

LP → Convex QP → Convex NLP → MILP → Non-convex NLP → MINLP
│                               │
└─ Polynomial-time             └─ NP-hard
```

**Key insight**: Convexity and linearity enable efficient solving. Integer variables and non-convexity add difficulty.

---

## Summary

| Problem Type | Variables | Objective | Constraints | Complexity | Algorithms |
|--------------|-----------|-----------|-------------|------------|------------|
| **LP** | Continuous | Linear | Linear | Polynomial | Simplex, Interior point |
| **MILP** | Integer + Continuous | Linear | Linear | NP-hard | Branch-and-bound, cuts |
| **QP** | Continuous | Quadratic | Linear | Poly (convex), NP-hard (general) | Interior point, active set |
| **SOCP** | Continuous | Linear | SOC | Polynomial | Interior point |
| **SDP** | Matrix (PSD) | Linear | Linear + PSD | Polynomial (slow) | Interior point |
| **NLP** | Continuous | Nonlinear | Nonlinear | Poly (convex), Hard (general) | SQP, Interior point |
| **MINLP** | Integer + Continuous | Nonlinear | Nonlinear | Very hard | Branch-and-bound, decomp |
| **CP** | Discrete | Any | Logical | NP-hard | Propagation, search |

**Problem type determines tool selection.** Identify your problem type first, then choose appropriate library and solver.
