# S3-Need-Driven: Simulation-Optimization Coupling

## Overview

Coupling optimization with simulation (from research/1.120-simulation) enables optimizing systems too complex for closed-form models.

## When to Couple Simulation + Optimization

### Use When:
- Objective function cannot be written analytically
- Complex stochastic processes
- System dynamics require detailed simulation
- What-if analysis insufficient (need optimal decisions)

### Don't Use When:
- Objective can be modeled directly (LP, MILP, NLP)
- Simulation too slow for many evaluations
- Can approximate with simpler model

## Coupling Approaches

### 1. Simulation-Based Optimization (Metaheuristics)
**Pattern**: Simulation evaluates objective, metaheuristic searches

```python
def objective(params):
    # Run simulation with params
    results = run_simulation(params, n_replications=30)
    return np.mean(results['cost'])

# Optimize using derivative-free method
result = scipy.optimize.minimize(objective, x0, method='Nelder-Mead')
```

**Suitable algorithms**:
- Genetic algorithms (pymoo)
- Simulated annealing
- Particle swarm
- Nelder-Mead, Powell (scipy.optimize)

**Challenge**: Each objective evaluation expensive (simulation run)

### 2. Simulation + Mathematical Programming
**Pattern**: Use simulation output as input to optimization

**Example**: Supply chain optimization
1. Simulate demand uncertainty → estimate demand distributions
2. Solve MILP for inventory/production decisions given demand
3. Validate decisions with simulation

### 3. Metamodel-Based Optimization
**Pattern**: Build surrogate model from simulation, optimize surrogate

**Steps**:
1. Sample parameter space (Latin hypercube, design of experiments)
2. Run simulations at sample points
3. Fit metamodel (polynomial, kriging, neural network)
4. Optimize metamodel (fast!)
5. Validate at optimal point with full simulation

**Advantage**: Separate expensive simulation from optimization

### 4. Iterative Optimization-Simulation
**Pattern**: Alternate between optimization and simulation validation

**Steps**:
1. Solve optimization with simplified model
2. Validate solution with detailed simulation
3. Update model based on simulation results
4. Re-optimize
5. Repeat until convergence

## Integration Patterns

### Pattern 1: Parameters → Simulation → Performance
Optimize control parameters:
```python
# Example: Inventory policy optimization
def evaluate_policy(reorder_point, order_quantity):
    sim_results = run_inventory_simulation(reorder_point, order_quantity, n_days=365)
    return sim_results['total_cost']

# Find best policy parameters
result = minimize(lambda p: evaluate_policy(p[0], p[1]), x0=[50, 100])
```

### Pattern 2: Simulation → Data → Optimization
Use simulation to generate scenarios:
```python
# Generate demand scenarios via simulation
scenarios = [simulate_demand() for _ in range(100)]

# Solve stochastic optimization with scenarios
model = ConcreteModel()
# ... define variables ...
for s, scenario in enumerate(scenarios):
    # Add constraints for this scenario
    model.add_component(f'demand_con_{s}', 
                        Constraint(expr=model.production >= scenario['demand']))
```

## Key Considerations

### Computational Budget
- Each simulation run costs time
- Limit optimization to <1000 evaluations typically
- Use efficient optimization algorithms (few evaluations)

### Stochasticity
- Simulation outputs are random
- Multiple replications needed for accuracy
- Statistical comparison of solutions

### Validation
- Validate optimal solution with independent simulation runs
- Check robustness to parameter variations

## Tools and Libraries

| Approach | Python Library | Notes |
|----------|---------------|-------|
| **Metaheuristics** | pymoo, scipy.optimize.differential_evolution | For black-box objectives |
| **Gradient-free NLP** | scipy.optimize (Nelder-Mead, Powell) | Small parameter spaces |
| **Metamodeling** | scikit-learn, GPy (Gaussian processes) | Build surrogates |
| **MP + Simulation** | Pyomo, PuLP (optimization) + SimPy, Ciw (simulation) | Separate tools |

## Example: Queueing System Optimization

**Problem**: Find staffing levels minimizing cost + wait time

**Simulation**: SimPy model of queueing system
**Optimization**: Minimize cost function evaluated by simulation

```python
def simulate_queue(n_servers):
    # Run SimPy simulation
    results = run_simpy_model(n_servers, sim_time=1000)
    avg_wait = results['avg_wait_time']
    cost = n_servers * server_cost + avg_wait * wait_penalty
    return cost

# Discrete optimization (integer servers)
best_cost = float('inf')
best_servers = None
for n in range(1, 20):
    cost = simulate_queue(n)
    if cost < best_cost:
        best_cost = cost
        best_servers = n
```

## References
- Fu, M.C. (2002). "Optimization for Simulation: Theory vs. Practice". INFORMS J. on Computing.
- Law, A.M. (2015). "Simulation Modeling and Analysis" (Chapter on optimization)
- Research 1.120 (Simulation libraries in this repository)

## Key Takeaways
1. **Use when objective can't be modeled directly**
2. **Computational cost is main constraint**
3. **Derivative-free methods required** (black-box objective)
4. **Metamodeling reduces evaluations**
5. **Validate optimal solution** with independent runs
