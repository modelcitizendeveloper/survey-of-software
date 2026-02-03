# MobX - Comprehensive Profile

**Bundle Size**: 16KB (minified + gzipped)
**GitHub Stars**: 27K
**Weekly Downloads**: 1.5M
**License**: MIT
**Maintainer**: Michel Weststrate (creator), community-maintained

## Overview

MobX is a battle-tested reactive state management library based on transparent functional reactive programming (TFRP). It automatically tracks dependencies between observables and reactions, making state management feel magical with minimal boilerplate.

**Key Innovation**: Automatic dependency tracking via Proxies and decorators, making any JavaScript object reactive without explicit subscription management.

## Architecture

### Core Concepts

MobX operates on three core primitives:

1. **Observable state**: Data that can change
2. **Computed values**: Derived values (memoized)
3. **Reactions**: Side effects that run when observables change

```typescript
import { makeObservable, observable, computed, action } from 'mobx'

class TodoStore {
  todos = []

  constructor() {
    makeObservable(this, {
      todos: observable,
      completedCount: computed,
      addTodo: action,
    })
  }

  get completedCount() {
    return this.todos.filter((todo) => todo.completed).length
  }

  addTodo(title: string) {
    this.todos.push({ id: Date.now(), title, completed: false })
  }
}

const todoStore = new TodoStore()
```

### Modern API (makeAutoObservable)

```typescript
import { makeAutoObservable } from 'mobx'

class CounterStore {
  count = 0

  constructor() {
    // Automatically makes all properties observable, getters computed, methods actions
    makeAutoObservable(this)
  }

  get doubleCount() {
    return this.count * 2
  }

  increment() {
    this.count++
  }

  decrement() {
    this.count--
  }
}

export const counterStore = new CounterStore()
```

### React Integration (mobx-react-lite)

```typescript
import { observer } from 'mobx-react-lite'

// Component automatically re-renders when accessed observables change
const Counter = observer(() => {
  return (
    <div>
      <p>Count: {counterStore.count}</p>
      <p>Double: {counterStore.doubleCount}</p>
      <button onClick={() => counterStore.increment()}>+</button>
    </div>
  )
})
```

**How it works**: MobX tracks which observables are accessed during render and subscribes only to those. When they change, the component re-renders.

## Advanced Patterns

### Computed Values (Memoization)

```typescript
class Store {
  users = []
  filter = 'all'

  constructor() {
    makeAutoObservable(this)
  }

  // Automatically cached, only recomputes when dependencies change
  get filteredUsers() {
    console.log('Filtering...') // Only runs when users or filter changes
    return this.users.filter((user) => {
      if (this.filter === 'active') return user.active
      if (this.filter === 'inactive') return !user.active
      return true
    })
  }

  // Can chain computed values
  get filteredUserCount() {
    return this.filteredUsers.length
  }
}
```

### Reactions (Side Effects)

```typescript
import { reaction, autorun, when } from 'mobx'

class UserStore {
  user = null

  constructor() {
    makeAutoObservable(this)

    // Runs whenever user changes
    reaction(
      () => this.user,
      (user) => {
        console.log('User changed:', user)
        localStorage.setItem('user', JSON.stringify(user))
      }
    )

    // Runs immediately and on every change
    autorun(() => {
      console.log('Current user:', this.user)
    })

    // Runs once when condition becomes true
    when(
      () => this.user !== null,
      () => {
        console.log('User logged in!')
      }
    )
  }

  setUser(user) {
    this.user = user
  }
}
```

### Async Actions

```typescript
import { flow } from 'mobx'

class DataStore {
  data = null
  loading = false
  error = null

  constructor() {
    makeAutoObservable(this, {
      fetchData: flow, // Special handling for generators
    })
  }

  // Generator-based async action (recommended)
  *fetchData(id: string) {
    this.loading = true
    this.error = null

    try {
      const response = yield fetch(`/api/data/${id}`)
      this.data = yield response.json()
    } catch (error) {
      this.error = error.message
    } finally {
      this.loading = false
    }
  }

  // Alternative: runInAction for promise-based
  async fetchDataPromise(id: string) {
    this.loading = true
    this.error = null

    try {
      const response = await fetch(`/api/data/${id}`)
      const data = await response.json()

      runInAction(() => {
        this.data = data
        this.loading = false
      })
    } catch (error) {
      runInAction(() => {
        this.error = error.message
        this.loading = false
      })
    }
  }
}
```

### Observable Collections

```typescript
import { observable, computed } from 'mobx'

class TodoListStore {
  // Observable array
  todos = observable([])

  // Observable map
  todosById = observable.map()

  // Observable set
  tags = observable.set()

  constructor() {
    makeAutoObservable(this)
  }

  addTodo(todo) {
    this.todos.push(todo) // Mutate directly, MobX tracks it
    this.todosById.set(todo.id, todo)
    todo.tags.forEach((tag) => this.tags.add(tag))
  }

  get todoCount() {
    return this.todos.length // Automatically reactive
  }
}
```

## Performance Characteristics

### Bundle Impact
- **MobX core**: 16KB
- **mobx-react-lite**: +3KB (19KB total)
- **Comparison**: 5x larger than Zustand, half the size of Redux Toolkit

### Re-render Optimization

MobX's automatic tracking provides excellent performance:

```typescript
class Store {
  user = { name: 'Alice', age: 30, email: 'alice@example.com' }

  constructor() {
    makeAutoObservable(this)
  }
}

// Component A: Only re-renders when name changes
const UserName = observer(() => <h1>{store.user.name}</h1>)

// Component B: Only re-renders when email changes
const UserEmail = observer(() => <p>{store.user.email}</p>)

// Changing email doesn't re-render UserName
store.user.email = 'new@example.com'
```

### Benchmark Results (TodoMVC)
- **Add 1000 todos**: 40ms (slightly faster than RTK)
- **Update 1 todo**: 1.7ms (fastest among tested)
- **Memory footprint**: 0.8MB baseline (2.5x less than RTK)

**Strengths**:
- Fine-grained reactivity (property-level tracking)
- Minimal manual optimization needed
- Efficient for deeply nested state

## Integration Patterns

### Next.js (App Router + SSR)

```typescript
// stores/RootStore.ts
import { makeAutoObservable } from 'mobx'

export class RootStore {
  count = 0

  constructor() {
    makeAutoObservable(this)
  }

  increment() {
    this.count++
  }

  hydrate(data: any) {
    this.count = data.count
  }
}

// app/providers.tsx
'use client'
import { createContext, useContext, useRef } from 'react'
import { RootStore } from '@/stores/RootStore'

const StoreContext = createContext<RootStore | null>(null)

export function StoreProvider({
  children,
  initialState,
}: {
  children: React.ReactNode
  initialState?: any
}) {
  const storeRef = useRef<RootStore>()

  if (!storeRef.current) {
    storeRef.current = new RootStore()
    if (initialState) {
      storeRef.current.hydrate(initialState)
    }
  }

  return (
    <StoreContext.Provider value={storeRef.current}>
      {children}
    </StoreContext.Provider>
  )
}

export function useStore() {
  const store = useContext(StoreContext)
  if (!store) throw new Error('useStore must be used within StoreProvider')
  return store
}

// app/page.tsx (server component)
export default async function Page() {
  const initialCount = await getCountFromDB()

  return (
    <StoreProvider initialState={{ count: initialCount }}>
      <ClientComponent />
    </StoreProvider>
  )
}

// app/ClientComponent.tsx
'use client'
import { observer } from 'mobx-react-lite'
import { useStore } from './providers'

export const ClientComponent = observer(() => {
  const store = useStore()
  return <button onClick={() => store.increment()}>{store.count}</button>
})
```

### TypeScript Best Practices

```typescript
import { makeAutoObservable, runInAction } from 'mobx'

interface User {
  id: string
  name: string
  email: string
}

class UserStore {
  users: User[] = []
  selectedUserId: string | null = null

  constructor() {
    makeAutoObservable(this)
  }

  // Computed value with type inference
  get selectedUser(): User | undefined {
    return this.users.find((u) => u.id === this.selectedUserId)
  }

  // Action with typed parameters
  addUser(user: User): void {
    this.users.push(user)
  }

  // Async action with proper typing
  async fetchUsers(): Promise<void> {
    const response = await fetch('/api/users')
    const users: User[] = await response.json()

    runInAction(() => {
      this.users = users
    })
  }
}

export const userStore = new UserStore()
```

### Testing

```typescript
import { configure } from 'mobx'
import { CounterStore } from './CounterStore'

// Enforce strict mode for tests
configure({ enforceActions: 'always' })

describe('CounterStore', () => {
  let store: CounterStore

  beforeEach(() => {
    store = new CounterStore()
  })

  it('increments count', () => {
    expect(store.count).toBe(0)

    store.increment()

    expect(store.count).toBe(1)
  })

  it('computes double count', () => {
    store.count = 5
    expect(store.doubleCount).toBe(10)
  })

  it('reacts to changes', () => {
    const values: number[] = []

    // Track values as they change
    autorun(() => {
      values.push(store.count)
    })

    store.increment()
    store.increment()

    expect(values).toEqual([0, 1, 2])
  })
})
```

## DevTools Integration

```bash
npm install mobx-react-devtools
```

```typescript
import { observer } from 'mobx-react-lite'
import DevTools from 'mobx-react-devtools'

function App() {
  return (
    <>
      {process.env.NODE_ENV === 'development' && <DevTools />}
      <YourApp />
    </>
  )
}
```

**Features**:
- Observable state tree inspection
- Action tracking
- Change logging
- Performance profiling
- Time-travel debugging (limited)

## Ecosystem

### Official Packages
- ✅ **mobx-react-lite** - React integration (hooks-based)
- ✅ **mobx-react** - React integration (class components + hooks)
- ✅ **mobx-state-tree** - Opinionated, TypeScript-first state management
- ✅ **mobx-utils** - Utility functions (fromPromise, lazyObservable, etc.)
- ✅ **mobx-react-devtools** - DevTools integration

### Community Packages
- `mobx-persist-store` - Persistence layer
- `mobx-react-form` - Form state management
- `mobx-router` - Routing integration
- `serializr` - Serialization/deserialization

### Framework Integrations
- ✅ React (primary)
- ✅ Next.js
- ✅ React Native
- ⚠️ Vue (possible via mobx-vue-lite)
- ⚠️ Angular (mobx-angular)
- ❌ Svelte (not recommended)

## Migration Complexity

### From Redux
**Effort**: Medium-High (4-6 days)

```typescript
// Redux
const increment = () => ({ type: 'INCREMENT' })
dispatch(increment())

// MobX
store.increment() // Direct method calls
```

**Challenges**:
- Shift from immutable patterns to mutable observables
- Remove action creators, reducers (use classes/methods)
- Rewrite middleware (use reactions)
- Flatten normalized state (MobX handles deep updates efficiently)

### From Zustand
**Effort**: Medium (3-4 days)

```typescript
// Zustand
const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
}))

// MobX
class Store {
  count = 0
  constructor() { makeAutoObservable(this) }
  increment() { this.count++ }
}
```

**Challenges**:
- Introduce class-based stores
- Wrap components with `observer`
- Add Provider for context (Zustand is provider-less)

## Governance & Viability

**Maintainer**: Michel Weststrate (creator, now less active), community-maintained
**Sponsorship**: Individual contributors, no corporate backing
**Release Cadence**: Minor every 3-6 months, patch as needed
**Breaking Changes**: Rare (v6 in 2020 was last major, removed decorators as default)

**Community Health**:
- GitHub Issues: ~100 open (well-maintained)
- Stack Overflow: 3K+ questions tagged "mobx"
- Weekly downloads: 1.5M (stable, slight decline from peak)
- Gitter chat: 2K+ members

**3-5 Year Outlook**: **MAINTENANCE MODE**
- Momentum: Stable but declining (overtaken by Zustand/Jotai)
- Maintainer engagement: Moderate (Michel Weststrate focused on other projects)
- Risk: Low-Medium (mature codebase, but shrinking mindshare)
- Trend: Still strong in enterprise, less adopted in new projects
- Long-term: Will remain viable but not cutting-edge

## When to Choose MobX

✅ **Use if**:
- Existing MobX codebase
- Prefer class-based, object-oriented style
- Need transparent reactivity (minimal boilerplate)
- Complex, deeply nested state
- Team experienced with reactive programming

❌ **Skip if**:
- Prefer functional programming → Zustand, Jotai
- Small bundle size critical → Zustand, Nanostores
- Vue project → Pinia
- Want cutting-edge ecosystem → Zustand, Jotai
- Need strict immutability → Redux Toolkit

## Code Examples

### E-Commerce Store

```typescript
import { makeAutoObservable, flow } from 'mobx'

class Product {
  id: string
  name: string
  price: number
  quantity = 0

  constructor(data: ProductData) {
    Object.assign(this, data)
    makeAutoObservable(this)
  }

  get total() {
    return this.price * this.quantity
  }

  updateQuantity(quantity: number) {
    this.quantity = quantity
  }
}

class CartStore {
  products = new Map<string, Product>()
  checkoutStatus: 'idle' | 'pending' | 'success' | 'error' = 'idle'

  constructor() {
    makeAutoObservable(this, {
      checkout: flow,
    })
  }

  get items() {
    return Array.from(this.products.values()).filter((p) => p.quantity > 0)
  }

  get total() {
    return this.items.reduce((sum, item) => sum + item.total, 0)
  }

  get itemCount() {
    return this.items.reduce((sum, item) => sum + item.quantity, 0)
  }

  addProduct(data: ProductData) {
    const product = new Product(data)
    this.products.set(product.id, product)
  }

  updateQuantity(id: string, quantity: number) {
    const product = this.products.get(id)
    if (product) {
      product.updateQuantity(quantity)
    }
  }

  clearCart() {
    this.products.forEach((product) => product.updateQuantity(0))
  }

  *checkout() {
    this.checkoutStatus = 'pending'

    try {
      yield fetch('/api/checkout', {
        method: 'POST',
        body: JSON.stringify({ items: this.items }),
      })

      this.checkoutStatus = 'success'
      this.clearCart()
    } catch (error) {
      this.checkoutStatus = 'error'
    }
  }
}

export const cartStore = new CartStore()

// Component
import { observer } from 'mobx-react-lite'

export const Cart = observer(() => {
  return (
    <div>
      {cartStore.items.map((item) => (
        <div key={item.id}>
          <span>{item.name}</span>
          <input
            type="number"
            value={item.quantity}
            onChange={(e) => cartStore.updateQuantity(item.id, +e.target.value)}
          />
          <span>${item.total}</span>
        </div>
      ))}
      <p>Total: ${cartStore.total} ({cartStore.itemCount} items)</p>
      <button onClick={() => cartStore.checkout()}>
        {cartStore.checkoutStatus === 'pending' ? 'Processing...' : 'Checkout'}
      </button>
    </div>
  )
})
```

### Form State with Validation

```typescript
import { makeAutoObservable, computed } from 'mobx'

class FormField {
  value = ''
  touched = false
  validators: ((value: string) => string | null)[]

  constructor(validators: ((value: string) => string | null)[] = []) {
    this.validators = validators
    makeAutoObservable(this)
  }

  get error() {
    if (!this.touched) return null

    for (const validator of this.validators) {
      const error = validator(this.value)
      if (error) return error
    }

    return null
  }

  get valid() {
    return this.error === null
  }

  setValue(value: string) {
    this.value = value
  }

  setTouched() {
    this.touched = true
  }

  reset() {
    this.value = ''
    this.touched = false
  }
}

class LoginFormStore {
  email = new FormField([
    (v) => (!v ? 'Email required' : null),
    (v) => (!v.includes('@') ? 'Invalid email' : null),
  ])

  password = new FormField([
    (v) => (!v ? 'Password required' : null),
    (v) => (v.length < 8 ? 'Password must be 8+ characters' : null),
  ])

  submitting = false

  constructor() {
    makeAutoObservable(this, {
      fields: computed,
      valid: computed,
      submit: flow,
    })
  }

  get fields() {
    return [this.email, this.password]
  }

  get valid() {
    return this.fields.every((f) => f.valid)
  }

  *submit() {
    // Mark all fields as touched
    this.fields.forEach((f) => f.setTouched())

    if (!this.valid) return

    this.submitting = true

    try {
      yield fetch('/api/login', {
        method: 'POST',
        body: JSON.stringify({
          email: this.email.value,
          password: this.password.value,
        }),
      })

      this.reset()
    } finally {
      this.submitting = false
    }
  }

  reset() {
    this.fields.forEach((f) => f.reset())
  }
}

export const loginFormStore = new LoginFormStore()

// Component
import { observer } from 'mobx-react-lite'

export const LoginForm = observer(() => {
  const { email, password } = loginFormStore

  return (
    <form onSubmit={(e) => { e.preventDefault(); loginFormStore.submit(); }}>
      <input
        value={email.value}
        onChange={(e) => email.setValue(e.target.value)}
        onBlur={() => email.setTouched()}
      />
      {email.error && <span>{email.error}</span>}

      <input
        type="password"
        value={password.value}
        onChange={(e) => password.setValue(e.target.value)}
        onBlur={() => password.setTouched()}
      />
      {password.error && <span>{password.error}</span>}

      <button disabled={!loginFormStore.valid || loginFormStore.submitting}>
        {loginFormStore.submitting ? 'Logging in...' : 'Login'}
      </button>
    </form>
  )
})
```

## Resources

- [Official Docs](https://mobx.js.org/)
- [GitHub Repository](https://github.com/mobxjs/mobx)
- [MobX-State-Tree](https://mobx-state-tree.js.org/) (Opinionated alternative)
- [Egghead.io Course](https://egghead.io/courses/manage-complex-state-in-react-apps-with-mobx)
- [Michel Weststrate's Blog](https://medium.com/@mweststrate)

**Last Updated**: 2026-01-16
**npm Trends**: [MobX vs Zustand vs Redux](https://npmtrends.com/mobx-vs-zustand-vs-redux)
