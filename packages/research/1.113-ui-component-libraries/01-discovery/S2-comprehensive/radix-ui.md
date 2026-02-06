# Radix UI - Technical Analysis

## Architecture Overview

### Headless/Unstyled Primitives

Radix UI provides **behavior and accessibility without styling**:

```tsx
import * as Dialog from '@radix-ui/react-dialog'

<Dialog.Root>
  <Dialog.Trigger className="your-button-class">Open</Dialog.Trigger>
  <Dialog.Portal>
    <Dialog.Overlay className="your-overlay-class" />
    <Dialog.Content className="your-content-class">
      <Dialog.Title>Title</Dialog.Title>
      <Dialog.Description>Description</Dialog.Description>
      <Dialog.Close>Close</Dialog.Close>
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
```

**You provide**: All styling (CSS, Tailwind, CSS-in-JS, etc.)

**Radix provides**: Accessibility, keyboard navigation, focus management, state management

## Design Philosophy

### Primitives, Not Components

Radix components are **building blocks**:

- **Low-level**: Granular control over every element
- **Composable**: Combine primitives to create custom components
- **Unstyled**: No opinions on visual design
- **Accessible**: WAI-ARIA compliant by default

**Intended use**: Foundation for design systems, not direct consumption.

### Component Model: Compound Components

All Radix components use **compound component pattern**:

```tsx
// Root: Manages state
<Dialog.Root open={open} onOpenChange={setOpen}>

  // Trigger: Opens dialog
  <Dialog.Trigger asChild>
    <button>Open</button>
  </Dialog.Trigger>

  // Portal: Renders outside DOM hierarchy
  <Dialog.Portal>

    // Overlay: Background overlay
    <Dialog.Overlay />

    // Content: Main dialog content
    <Dialog.Content>
      <Dialog.Title>Title</Dialog.Title>
      <Dialog.Description>Accessible description</Dialog.Description>
      <Dialog.Close>Close</Dialog.Close>
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
```

**Benefits:**
- Full control over structure
- Easy to understand what each part does
- Can customize/omit parts as needed

**Trade-off**: More verbose than single-component APIs

## Performance Characteristics

### Bundle Size

**Radix primitives are tiny:**

```
@radix-ui/react-dialog:     ~7 KB (gzipped)
@radix-ui/react-dropdown:   ~9 KB (gzipped)
@radix-ui/react-popover:    ~5 KB (gzipped)
@radix-ui/react-select:    ~15 KB (gzipped)
@radix-ui/react-slider:     ~4 KB (gzipped)
```

**No styling engine** = minimal overhead.

### Tree-Shaking

Perfect tree-shaking:

```tsx
// ✅ Only Dialog bundled
import * as Dialog from '@radix-ui/react-dialog'

// Each primitive is a separate package
import * as DropdownMenu from '@radix-ui/react-dropdown-menu'
```

**Import only what you use.**

### Runtime Performance

**Zero styling overhead**:
- No CSS-in-JS runtime
- No theme provider (unless you add one)
- Minimal JavaScript

**React performance**:
- Optimized re-renders
- Controlled/uncontrolled patterns
- No unnecessary state updates

### SSR Support

Full server-side rendering:

```tsx
// Works with Next.js, Remix out-of-box
import * as Dialog from '@radix-ui/react-dialog'
```

**No hydration issues** when used correctly.

## TypeScript Integration

### Type Safety

Fully typed in TypeScript:

```tsx
import * as Dialog from '@radix-ui/react-dialog'

interface DialogContentProps extends React.ComponentPropsWithoutRef<
  typeof Dialog.Content
> {
  className?: string
}

const DialogContent = React.forwardRef<
  React.ElementRef<typeof Dialog.Content>,
  DialogContentProps
>(({ className, children, ...props }, ref) => (
  <Dialog.Portal>
    <Dialog.Overlay />
    <Dialog.Content ref={ref} className={className} {...props}>
      {children}
    </Dialog.Content>
  </Dialog.Portal>
))
```

**Component types** exported for extensions.

### Polymorphic Components (asChild)

`asChild` prop enables **slot pattern**:

```tsx
// Render Trigger as custom component
<Dialog.Trigger asChild>
  <Link to="/settings">Open Settings</Link>
</Dialog.Trigger>
```

**Implementation**: Radix Slot merges props and renders as child.

**Typed correctly**: TypeScript infers child component props.

## Accessibility Implementation

### WAI-ARIA Compliant

Radix is **accessibility-first**:

**Dialog example:**
```tsx
<Dialog.Root>
  {/* Automatically adds:
      - role="dialog"
      - aria-modal="true"
      - aria-labelledby (points to Title)
      - aria-describedby (points to Description)
      - Focus trap
      - Escape key closes
      - Click outside closes
  */}
  <Dialog.Content>
    <Dialog.Title>Edit Profile</Dialog.Title>
    <Dialog.Description>
      Make changes to your profile here.
    </Dialog.Description>
  </Dialog.Content>
</Dialog.Root>
```

**Menu example:**
```tsx
<DropdownMenu.Root>
  {/* Automatically adds:
      - role="menu"
      - aria-haspopup="true"
      - Arrow key navigation
      - Home/End navigation
      - Type-ahead selection
      - Escape closes
  */}
</DropdownMenu.Root>
```

### Focus Management

**Automatic focus handling:**
- Focus trap in dialogs
- Focus return on close
- First/last item focus with Tab
- Roving tabindex in menus

### Keyboard Navigation

**Full keyboard support:**
- Arrow keys (menus, sliders, tabs)
- Enter/Space (activation)
- Escape (close/cancel)
- Home/End (navigation)
- Tab (focus management)

## Component Architecture

### 25+ Primitives

**Overlays:**
- Dialog (modal)
- Popover
- Dropdown Menu
- Context Menu
- Hover Card
- Tooltip

**Navigation:**
- Accordion
- Tabs
- Navigation Menu

**Forms:**
- Checkbox
- Radio Group
- Select
- Slider
- Switch
- Toggle
- Toggle Group

**Data Display:**
- Avatar
- Progress
- Scroll Area

**Utilities:**
- Collapsible
- Separator
- Label
- Visually Hidden
- Portal
- Slot

### State Management

Components can be **controlled or uncontrolled**:

```tsx
// Uncontrolled (Radix manages state)
<Dialog.Root>
  <Dialog.Trigger>Open</Dialog.Trigger>
  <Dialog.Content>Content</Dialog.Content>
</Dialog.Root>

// Controlled (you manage state)
const [open, setOpen] = useState(false)
<Dialog.Root open={open} onOpenChange={setOpen}>
  <Dialog.Trigger>Open</Dialog.Trigger>
  <Dialog.Content>Content</Dialog.Content>
</Dialog.Root>
```

**Flexibility**: Use uncontrolled for simple cases, controlled when you need to sync state.

## Styling Integration

### Works with Any Styling Solution

**Tailwind CSS:**
```tsx
<Dialog.Content className="rounded-lg bg-white p-6 shadow-xl">
  <Dialog.Title className="text-lg font-semibold">
    Edit Profile
  </Dialog.Title>
</Dialog.Content>
```

**CSS Modules:**
```tsx
import styles from './Dialog.module.css'

<Dialog.Content className={styles.content}>
  <Dialog.Title className={styles.title}>Edit Profile</Dialog.Title>
</Dialog.Content>
```

**Emotion/Styled Components:**
```tsx
const StyledContent = styled(Dialog.Content)`
  background: white;
  border-radius: 8px;
  padding: 24px;
`
```

**Vanilla CSS:**
```css
.dialog-content {
  background: white;
  border-radius: 8px;
  padding: 24px;
}
```

### Data Attributes for State

Radix adds **data attributes** for styling states:

```tsx
<Dialog.Overlay data-state="open" />

// CSS
.dialog-overlay[data-state='open'] {
  animation: fadeIn 200ms;
}

.dialog-overlay[data-state='closed'] {
  animation: fadeOut 200ms;
}
```

**Available states**: `data-state`, `data-disabled`, `data-orientation`, etc.

## Customization & Extension

### Building on Radix

Radix is **designed to be wrapped**:

```tsx
// Create your own styled Dialog
export const Dialog = (props) => (
  <RadixDialog.Root {...props} />
)

export const DialogTrigger = ({ children, ...props }) => (
  <RadixDialog.Trigger asChild {...props}>
    {children}
  </RadixDialog.Trigger>
)

export const DialogContent = ({ children, ...props }) => (
  <RadixDialog.Portal>
    <RadixDialog.Overlay className="fixed inset-0 bg-black/50" />
    <RadixDialog.Content
      className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
      {...props}
    >
      {children}
    </RadixDialog.Content>
  </RadixDialog.Portal>
)
```

**This is how shadcn/ui works** - it wraps Radix with Tailwind styles.

## Build System Integration

### Framework Agnostic

Works with all React build tools:

- **Next.js**: No special config
- **Vite**: Works out-of-box
- **Create React App**: No issues
- **Remix**: Full support
- **Gatsby**: Compatible

### No Build Step Required

Radix primitives are **pre-built**:
- No CSS to process
- No compile step
- Import and use

## Testing Considerations

### Unit Testing

Test as regular React components:

```tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import * as Dialog from '@radix-ui/react-dialog'

test('opens and closes dialog', async () => {
  const user = userEvent.setup()

  render(
    <Dialog.Root>
      <Dialog.Trigger>Open</Dialog.Trigger>
      <Dialog.Content>
        <Dialog.Title>Title</Dialog.Title>
        <Dialog.Close>Close</Dialog.Close>
      </Dialog.Content>
    </Dialog.Root>
  )

  await user.click(screen.getByText('Open'))
  expect(screen.getByText('Title')).toBeInTheDocument()

  await user.click(screen.getByText('Close'))
  expect(screen.queryByText('Title')).not.toBeInTheDocument()
})
```

**No special setup needed.**

### Accessibility Testing

Use `jest-axe` or `@axe-core/react`:

```tsx
import { axe } from 'jest-axe'

test('dialog is accessible', async () => {
  const { container } = render(<Dialog />)
  const results = await axe(container)
  expect(results).toHaveNoViolations()
})
```

Radix components **pass accessibility audits** by default.

## Maintenance & Development

### Development Model

- **Open source**: MIT licensed
- **Maintainer**: WorkOS (company-backed)
- **Community**: Active development
- **Stability**: Mature, production-ready

### Versioning

Radix follows **semantic versioning**:
- Major versions: Breaking changes
- Minor versions: New features
- Patch versions: Bug fixes

**Stable API**: Breaking changes rare after 1.0.

## Limitations & Constraints

### Not Ready-to-Use

**You must:**
- Write all CSS/styling
- Decide on visual design
- Create your own variants
- Handle theming

**Time investment**: More setup than pre-styled libraries.

### No Pre-Built Components

**Missing:**
- Pre-styled buttons, inputs
- Layout components (Grid, Stack)
- Utility components (Card, Badge)

**Mitigation**: Build these yourself or use with shadcn/ui.

### Verbose API

Compound components = more code:

```tsx
// Radix (verbose)
<Dialog.Root>
  <Dialog.Trigger>Open</Dialog.Trigger>
  <Dialog.Portal>
    <Dialog.Overlay />
    <Dialog.Content>
      <Dialog.Title>Title</Dialog.Title>
      <Dialog.Description>Description</Dialog.Description>
      <form>
        {/* ... */}
      </form>
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>

// vs Single-component API (concise)
<Dialog
  trigger={<button>Open</button>}
  title="Title"
  description="Description"
>
  <form>{/* ... */}</form>
</Dialog>
```

**Trade-off**: Verbosity for flexibility.

## When to Choose Radix UI (Technical POV)

### Ideal Technical Conditions

✅ **Use when:**
- Building custom design system
- Need full control over styling
- Want minimal bundle size
- Accessibility is critical
- Using Tailwind or custom CSS
- Team comfortable with compound components

❌ **Avoid when:**
- Need pre-styled components (use shadcn/ui instead)
- Want quick prototyping (use MUI/Chakra)
- Team unfamiliar with headless libraries
- Don't want to write CSS

## Technical Debt Considerations

### Low Long-Term Debt

- Stable API
- Company-backed (WorkOS)
- No major breaking changes expected
- Can migrate away (no vendor lock-in)

### Medium Setup Burden

- Must build your own component layer
- Theming requires custom solution
- More code to maintain vs pre-styled

## Conclusion

Radix UI is **the foundation for custom design systems**:

**Strengths:**
- Excellent accessibility (best-in-class)
- Minimal bundle size
- Full styling control
- Stable, production-ready API
- Powers shadcn/ui (proven at scale)

**Trade-offs:**
- Requires custom styling layer
- More verbose API
- More setup time
- No pre-built variants

**Best for**: Teams building custom design systems who need accessible primitives and full styling control. Not for rapid prototyping or teams wanting pre-styled components (use shadcn/ui for that).
