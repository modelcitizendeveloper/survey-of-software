# Simulation-Optimization Coupling

## Research Finding: Simheuristics Pattern

**Simheuristics**: Integration of simulation within metaheuristic frameworks for optimization under uncertainty.

**Academic evidence**: Multiple research papers (2017-2024) document coupling DES with genetic algorithms, particle swarm, simulated annealing.

---

## Common Pattern

```python
def objective_function(decision_variables):
    # decision_variables = [num_servers, buffer_size, ...]
    
    # Run simulation with these parameters
    metrics = run_simulation(decision_variables)
    
    # Return metric to optimize (minimize wait time, maximize throughput)
    return metrics['avg_wait_time']

# Metaheuristic search
from scipy.optimize import minimize
result = minimize(objective_function, x0=initial_guess, method='Nelder-Mead')
```

---

## Common Algorithms (Research Evidence)

### Genetic Algorithms
**Use case**: Multi-objective optimization (minimize cost AND wait time)
**Integration**: ActiveX/OLE Automation or direct Python coupling

### Particle Swarm Optimization
**Use case**: Continuous parameter optimization

### Simulated Annealing
**Use case**: Discrete/combinatorial decisions (which machines to add)

---

## Applications (Academic Literature)

- **Production scheduling**: DES + genetic algorithm for job shop scheduling
- **Inventory optimization**: DES + genetic algorithm for multi-product inventory policies
- **Manufacturing**: DES + metaheuristic for production line tuning

---

## Python Integration

All Python DES libraries integrate naturally with:
- **scipy.optimize**: Nelder-Mead, BFGS, etc.
- **OR-Tools**: Google's optimization library
- **DEAP**: Genetic algorithm library
- **Custom metaheuristics**: Python makes it easy

---

## Example: OR-Tools + SimPy

```python
from ortools.constraint_solver import pywrapcp

solver = pywrapcp.Solver("simulation_optimization")

# Define decision variables
num_servers = solver.IntVar(1, 10, "servers")

# Objective: minimize wait time from simulation
# (OR-Tools would call run_simulation() repeatedly)
```

---

## Challenges

1. **Computational cost**: Each objective evaluation = full simulation run
2. **Stochastic noise**: Simulation output varies (randomness)
3. **Common random numbers**: Ensure fair comparison across scenarios

---

## Summary

Python DES libraries integrate seamlessly with optimization tools (scipy, OR-Tools, DEAP). Simheuristics pattern is well-established in academic research and applicable to industrial problems.
