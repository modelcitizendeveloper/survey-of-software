# Victory

> "React.js components for modular charting and data visualization."

## Quick Facts

| Metric | Value |
|--------|-------|
| GitHub Stars | 11,200 |
| npm Weekly Downloads | ~284K |
| Rendering | SVG |
| License | MIT |
| Maintainer | Nearform (Formidable) |

## Why Victory?

Victory's unique value: **Cross-platform** (React + React Native)

Same API works on web and mobile:
```tsx
// Web
import { VictoryLine } from 'victory'

// React Native
import { VictoryLine } from 'victory-native'
```

## When to Choose Victory

| Scenario | Why Victory |
|----------|-------------|
| React + React Native | Same charting code |
| Composable charts | Modular component system |
| Themeable | Built-in theme support |

## Basic Usage

```tsx
import {
  VictoryChart,
  VictoryLine,
  VictoryAxis,
  VictoryTheme,
} from 'victory'

const data = [
  { x: 1, y: 2 },
  { x: 2, y: 3 },
  { x: 3, y: 5 },
  { x: 4, y: 4 },
]

function Chart() {
  return (
    <VictoryChart theme={VictoryTheme.material}>
      <VictoryLine data={data} />
      <VictoryAxis />
    </VictoryChart>
  )
}
```

## Chart Types

Standard charts:
- Line, Bar, Area, Scatter
- Pie, Polar
- Candlestick, ErrorBar
- Histogram, BoxPlot

## Composable Architecture

Victory's strength is composition:

```tsx
<VictoryChart>
  {/* Combine any elements */}
  <VictoryBar data={barData} />
  <VictoryLine data={lineData} />
  <VictoryScatter data={scatterData} />

  {/* Add annotations */}
  <VictoryAxis label="X Axis" />
  <VictoryAxis dependentAxis label="Y Axis" />

  {/* Add interactivity */}
  <VictoryTooltip />
  <VictoryZoomContainer />
</VictoryChart>
```

## Theming

Built-in themes + custom:

```tsx
import { VictoryTheme } from 'victory'

// Built-in
<VictoryChart theme={VictoryTheme.material} />
<VictoryChart theme={VictoryTheme.grayscale} />

// Custom
const customTheme = {
  axis: {
    style: {
      axis: { stroke: '#ccc' },
      tickLabels: { fill: '#666' },
    },
  },
  line: {
    style: {
      data: { stroke: '#c43a31' },
    },
  },
}

<VictoryChart theme={customTheme} />
```

## Animations

Built-in smooth transitions:

```tsx
<VictoryBar
  animate={{
    duration: 500,
    onLoad: { duration: 500 },
  }}
  data={data}
/>
```

## React Native Support

```tsx
// Install
npm install victory-native react-native-svg

// Use
import { VictoryPie } from 'victory-native'

function MobileChart() {
  return (
    <VictoryPie
      data={[
        { x: 'Cats', y: 35 },
        { x: 'Dogs', y: 40 },
        { x: 'Birds', y: 25 },
      ]}
    />
  )
}
```

## Limitations

1. **SVG only**: Can slow with large datasets
2. **Smaller ecosystem**: Fewer plugins than Chart.js
3. **Less popular**: 284K vs 9M (Recharts)
4. **Learning curve**: API different from other libraries

## Victory vs Alternatives

| Aspect | Victory | Recharts | Chart.js |
|--------|---------|----------|----------|
| React Native | ✅ | ❌ | ❌ |
| Composability | Excellent | Good | Limited |
| Community | Smaller | Large | Huge |
| Performance | SVG | SVG | Canvas |

## When to Use Victory

**Choose Victory when:**
- Building React + React Native app
- Want same charting code everywhere
- Need composable chart system

**Choose alternatives when:**
- Web only → Recharts (more popular)
- Large datasets → ECharts/Chart.js
- Custom visualizations → visx/D3

## Resources

- [Official Docs](https://commerce.nearform.com/open-source/victory/)
- [GitHub](https://github.com/FormidableLabs/victory)
- [victory-native](https://github.com/FormidableLabs/victory-native-xl)
