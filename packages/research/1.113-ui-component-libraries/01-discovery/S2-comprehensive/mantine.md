# Mantine - Technical Analysis

## Architecture Overview

### Full-Featured Modern Library

Mantine is a **batteries-included** React component library:

```tsx
import { Button, TextInput, DatePicker } from '@mantine/core'
import { useForm } from '@mantine/form'
import { useDebouncedValue } from '@mantine/hooks'
import { RichTextEditor } from '@mantine/tiptap'
```

**Packages:**
- **@mantine/core**: 120+ components
- **@mantine/hooks**: 70+ utility hooks
- **@mantine/form**: Form management
- **@mantine/dates**: Date/time components
- **@mantine/notifications**: Toast notifications
- **@mantine/tiptap**: Rich text editor
- **@mantine/dropzone**: File upload
- **@mantine/spotlight**: Command palette

Most comprehensive ecosystem in a single library.

## Styling Architecture

### CSS Modules + CSS-in-JS Hybrid

Mantine v7 uses **CSS modules** by default:

```tsx
import classes from './MyComponent.module.css'

<Button className={classes.custom}>Click</Button>
```

**Previously (v6)**: Emotion CSS-in-JS

**Migration rationale**: Better performance, simpler builds

### Theme System

Powerful theming via `MantineProvider`:

```tsx
import { MantineProvider, createTheme } from '@mantine/core'

const theme = createTheme({
  primaryColor: 'blue',
  fontFamily: 'Inter, sans-serif',
  spacing: { xs: '0.5rem', sm: '0.75rem', md: '1rem' },
  radius: { xs: '0.125rem', sm: '0.25rem', md: '0.5rem' },
  breakpoints: {
    xs: '30em',
    sm: '48em',
    md: '64em',
    lg: '74em',
    xl: '90em',
  },
  colors: {
    brand: ['#e3f2fd', '#90caf9', '#2196f3', ...],
  },
  components: {
    Button: {
      defaultProps: { size: 'md' },
      styles: (theme) => ({
        root: { borderRadius: theme.radius.sm },
      }),
    },
  },
})

<MantineProvider theme={theme}>
  <App />
</MantineProvider>
```

### Styles API

Granular component customization:

```tsx
<Button
  styles={(theme) => ({
    root: { backgroundColor: theme.colors.blue[6] },
    label: { fontSize: theme.fontSizes.lg },
    leftIcon: { marginRight: theme.spacing.md },
  })}
>
  Custom Button
</Button>
```

**Every sub-element** is styleable.

### CSS Variables

Mantine generates CSS variables:

```css
:root {
  --mantine-color-blue-6: #228be6;
  --mantine-spacing-md: 1rem;
  --mantine-radius-md: 0.5rem;
}
```

Enables dynamic theming without runtime CSS generation.

## Performance Characteristics

### Bundle Size

**Mantine v7 (2025):**
```
@mantine/core:        ~150 KB (tree-shaken commonly used)
Button only:           ~8 KB
DatePicker:           ~35 KB (with dayjs)
Full package:         ~400 KB (if importing everything)
```

**v7 vs v6**: ~40% smaller due to CSS modules

### Tree-Shaking

Excellent tree-shaking:

```tsx
// ✅ Perfect tree-shaking
import { Button, TextInput } from '@mantine/core'

// ❌ Avoid
import * as Mantine from '@mantine/core'
```

**Package splitting**: Separate packages (@mantine/dates, @mantine/tiptap) reduce main bundle.

### Runtime Performance

**CSS Modules = zero runtime overhead**:
- No CSS-in-JS parsing
- Static classNames
- No theme context lookups (unless using styles API)

**Component performance**:
- Optimized re-renders
- Virtual lists for large datasets
- Memoization built-in

### SSR Support

Full server-side rendering:

```tsx
// Works with Next.js, Remix out-of-box
import { MantineProvider } from '@mantine/core'

export default function Layout({ children }) {
  return (
    <MantineProvider>
      {children}
    </MantineProvider>
  )
}
```

**No special SSR setup needed** (v7+).

## TypeScript Integration

### Type Safety

Written in TypeScript-first:

```tsx
interface ButtonProps {
  variant?: 'filled' | 'light' | 'outline' | 'subtle' | 'default'
  color?: MantineColor
  size?: MantineSize
  radius?: MantineRadius
  fullWidth?: boolean
  leftSection?: ReactNode
  rightSection?: ReactNode
}
```

**Generic components**:

```tsx
<Select<string>
  data={['React', 'Vue', 'Svelte']}
  onChange={(value) => {
    // value is typed as string | null
  }}
/>
```

### Theme Typing

Extend theme types:

```tsx
import type { MantineThemeOverride } from '@mantine/core'

declare module '@mantine/core' {
  export interface MantineThemeColorsOverride {
    colors: Record<'brand', [string, ...string[]]>
  }
}

// Now 'brand' autocompletes
<Button color="brand">Click</Button>
```

### Form Typing

Form values fully typed:

```tsx
interface FormValues {
  email: string
  age: number
}

const form = useForm<FormValues>({
  initialValues: { email: '', age: 0 },
  validate: {
    email: (value) => (/^\S+@\S+$/.test(value) ? null : 'Invalid email'),
    age: (value) => (value >= 18 ? null : 'Must be 18+'),
  },
})

// form.values is typed as FormValues
```

## Component Composition

### Compound Components

Used extensively:

```tsx
<Tabs defaultValue="gallery">
  <Tabs.List>
    <Tabs.Tab value="gallery">Gallery</Tabs.Tab>
    <Tabs.Tab value="messages">Messages</Tabs.Tab>
  </Tabs.List>

  <Tabs.Panel value="gallery">Gallery content</Tabs.Panel>
  <Tabs.Panel value="messages">Messages content</Tabs.Panel>
</Tabs>
```

### Layout Components

Comprehensive layout primitives:

```tsx
// Stack (vertical)
<Stack gap="md">
  <Box>Item 1</Box>
  <Box>Item 2</Box>
</Stack>

// Group (horizontal)
<Group justify="space-between" align="center">
  <Button>Left</Button>
  <Button>Right</Button>
</Group>

// Grid
<Grid>
  <Grid.Col span={4}>1/3 width</Grid.Col>
  <Grid.Col span={8}>2/3 width</Grid.Col>
</Grid>

// Flex
<Flex direction="row" wrap="wrap" gap="md">
  <Box>Item</Box>
</Flex>
```

### Polymorphic Components

Every component supports `component` prop:

```tsx
<Button component="a" href="/dashboard">
  Dashboard
</Button>

<Button component={Link} to="/dashboard">
  Dashboard
</Button>
```

## Hooks Library

### Comprehensive Hooks (70+)

**State Management:**
```tsx
useLocalStorage('theme', 'light')
useSessionStorage('user', null)
useToggle(['light', 'dark'])
useDisclosure(false) // open/close state
```

**DOM Utilities:**
```tsx
useClickOutside(() => setOpened(false))
useHover()
useIntersection(ref, { threshold: 0.5 })
useWindowScroll()
useMediaQuery('(min-width: 768px)')
```

**Form & Input:**
```tsx
useDebouncedValue(search, 500)
useDebouncedState(search, 500)
useInputState('initial')
```

**Misc:**
```tsx
useClipboard()
useIdle(5000) // Detect user inactivity
useFavicon('/icon.png')
useDocumentTitle('Page Title')
```

**No other library provides this many hooks.**

## Form Management

### @mantine/form

Powerful form solution:

```tsx
import { useForm } from '@mantine/form'

const form = useForm({
  initialValues: {
    email: '',
    password: '',
    termsOfService: false,
  },

  validate: {
    email: (value) => (/^\S+@\S+$/.test(value) ? null : 'Invalid email'),
    password: (value) => (
      value.length >= 6 ? null : 'Password must be 6+ characters'
    ),
  },
})

<form onSubmit={form.onSubmit((values) => console.log(values))}>
  <TextInput
    label="Email"
    {...form.getInputProps('email')}
  />
  <PasswordInput
    label="Password"
    {...form.getInputProps('password')}
  />
  <Button type="submit">Submit</Button>
</form>
```

**Features:**
- Field-level validation
- Async validation
- Nested objects/arrays
- Dynamic lists
- Transform values

**Performance**: Only changed fields re-render.

## Date Components

### @mantine/dates

Rich date/time components:

```tsx
import { DatePicker, DateRangePicker, TimeInput } from '@mantine/dates'

<DatePicker
  value={date}
  onChange={setDate}
  minDate={new Date()}
  maxDate={dayjs(new Date()).add(1, 'month').toDate()}
/>

<DateRangePicker
  type="range"
  value={[startDate, endDate]}
  onChange={setRange}
/>

<TimeInput value={time} onChange={setTime} />
```

**Uses dayjs** (lightweight date library).

## Accessibility Implementation

### Excellent Accessibility

Mantine emphasizes a11y:

```tsx
// Modal focus trapping, Escape closes
<Modal opened={opened} onClose={close}>
  <Modal.Header>Title</Modal.Header>
  <Modal.Body>Content</Modal.Body>
</Modal>

// Menu keyboard navigation
<Menu>
  <Menu.Target><Button>Actions</Button></Menu.Target>
  <Menu.Dropdown>
    <Menu.Item>Download</Menu.Item>
  </Menu.Dropdown>
</Menu>
```

**Features:**
- Full keyboard navigation
- Screen reader support
- ARIA attributes automatic
- Focus management
- Skip links

**Documentation** emphasizes accessibility patterns.

## Customization Mechanisms

### Global Styles Override

```tsx
<MantineProvider
  theme={{
    components: {
      Button: {
        defaultProps: {
          size: 'md',
          variant: 'filled',
        },
        styles: {
          root: { fontWeight: 600 },
          label: { textTransform: 'uppercase' },
        },
      },
    },
  }}
>
```

### CSS Variables

Override via CSS:

```css
:root {
  --mantine-primary-color-filled: #1c7ed6;
  --mantine-radius-default: 0.5rem;
}
```

### Variants

Create custom variants:

```tsx
<MantineProvider
  theme={{
    components: {
      Button: Button.extend({
        variants: {
          danger: (theme) => ({
            root: {
              backgroundColor: theme.colors.red[6],
              color: 'white',
            },
          }),
        },
      }),
    },
  }}
>

// Usage
<Button variant="danger">Delete</Button>
```

## Build System Integration

### Next.js

Official integration:

```bash
npm install @mantine/next
```

```tsx
// app/layout.tsx
import { MantineProvider } from '@mantine/core'
import { ColorSchemeScript } from '@mantine/core'

export default function RootLayout({ children }) {
  return (
    <html>
      <head>
        <ColorSchemeScript />
      </head>
      <body>
        <MantineProvider>{children}</MantineProvider>
      </body>
    </html>
  )
}
```

### Vite

Works out-of-box:

```tsx
import '@mantine/core/styles.css'
```

### Remix

Official support with hydration handling.

## Testing Considerations

### Testing Utilities

`@mantine/tests` package provides utilities:

```tsx
import { render, screen } from '@mantine/tests'

test('renders button', () => {
  render(<Button>Click me</Button>)
  expect(screen.getByRole('button')).toHaveTextContent('Click me')
})
```

Handles MantineProvider automatically.

### Snapshot Testing

**Stable** with CSS Modules:
- No generated classNames
- Deterministic output

## Upgrade Path

### v6 → v7 Migration

Major changes (2024):
- Emotion → CSS Modules
- Import styles: `import '@mantine/core/styles.css'`
- Some component API changes

**Codemod available**:
```bash
npx @mantine/codemod@latest v6-to-v7 src/
```

**Breaking changes documented** thoroughly.

## Ecosystem

### Official Packages (All Free)

- **@mantine/hooks**: 70+ hooks
- **@mantine/form**: Form management
- **@mantine/dates**: Date/time components
- **@mantine/notifications**: Toast system
- **@mantine/tiptap**: Rich text editor
- **@mantine/dropzone**: File upload
- **@mantine/spotlight**: Command palette
- **@mantine/carousel**: Image carousel
- **@mantine/nprogress**: Progress bar

**Everything is free** (no premium tier).

### Community

- Active Discord community
- Regular releases
- Responsive maintainers

## Limitations & Constraints

### No Premium/Advanced Components

- No data grid (like MUI X)
- No Gantt chart
- No org chart

**Mitigation**: Use third-party libraries (TanStack Table, etc.)

### CSS Modules Learning Curve

Teams used to CSS-in-JS may need adjustment (v7+).

### Not Opinionated

- No specific design language (unlike MUI = Material, Ant = Enterprise)
- More customization needed for cohesive look

## When to Choose Mantine (Technical POV)

### Ideal Technical Conditions

✅ **Use when:**
- Want comprehensive component + hooks library
- Need form handling built-in
- Date/time pickers required
- Don't need premium components (data grid)
- Want zero-runtime styling (v7+)
- Team values DX and completeness

❌ **Avoid when:**
- Need data grid/advanced enterprise components
- Using Tailwind (different paradigm)
- Want specific design language (Material, etc.)

## Technical Debt Considerations

### Low Long-Term Debt

- v6→v7 migration smooth with codemod
- No premium licenses to manage
- Active development

### Low Maintenance Burden

- Regular updates
- Good backward compatibility within versions
- Community support

## Conclusion

Mantine is the **most feature-complete** free React UI library:

**Strengths:**
- 120+ components + 70+ hooks (everything you need)
- Excellent TypeScript support
- Zero-runtime styling (v7+)
- Comprehensive ecosystem (forms, dates, notifications, etc.)
- All free (no paid tiers)
- Great documentation

**Trade-offs:**
- No advanced data components (grid, charts)
- Less opinionated (more setup for cohesive design)
- Smaller community than MUI/Ant
- Not compatible with Tailwind

**Best for**: Teams that want a batteries-included library with modern DX, don't need advanced enterprise components, and value completeness over specific design languages.
