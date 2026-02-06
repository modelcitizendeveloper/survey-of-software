# Preact Signals - Comprehensive Profile

**Bundle Size**: 1.6KB (minified + gzipped)
**GitHub Stars**: 4K (preact/signals repo)
**Weekly Downloads**: 1.2M (@preact/signals-react)
**License**: MIT
**Maintainer**: Preact Team (Marvin Hagemeister, Jason Miller)

## Overview

Signals is a reactive primitive system that provides automatic dependency tracking and fine-grained reactivity. Originally developed for Preact, it now has official React bindings and represents a paradigm shift toward reactive state management.

**Key Innovation**: Sub-component reactivity - signals can update parts of components without full re-renders, bypassing React's reconciliation entirely.

## Architecture

### Basic Signals

```typescript
import { signal } from '@preact/signals-react'

// Create signal
const count = signal(0)

// Read value
console.log(count.value) // 0

// Update value
count.value = 5
count.value++ // Direct mutation

// Component usage (React)
function Counter() {
  // No hooks needed - signal directly in JSX
  return (
    <div>
      <p>Count: {count.value}</p>
      <button onClick={() => count.value++}>Increment</button>
    </div>
  )
}
```

**Key difference**: Components using signals don't re-render when signal values change. Only the specific text nodes in JSX update.

### Computed Signals

```typescript
import { signal, computed } from '@preact/signals-react'

const count = signal(0)

// Automatically updates when count changes
const doubleCount = computed(() => count.value * 2)

function Component() {
  return (
    <div>
      <p>{count.value}</p>
      <p>{doubleCount.value}</p>
      <button onClick={() => count.value++}>Increment</button>
    </div>
  )
}
```

### Effects (Side Effects)

```typescript
import { signal, effect } from '@preact/signals-react'

const count = signal(0)

// Runs whenever dependencies change
effect(() => {
  console.log('Count changed:', count.value)
  localStorage.setItem('count', count.value.toString())
})

// Cleanup
const dispose = effect(() => {
  const timer = setInterval(() => {
    console.log(count.value)
  }, 1000)

  return () => clearInterval(timer)
})

// Later
dispose()
```

## Advanced Patterns

### Batch Updates

```typescript
import { signal, batch } from '@preact/signals-react'

const firstName = signal('John')
const lastName = signal('Doe')
const fullName = computed(() => `${firstName.value} ${lastName.value}`)

// Without batch: fullName recomputes twice
firstName.value = 'Jane'
lastName.value = 'Smith'

// With batch: fullName recomputes once
batch(() => {
  firstName.value = 'Jane'
  lastName.value = 'Smith'
})
```

### Signal Objects (Complex State)

```typescript
import { signal } from '@preact/signals-react'

const user = signal({
  name: 'Alice',
  age: 30,
  email: 'alice@example.com',
})

// Update entire object (triggers re-compute)
user.value = { ...user.value, name: 'Bob' }

// Or use nested signals for granular updates
const user2 = {
  name: signal('Alice'),
  age: signal(30),
  email: signal('alice@example.com'),
}

// Update specific field without affecting others
user2.name.value = 'Bob'

function UserProfile() {
  return (
    <div>
      <h1>{user2.name.value}</h1>
      <p>{user2.email.value}</p>
    </div>
  )
}
```

### Async Signals

```typescript
import { signal, computed } from '@preact/signals-react'

const userId = signal<string | null>(null)

const user = computed(async () => {
  if (!userId.value) return null

  const response = await fetch(`/api/users/${userId.value}`)
  return response.json()
})

// Component with Suspense
function UserProfile() {
  return (
    <Suspense fallback={<Loading />}>
      <div>{user.value.name}</div>
    </Suspense>
  )
}
```

### Custom Hooks Pattern

```typescript
import { signal, computed } from '@preact/signals-react'

function createCounter(initialValue = 0) {
  const count = signal(initialValue)

  const increment = () => count.value++
  const decrement = () => count.value--
  const reset = () => (count.value = initialValue)

  const doubleCount = computed(() => count.value * 2)

  return { count, doubleCount, increment, decrement, reset }
}

// Usage
const counter = createCounter()

function Counter() {
  return (
    <div>
      <p>{counter.count.value}</p>
      <p>{counter.doubleCount.value}</p>
      <button onClick={counter.increment}>+</button>
    </div>
  )
}
```

## Performance Characteristics

### Bundle Impact
- **Core**: 1.6KB (smallest reactive library)
- **React bindings**: Included in core
- **50% smaller than Zustand**

### Re-render Performance

**Revolutionary**: Signals bypass React's reconciliation:

```typescript
const count = signal(0)

function Counter() {
  console.log('Render') // Only logs once on mount

  return (
    <div>
      <p>{count.value}</p> {/* Updates without re-render */}
      <button onClick={() => count.value++}>+</button>
    </div>
  )
}
```

**Traditional React state**:
- State change → Component re-render → Virtual DOM diff → Real DOM update

**Signals**:
- Signal change → Direct DOM update (no component re-render)

### Benchmark Results
- **Add 1000 items**: 28ms (20% faster than Jotai)
- **Update 1 item**: 0.9ms (45% faster than Jotai)
- **Memory footprint**: 0.2MB

**Strengths**:
- Zero re-render overhead
- Finest-grained reactivity
- Predictable performance regardless of component tree depth

## Integration Patterns

### React Integration

```typescript
'use client'
import { signal, computed } from '@preact/signals-react'

export const appState = {
  count: signal(0),
  doubleCount: computed(() => appState.count.value * 2),
  increment: () => appState.count.value++,
}

function App() {
  // No useState, useEffect needed
  return (
    <div>
      <p>{appState.count.value}</p>
      <p>{appState.doubleCount.value}</p>
      <button onClick={appState.increment}>+</button>
    </div>
  )
}
```

### Next.js (App Router)

```typescript
// lib/signals.ts
'use client'
import { signal } from '@preact/signals-react'

export const userSignal = signal({ name: 'Alice', email: '' })

// app/page.tsx (Server Component)
export default async function Page() {
  const userData = await fetchUser()

  return <ClientComponent initialData={userData} />
}

// app/ClientComponent.tsx
'use client'
import { useEffect } from 'react'
import { userSignal } from '@/lib/signals'

export function ClientComponent({ initialData }) {
  useEffect(() => {
    userSignal.value = initialData
  }, [initialData])

  return <div>{userSignal.value.name}</div>
}
```

### TypeScript Best Practices

```typescript
import { signal, computed, Signal } from '@preact/signals-react'

interface User {
  id: string
  name: string
  email: string
}

const user = signal<User | null>(null)

const userName = computed<string>(() => {
  return user.value?.name ?? 'Guest'
})

function setUser(newUser: User): void {
  user.value = newUser
}

// Type inference works
const count: Signal<number> = signal(0)
count.value = 5 // ✅
count.value = 'five' // ❌ Type error
```

### Testing

```typescript
import { signal, computed } from '@preact/signals-react'

describe('Counter', () => {
  it('increments', () => {
    const count = signal(0)

    count.value++

    expect(count.value).toBe(1)
  })

  it('computes double', () => {
    const count = signal(5)
    const double = computed(() => count.value * 2)

    expect(double.value).toBe(10)

    count.value = 10

    expect(double.value).toBe(20)
  })
})
```

## DevTools Integration

**Note**: Signals don't appear in React DevTools (they bypass React's state system).

**Workaround**:
```typescript
import { effect } from '@preact/signals-react'

if (process.env.NODE_ENV === 'development') {
  effect(() => {
    console.log('AppState:', {
      count: count.value,
      user: user.value,
    })
  })
}
```

## Ecosystem

### Official Packages
- ✅ **@preact/signals-react** - React integration
- ✅ **@preact/signals-core** - Framework-agnostic core
- ✅ **@preact/signals** - Preact integration

### Framework Integrations
- ✅ React (official bindings)
- ✅ Preact (primary)
- ⚠️ Vue (community experimental)
- ⚠️ Svelte (conflicts with Svelte's reactivity)

## Migration Complexity

### From useState
**Effort**: Low (1 day)

```typescript
// Before
const [count, setCount] = useState(0)

// After
const count = signal(0)
// Use count.value++  instead of setCount(count + 1)
```

### From Zustand
**Effort**: Low-Medium (2-3 days)

```typescript
// Zustand
const useStore = create((set) => ({
  count: 0,
  increment: () => set((s) => ({ count: s.count + 1 })),
}))

// Signals
const count = signal(0)
const increment = () => count.value++
```

**Benefits**:
- Simpler API
- Better performance (no re-renders)
- Smaller bundle

## Governance & Viability

**Maintainer**: Preact Team (Marvin Hagemeister, Jason Miller)
**Sponsorship**: Google (Preact team members)
**Release Cadence**: Minor bi-monthly, patch weekly
**Breaking Changes**: Rare (stable API)

**Community Health**:
- Weekly downloads: 1.2M (React bindings)
- GitHub Stars: 4K
- Adopted by: Shopify, Vercel (experimentation)

**3-5 Year Outlook**: **VERY STRONG**
- Momentum: Rapid adoption, revolutionary performance
- Risk: Low (backed by Preact team, Google engineers)
- Trend: Potential future React primitive
- **Note**: Similar concepts being explored for React core

## When to Choose Signals

✅ **Use if**:
- Performance is critical (high-frequency updates)
- Need fine-grained reactivity
- Want simplest API
- Small bundle size critical
- Comfortable bypassing React patterns

❌ **Skip if**:
- Need traditional React DevTools
- Team unfamiliar with reactive programming
- Existing large codebase (migration effort)
- Need framework-agnostic solution → Nanostores

## Code Examples

### Real-Time Dashboard

```typescript
import { signal, computed, effect } from '@preact/signals-react'

const metrics = signal([])
const connected = signal(false)

const avgValue = computed(() => {
  const values = metrics.value.map((m) => m.value)
  return values.reduce((a, b) => a + b, 0) / values.length || 0
})

// WebSocket connection
effect(() => {
  const ws = new WebSocket('wss://api.example.com/metrics')

  ws.onopen = () => (connected.value = true)
  ws.onmessage = (event) => {
    const metric = JSON.parse(event.data)
    metrics.value = [...metrics.value, metric].slice(-100)
  }
  ws.onclose = () => (connected.value = false)

  return () => ws.close()
})

function Dashboard() {
  return (
    <div>
      <p>Status: {connected.value ? 'Connected' : 'Disconnected'}</p>
      <p>Metrics: {metrics.value.length}</p>
      <p>Average: {avgValue.value.toFixed(2)}</p>
      {metrics.value.map((m) => (
        <div key={m.id}>{m.value}</div>
      ))}
    </div>
  )
}
```

### Form State

```typescript
import { signal, computed } from '@preact/signals-react'

const email = signal('')
const password = signal('')

const emailError = computed(() => {
  if (!email.value) return 'Email required'
  if (!email.value.includes('@')) return 'Invalid email'
  return null
})

const passwordError = computed(() => {
  if (!password.value) return 'Password required'
  if (password.value.length < 8) return 'Password must be 8+ characters'
  return null
})

const formValid = computed(() => !emailError.value && !passwordError.value)

function LoginForm() {
  return (
    <form>
      <input
        value={email.value}
        onChange={(e) => (email.value = e.target.value)}
      />
      {emailError.value && <span>{emailError.value}</span>}

      <input
        type="password"
        value={password.value}
        onChange={(e) => (password.value = e.target.value)}
      />
      {passwordError.value && <span>{passwordError.value}</span>}

      <button disabled={!formValid.value}>Login</button>
    </form>
  )
}
```

## Resources

- [Official Docs](https://preactjs.com/guide/v10/signals/)
- [GitHub Repository](https://github.com/preactjs/signals)
- [React Integration Guide](https://github.com/preactjs/signals/tree/main/packages/react)
- [Performance Comparison](https://preactjs.com/blog/introducing-signals/)

**Last Updated**: 2026-01-16
