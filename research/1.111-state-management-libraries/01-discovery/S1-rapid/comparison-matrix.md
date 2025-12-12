# State Management Libraries - Comparison Matrix

## Quantitative Comparison

| Library | Stars | Weekly DL | Bundle | TS Support | React | Vue | Vanilla |
|---------|-------|-----------|--------|------------|-------|-----|---------|
| Zustand | 56K | 15.4M | 3KB | Excellent | Yes | - | Yes |
| Jotai | 21K | 9.3M | 2KB | Excellent | Yes | - | - |
| Redux Toolkit | 11K | 6.5M | 33KB | Excellent | Yes | - | Yes |
| MobX | 28K | 2.3M | 16KB | Excellent | Yes | - | Yes |
| Pinia | 14K | 3.2M | 1KB | Excellent | - | Yes | - |
| TanStack Store | <1K | 50K | 2KB | Excellent | Yes | Yes | Yes |
| Recoil | 20K | 500K | 22KB | Good | Yes | - | - |

## Paradigm Comparison

| Library | Paradigm | Mental Model | Re-render Strategy |
|---------|----------|--------------|-------------------|
| Zustand | Flux-like | Single store | Selector-based |
| Jotai | Atomic | Bottom-up atoms | Per-atom |
| Redux Toolkit | Flux | Actions → Reducers | Selector-based |
| MobX | Reactive | Observables | Automatic tracking |
| Pinia | Store | Composition stores | Reactive refs |
| TanStack Store | Signal | Fine-grained signals | Signal-based |

## Feature Matrix

| Feature | Zustand | Jotai | Redux | MobX | Pinia |
|---------|---------|-------|-------|------|-------|
| DevTools | Good | Good | Excellent | Good | Good |
| Middleware | Yes | Yes | Yes | Yes | Yes |
| Persistence | Plugin | Built-in | Plugin | Plugin | Plugin |
| SSR | Yes | Yes | Yes | Yes | Yes |
| Code splitting | Easy | Easy | Complex | Medium | Easy |
| Data fetching | Manual | Manual | RTK Query | Manual | Manual |
| Time travel | Plugin | - | Built-in | MST | - |

## Learning Curve

```
Easy ──────────────────────────────────────────────── Hard

Zustand ►     (minutes to learn)
Pinia ►       (minutes to learn)
Jotai ►─►     (different paradigm)
MobX ►─►─►    (reactive concepts)
Redux ►─►─►─► (flux patterns, middleware)
```

## Bundle Size Impact

```
Application Size After Adding State Management:

          +1KB  +2KB  +3KB       +16KB        +33KB
            │     │     │           │             │
Pinia ──────┘     │     │           │             │
Jotai ────────────┘     │           │             │
TanStack Store ─────────┘           │             │
Zustand ────────────────────────────┘             │
MobX ─────────────────────────────────────────────┘
Redux Toolkit ────────────────────────────────────────┘
```

## Ecosystem & Integrations

| Library | Data Fetching | Forms | DevTools | SSR Frameworks |
|---------|---------------|-------|----------|----------------|
| Zustand | TanStack Query | Any | Redux DT | Next, Remix |
| Jotai | jotai-tanstack-query | Any | Jotai DT | Next, Remix |
| Redux | RTK Query | React Hook Form | Redux DT | Next, Remix |
| MobX | Manual | mobx-react-form | MobX DT | Next |
| Pinia | VueQuery | VeeValidate | Vue DT | Nuxt |

## Decision Tree

```
Do you use Vue?
├── Yes → Pinia (official, no alternatives)
└── No → React?
    ├── Small/medium project?
    │   ├── Need fine-grained reactivity? → Jotai
    │   └── Want simplest option? → Zustand
    ├── Enterprise/large team?
    │   └── Redux Toolkit (structure, patterns)
    └── Prefer reactive programming?
        └── MobX
```

## 2025 Trends

| Trend | Impact |
|-------|--------|
| Recoil archived | Migrate to Jotai or Zustand |
| Zustand dominance | Default for new React projects |
| Signal-based (TanStack) | Emerging, watch for adoption |
| Bundle size focus | Favors Zustand, Jotai, Pinia |
| TypeScript adoption | All major libraries have excellent support |

## Recommendation Summary

| Use Case | Primary | Alternative |
|----------|---------|-------------|
| New React project | Zustand | - |
| Fine-grained React | Jotai | Zustand |
| Enterprise React | Redux Toolkit | Zustand |
| Vue 3 | Pinia | - |
| Reactive preference | MobX | - |
| Migrating from Recoil | Jotai | Zustand |
| TanStack ecosystem | TanStack Store | Zustand |
