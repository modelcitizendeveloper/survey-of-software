# salabim: Discrete Event Simulation with Animation

## Key Research Discovery

**salabim offers a "yieldless" API** that doesn't require Python `yield` statements. This is a significant usability advantage for Python beginners compared to SimPy.

## Overview

- **Repository**: https://github.com/salabim/salabim
- **PyPI**: https://pypi.org/project/salabim/
- **Latest version**: 25.0.12 (October 2025)
- **License**: MIT
- **GitHub stars**: ~100-200
- **First release**: ~2018
- **JOSS paper**: Published 2018
- **Documentation**: https://www.salabim.org/manual/

## Unique Features

### 1. Yieldless API (Major Differentiator)

Research finding: salabim does NOT require `yield` statements for process control, making it more intuitive than SimPy.

**SimPy approach** (requires yield):
```python
def customer(env, server):
    with server.request() as req:
        yield req  # MUST yield
        yield env.timeout(5)  # MUST yield
```

**salabim approach** (yieldless):
```python
class Customer(sim.Component):
    def process(self):
        self.request(server)  # No yield needed
        self.hold(5)  # No yield needed
```

**Implication**: Lower learning curve for Python developers unfamiliar with generators.

### 2. Built-In Statistics

Unlike SimPy (manual data collection), salabim has powerful Monitor and Queue objects that automatically track statistics.

```python
# Automatic tracking
wait_time_monitor = sim.Monitor('wait_times')
wait_time_monitor.tally(value)  # Add data point

# Automatic statistics
print(wait_time_monitor.mean())  # Average
print(wait_time_monitor.std())  # Standard deviation
print(wait_time_monitor.percentile(95))  # 95th percentile
```

### 3. Built-In Animation Engine

**UNIQUE**: salabim has integrated 2D/3D animation capabilities. SimPy has none.

```python
import salabim as sim

class VisualCustomer(sim.Component):
    def setup(self):
        sim.AnimateCircle(radius=10, fillcolor='red', parent=self)
    
    def process(self):
        self.enter(waiting_queue)
        # Customer visually moves to queue position
        self.request(server)
        self.leave(waiting_queue)
        # Visual animation of service
```

**Use case**: Presentations, stakeholder demos, educational tools.

## Installation

```bash
pip install salabim
```

For visualization (optional):
```bash
pip install salabim[animation]
```

## Minimal Example: Queue System

```python
import salabim as sim

class Customer(sim.Component):
    def process(self):
        arrival_time = self.env.now()
        print(f"{self.name()} arrives at {arrival_time:.1f}")
        
        self.enter(waiting_queue)
        self.request(server)
        self.leave(waiting_queue)
        
        wait = self.env.now() - arrival_time
        wait_monitor.tally(wait)
        
        self.hold(sim.Exponential(4).sample())  # Service time
        print(f"{self.name()} departs at {self.env.now():.1f}")

class CustomerGenerator(sim.Component):
    def process(self):
        while True:
            Customer()
            self.hold(sim.Exponential(5).sample())  # Inter-arrival

# Setup
env = sim.Environment()
server = sim.Resource('Server')
waiting_queue = sim.Queue('WaitingQueue')
wait_monitor = sim.Monitor('WaitTimes')

CustomerGenerator()
env.run(till=100)

# Statistics automatically available
print(f"Average wait: {wait_monitor.mean():.2f}")
print(f"Queue length: {waiting_queue.length.mean():.2f}")
```

## Strengths (Evidence-Based)

1. **Yieldless API**: Easier learning curve than SimPy (no yield statements)
2. **Built-in statistics**: Monitor and Queue objects auto-track metrics
3. **Built-in animation**: 2D/3D visualization engine (unique among Python DES)
4. **Real-time mode**: Factor parameter for wall-clock sync
5. **Cross-platform**: Windows, macOS, Linux, iOS/iPadOS (Pythonista), Python in Excel
6. **Minimal requirements**: Lightweight when animation disabled
7. **MIT license**: Permissive

## Limitations (Research Findings)

1. **Smaller community**: ~100-200 GitHub stars vs SimPy's larger ecosystem
2. **Less documentation**: Comprehensive manual exists, but fewer tutorials/examples than SimPy
3. **Greenlet dependency**: Uses greenlets for yieldless API (additional dependency)

## Performance Note

Research finding: salabim uses **greenlet coroutines** for performance. No comprehensive benchmarks exist comparing to SimPy, but salabim claims "minimal overhead" when animation is disabled.

## When to Choose salabim

**Best for**:
- **Python beginners**: Yieldless API is more intuitive
- **Visualization-heavy projects**: Built-in animation for demos/presentations
- **Statistics-focused models**: Built-in Monitor objects reduce boilerplate

**Consider SimPy instead if**:
- You need largest community support
- You're comfortable with Python generators
- You want maximum ecosystem maturity (20+ years vs ~7 years)

## Learning Resources

- **Official manual**: https://www.salabim.org/manual/
- **Sample models**: Included with package
- **JOSS paper**: "salabim: discrete event simulation and animation in Python" (2018)

## API Comparison: salabim vs SimPy

| Feature | salabim | SimPy |
|---------|---------|-------|
| **Process definition** | Class-based, yieldless | Generator functions with yield |
| **Statistics** | Built-in Monitor objects | Manual (pandas integration) |
| **Animation** | Built-in 2D/3D | None (integrate matplotlib) |
| **Learning curve** | Lower (no yield) | Moderate (requires yield understanding) |
| **Community** | Smaller | Larger |
| **Maturity** | ~7 years | 20+ years |

## Research Gap Identified

No comprehensive performance benchmarks comparing salabim to SimPy were found. Both claim efficiency, but quantitative comparison is missing from public sources.

## Summary

salabim is an **excellent alternative to SimPy** for users who want:
- Easier API (yieldless)
- Built-in statistics
- Built-in animation

Trade-off: Smaller community and shorter track record than SimPy.

**Recommendation**: Try salabim first if you're new to DES and Python generators intimidate you. Fall back to SimPy if you need more community support or encounter edge cases.

See S2-comprehensive/modeling-paradigms.md for detailed comparison and S3-need-driven/learning-curve.md for time-to-competency analysis.
