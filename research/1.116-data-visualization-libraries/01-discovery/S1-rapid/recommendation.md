# Data Visualization Library Recommendation Guide

## Quick Decision Tree

```
Start Here
│
├─ What framework?
│  ├─ React → Continue below
│  ├─ React Native → Victory
│  ├─ Vue/Angular/Vanilla → Chart.js or ECharts
│  └─ Any (maximum control) → D3.js
│
├─ React: How many data points?
│  ├─ < 500 points → Recharts ✓
│  ├─ 500 - 5000 → Chart.js or Recharts
│  └─ > 5000 → ECharts (Canvas/WebGL)
│
├─ React: Standard or custom charts?
│  ├─ Standard (bar, line, pie) → Recharts ✓
│  ├─ Custom (network, force) → visx
│  └─ Many chart types → Nivo
│
└─ Special requirements?
   ├─ Server-side rendering → Nivo
   ├─ Geographic maps → ECharts or visx
   ├─ 3D charts → ECharts-GL
   └─ Commercial support → Highcharts
```

## The Default: Recharts

For **most React dashboards**, use Recharts:

```tsx
npm install recharts
```

**Why:**
- 9M weekly downloads (dominant)
- Declarative JSX API
- Great TypeScript support
- Built on D3 (solid math)
- Active maintenance

```tsx
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

<ResponsiveContainer width="100%" height={300}>
  <LineChart data={data}>
    <XAxis dataKey="name" />
    <YAxis />
    <Tooltip />
    <Line dataKey="value" stroke="#8884d8" />
  </LineChart>
</ResponsiveContainer>
```

---

## Recommendations by Scenario

### 1. Standard React Dashboard

**Recommended**: Recharts

- Line charts, bar charts, pie charts
- Interactive tooltips, legends
- Responsive design

```tsx
npm install recharts
```

---

### 2. Large Datasets (1000+ data points)

**Recommended**: ECharts

SVG-based libraries (Recharts, Victory) struggle with 1000+ points. ECharts uses Canvas/WebGL:

```tsx
npm install echarts echarts-for-react
```

Or for 50K+ points, use WebGL:
```javascript
series: [{ type: 'scatterGL', data: massiveDataset }]
```

---

### 3. Custom Visualizations

**Recommended**: visx

Need network graphs, custom force layouts, or unusual charts? visx gives D3 power with React idioms:

```tsx
npm install @visx/scale @visx/shape @visx/axis
```

Pick only packages you need (excellent tree-shaking).

---

### 4. Cross-Platform (React + React Native)

**Recommended**: Victory

Same API works on web and mobile:

```tsx
// Web
npm install victory

// Mobile
npm install victory-native react-native-svg
```

Same code, both platforms.

---

### 5. Server-Side Rendered Charts

**Recommended**: Nivo

Unique SSR API for generating charts on server:

```tsx
npm install @nivo/line @nivo/bar
```

Use case: Email reports, PDFs, static sites.

---

### 6. Simple Charts, Any Framework

**Recommended**: Chart.js

Fastest setup, works everywhere:

```tsx
npm install chart.js
```

For React: `npm install react-chartjs-2`

---

### 7. Enterprise with Support Requirements

**Recommended**: Highcharts (Commercial)

- Professional support
- Accessibility certified
- Long-term maintenance

Requires commercial license for business use.

---

## What NOT to Do

### Don't Use D3 for Standard Charts
D3 is a low-level toolkit. For bar/line/pie charts, use Recharts - it uses D3 under the hood anyway.

### Don't Use SVG Libraries for Large Data
SVG struggles past ~1000 data points. Switch to Canvas (Chart.js, ECharts).

### Don't Build Your Own Charting Library
Unless you have specific needs, existing libraries handle edge cases you haven't thought of.

---

## Library Tiers

### Tier 1: Start Here
| Library | Use For |
|---------|---------|
| Recharts | React dashboards |
| Chart.js | Quick charts, any framework |

### Tier 2: Specific Needs
| Library | Use For |
|---------|---------|
| ECharts | Large datasets, 3D, maps |
| visx | Custom visualizations |
| Victory | React + React Native |
| Nivo | SSR, variety |

### Tier 3: Special Cases
| Library | Use For |
|---------|---------|
| D3.js | Maximum control, custom everything |
| Highcharts | Enterprise, commercial support |
| Plotly | Scientific, 3D |

---

## Performance Summary

| Data Size | Recommended | Why |
|-----------|-------------|-----|
| < 500 | Recharts | Simplicity |
| 500-5000 | Chart.js | Canvas faster |
| 5000-50000 | ECharts | Optimized Canvas |
| 50000+ | ECharts-GL | WebGL required |

---

## Final Recommendations

### For Most React Projects
**Recharts** - Dominant, simple, effective

### For Large Datasets
**ECharts** - Canvas/WebGL performance

### For Custom Visualizations
**visx** - D3 power, React idioms

### For Cross-Platform
**Victory** - Only real option

### For Enterprise
**Highcharts** - Commercial support (or ECharts)
