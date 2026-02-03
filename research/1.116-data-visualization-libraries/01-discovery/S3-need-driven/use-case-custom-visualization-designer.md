# Use Case: Custom Visualization Designer

## Who Needs This

**Persona:** Maya Rodriguez, Senior Frontend Engineer at Design Agency

**Background:**
- 8 years experience, React + D3 expertise
- Builds bespoke data visualizations for client websites
- Works with designers on pixel-perfect implementations
- Portfolio-focused (unique work, not templates)

**Technical Context:**
- React + TypeScript
- Figma designs from design team (precise specs)
- Client sites (brand-focused, custom aesthetics)
- < 1000 data points (storytelling, not big data)

## Why They Need It

### Core Need

Create unique, brand-aligned data visualizations that match exact design specifications.

**Visualization requirements:**
- Custom chart types (not standard bar/line/pie)
- Pixel-perfect match to Figma designs
- Complex animations (staggered, choreographed)
- Unusual interactions (drag, scroll-driven)
- Brand-specific aesthetics (custom colors, fonts, shapes)

### Pain Points Without a Library

**1. High-level libraries too limiting**
- Recharts: Can't match custom designs
- Chart.js: Opinionated styling, hard to override
- Result: Fighting the library, not creating

**2. Building from scratch too slow**
- Implementing scales: 2-3 days
- Handling edge cases: 1 week
- Browser testing: 3-4 days
- Result: 2-3 weeks per custom chart

**3. D3 alone doesn't fit React**
- D3 mutations conflict with React
- `.select().data().join()` pattern awkward
- Mixing imperative + declarative code
- Result: Bugs, hydration errors, complexity

**4. Design-dev handoff friction**
- Designers specify exact pixels
- Pre-built charts approximate
- Result: Endless back-and-forth

### What Success Looks Like

**Design fidelity:**
- Pixel-perfect match to Figma (< 2px tolerance)
- Custom animations as specified
- Exact brand colors, fonts, spacing

**Development speed:**
- First custom chart: 2-3 days
- Iteration on design: < 2 hours
- Additional similar charts: 1 day

**Code quality:**
- React-idiomatic (declarative, not imperative)
- Reusable components (not one-offs)
- Maintainable (client can update data)

## Requirements Analysis

### Must-Have
- Full control over SVG elements
- D3 scales and shape generators (not reimplementing)
- React component API (JSX, not DOM manipulation)
- Custom animation support
- TypeScript support
- Small bundle (tree-shakeable)

### Nice-to-Have
- Pre-built axis components (customizable)
- Tooltip primitives (to extend)
- Responsive helpers

### Don't Need
- Built-in chart types (building custom)
- Large dataset support (< 1000 points)
- Canvas rendering (SVG is fine)
- Framework-agnostic (React-specific is fine)

## Library Evaluation

### Option 1: visx ⭐ **RECOMMENDED**

**Pros:**
- ✅ Low-level React primitives (full control)
- ✅ D3 scales + shape generators (don't reimplement)
- ✅ Declarative API (JSX, not DOM mutations)
- ✅ Modular (tree-shakeable, 30-60 KB)
- ✅ TypeScript first-class
- ✅ From Airbnb (well-maintained)

**Cons:**
- ❌ No built-in tooltips/legends (must build)
- ❌ More code than Recharts
- ❌ D3 knowledge required

**Code example:**
```tsx
import { scaleLinear, scaleBand } from '@visx/scale'
import { Bar } from '@visx/shape'
import { AxisBottom, AxisLeft } from '@visx/axis'
import { GridRows } from '@visx/grid'

interface DataPoint {
  category: string
  value: number
}

function CustomBarChart({ data, width, height }: Props) {
  // 1. Create scales (D3 math)
  const xScale = scaleBand<string>({
    domain: data.map(d => d.category),
    range: [0, width],
    padding: 0.3
  })

  const yScale = scaleLinear<number>({
    domain: [0, Math.max(...data.map(d => d.value))],
    range: [height, 0],
    nice: true
  })

  return (
    <svg width={width} height={height}>
      {/* Custom gradient (exact brand colors) */}
      <defs>
        <linearGradient id="brandGradient">
          <stop offset="0%" stopColor="#FF6B6B" />
          <stop offset="100%" stopColor="#4ECDC4" />
        </linearGradient>
      </defs>

      {/* Grid (customized) */}
      <GridRows scale={yScale} width={width} stroke="#E0E0E0" strokeDasharray="4,4" />

      {/* Bars (full control) */}
      {data.map((d, i) => (
        <Bar
          key={i}
          x={xScale(d.category)}
          y={yScale(d.value)}
          width={xScale.bandwidth()}
          height={height - yScale(d.value)}
          fill="url(#brandGradient)"
          rx={8}  // Rounded corners (per design)
          opacity={0.9}
          onMouseEnter={() => {/* Custom hover */}}
        />
      ))}

      {/* Axes (customized) */}
      <AxisBottom
        top={height}
        scale={xScale}
        tickLabelProps={() => ({
          fontFamily: 'Brand Font',
          fontSize: 14,
          fill: '#333'
        })}
      />
      <AxisLeft scale={yScale} />
    </svg>
  )
}
```

**Why it's perfect:**
- D3 scales: Don't reimplement math
- React components: Declarative, fits React model
- Full control: Every pixel customizable
- TypeScript: Catch errors early

**Time to first chart:** 1-2 days (learning visx + implementing design)

### Option 2: D3 (Raw)

**Pros:**
- ✅ Maximum power
- ✅ Can do anything

**Cons:**
- ❌ Imperative API (`.select().join()`)
- ❌ Conflicts with React (DOM mutations)
- ❌ Hydration errors
- ❌ More complex

**Code example:**
```tsx
useEffect(() => {
  d3.select(svgRef.current)
    .selectAll('rect')
    .data(data)
    .join('rect')
    .attr('x', d => xScale(d.category))
    // D3 controls DOM, React unaware
}, [data])
```

**Why not chosen:** Anti-pattern in React, causes bugs.

### Option 3: Recharts

**Pros:**
- ✅ Fast development
- ✅ Built-in features

**Cons:**
- ❌ Can't match custom designs
- ❌ Limited styling hooks
- ❌ Opinionated component structure

**Why not chosen:** Not flexible enough for pixel-perfect designs.

### Option 4: Nivo

**Pros:**
- ✅ Beautiful defaults
- ✅ React components

**Cons:**
- ❌ Higher-level than visx (less control)
- ❌ Harder to customize deeply

**Why not chosen:** Middle ground between Recharts and visx, but visx offers more control.

## Recommended Solution

**Library:** visx + react-spring (for animations)

**Why:**
1. **Full control** - Every SVG element customizable
2. **React-native** - JSX, not D3 DOM mutations
3. **D3 power** - Scales and shapes without reimplementing
4. **Small bundle** - Tree-shakeable (30-60 KB)
5. **TypeScript** - Type-safe custom components

**Trade-offs accepted:**
- More code than Recharts - Worth it for control
- Build tooltips ourselves - Enables custom designs
- D3 knowledge required - Team has expertise

## Implementation Plan

**Project: Custom Annual Report Visualizations**

**Week 1: Foundation**
- Set up visx + react-spring
- Create reusable scale utilities
- Build custom tooltip primitive
- Responsive container helper

**Week 2: Chart 1 (Custom Spiral Timeline)**
- Implement spiral layout algorithm
- Map data to spiral coordinates (visx scales)
- Animated entry (react-spring)
- Hover interactions

**Week 3: Chart 2 (Radial Progress Comparison)**
- Radial layout (not built-in)
- Custom arcs (visx shape generators)
- Staggered animation
- Click interactions

**Week 4: Chart 3 (Flow Sankey Variant)**
- Custom layout algorithm
- Curved paths (visx curves)
- Interactive filtering
- Polish + testing

**Expected outcome:** 3 unique charts in 4 weeks, vs impossible with Recharts.

## Success Metrics

**Design fidelity:**
- Pixel-perfect: < 2px deviation ✓
- Animation timing: Matches design specs ✓
- Brand colors: Exact hex values ✓

**Performance:**
- Bundle size: 45 KB (visx + react-spring)
- Render time: < 16ms (60 FPS)
- Animation smoothness: 60 FPS

**Development:**
- First chart: 2 days
- Subsequent charts: 1-1.5 days
- Design iterations: < 2 hours

## Real-World Example

**Project: Nike Annual Report (Hypothetical)**

**Requirement:** Custom "shoe-shaped" progress chart

**With visx:**
```tsx
import { scaleLinear } from '@visx/scale'
import { curveBasis } from '@visx/curve'
import { LinePath } from '@visx/shape'

// Define shoe outline path
const shoeOutline = "M 10,50 Q 30,20 80,30 L 100,50 ..."

// Use visx scales for data positioning
const progressScale = scaleLinear({
  domain: [0, 100],
  range: [0, shoePathLength]
})

// Fill shoe outline to match progress %
<clipPath id="progressClip">
  <rect width={progressScale(progressPercent)} height="100" />
</clipPath>
<path d={shoeOutline} clipPath="url(#progressClip)" fill="#FF6B6B" />
```

**Result:** Unique, brand-aligned chart that Recharts couldn't create.

## Animation Patterns with visx + react-spring

```tsx
import { useSpring, animated } from 'react-spring'

function AnimatedBar({ x, y, width, height }: Props) {
  const props = useSpring({
    from: { height: 0, opacity: 0 },
    to: { height, opacity: 1 },
    config: { tension: 280, friction: 60 }
  })

  return (
    <animated.rect
      x={x}
      y={props.height.to(h => y + height - h)}
      width={width}
      height={props.height}
      opacity={props.opacity}
    />
  )
}
```

## Lessons Learned

**What worked:**
- visx scales: Saved weeks vs manual math
- React-spring: Smoothest animations
- Modular imports: Kept bundle small
- TypeScript: Caught coordinate math errors

**What didn't:**
- Initial learning curve: visx + D3 concepts take time
- Tooltip positioning: More complex than expected

**Would do differently:**
- Build tooltip library earlier (reuse across projects)
- Create design system for visx components
- Document coordinate systems better

## Related Personas

- **Data Journalism Team** - Custom storytelling visualizations
- **Marketing Agency** - Brand-specific infographics
- **Product Designer** - Custom dashboard components
