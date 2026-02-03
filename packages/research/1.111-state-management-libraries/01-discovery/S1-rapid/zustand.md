# Zustand

> "A small, fast, and scalable bearbones state-management solution using simplified flux principles."

## Quick Facts

| Metric | Value |
|--------|-------|
| GitHub Stars | 56,076 |
| npm Weekly Downloads | 15.4M |
| Bundle Size | ~3KB |
| License | MIT |
| Maintainer | pmndrs (Poimandres) |
| Current Version | 5.0.9 |

## Why Zustand Dominates 2025

Zustand has become the default React state management choice for several reasons:

1. **Minimal API**: Create state + use it. That's it.
2. **No Provider**: Unlike Redux/Context, no wrapping components
3. **Hook-based**: Native React patterns
4. **Tiny bundle**: 3KB vs 33KB for Redux Toolkit
5. **Batteries included**: Middleware, devtools, persist out of box

## Basic Usage

```javascript
import { create } from 'zustand'

// Create store
const useStore = create((set) => ({
  bears: 0,
  increasePopulation: () => set((state) => ({ bears: state.bears + 1 })),
  removeAllBears: () => set({ bears: 0 }),
}))

// Use in component - no provider needed
function BearCounter() {
  const bears = useStore((state) => state.bears)
  return <h1>{bears} around here...</h1>
}
```

## Key Features

### Selectors for Performance
```javascript
// Only re-renders when `bears` changes
const bears = useStore((state) => state.bears)

// Shallow comparison for objects
import { shallow } from 'zustand/shallow'
const { nuts, honey } = useStore(
  (state) => ({ nuts: state.nuts, honey: state.honey }),
  shallow
)
```

### Middleware Stack
```javascript
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

const useStore = create(
  devtools(
    persist(
      (set) => ({
        bears: 0,
        addBear: () => set((state) => ({ bears: state.bears + 1 })),
      }),
      { name: 'bear-storage' }
    )
  )
)
```

### Async Actions
```javascript
const useStore = create((set) => ({
  fishies: {},
  fetch: async (pond) => {
    const response = await fetch(pond)
    set({ fishies: await response.json() })
  },
}))
```

### Computed/Derived State
```javascript
const useStore = create((set, get) => ({
  bears: 0,
  // Computed value
  doubleBears: () => get().bears * 2,
}))
```

## Middleware Options

| Middleware | Purpose |
|------------|---------|
| `devtools` | Redux DevTools integration |
| `persist` | localStorage/sessionStorage sync |
| `immer` | Immutable updates with mutations |
| `subscribeWithSelector` | Fine-grained subscriptions |

## Comparison with Alternatives

### vs Redux Toolkit
| Aspect | Zustand | Redux Toolkit |
|--------|---------|---------------|
| Bundle | 3KB | 33KB |
| Boilerplate | Minimal | More structure |
| Learning curve | Minutes | Hours |
| DevTools | Good | Excellent |
| Enterprise patterns | Flexible | Enforced |

### vs Jotai
| Aspect | Zustand | Jotai |
|--------|---------|-------|
| Mental model | Single store | Atoms |
| State shape | Top-down | Bottom-up |
| Derived state | Manual | Automatic |
| Re-renders | Selector-based | Atom-based |

## When to Choose Zustand

**Choose Zustand when:**
- Building a new React project
- Want minimal boilerplate
- Team prefers simplicity over structure
- Bundle size matters
- Don't need strict architectural patterns

**Consider alternatives when:**
- Need atomic/fine-grained reactivity → Jotai
- Enterprise with strict patterns → Redux Toolkit
- Prefer reactive/observable model → MobX

## Resources

- [Official Docs](https://zustand.docs.pmnd.rs/)
- [GitHub](https://github.com/pmndrs/zustand)
- [Comparison Guide](https://zustand.docs.pmnd.rs/getting-started/comparison)
