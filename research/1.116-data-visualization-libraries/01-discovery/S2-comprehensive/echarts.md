# ECharts - Technical Architecture

## Core Philosophy

ECharts (from Apache/Baidu) is a **configuration-driven, enterprise-grade** charting library with Canvas/WebGL rendering for massive datasets.

```javascript
const chart = echarts.init(document.getElementById('container'))
chart.setOption({
  xAxis: { type: 'category', data: ['Mon', 'Tue', 'Wed'] },
  yAxis: { type: 'value' },
  series: [{ data: [120, 200, 150], type: 'line' }]
})
```

## Rendering Architecture

### Multi-Renderer Support

ECharts supports **Canvas** (default) and **SVG** rendering:

```javascript
// Canvas (better for large datasets)
const chart = echarts.init(dom, null, { renderer: 'canvas' })

// SVG (better for small datasets, accessibility)
const chart = echarts.init(dom, null, { renderer: 'svg' })
```

### ZRender (Internal Rendering Engine)

ECharts uses **ZRender** - a lightweight 2D drawing library:

```
ECharts Config → ZRender Elements → Canvas/SVG Context → Pixels/DOM
```

**ZRender features:**
- Shape primitives (rect, circle, path, text, image)
- Event system (hover, click, drag)
- Animation engine
- Layer management (for performance)

## Performance: The Big Data Champion

### Benchmark Results

| Renderer | Data Points | Render Time | Interactive |
|----------|-------------|-------------|-------------|
| Canvas | 10,000 | ~50ms | Yes (smooth) |
| Canvas | 100,000 | ~200ms | Yes (60 FPS) |
| Canvas | 1,000,000 | ~1.5s | Laggy |
| WebGL | 1,000,000 | ~300ms | Yes (smooth) |
| WebGL | 10,000,000 | ~2s | Yes (60 FPS) |

**ECharts GL (WebGL extension):**
```javascript
import 'echarts-gl'

series: [{
  type: 'scatter3D',  // 3D scatter plot
  data: millionPoints,
  symbolSize: 2
}]
```

### Performance Optimizations

**1. Progressive Rendering**
```javascript
series: [{
  type: 'line',
  data: hugeDataset,
  progressive: 5000,        // Render 5000 points per frame
  progressiveThreshold: 10000  // Enable if > 10K points
}]
```

**2. Sampling**
```javascript
series: [{
  type: 'line',
  data: hugeDataset,
  sampling: 'lttb'  // Largest-Triangle-Three-Buckets
}]
```

**3. Data Zoom (Virtual Scrolling)**
```javascript
dataZoom: [{
  type: 'slider',
  start: 0,
  end: 10  // Show only 10% of data initially
}]
```
Only visible data is rendered = massive performance gain.

**4. Large Mode**
```javascript
series: [{
  type: 'scatter',
  large: true,           // Enable large mode
  largeThreshold: 2000,  // Activate if > 2000 points
  data: points
}]
```
Disables hover on individual points, renders as batch.

## Configuration System

### Option Object Structure

```javascript
{
  // Title
  title: {
    text: 'Sales Dashboard',
    subtext: 'Q1 2025',
    left: 'center'
  },

  // Tooltip
  tooltip: {
    trigger: 'axis',  // or 'item', 'none'
    formatter: '{b}: {c}'  // Template or function
  },

  // Legend
  legend: {
    data: ['Sales', 'Profit'],
    bottom: 0
  },

  // Grid (chart area)
  grid: {
    left: '10%',
    right: '10%',
    bottom: '15%',
    containLabel: true
  },

  // Axes
  xAxis: {
    type: 'category',  // or 'value', 'time', 'log'
    data: ['Mon', 'Tue', 'Wed'],
    axisLine: { lineStyle: { color: '#666' } },
    axisTick: { show: false }
  },

  yAxis: {
    type: 'value',
    axisLabel: { formatter: '{value} K' },
    splitLine: { lineStyle: { type: 'dashed' } }
  },

  // Data Zoom (pan/zoom controls)
  dataZoom: [
    { type: 'slider', start: 0, end: 100 },
    { type: 'inside' }  // Mouse wheel zoom
  ],

  // Toolbox (export, zoom, restore)
  toolbox: {
    feature: {
      saveAsImage: {},  // Export as PNG
      dataZoom: {},     // Box zoom
      restore: {},      // Reset
      dataView: {}      // Show data table
    }
  },

  // Series (the actual data)
  series: [{
    name: 'Sales',
    type: 'line',  // or 'bar', 'pie', 'scatter', 'heatmap', etc.
    data: [120, 200, 150, 80, 70, 110],
    smooth: true,  // Bezier curve smoothing
    areaStyle: {},  // Fill area under line
    emphasis: {
      focus: 'series'  // Highlight on hover
    }
  }]
}
```

## Chart Types (100+)

### Basic Charts
- Line, Area, Bar (stacked, grouped)
- Pie, Donut, Rose (Nightingale)
- Scatter, Bubble
- Candlestick (stock charts)
- Radar, Gauge, Funnel

### Advanced Charts
- Heatmap, Treemap
- Sankey (flow diagrams)
- Graph (network, force-directed)
- Parallel coordinates
- Boxplot, K-line

### 3D Charts (with echarts-gl)
- Scatter3D, Bar3D, Line3D
- Surface3D (3D surface plots)
- Globe (geographic 3D)

### Geographic
- Map (GeoJSON support)
- Heatmap on map
- Flow lines on map

## Coordinate Systems

ECharts supports multiple coordinate systems in one chart:

```javascript
{
  xAxis: { /* Cartesian X */ },
  yAxis: { /* Cartesian Y */ },
  polar: { /* Polar coordinates */ },
  geo: { /* Geographic */ },

  series: [
    { type: 'bar', coordinateSystem: 'cartesian2d' },
    { type: 'line', coordinateSystem: 'polar' },
    { type: 'scatter', coordinateSystem: 'geo' }
  ]
}
```

## Visual Encoding

Map data to visual properties:

```javascript
visualMap: {
  type: 'continuous',  // or 'piecewise'
  min: 0,
  max: 100,
  dimension: 2,  // Which data dimension
  inRange: {
    color: ['#50a3ba', '#eac736', '#d94e5d']  // Gradient
  }
}
```

Automatically colors data points based on value.

## Responsive Design

### Container Size

```javascript
// Auto-resize on window resize
window.addEventListener('resize', () => {
  chart.resize()
})
```

### Media Queries

```javascript
option: {
  baseOption: { /* Default config */ },
  media: [
    {
      query: { maxWidth: 500 },
      option: {
        legend: { bottom: 0 },
        grid: { left: 50 }
      }
    },
    {
      query: { minWidth: 500 },
      option: {
        legend: { right: 0 },
        grid: { left: 100 }
      }
    }
  ]
}
```

## Animation

### Built-in Animations

```javascript
animation: true,
animationDuration: 1000,
animationEasing: 'cubicOut',
animationDelay: (idx) => idx * 50  // Stagger
```

**Easing functions:**
- Linear, quadratic, cubic, quartic
- Elastic, bounce, back

### Update Animations

```javascript
chart.setOption(newOption, {
  notMerge: false,  // Merge with existing option
  lazyUpdate: false,
  silent: false
})
```

Automatically animates transitions between states.

## Bundle Size

```
echarts (full): 1.1 MB (uncompressed), ~320 KB gzipped

Tree-shaking (modular):
import * as echarts from 'echarts/core'
import { LineChart, BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

echarts.use([LineChart, BarChart, GridComponent, TooltipComponent, CanvasRenderer])

Result: ~150 KB gzipped (with only needed components)
```

**Comparison:**
- ECharts (modular): 150 KB gzipped
- Recharts: 130 KB gzipped
- Chart.js: 60 KB gzipped ✓

ECharts is heavier, but handles 100x more data.

## TypeScript Support

**Type Coverage:** Good (ships with types)

```typescript
import * as echarts from 'echarts/core'
import type { EChartsOption } from 'echarts'

const option: EChartsOption = {
  xAxis: { type: 'category', data: ['Mon', 'Tue'] },
  yAxis: { type: 'value' },
  series: [{ type: 'line', data: [120, 200] }]
}

const chart = echarts.init(document.getElementById('main')!)
chart.setOption(option)
```

## React Integration

### echarts-for-react (Community)

```tsx
import ReactECharts from 'echarts-for-react'

function App() {
  const option = {
    xAxis: { type: 'category', data: ['Mon', 'Tue', 'Wed'] },
    yAxis: { type: 'value' },
    series: [{ type: 'line', data: [120, 200, 150] }]
  }

  return <ReactECharts option={option} />
}
```

**Wrapper handles:**
- Chart initialization
- Option updates
- Resize on container change
- Cleanup on unmount

## Accessibility

### SVG Renderer

```javascript
const chart = echarts.init(dom, null, { renderer: 'svg' })
```

SVG output is more accessible than Canvas:
- Screen readers can parse SVG elements
- Each element selectable/inspectable

### ARIA Support

```javascript
aria: {
  enabled: true,
  label: 'Sales chart showing upward trend',
  decal: {
    show: true  // Adds patterns for colorblind users
  }
}
```

Decal patterns help distinguish series without color.

## Internationalization

Built-in language packs:

```javascript
import 'echarts/i18n/langEN'
import 'echarts/i18n/langZH'

const chart = echarts.init(dom, 'en')  // or 'zh'
```

## Key Strengths

1. **Massive datasets** - 10M points with WebGL
2. **100+ chart types** - Most comprehensive library
3. **Enterprise features** - Data zoom, export, theming
4. **Great docs** - Chinese + English, many examples
5. **Active development** - Apache Foundation backing

## Key Limitations

1. **Large bundle** - 320 KB full, 150 KB tree-shaken
2. **Complex API** - Steep learning curve
3. **Imperative** - Not React-idiomatic (config objects)
4. **Overkill for simple charts** - Use Recharts instead

## When to Use ECharts

**Ideal for:**
- 10,000+ data points
- Enterprise dashboards
- Need many chart types
- Geographic visualizations
- 3D charts

**Not ideal for:**
- Simple charts with < 1000 points (use Recharts)
- React-first projects preferring JSX (use Recharts)
- Bundle size critical (use Chart.js)
- Custom novel visualizations (use D3)
