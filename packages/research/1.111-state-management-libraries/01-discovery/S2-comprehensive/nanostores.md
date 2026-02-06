# Nanostores - Comprehensive Profile

**Bundle Size**: 334 bytes (core), 1KB with React bindings
**GitHub Stars**: 5K
**Weekly Downloads**: 400K
**License**: MIT
**Maintainer**: Andrey Sitnik (creator of PostCSS, Autoprefixer)

## Overview

Nanostores is a tiny, framework-agnostic state management library that works with React, Vue, Svelte, Solid, and vanilla JavaScript. Its extreme focus on bundle size makes it ideal for micro-frontends and performance-critical applications.

**Key Innovation**: Framework-agnostic design with minimal bundle cost, using atoms and computed stores pattern.

## Architecture

### Atoms (Primitive Stores)

```typescript
import { atom } from 'nanostores'

// Create atom
export const $count = atom(0)

// Get value
console.log($count.get()) // 0

// Set value
$count.set(5)

// Update based on current value
$count.set($count.get() + 1)

// Subscribe to changes
const unbind = $count.subscribe((value) => {
  console.log('Count changed:', value)
})

// Cleanup
unbind()
```

**Naming convention**: Store names prefixed with `$` to distinguish from regular variables.

### Maps (Object Stores)

```typescript
import { map } from 'nanostores'

export const $user = map({
  name: 'Alice',
  email: 'alice@example.com',
  age: 30,
})

// Get entire value
console.log($user.get()) // { name: 'Alice', ... }

// Update specific key
$user.setKey('name', 'Bob')

// Get specific key
console.log($user.get().name) // 'Bob'

// Subscribe to changes
$user.subscribe((value) => {
  console.log('User changed:', value)
})
```

### Computed Stores

```typescript
import { computed } from 'nanostores'

export const $count = atom(0)

// Automatically updates when $count changes
export const $doubleCount = computed($count, (count) => count * 2)

// Can depend on multiple stores
export const $firstName = atom('John')
export const $lastName = atom('Doe')

export const $fullName = computed(
  [$firstName, $lastName],
  (first, last) => `${first} ${last}`
)

// Usage
console.log($fullName.get()) // 'John Doe'
$firstName.set('Jane')
console.log($fullName.get()) // 'Jane Doe'
```

## React Integration

```typescript
import { useStore } from '@nanostores/react'
import { $count, $user } from './stores'

function Counter() {
  const count = useStore($count)

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => $count.set($count.get() + 1)}>Increment</button>
    </div>
  )
}

function UserProfile() {
  const user = useStore($user)

  return (
    <div>
      <h1>{user.name}</h1>
      <input
        value={user.email}
        onChange={(e) => $user.setKey('email', e.target.value)}
      />
    </div>
  )
}
```

## Advanced Patterns

### Actions (Encapsulated Logic)

```typescript
import { atom } from 'nanostores'

export const $todos = atom([])

export function addTodo(title: string) {
  $todos.set([
    ...$todos.get(),
    { id: Date.now(), title, completed: false },
  ])
}

export function toggleTodo(id: number) {
  $todos.set(
    $todos.get().map((todo) =>
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    )
  )
}

export function removeTodo(id: number) {
  $todos.set($todos.get().filter((todo) => todo.id !== id))
}

// Component
function TodoList() {
  const todos = useStore($todos)

  return (
    <div>
      {todos.map((todo) => (
        <div key={todo.id}>
          <span>{todo.title}</span>
          <button onClick={() => toggleTodo(todo.id)}>Toggle</button>
          <button onClick={() => removeTodo(todo.id)}>Remove</button>
        </div>
      ))}
      <button onClick={() => addTodo('New todo')}>Add</button>
    </div>
  )
}
```

### Async Actions

```typescript
import { map } from 'nanostores'

export const $user = map({
  data: null,
  loading: false,
  error: null,
})

export async function fetchUser(id: string) {
  $user.setKey('loading', true)
  $user.setKey('error', null)

  try {
    const response = await fetch(`/api/users/${id}`)
    const data = await response.json()

    $user.setKey('data', data)
  } catch (error) {
    $user.setKey('error', error.message)
  } finally {
    $user.setKey('loading', false)
  }
}

// Component
function UserProfile({ userId }) {
  const { data, loading, error } = useStore($user)

  useEffect(() => {
    fetchUser(userId)
  }, [userId])

  if (loading) return <Loading />
  if (error) return <Error message={error} />

  return <div>{data.name}</div>
}
```

### Tasks (Async Store Pattern)

```typescript
import { task } from 'nanostores'

export const fetchUserTask = task(async (store, userId: string) => {
  const response = await fetch(`/api/users/${userId}`)
  return response.json()
})

// Component
function UserProfile({ userId }) {
  const result = useStore(fetchUserTask(userId))

  if (result.loading) return <Loading />
  if (result.error) return <Error error={result.error} />

  return <div>{result.data.name}</div>
}
```

### Lazy Stores (On-Demand Initialization)

```typescript
import { computed, onMount } from 'nanostores'

export const $userId = atom<string | null>(null)

export const $user = computed($userId, async (userId) => {
  if (!userId) return null

  const response = await fetch(`/api/users/${userId}`)
  return response.json()
})

// Only starts fetching when component mounts
onMount($user, () => {
  console.log('User store mounted')

  return () => {
    console.log('User store unmounted')
  }
})
```

## Performance Characteristics

### Bundle Impact
- **Core**: 334 bytes (smallest state library)
- **React bindings**: +700 bytes (1KB total)
- **With computed**: +200 bytes
- **Comparison**: 3x smaller than Zustand, 50x smaller than Redux Toolkit

### Re-render Optimization

Nanostores provides component-level subscriptions:

```typescript
// Component A: Only subscribes to $firstName
function FirstName() {
  const firstName = useStore($firstName)
  return <p>{firstName}</p>
}

// Component B: Only subscribes to $lastName
function LastName() {
  const lastName = useStore($lastName)
  return <p>{lastName}</p>
}

// Changing $firstName doesn't re-render LastName
```

### Benchmark Results
- **Add 1000 items**: ~40ms
- **Update 1 item**: ~2ms
- **Memory footprint**: <0.2MB

**Strengths**:
- Minimal overhead
- Efficient subscriptions
- Framework-agnostic (no React-specific dependencies)

## Integration Patterns

### Multi-Framework Support

**React**:
```typescript
import { useStore } from '@nanostores/react'
const count = useStore($count)
```

**Vue**:
```typescript
import { useStore } from '@nanostores/vue'
const count = useStore($count)
```

**Svelte**:
```svelte
<script>
  import { count } from './stores'
</script>

<p>Count: {$count}</p>
<button on:click={() => $count.set($count.get() + 1)}>Increment</button>
```

**Solid**:
```typescript
import { useStore } from '@nanostores/solid'
const count = useStore($count)
```

**Vanilla JS**:
```typescript
const unbind = $count.subscribe((value) => {
  document.getElementById('count').textContent = value
})
```

### Persistence

```typescript
import { persistentAtom } from '@nanostores/persistent'

export const $theme = persistentAtom<'light' | 'dark'>('theme', 'light', {
  encode: JSON.stringify,
  decode: JSON.parse,
})

// Automatically syncs with localStorage
$theme.set('dark')
```

### Router Integration

```typescript
import { createRouter } from '@nanostores/router'

export const $router = createRouter({
  home: '/',
  user: '/users/:id',
  post: '/posts/:slug',
})

// Navigate
$router.open('/users/123')

// Get current route
const page = $router.get()
console.log(page.route) // 'user'
console.log(page.params) // { id: '123' }

// React component
function App() {
  const page = useStore($router)

  if (page.route === 'home') return <Home />
  if (page.route === 'user') return <User id={page.params.id} />
  return <NotFound />
}
```

### TypeScript Best Practices

```typescript
import { atom, map, computed } from 'nanostores'

interface User {
  id: string
  name: string
  email: string
}

// Typed atom
export const $userId = atom<string | null>(null)

// Typed map
export const $user = map<User | null>(null)

// Typed computed
export const $userName = computed($user, (user): string => {
  return user?.name ?? 'Guest'
})

// Type-safe actions
export function setUser(user: User): void {
  $user.set(user)
}
```

## Ecosystem

### Official Packages
- ✅ **@nanostores/react** - React integration
- ✅ **@nanostores/vue** - Vue integration
- ✅ **@nanostores/solid** - Solid integration
- ✅ **@nanostores/persistent** - LocalStorage persistence
- ✅ **@nanostores/router** - Routing
- ✅ **@nanostores/query** - Async query utilities

### Framework Integrations
- ✅ React
- ✅ Vue
- ✅ Svelte
- ✅ Solid
- ✅ Vanilla JS
- ✅ Preact

## Migration Complexity

### From Zustand
**Effort**: Low (1-2 days)

```typescript
// Zustand
const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
}))

// Nanostores
export const $count = atom(0)
export const increment = () => $count.set($count.get() + 1)

// Component
const count = useStore($count)
<button onClick={increment}>
```

### From Redux
**Effort**: Medium (2-3 days)

**Benefits**:
- Massive bundle size reduction
- Simpler API
- No boilerplate

## Governance & Viability

**Maintainer**: Andrey Sitnik (@ai, creator of PostCSS)
**Sponsorship**: Community-funded, Evil Martians support
**Release Cadence**: Patch monthly, minor quarterly
**Breaking Changes**: Rare (stable API since v1.0)

**Community Health**:
- Weekly downloads: 400K (+150% YoY)
- GitHub Stars: 5K
- Used by: Astro (official integration)

**3-5 Year Outlook**: **STRONG**
- Momentum: Growing, especially in micro-frontends
- Risk: Low (simple, stable codebase)
- Trend: Becoming standard for multi-framework projects

## When to Choose Nanostores

✅ **Use if**:
- Bundle size is critical (mobile, edge)
- Multi-framework project (monorepo with React + Vue)
- Micro-frontends
- Library/component development
- Simple state needs

❌ **Skip if**:
- Need complex async state → React Query + Zustand
- Need DevTools → Zustand, Redux
- Large team needing strict patterns → Redux Toolkit

## Code Examples

### Authentication Store

```typescript
import { map } from 'nanostores'
import { persistentAtom } from '@nanostores/persistent'

export const $token = persistentAtom<string | null>('auth_token', null)

export const $user = map({
  data: null,
  loading: false,
  error: null,
})

export async function login(email: string, password: string) {
  $user.setKey('loading', true)
  $user.setKey('error', null)

  try {
    const response = await fetch('/api/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    })

    const data = await response.json()

    $user.setKey('data', data.user)
    $token.set(data.token)
  } catch (error) {
    $user.setKey('error', error.message)
  } finally {
    $user.setKey('loading', false)
  }
}

export function logout() {
  $user.set({ data: null, loading: false, error: null })
  $token.set(null)
}

// Component
function LoginForm() {
  const { loading, error } = useStore($user)

  return (
    <form onSubmit={(e) => { e.preventDefault(); login(email, password); }}>
      {/* ... */}
      <button disabled={loading}>
        {loading ? 'Logging in...' : 'Login'}
      </button>
      {error && <p>{error}</p>}
    </form>
  )
}
```

## Resources

- [Official Docs](https://github.com/nanostores/nanostores)
- [React Integration](https://github.com/nanostores/react)
- [Vue Integration](https://github.com/nanostores/vue)
- [Astro Integration](https://docs.astro.build/en/guides/integrations-guide/nano stores/)

**Last Updated**: 2026-01-16
