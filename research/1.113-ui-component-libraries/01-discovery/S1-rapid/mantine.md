# Mantine

> "A fully featured React components library."

## Quick Facts

| Metric | Value |
|--------|-------|
| GitHub Stars | ~28,000 |
| npm Weekly Downloads | ~500,000 |
| Bundle Size | Medium |
| License | MIT |
| Components | 120+ |
| Hooks | 70+ |
| Current Version | 8.x (2025) |

## Why Mantine Stands Out

Mantine offers the **best balance of features, modern DX, and flexibility** in 2025. It's like MUI but with better developer experience and more hooks.

Key differentiators:
1. **120+ components** - More than Chakra
2. **70+ hooks** - More than any competitor
3. **Modular packages** - Install only what you need
4. **Modern defaults** - Dark mode, SSR, TypeScript

## Modular Architecture

Install only what you need:

```bash
npm install @mantine/core @mantine/hooks  # Core + hooks
npm install @mantine/form                  # Form management
npm install @mantine/dates                 # Date pickers
npm install @mantine/notifications         # Toast notifications
npm install @mantine/modals               # Modal manager
npm install @mantine/spotlight            # Command palette
npm install @mantine/carousel             # Carousel
npm install @mantine/dropzone             # File upload
npm install @mantine/tiptap               # Rich text editor
```

## Key Features

### Component Library (120+)
Everything you need:
- All standard components (buttons, inputs, etc.)
- Rich text editor (Tiptap integration)
- Date pickers
- File upload with dropzone
- Command palette (Spotlight)
- Charts and data visualization

### Hooks Library (70+)
```tsx
import {
  useDebouncedValue,
  useClickOutside,
  useMediaQuery,
  useLocalStorage,
  useHotkeys,
  useIdle,
  useNetwork,
  useClipboard
} from '@mantine/hooks'

// Works standalone - no Mantine UI required
const [value, setValue] = useState('')
const [debounced] = useDebouncedValue(value, 200)
```

### Form Management
```tsx
import { useForm } from '@mantine/form'

const form = useForm({
  initialValues: { email: '', password: '' },
  validate: {
    email: (value) => (/^\S+@\S+$/.test(value) ? null : 'Invalid email'),
    password: (value) => (value.length >= 6 ? null : 'Too short'),
  },
})

return (
  <form onSubmit={form.onSubmit(handleSubmit)}>
    <TextInput {...form.getInputProps('email')} />
    <PasswordInput {...form.getInputProps('password')} />
    <Button type="submit">Submit</Button>
  </form>
)
```

### Theming
```tsx
import { MantineProvider, createTheme } from '@mantine/core'

const theme = createTheme({
  primaryColor: 'violet',
  fontFamily: 'Inter, sans-serif',
  defaultRadius: 'md',
})

<MantineProvider theme={theme}>
  <App />
</MantineProvider>
```

## When to Choose Mantine

**Choose Mantine when:**
- Want full-featured library with modern DX
- Need extensive hooks library
- Building applications with many forms
- Want built-in dark mode
- Need date pickers, rich text, file upload

**Consider alternatives when:**
- Using Tailwind → shadcn/ui
- Need Material Design → MUI
- Building admin panels → Ant Design
- Want smallest bundle → Chakra

## Mantine vs Alternatives

| Aspect | Mantine | MUI | Chakra | Ant Design |
|--------|---------|-----|--------|------------|
| Components | 120+ | 50+ | 50+ | 60+ |
| Hooks | 70+ | Few | Few | Few |
| Styling | CSS-in-JS | CSS-in-JS | Props | CSS |
| Bundle | Medium | Large | Medium | Large |
| DX | Excellent | Good | Excellent | Good |
| Form | Built-in | External | External | Built-in |

## Unique Features

- **Spotlight**: Command palette (Cmd+K)
- **Notifications**: Toast system
- **Modals manager**: Programmatic modals
- **Rich text**: Tiptap integration
- **Dropzone**: File upload with preview
- **Carousel**: Built-in carousel

## Resources

- [Official Docs](https://mantine.dev/)
- [GitHub](https://github.com/mantinedev/mantine)
- [Hooks](https://mantine.dev/hooks/package/)
- [UI Components](https://mantine.dev/core/getting-started/)
