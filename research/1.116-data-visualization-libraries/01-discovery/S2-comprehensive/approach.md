# S2-comprehensive: Technical Deep-Dive

## Focus

This pass analyzes the **internal architecture, algorithms, and implementation details** of data visualization libraries. While S1 answered "WHICH library?", S2 answers "HOW does it work?"

## Analysis Framework

For each library, we examine:

### 1. Architecture
- Rendering pipeline (SVG/Canvas/WebGL)
- Component hierarchy and composition
- Data flow and transformation
- Memory management

### 2. Algorithms
- Scale calculations (linear, log, time, band)
- Layout algorithms (force-directed, tree, arc)
- Interpolation methods
- Animation timing functions

### 3. Performance
- Rendering benchmarks (elements/second)
- Bundle size and tree-shaking
- Memory usage patterns
- Optimization strategies

### 4. API Design
- Programming paradigms (declarative vs imperative)
- Type safety and TypeScript support
- Extension points and customization
- Error handling

### 5. Integration Patterns
- Framework-specific bindings (React, Vue, Angular)
- SSR compatibility
- Build tool requirements
- Testing strategies

## Libraries Analyzed

1. **Recharts** - Composable React components
2. **D3.js** - Low-level DOM manipulation
3. **Chart.js** - Imperative Canvas API
4. **ECharts** - Configuration-driven rendering
5. **Nivo** - React wrapper with SSR
6. **visx** - React primitives for D3
7. **Victory** - Cross-platform React Native

## Key Insights from S2

### Rendering Pipeline Trade-offs

**SVG Pipeline** (Recharts, Victory, Nivo)
```
Data → Scale → React Component → SVG Element → DOM
```
- Each data point becomes a DOM node
- Accessible, inspectable, stylable
- Hits performance wall at ~1000 elements

**Canvas Pipeline** (Chart.js, ECharts)
```
Data → Scale → Canvas Context → Bitmap
```
- All points rendered as pixels
- No individual element access
- Handles 1000-50000 points smoothly

**WebGL Pipeline** (ECharts-GL)
```
Data → Scale → Shader → GPU → Frame Buffer
```
- GPU-accelerated geometry
- Handles 50000+ points
- Complex setup, harder debugging

### React Integration Patterns

**Pattern 1: Library Owns DOM** (Recharts, Nivo)
```tsx
<LineChart data={data}>
  <Line dataKey="value" />
</LineChart>
```
- Library renders SVG elements
- React controls when to render
- Easy to use, limited flexibility

**Pattern 2: D3 Math, React Rendering** (visx)
```tsx
const scale = scaleLinear().domain([0, 100]).range([0, 500])
return data.map(d => <circle cx={scale(d.x)} r={5} />)
```
- D3 for calculations only
- React renders DOM
- More control, more code

**Pattern 3: D3 Controls DOM** (Anti-pattern)
```tsx
useEffect(() => {
  d3.select(ref.current).selectAll('rect').data(data).join('rect')
}, [data])
```
- D3 mutates DOM directly
- React unaware of changes
- Breaks React's model

### Performance Bottlenecks

1. **SVG Layout Thrashing** - Reading/writing layout repeatedly
2. **Animation Frame Budget** - Exceeding 16ms per frame
3. **Memory Leaks** - Not cleaning up event listeners
4. **Re-render Cascades** - Unnecessary recalculations

## Comparison by Dimension

See `feature-comparison.md` for detailed side-by-side analysis.
