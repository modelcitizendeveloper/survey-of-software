# S2-Comprehensive: Commercial vs Open-Source Solvers

## Performance Gap Analysis

### Historical Context (Pre-2024)
Commercial solvers (Gurobi, CPLEX) were 5-10x faster than open-source on large MILP instances

### Current Status (2025)
**Major shift**: Gurobi and MindOpt withdrew from Mittelmann benchmarks (Aug/Dec 2024), reducing transparency

## Open-Source Solvers

### HiGHS (MIT License)
**Adoption signal**: Chosen as default LP/MIP solver by:
- SciPy 1.6.0+ (2021)
- MATLAB Optimization Toolbox

**Performance**: Competitive with commercial on LP, good on MILP
**Conclusion**: Rising star, closing performance gap

### SCIP (Apache 2.0, since v9.0)
**Status**: Fastest academic MILP/MINLP solver
**Previous barrier**: Academic-only license
**Now**: Fully open-source (Apache 2.0)
**Performance**: Competitive with commercial on many problems

### IPOPT (EPL)
**Focus**: Large-scale nonlinear programming
**Performance**: Industry standard open-source NLP solver
**Limitation**: Local optima only (non-convex problems)

### CBC (EPL)
**Maturity**: 15+ years
**Bundled**: PuLP default
**Performance**: 2-5x slower than SCIP, adequate for small-medium MILP

## Commercial Solvers

### Gurobi
**Pricing**: ~$10k-100k+/year (enterprise)
**Academic**: Free
**Performance**: Historically fastest MILP solver
**Benchmark status**: Withdrew August 2024

### CPLEX (IBM)
**Pricing**: Similar to Gurobi
**Academic**: Free
**Strengths**: High-dimensionality problems, non-convex MIQP
**Benchmark status**: Still participates

### MOSEK
**Focus**: Conic optimization (SOCP, SDP)
**Pricing**: ~$5k-50k/year
**Academic**: Free
**Assessment**: Best commercial option for conic problems

### KNITRO (Artelys)
**Focus**: Nonlinear programming
**Performance**: 2-10x faster than IPOPT on many NLP
**Pricing**: $5k-50k/year

## When Commercial Worth Cost

### Clear Justifications:
1. **Very large MILP**: 100k+ variables, 10k+ integer variables
2. **Time-critical production**: Real-time optimization, tight SLAs
3. **ROI analysis**: If optimization saves $100k+/year, $10k solver cost justified
4. **Professional support**: Mission-critical applications need vendor support

### Questionable:
1. **Small-medium problems**: Open-source competitive
2. **Research/exploration**: Need flexibility more than maximum speed
3. **Budget constraints**: $10k-100k is significant

## Academic vs Industry Access

### Academic Advantages:
- **Free commercial licenses**: Gurobi, CPLEX, MOSEK free for academic use
- **Full functionality**: No feature limitations
- **Ideal for research**: Test multiple solvers

### Industry Reality:
- **Must pay**: Commercial licenses expensive
- **Open-source competitive**: HiGHS, SCIP often sufficient
- **Hybrid approach**: Develop with open-source, deploy with commercial if needed

## Cost Comparison

| Solver | License | Annual Cost (Enterprise) | Academic |
|--------|---------|-------------------------|----------|
| **HiGHS** | MIT | Free | Free |
| **SCIP** | Apache 2.0 | Free | Free |
| **CBC** | EPL | Free | Free |
| **IPOPT** | EPL | Free | Free |
| **Gurobi** | Commercial | $10k-100k+ | Free |
| **CPLEX** | Commercial | $10k-100k+ | Free |
| **MOSEK** | Commercial | $5k-50k | Free |
| **KNITRO** | Commercial | $5k-50k | Free |

## Performance Tiers (Based on Historical Data)

### LP
1. **Tier 1**: HiGHS, Gurobi, CPLEX (gap narrowed)
2. **Tier 2**: GLOP, CLP
3. **Tier 3**: GLPK

### MILP
1. **Tier 1**: Gurobi, CPLEX (historically)
2. **Tier 2**: SCIP (best open-source)
3. **Tier 3**: HiGHS, CBC
4. **Tier 4**: GLPK

### NLP
1. **Tier 1**: KNITRO, SNOPT
2. **Tier 2**: IPOPT (excellent for open-source)

### Convex Conic
1. **Tier 1**: MOSEK
2. **Tier 2**: Clarabel, SCS, ECOS

## Open-Source Advantages

1. **Cost**: Free (obviously)
2. **Transparency**: Source code available
3. **Community**: Active development, bug reporting
4. **Flexibility**: Modify if needed
5. **No licensing**: No license servers, floating licenses, compliance issues

## Commercial Advantages

1. **Performance**: Still faster on largest instances
2. **Support**: Professional support contracts
3. **Features**: Advanced tuning, cloud, distributed solving
4. **Testing**: Extensive QA, stability guarantees

## Trend: Closing Gap

**Evidence**:
- HiGHS adoption by SciPy, MATLAB
- SCIP now Apache 2.0 (removed licensing barrier)
- OR-Tools CP-SAT award-winning (beats commercial CP)

**Implication**: Open-source increasingly viable for production

## Recommendations

### Start with Open-Source:
- HiGHS (LP/MILP)
- SCIP (MILP/MINLP)
- IPOPT (NLP)
- OR-Tools (CP, routing)
- CVXPY with open solvers (convex)

### Upgrade to Commercial When:
- Profiling shows solver is bottleneck
- Problem size requires maximum performance
- Budget justifies cost (ROI positive)
- Professional support needed

### Migration Path:
Use Pyomo for seamless open-source → commercial migration:
```python
# Development
solver = SolverFactory('scip')

# Production (same model code!)
solver = SolverFactory('gurobi')
```

## Licensing Considerations

### Open-Source Licenses:
- **MIT** (HiGHS): Most permissive
- **Apache 2.0** (SCIP, OR-Tools): Permissive, patent protection
- **EPL** (IPOPT, CBC): Weak copyleft
- **GPL**: Strong copyleft (few optimization solvers)

### Commercial Licenses:
- **Named-user**: Tied to individual
- **Floating**: Shared pool of licenses
- **Cloud**: Usage-based pricing
- **Academic**: Free but restricted to academic use

## Key Findings

1. **Open-source competitive for many use cases**: No longer automatically commercial
2. **HiGHS emergence**: Major development (SciPy, MATLAB adoption)
3. **SCIP Apache 2.0**: Removes licensing barrier for best open-source MILP
4. **Benchmark withdrawal**: Reduced transparency for commercial performance
5. **Commercial still faster on huge MILP**: But gap narrowed
6. **CP-SAT excellence**: OR-Tools competitive with commercial CP solvers
7. **Convex exception**: MOSEK significantly faster than open-source for conic

## Decision Framework

```
Problem size and performance requirements?
├─ Small-medium → Open-source sufficient
│  └─ HiGHS, SCIP, IPOPT, OR-Tools
│
├─ Large, but not time-critical → Try open-source first
│  └─ Profile before deciding on commercial
│
└─ Very large AND time-critical → Commercial justified
   └─ Gurobi, CPLEX (MILP), MOSEK (conic), Knitro (NLP)

Budget available?
├─ No → Open-source (HiGHS, SCIP excellent)
├─ Academic → Free commercial licenses available
└─ Industry → Evaluate ROI (does speed improvement justify cost?)
```

## Conclusion

**2025 landscape**: Open-source solvers increasingly viable for production. Start with open-source; upgrade to commercial only when profiling demonstrates clear need. The performance gap has narrowed significantly, especially for LP and medium-scale MILP.

**Biggest winners**: HiGHS (LP/MILP), SCIP (MILP/MINLP), OR-Tools (CP), IPOPT (NLP)

**Commercial still justified for**: Very large MILP, professional support needs, conic optimization (MOSEK)
