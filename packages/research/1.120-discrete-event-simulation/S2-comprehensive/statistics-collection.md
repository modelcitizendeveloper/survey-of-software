# Statistics Collection

## Key Research Finding: Philosophy Divide

**SimPy/Ciw/desmod**: Unopinionated (you build your own data collection)
**salabim**: Opinionated (built-in Monitor and Queue statistics)
**Mesa**: Built-in DataCollector for agent properties

## SimPy Approach: Manual Collection

```python
wait_times = []

def customer(env, server):
    arrival = env.now
    with server.request() as req:
        yield req
        wait = env.now - arrival
        wait_times.append(wait)  # Manual tracking

# After simulation
import pandas as pd
df = pd.DataFrame({'wait': wait_times})
print(df['wait'].mean())  # Analyze with pandas
```

**Pros**: Full control, integrate any analysis library
**Cons**: More boilerplate code

## salabim Approach: Built-In Monitors

```python
wait_monitor = sim.Monitor('wait_times')

class Customer(sim.Component):
    def process(self):
        arrival = self.env.now()
        self.request(server)
        wait = self.env.now() - arrival
        wait_monitor.tally(wait)  # Automatic statistics

# Automatic analysis
print(wait_monitor.mean())
print(wait_monitor.std())
print(wait_monitor.percentile(95))
wait_monitor.print_histogram()
```

**Pros**: Less boilerplate, instant statistics
**Cons**: Tied to salabim's Monitor API

## Mesa Approach: DataCollector

```python
def compute_metric(model):
    return sum(agent.wealth for agent in model.schedule.agents)

model.datacollector = mesa.DataCollector(
    model_reporters={"Total Wealth": compute_metric},
    agent_reporters={"Wealth": "wealth"}
)

# Collect each step
model.datacollector.collect(model)

# Retrieve as DataFrame
df = model.datacollector.get_model_vars_dataframe()
```

**Pros**: Built-in for agent properties, time-series data
**Cons**: Mesa-specific, not general DES pattern

## Best Practices (Paradigm-Agnostic)

### 1. Warm-Up Period
Discard initial time when system is empty (not representative).

```python
if env.now > warm_up_time:
    wait_times.append(wait)  # Only collect after warm-up
```

### 2. Time-Average vs Entity-Average
- **Time-average**: Queue length over time (integral)
- **Entity-average**: Wait time per entity (mean)

### 3. Confidence Intervals
Run multiple replications, report mean ± CI.

```python
import numpy as np
results = [run_simulation() for _ in range(30)]
mean = np.mean(results)
ci = 1.96 * np.std(results) / np.sqrt(30)  # 95% CI
print(f"Mean: {mean:.2f} ± {ci:.2f}")
```

## Integration with pandas

All libraries integrate naturally with pandas:

```python
results = []
for rep in range(100):
    metrics = run_simulation()  # Returns dict
    results.append(metrics)

df = pd.DataFrame(results)
df.describe()  # Statistical summary
df.to_csv('results.csv')  # Export
```

## Recommendation

**For quick prototypes**: Use salabim's built-in Monitors (less code)
**For production models**: Use SimPy + pandas (more control, familiar tools)
**For agent models**: Use Mesa's DataCollector (purpose-built for ABM)

## Summary

salabim reduces boilerplate with built-in statistics. SimPy requires manual collection but integrates seamlessly with Python data science ecosystem (pandas, numpy, scipy).
