# S4-Strategic: Solver Landscape 2025

## Open-Source Solver Status

### Linear Programming (LP)

**HiGHS** (MIT License)
- **Status**: Rising star, production-ready
- **Adoption**: SciPy 1.6.0+, MATLAB default
- **Performance**: Competitive with commercial
- **Algorithms**: Dual simplex, primal simplex, interior point
- **Assessment**: Best open-source LP solver

**CLP** (Coin-OR, EPL)
- **Status**: Mature, stable
- **Performance**: Good, slower than HiGHS
- **Part of**: COIN-OR optimization suite

**GLPK** (GPL)
- **Status**: Widely available, basic performance
- **Use case**: Small problems, availability matters
- **Limitation**: GPL license (copyleft)

### Mixed-Integer Linear Programming (MILP)

**SCIP** (Apache 2.0 since v9.0)
- **Status**: Fastest academic MILP solver
- **Major development**: Now fully open-source (was academic-only)
- **Performance**: Competitive with commercial on many problems
- **Also handles**: MINLP
- **Assessment**: Best open-source MILP

**CBC** (COIN-OR, EPL)
- **Status**: Mature, widely used
- **Bundled with**: PuLP
- **Performance**: 2-5x slower than SCIP, adequate for small-medium
- **Reliability**: Very stable

**HiGHS** (MIT)
- **Status**: Also does MILP (not just LP)
- **Performance**: Good, improving
- **Advantage**: Same solver for LP and MILP

### Nonlinear Programming (NLP)

**IPOPT** (EPL)
- **Status**: Standard open-source NLP solver
- **Algorithm**: Interior point
- **Scale**: Large-scale capable
- **Dependencies**: Requires linear algebra library (HSL, MUMPS, Pardiso)
- **Assessment**: Industry standard for open-source NLP
- **Limitation**: Local optima (non-convex problems)

**Bonmin**, **Couenne** (EPL)
- **Focus**: MINLP (mixed-integer nonlinear)
- **Status**: Academic, slower
- **Use case**: When MINLP required and commercial not available

### Convex Optimization

**Clarabel** (Apache 2.0)
- **Language**: Rust
- **Status**: Modern, becoming CVXPY default
- **Handles**: SOCP, SDP, QP

**SCS** (MIT)
- **Focus**: Conic optimization
- **Robustness**: Very robust, medium accuracy
- **Use case**: Large-scale conic problems

**OSQP** (Apache 2.0)
- **Focus**: Quadratic programming (QP)
- **Performance**: Very fast for QP
- **Use case**: Model predictive control, embedded

**ECOS** (GPL)
- **Focus**: Second-order cone programming (SOCP)
- **Performance**: Fast for small-medium SOCP

### Constraint Programming

**OR-Tools CP-SAT** (Apache 2.0)
- **Developer**: Google
- **Status**: Award-winning (MiniZinc Challenge medals)
- **Performance**: Competitive with commercial CP solvers
- **Assessment**: Best-in-class open-source CP

---

## Commercial Solver Status

### MILP Leaders

**Gurobi**
- **Pricing**: ~$10k-100k+/year (enterprise), free (academic)
- **Performance**: Historically fastest MILP
- **Benchmark status**: Withdrew August 2024
- **Support**: Excellent professional support
- **Adoption**: Wide industry use

**CPLEX** (IBM)
- **Pricing**: Similar to Gurobi
- **Performance**: Competitive with Gurobi
- **Strengths**: High-dimensionality, non-convex MIQP
- **Benchmark status**: Still participates
- **Enterprise**: IBM support and integration

**Xpress** (FICO)
- **Pricing**: Similar tier
- **Performance**: Competitive
- **Features**: Mosel modeling language

### NLP Specialists

**KNITRO** (Artelys)
- **Pricing**: $5k-50k/year
- **Performance**: 2-10x faster than IPOPT on many problems
- **Algorithms**: Interior point, SQP, active set
- **Use case**: Large-scale nonlinear

**SNOPT** (Stanford)
- **Focus**: Sparse NLP
- **Academic roots**: Stanford research
- **Adoption**: Aerospace, engineering

### Conic Optimization

**MOSEK**
- **Pricing**: $5k-50k/year, free (academic)
- **Focus**: SOCP, SDP, conic optimization
- **Performance**: Significantly faster than open-source for conic
- **Assessment**: Best commercial conic solver

### Global MINLP

**BARON**
- **Focus**: Global MINLP solver
- **Algorithm**: Branch-and-reduce
- **Performance**: Slow (problem is hard), but finds global optima
- **Use case**: When global optimum required for non-convex

---

## Solver Selection by Problem Type

| Problem | Open-Source Leader | Commercial Leader | Gap |
|---------|-------------------|------------------|-----|
| **LP** | HiGHS | Gurobi, CPLEX | Narrow |
| **MILP (small-medium)** | SCIP, HiGHS | Gurobi, CPLEX | Medium |
| **MILP (large)** | SCIP | Gurobi, CPLEX | Wide |
| **NLP** | IPOPT | Knitro, SNOPT | Medium |
| **Convex conic** | Clarabel, SCS | MOSEK | Wide |
| **CP** | OR-Tools CP-SAT | CPLEX CP | Narrow |
| **Global MINLP** | SCIP, Couenne | BARON | Medium |

---

## Major Developments (2020-2025)

1. **HiGHS adoption** (2021): SciPy, MATLAB → production validation
2. **SCIP Apache 2.0** (2024): Removed licensing barrier
3. **Gurobi/MindOpt withdrawal** (2024): Benchmark transparency reduced
4. **OR-Tools CP-SAT awards** (2018-2021): Best-in-class CP
5. **Clarabel emergence** (2023-2024): Modern Rust-based conic solver

---

## Performance Trends

**Open-source improving**:
- HiGHS: LP competitive with commercial
- SCIP: MILP gap narrowing
- CP-SAT: CP competitive/superior to commercial

**Commercial maintaining edge**:
- Very large MILP (100k+ variables, 10k+ integer)
- Conic optimization (MOSEK >> open-source)
- Professional support and features

**Inflection point**: Medium-scale problems (<10k integer variables) now often solvable with open-source.

---

## Licensing Landscape

### Open-Source Licenses
- **MIT** (HiGHS, SCS, OSQP): Most permissive
- **Apache 2.0** (SCIP, OR-Tools, Clarabel): Permissive, patent protection
- **EPL** (IPOPT, CBC, CLP, Bonmin, Couenne): Weak copyleft
- **GPL** (GLPK, ECOS): Strong copyleft (limits commercial use)

### Commercial Licenses
- **Named-user**: Per-person
- **Floating**: Shared pool
- **Cloud/Usage-based**: Pay per solve
- **Academic**: Free but restricted to research/teaching

---

## Future Outlook

### Likely Developments
1. **Continued open-source strengthening**: SCIP, HiGHS performance improvements
2. **ML integration**: Learned heuristics in solvers
3. **Cloud-native**: Optimization-as-a-service
4. **GPU acceleration**: MILP on GPUs (early stage)
5. **Quantum**: Long-term (10+ years)

### Open Questions
1. **Will commercial performance gap close completely?** (Probably not, but threshold rising)
2. **Will Gurobi/CPLEX return to public benchmarks?** (Unknown)
3. **Will more companies adopt open-source for production?** (Likely yes)

---

## Recommendations

### For Most Users
**Start with open-source**:
- LP: HiGHS
- MILP: SCIP or HiGHS
- NLP: IPOPT
- Convex: CVXPY with Clarabel/SCS
- CP: OR-Tools CP-SAT

### Upgrade to Commercial When
- Very large MILP (>100k variables, >10k integer)
- Conic optimization (MOSEK)
- Professional support needed
- ROI justifies cost

### Academic Users
- Free commercial licenses available
- Test both open-source and commercial
- Report both for reproducibility

---

## Key Insight

**Solver landscape in 2025 favors open-source** for many use cases. HiGHS, SCIP, IPOPT, and OR-Tools are production-ready and competitive. Commercial solvers maintain edge on largest problems and provide professional support, but threshold for "need commercial" has risen significantly.

**Strategic recommendation**: Build on open-source, upgrade to commercial only when profiling demonstrates clear performance need. Pyomo enables seamless migration.
