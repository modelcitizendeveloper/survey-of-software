# shadcn/ui

> "Beautifully designed components that you can copy and paste into your apps."

## Quick Facts

| Metric | Value |
|--------|-------|
| GitHub Stars | 85,500 |
| npm Downloads | N/A (copy-paste model) |
| Bundle Impact | Zero (code lives in your project) |
| License | MIT |
| Foundation | Radix UI + Tailwind CSS |
| Creator | shadcn (Shadid Haque) |

## Why shadcn/ui Dominates 2025

shadcn/ui exploded in popularity because it solves the fundamental tension in component libraries: **you get pre-built components but own the code**.

Traditional libraries:
- Install npm package → locked into their API
- Updates can break your app
- Customization requires overrides

shadcn/ui:
- Copy components into your project
- Full source code ownership
- Customize anything directly
- No version lock-in

## How It Works

```bash
# Initialize in your project
npx shadcn@latest init

# Add components as needed
npx shadcn@latest add button
npx shadcn@latest add dialog
npx shadcn@latest add form
```

Components are copied to `components/ui/` in your project:

```
src/
└── components/
    └── ui/
        ├── button.tsx      # You own this
        ├── dialog.tsx      # Modify freely
        └── form.tsx        # Full control
```

## Key Features

### Built on Radix UI
All complex components (Dialog, Dropdown, Tabs) use Radix primitives underneath:
- WAI-ARIA compliant
- Keyboard navigation
- Focus management
- Screen reader support

### Styled with Tailwind CSS
```tsx
// Example button variants
const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground",
        outline: "border border-input bg-background hover:bg-accent",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
      },
    },
  }
)
```

### CSS Variables for Theming
```css
/* globals.css */
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --primary: 222.2 47.4% 11.2%;
  --primary-foreground: 210 40% 98%;
}

.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
}
```

## Component Library

40+ components available:

**Layout**: Accordion, Card, Collapsible, Separator, Tabs
**Forms**: Button, Checkbox, Input, Radio, Select, Slider, Switch, Textarea
**Feedback**: Alert, Badge, Progress, Skeleton, Toast
**Overlay**: Dialog, Drawer, Popover, Sheet, Tooltip
**Data**: Calendar, Data Table, Command (cmdk)
**Navigation**: Breadcrumb, Dropdown Menu, Menubar, Navigation Menu

## When to Choose shadcn/ui

**Choose shadcn/ui when:**
- Using Tailwind CSS
- Want full code ownership
- Building custom-branded apps
- Need to modify component internals
- Using Next.js, Remix, or Vite

**Consider alternatives when:**
- Not using Tailwind → MUI, Chakra, Mantine
- Need Vue support → Headless UI
- Want zero setup → Chakra UI
- Need more components out of box → Mantine

## Comparison with Similar

| Aspect | shadcn/ui | Radix UI | Headless UI |
|--------|-----------|----------|-------------|
| Styling | Pre-styled (Tailwind) | Unstyled | Unstyled |
| Ownership | Full (copied code) | npm package | npm package |
| Framework | React | React | React, Vue |
| Customization | Modify source | Style yourself | Style yourself |

## Resources

- [Official Docs](https://ui.shadcn.com/)
- [GitHub](https://github.com/shadcn-ui/ui)
- [Component Examples](https://ui.shadcn.com/examples)
- [Themes](https://ui.shadcn.com/themes)
