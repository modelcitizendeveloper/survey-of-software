# Chart.js

> "Simple yet flexible JavaScript charting library."

## Quick Facts

| Metric | Value |
|--------|-------|
| GitHub Stars | 64,000 |
| npm Weekly Downloads | ~3M |
| Rendering | Canvas |
| License | MIT |
| React Wrapper | react-chartjs-2 |

## Why Chart.js?

Chart.js is the **simplest way** to add charts to any project:

1. **Tiny**: ~60KB gzipped (with tree-shaking)
2. **Fast**: Canvas rendering
3. **Simple API**: Works in minutes
4. **Framework agnostic**: Works anywhere
5. **Huge ecosystem**: 100s of plugins

## Core Concept: Canvas Performance

Chart.js renders to Canvas (not SVG):
- Faster for 1000+ points
- Lower memory usage
- Smaller file size
- No DOM bloat

Trade-off: Can't select/style individual elements with CSS.

## React Integration

```tsx
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'
import { Line } from 'react-chartjs-2'

// Register components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

function LineChart() {
  const data = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr'],
    datasets: [
      {
        label: 'Sales',
        data: [65, 59, 80, 81],
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
    ],
  }

  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: 'Monthly Sales' },
    },
  }

  return <Line data={data} options={options} />
}
```

## Chart Types

Built-in (8 types):
- Line, Bar, Pie, Doughnut
- Radar, Polar Area
- Bubble, Scatter

## Key Features

### Responsive by Default
```javascript
options: {
  responsive: true,
  maintainAspectRatio: true,
}
```

### Animations
```javascript
options: {
  animation: {
    duration: 1000,
    easing: 'easeOutQuart',
  },
}
```

### Plugins
```javascript
import zoomPlugin from 'chartjs-plugin-zoom'
ChartJS.register(zoomPlugin)

options: {
  plugins: {
    zoom: {
      zoom: { wheel: { enabled: true } },
      pan: { enabled: true },
    },
  },
}
```

## Tree-Shaking (v3+)

Only import what you need:

```javascript
// Full bundle (~60KB)
import Chart from 'chart.js/auto'

// Tree-shaken (~20KB for simple line chart)
import { Chart, LineElement, PointElement, LineController, CategoryScale, LinearScale } from 'chart.js'
Chart.register(LineElement, PointElement, LineController, CategoryScale, LinearScale)
```

## Limitations

1. **Limited chart types**: 8 built-in (vs 20+ in ECharts)
2. **Less customizable**: No arbitrary shapes
3. **Canvas limitations**: Can't CSS style elements
4. **No geographic maps**: Need plugins

## Chart.js vs Alternatives

| Aspect | Chart.js | Recharts | ECharts |
|--------|----------|----------|---------|
| Setup time | Minutes | Minutes | Hours |
| Bundle | ~20-60KB | ~100KB | ~100KB+ |
| Chart types | 8 | 12 | 20+ |
| Rendering | Canvas | SVG | Canvas/WebGL |
| Customization | Moderate | Limited | High |
| React-first | No | Yes | No |

## When to Use Chart.js

**Choose Chart.js when:**
- Need quick, simple charts
- Bundle size matters
- Using vanilla JS or any framework
- Standard chart types sufficient
- Want lots of plugin options

**Choose alternatives when:**
- Need React-first → Recharts
- Need 10K+ points → ECharts
- Need custom visualizations → visx/D3

## Resources

- [Official Docs](https://www.chartjs.org/)
- [GitHub](https://github.com/chartjs/Chart.js)
- [react-chartjs-2](https://react-chartjs-2.js.org/)
- [Plugin Directory](https://github.com/chartjs/awesome)
