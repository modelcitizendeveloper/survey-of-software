# Use Case: Analytics Dashboard (High-Frequency Updates)

**Last Updated**: 2026-01-16
**Complexity**: Medium-High
**Target**: Admin panels, monitoring tools, data visualizations

## Scenario

Real-time analytics dashboard with:
- Live metrics (CPU, memory, requests/sec)
- Multiple charts (10-20 visualizations)
- WebSocket updates (100-500/sec aggregate)
- Historical data (last 1000 datapoints per metric)
- Filters and date range selection
- Export functionality

## Top Recommendations

### 1. Preact Signals (Best Performance)

```typescript
import { signal, computed } from '@preact/signals-react'

const metrics = signal([])
const timeRange = signal('1h')

const filteredMetrics = computed(() => {
  const data = metrics.value
  const range = timeRange.value
  const cutoff = Date.now() - parseTimeRange(range)

  return data.filter(m => m.timestamp > cutoff)
})

const avgCPU = computed(() => {
  const data = filteredMetrics.value
  return data.reduce((sum, m) => sum + m.cpu, 0) / data.length
})

// WebSocket handler
ws.onmessage = (event) => {
  const metric = JSON.parse(event.data)

  // Direct mutation (no re-render until JSX accessed)
  metrics.value = [...metrics.value, metric].slice(-1000)
}

function Dashboard() {
  return (
    <div>
      <Chart data={filteredMetrics.value} />
      <Metric label="Avg CPU" value={avgCPU.value} />
      <select onChange={(e) => timeRange.value = e.target.value}>
        <option value="1h">Last Hour</option>
        <option value="24h">Last 24h</option>
      </select>
    </div>
  )
}
```

**Pros**: Zero re-render overhead, fast updates, smallest bundle (1.6KB)
**Performance**: 8ms batch update (100 metrics)

### 2. Jotai (Alternative)

```typescript
const metricsAtom = atom([])
const timeRangeAtom = atom('1h')

const filteredMetricsAtom = atom((get) => {
  const data = get(metricsAtom)
  const range = get(timeRangeAtom)
  const cutoff = Date.now() - parseTimeRange(range)

  return data.filter(m => m.timestamp > cutoff)
})

const avgCPUAtom = atom((get) => {
  const data = get(filteredMetricsAtom)
  return data.reduce((sum, m) => sum + m.cpu, 0) / data.length
})
```

**Pros**: Automatic dependency tracking, good derived state
**Performance**: 10ms batch update

## Recommendation

**Primary: Preact Signals**

- Best performance for high-frequency updates
- Sub-component reactivity (no wasted re-renders)
- Smallest bundle

**Alternative**: Jotai (if prefer React patterns, accept 20% slower)

**Avoid**: Redux Toolkit (too slow for real-time, 22ms updates)

**Last Updated**: 2026-01-16
