# S2-Comprehensive: Solver Performance Comparison

## Overview

Solver performance varies dramatically based on problem type, size, and structure. This document summarizes benchmark findings and performance characteristics.

## Key Finding: Commercial Withdrawal from Public Benchmarks

**Major development (2024)**: Gurobi (August 2024) and MindOpt (December 2024) withdrew from Mittelmann benchmarks, reducing transparency in commercial vs open-source comparison.

## Mittelmann Benchmarks

**Source**: Hans Mittelmann, Arizona State University (plato.asu.edu/bench.html)

**Coverage**:
- Mixed-integer linear programming (MILP)
- Linear programming (LP)
- Network optimization
- Nonlinear programming (NLP)
- Semidefinite programming (SDP)

**Interactive visualizations**: mattmilten.github.io/mittelmann-plots (shows pairwise time comparisons)

**Status (2025)**: Gurobi and MindOpt results removed. Remaining solvers: SCIP, HiGHS, CBC, GLPK, Xpress, others.

## MILP Performance Tiers (Pre-Withdrawal Era)

### Tier 1: Premium Commercial
**Before withdrawal, Gurobi and CPLEX were**:
- 5-10x faster than open-source on large instances
- Most consistent across problem classes
- **Cost**: $10k-100k+ annually (enterprise)
- **Academic**: Free

**When justified**:
- Large-scale instances (100k+ variables, 10k+ integer)
- Time-critical applications (real-time optimization)
- Mission-critical production systems

### Tier 2: Open-Source Leaders
**SCIP (now Apache 2.0)**:
- Fastest open-source MILP solver
- Competitive with commercial on many problems
- Active development

**HiGHS**:
- Rising star (adopted by SciPy 1.6.0+, MATLAB)
- Excellent LP performance
- Good MILP performance
- MIT license, no dependencies

**CBC (COIN-OR)**:
- Mature, stable
- Bundled with PuLP
- 2-5x slower than SCIP on average
- Good for small-medium problems

### Tier 3: Basic Open-Source
**GLPK**:
- Widely available
- Slower than CBC/SCIP/HiGHS
- Suitable for small problems (<10k variables)

## LP Performance

**HiGHS**: Competitive with commercial solvers
- Chosen by SciPy and MATLAB as default LP solver
- Signal of high quality

**GLOP** (Google, in OR-Tools): Good performance for LP

**Commercial** (Gurobi, CPLEX): Still faster on very large instances, but gap narrowed significantly with HiGHS.

## NLP Performance

### Open-Source
**IPOPT** (Interior Point OPTimizer):
- Standard open-source NLP solver
- Large-scale capable (10k+ variables)
- Requires linear algebra libraries (HSL, MUMPS, Pardiso)
- Finds local optima (non-convex problems)

### Commercial
**Knitro**: Premium NLP solver (Artelys)
- Multiple algorithms (interior point, SQP, active set)
- Faster than IPOPT on many problems
- $5k-50k+ annually

**SNOPT**: Academic/commercial
- Sparse NLP
- Used in aerospace, engineering

**Performance gap**: Commercial 2-10x faster than IPOPT for large-scale NLP, but IPOPT excellent for open-source.

## Convex Optimization Performance

### SOCP/SDP
**MOSEK**: Commercial, best performance for conic problems
- Free for academic use
- Industry standard for SOCP/SDP

**Open-source**:
- **SCS**: Robust, medium accuracy
- **ECOS**: Good for small-medium SOCP
- **Clarabel**: Modern (Rust), becoming default in CVXPY

**Performance**: MOSEK 2-5x faster, but open-source sufficient for many applications.

## Constraint Programming

**OR-Tools CP-SAT**: Award-winning
- MiniZinc Challenge medals (2018, 2019, 2020, 2021)
- Competitive with commercial CP solvers
- Free, open-source (Apache 2.0)

**Commercial CP**:
- IBM CPLEX CP Optimizer
- Gecode

**Performance**: CP-SAT competitive, sometimes superior.

## Problem Size Scaling

### LP
- **Small** (<1k variables): All solvers fast (<1 second)
- **Medium** (1k-100k): HiGHS, commercial excel
- **Large** (100k-1M+): Interior point methods (HiGHS, Gurobi, CPLEX) scale better than simplex

### MILP
- **Small** (<100 integer vars): All solvers acceptable
- **Medium** (100-10k integer): SCIP, HiGHS, commercial
- **Large** (10k+ integer): Commercial formerly dominated (before withdrawal); SCIP best open-source

### NLP
- **Small** (<100 vars): scipy.optimize sufficient
- **Medium** (100-10k): IPOPT, commercial
- **Large** (10k+): IPOPT, Knitro, SNOPT

**Key insight**: Problem size alone doesn't determine hardness. Structure matters more (e.g., network flow LP with 1M variables easier than general MILP with 1k integer variables).

## Formulation Impact on Performance

**Example**: Same problem, different formulations can solve 10-1000x faster.

**Tight formulation**: LP relaxation close to integer hull
- Fewer branch-and-bound nodes
- Faster solve

**Weak formulation**: LP relaxation loose
- Many nodes explored
- Slow solve

**Techniques to improve formulation**:
- Disaggregation (break large constraints)
- Symmetry breaking (eliminate symmetric solutions)
- Valid inequalities (tighten relaxation)
- Alternative variable representations

**Impact often exceeds solver choice**: Well-formulated problem on CBC can solve faster than poorly-formulated on Gurobi.

## Practical Performance Factors

### 1. Presolve
Modern solvers spend significant time in presolve:
- Can eliminate 50-90% of variables/constraints
- Sometimes solves problem entirely
- Usually worth the time

### 2. Warm Starting
**MILP**: Providing known feasible solution speeds up solving
**NLP**: Good initial guess critical for non-convex

### 3. Parallelization
**MILP**: Scales well to 4-8 cores, diminishing returns beyond 16
**NLP**: Limited parallelization (inherently sequential)

### 4. Tolerances
Relaxing optimality/feasibility tolerances (e.g., 1% vs 0.01%) can yield 10x speedup.

### 5. Time Limits
For large MILP, setting time limit and accepting near-optimal solution often practical.

## Benchmark Caveats

1. **Problem-dependent**: Solver rankings vary by problem class
2. **Version-dependent**: Solvers improve continuously
3. **Tuning**: Default parameters may not be optimal
4. **Hardware**: Benchmark hardware may differ from yours
5. **Withdrawn solvers**: Gurobi/CPLEX performance no longer publicly tracked

## Python Library Overhead

**Modeling language overhead typically <10% of solve time** for large problems.

**Direct API vs modeling language**:
- gurobipy (direct) slightly faster than Pyomo+Gurobi
- Matters for tiny problems (<1s solve) or many sequential solves
- For large problems (>10s), solver dominates

**Recommendation**: Use algebraic modeling (Pyomo, CVXPY, PuLP) unless profiling shows bottleneck.

## Performance Recommendations by Problem Type

| Problem Type | Open-Source | Commercial | Comment |
|--------------|-------------|------------|---------|
| **LP** | HiGHS, GLOP | Gurobi, CPLEX | Gap narrowed significantly |
| **MILP (small-medium)** | SCIP, HiGHS, CBC | Gurobi, CPLEX | Open-source acceptable |
| **MILP (large)** | SCIP | Gurobi, CPLEX | Commercial faster (historically) |
| **Convex QP** | OSQP | Gurobi, MOSEK | Open-source good |
| **NLP** | IPOPT | Knitro, SNOPT | IPOPT very capable |
| **SOCP/SDP** | SCS, ECOS | MOSEK | MOSEK best |
| **CP** | OR-Tools CP-SAT | CPLEX CP | CP-SAT award-winning |
| **Global MINLP** | SCIP, Couenne | BARON | All slow (hard problem) |

## When Commercial Solvers Worth the Cost

1. **Very large MILP**: 100k+ variables, 10k+ integer
2. **Time-critical**: Real-time optimization, tight deadlines
3. **ROI justifies**: If optimization saves $100k+, $10k solver cost trivial
4. **Support needed**: Commercial provides professional support

## When Open-Source Sufficient

1. **Small-medium problems**: Open-source competitive
2. **Budget constraints**: Free vs $10k-100k
3. **Academic/research**: Test multiple solvers
4. **HiGHS/SCIP for LP/MILP**: Closing performance gap

## Testing Methodology

To compare solvers on YOUR problems:

```python
import time
from pyomo.environ import *

def solve_with_solver(model, solver_name):
    solver = SolverFactory(solver_name)
    start = time.time()
    result = solver.solve(model, tee=False)
    elapsed = time.time() - start
    return elapsed, result

# Test multiple solvers
for solver in ['glpk', 'cbc', 'scip', 'gurobi']:
    elapsed, result = solve_with_solver(model, solver)
    print(f"{solver}: {elapsed:.2f}s, obj={value(model.obj)}")
```

**Important**: Test on YOUR problem instances, not just benchmarks.

## Key Takeaways

1. **HiGHS emergence**: Major development in open-source landscape (SciPy, MATLAB adoption)
2. **SCIP now Apache 2.0**: Eliminates licensing barrier for best open-source MILP
3. **CP-SAT excellence**: OR-Tools CP-SAT world-class for scheduling
4. **Commercial gap varies**: Large for giant MILP, small for LP/medium MILP
5. **Formulation matters more than solver**: Good formulation on CBC > bad formulation on Gurobi
6. **Benchmark withdrawal reduces transparency**: Harder to compare commercial vs open-source

## References

- Mittelmann Benchmarks: plato.asu.edu/bench.html
- Interactive visualizations: mattmilten.github.io/mittelmann-plots
- MIPLIB: miplib.zib.de (problem library)
- HiGHS paper: Huangfu & Hall, 2018
- SCIP Optimization Suite 9.0: Optimization Online 2024
