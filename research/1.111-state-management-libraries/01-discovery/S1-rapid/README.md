# 1.111 State Management Libraries - S1 Rapid Discovery

## Quick Decision Guide

| Situation | Recommendation |
|-----------|----------------|
| New React project (90% of cases) | **Zustand** |
| Enterprise React with strict patterns | Redux Toolkit |
| Need fine-grained reactivity | Jotai |
| Vue project | **Pinia** (official) |
| Reactive programming preference | MobX |
| Already using TanStack ecosystem | TanStack Store |
| Currently using Recoil | **Migrate to Jotai or Zustand** |

## 2025 Landscape Summary

### React Ecosystem

```
Downloads (weekly npm):
Zustand:        ████████████████████████████████  15.4M
Jotai:          ████████████████████             9.3M
Redux Toolkit:  █████████████                    6.5M
MobX:           █████                            2.3M
```

**Key Development**: Recoil (Facebook) was **archived on Jan 1, 2025**. Projects using Recoil should migrate to Jotai (similar atomic model) or Zustand.

### Vue Ecosystem

**Pinia** is the official Vue state management library. Vuex is in maintenance mode. No decision needed - use Pinia.

## Library Profiles

| Library | Bundle | Stars | Paradigm | Learning Curve |
|---------|--------|-------|----------|----------------|
| Zustand | 3KB | 56K | Store + hooks | Very low |
| Jotai | 2KB | 21K | Atomic | Low |
| Redux Toolkit | 33KB | 11K | Flux/reducers | Medium |
| MobX | 16KB | 28K | Observable | Medium |
| Pinia | 1KB | 14K | Store | Very low |
| TanStack Store | 2KB | <1K | Signals | Low |

## When to Use Each

### Zustand (Default Choice)
```javascript
// Create store in 3 lines
const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
}))
```
- Minimal boilerplate
- Hook-based API
- No providers needed
- Middleware support (persist, devtools)
- **Best for**: Most projects

### Jotai (Atomic State)
```javascript
// Define atoms independently
const countAtom = atom(0)
const doubledAtom = atom((get) => get(countAtom) * 2)
```
- Bottom-up state composition
- Surgical re-renders (only what changed)
- Great for complex derived state
- TypeScript-first
- **Best for**: Apps with complex state interdependencies

### Redux Toolkit (Enterprise)
```javascript
// Structured slices with built-in patterns
const counterSlice = createSlice({
  name: 'counter',
  initialState: { value: 0 },
  reducers: {
    increment: (state) => { state.value += 1 },
  },
})
```
- Predictable state updates
- Excellent DevTools
- RTK Query for data fetching
- Time-travel debugging
- **Best for**: Large teams needing strict patterns

### Pinia (Vue Official)
```javascript
// Composition API style
export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const increment = () => count.value++
  return { count, increment }
})
```
- 1KB bundle size
- Full TypeScript support
- DevTools integration
- No mutations (unlike Vuex)
- **Best for**: All Vue 3 projects

### MobX (Reactive)
```javascript
// Observable classes
class TodoStore {
  @observable todos = []
  @action addTodo(todo) { this.todos.push(todo) }
}
```
- Automatic dependency tracking
- Class-based or functional
- Minimal boilerplate
- **Best for**: Teams preferring reactive programming

## Migration Paths

### From Recoil to Jotai
Jotai has similar atomic model:
- `atom()` → `atom()`
- `selector()` → `atom()` with getter
- `useRecoilState()` → `useAtom()`
- `useRecoilValue()` → `useAtomValue()`

### From Vuex to Pinia
- State → `state` or `ref()`
- Mutations → removed (just modify state)
- Actions → `actions` or functions
- Getters → `getters` or `computed()`

## Sources

- [State Management in 2025 - DEV](https://dev.to/hijazi313/state-management-in-2025-when-to-use-context-redux-zustand-or-jotai-2d2k)
- [Zustand vs Redux vs Jotai - Better Stack](https://betterstack.com/community/guides/scaling-nodejs/zustand-vs-redux-toolkit-vs-jotai/)
- [Pinia Official Docs](https://pinia.vuejs.org/)
- [Recoil Archive Notice](https://github.com/facebookexperimental/Recoil)
- [TanStack Store](https://tanstack.com/store/latest/docs/overview)
