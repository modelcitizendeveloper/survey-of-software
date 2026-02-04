# S3-Need-Driven: Learning Curve Assessment

## Overview

Learning curve estimates based on documentation quality, community resources, and complexity.

## Learning Curve Rankings

### Easy (1-2 days to productive)
**PuLP**: Simplest LP/MILP modeling
- Minimal concepts: LpProblem, LpVariable, constraints
- Pythonic syntax
- Excellent tutorials

**scipy.optimize** (basic): Continuous optimization
- Functional interface (pass functions)
- Part of scipy (familiar to scientists)
- Good documentation

### Moderate (1 week to productive)
**Pyomo**: Algebraic modeling
- New syntax (ConcreteModel, Var, Objective, Constraint)
- Set-based indexing concept
- Solver installation required
- Excellent docs and textbook

**CVXPY**: Convex optimization
- DCP rules learning curve
- Need to understand convexity
- Good documentation and examples

**OR-Tools**: Multiple modules
- Different APIs for LP, CP, routing
- Good Google developer docs
- Many examples

### Advanced (2-4 weeks to productive)
**GEKKO**: Dynamic optimization
- Dynamic optimization concepts (DAE, MPC)
- Specialized domain
- Good tutorials but smaller community

**pymoo**: Multi-objective optimization
- Evolutionary algorithm concepts
- Multi-objective theory (Pareto frontier)
- IEEE paper + docs

## Learning Resources by Library

### scipy.optimize
**Official docs**: ⭐⭐⭐⭐⭐ Excellent
- https://docs.scipy.org/doc/scipy/reference/optimize.html
- Clear API reference
- Many examples

**Tutorials**: ⭐⭐⭐⭐ Good
- Real Python tutorials
- Stack Overflow coverage

**Community**: ⭐⭐⭐⭐⭐ Huge (scipy ecosystem)

### PuLP
**Official docs**: ⭐⭐⭐⭐ Good
- https://coin-or.github.io/pulp/
- Case studies
- Clear examples

**Tutorials**: ⭐⭐⭐ Adequate
- Medium articles
- University course materials

**Community**: ⭐⭐⭐ Good

### Pyomo
**Official docs**: ⭐⭐⭐⭐⭐ Excellent
- https://pyomo.readthedocs.io
- Comprehensive
- API reference + conceptual

**Book**: "Pyomo — Optimization Modeling in Python" (Springer)

**Tutorials**: ⭐⭐⭐⭐⭐ Excellent
- University courses use Pyomo
- Many academic examples

**Community**: ⭐⭐⭐⭐ Strong (academic)

### CVXPY
**Official docs**: ⭐⭐⭐⭐⭐ Excellent
- https://www.cvxpy.org
- Tutorial, examples, API reference
- DCP rules explained

**Academic paper**: JMLR 2016

**Tutorials**: ⭐⭐⭐⭐⭐ Excellent
- Stanford CVX101 course
- Many examples

**Community**: ⭐⭐⭐⭐ Strong (academic + industry)

### OR-Tools
**Official docs**: ⭐⭐⭐⭐⭐ Excellent
- https://developers.google.com/optimization
- Google-quality docs
- Many examples for each module

**Tutorials**: ⭐⭐⭐⭐ Good
- Routing tutorial excellent
- CP-SAT examples

**Community**: ⭐⭐⭐⭐ Good (Google + community)

### GEKKO
**Official docs**: ⭐⭐⭐ Adequate
- https://gekko.readthedocs.io
- Focus on examples

**Tutorials**: ⭐⭐⭐ Good
- APMonitor tutorials (BYU)
- Specialized for dynamic optimization

**Community**: ⭐⭐ Small (niche domain)

### pymoo
**Official docs**: ⭐⭐⭐⭐ Good
- https://pymoo.org
- Algorithms documented
- Getting started guides

**Academic paper**: IEEE Access 2020

**Community**: ⭐⭐⭐ Growing

## Common Learning Challenges

### Challenge 1: Problem Type Identification
**Difficulty**: Moderate
**Solution**: Use decision trees in this research (S1-rapid/approach.md)

### Challenge 2: Mathematical Formulation
**Difficulty**: Hard (requires optimization knowledge)
**Solution**: Start with generic patterns (S3-need-driven/use-cases.md), adapt

### Challenge 3: Solver Installation
**Difficulty**: Variable
- **Easy**: PuLP (CBC bundled), OR-Tools (bundled), scipy (built-in)
- **Moderate**: Pyomo (install GLPK, CBC separately)
- **Hard**: IPOPT (requires linear algebra libraries)

### Challenge 4: Debugging Infeasibility
**Difficulty**: Hard
**Tips**:
- Start with small test instances
- Remove constraints incrementally
- Check constraint units and scales
- Use solver diagnostics (IIS - Irreducible Infeasible Set)

### Challenge 5: Performance Tuning
**Difficulty**: Advanced
**Requires**: Understanding of algorithms, formulation quality

## Recommended Learning Paths

### Path 1: Beginner (LP/MILP)
1. Week 1: PuLP basics (simple LP)
2. Week 2: PuLP + integer variables (MILP)
3. Week 3: Graduate to Pyomo for complex models
4. Week 4: Experiment with solvers (CBC, SCIP, commercial if available)

### Path 2: Scientific Computing Background
1. Week 1: scipy.optimize (unconstrained, then constrained)
2. Week 2: CVXPY (if working with convex problems)
3. Week 3: Pyomo (when need MILP or multi-solver)

### Path 3: Scheduling/Combinatorial
1. Week 1: Basic MILP with PuLP
2. Week 2: OR-Tools CP-SAT
3. Week 3: Advanced CP-SAT features
4. Week 4: Routing module if needed

### Path 4: Nonlinear/Dynamic
1. Week 1-2: scipy.optimize (NLP basics)
2. Week 3-4: Pyomo + IPOPT
3. Week 5+: GEKKO for dynamic optimization

## Time to First Working Model

| Library | Simple Problem | Complex Problem |
|---------|---------------|----------------|
| **PuLP** | 30 min | 2-4 hours |
| **scipy.optimize** | 15 min | 1-2 hours |
| **Pyomo** | 1-2 hours | 4-8 hours |
| **CVXPY** | 1 hour | 3-5 hours |
| **OR-Tools** | 1-2 hours | 4-8 hours |
| **GEKKO** | 2-3 hours | 1-2 days |

(Assumes familiarity with Python and optimization concepts)

## Success Factors

### Accelerate Learning:
1. **Start with examples**: Modify existing code before writing from scratch
2. **Small test instances**: Debug on tiny problems
3. **One concept at a time**: Don't combine learning optimization + new domain + new library
4. **Community**: Stack Overflow, GitHub issues
5. **Documentation quality**: Pyomo, CVXPY, OR-Tools have excellent docs

### Common Mistakes:
1. **Wrong problem type**: Using MILP tools for NLP, or vice versa
2. **Scaling issues**: Variables differ by orders of magnitude
3. **Infeasibility**: Over-constrained problem
4. **Performance expectations**: Not all problems solvable quickly
5. **Premature optimization**: Worry about formulation before solving

## Key Takeaways

1. **PuLP easiest entry point** for LP/MILP
2. **scipy.optimize easiest for continuous** problems
3. **Documentation quality matters**: Pyomo, CVXPY, OR-Tools shine
4. **Generic patterns accelerate learning**: Adapt examples from use-cases.md
5. **Community support varies**: scipy, Pyomo, CVXPY have strong communities
6. **Time investment**: 1 week to productivity for most libraries (moderate problems)
