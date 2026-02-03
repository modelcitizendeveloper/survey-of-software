# Use Case: Data Scientist with Large Datasets

## Who Needs This

**Persona:** Dr. Alex Chen, Research Data Scientist at FinTech Company

**Background:**
- PhD in Statistics, 5 years industry experience
- Analyzes trading patterns, fraud detection
- Works in Python (Jupyter) + web interface for stakeholders
- Publishes findings to executives monthly

**Technical Context:**
- Python backend (pandas, NumPy)
- Web frontend for interactive exploration
- Datasets: 10K-1M data points (stock prices, transactions)
- Needs: zoom, pan, filter, export

## Why They Need It

### Core Need

Visualize large time-series datasets for pattern discovery and stakeholder communication.

**Chart requirements:**
- Time series (stock prices, anomaly detection)
- Heatmaps (correlation matrices)
- Scatter plots (clustering, outliers)
- 3D surface plots (parameter optimization)
- Interactive controls (zoom, pan, brush selection)

### Pain Points Without a Library

**1. Performance with large datasets**
- Plotting 100K points in Jupyter: slow
- Web visualization of 100K points: browser crashes
- Result: Forced to downsample, lose detail

**2. Static vs Interactive trade-off**
- Matplotlib/Seaborn: Static images, no interaction
- Plotly: Interactive but slow with 50K+ points
- Result: Can't explore data fluidly

**3. Stakeholder communication**
- Executives need web dashboards, not Jupyter notebooks
- Need professional-looking, interactive charts
- Must export to PowerPoint/PDF

**4. Framework knowledge gap**
- Expert in Python, not JavaScript/React
- Don't want to learn complex frontend frameworks
- Result: Struggle with web visualization tools

### What Success Looks Like

**Performance:**
- 100K points: Smooth 60 FPS interaction
- 1M points: Usable (30 FPS) with WebGL

**Workflow:**
- Analyze in Python → Export data
- Build web dashboard with minimal JS knowledge
- Stakeholders explore interactively

**Features:**
- Zoom/pan (explore time windows)
- Export charts (PNG, SVG for reports)
- Data zoom slider (virtual scrolling)
- Multiple coordinated views (linked brushing)

## Requirements Analysis

### Must-Have
- Handle 10K-1M data points smoothly
- Canvas or WebGL rendering (not SVG)
- Interactive controls (zoom, pan, brush)
- Export functionality (PNG, PDF)
- Time series optimizations
- Framework-agnostic (or simple wrapper)

### Nice-to-Have
- 3D chart support
- Heatmap support
- Geographic visualizations
- Chinese + English docs (team is multilingual)

### Don't Need
- React-specific API (not a React expert)
- Mobile responsiveness (desktop tool)
- Server-side rendering
- Tiny bundle size (rich features more important)

## Library Evaluation

### Option 1: ECharts ⭐ **RECOMMENDED**

**Pros:**
- ✅ Handles 100K points smoothly (Canvas)
- ✅ WebGL extension for 1M+ points (echarts-gl)
- ✅ Built-in data zoom, pan controls
- ✅ Export to PNG built-in
- ✅ 100+ chart types (heatmaps, 3D, geo)
- ✅ Framework-agnostic (simple JavaScript)
- ✅ Excellent Chinese + English documentation

**Cons:**
- ❌ 320 KB full bundle (150 KB tree-shaken)
- ❌ Config-driven API (learning curve)

**Code example:**
```javascript
const chart = echarts.init(document.getElementById('main'))

chart.setOption({
  xAxis: { type: 'time' },
  yAxis: { type: 'value' },

  // Data zoom for interactive exploration
  dataZoom: [
    { type: 'slider', start: 0, end: 10 },
    { type: 'inside' }  // Mouse wheel zoom
  ],

  // Toolbox for export
  toolbox: {
    feature: {
      dataZoom: {},
      saveAsImage: {}  // Export PNG
    }
  },

  series: [{
    type: 'line',
    data: largeDataset,  // 100K points
    sampling: 'lttb',    // Downsample visually
    large: true          // Large dataset mode
  }]
})
```

**Performance:**
- 10K points: 60 FPS
- 100K points: 60 FPS (with sampling)
- 1M points: 60 FPS (with WebGL)

**Time to first chart:** 2-3 hours (learning config structure)

### Option 2: Plotly.js

**Pros:**
- ✅ Python integration (plotly.py)
- ✅ 40+ chart types (scientific charts)
- ✅ 3D charts built-in
- ✅ WebGL support

**Cons:**
- ❌ Performance ceiling ~50K points
- ❌ Large bundle (> 3 MB uncompressed)
- ❌ Slower than ECharts at scale

**Why not chosen:** Performance doesn't match ECharts for large datasets.

### Option 3: Chart.js

**Pros:**
- ✅ Handles 10K points smoothly
- ✅ Small bundle (60 KB)
- ✅ Simple API

**Cons:**
- ❌ Performance ceiling ~10K points
- ❌ Limited chart types (no heatmap, 3D)
- ❌ No built-in data zoom controls

**Why not chosen:** Can't handle 100K+ point datasets.

### Option 4: D3

**Pros:**
- ✅ Maximum flexibility
- ✅ Can use Canvas for performance

**Cons:**
- ❌ Steep learning curve (JavaScript + D3 API)
- ❌ Must build zoom/pan controls yourself
- ❌ No export functionality built-in
- ❌ Weeks to build what ECharts provides

**Why not chosen:** Too much JavaScript expertise required.

## Recommended Solution

**Library:** ECharts (with echarts-gl for 3D)

**Why:**
1. **Performance at scale** - 100K points smoothly, 1M+ with WebGL
2. **Built-in controls** - Data zoom, pan, export (saves weeks)
3. **Rich chart library** - Heatmaps, 3D, geo maps all built-in
4. **Framework-agnostic** - Minimal JavaScript knowledge needed
5. **Enterprise backing** - Apache Foundation, active development

**Trade-offs accepted:**
- Bundle size (150-320 KB) - Features justify size
- Config API learning curve - Worth it for built-in features
- Not Python-native - But simple JavaScript integration

## Implementation Plan

**Week 1: Setup & Learning**
- Install ECharts, echarts-gl
- Build first time series with data zoom
- Test performance with real datasets (100K points)
- Set up export workflow

**Week 2: Core Charts**
- Time series anomaly detection chart
- Correlation heatmap
- Scatter plot for clustering
- 3D surface for parameter space

**Week 3: Dashboard Integration**
- Create reusable chart templates
- Wire up to Python data pipeline
- Add responsive container
- Stakeholder review

**Week 4: Polish**
- Custom theme (match company brand)
- Tooltip customization
- Export to PDF workflow
- Documentation

**Expected outcome:** Production dashboard in 1 month, vs 3+ months building custom.

## Success Metrics

**Performance:**
- 100K points: 60 FPS ✓
- 1M points (WebGL): 30+ FPS ✓
- Initial load: < 2 seconds

**Workflow:**
- Python → JSON → ECharts: Automated pipeline
- Stakeholder self-serve: Interactive exploration
- Report generation: PNG export → PowerPoint

**Adoption:**
- Executives use dashboard monthly
- Reduced ad-hoc chart requests by 80%
- Faster insight discovery (interactive vs static)

## Real-World Example

**Fraud Detection Dashboard:**

**Dataset:** 500K transactions per day

**Charts:**
- Time series: Transaction volume (500K points, data zoom)
- Heatmap: Fraud score by hour/day
- Scatter: Amount vs velocity (anomaly highlighting)
- Geo map: Transactions by location

**Performance:**
```javascript
// Enable large mode for 500K points
series: [{
  type: 'scatter',
  large: true,
  largeThreshold: 2000,
  data: transactions,  // 500K points
  symbolSize: 2
}]
```

**Result:** Smooth interaction, fraud analysts zoom into suspicious patterns, catch fraud 2 days faster on average.

## Lessons Learned

**What worked:**
- Data zoom slider: Stakeholders love interactive exploration
- Export PNG: Easy to include charts in reports
- LTTB sampling: Visually identical, 10x faster

**What didn't:**
- Initial learning curve: Config structure takes time
- WebGL setup: More complex than expected

**Would do differently:**
- Start with ECharts examples gallery (copy-paste-modify)
- Use tree-shaking earlier (reduce bundle size)
- Test 3D charts earlier (some were unnecessary)

## Related Personas

- **Financial Analyst** - Similar needs (time series, large data)
- **IoT Engineer** - Sensor data visualization (time series, heatmaps)
- **Bioinformatics Researcher** - Genomic data (large datasets, specialized charts)
