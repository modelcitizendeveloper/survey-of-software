# Pinia - Comprehensive Profile

**Bundle Size**: 6KB (minified + gzipped)
**GitHub Stars**: 14K
**Weekly Downloads**: 7M
**License**: MIT
**Maintainer**: Vue.js Core Team (Eduardo San Martin Morote, primary)

## Overview

Pinia is the official state management library for Vue.js, succeeding Vuex as the recommended solution. It provides a simpler, more intuitive API with full TypeScript support and better DevTools integration than its predecessor.

**Key Innovation**: Composition API-first design with automatic type inference, eliminating the need for mutations and supporting both Options API and Composition API styles.

## Architecture

### Store Definition

```typescript
// stores/counter.ts
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', {
  // State
  state: () => ({
    count: 0,
    name: 'Counter',
  }),

  // Getters (computed properties)
  getters: {
    doubleCount: (state) => state.count * 2,

    // Getters can access other getters
    doubleCountPlusOne(): number {
      return this.doubleCount + 1
    },
  },

  // Actions (methods, can be async)
  actions: {
    increment() {
      this.count++
    },

    async fetchCount() {
      const response = await fetch('/api/count')
      const data = await response.json()
      this.count = data.count
    },
  },
})
```

### Composition API Style (Setup Stores)

```typescript
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', () => {
  // State (refs)
  const count = ref(0)
  const name = ref('Counter')

  // Getters (computed)
  const doubleCount = computed(() => count.value * 2)

  // Actions (functions)
  function increment() {
    count.value++
  }

  async function fetchCount() {
    const response = await fetch('/api/count')
    const data = await response.json()
    count.value = data.count
  }

  return { count, name, doubleCount, increment, fetchCount }
})
```

### Component Usage

```vue
<script setup>
import { useCounterStore } from '@/stores/counter'

const counter = useCounterStore()

// Can destructure (but loses reactivity without storeToRefs)
const { count, doubleCount } = counter

// Prefer storeToRefs for reactive destructuring
import { storeToRefs } from 'pinia'
const { count, doubleCount } = storeToRefs(counter)
const { increment } = counter // Actions can be destructured directly
</script>

<template>
  <div>
    <p>Count: {{ counter.count }}</p>
    <p>Double: {{ counter.doubleCount }}</p>
    <button @click="counter.increment">Increment</button>
  </div>
</template>
```

## Advanced Patterns

### State Reset

```typescript
export const useUserStore = defineStore('user', {
  state: () => ({
    name: '',
    email: '',
    age: 0,
  }),

  actions: {
    reset() {
      // Reset to initial state
      this.$reset()
    },

    // Or partial reset
    clearEmail() {
      this.$patch({ email: '' })
    },
  },
})
```

### Subscribing to State Changes

```typescript
import { watch } from 'vue'

const counter = useCounterStore()

// Subscribe to entire store
counter.$subscribe((mutation, state) => {
  console.log('Store changed:', mutation.type, state)

  // Persist to localStorage
  localStorage.setItem('counter', JSON.stringify(state))
})

// Subscribe to specific state
watch(() => counter.count, (newCount) => {
  console.log('Count changed:', newCount)
})
```

### Store Plugins

```typescript
import { createPinia } from 'pinia'

const pinia = createPinia()

// Plugin for persistence
pinia.use(({ store }) => {
  const storedState = localStorage.getItem(store.$id)
  if (storedState) {
    store.$patch(JSON.parse(storedState))
  }

  store.$subscribe((mutation, state) => {
    localStorage.setItem(store.$id, JSON.stringify(state))
  })
})

// Plugin for logging
pinia.use(({ store }) => {
  store.$onAction(({ name, args, after, onError }) => {
    console.log(`Action ${name} called with args:`, args)

    after((result) => {
      console.log(`Action ${name} finished with result:`, result)
    })

    onError((error) => {
      console.error(`Action ${name} failed:`, error)
    })
  })
})

export default pinia
```

### Composing Stores

```typescript
export const useUserStore = defineStore('user', {
  state: () => ({
    userId: null,
  }),

  actions: {
    async fetchUser(id: string) {
      this.userId = id
      // ...
    },
  },
})

export const usePostsStore = defineStore('posts', {
  state: () => ({
    posts: [],
  }),

  actions: {
    async fetchUserPosts() {
      // Access another store
      const userStore = useUserStore()

      const response = await fetch(`/api/users/${userStore.userId}/posts`)
      this.posts = await response.json()
    },
  },
})
```

### Getters with Parameters

```typescript
export const useProductStore = defineStore('products', {
  state: () => ({
    products: [],
  }),

  getters: {
    // Return a function for parameterized getters
    getProductById: (state) => (id: string) => {
      return state.products.find((p) => p.id === id)
    },

    // Or use arrow function directly
    filterByCategory: (state) => (category: string) => {
      return state.products.filter((p) => p.category === category)
    },
  },
})

// Usage
const productStore = useProductStore()
const product = productStore.getProductById('123')
const electronics = productStore.filterByCategory('electronics')
```

## Performance Characteristics

### Bundle Impact
- **Core**: 6KB (2x larger than Zustand, 3x smaller than Redux Toolkit)
- **Lightweight for Vue ecosystem**
- **No dependencies** (beyond Vue itself)

### Re-render Optimization

Vue's reactivity system automatically optimizes re-renders:

```vue
<script setup>
import { useUserStore } from '@/stores/user'
import { storeToRefs } from 'pinia'

const userStore = useUserStore()

// Only re-renders when name changes
const { name } = storeToRefs(userStore)

// Or access specific properties
</script>

<template>
  <h1>{{ userStore.name }}</h1>
</template>
```

### Benchmark Results (Vue TodoMVC)
- **Add 1000 todos**: 42ms
- **Update 1 todo**: 1.9ms
- **Memory footprint**: 0.5MB baseline

**Note**: Direct comparison with React libraries isn't meaningful due to different rendering systems.

## Integration Patterns

### Nuxt 3 (Vue's Next.js equivalent)

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ['@pinia/nuxt'],
})

// stores/counter.ts
export const useCounterStore = defineStore('counter', {
  state: () => ({ count: 0 }),
  actions: {
    increment() {
      this.count++
    },
  },
})

// pages/index.vue
<script setup>
const counter = useCounterStore()
</script>

// Server-side rendering works automatically
```

### SSR with State Hydration

```typescript
// server.ts
import { createPinia } from 'pinia'
import { useUserStore } from './stores/user'

const pinia = createPinia()
const userStore = useUserStore(pinia)

// Fetch initial state on server
await userStore.fetchUser('123')

// Serialize state
const state = pinia.state.value

// Send to client
res.send(`
  <script>
    window.__PINIA_STATE__ = ${JSON.stringify(state)}
  </script>
`)

// client.ts
const pinia = createPinia()

if (window.__PINIA_STATE__) {
  pinia.state.value = window.__PINIA_STATE__
}
```

### TypeScript Best Practices

```typescript
import { defineStore } from 'pinia'

interface User {
  id: string
  name: string
  email: string
}

interface UserState {
  users: User[]
  currentUserId: string | null
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    users: [],
    currentUserId: null,
  }),

  getters: {
    // Return type inferred automatically
    currentUser(state): User | undefined {
      return state.users.find((u) => u.id === state.currentUserId)
    },

    // Explicit return type
    userCount(): number {
      return this.users.length
    },
  },

  actions: {
    // Typed parameters and return
    async fetchUser(id: string): Promise<User> {
      const response = await fetch(`/api/users/${id}`)
      const user: User = await response.json()

      this.users.push(user)
      this.currentUserId = user.id

      return user
    },
  },
})

// Store type is automatically inferred
const userStore = useUserStore()
userStore.currentUser // Type: User | undefined
```

### Testing

```typescript
import { setActivePinia, createPinia } from 'pinia'
import { useCounterStore } from '@/stores/counter'

describe('Counter Store', () => {
  beforeEach(() => {
    // Create fresh pinia instance for each test
    setActivePinia(createPinia())
  })

  it('increments count', () => {
    const counter = useCounterStore()

    expect(counter.count).toBe(0)

    counter.increment()

    expect(counter.count).toBe(1)
  })

  it('computes double count', () => {
    const counter = useCounterStore()

    counter.count = 5

    expect(counter.doubleCount).toBe(10)
  })

  it('resets state', () => {
    const counter = useCounterStore()

    counter.count = 10

    counter.$reset()

    expect(counter.count).toBe(0)
  })
})
```

## DevTools Integration

**Vue DevTools** provides excellent Pinia integration:

- Timeline tracking for all mutations
- State inspection and editing
- Action history
- Time-travel debugging
- Store navigation

```typescript
// Automatic in development, enabled by default
const pinia = createPinia()

// Custom DevTools name
export const useUserStore = defineStore('user', {
  state: () => ({ name: 'Alice' }),
})
```

## Ecosystem

### Official Packages
- ✅ **@pinia/nuxt** - Nuxt integration
- ✅ **@pinia/testing** - Testing utilities
- ✅ **pinia-plugin-persistedstate** - Persistence
- ✅ **pinia-plugin-history** - Undo/redo

### Community Plugins
- `pinia-shared-state` - Cross-tab synchronization
- `pinia-orm` - ORM for normalized data
- `pinia-plugin-debounce` - Debounce actions

### Framework Integrations
- ✅ Vue 3 (primary)
- ✅ Nuxt 3
- ⚠️ Vue 2 (via compatibility plugin)
- ❌ React (Vue-specific)

## Migration Complexity

### From Vuex
**Effort**: Low-Medium (1-3 days)

```typescript
// Vuex
const store = createStore({
  state: { count: 0 },
  mutations: {
    increment(state) {
      state.count++
    },
  },
  actions: {
    incrementAsync({ commit }) {
      setTimeout(() => commit('increment'), 1000)
    },
  },
})

// Pinia
const useCounterStore = defineStore('counter', {
  state: () => ({ count: 0 }),
  actions: {
    increment() {
      this.count++
    },
    async incrementAsync() {
      await new Promise((resolve) => setTimeout(resolve, 1000))
      this.count++
    },
  },
})
```

**Benefits**:
- No more mutations (actions can mutate state directly)
- Better TypeScript support
- Simpler module structure
- Composition API style available

### From Context API (React)
**Not applicable**: Pinia is Vue-specific. For React → Vue migration, consider the entire component rewrite, not just state management.

## Governance & Viability

**Maintainer**: Vue.js Core Team (Eduardo San Martin Morote @posva, primary)
**Sponsorship**: Vue.js Foundation, corporate sponsors
**Release Cadence**: Minor every 2-3 months, patch weekly
**Breaking Changes**: Rare (stable since v2.0 in 2021)

**Community Health**:
- Official Vue.js recommendation (replaced Vuex)
- GitHub Discussions: 200+ topics
- Discord (Vue Land): 60K+ members
- Weekly downloads: 7M (+300% since becoming official)

**3-5 Year Outlook**: **VERY STRONG**
- Momentum: Official Vue state management solution
- Maintainer engagement: Very high (core Vue team)
- Risk: Extremely low (backed by Vue.js project)
- Trend: Will remain the default for Vue ecosystem
- Long-term: Tied to Vue's success (which is very strong)

## When to Choose Pinia

✅ **Use if**:
- Building with Vue 3 or Nuxt 3
- Need official, well-supported solution
- Want excellent TypeScript support
- Migrating from Vuex
- Need DevTools integration

❌ **Skip if**:
- Building with React → Zustand, Jotai
- Building with Svelte → Svelte stores
- Very simple state → Vue's `ref()` and `reactive()` sufficient

## Code Examples

### Shopping Cart (Options API Style)

```typescript
import { defineStore } from 'pinia'

interface CartItem {
  id: string
  name: string
  price: number
  quantity: number
}

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [] as CartItem[],
  }),

  getters: {
    itemCount: (state) => {
      return state.items.reduce((sum, item) => sum + item.quantity, 0)
    },

    total: (state) => {
      return state.items.reduce((sum, item) => sum + item.price * item.quantity, 0)
    },

    getItemById: (state) => (id: string) => {
      return state.items.find((item) => item.id === id)
    },
  },

  actions: {
    addItem(product: Omit<CartItem, 'quantity'>) {
      const existingItem = this.getItemById(product.id)

      if (existingItem) {
        existingItem.quantity++
      } else {
        this.items.push({ ...product, quantity: 1 })
      }
    },

    updateQuantity(id: string, quantity: number) {
      const item = this.getItemById(id)

      if (item) {
        item.quantity = quantity

        if (quantity <= 0) {
          this.removeItem(id)
        }
      }
    },

    removeItem(id: string) {
      const index = this.items.findIndex((item) => item.id === id)

      if (index !== -1) {
        this.items.splice(index, 1)
      }
    },

    clearCart() {
      this.items = []
    },

    async checkout() {
      const response = await fetch('/api/checkout', {
        method: 'POST',
        body: JSON.stringify({ items: this.items }),
      })

      if (response.ok) {
        this.clearCart()
      }
    },
  },
})
```

### User Authentication (Composition API Style)

```typescript
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

interface User {
  id: string
  name: string
  email: string
}

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const isAuthenticated = computed(() => !!user.value && !!token.value)
  const userName = computed(() => user.value?.name ?? 'Guest')

  // Actions
  async function login(email: string, password: string) {
    loading.value = true
    error.value = null

    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })

      if (!response.ok) {
        throw new Error('Login failed')
      }

      const data = await response.json()

      user.value = data.user
      token.value = data.token

      // Store token
      localStorage.setItem('auth_token', data.token)
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Unknown error'
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('auth_token')
  }

  async function refreshToken() {
    const storedToken = localStorage.getItem('auth_token')

    if (!storedToken) return

    try {
      const response = await fetch('/api/refresh', {
        headers: { Authorization: `Bearer ${storedToken}` },
      })

      const data = await response.json()

      user.value = data.user
      token.value = data.token
    } catch {
      logout()
    }
  }

  return {
    user,
    token,
    loading,
    error,
    isAuthenticated,
    userName,
    login,
    logout,
    refreshToken,
  }
})
```

### Real-Time Dashboard (with WebSocket)

```typescript
import { defineStore } from 'pinia'

interface Metric {
  id: string
  value: number
  timestamp: number
}

export const useDashboardStore = defineStore('dashboard', {
  state: () => ({
    metrics: [] as Metric[],
    connected: false,
    ws: null as WebSocket | null,
  }),

  getters: {
    latestMetrics: (state) => {
      return state.metrics.slice(-10) // Last 10 metrics
    },

    averageValue: (state) => {
      if (state.metrics.length === 0) return 0
      const sum = state.metrics.reduce((acc, m) => acc + m.value, 0)
      return sum / state.metrics.length
    },
  },

  actions: {
    connect() {
      this.ws = new WebSocket('wss://api.example.com/metrics')

      this.ws.onopen = () => {
        this.connected = true
      }

      this.ws.onmessage = (event) => {
        const metric: Metric = JSON.parse(event.data)
        this.addMetric(metric)
      }

      this.ws.onclose = () => {
        this.connected = false

        // Reconnect after 5s
        setTimeout(() => this.connect(), 5000)
      }
    },

    disconnect() {
      if (this.ws) {
        this.ws.close()
        this.ws = null
        this.connected = false
      }
    },

    addMetric(metric: Metric) {
      this.metrics.push(metric)

      // Keep only last 1000 metrics
      if (this.metrics.length > 1000) {
        this.metrics = this.metrics.slice(-1000)
      }
    },

    clearMetrics() {
      this.metrics = []
    },
  },
})
```

## Resources

- [Official Docs](https://pinia.vuejs.org/)
- [GitHub Repository](https://github.com/vuejs/pinia)
- [Vue Mastery Course](https://www.vuemastery.com/courses/pinia/)
- [Migration from Vuex](https://pinia.vuejs.org/cookbook/migration-vuex.html)
- [Eduardo's Blog](https://esm.dev/)

**Last Updated**: 2026-01-16
**npm Trends**: [Pinia vs Vuex](https://npmtrends.com/pinia-vs-vuex)
