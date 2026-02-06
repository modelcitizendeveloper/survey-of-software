# Pyomo: Python Optimization Modeling Objects

## Overview

Pyomo is a Python-based open-source software package for formulating and analyzing optimization models. It is an **algebraic modeling language (AML)** that allows you to express optimization problems using mathematical notation, similar to AMPL or GAMS.

**Key finding**: With 2,127 GitHub stars and 123,641 weekly downloads, Pyomo is the leading Python algebraic modeling language, offering interfaces to 20+ solver backends.

## Installation

```bash
# Basic installation
pip install pyomo

# With optional solver interfaces
pip install pyomo[optional]
```

**Note**: Pyomo is a modeling language, not a solver. You must install solvers separately (GLPK, CBC, IPOPT, Gurobi, etc.).

## Problem Types Supported

Pyomo supports virtually all optimization problem types through its extensible architecture:

| Problem Type | Supported | Notes |
|--------------|-----------|-------|
| Linear Programming (LP) | ✅ Yes | Via GLPK, CBC, HiGHS, Gurobi, CPLEX, etc. |
| Mixed-Integer Linear (MILP) | ✅ Yes | All MILP solvers |
| Quadratic Programming (QP) | ✅ Yes | Via Gurobi, CPLEX, MOSEK |
| Nonlinear Programming (NLP) | ✅ Yes | Via IPOPT, SNOPT, KNITRO, BARON |
| Mixed-Integer NLP (MINLP) | ✅ Yes | Via BARON, Couenne, BONMIN |
| Stochastic Programming | ✅ Yes | PySP extension |
| Dynamic Optimization | ✅ Yes | Pyomo.DAE for differential-algebraic equations |
| Disjunctive Programming | ✅ Yes | GDP extension (generalized disjunctive programming) |

Pyomo's strength is **solver flexibility**: same model code can be solved with different backends.

## Basic Example: Linear Programming

```python
from pyomo.environ import *

# Create a concrete model
model = ConcreteModel()

# Decision variables
model.x = Var(domain=NonNegativeReals)
model.y = Var(domain=NonNegativeReals)

# Objective: maximize x + 2y
model.obj = Objective(expr=model.x + 2*model.y, sense=maximize)

# Constraints
model.con1 = Constraint(expr=2*model.x + model.y <= 20)
model.con2 = Constraint(expr=model.x + 2*model.y <= 20)

# Solve with GLPK (open-source LP solver)
solver = SolverFactory('glpk')
result = solver.solve(model, tee=True)  # tee=True shows solver output

# Display results
print(f"x = {value(model.x)}")
print(f"y = {value(model.y)}")
print(f"Objective = {value(model.obj)}")
```

## Basic Example: Mixed-Integer Programming

```python
from pyomo.environ import *

model = ConcreteModel()

# Integer decision variables
model.x = Var(domain=NonNegativeIntegers)
model.y = Var(domain=NonNegativeIntegers)

# Objective
model.obj = Objective(expr=model.x + 2*model.y, sense=maximize)

# Constraints
model.con1 = Constraint(expr=2*model.x + model.y <= 20)
model.con2 = Constraint(expr=model.x + 2*model.y <= 20)

# Solve with CBC (open-source MILP solver)
solver = SolverFactory('cbc')
result = solver.solve(model)

print(f"x = {value(model.x)}")  # Integer value
print(f"y = {value(model.y)}")  # Integer value
print(f"Objective = {value(model.obj)}")
```

## Basic Example: Nonlinear Programming

```python
from pyomo.environ import *

model = ConcreteModel()

# Variables with bounds
model.x = Var(bounds=(0, 10), initialize=5)
model.y = Var(bounds=(0, 10), initialize=5)

# Nonlinear objective
model.obj = Objective(expr=model.x**2 + model.y**2)

# Nonlinear constraint
model.con1 = Constraint(expr=model.x**2 + model.y >= 4)

# Solve with IPOPT (open-source NLP solver)
solver = SolverFactory('ipopt')
result = solver.solve(model, tee=False)

print(f"x = {value(model.x)}")
print(f"y = {value(model.y)}")
print(f"Objective = {value(model.obj)}")
```

## Basic Example: Indexed Variables and Constraints

Pyomo excels at modeling problems with sets and indices:

```python
from pyomo.environ import *

model = ConcreteModel()

# Sets
model.PROJECTS = Set(initialize=['A', 'B', 'C', 'D'])

# Parameters (data)
cost = {'A': 10, 'B': 15, 'C': 12, 'D': 8}
return_val = {'A': 20, 'B': 30, 'C': 25, 'D': 15}
model.budget = Param(initialize=30)

# Indexed binary variables: select[p] = 1 if project p is selected
model.select = Var(model.PROJECTS, domain=Binary)

# Objective: maximize total return
model.obj = Objective(
    expr=sum(return_val[p] * model.select[p] for p in model.PROJECTS),
    sense=maximize
)

# Budget constraint
model.budget_con = Constraint(
    expr=sum(cost[p] * model.select[p] for p in model.PROJECTS) <= model.budget
)

# Solve
solver = SolverFactory('cbc')
solver.solve(model)

# Display selected projects
print("Selected projects:")
for p in model.PROJECTS:
    if value(model.select[p]) > 0.5:  # Binary variable
        print(f"  {p}: return = {return_val[p]}, cost = {cost[p]}")
```

## API Design Philosophy

**Algebraic modeling language**: Express models using mathematical notation close to textbook formulations.

**Advantages**:
- Readable models (looks like mathematics)
- Separation of model and data
- Reusable model structure
- Easy to modify and extend
- Solver-agnostic (change solver with one line)
- Structured indexing (sets, parameters, indexed variables)

**Disadvantages**:
- Learning curve (new syntax and concepts)
- More verbose than direct solver APIs for simple problems
- Overhead for very small problems
- Requires understanding of both Pyomo syntax and optimization theory

## Solver Backends (20+ supported)

Pyomo interfaces with external solvers via file-based or direct API communication.

### Open-Source Linear/Integer
- **GLPK**: GNU Linear Programming Kit
- **CBC**: COIN-OR Branch and Cut
- **HiGHS**: High-performance LP/MIP solver

### Open-Source Nonlinear
- **IPOPT**: Interior Point OPTimizer (large-scale NLP)
- **Couenne**: Convex Over and Under ENvelopes for NLP (MINLP)
- **BONMIN**: Basic Open-source Nonlinear Mixed INteger (MINLP)

### Commercial
- **Gurobi**: Leading commercial MILP/QP solver
- **CPLEX**: IBM commercial solver
- **MOSEK**: Conic optimization specialist
- **XPRESS**: FICO solver
- **KNITRO**: Nonlinear optimization
- **BARON**: Global MINLP solver

### Specialized
- **Mindtpy**: Pyomo's built-in MINLP solver
- **SCIP**: Open-source MILP/MINLP
- **GDPopt**: Generalized disjunctive programming

Use `SolverFactory('solver_name')` to select solver.

## When to Use Pyomo

### ✅ Good fit when:
- **Complex models**: Many constraints, indexed variables, reusable structure
- **Solver flexibility**: Want to try multiple solvers (CBC, Gurobi, IPOPT) on same model
- **Academic research**: Need to document model structure, try different formulations
- **Data-driven models**: Separate model logic from data, load data from files/databases
- **Mixed problem types**: LP, MILP, NLP in same project
- **Advanced features**: Stochastic programming, disjunctive programming, DAE systems
- **Model archival**: Mathematical formulation readable years later

### ❌ Not suitable when:
- **Simple one-off problems**: scipy.optimize or PuLP simpler
- **Constraint programming**: OR-Tools CP-SAT better for scheduling
- **Convex optimization**: CVXPY provides DCP verification
- **Maximum performance**: Direct solver APIs (gurobipy) slightly faster
- **No solver installation**: Pyomo requires external solvers (unlike OR-Tools)

## Community and Maturity

| Metric | Value/Status |
|--------|--------------|
| **GitHub stars** | 2,127 |
| **Downloads** | 123,641 per week (PyPI) |
| **Maturity** | Mature (15+ years) |
| **Maintenance** | Active (Pyomo v6.9.4, Sept 2025) |
| **Documentation** | Excellent (pyomo.readthedocs.io, textbook available) |
| **License** | BSD (permissive) |
| **Python versions** | 3.8+ (3.8 dropped in 6.9.3) |
| **Contributors** | 100+ |

Pyomo is the **academic standard** for optimization modeling in Python. Used extensively in research and teaching.

## Key Findings from Research

1. **Ecosystem leader**: 20+ solver interfaces make Pyomo the most flexible Python modeling language for solver experimentation.

2. **Active development**: Regular releases (v6.9.4 in 2025), new features like logic-based discrete steepest descent in GDPopt.

3. **Extensions**: Pyomo.DAE (differential-algebraic equations), PySP (stochastic programming), GDP (disjunctive programming) enable advanced problem types.

4. **Educational adoption**: Many universities use Pyomo for teaching optimization. Textbook "Pyomo — Optimization Modeling in Python" available.

5. **Academic roots**: Developed at Sandia National Laboratories, widely used in energy systems, chemical engineering, operations research.

## Comparison with Alternatives

| Feature | Pyomo | CVXPY | PuLP | OR-Tools |
|---------|-------|-------|------|----------|
| Problem types | LP, MILP, NLP, MINLP | Convex only | LP, MILP | LP, MILP, CP |
| Solver backends | 20+ | 10+ | 10+ | Bundled |
| Modeling style | Algebraic | Algebraic (DCP) | Algebraic | Object-oriented |
| Learning curve | Moderate | Moderate | Easy | Moderate |
| Flexibility | Highest | Medium | Medium | Lower |
| Performance overhead | Low | Low | Low | Very low |
| Best for | Multi-solver research | Convex problems | Simple LP/MILP | Production, CP |

## Example Use Cases (Generic)

### Production Planning with Time Periods
Determine production quantities over time to minimize cost while meeting demand.

```python
from pyomo.environ import *

model = ConcreteModel()

# Sets
model.PRODUCTS = Set(initialize=['A', 'B', 'C'])
model.PERIODS = RangeSet(1, 12)  # 12 time periods

# Parameters (data)
model.demand = Param(model.PRODUCTS, model.PERIODS, initialize=demand_data)
model.production_cost = Param(model.PRODUCTS, initialize=prod_cost_data)
model.inventory_cost = Param(model.PRODUCTS, initialize=inv_cost_data)
model.capacity = Param(model.PERIODS, initialize=capacity_data)

# Variables
model.produce = Var(model.PRODUCTS, model.PERIODS, domain=NonNegativeReals)
model.inventory = Var(model.PRODUCTS, model.PERIODS, domain=NonNegativeReals)

# Objective: minimize total cost
def total_cost_rule(m):
    return sum(m.production_cost[p] * m.produce[p, t] +
               m.inventory_cost[p] * m.inventory[p, t]
               for p in m.PRODUCTS for t in m.PERIODS)
model.obj = Objective(rule=total_cost_rule, sense=minimize)

# Inventory balance constraints
def inventory_balance_rule(m, p, t):
    if t == 1:
        return m.inventory[p, t] == m.produce[p, t] - m.demand[p, t]
    else:
        return m.inventory[p, t] == m.inventory[p, t-1] + m.produce[p, t] - m.demand[p, t]
model.inventory_balance = Constraint(model.PRODUCTS, model.PERIODS, rule=inventory_balance_rule)

# Capacity constraint
def capacity_rule(m, t):
    return sum(m.produce[p, t] for p in m.PRODUCTS) <= m.capacity[t]
model.capacity_con = Constraint(model.PERIODS, rule=capacity_rule)

solver = SolverFactory('glpk')
solver.solve(model)
```

### Network Design with Fixed Costs
Select facilities to open (binary decisions) and route flows to minimize total cost.

```python
from pyomo.environ import *

model = ConcreteModel()

model.FACILITIES = Set(initialize=['F1', 'F2', 'F3'])
model.CUSTOMERS = Set(initialize=['C1', 'C2', 'C3', 'C4'])

# Binary: open facility or not
model.open = Var(model.FACILITIES, domain=Binary)

# Continuous: flow from facility to customer
model.flow = Var(model.FACILITIES, model.CUSTOMERS, domain=NonNegativeReals)

# Objective: minimize fixed costs + variable costs
def total_cost_rule(m):
    fixed = sum(fixed_cost[f] * m.open[f] for f in m.FACILITIES)
    variable = sum(transport_cost[f, c] * m.flow[f, c]
                   for f in m.FACILITIES for c in m.CUSTOMERS)
    return fixed + variable
model.obj = Objective(rule=total_cost_rule, sense=minimize)

# Meet customer demand
def demand_rule(m, c):
    return sum(m.flow[f, c] for f in m.FACILITIES) >= demand[c]
model.demand_con = Constraint(model.CUSTOMERS, rule=demand_rule)

# Facility capacity (only if open)
def capacity_rule(m, f):
    return sum(m.flow[f, c] for c in m.CUSTOMERS) <= capacity[f] * m.open[f]
model.capacity_con = Constraint(model.FACILITIES, rule=capacity_rule)

solver = SolverFactory('cbc')
solver.solve(model)
```

## Performance Characteristics

Pyomo adds modest overhead for:
- Model construction (building expression trees)
- Communication with solver (file-based or API)

For large models (10,000+ variables), overhead typically <10% of total solve time. Solver performance dominates.

**Tips for performance**:
- Use indexed variables/constraints instead of loops
- Choose fast solvers (Gurobi > CBC for MILP)
- Consider direct API interfaces (pyomo-gurobi-direct) for large models

## Advanced Features

### Abstract Models
Separate model structure from data:
```python
model = AbstractModel()
# Define structure with undefined parameters
model.load('data.dat')  # Load data later
```

### Persistent Solvers
Reuse solver instance across multiple solves (incremental changes):
```python
solver = SolverFactory('gurobi', solver_io='python')
solver.set_instance(model)
solver.solve()
# Modify model
solver.solve()  # Incremental solve
```

### Suffixes
Access solver-specific information (dual values, reduced costs):
```python
model.dual = Suffix(direction=Suffix.IMPORT)
solver.solve(model)
print(model.dual[model.con1])  # Dual value of constraint
```

## References

- Official documentation: https://pyomo.readthedocs.io
- GitHub: https://github.com/Pyomo/pyomo (2.1k stars)
- Textbook: Bynum et al., "Pyomo — Optimization Modeling in Python", Springer
- Website: http://www.pyomo.org

## Summary

**Pyomo** is the most comprehensive Python optimization modeling language:
- 20+ solver backends (most flexible)
- All problem types (LP, MILP, NLP, MINLP, stochastic, dynamic)
- Algebraic modeling for complex, structured problems
- Academic standard for optimization research

**Choose Pyomo** when:
- You need solver flexibility (try Gurobi, CBC, IPOPT on same model)
- Model complexity justifies algebraic modeling overhead
- Academic research or teaching
- Advanced features (stochastic, disjunctive, DAE)

**Look elsewhere** for:
- Simple one-off problems (scipy.optimize, PuLP)
- Convex with verification (CVXPY)
- Constraint programming (OR-Tools)
- Maximum performance (direct APIs)
