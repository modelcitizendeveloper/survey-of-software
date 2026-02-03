# Chart.js - Technical Architecture

## Core Philosophy

Chart.js is an **imperative, configuration-driven** Canvas charting library. You provide a config object, it renders to Canvas.

```javascript
new Chart(ctx, {
  type: 'line',
  data: { /* ... */ },
  options: { /* ... */ }
})
```

## Rendering Architecture

### Canvas-First Design

Unlike SVG libraries (Recharts, D3), Chart.js renders to Canvas:

```javascript
const canvas = document.querySelector('canvas')
const ctx = canvas.getContext('2d')

// Chart.js draws pixels directly
ctx.fillRect(x, y, width, height)
ctx.stroke()
```

**Implications:**
- Fast for 1000-50000 data points
- No individual element access (all pixels)
- Less accessible (no DOM nodes for screen readers)
- Harder to customize (no CSS styling)

### Rendering Pipeline

```
Config Object → Chart Instance → Rendering Engine → Canvas Context → Pixels
```

**Detailed steps:**
1. **Parse config** - Validate chart type, data, options
2. **Calculate layout** - Determine axis positions, label spacing
3. **Generate scales** - Map data values to pixel coordinates
4. **Render elements** - Draw axes, grid, data points, labels
5. **Register interactions** - Set up hover/click handlers
6. **Animation loop** - Interpolate values over time

## Chart Types

Built-in chart types (extensible):

### Basic
- `line` - Time series, trends
- `bar` - Comparisons (vertical/horizontal)
- `pie` / `doughnut` - Part-to-whole
- `radar` - Multivariate data
- `polarArea` - Circular bar chart
- `scatter` - X-Y relationships
- `bubble` - X-Y-Z (size as 3rd dimension)

### Mixed
```javascript
{
  type: 'line',
  data: {
    datasets: [
      { type: 'line', data: [...] },
      { type: 'bar', data: [...] }
    ]
  }
}
```

## Configuration Structure

```javascript
new Chart(ctx, {
  type: 'line',

  data: {
    labels: ['Jan', 'Feb', 'Mar'],  // X-axis labels
    datasets: [{
      label: 'Sales',
      data: [10, 20, 15],
      borderColor: 'rgb(75, 192, 192)',
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
      tension: 0.1  // Line curvature
    }]
  },

  options: {
    responsive: true,
    maintainAspectRatio: true,
    aspectRatio: 2,  // width:height ratio

    scales: {
      x: {
        type: 'linear',  // or 'category', 'time', 'logarithmic'
        title: { display: true, text: 'Month' }
      },
      y: {
        beginAtZero: true,
        ticks: { callback: (value) => `$${value}` }
      }
    },

    plugins: {
      legend: { display: true, position: 'top' },
      tooltip: { enabled: true, mode: 'index' },
      title: { display: true, text: 'Sales Dashboard' }
    },

    interaction: {
      mode: 'nearest',  // or 'index', 'point', 'dataset'
      intersect: false
    },

    animation: {
      duration: 1000,
      easing: 'easeInOutQuart'
    }
  }
})
```

## Scale System

Chart.js has its own scale implementations (not D3).

### Scale Types

**1. Linear Scale**
```javascript
scales: {
  y: {
    type: 'linear',
    min: 0,
    max: 100,
    ticks: {
      stepSize: 10,
      callback: (value) => value + '%'
    }
  }
}
```

**2. Logarithmic Scale**
```javascript
scales: {
  y: { type: 'logarithmic' }
}
```

**3. Category Scale** (discrete)
```javascript
scales: {
  x: {
    type: 'category',
    labels: ['A', 'B', 'C']
  }
}
```

**4. Time Scale** (requires date-fns or moment.js)
```javascript
import 'chartjs-adapter-date-fns'

scales: {
  x: {
    type: 'time',
    time: {
      unit: 'day',
      displayFormats: { day: 'MMM d' }
    }
  }
}
```

## Performance Characteristics

### Benchmark Results

| Data Points | Render Time | Frame Rate |
|-------------|-------------|------------|
| 100 | ~3ms | 333 FPS |
| 1,000 | ~12ms | 83 FPS |
| 10,000 | ~80ms | 12 FPS |
| 50,000 | ~450ms | 2 FPS |

**Performance ceiling: ~10,000 points for smooth interaction**

### Why Canvas is Faster than SVG

1. **No DOM overhead** - Single Canvas element, not 1000s of SVG nodes
2. **Direct pixel manipulation** - Bypasses layout/paint pipeline
3. **GPU acceleration** - Modern browsers use GPU for Canvas

### Optimization Strategies

**1. Data Decimation** (built-in)
```javascript
options: {
  parsing: false,  // Assume data is pre-parsed
  decimation: {
    enabled: true,
    algorithm: 'lttb',  // Largest-Triangle-Three-Buckets
    samples: 500
  }
}
```

**LTTB Algorithm:**
- Downsamples 10,000 points → 500 points
- Preserves visual shape
- ~10x performance improvement

**2. Disable Animations**
```javascript
options: { animation: false }
```

**3. Reduce Update Frequency**
```javascript
chart.update('none')  // No animation
// vs
chart.update()  // Default animation
```

## Bundle Size

```
chart.js: 242 KB (uncompressed)
chart.js: ~60 KB (gzipped)
```

**Tree-shaking:** Not supported well
- Must import entire library
- Use auto-tree-shaking bundler (Webpack 5+)

**Comparison:**
- Recharts: 130 KB gzipped
- Chart.js: 60 KB gzipped ✓ (smaller)

## Plugin System

Chart.js is highly extensible via plugins.

### Built-in Plugins

```javascript
import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

Chart.register(
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  Title,
  Tooltip,
  Legend
)
```

### Custom Plugin

```javascript
const customPlugin = {
  id: 'customPlugin',

  beforeDraw(chart, args, options) {
    const { ctx, chartArea } = chart
    ctx.fillStyle = 'rgba(255, 0, 0, 0.1)'
    ctx.fillRect(chartArea.left, chartArea.top, chartArea.width, chartArea.height)
  },

  afterDatasetDraw(chart, args, options) {
    // Called after each dataset renders
  }
}

Chart.register(customPlugin)
```

**Plugin hooks:**
- `beforeInit`, `afterInit`
- `beforeUpdate`, `afterUpdate`
- `beforeDraw`, `afterDraw`
- `beforeDatasetDraw`, `afterDatasetDraw`
- 20+ hooks total

## Animation System

### Configuration

```javascript
options: {
  animation: {
    duration: 1000,
    easing: 'easeOutQuart',
    delay: (context) => context.dataIndex * 50,  // Stagger
    loop: false,

    // Specific animations
    x: { duration: 2000 },  // X-axis animation
    y: { duration: 1000 }   // Y-axis animation
  }
}
```

**Easing functions:**
- Linear: `linear`
- Ease: `easeInQuad`, `easeOutQuad`, `easeInOutQuad`
- Cubic, Quart, Quint, Expo, Circ, Back, Elastic

### Animation Events

```javascript
options: {
  onProgress(animation) {
    console.log(`Progress: ${animation.currentStep / animation.numSteps}`)
  },
  onComplete(animation) {
    console.log('Animation finished')
  }
}
```

## Responsive Design

### Auto-Resize

```javascript
options: {
  responsive: true,
  maintainAspectRatio: true,
  aspectRatio: 2  // width:height
}
```

**Implementation:**
- Uses `ResizeObserver` (with polyfill)
- Redraws chart on container resize
- Debounced to avoid excessive redraws

### Manual Size Control

```javascript
chart.resize(width, height)
```

## Interaction Modes

### Hover/Click Behavior

```javascript
options: {
  interaction: {
    mode: 'index',      // 'point', 'nearest', 'dataset', 'x', 'y'
    intersect: false,   // Trigger on axis, not just point
    axis: 'x'           // Only consider x-axis distance
  }
}
```

**Modes:**
- `point` - Hover directly over point
- `nearest` - Closest point to cursor
- `index` - All points at same x-index
- `dataset` - All points in dataset
- `x` / `y` - Points along axis

### Custom Interactions

```javascript
canvas.onclick = (evt) => {
  const points = chart.getElementsAtEventForMode(
    evt,
    'nearest',
    { intersect: true },
    false
  )

  if (points.length) {
    const { datasetIndex, index } = points[0]
    console.log(chart.data.datasets[datasetIndex].data[index])
  }
}
```

## Accessibility

### Limitations

Canvas is inherently less accessible:
- No DOM elements for screen readers
- No keyboard navigation
- Difficult to provide alt text for individual data points

### Mitigations

```html
<canvas aria-label="Sales chart showing upward trend">
  Fallback: Sales increased from $100 in Jan to $300 in Mar
</canvas>
```

**Accessibility plugins:**
- [chartjs-plugin-a11y-legend](https://github.com/julianna-langston/chartjs-plugin-a11y-legend)
- Adds keyboard navigation
- ARIA labels for data points

## React Integration

### react-chartjs-2 (Official Wrapper)

```tsx
import { Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

function App() {
  const data = {
    labels: ['Jan', 'Feb', 'Mar'],
    datasets: [{ data: [10, 20, 15] }]
  }

  return <Line data={data} options={{ responsive: true }} />
}
```

**Wrapper handles:**
- Canvas element creation
- Chart instance management
- Update/destroy lifecycle
- TypeScript types

## TypeScript Support

**Type Coverage:** Excellent

```typescript
import { ChartConfiguration, ChartType } from 'chart.js'

const config: ChartConfiguration<'line'> = {
  type: 'line',
  data: {
    labels: ['A', 'B'],
    datasets: [{
      label: 'Dataset',
      data: [1, 2]
    }]
  }
}

// Custom types
interface CustomDataPoint {
  x: number
  y: number
  label: string
}

const scatterConfig: ChartConfiguration<'scatter', CustomDataPoint[]> = {
  type: 'scatter',
  data: {
    datasets: [{
      data: [
        { x: 1, y: 2, label: 'Point A' },
        { x: 3, y: 4, label: 'Point B' }
      ]
    }]
  }
}
```

## Key Strengths

1. **Canvas performance** - Handles 10K points smoothly
2. **Simple API** - Config object easier than D3
3. **Small bundle** - 60 KB gzipped
4. **Great docs** - Comprehensive, well-organized
5. **Active maintenance** - Regular releases

## Key Limitations

1. **Less flexible than D3** - Opinionated chart types
2. **Accessibility** - Canvas harder for screen readers
3. **Customization limits** - Harder to style than SVG
4. **No React-native API** - Imperative, not declarative

## When to Use Chart.js

**Ideal for:**
- 1,000-10,000 data points
- Framework-agnostic projects (Vue, Angular, vanilla JS)
- Performance-critical dashboards
- Teams prioritizing simplicity

**Not ideal for:**
- Custom visualizations (use D3)
- React-first projects (Recharts more idiomatic)
- Heavy accessibility requirements (use SVG libraries)
