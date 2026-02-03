# Valtio - Comprehensive Profile

**Bundle Size**: 3.5KB (minified + gzipped)
**GitHub Stars**: 9K
**Weekly Downloads**: 700K
**License**: MIT
**Maintainer**: Poimandres (Daishi Kato, primary author)

## Overview

Valtio is a proxy-based state management library that makes state mutable and automatically tracks changes. It leverages ES6 Proxies to provide a seamless, intuitive API where you mutate state directly and components automatically re-render when accessed properties change.

**Key Innovation**: Mutable state syntax with automatic immutability under the hood, using Proxies for surgical re-renders without manual optimization.

## Architecture

### Basic Usage

```typescript
import { proxy, useSnapshot } from 'valtio'

// Create mutable proxy state
const state = proxy({
  count: 0,
  text: 'hello',
})

// Mutate directly (no setState, no dispatch)
state.count++
state.text = 'world'

// Component usage
function Counter() {
  const snap = useSnapshot(state) // Snapshot for render

  return (
    <div>
      <p>{snap.count}</p>
      <button onClick={() => state.count++}>Increment</button>
    </div>
  )
}
```

**How it works**: `proxy()` creates a mutable proxy. `useSnapshot()` creates an immutable snapshot for rendering and tracks which properties are accessed, subscribing only to those.

### Nested Objects

```typescript
const state = proxy({
  user: {
    name: 'Alice',
    age: 30,
    address: {
      city: 'NYC',
      zip: '10001',
    },
  },
  todos: [],
})

// Mutate nested properties directly
state.user.name = 'Bob'
state.user.address.city = 'SF'
state.todos.push({ id: 1, title: 'Task 1', done: false })

// Component only re-renders when accessed properties change
function UserCity() {
  const snap = useSnapshot(state)
  return <p>{snap.user.address.city}</p> // Only re-renders when city changes
}
```

## Advanced Patterns

### Derived State (derive)

```typescript
import { proxy, derive } from 'valtio/utils'

const state = proxy({
  count: 0,
})

// Automatically updates when count changes
const derived = derive({
  double: (get) => get(state).count * 2,
  triple: (get) => get(state).count * 3,
})

function Component() {
  const snap = useSnapshot(derived)
  return <p>{snap.double}</p> // Re-renders when count changes
}
```

### Subscriptions

```typescript
import { subscribe } from 'valtio'

const state = proxy({ count: 0 })

// Subscribe to any change
const unsubscribe = subscribe(state, () => {
  console.log('State changed:', state.count)
})

// Cleanup
unsubscribe()
```

### Computed Properties (proxyWithComputed)

```typescript
import { proxyWithComputed } from 'valtio/utils'

const state = proxyWithComputed(
  {
    firstName: 'John',
    lastName: 'Doe',
  },
  {
    // Computed property
    fullName: (snap) => `${snap.firstName} ${snap.lastName}`,
  }
)

function Component() {
  const snap = useSnapshot(state)
  return <h1>{snap.fullName}</h1> // Automatically updates
}
```

### Persistence (proxyWithHistory)

```typescript
import { proxyWithHistory } from 'valtio/utils'

const state = proxyWithHistory({ count: 0 })

// Mutate as usual
state.value.count++

// Undo/redo
state.undo()
state.redo()

// Check history
console.log(state.history) // [{ count: 0 }, { count: 1 }]
console.log(state.index) // Current position in history
```

### Async Actions

```typescript
const state = proxy({
  user: null,
  loading: false,
  error: null,
})

async function fetchUser(id: string) {
  state.loading = true
  state.error = null

  try {
    const response = await fetch(`/api/users/${id}`)
    const data = await response.json()

    state.user = data
  } catch (error) {
    state.error = error.message
  } finally {
    state.loading = false
  }
}

function UserProfile({ userId }) {
  const snap = useSnapshot(state)

  useEffect(() => {
    fetchUser(userId)
  }, [userId])

  if (snap.loading) return <Loading />
  if (snap.error) return <Error message={snap.error} />

  return <div>{snap.user.name}</div>
}
```

## Performance Characteristics

### Bundle Impact
- **Core**: 3.5KB (comparable to Zustand)
- **With utilities**: +1KB
- **Smallest proxy-based solution**

### Re-render Optimization

Valtio automatically tracks property access:

```typescript
const state = proxy({
  user: { name: 'Alice', email: 'alice@example.com' },
  settings: { theme: 'dark' },
})

// Component A: Only re-renders when name changes
function UserName() {
  const snap = useSnapshot(state)
  return <h1>{snap.user.name}</h1>
}

// Component B: Only re-renders when theme changes
function Theme() {
  const snap = useSnapshot(state)
  return <p>{snap.settings.theme}</p>
}

// Changing email doesn't re-render either component
state.user.email = 'new@example.com'
```

### Benchmark Results (TodoMVC)
- **Add 1000 todos**: 36ms (similar to Jotai)
- **Update 1 todo**: 1.7ms (fast)
- **Memory footprint**: 0.4MB baseline

**Strengths**:
- Fine-grained reactivity at property level
- Zero manual optimization needed
- Excellent for deeply nested state

## Integration Patterns

### Next.js (App Router + SSR)

```typescript
'use client'
import { proxy, useSnapshot } from 'valtio'
import { proxyWithHistory } from 'valtio/utils'

// Store definition
export const appState = proxy({
  count: 0,
  increment: () => appState.count++,
})

// SSR hydration
export function useHydrate(initialData: any) {
  useEffect(() => {
    if (initialData) {
      Object.assign(appState, initialData)
    }
  }, [initialData])
}

// Server component
export default async function Page() {
  const initialCount = await getCountFromDB()

  return (
    <ClientComponent initialData={{ count: initialCount }} />
  )
}

// Client component
'use client'
function ClientComponent({ initialData }) {
  useHydrate(initialData)
  const snap = useSnapshot(appState)

  return <button onClick={appState.increment}>{snap.count}</button>
}
```

### TypeScript Best Practices

```typescript
interface User {
  id: string
  name: string
  email: string
}

interface AppState {
  users: User[]
  selectedUserId: string | null
  addUser: (user: User) => void
  selectUser: (id: string) => void
}

const state = proxy<AppState>({
  users: [],
  selectedUserId: null,

  addUser(user) {
    this.users.push(user)
  },

  selectUser(id) {
    this.selectedUserId = id
  },
})

// Type-safe snapshot
function Component() {
  const snap = useSnapshot(state) // Type inferred
  snap.users // Type: User[]
  return <div>{snap.users.length}</div>
}
```

### Testing

```typescript
import { proxy, snapshot } from 'valtio'

describe('Counter Store', () => {
  it('increments count', () => {
    const state = proxy({ count: 0 })

    state.count++

    expect(snapshot(state).count).toBe(1)
  })

  it('handles async actions', async () => {
    const state = proxy({
      data: null,
      fetch: async () => {
        state.data = await Promise.resolve({ value: 42 })
      },
    })

    await state.fetch()

    expect(snapshot(state).data).toEqual({ value: 42 })
  })
})
```

## DevTools Integration

```typescript
import { devtools } from 'valtio/utils'

const state = proxy({ count: 0 })

// Connect to Redux DevTools
devtools(state, { name: 'AppState', enabled: true })

// Now mutations appear in Redux DevTools
state.count++ // Logged as action in DevTools
```

## Ecosystem

### Official Utilities
- ✅ **valtio/utils** - derive, proxyWithComputed, proxyWithHistory
- ✅ **valtio/macro** - Babel macro for advanced optimizations
- ✅ **valtio/vanilla** - Framework-agnostic core

### Framework Integrations
- ✅ React (primary)
- ✅ Vanilla JS
- ⚠️ Vue (via @vue/reactivity adapter)
- ⚠️ Svelte (limited)

## Migration Complexity

### From Zustand
**Effort**: Low (1-2 days)

```typescript
// Zustand
const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
}))

// Valtio
const state = proxy({
  count: 0,
  increment: () => state.count++,
})
```

### From MobX
**Effort**: Low-Medium (2-3 days)

```typescript
// MobX
class Store {
  count = 0
  constructor() { makeAutoObservable(this) }
  increment() { this.count++ }
}

// Valtio
const state = proxy({
  count: 0,
  increment() { this.count++ },
})
```

**Benefits**: Simpler API, no decorators/makeObservable calls.

## Governance & Viability

**Maintainer**: Poimandres (Daishi Kato @dai-shi)
**Sponsorship**: Community-funded
**Release Cadence**: Patch bi-weekly, minor quarterly
**Breaking Changes**: Rare (v2 in 2024)

**Community Health**:
- Weekly downloads: 700K (+100% YoY)
- GitHub Stars: 9K
- Used by: Vercel, Linear (internal)

**3-5 Year Outlook**: **STRONG**
- Momentum: Growing steadily
- Risk: Low (simple, focused)
- Trend: Popular for apps needing mutable API

## When to Choose Valtio

✅ **Use if**:
- Prefer mutable state syntax
- Need fine-grained reactivity
- Small bundle size critical
- Deeply nested state
- Want minimal boilerplate

❌ **Skip if**:
- Prefer immutable patterns → Zustand, Redux
- Need strict enforcement → Redux Toolkit
- Vue project → Pinia

## Code Examples

### Shopping Cart

```typescript
import { proxy, useSnapshot } from 'valtio'

const cartState = proxy({
  items: [],

  addItem(product) {
    const existing = this.items.find((i) => i.id === product.id)

    if (existing) {
      existing.quantity++
    } else {
      this.items.push({ ...product, quantity: 1 })
    }
  },

  updateQuantity(id, quantity) {
    const item = this.items.find((i) => i.id === id)

    if (item) {
      item.quantity = quantity

      if (quantity <= 0) {
        this.removeItem(id)
      }
    }
  },

  removeItem(id) {
    const index = this.items.findIndex((i) => i.id === id)
    if (index !== -1) {
      this.items.splice(index, 1)
    }
  },

  get total() {
    return this.items.reduce((sum, item) => sum + item.price * item.quantity, 0)
  },

  clearCart() {
    this.items = []
  },
})

function Cart() {
  const snap = useSnapshot(cartState)

  return (
    <div>
      {snap.items.map((item) => (
        <div key={item.id}>
          <span>{item.name}</span>
          <input
            type="number"
            value={item.quantity}
            onChange={(e) => cartState.updateQuantity(item.id, +e.target.value)}
          />
        </div>
      ))}
      <p>Total: ${snap.total}</p>
      <button onClick={() => cartState.clearCart()}>Clear</button>
    </div>
  )
}
```

## Resources

- [Official Docs](https://valtio.pmnd.rs/)
- [GitHub Repository](https://github.com/pmndrs/valtio)
- [Examples](https://github.com/pmndrs/valtio/tree/main/examples)
- [Daishi Kato's Blog](https://blog.axlight.com/)

**Last Updated**: 2026-01-16
