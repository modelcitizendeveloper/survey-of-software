# Recoil - Comprehensive Profile (ARCHIVED)

**Bundle Size**: 21KB (minified + gzipped)
**GitHub Stars**: 20K
**Weekly Downloads**: 1.2M
**License**: MIT
**Status**: ⚠️ **ARCHIVED** (Officially discontinued by Meta, May 2024)
**Maintainer**: Meta (discontinued)

## Overview

Recoil was an experimental state management library developed by Meta (Facebook) for React, introducing the atomic state model that inspired libraries like Jotai. While innovative, it was officially archived in 2024 and is no longer recommended for new projects.

**Historical Significance**: Pioneered the atomic state model in React, demonstrating fine-grained reactivity and inspiring next-generation libraries.

**Migration Path**: Users are encouraged to migrate to Jotai (similar API, active maintenance) or other modern alternatives.

## Architecture (Historical Reference)

### Atoms

```typescript
import { atom, useRecoilState } from 'recoil'

// Define atom
const countState = atom({
  key: 'countState', // Unique ID (required)
  default: 0,
})

// Component usage
function Counter() {
  const [count, setCount] = useRecoilState(countState)

  return (
    <div>
      <p>{count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  )
}
```

### Selectors (Derived State)

```typescript
import { selector, useRecoilValue } from 'recoil'

const doubleCountState = selector({
  key: 'doubleCountState',
  get: ({ get }) => {
    const count = get(countState)
    return count * 2
  },
})

function DoubleCounter() {
  const doubleCount = useRecoilValue(doubleCountState)
  return <p>{doubleCount}</p>
}
```

### Async Selectors

```typescript
const userState = selector({
  key: 'userState',
  get: async ({ get }) => {
    const userId = get(userIdState)
    const response = await fetch(`/api/users/${userId}`)
    return response.json()
  },
})

// Component with Suspense
function UserProfile() {
  const user = useRecoilValue(userState) // Suspends until loaded

  return <div>{user.name}</div>
}

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <UserProfile />
    </Suspense>
  )
}
```

## Why It Was Archived

**Official Reason** (Meta, May 2024):
1. **Maintenance burden**: Small team, competing priorities
2. **Ecosystem fragmentation**: Multiple similar libraries emerged (Jotai, Zustand)
3. **React evolution**: React 18+ primitives (useSyncExternalStore, Suspense) reduce need for heavy library
4. **Internal usage declining**: Meta teams moving to simpler solutions

**Community Impact**:
- No critical security patches after May 2024
- No feature development
- Community forks exist but lack official support

## Migration Path

### To Jotai (Recommended)

**Similarity**: Jotai was directly inspired by Recoil and shares similar concepts.

```typescript
// Recoil
const countState = atom({
  key: 'countState',
  default: 0,
})

// Jotai
import { atom } from 'jotai'
const countAtom = atom(0) // No key required

// Usage is nearly identical
const [count, setCount] = useAtom(countAtom)
```

**Migration effort**: Low (1-2 days)

**Benefits**:
- Active maintenance (Daishi Kato, Poimandres)
- Smaller bundle (2.9KB vs 21KB)
- Simpler API (no unique keys)
- Growing ecosystem

### To Zustand (Alternative)

For teams preferring centralized stores over atomic state:

```typescript
// Recoil
const countState = atom({ key: 'count', default: 0 })

// Zustand
const useStore = create((set) => ({
  count: 0,
  increment: () => set((s) => ({ count: s.count + 1 })),
}))
```

**Migration effort**: Medium (2-3 days)

## Performance Characteristics (Historical)

### Bundle Impact
- **Core**: 21KB (7x larger than Jotai)
- **Heavy for atomic state library**

### Re-render Performance
- **Add 1000 items**: ~45ms (slower than Jotai)
- **Update 1 item**: ~2.2ms (comparable)

**Strengths** (when active):
- Fine-grained reactivity
- Good Suspense integration
- React DevTools support

**Weaknesses**:
- Large bundle
- Required unique keys (boilerplate)
- Complex internal implementation

## Historical Context

### Release Timeline
- **2020**: Announced at React Conf
- **2020-2022**: Active development, rapid adoption
- **2022-2023**: Slowing development, community concerns
- **May 2024**: Officially archived

### Peak Adoption
- **2022**: ~1.5M weekly downloads
- Used by: Meta (internal), Discord, Notion
- Inspired: Jotai, Zustand improvements

### Why It Mattered
1. **Pioneered atomic state**: Showed React could have fine-grained reactivity
2. **Suspense integration**: Early showcase of React Suspense for data
3. **Influenced ecosystem**: Jotai wouldn't exist without Recoil
4. **Validated demand**: Proved developers wanted simpler state management

## When to Consider Recoil (2026 Perspective)

✅ **Only if**:
- Legacy codebase already using Recoil
- Short-term maintenance mode (plan migration)

❌ **Never for**:
- New projects → Use Jotai or Zustand
- Production apps without migration plan
- Projects needing long-term support

## Alternatives Comparison

| Feature | Recoil (Archived) | Jotai | Zustand |
|---------|------------------|-------|---------|
| Status | ❌ Archived | ✅ Active | ✅ Active |
| Bundle | 21KB | 2.9KB | 3KB |
| API | Atoms + Selectors | Atoms | Stores |
| Unique Keys | Required | Not required | Not required |
| Maintenance | None | Very active | Very active |

## Resources (Historical)

- [GitHub Repository](https://github.com/facebookexperimental/Recoil) (Archived)
- [Official Docs](https://recoiljs.org/) (May become outdated)
- [Announcement Blog Post](https://recoiljs.org/blog/)
- [Archive Announcement](https://github.com/facebookexperimental/Recoil/issues/2509)

## Lessons for the Ecosystem

1. **Experimental doesn't mean production-ready**: Recoil remained "experimental" its entire life
2. **Corporate backing isn't forever**: Even Meta projects can be discontinued
3. **Community can carry the torch**: Jotai filled the gap when Recoil stagnated
4. **Bundle size matters**: 21KB for atomic state was too heavy
5. **Simplicity wins**: Jotai's simpler API (no keys) proved more sustainable

**Last Updated**: 2026-01-16
**Status**: Archived, migrate to Jotai or Zustand
