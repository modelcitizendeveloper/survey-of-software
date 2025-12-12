# Data Visualization Libraries - Comparison Matrix

## Quantitative Comparison

| Library | Stars | Weekly DL | Rendering | React-First |
|---------|-------|-----------|-----------|-------------|
| D3.js | 108K | 4.5M | SVG/Canvas | No |
| Chart.js | 64K | 3M | Canvas | No |
| ECharts | 61K | 1M | Canvas/WebGL | No |
| Recharts | 25.6K | 9M | SVG | Yes |
| visx | 19K | 350K | SVG | Yes |
| Nivo | 13.6K | 500K | SVG/Canvas | Yes |
| Victory | 11.2K | 284K | SVG | Yes |

## Feature Matrix

| Feature | Recharts | Chart.js | ECharts | visx | Nivo | Victory | D3 |
|---------|----------|----------|---------|------|------|---------|-----|
| Standard charts | ★★★★★ | ★★★★★ | ★★★★★ | ★★★ | ★★★★★ | ★★★★ | ★★★ |
| Custom viz | ★★ | ★★ | ★★★ | ★★★★★ | ★★★ | ★★★ | ★★★★★ |
| Large datasets | ★★ | ★★★★ | ★★★★★ | ★★ | ★★★ | ★★ | ★★★★ |
| Learning curve | ★★★★★ | ★★★★★ | ★★★ | ★★★ | ★★★★ | ★★★★ | ★ |
| TypeScript | ★★★★★ | ★★★★ | ★★★ | ★★★★★ | ★★★★ | ★★★★ | ★★★ |
| React Native | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| SSR | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| 3D charts | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |
| Geographic | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |

## Rendering Technology

| Renderer | Libraries | Data Point Limit | Interactivity |
|----------|-----------|------------------|---------------|
| SVG | Recharts, visx, Victory, Nivo | ~1000 | Full DOM access |
| Canvas | Chart.js, ECharts | ~50,000 | Event-based |
| WebGL | ECharts-GL, D3 | 100K+ | Limited |

### Performance Comparison

```
Data points vs render time (approximate):

100 points:    SVG ██  Canvas ██  WebGL ██  (all fast)
1,000 points:  SVG ████  Canvas ██  WebGL ██
10,000 points: SVG █████████████  Canvas ████  WebGL ██
100,000 points: SVG (fails)  Canvas ████████  WebGL ████
```

## Decision Matrix by Use Case

### Standard Dashboard Charts
| Priority | Best Choice |
|----------|-------------|
| React ecosystem | **Recharts** |
| Simplicity | Chart.js |
| SSR needed | Nivo |

### Large Datasets (1000+ points)
| Priority | Best Choice |
|----------|-------------|
| Performance | **ECharts** |
| Simplicity | Chart.js |
| Control | D3 + Canvas |

### Custom Visualizations
| Priority | Best Choice |
|----------|-------------|
| React project | **visx** |
| Any project | D3 |
| Network graphs | D3/visx |

### Cross-Platform (React + React Native)
| Priority | Best Choice |
|----------|-------------|
| Same API | **Victory** |
| Only option | Victory |

### Enterprise Requirements
| Priority | Best Choice |
|----------|-------------|
| Commercial support | Highcharts |
| Feature-rich | ECharts |
| Community | Recharts |

## Bundle Size Comparison

```
Approximate bundle sizes (gzipped):

D3 (full):        ████████████████████████████  ~80KB
ECharts (full):   ██████████████████████████    ~70KB
Recharts:         ██████████████████████        ~60KB
Chart.js (full):  ████████████████              ~45KB
Nivo (line):      ██████████████                ~40KB
visx (bar):       ████████                      ~25KB
Chart.js (tree):  ██████                        ~20KB
Victory (line):   ████████                      ~25KB
```

## Migration Paths

### From Chart.js to React
- Use `react-chartjs-2` wrapper
- Or switch to Recharts for React-first DX

### From Recharts to More Power
- Add visx for custom components
- Or ECharts for performance

### From D3 to React
- Use visx (D3 concepts, React components)
- Or Recharts for simplicity

## Quick Reference

### "I need charts quickly"
→ **Recharts** (React) or **Chart.js** (any)

### "I have lots of data"
→ **ECharts** (Canvas/WebGL)

### "I need full control"
→ **D3** (direct) or **visx** (React)

### "I'm building React + React Native"
→ **Victory**

### "I need server-rendered charts"
→ **Nivo**

### "I need commercial support"
→ **Highcharts** (paid license)
