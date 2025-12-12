# Headless UI

> "Completely unstyled, fully accessible UI components, designed to integrate beautifully with Tailwind CSS."

## Quick Facts

| Metric | Value |
|--------|-------|
| GitHub Stars | ~26,000 |
| npm Weekly Downloads | ~800,000 |
| Bundle Size | Small |
| License | MIT |
| Maintainer | Tailwind Labs |
| Framework | React & Vue |

## What Headless UI Is

Headless UI is Tailwind Labs' official component library. It provides the **behavior and accessibility** of complex UI components without any styling - you use Tailwind (or any CSS) to style them.

## Key Differentiator: Vue Support

Unlike Radix (React only), Headless UI supports both React and Vue:

```bash
# React
npm install @headlessui/react

# Vue
npm install @headlessui/vue
```

## How It Works

```tsx
import { Dialog, Transition } from '@headlessui/react'
import { Fragment } from 'react'

function MyDialog({ isOpen, setIsOpen }) {
  return (
    <Transition appear show={isOpen} as={Fragment}>
      <Dialog onClose={() => setIsOpen(false)}>
        <Transition.Child
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-black/25" />
        </Transition.Child>

        <div className="fixed inset-0 overflow-y-auto">
          <Dialog.Panel className="mx-auto max-w-md rounded bg-white p-6">
            <Dialog.Title className="text-lg font-medium">
              Payment successful
            </Dialog.Title>
            <Dialog.Description>
              Your payment has been processed.
            </Dialog.Description>
            <button onClick={() => setIsOpen(false)}>
              Got it, thanks!
            </button>
          </Dialog.Panel>
        </div>
      </Dialog>
    </Transition>
  )
}
```

## Key Features

### Tailwind CSS Plugin
```js
// tailwind.config.js
module.exports = {
  plugins: [
    require('@headlessui/tailwindcss')
  ],
}
```

Enables state-based styling:
```html
<Listbox.Option className="ui-active:bg-blue-500 ui-active:text-white">
  Option
</Listbox.Option>
```

### Built-in Transitions
```tsx
<Transition
  show={isOpen}
  enter="transition-opacity duration-75"
  enterFrom="opacity-0"
  enterTo="opacity-100"
  leave="transition-opacity duration-150"
  leaveFrom="opacity-100"
  leaveTo="opacity-0"
>
  <div>Content</div>
</Transition>
```

### Full Accessibility
- WAI-ARIA compliant
- Keyboard navigation
- Focus management
- Screen reader support

## Available Components

| Component | Description |
|-----------|-------------|
| Menu | Dropdown menus |
| Listbox | Custom select |
| Combobox | Autocomplete select |
| Switch | Toggle switch |
| Disclosure | Show/hide content |
| Dialog | Modal dialogs |
| Popover | Floating panels |
| Radio Group | Radio buttons |
| Tabs | Tabbed interface |
| Transition | CSS transitions |

**Note**: Fewer components than Radix (~10 vs 25+), but covers most common needs.

## When to Choose Headless UI

**Choose Headless UI when:**
- Using Tailwind CSS
- Need Vue support
- Building with Tailwind UI templates
- Want official Tailwind integration
- Need simple, focused component set

**Consider alternatives when:**
- Need more components → Radix UI (25+)
- Want pre-styled → shadcn/ui
- Not using Tailwind → Radix UI

## Headless UI vs Radix

| Aspect | Headless UI | Radix UI |
|--------|-------------|----------|
| Maintainer | Tailwind Labs | WorkOS |
| Framework | React, Vue | React only |
| Components | ~10 | 25+ |
| Focus | Tailwind integration | General headless |
| Transitions | Built-in | Separate |

## Resources

- [Official Docs](https://headlessui.com/)
- [GitHub](https://github.com/tailwindlabs/headlessui)
- [Tailwind UI](https://tailwindui.com/) (premium, uses Headless UI)
