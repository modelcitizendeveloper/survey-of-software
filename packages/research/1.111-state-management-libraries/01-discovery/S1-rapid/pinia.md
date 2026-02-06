# Pinia

> "The intuitive store for Vue.js"

## Quick Facts

| Metric | Value |
|--------|-------|
| GitHub Stars | ~13,500 |
| npm Weekly Downloads | 3.2M |
| Bundle Size | ~1KB |
| License | MIT |
| Status | **Official Vue state management** |
| Current Version | 3.0.x |

## Official Status

Pinia is the **official state management library for Vue 3**. Vuex is in maintenance mode and will not receive new features.

> "With Pinia serving the same role in the ecosystem, Vuex is now in maintenance mode. It still works, but will no longer receive new features. It is recommended to use Pinia for new applications."

## Why Pinia?

1. **Tiny**: 1KB bundle - smallest state management library
2. **No Mutations**: Unlike Vuex, just modify state directly
3. **TypeScript**: First-class TypeScript support
4. **Modular**: Stores are independent modules
5. **DevTools**: Full Vue DevTools integration
6. **SSR Ready**: Works with Nuxt and SSR out of the box

## Basic Usage

### Options API Style
```javascript
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', {
  state: () => ({
    count: 0,
    name: 'Eduardo',
  }),
  getters: {
    doubleCount: (state) => state.count * 2,
  },
  actions: {
    increment() {
      this.count++
    },
    async fetchData() {
      const res = await fetch('/api/data')
      this.data = await res.json()
    },
  },
})
```

### Composition API Style (Recommended)
```javascript
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCounterStore = defineStore('counter', () => {
  // State
  const count = ref(0)
  const name = ref('Eduardo')

  // Getters
  const doubleCount = computed(() => count.value * 2)

  // Actions
  function increment() {
    count.value++
  }

  async function fetchData() {
    const res = await fetch('/api/data')
    return res.json()
  }

  return { count, name, doubleCount, increment, fetchData }
})
```

### Using in Components
```vue
<script setup>
import { useCounterStore } from '@/stores/counter'

const counter = useCounterStore()

// Access state and getters
console.log(counter.count)
console.log(counter.doubleCount)

// Call actions
counter.increment()

// Destructure with storeToRefs for reactivity
import { storeToRefs } from 'pinia'
const { count, doubleCount } = storeToRefs(counter)
</script>

<template>
  <p>Count: {{ counter.count }}</p>
  <p>Double: {{ counter.doubleCount }}</p>
  <button @click="counter.increment()">+</button>
</template>
```

## Key Features

### No Mutations Required
```javascript
// Vuex (old way)
mutations: {
  SET_COUNT(state, value) {
    state.count = value
  }
}
// Then: commit('SET_COUNT', 5)

// Pinia (new way)
actions: {
  setCount(value) {
    this.count = value  // Direct modification
  }
}
// Or just: store.count = 5
```

### Async Actions
```javascript
// Actions can be async - no separate middleware needed
actions: {
  async fetchUser(id) {
    try {
      this.loading = true
      this.user = await api.getUser(id)
    } catch (error) {
      this.error = error
    } finally {
      this.loading = false
    }
  }
}
```

### Store Composition
```javascript
import { useUserStore } from './user'
import { useCartStore } from './cart'

export const useCheckoutStore = defineStore('checkout', () => {
  const user = useUserStore()
  const cart = useCartStore()

  const canCheckout = computed(() =>
    user.isLoggedIn && cart.items.length > 0
  )

  return { canCheckout }
})
```

### Plugins
```javascript
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

// In store - persist to localStorage
export const useStore = defineStore('main', {
  state: () => ({ saved: '' }),
  persist: true,  // Enable persistence
})
```

## Migration from Vuex

| Vuex | Pinia |
|------|-------|
| `state` | `state` or `ref()` |
| `mutations` | **Removed** (modify state directly) |
| `actions` | `actions` or functions |
| `getters` | `getters` or `computed()` |
| `modules` | Separate stores |
| `mapState` | `storeToRefs()` |
| `commit()` | Direct call or `$patch()` |
| `dispatch()` | Direct call |

### Example Migration

```javascript
// Vuex
const store = new Vuex.Store({
  state: { count: 0 },
  mutations: {
    INCREMENT(state) { state.count++ }
  },
  actions: {
    increment({ commit }) { commit('INCREMENT') }
  },
  getters: {
    double: (state) => state.count * 2
  }
})

// Pinia equivalent
const useStore = defineStore('main', () => {
  const count = ref(0)
  const double = computed(() => count.value * 2)
  function increment() { count.value++ }
  return { count, double, increment }
})
```

## When to Choose Pinia

**Always choose Pinia for Vue 3 projects.** There's no competition in the Vue ecosystem:

- Vuex is deprecated for new projects
- Pinia is official and maintained
- 1KB bundle size (smallest)
- Best TypeScript support

## Resources

- [Official Docs](https://pinia.vuejs.org/)
- [GitHub](https://github.com/vuejs/pinia)
- [Migration from Vuex](https://pinia.vuejs.org/cookbook/migration-vuex.html)
