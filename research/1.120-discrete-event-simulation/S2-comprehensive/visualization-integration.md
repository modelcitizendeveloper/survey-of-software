# Visualization Integration

## Key Research Finding: salabim is Unique

**salabim** is the ONLY Python DES library with built-in 2D/3D animation. All others require manual matplotlib/plotly integration.

## Built-In Animation Capabilities

### salabim: Integrated Animation Engine
```python
import salabim as sim

class VisualCustomer(sim.Component):
    def setup(self):
        sim.AnimateCircle(radius=10, fillcolor='red', parent=self)
    
    def process(self):
        self.enter(queue)  # Visually animates movement
        self.request(server)
```

**Features**: 2D/3D shapes, real-time animation, automatic positioning

### Mesa: Built-In Grid Visualizer
```python
from mesa.visualization.modules import CanvasGrid

grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)
server = mesa.visualization.ModularServer(
    Model, [grid], "Model", model_params
)
server.launch()
```

**Features**: Web-based visualization, grid/network display, charts

### SimPy/Ciw/desmod: NO Built-In Visualization
Must integrate matplotlib, plotly, or other libraries manually.

## Manual Visualization Patterns

### matplotlib Integration (Static Plots)
```python
import matplotlib.pyplot as plt

# After simulation
plt.hist(wait_times, bins=30)
plt.xlabel('Wait Time')
plt.ylabel('Frequency')
plt.show()

# Time-series plot
plt.plot(timestamps, queue_lengths)
plt.xlabel('Time')
plt.ylabel('Queue Length')
plt.show()
```

### plotly Integration (Interactive)
```python
import plotly.express as px

df = pd.DataFrame({'wait': wait_times})
fig = px.histogram(df, x='wait', nbins=30)
fig.show()  # Opens in browser
```

### Streamlit/Dash (Web Dashboards)
```python
import streamlit as st

st.title('Simulation Dashboard')
st.line_chart(df['queue_length'])
st.metric('Avg Wait', f"{df['wait'].mean():.2f}")
```

## Animation for Presentation

**Problem**: Static plots don't engage stakeholders.

**Solutions**:
1. **Use salabim**: Built-in animation (if switching libraries is feasible)
2. **matplotlib.animation**: Create animated plots in SimPy
3. **Web-based**: D3.js visualization with SimPy backend
4. **Record screen**: Run real-time simulation (SimPy), record with OBS

## Recommendation by Use Case

| Need | Library | Approach |
|------|---------|----------|
| **Quick static plots** | Any | matplotlib/plotly |
| **Interactive dashboards** | Any | Streamlit/Dash |
| **Built-in animation** | salabim | Use AnimateCircle, AnimateRectangle |
| **Agent visualization** | Mesa | Built-in CanvasGrid |
| **Presentation demos** | salabim | Real-time animation |

## Summary

salabim's built-in animation is a **major differentiator** for presentation-heavy projects. For data analysis (histograms, time-series), all libraries integrate equally well with matplotlib/pandas.

If animation is critical, start with salabim. If analysis is primary, any library works (integrate matplotlib manually).
