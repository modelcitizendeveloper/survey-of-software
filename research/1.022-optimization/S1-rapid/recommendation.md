# S1-Rapid: Library Selection Recommendations

## Executive Summary

Based on research of Python optimization libraries (PyPI statistics, GitHub activity, documentation quality, and community feedback), selection depends primarily on **problem type**, followed by solver flexibility needs and simplicity requirements.

**Key insight**: Problem type (LP, MILP, NLP, convex) is the dominant selection criterion, not application domain.

## Quick Decision Tree

```
What problem type?
│
├─ Linear/Integer Programming (LP/MILP)?
│  ├─ Simple, one-off problem? → PuLP (easiest)
│  ├─ Need solver flexibility? → Pyomo (20+ solvers)
│  ├─ Production, constraint programming? → OR-Tools (CP-SAT)
│  └─ Already using scipy? → scipy.optimize.linprog (HiGHS backend)
│
├─ Convex Optimization?
│  └─ CVXPY (DCP verification, specialized solvers)
│
├─ Nonlinear Programming (NLP)?
│  ├─ Small-medium scale? → scipy.optimize (BFGS, SLSQP)
│  ├─ Large scale or need solvers? → Pyomo + IPOPT
│  └─ Dynamic optimization / DAE? → GEKKO
│
├─ Multi-Objective?
│  └─ pymoo (Pareto frontier, genetic algorithms)
│
└─ Constraint Programming / Scheduling?
   └─ OR-Tools CP-SAT (best-in-class)
```

## Detailed Recommendations by Scenario

### Scenario 1: Getting Started / Learning
**Recommendation**: **PuLP** (if LP/MILP) or **scipy.optimize** (if continuous)

**Rationale**:
- PuLP: Simplest algebraic modeling for LP/MILP, CBC bundled
- scipy.optimize: Zero installation (part of scipy), good for continuous problems
- Both have gentle learning curves and excellent documentation

**Example**: Student learning optimization, analyst solving occasional problems

### Scenario 2: Rapid Prototyping
**Recommendation**: **scipy.optimize** (continuous) or **PuLP** (discrete)

**Rationale**:
- Fast to code, minimal boilerplate
- Good for experiments and proof-of-concept
- Can graduate to more powerful tools later

**Example**: Researcher testing optimization approach, data scientist exploring models

### Scenario 3: Production LP/MILP
**Recommendation**: **OR-Tools** or **Pyomo + HiGHS/Gurobi**

**Rationale**:
- OR-Tools: Google-maintained, bundled solvers, excellent performance (CP-SAT), production-ready
- Pyomo + HiGHS: Open-source, competitive performance, flexible
- Pyomo + Gurobi: Maximum performance if license available

**Example**: Logistics optimization service, resource allocation system, production planning application

### Scenario 4: Convex Optimization
**Recommendation**: **CVXPY**

**Rationale**:
- Automatic convexity verification (DCP analysis)
- Specialized solvers for convex problems
- Standard tool for machine learning, portfolio optimization, signal processing

**Example**: Portfolio optimization, Lasso/ridge regression, SVM training, control systems

### Scenario 5: Nonlinear Programming
**Recommendation**: **scipy.optimize** (small-medium) or **Pyomo + IPOPT** (large)

**Rationale**:
- scipy.optimize: Built-in, good algorithms (BFGS, trust-region), handles constraints
- Pyomo + IPOPT: Large-scale NLP, more solver options, algebraic modeling

**Example**: Parameter estimation, engineering design optimization, calibration against simulation

### Scenario 6: Scheduling / Combinatorial
**Recommendation**: **OR-Tools CP-SAT**

**Rationale**:
- Best-in-class constraint programming solver
- Specialized for scheduling, sequencing, assignment
- MiniZinc Challenge winner

**Example**: Job shop scheduling, employee rostering, task assignment, timetabling

### Scenario 7: Vehicle Routing
**Recommendation**: **OR-Tools routing module**

**Rationale**:
- Specialized routing solvers
- Rich constraint modeling (time windows, capacities, precedence)
- Tuned metaheuristics

**Example**: Delivery routing, technician dispatch, field service optimization

### Scenario 8: Academic Research / Multi-Solver Comparison
**Recommendation**: **Pyomo**

**Rationale**:
- 20+ solver backends (most flexible)
- Same model code across different solvers
- Extensive features (stochastic, disjunctive, DAE)
- Academic standard

**Example**: Comparing MILP solvers, testing problem formulations, operations research research

### Scenario 9: Maximum MILP Performance
**Recommendation**: **Gurobi** (direct API) or **CPLEX** (direct API)

**Rationale**:
- Fastest commercial solvers for large-scale MILP
- Direct API (gurobipy, docplex) avoids modeling language overhead
- Worth cost for time-critical, large-scale problems

**Example**: Large-scale logistics (100k+ variables), real-time optimization with tight deadlines

### Scenario 10: Multi-Objective Optimization
**Recommendation**: **pymoo**

**Rationale**:
- Only library specialized for multi-objective
- Generates Pareto frontier
- Modern evolutionary algorithms (NSGA-II, NSGA-III, MOEAD)

**Example**: Design optimization with competing objectives, trade-off analysis

### Scenario 11: Dynamic Optimization / Optimal Control
**Recommendation**: **GEKKO** or **Pyomo.DAE**

**Rationale**:
- GEKKO: Specialized for dynamic optimization, MPC, DAE systems
- Pyomo.DAE: Integrates with Pyomo ecosystem

**Example**: Process control, trajectory optimization, model predictive control

### Scenario 12: Already Using SciPy/NumPy
**Recommendation**: **scipy.optimize** (first), consider **CVXPY** if convex

**Rationale**:
- Zero additional dependencies
- Integrates with existing scipy/numpy code
- Good default for scientific computing workflows

**Example**: Scientific computing pipelines, data analysis notebooks

## Library Comparison Matrix

| Library | Problem Types | Difficulty | Solver Flexibility | Performance | Best For |
|---------|--------------|------------|-------------------|-------------|----------|
| **scipy.optimize** | LP, NLP | ⭐ Easy | ⭐ Low (HiGHS for LP only) | ⭐⭐ Good | Continuous, prototyping, scipy users |
| **OR-Tools** | LP, MILP, CP, VRP | ⭐⭐ Moderate | ⭐⭐ Medium (bundled) | ⭐⭐⭐ Excellent | Production, scheduling, routing |
| **Pyomo** | LP, MILP, NLP, MINLP | ⭐⭐ Moderate | ⭐⭐⭐ High (20+ solvers) | ⭐⭐ Good | Multi-solver research, complex models |
| **CVXPY** | Convex (LP, QP, SOCP, SDP) | ⭐⭐ Moderate | ⭐⭐ Medium | ⭐⭐⭐ Excellent | Convex optimization, ML, finance |
| **PuLP** | LP, MILP | ⭐ Easy | ⭐⭐ Medium | ⭐⭐ Good | Simple LP/MILP, learning |
| **GEKKO** | NLP, MINLP, DAE | ⭐⭐⭐ Advanced | ⭐⭐ Medium | ⭐⭐ Good | Dynamic optimization, MPC |
| **pymoo** | Multi-objective | ⭐⭐ Moderate | N/A | ⭐⭐ Good | Multi-objective, evolutionary |

## Problem Type → Library Mapping

| Problem Type | First Choice | Alternative | Commercial Option |
|--------------|-------------|-------------|-------------------|
| **LP** | PuLP, scipy.optimize.linprog | Pyomo + HiGHS | Gurobi, CPLEX |
| **MILP** | PuLP, OR-Tools | Pyomo + CBC/SCIP | Gurobi, CPLEX |
| **QP (convex)** | CVXPY | Pyomo + Gurobi | Gurobi, MOSEK |
| **NLP (small)** | scipy.optimize | - | - |
| **NLP (large)** | Pyomo + IPOPT | GEKKO | KNITRO, SNOPT |
| **MINLP** | Pyomo + SCIP | GEKKO | BARON |
| **Convex** | CVXPY | - | MOSEK |
| **CP** | OR-Tools CP-SAT | - | - |
| **Multi-objective** | pymoo | - | - |
| **Dynamic** | GEKKO | Pyomo.DAE | - |

## Solver Selection Guidance

### Open-Source Solvers (Free)

**Linear Programming:**
- **HiGHS**: Rising star, adopted by SciPy and MATLAB. Fast, MIT license.
- **GLPK**: Mature, widely available. Slower than HiGHS.
- **CLP**: COIN-OR, good quality.

**Mixed-Integer:**
- **SCIP**: Fastest academic solver. Now Apache 2.0 (was academic-only).
- **CBC**: COIN-OR, bundled with PuLP. Solid performance.
- **HiGHS**: Also does MILP (not just LP).

**Nonlinear:**
- **IPOPT**: Interior point, large-scale. EPL license.
- **Bonmin**, **Couenne**: MINLP solvers. Academic use.

**Constraint Programming:**
- **OR-Tools CP-SAT**: Best-in-class. Apache 2.0.

**Convex:**
- **Clarabel**: Modern, Rust-based. Default in CVXPY.
- **SCS**: Robust, medium accuracy.
- **OSQP**: Fast for QP.

### Commercial Solvers (Licensed)

**When to consider**:
- Large-scale MILP (100k+ variables)
- Time-critical applications
- Maximum performance needed
- Budget available

**Top choices**:
- **Gurobi**: Fastest overall, excellent support, free for academics
- **CPLEX**: IBM, strong on high-dimensionality, free for academics
- **MOSEK**: Best for conic (SOCP, SDP), free for academics

**Cost vs benefit**: For small-medium problems, open-source competitive. For very large or time-critical, commercial worth cost.

## Common Migration Paths

### 1. Learning → Production
**Path**: PuLP → OR-Tools or Pyomo + HiGHS

**Rationale**: Start simple with PuLP, graduate to production-grade tools as needs grow.

### 2. Prototype → Scale
**Path**: scipy.optimize → Pyomo + IPOPT → Pyomo + commercial NLP solver

**Rationale**: Prototype with scipy, add algebraic modeling for complexity, scale to commercial for performance.

### 3. Open-Source → Commercial
**Path**: Pyomo + CBC → Pyomo + Gurobi (same model code!)

**Rationale**: Develop with open-source, deploy with commercial for performance. Pyomo makes this seamless.

### 4. General → Specialized
**Path**: Pyomo → CVXPY (if convex) or OR-Tools CP-SAT (if scheduling)

**Rationale**: Recognize problem structure, use specialized tool.

## Anti-Recommendations

### ❌ Don't use scipy.optimize for:
- Integer variables (no MILP support)
- Large-scale LP (use HiGHS via Pyomo or scipy.optimize.linprog)

### ❌ Don't use PuLP for:
- Nonlinear problems (no NLP support)
- Constraint programming (no CP support)

### ❌ Don't use CVXPY for:
- Non-convex problems (DCP will reject)
- Integer programming (limited support)

### ❌ Don't use OR-Tools for:
- Nonlinear programming (no NLP support)
- If algebraic modeling strongly preferred (Pyomo better)

### ❌ Don't use Pyomo for:
- Simple one-off problems (overhead not worth it)
- Constraint programming (OR-Tools CP-SAT better)

### ❌ Don't use commercial solvers for:
- Small problems (overkill)
- Budget-constrained projects (open-source competitive)
- Academic use without free license

## Final Recommendations Summary

### **Default Starting Points**

1. **LP/MILP**: Start with **PuLP** (easiest)
2. **Convex**: Use **CVXPY** (DCP verification)
3. **Continuous NLP**: Use **scipy.optimize** (built-in)
4. **Scheduling**: Use **OR-Tools CP-SAT** (best-in-class)
5. **Multi-objective**: Use **pymoo** (specialized)

### **When to Graduate to More Powerful Tools**

- PuLP → **Pyomo** when need solver flexibility or complex models
- scipy.optimize → **Pyomo + IPOPT** when NLP gets large
- Open-source → **Commercial** when performance critical (Gurobi, CPLEX)

### **Production Deployments**

- **OR-Tools**: Safest choice (Google-backed, bundled solvers, proven)
- **Pyomo + HiGHS/Gurobi**: Strong alternative with solver flexibility
- **CVXPY**: If convex problems (finance, ML, control)

### **Academic Research**

- **Pyomo**: Standard for operations research (20+ solvers, extensive features)
- **CVXPY**: Standard for convex optimization (Stanford, widely cited)
- **OR-Tools**: For constraint programming research

## Surprising Findings from Research

1. **HiGHS adoption**: SciPy and MATLAB both chose HiGHS as default LP/MIP solver. Strong signal of quality.

2. **SCIP now Apache 2.0**: Previously academic-only, now fully open source. Major development for open-source MILP.

3. **Gurobi/CPLEX withdrew from Mittelmann benchmarks**: Reduces transparency. Open-source performance harder to compare.

4. **OR-Tools CP-SAT dominance**: Google's CP-SAT wins MiniZinc Challenge medals, competitive with commercial CP solvers.

5. **CVXPY's DCP is unique**: Only Python library with automatic convexity verification. Killer feature for convex problems.

6. **Pyomo's 20+ solvers**: Far exceeds other modeling languages in flexibility.

7. **PuLP's simplicity**: Still best entry point after 15+ years.

## References

This recommendation is based on:
- Library download statistics (PyPI, conda)
- GitHub metrics (stars, activity, contributors)
- Documentation quality assessment
- Academic publications (JMLR, IEEE Access, Nature Methods)
- Mittelmann benchmark analysis
- Community feedback (Stack Overflow, forums)
- Solver adoption patterns (SciPy, MATLAB)

## Conclusion

**Problem type determines library choice**. Once you know your problem type:

- **LP/MILP**: PuLP (simple) or OR-Tools/Pyomo (production)
- **Convex**: CVXPY
- **NLP**: scipy.optimize (small) or Pyomo (large)
- **CP**: OR-Tools CP-SAT
- **Multi-objective**: pymoo

Start with the simplest tool that fits your problem. Graduate to more powerful tools as needs grow. Pyomo provides migration path from open-source to commercial solvers with same model code.

The Python optimization ecosystem in 2025 is mature, with excellent open-source options competitive with commercial tools for many use cases.
