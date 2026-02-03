# Use Case: Building Company Design System

## Who Needs This

**Persona**: Jessica, Design Systems Engineer at Growing Tech Company

**Context**:
- Company has 20-50 engineers across 3-5 product teams
- Multiple products need consistent UI (web app, admin, marketing site)
- Design team created brand guidelines and design system in Figma
- Need to implement design system as React component library
- 6-12 month timeline to build + adopt across teams

**Technical background**:
- Strong React and CSS expertise
- Team comfortable with advanced patterns
- Accessibility is priority (WCAG AA minimum)
- Will maintain design system long-term (2-5+ years)

## Why They Need UI Component Libraries

### Pain Points

**1. Design-to-Code Gap**
- Designers create beautiful Figma components
- Engineers re-implement in React (inconsistently)
- Each product team builds own version
- "Same button" looks different across products

**2. Consistency at Scale**
- 5 products × 10 engineers = 50 different interpretations
- No single source of truth
- Brand guidelines PDF ignored
- QA finds inconsistencies too late

**3. Accessibility Complexity**
- Modal focus trapping is hard
- Keyboard navigation requires expertise
- ARIA attributes easy to get wrong
- Screen reader testing time-consuming

**4. Maintenance Burden**
- Each team maintains own components
- Bug fixes don't propagate
- Security issues duplicated
- Refactors require coordinating across teams

### Goals

**Primary**: Create internal component library that all teams use

**Secondary**:
- Match design system from Figma pixel-perfect
- Ensure accessibility compliance
- Enable teams to ship faster
- Reduce design-to-code inconsistencies

### Requirements

**Must-haves**:
- Full control over styling (match brand exactly)
- Accessible by default (WAI-ARIA compliant)
- Customizable (designers will iterate)
- Maintainable (5+ year lifecycle)
- Documentation for engineers

**Nice-to-haves**:
- Storybook integration
- Design tokens
- Dark mode support
- Animation/transitions

**Don't need**:
- Pre-built visual designs (have Figma)
- Specific design language (not Material/Enterprise)
- Rapid prototyping (building for years)

## Decision Criteria

### 1. Styling Control
**Critical**: Must match brand pixel-perfect

**What this means**:
- ✅ 100% control over CSS
- ✅ Can implement custom design tokens
- ✅ No library opinions on visual design
- ❌ Pre-styled libraries lock into aesthetics

### 2. Accessibility Foundation
**Critical**: Don't want to build from scratch

**What this means**:
- ✅ WAI-ARIA compliant primitives
- ✅ Keyboard navigation built-in
- ✅ Focus management automatic
- ❌ Can't afford to mess up accessibility

### 3. Composability
**Important**: Need to build custom patterns

**What this means**:
- ✅ Compound components (fine-grained control)
- ✅ Headless/unstyled (add own styles)
- ✅ Extensible APIs
- ❌ Black-box components won't work

### 4. Long-Term Stability
**Important**: 5+ year maintenance

**What this means**:
- ✅ Stable API (minimal breaking changes)
- ✅ Company or strong community backing
- ✅ Security updates
- ❌ Hobby projects risky

### 5. Developer Experience
**Moderate**: Internal teams will use this

**What this means**:
- ✅ Good TypeScript support
- ✅ Clear documentation
- ✅ Familiar patterns
- ⚠️ Learning curve acceptable (one-time cost)

## Why Existing Solutions Fall Short

**Pre-styled libraries (MUI, Ant Design)**:
- ❌ Material/Enterprise aesthetic baked in
- ❌ Hard to override completely
- ❌ Teams recognize "this is MUI"
- ❌ Not a unique design system

**shadcn/ui (copy-paste)**:
- ⚠️ Good for small teams
- ❌ Doesn't scale to 50 engineers (no npm updates)
- ❌ Each team copies different versions
- ❌ Bug fixes don't propagate

**Building 100% from scratch**:
- ❌ 12-18 months engineering time
- ❌ Accessibility bugs will happen
- ❌ Reinventing solved problems (focus traps, etc.)
- ❌ ROI negative vs using primitives

## Success Metrics

**Month 3**: First component library version (alpha)
**Month 6**: All teams migrated to design system
**Month 12**: Zero design inconsistencies found in QA
**Year 2+**: System evolves without breaking teams

**Longer term**:
- Design-to-code gap eliminated
- Teams ship 30% faster (no reimplementing)
- Accessibility audits pass
- Single update fixes bugs across all products

## Library Recommendations for This Persona

### Best Fit: Radix UI

**Why it works**:
- ✅ **Headless primitives** = full styling control
- ✅ **Best accessibility** (built by a11y experts)
- ✅ **25+ components** (covers common needs)
- ✅ **Compound patterns** (fine-grained control)
- ✅ **Stable API** (WorkOS-backed)
- ✅ **Battle-tested** (powers shadcn/ui, thousands of companies)

**How to use**:
1. Install Radix primitives (@radix-ui/react-*)
2. Wrap with custom styling matching Figma
3. Publish as internal npm package
4. Teams import from company design system

**Example**:
```tsx
// @company/design-system/Button.tsx
import * as RadixButton from '@radix-ui/react-button'
import { cva } from 'class-variance-authority'

const buttonStyles = cva('...company-specific-styles...', {
  variants: { ... }
})

export const Button = ({ children, ...props }) => (
  <RadixButton.Root className={buttonStyles(props)}>
    {children}
  </RadixButton.Root>
)
```

**Why it might not**:
- ⚠️ Requires CSS expertise (but you have designers)
- ⚠️ More setup time (6 months acceptable for multi-year use)

### Alternative: Headless UI

**Why it works**:
- ✅ Minimal, headless components
- ✅ Excellent accessibility
- ✅ Tailwind Labs-backed (stable)
- ✅ Simpler API than Radix

**Why it might not**:
- ❌ Only 14 components (vs Radix 25+)
- ❌ Less comprehensive (no tooltips, sliders, etc.)
- ❌ Smaller ecosystem

**Best for**: Teams using Tailwind, need fewer components

### Consider: Building on shadcn/ui Pattern

**Why**:
- ✅ Use Radix + Tailwind foundation
- ✅ Customize to match brand
- ✅ Publish as internal package

**Approach**:
1. Fork shadcn/ui components
2. Customize with company design tokens
3. Publish to internal npm registry
4. Teams install via npm (not copy-paste)

### Avoid: MUI, Ant Design, Chakra

**Why**:
- ❌ Pre-styled = not a custom design system
- ❌ Teams will say "this looks like MUI"
- ❌ Deep customization fights library opinions
- ❌ Not building design system, just theming one

## Real-World Example

**Scenario**: Building "Acme Design System" for company products

**What Jessica needs**:
- Custom button (brand colors, fonts, hover states)
- Modal (brand animations, layout)
- Dropdown (custom arrow, transitions)
- Form inputs (brand focus states)
- Navigation (unique design)

**With Radix UI** (6 months):
- Month 1: Setup Radix, design token system
- Month 2-3: Wrap 15-20 core components
- Month 4: Documentation, Storybook
- Month 5-6: Team adoption, feedback, iteration
- **Result**: Custom design system matching Figma

**With MUI customization** (6 months):
- Month 1-2: Deep theme customization
- Month 3: Fighting MUI defaults
- Month 4: Realizing some things can't be changed
- Month 5: Designers unhappy with compromises
- Month 6: Considering rebuild
- **Result**: Looks like "customized MUI", not unique system

**With 100% scratch** (12-18 months):
- Month 1-3: Build button, input, modal
- Month 4-6: Add accessibility
- Month 7-9: Debug focus traps, keyboard nav
- Month 10-12: Add advanced components
- Month 13-18: Fix bugs, edge cases
- **Result**: Working but lots of maintenance debt

**Radix wins**: Custom look, accessibility built-in, maintainable

## Persona Objections & Responses

**"Why not just use shadcn/ui?"**
- shadcn/ui is copy-paste (teams get different versions)
- You need npm package for consistency
- Solution: Build internal package using Radix (like shadcn does)

**"Can't we just theme MUI deeply?"**
- Possible but fights library at every step
- Still looks like "Material Design derivative"
- Design system should feel unique, not themed

**"Isn't building on primitives too much work?"**
- Upfront: Yes (6 months vs 2 months for theming)
- Long-term: No (full control, no fighting library)
- ROI positive over 5 years

**"What about maintenance burden?"**
- Radix handles hard parts (accessibility, behavior)
- You maintain styling only (which you'd do anyway)
- Stable API means fewer breaking changes

## Bottom Line

**Design system teams should use headless primitives**:

**Best choice**: Radix UI (most comprehensive, best accessibility)
**Tailwind teams**: Headless UI or Radix + Tailwind
**Vue support needed**: Headless UI (only option)

**Pattern**:
1. Radix/Headless UI (behavior + a11y)
2. Custom styling (Tailwind, CSS Modules, CSS-in-JS)
3. Internal npm package
4. Storybook docs
5. Teams consume via npm

**Don't theme pre-styled libraries**: You want a design system, not "MUI with our colors".

**Don't build 100% from scratch**: Use primitives for accessibility/behavior, custom style everything else.
