# S3-Need-Driven: Generic Use Case Patterns

## Overview

Optimization use cases organized by **problem pattern**, not industry. These patterns are application-neutral and reusable.

## 1. Resource Allocation

### Pattern
Allocate limited resources across competing options to maximize total value.

### Mathematical Structure
- **Variables**: Allocation amounts (continuous or discrete)
- **Objective**: Maximize total value or minimize total cost
- **Constraints**: Resource limits, minimum/maximum allocations

### Problem Types
- **Continuous allocation**: LP
- **Discrete allocation**: MILP
- **With diminishing returns**: Convex optimization (QP)

### Generic Examples
- Budget allocation across projects
- Computing capacity allocation across workloads
- Storage space allocation across tenants
- Energy allocation across production units
- Personnel allocation across tasks

### Modeling Pattern
```python
# Pyomo example
model = ConcreteModel()
model.OPTIONS = Set(initialize=options)
model.allocate = Var(model.OPTIONS, domain=NonNegativeReals)
model.obj = Objective(expr=sum(value[o] * model.allocate[o] for o in model.OPTIONS), sense=maximize)
model.capacity = Constraint(expr=sum(model.allocate[o] for o in model.OPTIONS) <= total_capacity)
```

---

## 2. Scheduling with Constraints

### Pattern
Schedule tasks over time subject to precedence, resource limits, and time windows.

### Mathematical Structure
- **Variables**: Start/end times, binary assignment variables
- **Objective**: Minimize makespan, minimize tardiness, maximize throughput
- **Constraints**: Precedence (A before B), resource capacity, time windows, no-overlap

### Problem Types
- **Discrete time**: MILP
- **Continuous time**: NLP or CP
- **With logical constraints**: Constraint Programming (CP)

### Generic Examples
- Job shop scheduling (tasks on machines)
- Project scheduling with dependencies
- Appointment scheduling with availability windows
- Batch production scheduling
- Maintenance scheduling with downtime constraints

### Modeling Approach
**Constraint Programming** (OR-Tools CP-SAT) often best for scheduling due to:
- Natural expression of logical constraints (no-overlap, all-different)
- Domain propagation effectiveness
- Award-winning performance

```python
# OR-Tools CP-SAT example
from ortools.sat.python import cp_model

model = cp_model.CpModel()
# Interval variables for tasks
intervals = []
for task in tasks:
    start = model.NewIntVar(0, horizon, f'start_{task}')
    duration = durations[task]
    end = model.NewIntVar(0, horizon, f'end_{task}')
    interval = model.NewIntervalVar(start, duration, end, f'interval_{task}')
    intervals.append(interval)

# No-overlap constraint
model.AddNoOverlap(intervals)

# Minimize makespan
makespan = model.NewIntVar(0, horizon, 'makespan')
for interval in intervals:
    model.Add(makespan >= interval.EndExpr())
model.Minimize(makespan)
```

---

## 3. Selection and Assignment

### Pattern
Select subset of items or assign items to slots, optimizing total value subject to constraints.

### Mathematical Structure
- **Variables**: Binary (selected/not, assigned/not)
- **Objective**: Maximize value or minimize cost
- **Constraints**: Cardinality (select exactly K), capacity, exclusion, dependency

### Problem Types
- **Binary selection**: MILP
- **Assignment with matching**: MILP (assignment problem)

### Generic Examples
- Project portfolio selection with budget
- Facility location (which facilities to open)
- Supplier selection in procurement
- Feature selection in product design
- Worker-task assignment
- Knapsack problems (packing with value)

### Modeling Pattern
```python
# Binary selection
model.select = Var(ITEMS, domain=Binary)
model.obj = Objective(expr=sum(value[i] * model.select[i] for i in ITEMS), sense=maximize)
model.budget = Constraint(expr=sum(cost[i] * model.select[i] for i in ITEMS) <= budget_limit)

# Cardinality: select exactly K items
model.cardinality = Constraint(expr=sum(model.select[i] for i in ITEMS) == K)
```

---

## 4. Network Flow and Routing

### Pattern
Route flow through network minimizing cost or maximizing throughput.

### Mathematical Structure
- **Variables**: Flow on each arc
- **Objective**: Minimize cost or maximize flow
- **Constraints**: Flow conservation (inflow = outflow), capacity limits

### Problem Types
- **Continuous flow**: LP (network simplex)
- **Discrete routing**: MILP
- **Vehicle routing**: Specialized algorithms (OR-Tools routing)

### Generic Examples
- Supply chain network (factory → warehouse → customer)
- Transportation routing (minimize distance/cost)
- Communication network routing (maximize throughput)
- Pipeline flow optimization
- Logistics network design

### Modeling Advantage
Network flow problems have **special structure** enabling very efficient solution (network simplex faster than general LP).

```python
# Min-cost flow (OR-Tools)
from ortools.graph import pywrapgraph

min_cost_flow = pywrapgraph.SimpleMinCostFlow()
for (source, dest, capacity, cost) in arcs:
    min_cost_flow.AddArcWithCapacityAndUnitCost(source, dest, capacity, cost)

# Supply/demand at nodes
for node, supply in supplies.items():
    min_cost_flow.SetNodeSupply(node, supply)
```

---

## 5. Cutting and Packing

### Pattern
Cut raw materials into required pieces minimizing waste, or pack items into containers minimizing containers used.

### Mathematical Structure
- **Variables**: Pattern usage (how many times each cutting/packing pattern used)
- **Objective**: Minimize waste or minimize containers
- **Constraints**: Meet demand for each item size

### Problem Types
- **1D cutting stock**: Column generation (LP/MILP)
- **2D/3D bin packing**: MILP (very hard)

### Generic Examples
- Cutting steel rolls into required widths
- Cutting fabric into pattern pieces
- Packing boxes into shipping containers
- Packing advertisements into pages
- Memory allocation in computing

### Algorithmic Approach
**Column generation**: Generate cutting patterns on-the-fly rather than enumerate all upfront.

---

## 6. Blending and Mixing

### Pattern
Mix inputs to meet output specifications at minimum cost.

### Mathematical Structure
- **Variables**: Quantity of each input
- **Objective**: Minimize total cost
- **Constraints**: Meet requirements for output properties (nutrients, strength, etc.)

### Problem Types
- **Linear blending**: LP
- **With nonlinear properties**: NLP

### Generic Examples
- Feed/nutrition blending (meet nutrient requirements)
- Chemical blending (meet specification)
- Fuel blending (octane rating, emissions)
- Alloy blending (metal composition)
- Portfolio blending (risk/return characteristics)

---

## 7. Portfolio Optimization

### Pattern
Select combination of assets balancing risk and return.

### Mathematical Structure
- **Variables**: Portfolio weights (allocation to each asset)
- **Objective**: Minimize risk (variance) or maximize return
- **Constraints**: Total weight = 1, minimum return target, diversification limits

### Problem Types
- **Mean-variance**: Quadratic programming (QP)
- **With constraints**: Convex optimization (CVXPY)
- **With cardinality limits**: MILP (select K of N assets)

### Generic Example
```python
# CVXPY portfolio optimization
w = cp.Variable(n_assets)  # Portfolio weights
risk = cp.quad_form(w, cov_matrix)
objective = cp.Minimize(risk)
constraints = [
    cp.sum(w) == 1,          # Weights sum to 1
    w >= 0,                   # No short selling
    returns @ w >= target     # Meet return target
]
problem = cp.Problem(objective, constraints)
```

---

## 8. Parameter Estimation and Calibration

### Pattern
Find model parameters that best fit observed data.

### Mathematical Structure
- **Variables**: Model parameters
- **Objective**: Minimize prediction error (least-squares, maximum likelihood)
- **Constraints**: Parameter bounds, physical constraints

### Problem Types
- **Linear regression**: LP or QP
- **Nonlinear regression**: NLP
- **With regularization**: Convex optimization (Lasso, ridge)

### Generic Examples
- Calibrate simulation parameters to match real system
- Fit demand model to historical data
- Estimate failure rates from field data
- Calibrate financial model to market data

### Modeling Pattern
```python
# scipy.optimize for calibration
def simulation_error(params):
    predictions = run_simulation(params)
    return np.sum((predictions - observations)**2)

result = minimize(simulation_error, initial_params, bounds=param_bounds)
```

---

## 9. Multi-Objective Trade-off Analysis

### Pattern
Optimize multiple competing objectives simultaneously.

### Mathematical Structure
- **Variables**: Design or decision variables
- **Objectives**: Multiple objective functions (e.g., cost, performance, quality)
- **Output**: Pareto frontier (set of non-dominated solutions)

### Problem Types
- **Multi-objective optimization**: Evolutionary algorithms (pymoo)
- **Convex multi-objective**: Weighted sum or epsilon-constraint

### Generic Examples
- Product design: minimize cost, maximize quality, minimize weight
- System design: maximize performance, minimize energy, minimize cost
- Policy design: maximize effectiveness, minimize cost, minimize risk

### Approach
```python
# pymoo for multi-objective
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize

# Define problem with multiple objectives
problem = MyMultiObjectiveProblem()

algorithm = NSGA2(pop_size=100)
result = minimize(problem, algorithm, ('n_gen', 200))

# Result contains Pareto frontier
pareto_front = result.F
```

---

## 10. Robust and Worst-Case Optimization

### Pattern
Optimize for worst-case performance under uncertainty.

### Mathematical Structure
- **Variables**: Decision variables
- **Objective**: Minimize worst-case cost or maximize worst-case performance
- **Uncertainty**: Set of possible scenarios (no probability distribution)

### Problem Types
- **Robust LP**: Reformulate as larger LP
- **Robust convex**: CVXPY with norm constraints

### Generic Examples
- Portfolio optimization: minimize worst-case loss
- Network design: maximize worst-case capacity
- Production planning: meet worst-case demand
- Control design: stability under worst-case disturbances

---

## Use Case to Library Mapping

| Use Case Pattern | Primary Library | Alternative | Problem Type |
|------------------|----------------|-------------|--------------|
| **Resource Allocation** | PuLP, Pyomo | scipy.optimize | LP, MILP, QP |
| **Scheduling** | OR-Tools CP-SAT | Pyomo | CP, MILP |
| **Selection/Assignment** | PuLP, OR-Tools | Pyomo | MILP |
| **Network Flow** | OR-Tools, Pyomo | PuLP | LP, MILP |
| **Cutting/Packing** | Pyomo, OR-Tools | PuLP | MILP |
| **Blending** | PuLP, Pyomo | scipy.optimize | LP |
| **Portfolio** | CVXPY | Pyomo | QP, Convex |
| **Parameter Estimation** | scipy.optimize | Pyomo+IPOPT | NLP |
| **Multi-Objective** | pymoo | CVXPY (weighted) | Multi-objective |
| **Robust** | CVXPY | Pyomo | Convex, LP |

## Pattern Recognition Strategy

When facing an optimization problem:

1. **Identify pattern**: Does it match a known use case?
2. **Determine problem type**: LP, MILP, NLP, convex, CP?
3. **Select library**: Based on problem type and pattern
4. **Adapt generic model**: Customize pattern to your specifics
5. **Validate**: Test on small instance, verify results make sense

Most real problems are variations of these 10 patterns.
