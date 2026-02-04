# Use Case: Mobile App Developer (React Native)

## Who Needs This

**Persona:** Jordan Kim, Mobile Developer at Health Tech Startup

**Background:**
- 4 years React Native experience
- Building fitness tracking app
- Solo mobile developer (small team)
- Shipping on iOS + Android simultaneously

**Technical Context:**
- React Native 0.72, Expo
- Existing UI: React Native Paper
- Offline-first architecture (local SQLite)
- Health metrics (steps, heart rate, sleep)

## Why They Need It

### Core Need

Display health metrics in mobile fitness app with touch interactions.

**Chart requirements:**
- Line charts (daily steps, heart rate trends)
- Bar charts (weekly comparisons)
- Progress arcs (goal completion)
- Touch-friendly (finger targets, not mouse precision)
- Works offline (no web dependencies)
- iOS + Android (single codebase)

### Pain Points Without a Library

**1. Web charts don't work in React Native**
- Recharts: Uses SVG (Web SVG ≠ React Native SVG)
- Chart.js: Uses Canvas (needs react-native-canvas)
- D3: Requires DOM (React Native has no DOM)
- Result: Most charting libraries unusable

**2. React Native SVG differences**
```tsx
// Web SVG
<svg><path d="M 0,0 L 100,100" /></svg>

// React Native SVG
import Svg, { Path } from 'react-native-svg'
<Svg><Path d="M 0,0 L 100,100" /></Svg>
```
Different imports, different APIs.

**3. Touch interactions different**
- Web: Mouse events (hover, click)
- Mobile: Touch events (press, long-press, swipe)
- Tooltips: Can't "hover" on touch screens
- Result: Gesture system must be rethought

**4. Performance constraints**
- Mobile CPUs slower than desktop
- Battery life concerns
- Memory limits tighter
- Result: Need lightweight, efficient charts

### What Success Looks Like

**Cross-platform:**
- Single codebase for iOS + Android
- Native feel on both platforms
- No platform-specific code

**Touch-optimized:**
- Large tap targets (44x44 pts minimum)
- Swipe to navigate time periods
- Long-press for details (not hover)
- Haptic feedback

**Performance:**
- 60 FPS on mid-range phones
- < 50 MB memory footprint
- Minimal battery impact

## Requirements Analysis

### Must-Have
- React Native compatibility (not web charts)
- Touch gestures (pan, zoom, press)
- iOS + Android support
- Offline-capable (no web dependencies)
- Lightweight bundle (< 100 KB)
- Active maintenance

### Nice-to-Have
- Animations (smooth transitions)
- Customization (match app brand)
- TypeScript support

### Don't Need
- Large datasets (< 1000 points)
- Server-side rendering
- Web browser support
- Accessibility (mobile screen readers less critical for this app)

## Library Evaluation

### Option 1: Victory Native ⭐ **RECOMMENDED**

**Pros:**
- ✅ Built for React Native (Web + Native)
- ✅ Touch gestures built-in
- ✅ iOS + Android support
- ✅ Similar API to web (Victory)
- ✅ TypeScript support
- ✅ Active development (Formidable Labs)

**Cons:**
- ❌ 284K weekly downloads (less than web libs)
- ❌ 210 KB bundle (larger)
- ❌ Fewer examples than Recharts

**Code example:**
```tsx
import { VictoryLine, VictoryChart, VictoryAxis } from 'victory-native'

function StepsChart({ data }: { data: StepsData[] }) {
  return (
    <VictoryChart>
      <VictoryAxis />
      <VictoryLine
        data={data}
        x="date"
        y="steps"
        style={{ data: { stroke: "#4ECDC4" } }}
      />
    </VictoryChart>
  )
}
```

**Touch interactions:**
```tsx
import { VictoryZoomContainer } from 'victory-native'

<VictoryChart containerComponent={<VictoryZoomContainer />}>
  {/* Pinch to zoom, pan to navigate */}
</VictoryChart>
```

**Time to first chart:** 2-3 hours

### Option 2: react-native-chart-kit

**Pros:**
- ✅ Designed for React Native
- ✅ Simple API
- ✅ Bezier curves (smooth lines)

**Cons:**
- ❌ Limited chart types (no radar, area)
- ❌ Less customizable
- ❌ Limited gesture support
- ❌ Smaller community

**Why not chosen:** Less flexible, fewer features than Victory.

### Option 3: react-native-svg-charts

**Pros:**
- ✅ Uses react-native-svg directly
- ✅ Lightweight

**Cons:**
- ❌ Archived (no longer maintained)
- ❌ No TypeScript
- ❌ Breaking changes in React Native 0.70+

**Why not chosen:** No longer maintained (critical for mobile).

### Option 4: Recharts (Web Version)

**Pros:**
- ✅ Familiar API

**Cons:**
- ❌ Doesn't work in React Native (uses Web SVG)
- ❌ Requires WebView wrapper (poor performance)

**Why not chosen:** Not compatible with React Native.

### Option 5: D3 + react-native-svg

**Pros:**
- ✅ Maximum control
- ✅ D3 math works in React Native

**Cons:**
- ❌ Must build everything (scales, axes, tooltips)
- ❌ Touch gestures not built-in
- ❌ Weeks of development

**Why not chosen:** Too much work for standard charts.

## Recommended Solution

**Library:** Victory Native

**Why:**
1. **Built for React Native** - Not a web port, native-first
2. **Touch-optimized** - Zoom, pan containers built-in
3. **Cross-platform** - Same code for iOS + Android
4. **Consistent API** - If team knows Victory (web), easy to learn
5. **Well-maintained** - Formidable Labs backing

**Trade-offs accepted:**
- Larger bundle (210 KB) - Features justify size
- Smaller community than Recharts - But active development
- Learning curve - Worth it for mobile-specific features

## Implementation Plan

**Week 1: Setup & Basics**
- Install Victory Native + react-native-svg
- Create first line chart (daily steps)
- Test on iOS + Android simulators
- Real device testing (performance)

**Week 2: Core Charts**
- Bar chart (weekly step comparison)
- Progress arc (daily goal)
- Heart rate chart (time series)
- Touch interactions (zoom, pan)

**Week 3: Polish**
- Custom theme (match app brand)
- Animations (chart entry, data updates)
- Haptic feedback on long-press
- Offline data handling

**Week 4: Testing & Optimization**
- Performance profiling (React DevTools)
- Memory usage monitoring
- Battery impact testing
- Edge cases (empty data, single point)

**Expected outcome:** Production-ready charts in 4 weeks.

## Success Metrics

**Cross-platform:**
- iOS + Android: Identical behavior ✓
- Single codebase: No platform-specific code ✓

**Performance:**
- 60 FPS on iPhone 11 (mid-range) ✓
- Memory: < 30 MB per chart
- Battery: < 2% per hour (background)

**User experience:**
- Touch targets: 44+ pts (Apple HIG)
- Swipe navigation: Smooth
- Haptic feedback: On interactions

## Real-World Example

**Feature: 7-Day Step History**

```tsx
import { VictoryLine, VictoryChart, VictoryAxis, VictoryTheme } from 'victory-native'
import { View, Text, Pressable } from 'react-native'
import * as Haptics from 'expo-haptics'

function WeeklyStepsChart({ data }: Props) {
  const [selectedPoint, setSelectedPoint] = useState<DataPoint | null>(null)

  return (
    <View>
      <VictoryChart theme={VictoryTheme.material}>
        <VictoryAxis
          tickFormat={(date) => new Date(date).toLocaleDateString('en-US', { weekday: 'short' })}
        />
        <VictoryAxis dependentAxis />

        <VictoryLine
          data={data}
          x="date"
          y="steps"
          style={{
            data: { stroke: "#4ECDC4", strokeWidth: 3 }
          }}
          events={[{
            target: 'data',
            eventHandlers: {
              onPressIn: (evt, props) => {
                Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light)
                setSelectedPoint(props.datum)
                return []
              }
            }
          }]}
        />
      </VictoryChart>

      {selectedPoint && (
        <View style={styles.tooltip}>
          <Text>{selectedPoint.date}: {selectedPoint.steps} steps</Text>
        </View>
      )}
    </View>
  )
}
```

**Touch interactions:**
- Press data point → Show tooltip + haptic feedback
- Swipe chart → Navigate to previous/next week
- Pinch → Zoom into specific days

## Mobile-Specific Challenges

### 1. Tooltip on Touch Screens

**Problem:** No "hover" on touch
**Solution:** Long-press or tap to show tooltip

```tsx
events={[{
  target: 'data',
  eventHandlers: {
    onPressIn: (evt, props) => {
      showTooltip(props.datum)
    },
    onPressOut: () => {
      hideTooltip()
    }
  }
}]}
```

### 2. Small Screen Real Estate

**Problem:** Desktop charts too dense for mobile
**Solution:** Simplify, larger tap targets

```tsx
// Desktop: 7 days visible
// Mobile: 3 days visible (swipe for more)
<VictoryChart domain={{ x: [todayMinus3Days, today] }} />
```

### 3. Performance on Older Devices

**Problem:** iPhone 8 struggles with 500 points
**Solution:** Downsample or use simpler chart

```tsx
const displayData = data.length > 100
  ? downsample(data, 100)
  : data
```

### 4. Dark Mode Support

**Problem:** Charts don't match system theme
**Solution:** Detect color scheme, apply theme

```tsx
import { useColorScheme } from 'react-native'

const colorScheme = useColorScheme()
const chartTheme = colorScheme === 'dark' ? darkTheme : lightTheme

<VictoryChart theme={chartTheme} />
```

## Lessons Learned

**What worked:**
- Victory Native: Smooth on both platforms
- Touch events: Long-press better than tap (more intentional)
- Downsampling: 100 points max keeps performance smooth

**What didn't:**
- Tooltips: Hard to dismiss on touch (had to add "tap outside")
- Animations: Too slow on Android (reduced duration)

**Would do differently:**
- Test on real devices earlier (simulators too fast)
- Build design system for chart colors upfront
- Add loading skeletons (data fetch can be slow)

## Related Personas

- **Wearable App Developer** - Similar constraints (small screen, touch)
- **Health Coach Platform** - Mobile-first, similar metrics
- **Fitness Startup** - Cross-platform React Native + charts
