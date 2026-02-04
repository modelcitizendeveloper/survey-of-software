# Real-Time vs Batch Simulation

## Research Finding: Real-Time Widely Supported

Both **SimPy** and **salabim** support wall-clock synchronization (real-time mode).

## Batch Simulation (Default Mode)

**How it works**: Simulation runs "as fast as possible," jumping from event to event without wall-clock delay.

**Use cases**:
- Capacity planning (run 10k simulation days in minutes)
- Monte Carlo replication (run 100 replications quickly)
- Optimization (simulation within optimization loop)

**All libraries**: SimPy, salabim, Ciw, Mesa, desmod support batch mode.

## Real-Time Simulation

**How it works**: Synchronize simulation clock with wall-clock time (1 sim-second = 1 real-second).

### SimPy Implementation:
```python
import simpy.rt

env = simpy.rt.RealtimeEnvironment(factor=1.0)  # Real-time
# factor=0.1 → 10x faster than real-time
# factor=10 → 10x slower

env.run(until=100)  # Takes 100 real seconds (if factor=1.0)
```

**strict mode** (default): Raises error if computation can't keep up with real-time.

### salabim Implementation:
```python
env = sim.Environment()
env.run(till=100, real_time=True, speed=1.0)  # Real-time
# speed=10 → 10x faster
```

## Use Cases for Real-Time Mode

1. **Interactive demonstrations**: Visualize simulation progressing in real-time for stakeholders
2. **Hardware-in-the-loop**: Interface simulation with physical hardware (sensors, actuators)
3. **Educational tools**: Students watch events unfold at comprehensible pace
4. **Human-in-the-loop**: Operator makes decisions during simulation run

## When NOT to Use Real-Time

- **Large-scale simulations**: 10k simulation days would take months of real-time
- **Monte Carlo replication**: Need speed, not real-time visualization
- **Optimization**: Simulation called 1000s of times, real-time would be impractical

## Libraries Without Real-Time Support

**Ciw, Mesa, desmod**: No documented real-time synchronization feature (as of October 2025).

**Workaround**: Can build custom real-time wrapper using `time.sleep()`, but not built-in.

## Summary

Real-time simulation is useful for **demos and education**, not production analysis. SimPy and salabim provide built-in support; others do not.
