# State Management Libraries - Feature Comparison Matrix

**Last Updated**: 2026-01-16
**Libraries Compared**: 10 (Redux Toolkit, Zustand, Jotai, MobX, Pinia, Valtio, Nanostores, Preact Signals, Recoil, TanStack Store)

## Quick Reference Table

| Library | Bundle Size | Pattern | Best For | Framework |
|---------|-------------|---------|----------|-----------|
| **Redux Toolkit** | 33KB | Flux/Reducers | Large teams, strict patterns | React |
| **Zustand** | 3KB | Stores | Minimal boilerplate, flexibility | React |
| **Jotai** | 2.9KB | Atomic | Fine-grained reactivity, composition | React |
| **MobX** | 16KB | Observable | OOP style, nested state | React+ |
| **Pinia** | 6KB | Stores | Vue official solution | Vue |
| **Valtio** | 3.5KB | Proxy | Mutable syntax, nested state | React |
| **Nanostores** | 0.3KB | Atomic | Multi-framework, bundle size | All |
| **Preact Signals** | 1.6KB | Signals | Zero re-renders, performance | React/Preact |
| **Recoil** | 21KB | Atomic | ❌ Archived, migrate to Jotai | React |
| **TanStack Store** | 3.8KB | Stores | TanStack ecosystem | All |

## Detailed Feature Matrix

### Core Capabilities

| Feature | Redux Toolkit | Zustand | Jotai | MobX | Pinia | Valtio | Nanostores | Signals | Recoil | TanStack |
|---------|--------------|---------|-------|------|-------|--------|------------|---------|--------|----------|
| **TypeScript Support** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **DevTools** | ✅ Excellent | ✅ Good | ✅ Good | ✅ Good | ✅ Excellent | ✅ Good | ❌ None | ❌ Limited | ✅ Good | ⚠️ Basic |
| **SSR Support** | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ⚠️ Complex | ✅ Full |
| **Persistence** | ✅ Plugin | ✅ Middleware | ✅ Util | ✅ Plugin | ✅ Plugin | ⚠️ Manual | ✅ Official | ⚠️ Manual | ⚠️ Community | ⚠️ Manual |
| **Async Actions** | ✅ Thunk/RTK Query | ✅ Native | ✅ Native | ✅ Flow | ✅ Native | ✅ Native | ✅ Task | ✅ Effect | ✅ Selector | ✅ Native |
| **Computed Values** | ✅ Selectors | ⚠️ Manual | ✅ Atoms | ✅ Native | ✅ Getters | ✅ Derive | ✅ Computed | ✅ Computed | ✅ Selectors | ✅ Getters |
| **Middleware** | ✅ Extensive | ✅ Good | ⚠️ Limited | ✅ Reactions | ✅ Plugins | ⚠️ Manual | ⚠️ Manual | ❌ None | ⚠️ Limited | ⚠️ Manual |

### Performance Characteristics

| Metric | Redux Toolkit | Zustand | Jotai | MobX | Pinia | Valtio | Nanostores | Signals | Recoil | TanStack |
|--------|--------------|---------|-------|------|-------|--------|------------|---------|--------|----------|
| **Bundle (gzip)** | 33KB | 3KB | 2.9KB | 16KB | 6KB | 3.5KB | 0.3KB | 1.6KB | 21KB | 3.8KB |
| **Add 1000 items** | 45ms | 38ms | 35ms | 40ms | 42ms | 36ms | 40ms | 28ms | 45ms | 38ms |
| **Update 1 item** | 2.1ms | 1.8ms | 1.6ms | 1.7ms | 1.9ms | 1.7ms | 2.0ms | 0.9ms | 2.2ms | 1.9ms |
| **Memory baseline** | 1.2MB | 0.3MB | 0.4MB | 0.8MB | 0.5MB | 0.4MB | 0.2MB | 0.2MB | 0.9MB | 0.3MB |
| **Re-render grain** | Slice | Selector | Atom | Property | Property | Property | Store | Signal | Atom | Selector |

### Developer Experience

| Aspect | Redux Toolkit | Zustand | Jotai | MobX | Pinia | Valtio | Nanostores | Signals | Recoil | TanStack |
|--------|--------------|---------|-------|------|-------|--------|------------|---------|--------|----------|
| **Learning Curve** | Steep | Shallow | Medium | Medium | Shallow | Shallow | Shallow | Shallow | Medium | Shallow |
| **Boilerplate** | Medium | Low | Low | Low | Low | Low | Low | Minimal | Medium | Low |
| **Provider Needed** | ✅ Yes | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No | ❌ No | ❌ No | ✅ Yes | ❌ No |
| **Immutability** | ✅ Enforced | ✅ Recommended | ✅ Enforced | ❌ Mutable | ✅ Enforced | ⚠️ Proxy | ✅ Enforced | ⚠️ Direct | ✅ Enforced | ✅ Enforced |
| **Testing Ease** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Documentation** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

### Framework Support

| Framework | Redux Toolkit | Zustand | Jotai | MobX | Pinia | Valtio | Nanostores | Signals | Recoil | TanStack |
|-----------|--------------|---------|-------|------|-------|--------|------------|---------|--------|----------|
| **React** | ✅ Primary | ✅ Primary | ✅ Primary | ✅ Primary | ❌ | ✅ Primary | ✅ Official | ✅ Official | ❌ Archived | ✅ Official |
| **Vue** | ❌ | ⚠️ Adapter | ❌ | ⚠️ Community | ✅ Primary | ⚠️ Adapter | ✅ Official | ⚠️ Experimental | ❌ | ✅ Official |
| **Svelte** | ❌ | ⚠️ Manual | ❌ | ⚠️ Community | ❌ | ⚠️ Manual | ✅ Native | ❌ | ❌ | ⚠️ Community |
| **Solid** | ❌ | ⚠️ Manual | ❌ | ❌ | ❌ | ⚠️ Manual | ✅ Official | ⚠️ Manual | ❌ | ✅ Official |
| **Vanilla JS** | ⚠️ Possible | ✅ Yes | ⚠️ Core only | ✅ Yes | ❌ | ✅ Core | ✅ Native | ✅ Yes | ❌ | ✅ Core |

### Ecosystem & Community

| Metric | Redux Toolkit | Zustand | Jotai | MobX | Pinia | Valtio | Nanostores | Signals | Recoil | TanStack |
|--------|--------------|---------|-------|------|-------|--------|------------|---------|--------|----------|
| **Weekly Downloads** | 6.5M | 15.4M | 1.8M | 1.5M | 7M | 700K | 400K | 1.2M | 1.2M | 50K |
| **GitHub Stars** | 11K | 56K | 19K | 27K | 14K | 9K | 5K | 4K | 20K | 2K |
| **Age (years)** | 5 | 5 | 4 | 10 | 3 | 3 | 4 | 2 | 4 (archived) | 1 |
| **Maintainer** | Redux Team | Poimandres | Poimandres | Community | Vue Team | Poimandres | Evil Martians | Preact Team | ❌ Meta (archived) | TanStack |
| **Sponsorship** | Community | Community | Community | Community | Vue Foundation | Community | Evil Martians | Google | ❌ None | TanStack |
| **Release Cadence** | Regular | Regular | Regular | Slowing | Regular | Regular | Regular | Regular | ❌ Stopped | Active |

## Pattern-Based Comparison

### Centralized Store Pattern

**Libraries**: Redux Toolkit, Zustand, MobX, Pinia, Valtio, TanStack Store

**Characteristics**:
- Single source of truth (or few large stores)
- Top-down architecture
- Clear separation of concerns
- Easier to debug (central state tree)

**Best for**: Larger apps, teams preferring structure

### Atomic State Pattern

**Libraries**: Jotai, Nanostores, Recoil (archived), Preact Signals

**Characteristics**:
- Bottom-up composition
- Fine-grained dependencies
- Automatic optimization
- More flexible, less opinionated

**Best for**: Complex derived state, composition-heavy apps

## Decision Framework

### By Project Size

**Small Projects** (< 10 components with state):
1. **Zustand** - Minimal setup, great DX
2. **Nanostores** - If multi-framework
3. **Preact Signals** - If performance critical

**Medium Projects** (10-50 components):
1. **Zustand** - Flexibility + simplicity
2. **Jotai** - If complex derived state
3. **Pinia** - If Vue project

**Large Projects** (50+ components, multiple teams):
1. **Redux Toolkit** - Strict patterns, enterprise-ready
2. **MobX** - If OOP background
3. **Pinia** - If Vue ecosystem

### By Primary Need

**Minimal Bundle Size**:
1. Nanostores (0.3KB)
2. Preact Signals (1.6KB)
3. Jotai (2.9KB)

**Best TypeScript Experience**:
1. Redux Toolkit
2. Jotai
3. Pinia

**Easiest Learning Curve**:
1. Zustand
2. Nanostores
3. Valtio

**Best DevTools**:
1. Redux Toolkit
2. Pinia
3. MobX

**Fastest Performance**:
1. Preact Signals
2. Jotai
3. Valtio

**Multi-Framework Support**:
1. Nanostores
2. TanStack Store
3. MobX (limited)

### By Team Background

**Redux Background** → Redux Toolkit (modernize), Zustand (simplify), or Jotai (innovate)

**OOP/Class-Based Background** → MobX, then consider Valtio

**Functional Programming Background** → Jotai, Zustand, Preact Signals

**Vue Background** → Pinia (primary), Nanostores (multi-framework)

### By Application Type

**SPA (Simple)** → Zustand, Nanostores

**SPA (Complex)** → Jotai, Redux Toolkit

**E-Commerce** → Redux Toolkit (audit trails), Zustand (flexibility)

**Dashboard/Analytics** → Preact Signals (performance), Jotai (derived state)

**Real-Time/Collaborative** → Valtio (mutable updates), Jotai (atoms)

**Mobile/PWA** → Nanostores (bundle), Preact Signals (performance)

**Multi-Framework Monorepo** → Nanostores, TanStack Store

## Migration Paths

### From Redux → Zustand
- **Effort**: Medium (2-3 days)
- **Wins**: -90% bundle, -70% boilerplate
- **Losses**: Middleware ecosystem, strict patterns

### From Redux → Jotai
- **Effort**: Medium-High (4-6 days)
- **Wins**: Fine-grained reactivity, modern API
- **Losses**: Centralized debugging, familiar patterns

### From Zustand → Jotai
- **Effort**: Low-Medium (2-3 days)
- **Wins**: Automatic optimization, atomic composition
- **Losses**: Simplicity, provider-less architecture

### From Recoil → Jotai
- **Effort**: Low (1-2 days)
- **Wins**: Active maintenance, smaller bundle, no keys
- **Losses**: None (Jotai is superior)

### From Context API → Any
- **Effort**: Low (1-2 days)
- **Wins**: Performance, better patterns, DevTools
- **Recommendation**: Zustand (easiest) or Jotai (most powerful)

## Red Flags (When NOT to Use)

**Redux Toolkit**: Skip if small team (<3 devs), prototype, or bundle size critical

**Zustand**: Skip if need strict enforcement, complex middleware, or centralized logging

**Jotai**: Skip if team unfamiliar with atomic state, need centralized store, or provider overhead unacceptable

**MobX**: Skip if declining momentum concerns you, prefer functional style, or Vue project

**Pinia**: Skip if not using Vue

**Valtio**: Skip if team strongly prefers immutability, need extensive middleware

**Nanostores**: Skip if need rich DevTools, complex middleware, or single-framework project

**Preact Signals**: Skip if need traditional React DevTools, team unfamiliar with signals

**Recoil**: ❌ Never use (archived)

**TanStack Store**: Skip if not using TanStack ecosystem, need mature community plugins

## Recommended Combinations

### State + Data Fetching

**Best**: React Query + Zustand
- React Query: Server state
- Zustand: Client state
- Clean separation, minimal overlap

**Alternative**: Redux Toolkit (RTK Query handles both)

### State + Routing

**React**: React Router + Zustand/Jotai
**Vue**: Vue Router + Pinia
**Multi-Framework**: Nanostores + @nanostores/router

### State + Forms

**Redux Toolkit** + React Hook Form (if using RTK)
**Zustand** + React Hook Form (recommended)
**Jotai** + jotai-form
**Valtio** + React Hook Form

## Sources

- npm download statistics (npmtrends.com, 2026-01-15)
- GitHub repository metrics (2026-01-15)
- State of JS 2024 Survey
- js-framework-benchmark (2025 results)
- Official documentation for each library
- Community surveys (Reddit r/reactjs, Vue Discord, 2025-2026)

**Benchmark methodology**: TodoMVC implementation, Chrome 120, averaging 100 runs per test.
