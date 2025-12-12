# Apache ECharts

> "An open-source JavaScript visualization library."

## Quick Facts

| Metric | Value |
|--------|-------|
| GitHub Stars | 61,000 |
| npm Weekly Downloads | ~1M |
| Rendering | Canvas/SVG/WebGL |
| License | Apache 2.0 |
| Maintainer | Apache Foundation |

## Why ECharts?

ECharts is the **performance champion** for large datasets:

1. **Canvas/WebGL**: Handles 10K-100K+ data points
2. **Feature-rich**: 20+ chart types, maps, 3D
3. **Enterprise-ready**: Used by major companies
4. **Mobile-optimized**: Small, modular bundle

## When to Choose ECharts

| Scenario | Why ECharts |
|----------|-------------|
| 1000+ data points | Canvas beats SVG |
| 50000+ data points | WebGL support |
| Real-time dashboards | Efficient updates |
| Geographic maps | Built-in support |
| 3D visualizations | ECharts-GL |

## React Integration

```tsx
// Using echarts-for-react wrapper
import ReactECharts from 'echarts-for-react'

function Chart() {
  const option = {
    xAxis: {
      type: 'category',
      data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
    },
    yAxis: {
      type: 'value',
    },
    series: [
      {
        data: [120, 200, 150, 80, 70],
        type: 'bar',
      },
    ],
  }

  return <ReactECharts option={option} />
}
```

**Note**: The `echarts-for-react` wrapper is somewhat outdated. For production, consider a custom wrapper:

```tsx
import { useEffect, useRef } from 'react'
import * as echarts from 'echarts'

function EChart({ option }) {
  const ref = useRef(null)
  const chartRef = useRef(null)

  useEffect(() => {
    chartRef.current = echarts.init(ref.current)
    return () => chartRef.current?.dispose()
  }, [])

  useEffect(() => {
    chartRef.current?.setOption(option)
  }, [option])

  return <div ref={ref} style={{ width: '100%', height: 400 }} />
}
```

## Configuration-Based API

ECharts uses a declarative options object:

```javascript
const option = {
  title: { text: 'Sales Report' },
  tooltip: { trigger: 'axis' },
  legend: { data: ['Sales', 'Returns'] },
  xAxis: { type: 'category', data: months },
  yAxis: { type: 'value' },
  series: [
    { name: 'Sales', type: 'line', data: salesData },
    { name: 'Returns', type: 'bar', data: returnsData },
  ],
}
```

## Chart Types

ECharts supports 20+ chart types:

**Standard:**
- Line, Bar, Pie, Scatter
- Radar, Heatmap, Treemap
- Candlestick, Boxplot

**Advanced:**
- Sankey, Sunburst, Graph (network)
- Map (geographic)
- Parallel coordinates
- Funnel, Gauge

**3D (with ECharts-GL):**
- 3D Bar, Line, Scatter
- Surface, Globe
- Flow

## Performance: Large Datasets

```javascript
// Enable large mode for 10K+ points
series: [{
  type: 'scatter',
  large: true,
  largeThreshold: 2000,
  data: largeDataset // 100K points OK
}]

// For 100K+ points, use WebGL
series: [{
  type: 'scatterGL', // Requires echarts-gl
  data: massiveDataset
}]
```

## Limitations

1. **Complex API**: Many options to learn
2. **React wrapper outdated**: May need custom integration
3. **Bundle size**: Full library is large (use modular imports)
4. **Styling**: Less flexible than D3/visx

## ECharts vs Alternatives

| Aspect | ECharts | Recharts | D3 |
|--------|---------|----------|-----|
| Performance | Excellent | Good | Depends |
| Chart variety | 20+ | 10 | Unlimited |
| Learning curve | Moderate | Easy | Steep |
| Customization | Good | Limited | Maximum |
| React integration | OK | Excellent | Manual |

## Resources

- [Official Docs](https://echarts.apache.org/)
- [Examples](https://echarts.apache.org/examples/)
- [GitHub](https://github.com/apache/echarts)
- [echarts-for-react](https://github.com/hustcc/echarts-for-react)
