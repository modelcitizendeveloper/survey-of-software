# S3 Persona-Based Recommendations

## Quick Reference Matrix

| Persona | Best Choice | Alternative | Avoid |
|---------|-------------|-------------|-------|
| **Startup MVP** | shadcn/ui | Mantine | Radix UI, Ant Design |
| **Enterprise Dashboard** | Ant Design | MUI X | shadcn/ui, Chakra UI |
| **Design System** | Radix UI | Headless UI | MUI, Ant Design |
| **Freelance Developer** | shadcn/ui | Mantine | Ant Design, Radix UI |
| **Open-Source Tool** | Headless UI | Radix UI | MUI, Ant Design |

## Decision Tree by Context

### By Team Size

**Solo / 1-3 people**:
- Default: shadcn/ui (Tailwind) or Mantine (others)
- Why: Fast setup, comprehensive, minimal decisions

**Small team / 5-15 people**:
- Default: Chakra UI or Mantine
- Why: Easy to learn, consistent DX

**Enterprise team / 20+ people**:
- Default: Ant Design (data-heavy) or MUI (Material Design)
- Why: Proven at scale, vendor stability

**Design systems team**:
- Default: Radix UI
- Why: Building foundation, need full control

### By Project Type

**Consumer SaaS / Web App**:
- shadcn/ui (modern aesthetic)
- Chakra UI (easy customization)
- Mantine (comprehensive features)

**Enterprise / B2B Dashboard**:
- Ant Design (best data table)
- MUI X (if budget for Premium)
- Mantine (free alternative)

**Marketing Site / Portfolio**:
- shadcn/ui (beautiful defaults)
- Headless UI + custom (if unique design)

**CLI Tool / Electron App**:
- Headless UI (smallest bundle)
- Radix UI (modular, small)

**Internal Design System**:
- Radix UI (accessibility primitives)
- Headless UI (simpler, Tailwind-friendly)

### By Timeline

**< 2 weeks** (prototype):
- shadcn/ui or Mantine (fastest)
- Chakra UI (if team knows it)

**1-3 months** (MVP):
- shadcn/ui, Mantine, or Chakra
- Ant Design (if enterprise features needed)

**6+ months** (design system):
- Radix UI (build proper foundation)
- Headless UI (if Tailwind + simpler needs)

### By Budget

**$0 budget**:
- ✅ shadcn/ui, Mantine, Chakra UI, Radix UI, Headless UI
- ❌ MUI X Premium ($1660/dev)

**< $1000 budget**:
- MUI X Pro ($495/dev) viable
- Otherwise use free options

**Enterprise budget**:
- MUI X Premium ($1660/dev) for best data grid
- Ant Design Pro Components (varies)
- Commercial support contracts available

### By Technical Constraints

**Bundle size < 50 KB**:
- Headless UI (~12 KB)
- Radix UI (~15-25 KB)
- shadcn/ui (~20-30 KB)

**Bundle size < 100 KB**:
- Mantine (~40-60 KB)
- Chakra UI (~45 KB)

**No bundle constraint**:
- MUI (~70-150 KB)
- Ant Design (~100-200 KB)

**Styling approach**:
- **Tailwind**: shadcn/ui or Headless UI
- **CSS Modules**: Mantine
- **CSS-in-JS**: Chakra UI or MUI
- **Custom CSS**: Radix UI or Headless UI

## Persona Deep-Dives

### Startup Founder (Sarah)

**Primary need**: Ship investor-ready MVP in 6 weeks

**Recommendation: shadcn/ui**

**Why**:
- Beautiful defaults (investor-ready without design work)
- Fast setup (productive day 1)
- Owns code (easy to pivot/customize)
- Modern aesthetic (2025 standards)

**Timeline value**:
- Week 1: Core UI built
- Week 3: Product features working
- Week 6: Launched

**Alternative: Mantine** (if not using Tailwind)

**Objection handling**:
- "Too opinionated?" → You'll pivot post-PMF anyway
- "Bundle size?" → 20 KB acceptable for MVP
- "Manual updates?" → Startups customize anyway

### Enterprise Engineer (Michael)

**Primary need**: Robust data tables, complex forms

**Recommendation: Ant Design**

**Why**:
- Best-in-class Table component
- Powerful form system (rc-field-form)
- Alibaba-backed stability
- 60+ enterprise components

**ROI calculation**:
- Building custom table: 3-6 months
- Ant Design: 2-3 weeks
- Savings: $200K-$400K in eng time

**Alternative: MUI X** (if budget for Premium)

**Objection handling**:
- "Bundle size?" → Enterprise WiFi fast enough
- "Aesthetic?" → Enterprise customers don't care
- "Customization?" → Token system allows theming

### Design System Engineer (Jessica)

**Primary need**: Build internal component library

**Recommendation: Radix UI**

**Why**:
- Full styling control (match Figma pixel-perfect)
- Best accessibility (WAI-ARIA experts)
- Compound components (fine-grained control)
- WorkOS-backed stability

**Pattern**:
1. Wrap Radix primitives
2. Add company styling
3. Publish to internal npm
4. Teams consume via npm install

**Alternative: Headless UI** (if using Tailwind, fewer components needed)

**Objection handling**:
- "Too much work?" → 6 months for 5-year system (worth it)
- "Why not theme MUI?" → Want design system, not "MUI with our colors"
- "Maintenance burden?" → Radix handles hard parts (a11y, behavior)

### Freelance Developer (David)

**Primary need**: Ship client projects fast, maximize profit

**Recommendation: shadcn/ui**

**Why**:
- Professional appearance (portfolio-worthy)
- Fast customization (client branding in 10 min)
- Reusable across projects
- Code ownership (tweak anything)

**Business value**:
- Time saved: 1-2 weeks per project
- Money saved: $2K-$4K per project
- Quality: More professional than custom
- Clients: Happier (modern UI)

**Alternative: Mantine** (if not using Tailwind)

**Objection handling**:
- "All projects look same?" → Change colors/fonts/spacing
- "Client wants custom?" → You own code, edit freely
- "Licensing?" → MIT (free for commercial)

### Open-Source Maintainer (Alex)

**Primary need**: Small bundle, excellent accessibility

**Recommendation: Headless UI**

**Why**:
- Smallest bundle (~12 KB)
- Excellent accessibility (Tailwind Labs quality)
- Free (MIT)
- Contributors know it (lower barrier)

**Success metrics**:
- Bundle: < 20 KB (Lighthouse 95+)
- Accessibility: Zero GitHub issues
- Contributors: Familiar patterns

**Alternative: Radix UI** (if need more components)

**Objection handling**:
- "Dependencies risky?" → Tailwind Labs-backed
- "Only 14 components?" → Usually enough for dev tools
- "Contributors complain?" → Devs respect Headless UI

## Common Scenarios

### "I'm using Tailwind CSS"

**→ shadcn/ui** (first choice)
- Purpose-built for Tailwind
- Beautiful defaults
- Code ownership

**→ Headless UI** (minimal approach)
- Smaller bundle
- Vue support (if needed)
- Simpler API

### "I need advanced data tables"

**→ Ant Design** (best free option)
- Industry-leading Table component
- Virtual scrolling, filtering, sorting, grouping
- Free

**→ MUI X Data Grid Premium** (if budget)
- $1660/dev but excellent
- Commercial support

**→ Mantine + TanStack Table** (build it)
- Free but requires integration
- More control

### "I'm building a design system"

**→ Radix UI** (for React)
- Most comprehensive primitives (25+)
- Best accessibility
- Battle-tested

**→ Headless UI** (for Vue or simpler needs)
- Vue support (unique)
- Simpler API
- 14 components

### "I need to ship tomorrow"

**→ shadcn/ui or Mantine**
- Fastest setup
- Copy-paste examples
- Beautiful defaults

**→ Chakra UI** (if team knows it)
- Prop-based styling (fast)

### "Bundle size is critical"

**→ Headless UI** (~12 KB)
**→ Radix UI** (~5-7 KB per primitive)
**→ shadcn/ui** (~20 KB)

Avoid: MUI (70+ KB), Ant Design (100+ KB)

### "I have zero budget"

All libraries are free except:
- ❌ MUI X Premium ($1660/dev)
- ❌ Ant Design Pro (varies, enterprise)

Use:
- ✅ Mantine (most comprehensive free)
- ✅ Chakra UI
- ✅ shadcn/ui
- ✅ Radix UI
- ✅ Headless UI

## Anti-Patterns

### Don't Choose Libraries By:

**❌ GitHub stars alone**
- MUI has most stars but not best for all use cases
- Match library to your context

**❌ "Everyone uses X"**
- shadcn/ui popular NOW but Radix better for design systems
- Ant Design popular in China, MUI in West (both good)

**❌ Avoiding dependencies**
- "Not invented here" syndrome
- Building custom components = weeks of work

**❌ Bundle size obsession (when not critical)**
- Startups: 50 KB library OK if ships 2 weeks faster
- Enterprise: 200 KB OK on fast WiFi

### Do Choose Libraries By:

**✅ Project context** (MVP vs enterprise vs design system)
**✅ Team skills** (Tailwind? CSS-in-JS?)
**✅ Actual requirements** (data tables? forms?)
**✅ Timeline** (weeks vs months)
**✅ Budget** (free vs can pay)

## Decision Flowchart

```
What are you building?
│
├─ MVP / Startup
│  ├─ Using Tailwind? → shadcn/ui
│  └─ Not using Tailwind? → Mantine
│
├─ Enterprise Dashboard
│  ├─ Data-heavy? → Ant Design
│  ├─ Material Design? → MUI
│  └─ Modern DX? → Mantine
│
├─ Design System
│  ├─ React-only? → Radix UI
│  └─ Need Vue? → Headless UI
│
├─ Client Projects (Freelance)
│  ├─ Using Tailwind? → shadcn/ui
│  └─ Not using Tailwind? → Mantine
│
└─ Open Source Tool
   ├─ Bundle critical? → Headless UI
   └─ More components? → Radix UI
```

## The 2025 Safe Defaults

**If unsure**, these are safe bets:

**Consumer apps**: shadcn/ui or Mantine
**Enterprise apps**: Ant Design or MUI
**Design systems**: Radix UI
**Everything else**: shadcn/ui (Tailwind) or Mantine (others)

**Rationale**: Most common needs covered, proven at scale, active maintenance.
