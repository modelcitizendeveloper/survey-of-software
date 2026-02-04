# S2-Comprehensive: Solver Algorithms

## Overview

Optimization solvers implement algorithms that compute optimal solutions. Understanding algorithm categories helps select appropriate solvers and diagnose performance issues.

## Algorithm Categories by Problem Type

### 1. Linear Programming Algorithms

#### Simplex Method
**Invented**: George Dantzig, 1947

**Principle**: Walk along edges of feasible polyhedron from vertex to vertex, always improving objective.

**Steps**:
1. Start at feasible vertex
2. Identify improving edge (reduced cost < 0)
3. Move to adjacent vertex along edge
4. Repeat until no improving edges exist

**Complexity**:
- Worst-case: Exponential (Klee-Minty cube)
- Average-case: Polynomial (empirically)
- Practical performance: Excellent

**Variants**:
- Primal simplex
- Dual simplex (maintains dual feasibility)
- Revised simplex (matrix form, more efficient)
- Network simplex (specialized for network problems)

**Solvers**: GLPK, CLP, GLOP (Google), Gurobi, CPLEX

#### Interior Point Methods
**Invented**: Karmarkar, 1984 (modern version)

**Principle**: Move through interior of feasible region toward optimum.

**Steps**:
1. Start at interior point
2. Follow central path (points equally far from boundaries)
3. Apply barrier method to penalize boundary violations
4. Converge to optimum on boundary

**Complexity**: Polynomial-time (theory and practice)

**Advantages**:
- Guaranteed polynomial time
- Better for large-scale problems
- Parallelizable

**Disadvantages**:
- More complex implementation
- Does not exploit warm starts as well as simplex

**Solvers**: IPOPT (nonlinear), Gurobi, CPLEX, MOSEK, HiGHS

**When to use**:
- Large-scale LP (100k+ variables)
- When polynomial-time guarantee matters
- Problems without warm start

---

### 2. Mixed-Integer Programming Algorithms

#### Branch-and-Bound
**Principle**: Systematically enumerate solution space using bounds to prune.

**Steps**:
1. Solve LP relaxation (remove integer constraints) → lower bound
2. If solution integer, update incumbent (best known)
3. If fractional, branch: create two subproblems
   - Subproblem 1: Add constraint `x_i ≤ ⌊x_i*⌋`
   - Subproblem 2: Add constraint `x_i ≥ ⌈x_i*⌉`
4. Prune branches where bound ≥ incumbent
5. Repeat until all branches explored or pruned

**Tree structure**:
```
         LP relaxation (3.7, 2.3) → obj = 15.2
        /                              \
    x ≤ 3                              x ≥ 4
   (3, 2.6)                           (4, 1.8)
   obj = 14.8                         obj = 15.5 (prune if incumbent < 15.5)
```

**Node selection strategies**:
- Depth-first: Quickly find feasible solutions
- Best-bound: Prove optimality faster
- Hybrid: Modern solvers use sophisticated strategies

**Variable selection**: Which fractional variable to branch on?
- Most fractional
- Pseudocost branching (estimate impact)
- Strong branching (tentatively solve subproblems)

#### Cutting Planes
**Principle**: Add linear inequalities (cuts) that eliminate fractional solutions without removing integer solutions.

**Types of cuts**:

1. **Gomory cuts**: General integer cuts from simplex tableau
2. **Cover cuts**: For knapsack constraints
3. **Clique cuts**: From conflict graphs
4. **MIR (Mixed-Integer Rounding)**: For mixed-integer constraints
5. **Lift-and-project**: Strengthen constraints
6. **Problem-specific**: Exploit special structure

**Example**: For `x₁ + x₂ ≤ 1.5` with `x₁, x₂ binary`, LP relaxation allows `x₁ = x₂ = 0.75`. Cut `x₁ + x₂ ≤ 1` eliminates this fractional solution.

#### Branch-and-Cut
**Modern standard**: Combine branch-and-bound with cutting planes.

**Process**:
1. Solve LP relaxation
2. Generate cuts to strengthen relaxation
3. Branch if still fractional
4. Apply cuts at each node

**Modern solvers**: Gurobi, CPLEX, SCIP use sophisticated branch-and-cut with:
- Automatic cut generation
- Primal heuristics (find feasible solutions quickly)
- Parallelization
- Presolve (problem reduction)

#### Presolve
**Principle**: Simplify problem before solving.

**Techniques**:
- Remove redundant constraints
- Fix variables (if bounds imply fixed value)
- Tighten bounds
- Detect special structure
- Aggregate variables
- Dual reductions

**Impact**: Can reduce problem size dramatically, sometimes solving problem in presolve.

---

### 3. Nonlinear Programming Algorithms

#### Gradient-Based Methods

**Gradient Descent**:
```
x_{k+1} = x_k - α_k ∇f(x_k)
```
Move in direction of steepest descent. Simple but slow convergence.

**Newton's Method**:
```
x_{k+1} = x_k - [∇²f(x_k)]⁻¹ ∇f(x_k)
```
Use second derivatives (Hessian) for quadratic convergence. Expensive per iteration.

**Quasi-Newton (BFGS, L-BFGS)**:
Approximate Hessian from gradient history. Balance of speed and accuracy.

- **BFGS**: Full Hessian approximation
- **L-BFGS**: Limited-memory variant (for large-scale)

**Advantages**: Fast convergence for smooth problems

**Requirements**: First derivatives (gradients), optionally second derivatives

#### Sequential Quadratic Programming (SQP)
**Principle**: Solve sequence of quadratic programming subproblems.

**Steps**:
1. Approximate objective and constraints with quadratic/linear models
2. Solve QP subproblem for search direction
3. Line search along direction
4. Update approximations
5. Repeat until convergence

**Performance**: Very effective for smooth constrained NLP

**Solvers**: SNOPT, NLPQL, scipy.optimize (SLSQP)

#### Interior Point Methods (Barrier Methods)
**Principle**: Penalize constraint violations with barrier function.

**Barrier function**: `f(x) + μ Σ -log(g_i(x))`

As `μ → 0`, barrier pushes solution toward feasible region boundary.

**Advantages**:
- Handles inequality constraints naturally
- Good for large-scale problems
- Polynomial-time for convex problems

**Solvers**: IPOPT, Knitro

#### Trust Region Methods
**Principle**: Limit step size to region where quadratic model is trusted.

**Steps**:
1. Build quadratic model of objective around current point
2. Solve for step within trust region (radius Δ)
3. Evaluate actual improvement vs predicted
4. If good agreement, accept step and expand trust region
5. If poor agreement, reject step and shrink trust region

**Advantages**: Robust to poor initialization, handles non-smooth regions

**Solvers**: scipy.optimize (trust-constr), TAO

---

### 4. Derivative-Free Optimization

**Use case**: Objective function is black-box, non-smooth, or noisy (e.g., simulation output).

#### Nelder-Mead Simplex
**Principle**: Geometric search using simplex (n+1 points in n dimensions).

**Operations**:
- Reflection: Mirror worst point through centroid
- Expansion: Extend if reflection improves
- Contraction: Shrink if reflection fails
- Shrink: Contract entire simplex

**Advantages**: Robust, no derivatives needed

**Disadvantages**: Slow, can stall, no convergence guarantees

#### Powell's Method
**Principle**: Sequential line searches along conjugate directions.

**Advantages**: More efficient than Nelder-Mead for smooth problems

#### Pattern Search
**Principle**: Evaluate at geometric patterns around current point.

**Mesh adaptive direct search (MADS)**: Theoretical convergence guarantees.

---

### 5. Metaheuristics

**Use case**: Global optimization, non-convex problems, combinatorial problems.

#### Genetic Algorithms
**Principle**: Evolutionary process with selection, crossover, mutation.

**Steps**:
1. Initialize population
2. Evaluate fitness
3. Select parents (roulette wheel, tournament)
4. Crossover (combine parent genes)
5. Mutation (random changes)
6. Replace population
7. Repeat for generations

**Advantages**: Global search, handles non-convex, no derivatives

**Disadvantages**: Many evaluations, no optimality guarantee

#### Simulated Annealing
**Principle**: Probabilistically accept worse solutions to escape local optima.

**Temperature schedule**: Start hot (accept most moves), cool down (become greedy).

**Metropolis criterion**: Accept worse solution with probability `exp(-ΔE/T)`

#### Particle Swarm Optimization
**Principle**: Particles explore space influenced by personal best and swarm best.

**Update rule**:
```
v_{i,t+1} = w·v_{i,t} + c₁·r₁·(p_i - x_{i,t}) + c₂·r₂·(g - x_{i,t})
x_{i,t+1} = x_{i,t} + v_{i,t+1}
```

Where:
- `v_i`: Velocity of particle i
- `p_i`: Personal best of particle i
- `g`: Global best of swarm
- `w, c₁, c₂`: Parameters
- `r₁, r₂`: Random numbers

**Advantages**: Simple, effective for many problems

**Python library**: pymoo, scipy.optimize.differential_evolution

---

### 6. Constraint Programming Algorithms

#### Domain Propagation
**Principle**: Remove values from variable domains that cannot satisfy constraints.

**Arc consistency**: For constraint between x and y, remove values from x's domain that have no supporting value in y's domain.

**Example**: `x + y = 10, x ∈ {1,2,3}, y ∈ {7,8,9}`
After propagation: `x ∈ {1,2,3}, y ∈ {7,8,9}` (already consistent)

If `x ∈ {1,2}, y ∈ {7,8,9,10}` → propagate → `y ∈ {8,9}` (x=1→y=9, x=2→y=8)

#### Backtracking Search
**Principle**: Assign variables sequentially, backtrack when conflict detected.

**With constraint propagation**: Propagate after each assignment to detect conflicts early.

**Heuristics**:
- Variable ordering: Which variable to assign next? (most constrained first)
- Value ordering: Which value to try? (least constraining first)

#### CP-SAT (OR-Tools)
Modern CP solver using Boolean satisfiability (SAT) techniques:
- Encode constraints as Boolean formulas
- Use advanced SAT solver techniques
- Combine with LP relaxation for optimization

**Performance**: Award-winning (MiniZinc Challenge medals)

---

## Algorithm Selection by Problem Type

| Problem Type | Primary Algorithm | Solvers |
|--------------|------------------|---------|
| **LP** | Simplex or Interior Point | HiGHS, GLPK, CLP, Gurobi, CPLEX |
| **MILP** | Branch-and-Cut | CBC, SCIP, HiGHS, Gurobi, CPLEX |
| **Convex QP** | Interior Point | OSQP, MOSEK, Gurobi, CPLEX |
| **Convex NLP** | Interior Point, SQP | IPOPT, Knitro, SNOPT |
| **Non-convex NLP** | SQP, Trust Region, Multi-start | IPOPT (local), BARON (global) |
| **MINLP** | Branch-and-Bound + NLP | SCIP, BARON, Bonmin, Couenne |
| **CP** | Domain Propagation + Search | OR-Tools CP-SAT, Gecode |
| **Global non-convex** | Metaheuristics, Branch-and-Bound | Genetic algorithms, BARON |

---

## Modern Solver Enhancements

### Parallelization
- **Branch-and-bound**: Solve multiple nodes concurrently
- **Portfolio approaches**: Try multiple strategies in parallel
- **Multi-threading**: Modern solvers (Gurobi, CPLEX) use 8-16 cores effectively

### Machine Learning in Solvers
- **Branching heuristics**: Learn variable selection from problem history
- **Cut selection**: Learn which cuts are effective
- **Node selection**: Learn promising branches
- **Warm starting**: Transfer solutions across similar problems

### Automatic Tuning
- **Parameter tuning**: Solvers have 100+ parameters
- **Gurobi Tuning Tool**: Automatically find best parameter settings for problem class

---

## Algorithmic Complexity Summary

| Algorithm | Worst-Case | Average-Case | Practical |
|-----------|-----------|--------------|-----------|
| **Simplex** | Exponential | Polynomial | Excellent |
| **Interior Point** | Polynomial | Polynomial | Very good |
| **Branch-and-Bound** | Exponential | Varies | Good with cuts |
| **SQP** | N/A (iterative) | Superlinear | Excellent (smooth NLP) |
| **IPOPT** | Polynomial (convex) | Varies | Very good |
| **Genetic Algorithms** | N/A | N/A | Depends on problem |

---

## Key Insights

1. **Simplex vs Interior Point**: Simplex better for small-medium LP, interior point for large-scale. Simplex exploits warm starts better.

2. **Cuts are critical for MILP**: Modern MILP performance comes from sophisticated cutting plane generation, not just branch-and-bound.

3. **Convexity enables efficiency**: Convex problems have polynomial-time algorithms. Non-convex may require global optimization methods.

4. **Derivatives matter**: Gradient-based NLP algorithms much faster than derivative-free for smooth problems. Use automatic differentiation.

5. **Presolve can be transformative**: Sometimes reduces problem to trivial size.

6. **Metaheuristics don't guarantee optimality**: But useful for hard non-convex problems where local methods fail.

7. **CP excels at scheduling**: Domain propagation very effective for combinatorial structure (no-overlap, all-different).

8. **Algorithm choice impacts performance 10-1000x**: Choosing right algorithm/solver for problem type is critical.

## References

- Nocedal & Wright, "Numerical Optimization" (2006)
- Wolsey, "Integer Programming" (2020)
- Boyd & Vandenberghe, "Convex Optimization" (2004)
- Biegler, "Nonlinear Programming" (2010)
