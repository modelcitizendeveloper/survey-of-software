# Use Case: Vue 3 Projects

**Last Updated**: 2026-01-16
**Framework**: Vue 3 (Composition API)
**Target**: All Vue applications

## Recommendation

**Primary (and only serious choice): Pinia**

## Why Pinia

### Official Vue State Management

Pinia is the official state management library for Vue 3, recommended by the Vue core team.

### Excellent Integration

```typescript
// stores/counter.ts
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', {
  state: () => ({
    count: 0,
    name: 'Counter',
  }),

  getters: {
    doubleCount: (state) => state.count * 2,
  },

  actions: {
    increment() {
      this.count++
    },
    async fetchCount() {
      const data = await fetch('/api/count')
      this.count = data.count
    },
  },
})

// Component (Composition API)
<script setup>
import { useCounterStore } from '@/stores/counter'
import { storeToRefs } from 'pinia'

const counter = useCounterStore()
const { count, doubleCount } = storeToRefs(counter)
</script>

<template>
  <div>
    <p>{{ count }}</p>
    <p>{{ doubleCount }}</p>
    <button @click="counter.increment">+</button>
  </div>
</template>
```

### Key Advantages

1. **Vue DevTools Integration**: Perfect visibility
2. **TypeScript**: Excellent inference
3. **Hot Module Replacement**: Preserves state during dev
4. **SSR Support**: Nuxt 3 integration out-of-box
5. **Composition API Style**: Modern Vue patterns

### When NOT Pinia

**Only if**:
- Multi-framework project (React + Vue) → Nanostores
- Extreme bundle constraints → Nanostores (6KB vs 0.3KB)

**Otherwise**: Always use Pinia for Vue

## Migration from Vuex

Low effort (1-2 days):

```typescript
// Vuex
const store = createStore({
  state: { count: 0 },
  mutations: { increment(state) { state.count++ } },
  actions: { incrementAsync({ commit }) { commit('increment') } },
})

// Pinia (simpler)
const useCounterStore = defineStore('counter', {
  state: () => ({ count: 0 }),
  actions: {
    increment() { this.count++ },
    async incrementAsync() { this.count++ },
  },
})
```

**Wins**: No more mutations, better TypeScript, simpler API

**Last Updated**: 2026-01-16
