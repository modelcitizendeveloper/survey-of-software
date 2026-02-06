# Radix UI

> "Low-level UI component library with a focus on accessibility, customization and developer experience."

## Quick Facts

| Metric | Value |
|--------|-------|
| GitHub Stars | ~17,000 |
| npm Weekly Downloads | ~226,000 |
| Bundle Size | Small (per-component imports) |
| License | MIT |
| Maintainer | WorkOS |
| Framework | React only |

## What Radix UI Is

Radix UI is a collection of **unstyled, accessible UI primitives**. It provides the behavior and accessibility of complex components (dialogs, dropdowns, tabs) without any visual styling.

Think of it as the "engine" of UI components - you add the "body" (styles).

## Why Radix Matters

Radix powers many popular libraries:
- **shadcn/ui** - Built entirely on Radix primitives
- Many design systems use Radix as foundation

Building accessible UI components is hard:
- ARIA attributes
- Keyboard navigation
- Focus management
- Screen reader support

Radix handles all of this, letting you focus on styling.

## How It Works

```tsx
import * as Dialog from '@radix-ui/react-dialog'

// Completely unstyled - you add all CSS
function MyDialog() {
  return (
    <Dialog.Root>
      <Dialog.Trigger>Open</Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/50" />
        <Dialog.Content className="fixed top-1/2 left-1/2 ...">
          <Dialog.Title>Edit Profile</Dialog.Title>
          <Dialog.Description>Make changes here.</Dialog.Description>
          <Dialog.Close>Close</Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  )
}
```

## Key Features

### Accessibility Built-in
- WAI-ARIA compliant
- Keyboard navigation (Arrow keys, Escape, Tab)
- Focus trapping in modals
- Screen reader announcements
- Correct ARIA roles and attributes

### Composable Architecture
Each component exposes multiple parts you can style independently:

```tsx
// Full control over each part
<Accordion.Root>
  <Accordion.Item>
    <Accordion.Header>
      <Accordion.Trigger />
    </Accordion.Header>
    <Accordion.Content />
  </Accordion.Item>
</Accordion.Root>
```

### Controlled & Uncontrolled
```tsx
// Uncontrolled (internal state)
<Dialog.Root>...</Dialog.Root>

// Controlled (you manage state)
<Dialog.Root open={isOpen} onOpenChange={setIsOpen}>
  ...
</Dialog.Root>
```

### Tree-shakeable
Import only what you need:
```tsx
import * as Dialog from '@radix-ui/react-dialog'
import * as Tabs from '@radix-ui/react-tabs'
// Only these components in your bundle
```

## Available Primitives

**Overlay**: Dialog, Alert Dialog, Popover, Tooltip, Hover Card, Context Menu, Dropdown Menu
**Form**: Checkbox, Radio Group, Select, Slider, Switch, Toggle, Toggle Group
**Navigation**: Navigation Menu, Tabs, Menubar
**Layout**: Accordion, Collapsible, Scroll Area, Separator
**Utility**: Avatar, Aspect Ratio, Progress, Label, Visually Hidden

## When to Choose Radix

**Choose Radix when:**
- Building a custom design system
- Need full styling control
- Want accessible primitives without opinions
- Using with Tailwind or any CSS solution
- Building component library for your org

**Consider alternatives when:**
- Want pre-styled components → shadcn/ui (uses Radix!)
- Need Vue support → Headless UI
- Want everything out of box → MUI, Mantine

## Radix vs Others

| Aspect | Radix UI | Headless UI | shadcn/ui |
|--------|----------|-------------|-----------|
| Styling | None | None | Tailwind |
| Components | 25+ | 10 | 40+ |
| Maintainer | WorkOS | Tailwind Labs | Community |
| Framework | React | React, Vue | React |

## Resources

- [Official Docs](https://www.radix-ui.com/primitives)
- [GitHub](https://github.com/radix-ui/primitives)
- [Accessibility Guide](https://www.radix-ui.com/primitives/docs/overview/accessibility)
