# Jotai

> "Primitive and flexible state management for React"

## Quick Facts

| Metric | Value |
|--------|-------|
| GitHub Stars | 20,800 |
| npm Weekly Downloads | 9.3M |
| Bundle Size | ~2KB (core) |
| License | MIT |
| Maintainer | pmndrs (Poimandres) |
| Current Version | 2.16.0 |

## Core Concept: Atoms

Jotai's atomic model is fundamentally different from store-based solutions:

- **Redux/Zustand**: Single store, top-down state tree
- **Jotai**: Independent atoms, bottom-up composition

```javascript
// Each atom is independent
const countAtom = atom(0)
const nameAtom = atom('Guest')
const darkModeAtom = atom(false)
```

## Why Choose Jotai?

1. **Surgical Re-renders**: Only components using changed atoms update
2. **No Selectors Needed**: Atoms ARE the selectors
3. **Derived State Built-in**: Atoms can depend on other atoms
4. **TypeScript First**: Excellent type inference
5. **React Suspense Ready**: Built-in async support

## Basic Usage

```javascript
import { atom, useAtom, useAtomValue, useSetAtom } from 'jotai'

// Primitive atom
const countAtom = atom(0)

// Derived atom (read-only)
const doubleAtom = atom((get) => get(countAtom) * 2)

// Derived atom (read-write)
const countPlusOneAtom = atom(
  (get) => get(countAtom) + 1,
  (get, set, newValue) => set(countAtom, newValue - 1)
)

// In component
function Counter() {
  const [count, setCount] = useAtom(countAtom)
  const double = useAtomValue(doubleAtom)

  return (
    <div>
      <p>Count: {count}, Double: {double}</p>
      <button onClick={() => setCount(c => c + 1)}>+</button>
    </div>
  )
}
```

## Key Features

### Async Atoms
```javascript
const urlAtom = atom('https://api.example.com/data')

const fetchDataAtom = atom(async (get) => {
  const response = await fetch(get(urlAtom))
  return response.json()
})

// Automatically triggers Suspense
function DataComponent() {
  const data = useAtomValue(fetchDataAtom)
  return <pre>{JSON.stringify(data)}</pre>
}
```

### Atom Families (Dynamic Atoms)
```javascript
import { atomFamily } from 'jotai/utils'

const todoAtomFamily = atomFamily((id) =>
  atom({ id, text: '', completed: false })
)

// Usage
const todo1Atom = todoAtomFamily('todo-1')
const todo2Atom = todoAtomFamily('todo-2')
```

### Persistence
```javascript
import { atomWithStorage } from 'jotai/utils'

const darkModeAtom = atomWithStorage('darkMode', false)
// Automatically syncs with localStorage
```

### Integration Extensions

| Extension | Purpose |
|-----------|---------|
| `jotai/utils` | Storage, reset, focusing |
| `jotai-tanstack-query` | TanStack Query integration |
| `jotai-immer` | Immutable updates |
| `jotai-xstate` | XState integration |
| `jotai-trpc` | tRPC integration |

## Comparison with Alternatives

### vs Zustand
| Aspect | Jotai | Zustand |
|--------|-------|---------|
| Mental model | Atoms (bottom-up) | Store (top-down) |
| Re-renders | Automatic per-atom | Manual with selectors |
| Derived state | First-class | Manual |
| Learning curve | Different paradigm | Familiar patterns |
| Bundle | 2KB | 3KB |

### vs Recoil
| Aspect | Jotai | Recoil |
|--------|-------|--------|
| Status | Active | **Archived (Jan 2025)** |
| API | Simpler | More features |
| String keys | No | Yes |
| Bundle | 2KB | 22KB |

## Migration from Recoil

Jotai is the natural successor for Recoil projects:

```javascript
// Recoil
const countState = atom({ key: 'count', default: 0 })
const doubleSelector = selector({
  key: 'double',
  get: ({ get }) => get(countState) * 2,
})

// Jotai
const countAtom = atom(0)
const doubleAtom = atom((get) => get(countAtom) * 2)
```

| Recoil | Jotai |
|--------|-------|
| `atom()` | `atom()` |
| `selector()` | `atom()` with getter |
| `useRecoilState()` | `useAtom()` |
| `useRecoilValue()` | `useAtomValue()` |
| `useSetRecoilState()` | `useSetAtom()` |

## When to Choose Jotai

**Choose Jotai when:**
- Need fine-grained reactivity
- Building apps with complex derived state
- Want minimal re-renders by default
- Migrating from Recoil
- Like composing small state pieces

**Consider alternatives when:**
- Team prefers single store → Zustand
- Need strict enterprise patterns → Redux Toolkit
- Prefer reactive/class model → MobX

## Resources

- [Official Docs](https://jotai.org/)
- [GitHub](https://github.com/pmndrs/jotai)
- [Comparison](https://jotai.org/docs/basics/comparison)
