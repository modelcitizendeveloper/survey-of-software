# Chakra UI

> "Create accessible React apps with speed."

## Quick Facts

| Metric | Value |
|--------|-------|
| GitHub Stars | ~38,800 |
| npm Weekly Downloads | ~587,000 |
| Bundle Size | Medium |
| License | MIT |
| Styling | Prop-based (Style Props) |
| Focus | DX + Accessibility |

## What Makes Chakra Different

Chakra UI's key innovation is **prop-based styling**:

```tsx
// Traditional (CSS/className)
<button className="bg-blue-500 px-4 py-2 rounded">Click</button>

// Chakra (Style Props)
<Button bg="blue.500" px={4} py={2} borderRadius="md">Click</Button>
```

This eliminates the need to:
- Write CSS files
- Create CSS classes
- Switch between files

## Key Features

### Style Props
Every CSS property is available as a prop:

```tsx
<Box
  mt={4}                    // margin-top
  p={[2, 4, 6]}            // responsive padding
  bg="gray.100"            // background
  _hover={{ bg: 'gray.200' }} // pseudo-selectors
  display={{ base: 'block', md: 'flex' }} // responsive
>
  Content
</Box>
```

### Responsive by Default
```tsx
// Mobile: 100%, Tablet: 50%, Desktop: 25%
<Box width={{ base: '100%', md: '50%', lg: '25%' }}>
  Responsive without media queries
</Box>
```

### Excellent Accessibility
- All components are WAI-ARIA compliant
- Focus management built-in
- Keyboard navigation
- Screen reader support

### Easy Theming
```tsx
import { extendTheme } from '@chakra-ui/react'

const theme = extendTheme({
  colors: {
    brand: {
      50: '#f5fee5',
      500: '#38A169',
      900: '#1a202c',
    },
  },
  fonts: {
    heading: 'Inter, sans-serif',
    body: 'Inter, sans-serif',
  },
})
```

## Component Library

50+ components:

**Layout**: Box, Center, Container, Flex, Grid, Stack, Wrap
**Forms**: Button, Checkbox, Input, Radio, Select, Slider, Switch, Textarea
**Data Display**: Avatar, Badge, Card, List, Table, Tag
**Feedback**: Alert, Progress, Skeleton, Spinner, Toast
**Overlay**: Drawer, Menu, Modal, Popover, Tooltip
**Typography**: Heading, Text, Highlight

## When to Choose Chakra UI

**Choose Chakra when:**
- Want fast development with excellent DX
- Building custom-branded applications
- Need high customization without fighting framework
- Want accessible components by default
- Prefer props over CSS

**Consider alternatives when:**
- Using Tailwind → shadcn/ui
- Need enterprise data table → Ant Design, MUI
- Want Material Design → MUI
- Need more components → Mantine

## Drawbacks

1. **Fewer components** than MUI/Ant Design
2. **Style props can get verbose** for complex styling
3. **Runtime CSS-in-JS** (performance in some cases)
4. **No data table** (use third-party like TanStack Table)

## Chakra vs Alternatives

| Aspect | Chakra UI | MUI | shadcn/ui |
|--------|-----------|-----|-----------|
| Styling | Props | CSS-in-JS | Tailwind |
| Customization | Excellent | Moderate | Full |
| Bundle | Medium | Large | Zero |
| Components | 50+ | 50+ | 40+ |
| Learning | Easy | Medium | Low |

## Resources

- [Official Docs](https://chakra-ui.com/)
- [GitHub](https://github.com/chakra-ui/chakra-ui)
- [Component Docs](https://chakra-ui.com/docs/components)
- [Chakra Templates](https://chakra-templates.dev/)
