# S2 Technical Recommendations

## Decision Framework: Architecture-First

Choose based on **technical architecture requirements**, not popularity:

### 1. Styling Architecture Decision

**Question**: What styling approach does your team use?

```
├─ Tailwind CSS
│  ├─ Want pre-built components → shadcn/ui
│  └─ Building from primitives → Headless UI
│
├─ CSS Modules / Vanilla CSS
│  ├─ Want comprehensive library → Mantine
│  └─ Building design system → Radix UI
│
└─ CSS-in-JS (Emotion, styled-components)
   ├─ Prop-based styling preference → Chakra UI
   ├─ Material Design required → MUI
   └─ Enterprise/data-heavy → Ant Design
```

### 2. Performance Requirements

**Question**: What are your bundle/performance constraints?

| Requirement | Recommendation | Bundle Size | Runtime Cost |
|-------------|---------------|-------------|--------------|
| **< 20 KB total** | Headless UI or Radix UI | ~8-15 KB | Zero |
| **< 50 KB total** | shadcn/ui or Mantine | ~20-35 KB | Zero (static CSS) |
| **< 100 KB total** | Chakra UI | ~45 KB | Low (Emotion cached) |
| **No constraint** | MUI or Ant Design | ~70-85 KB | Medium (CSS-in-JS) |

**Runtime performance ranking:**
1. Headless UI + Tailwind (static classes)
2. Radix UI + CSS Modules (static CSS)
3. Mantine v7 (CSS Modules)
4. shadcn/ui (CVA + Tailwind)
5. Chakra UI (Emotion cached)
6. MUI (Emotion runtime)
7. Ant Design (token system + CSS-in-JS)

### 3. Component Coverage Needs

**Question**: What components do you absolutely need?

| Need | Best Choice | Why |
|------|------------|-----|
| **Advanced data tables** | Ant Design | Best-in-class Table with sorting, filtering, pagination, fixed columns, virtual scrolling |
| **Date/time pickers** | Mantine or Ant Design | Comprehensive date components (Mantine free, Ant Design free, MUI X paid) |
| **Form handling** | Ant Design or Mantine | Powerful form libraries (@ant-design/form, @mantine/form) |
| **Rich text editor** | Mantine | @mantine/tiptap built-in (others need third-party) |
| **File upload** | Mantine | @mantine/dropzone built-in |
| **Command palette** | Mantine | @mantine/spotlight built-in |
| **Basic components only** | Headless UI or Radix UI | Overlays, menus, navigation - build the rest |

**Component count (free):**
- Mantine: 120+ (most comprehensive)
- Ant Design: 60+ (enterprise focus)
- MUI: 50+ core (MUI X paid)
- Chakra UI: 50+
- shadcn/ui: 40+
- Radix UI: 25+ primitives
- Headless UI: 14 components

### 4. Customization Depth

**Question**: How much customization do you need?

```
Full Custom Design System (from scratch)
├─ React-only → Radix UI
└─ Need Vue support → Headless UI
   │
   └─ Then consider wrapping like shadcn/ui does

Moderate Customization (theme existing library)
├─ Easiest via props → Chakra UI
├─ Best theming system → Mantine
└─ Need Material base → MUI

Minimal Customization (use defaults)
├─ Material Design → MUI
├─ Enterprise aesthetic → Ant Design
└─ Modern minimalist → Mantine or Chakra
```

## Technical Architecture Patterns

### Pattern 1: Headless + Styling Layer

**Best for**: Maximum control, custom design systems

**Architecture:**
```
Radix UI (behavior/a11y) + Tailwind CSS (styling) + CVA (variants) = shadcn/ui pattern
```

**Example implementation:**
```tsx
// 1. Start with Radix primitive
import * as DialogPrimitive from '@radix-ui/react-dialog'

// 2. Add Tailwind styling layer
const DialogContent = ({ children, ...props }) => (
  <DialogPrimitive.Portal>
    <DialogPrimitive.Overlay className="fixed inset-0 bg-black/50" />
    <DialogPrimitive.Content
      className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2
                 max-w-md rounded-lg bg-white p-6 shadow-xl"
      {...props}
    >
      {children}
    </DialogPrimitive.Content>
  </DialogPrimitive.Portal>
)

// 3. Add variants with CVA
import { cva } from 'class-variance-authority'

const dialogVariants = cva('rounded-lg bg-white p-6', {
  variants: {
    size: {
      sm: 'max-w-sm',
      md: 'max-w-md',
      lg: 'max-w-lg',
    },
  },
})
```

**Pros:**
- Complete styling control
- Smallest possible bundle
- Perfect accessibility
- No library updates break your styles

**Cons:**
- More initial setup
- Must build component layer yourself
- Need CSS/Tailwind proficiency

### Pattern 2: Full-Featured Library

**Best for**: Rapid development, standard applications

**Architecture:**
```
Mantine or Chakra UI (complete system)
```

**Example implementation:**
```tsx
import { MantineProvider } from '@mantine/core'
import { Button, Modal, Table } from '@mantine/core'

// Theme once, use everywhere
<MantineProvider theme={{ primaryColor: 'blue' }}>
  <App />
</MantineProvider>
```

**Pros:**
- Everything included (components + hooks + forms + dates)
- Fast time-to-market
- Consistent DX across all components
- Minimal setup

**Cons:**
- Larger bundle (but still reasonable)
- Some unused features bundled
- Less styling control
- Design system opinions baked in

### Pattern 3: Enterprise Pre-Styled

**Best for**: Enterprise applications, data-heavy dashboards

**Architecture:**
```
Ant Design or MUI (established enterprise libraries)
```

**Example implementation:**
```tsx
import { ConfigProvider } from 'antd'
import { Table, Form, DatePicker } from 'antd'

<ConfigProvider theme={{ token: { colorPrimary: '#00b96b' } }}>
  <App />
</ConfigProvider>
```

**Pros:**
- Advanced components (data tables, complex forms)
- Proven at scale (Alibaba, Netflix, Spotify)
- Enterprise features out-of-box
- Commercial support available

**Cons:**
- Largest bundles
- Strong visual identity (hard to customize away)
- CSS-in-JS overhead (MUI, Ant v5)
- Premium features may require payment (MUI X)

## Technical Migration Paths

### From Bootstrap → Modern Libraries

**Easiest**: Chakra UI (prop-based similar to Bootstrap classes)
```tsx
// Bootstrap
<div className="d-flex justify-content-between align-items-center p-4">

// Chakra UI
<Flex justify="space-between" align="center" p={4}>
```

**Alternative**: Mantine (comprehensive like Bootstrap)

### From Material-UI v4 → Modern

**Stay in ecosystem**: MUI v5 (codemod available)
```bash
npx @mui/codemod v5.0.0/preset-safe src/
```

**Switch to headless**: Radix UI + Tailwind (rewrites but full control)

### From Custom CSS → Component Library

**If using Tailwind**: shadcn/ui (keeps Tailwind patterns)

**If not using Tailwind**: Mantine (CSS Modules, familiar patterns)

### From CSS-in-JS → Modern

**2025 trend**: Move away from runtime CSS-in-JS

- **Mantine v6 → v7**: Emotion → CSS Modules (official migration)
- **Chakra v2 → v3**: Moving to zero-runtime (Panda CSS)
- **Alternative**: Switch to shadcn/ui or Headless UI (no CSS-in-JS)

## Testing Architecture

### For Maximum Test Stability

**Choose**: Mantine v7, Radix UI, Headless UI, or shadcn/ui

**Why**: Static CSS = stable snapshots
```tsx
// Generated class: "Button_root__abc123" (stable across runs)
<button className="rounded-lg bg-blue-500 px-4 py-2">
  Click me
</button>
```

### If Using CSS-in-JS Libraries

**Avoid**: Snapshot testing

**Instead**: Test behavior and DOM structure
```tsx
// ❌ Snapshot (breaks on CSS-in-JS updates)
expect(container).toMatchSnapshot()

// ✅ Behavior + structure
expect(screen.getByRole('button')).toHaveTextContent('Click me')
expect(screen.getByRole('button')).toHaveClass('MuiButton-root')
```

## SSR/Framework-Specific Recommendations

### Next.js App Router

**Best**: Mantine, shadcn/ui, Headless UI, Radix UI
- No special config needed
- Server Components compatible
- Excellent hydration

**Good**: Chakra UI, MUI
- Require provider plugins
- Client Components needed

**Avoid**: Ant Design v4 (use v5 for better SSR)

### Remix

**Best**: All modern libraries work well
- Mantine has official support
- MUI works with minor config
- Headless/Radix work out-of-box

### Vite

**Best**: All libraries (Vite's tree-shaking is excellent)
- shadcn/ui (designed for Vite)
- Mantine (official Vite support)
- Headless UI (minimal config)

## TypeScript-First Projects

**All libraries** have excellent TypeScript support in 2025.

**Special mentions:**
- **Mantine**: Best generic component types (Table, Select, etc.)
- **MUI**: Best polymorphic component typing
- **Chakra**: Best style prop type inference
- **Radix**: Best primitive type exports for wrapping

## Accessibility-Critical Applications

**Tier 1**: Radix UI, Headless UI, shadcn/ui
- Accessibility-first design
- 100% WAI-ARIA compliant
- Built by a11y experts

**Tier 2**: Chakra UI, Mantine
- Strong accessibility
- Minor gaps in edge cases
- 95%+ compliant

**Tier 3**: MUI, Ant Design
- Good for common patterns
- Enterprise accessibility decent
- Some complex widgets have gaps
- 80-85% compliant

## Final Recommendations by Use Case

### New Project, Modern Stack

**Default**: shadcn/ui (if using Tailwind) or Mantine (if not)

**Why**: Best DX, modern architecture, zero technical debt

### Enterprise Dashboard

**Default**: Ant Design (data-heavy) or MUI (Material Design)

**Why**: Best data tables, proven at scale, commercial support

### Custom Design System

**Default**: Radix UI

**Why**: Accessibility-first primitives, full styling control, wrap like shadcn/ui

### Tailwind Project

**Default**: shadcn/ui

**Why**: Purpose-built for Tailwind, code ownership, excellent integration

### Vue Project

**Only option**: Headless UI

**Why**: Only modern headless library with Vue support

### Maximum Performance

**Default**: Headless UI or Radix UI

**Why**: Smallest bundles, zero runtime overhead, static CSS

### Rapid Prototyping

**Default**: Chakra UI or Mantine

**Why**: Intuitive APIs, comprehensive features, fast setup

## Anti-Recommendations

### When NOT to Choose Each Library

**❌ shadcn/ui**: Not using Tailwind, need automatic updates, team unfamiliar with Radix patterns

**❌ MUI**: Custom design system required (not Material), bundle size critical (<50 KB)

**❌ Ant Design**: Consumer-facing app (enterprise aesthetic), bundle size critical

**❌ Chakra UI**: Need zero runtime cost, using Tailwind (different paradigm), need advanced data components

**❌ Mantine**: Using Tailwind (incompatible), need paid support, need advanced data grid

**❌ Radix UI**: Need pre-styled components (use shadcn/ui instead), rapid prototyping, team new to React

**❌ Headless UI**: Need comprehensive component set (14 components not enough), not using Tailwind (suboptimal DX)

## The 2025 Meta

**Trends:**
1. **Headless libraries rising**: Radix/Headless UI gaining market share
2. **CSS-in-JS declining**: Mantine v7 migration signals shift
3. **Tailwind dominance**: shadcn/ui proves copy-paste model works
4. **Accessibility standard**: All modern libraries must be WAI-ARIA compliant

**Prediction**: By 2026, most new projects will use either:
- shadcn/ui (Tailwind users)
- Mantine (non-Tailwind users)
- Enterprise libraries (MUI/Ant for data apps)

**The "safe bet" for 2025**: Mantine (comprehensive, modern, free, CSS Modules)
