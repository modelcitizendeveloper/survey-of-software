# Integration Patterns

## Pattern 1: pandas for Data Management

**All libraries** integrate naturally with pandas for results storage and analysis.

```python
results = []
def customer(env, server):
    arrival = env.now
    # ... simulation logic ...
    results.append({'arrival': arrival, 'wait': wait, 'service': service})

# After simulation
df = pd.DataFrame(results)
df.describe()  # Statistics
df.to_csv('results.csv')  # Export
df.groupby('customer_type').mean()  # Segmentation
```

---

## Pattern 2: Optimization Coupling (Simheuristics)

**Research finding**: "Simheuristics" pattern couples metaheuristics with DES for simulation-based optimization.

```python
from scipy.optimize import minimize

def objective(params):
    num_servers = int(params[0])
    avg_wait = run_simulation(num_servers)  # DES call
    return avg_wait  # Minimize

result = minimize(objective, x0=[5], method='Nelder-Mead')
optimal_servers = int(result.x[0])
```

**Common algorithms**:
- Genetic algorithms
- Particle swarm
- Simulated annealing
- OR-Tools integration

---

## Pattern 3: Web Dashboards

**Streamlit** (quick prototypes):
```python
import streamlit as st

num_servers = st.slider('Servers', 1, 10, 5)
metrics = run_simulation(num_servers)
st.metric('Avg Wait', f"{metrics['wait']:.2f}")
st.line_chart(metrics['queue_over_time'])
```

**Dash** (production dashboards):
```python
import dash
from dash import dcc, html

app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Slider(id='servers', min=1, max=10),
    dcc.Graph(id='results')
])
# Callback runs simulation on slider change
```

---

## Pattern 4: Database Integration

**Store parameters and results** in database for experiment tracking:

```python
import sqlite3

conn = sqlite3.connect('experiments.db')

# Store experiment
conn.execute('''
    INSERT INTO experiments (num_servers, avg_wait, timestamp)
    VALUES (?, ?, ?)
''', (num_servers, avg_wait, datetime.now()))

# Retrieve historical results
df = pd.read_sql('SELECT * FROM experiments', conn)
```

---

## Pattern 5: Monte Carlo Replication

Run simulation N times with different random seeds:

```python
import numpy as np

def run_replication(seed):
    np.random.seed(seed)
    return run_simulation()

results = [run_replication(seed) for seed in range(100)]
mean = np.mean(results)
ci = 1.96 * np.std(results) / np.sqrt(len(results))
print(f"Mean: {mean:.2f} ± {ci:.2f}")
```

---

## Summary

Python DES libraries integrate seamlessly with:
- **pandas**: Data management
- **scipy/OR-Tools**: Optimization
- **Streamlit/Dash**: Dashboards
- **SQL databases**: Experiment tracking
- **numpy**: Statistical analysis
