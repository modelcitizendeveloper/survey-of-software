# 1.116 Data Visualization Libraries - S1 Rapid Discovery

## Quick Decision Guide

| Situation | Recommendation |
|-----------|----------------|
| React dashboard (standard charts) | **Recharts** |
| Custom/complex visualizations | **visx** |
| Large datasets (1000+ points) | **ECharts** or **Chart.js** |
| React Native cross-platform | **Victory** |
| Full creative control | **D3.js** |
| Enterprise with support needs | **Highcharts** (commercial) |

## 2025 Landscape

### Weekly Downloads (npm)

```
Recharts:    ███████████████████████████████████  9M
D3.js:       █████████████████████████            4.5M
Chart.js:    ████████████████████                 3M
ECharts:     ███████████                          1M
Nivo:        ███                                  500K
visx:        ██                                   350K
Victory:     ██                                   284K
```

### GitHub Stars

```
D3.js:       ████████████████████████████████████████████████  108K
Chart.js:    ██████████████████████████████████████            64K
ECharts:     ████████████████████████████████████              61K
Recharts:    █████████████████████████                         25.6K
visx:        ███████████████████                               19K
Nivo:        ██████████████                                    13.6K
Victory:     ███████████                                       11.2K
```

## The Default Choice: Recharts

For **most React dashboards**, Recharts is the answer:

```tsx
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

const data = [
  { name: 'Jan', value: 400 },
  { name: 'Feb', value: 300 },
  { name: 'Mar', value: 600 },
]

function Chart() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="value" stroke="#8884d8" />
      </LineChart>
    </ResponsiveContainer>
  )
}
```

**Why Recharts wins:**
- 9M weekly downloads (32x more than next React-specific library)
- Declarative JSX API
- Built on D3 (solid math)
- Great TypeScript support
- Active maintenance

## When NOT to Use Recharts

| Scenario | Better Choice |
|----------|---------------|
| 1000+ data points | ECharts (WebGL) |
| Network graphs, force layouts | D3.js or visx |
| Highly custom animations | D3.js |
| Server-side rendering | Nivo |
| React + React Native | Victory |
| Need commercial support | Highcharts |

## Library Tiers

### Tier 1: High-Level React (Easiest)
| Library | Best For | Trade-off |
|---------|----------|-----------|
| Recharts | Dashboards | Limited customization |
| Nivo | SSR, variety | Smaller community |
| Victory | Cross-platform | Less popular |

### Tier 2: Low-Level React (More Control)
| Library | Best For | Trade-off |
|---------|----------|-----------|
| visx | Custom D3+React | Steeper learning curve |

### Tier 3: Framework Agnostic (Maximum Power)
| Library | Best For | Trade-off |
|---------|----------|-----------|
| D3.js | Anything custom | Very steep learning curve |
| ECharts | Large datasets | Complex API |
| Chart.js | Quick setup | Less flexible |

## Rendering: SVG vs Canvas vs WebGL

| Renderer | Best For | Limit |
|----------|----------|-------|
| SVG | <1000 points, interactivity | Slows down with many elements |
| Canvas | 1K-50K points | Fast but no DOM manipulation |
| WebGL | 50K+ points | Fastest, complex setup |

**Rule of thumb:**
- Under 1,000 points → SVG (Recharts, Victory)
- 1,000-50,000 points → Canvas (Chart.js, ECharts)
- 50,000+ points → WebGL (ECharts with GL)

## Sources

- [Best React Chart Libraries 2025 - LogRocket](https://blog.logrocket.com/best-react-chart-libraries-2025/)
- [npm trends: nivo vs recharts vs victory](https://npmtrends.com/nivo-vs-recharts-vs-victory)
- [visx - Airbnb](https://github.com/airbnb/visx)
- [Apache ECharts](https://echarts.apache.org/)
