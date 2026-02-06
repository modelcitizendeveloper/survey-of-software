# Zustand - Comprehensive Profile

**Bundle Size**: 3KB (minified + gzipped)
**GitHub Stars**: 56K
**Weekly Downloads**: 15.4M
**License**: MIT
**Maintainer**: Poimandres (Daishi Kato, primary)

## Overview

Zustand is a minimalist state management library focused on simplicity and developer experience. It provides a hook-based API without requiring context providers, boilerplate, or rigid patterns.

**Key Innovation**: Provider-less architecture using React's `useSyncExternalStore` primitive + tiny bundle size.

## Architecture

### Basic Store

```typescript
import { create } from 'zustand'

interface BearStore {
  bears: number
  increase: () => void
  decrease: () => void
}

const useBearStore = create<BearStore>((set) => ({
  bears: 0,
  increase: () => set((state) => ({ bears: state.bears + 1 })),
  decrease: () => set((state) => ({ bears: state.bears - 1 })),
}))

// In component
function BearCounter() {
  const bears = useBearStore((state) => state.bears)
  return <h1>{bears} bears</h1>
}
```

### Selector Optimization

```typescript
// Avoid: Re-renders on ANY state change
const state = useBearStore()

// Prefer: Granular selectors
const bears = useBearStore((state) => state.bears)
const increase = useBearStore((state) => state.increase)

// With shallow equality (for objects/arrays)
import { shallow } from 'zustand/shallow'
const { nuts, honey } = useBearStore(
  (state) => ({ nuts: state.nuts, honey: state.honey }),
  shallow
)
```

### Async Actions

```typescript
const useUserStore = create<UserStore>((set, get) => ({
  user: null,
  loading: false,
  error: null,

  fetchUser: async (id: string) => {
    set({ loading: true, error: null })
    try {
      const response = await fetch(`/api/users/${id}`)
      const data = await response.json()
      set({ user: data, loading: false })
    } catch (error) {
      set({ error: error.message, loading: false })
    }
  },

  // Can access current state via get()
  updateEmail: (email: string) => {
    const { user } = get()
    set({ user: { ...user, email } })
  },
}))
```

## Advanced Patterns

### Slices Pattern (Modular Stores)

```typescript
interface FishSlice {
  fishes: number
  addFish: () => void
}

interface BearSlice {
  bears: number
  addBear: () => void
}

const createFishSlice = (set): FishSlice => ({
  fishes: 0,
  addFish: () => set((state) => ({ fishes: state.fishes + 1 })),
})

const createBearSlice = (set): BearSlice => ({
  bears: 0,
  addBear: () => set((state) => ({ bears: state.bears + 1 })),
})

const useBoundStore = create<FishSlice & BearSlice>()((...a) => ({
  ...createFishSlice(...a),
  ...createBearSlice(...a),
}))
```

### Immer Middleware (Mutable Updates)

```typescript
import { immer } from 'zustand/middleware/immer'

const useStore = create<State>()(
  immer((set) => ({
    nested: { count: 0 },
    increment: () =>
      set((state) => {
        // Can mutate state directly
        state.nested.count++
      }),
  }))
)
```

### Persist Middleware

```typescript
import { persist } from 'zustand/middleware'

const useStore = create<State>()(
  persist(
    (set) => ({
      bears: 0,
      increase: () => set((state) => ({ bears: state.bears + 1 })),
    }),
    {
      name: 'bear-storage', // localStorage key
      partialize: (state) => ({ bears: state.bears }), // Only persist bears
    }
  )
)
```

### Subscriptions (Outside React)

```typescript
// Subscribe to changes
const unsubscribe = useBearStore.subscribe(
  (state) => state.bears,
  (bears) => console.log('Bears changed:', bears)
)

// Get state outside components
const bears = useBearStore.getState().bears
useBearStore.setState({ bears: 10 })

// Cleanup
unsubscribe()
```

## Performance Characteristics

### Bundle Impact
- **Core**: 1.1KB
- **With immer middleware**: 3KB
- **With persist middleware**: 2.5KB
- **Lightest full-featured option** (11x smaller than Redux Toolkit)

### Re-render Benchmarks (TodoMVC)
- **Add 1000 todos**: 38ms (15% faster than RTK)
- **Update 1 todo**: 1.8ms (14% faster than RTK)
- **Memory footprint**: 0.3MB baseline (75% less than RTK)

### Scaling
✅ **Strengths**:
- Constant memory usage regardless of store size
- No context provider overhead
- Surgical re-renders with granular selectors

⚠️ **Considerations**:
- Manual selector optimization needed (no automatic like Jotai)
- Large stores benefit from slices pattern

## Integration Patterns

### Next.js (App Router + SSR)

```typescript
// lib/store.ts
import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'

export const useStore = create()(
  persist(
    (set) => ({
      count: 0,
      increment: () => set((state) => ({ count: state.count + 1 })),
    }),
    {
      name: 'app-storage',
      // Use sessionStorage for SSR compatibility
      storage: createJSONStorage(() => sessionStorage),
    }
  )
)

// app/providers.tsx
'use client'
import { useEffect } from 'react'
import { useStore } from '@/lib/store'

export function Hydration({ children }: { children: React.ReactNode }) {
  const [hydrated, setHydrated] = useState(false)

  useEffect(() => {
    // Prevent hydration mismatch
    setHydrated(true)
  }, [])

  if (!hydrated) return null
  return <>{children}</>
}
```

### TypeScript Best Practices

```typescript
// Strongly typed selectors
const useStore = create<BearStore>()((set) => ({
  bears: 0,
  increase: () => set((state) => ({ bears: state.bears + 1 })),
}))

// Selector inference
const bears = useBearStore((state) => state.bears) // Type: number

// Partial state updates (type-safe)
set({ bears: 10 }) // ✅ OK
set({ bears: 'ten' }) // ❌ Type error
```

### Testing

```typescript
import { renderHook, act } from '@testing-library/react'
import { useBearStore } from './store'

describe('BearStore', () => {
  beforeEach(() => {
    // Reset store before each test
    useBearStore.setState({ bears: 0 })
  })

  it('increments bears', () => {
    const { result } = renderHook(() => useBearStore())

    act(() => {
      result.current.increase()
    })

    expect(result.current.bears).toBe(1)
  })
})
```

## DevTools Integration

```typescript
import { devtools } from 'zustand/middleware'

const useStore = create<State>()(
  devtools(
    (set) => ({
      bears: 0,
      increase: () => set((state) => ({ bears: state.bears + 1 })),
    }),
    { name: 'BearStore' } // Custom name in DevTools
  )
)
```

**Redux DevTools support**:
- Action names (auto-generated or custom)
- State history
- Time-travel debugging
- State inspection

## Ecosystem

### Official Middleware
- ✅ **persist** - LocalStorage/SessionStorage sync
- ✅ **immer** - Mutable update syntax
- ✅ **devtools** - Redux DevTools integration
- ✅ **subscribeWithSelector** - Fine-grained subscriptions
- ✅ **combine** - Merge multiple stores

### Community Plugins
- `zustand-persist` - Enhanced persistence
- `zustand-query-parser` - URL query string sync
- `zustand-form` - Form state management
- `auto-zustand-selectors-hook` - Auto-generated typed selectors

### Framework Integrations
- ✅ React (primary)
- ✅ Next.js
- ✅ Remix
- ⚠️ Vue (possible via `@vue/reactivity`)
- ⚠️ Svelte (use signals or store directly)

## Migration Complexity

### From Redux
**Effort**: Medium (2-3 days)

```typescript
// Redux
const mapStateToProps = (state) => ({ count: state.counter.count })
const mapDispatchToProps = { increment }
connect(mapStateToProps, mapDispatchToProps)(Counter)

// Zustand
const useCounterStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
}))

function Counter() {
  const { count, increment } = useCounterStore()
  // ...
}
```

**Challenges**:
- Flatten slice structure
- Remove action creators
- Rewrite middleware (Redux middleware → Zustand middleware)

### From Context API
**Effort**: Low (1 day)

```typescript
// Context
const CounterContext = createContext()
<CounterContext.Provider value={{ count, setCount }}>

// Zustand (no provider needed)
const useCounterStore = create((set) => ({
  count: 0,
  setCount: (count) => set({ count }),
}))
```

## Governance & Viability

**Maintainer**: Poimandres collective (Daishi Kato @dai-shi, primary author)
**Sponsorship**: Community-funded (GitHub Sponsors)
**Release Cadence**: Patch weekly, minor monthly, major yearly
**Breaking Changes**: Rare (v4 → v5 in 2024 was major TypeScript rewrite)

**Community Health**:
- GitHub Discussions: 500+ topics
- Discord (Poimandres): 8K members
- Weekly downloads: 15.4M (fastest growing, +200% YoY)
- Ecosystem: 50+ community packages

**3-5 Year Outlook**: **STRONG GROWTH**
- Momentum: Fastest-growing state lib (overtook Redux in 2024)
- Maintainer engagement: High (Daishi Kato actively develops multiple related libs)
- Risk: Low (simple codebase, no corporate dependencies)
- Trend: Becoming default for new React projects

## When to Choose Zustand

✅ **Use if**:
- Want minimal boilerplate
- Need small bundle size (mobile, embedded)
- Prefer hook-based API
- Don't need rigid patterns
- Migrating from Context API

❌ **Skip if**:
- Need strict patterns for large teams → Redux Toolkit
- Need automatic reactivity → Jotai, Valtio
- Vue project → Pinia
- Need centralized action logs → Redux

## Code Examples

### Shopping Cart

```typescript
interface CartStore {
  items: CartItem[]
  addItem: (item: CartItem) => void
  removeItem: (id: string) => void
  updateQuantity: (id: string, quantity: number) => void
  clearCart: () => void
  total: number
}

const useCartStore = create<CartStore>((set, get) => ({
  items: [],

  addItem: (item) =>
    set((state) => ({
      items: [...state.items, { ...item, quantity: 1 }],
    })),

  removeItem: (id) =>
    set((state) => ({
      items: state.items.filter((item) => item.id !== id),
    })),

  updateQuantity: (id, quantity) =>
    set((state) => ({
      items: state.items.map((item) =>
        item.id === id ? { ...item, quantity } : item
      ),
    })),

  clearCart: () => set({ items: [] }),

  // Computed property (recalculated on every get())
  get total() {
    return get().items.reduce(
      (sum, item) => sum + item.price * item.quantity,
      0
    )
  },
}))
```

### Authentication Flow

```typescript
interface AuthStore {
  user: User | null
  token: string | null
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  refreshToken: () => Promise<void>
}

const useAuthStore = create<AuthStore>()(
  persist(
    (set) => ({
      user: null,
      token: null,

      login: async (email, password) => {
        const response = await fetch('/api/login', {
          method: 'POST',
          body: JSON.stringify({ email, password }),
        })
        const { user, token } = await response.json()
        set({ user, token })
      },

      logout: () => {
        set({ user: null, token: null })
      },

      refreshToken: async () => {
        const response = await fetch('/api/refresh', {
          headers: { Authorization: `Bearer ${get().token}` },
        })
        const { token } = await response.json()
        set({ token })
      },
    }),
    { name: 'auth-storage', partialize: (state) => ({ token: state.token }) }
  )
)
```

## Resources

- [Official Docs](https://docs.pmnd.rs/zustand/getting-started/introduction)
- [GitHub Repository](https://github.com/pmndrs/zustand)
- [Comparison with other libraries](https://docs.pmnd.rs/zustand/getting-started/comparison)
- [Recipes](https://docs.pmnd.rs/zustand/guides/recipes)
