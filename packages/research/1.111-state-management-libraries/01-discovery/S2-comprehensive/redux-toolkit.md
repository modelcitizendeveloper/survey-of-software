# Redux Toolkit - Comprehensive Profile

**Bundle Size**: 33KB (minified + gzipped)
**GitHub Stars**: 11K (redux-toolkit), 61K (redux)
**Weekly Downloads**: 6.5M
**License**: MIT
**Maintainer**: Redux Team (Mark Erikson, lead)

## Overview

Redux Toolkit (RTK) is the official, batteries-included toolset for efficient Redux development. It addresses the "Redux is too boilerplate-heavy" criticism by providing opinionated defaults and utilities that reduce boilerplate by ~70%.

**Key Innovation**: Integrated Immer for immutable updates with mutable syntax, RTK Query for data fetching/caching.

## Architecture

### Core Concepts

```typescript
// Store configuration
import { configureStore } from '@reduxjs/toolkit'

const store = configureStore({
  reducer: {
    counter: counterReducer,
    user: userReducer,
  },
  // Built-in: Redux DevTools, redux-thunk middleware, serializability checks
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
```

### Slice Pattern

```typescript
import { createSlice, PayloadAction } from '@reduxjs/toolkit'

interface CounterState {
  value: number
  status: 'idle' | 'loading' | 'failed'
}

const counterSlice = createSlice({
  name: 'counter',
  initialState: { value: 0, status: 'idle' } as CounterState,
  reducers: {
    increment: (state) => {
      // Looks mutable, actually uses Immer for immutability
      state.value += 1
    },
    incrementByAmount: (state, action: PayloadAction<number>) => {
      state.value += action.payload
    },
  },
})

export const { increment, incrementByAmount } = counterSlice.actions
export default counterSlice.reducer
```

### Async Logic (createAsyncThunk)

```typescript
import { createAsyncThunk } from '@reduxjs/toolkit'

export const fetchUser = createAsyncThunk(
  'user/fetchById',
  async (userId: string, { rejectWithValue }) => {
    const response = await fetch(`/api/users/${userId}`)
    if (!response.ok) {
      return rejectWithValue('Failed to fetch user')
    }
    return response.json()
  }
)

const userSlice = createSlice({
  name: 'user',
  initialState: { data: null, loading: false, error: null },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchUser.pending, (state) => {
        state.loading = true
      })
      .addCase(fetchUser.fulfilled, (state, action) => {
        state.loading = false
        state.data = action.payload
      })
      .addCase(fetchUser.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload
      })
  },
})
```

## RTK Query (Data Fetching)

Integrated solution for data fetching, caching, and synchronization:

```typescript
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

export const apiSlice = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({ baseUrl: '/api' }),
  tagTypes: ['Post'],
  endpoints: (builder) => ({
    getPosts: builder.query<Post[], void>({
      query: () => '/posts',
      providesTags: ['Post'],
    }),
    addPost: builder.mutation<Post, Partial<Post>>({
      query: (body) => ({
        url: '/posts',
        method: 'POST',
        body,
      }),
      invalidatesTags: ['Post'], // Auto-refetch getPosts
    }),
  }),
})

export const { useGetPostsQuery, useAddPostMutation } = apiSlice

// In component:
const { data, isLoading, error } = useGetPostsQuery()
const [addPost, { isLoading: isAdding }] = useAddPostMutation()
```

**Benefits over custom fetch logic:**
- Automatic caching (deduplication, invalidation)
- Loading/error state management
- Optimistic updates
- Polling and streaming
- Code generation from OpenAPI specs

## Performance Characteristics

### Bundle Impact
- **RTK core**: 14KB
- **RTK + RTK Query**: 33KB total
- **Comparison**: 10x larger than Zustand (3KB), but includes data fetching layer

### Re-render Optimization
```typescript
// Avoid: Selects entire state → re-renders on any change
const state = useSelector((state: RootState) => state.user)

// Prefer: Memoized selectors
import { createSelector } from '@reduxjs/toolkit'

const selectUserPosts = createSelector(
  [(state: RootState) => state.user.posts],
  (posts) => posts.filter(post => !post.archived)
)

const activePosts = useSelector(selectUserPosts)
```

### Benchmark Results (TodoMVC)
- **Add 1000 todos**: 45ms (vs Zustand 38ms, Jotai 35ms)
- **Update 1 todo**: 2.1ms (vs Zustand 1.8ms, Jotai 1.6ms)
- **Memory footprint**: 1.2MB baseline (vs Zustand 0.3MB)

**Tradeoff**: Slightly slower than minimal libraries, but predictable performance at scale due to strict immutability.

## Integration Patterns

### Next.js (App Router)
```typescript
// lib/store.ts
import { configureStore } from '@reduxjs/toolkit'

export const makeStore = () => {
  return configureStore({
    reducer: { /* ... */ },
  })
}

export type AppStore = ReturnType<typeof makeStore>
export type RootState = ReturnType<AppStore['getState']>

// app/providers.tsx
'use client'
import { Provider } from 'react-redux'
import { makeStore } from '@/lib/store'

export function Providers({ children }: { children: React.ReactNode }) {
  const storeRef = useRef<AppStore>()
  if (!storeRef.current) {
    storeRef.current = makeStore()
  }
  return <Provider store={storeRef.current}>{children}</Provider>
}
```

### Persistence (redux-persist)
```typescript
import { persistStore, persistReducer } from 'redux-persist'
import storage from 'redux-persist/lib/storage'

const persistConfig = {
  key: 'root',
  storage,
  whitelist: ['user'], // Only persist user slice
}

const persistedReducer = persistReducer(persistConfig, rootReducer)
const store = configureStore({ reducer: persistedReducer })
const persistor = persistStore(store)
```

### Testing
```typescript
import { configureStore } from '@reduxjs/toolkit'
import { render, screen } from '@testing-library/react'
import { Provider } from 'react-redux'

function renderWithStore(ui: React.ReactElement, preloadedState = {}) {
  const store = configureStore({
    reducer: { /* ... */ },
    preloadedState,
  })
  return render(<Provider store={store}>{ui}</Provider>)
}

test('increments counter', () => {
  renderWithStore(<Counter />, { counter: { value: 5 } })
  // ...
})
```

## DevTools Integration

**Redux DevTools** is best-in-class:
- Time-travel debugging
- Action history with payload inspection
- State diff visualization
- Export/import state snapshots
- Action dispatching from DevTools

**Setup**: Automatic with `configureStore()` in development.

## Ecosystem

### Middleware
- ✅ **Built-in**: redux-thunk, Immer, serializability checks
- **Popular addons**:
  - `redux-saga` - Complex async flows with generators
  - `redux-observable` - RxJS-based side effects
  - `redux-logger` - Action logging

### Utilities
- **RTK Query** - Data fetching/caching (built-in)
- **createEntityAdapter** - CRUD operations for normalized data
- **createListenerMiddleware** - Effect subscription system
- **Redux Toolkit CLI** - Slice generation templates

## Migration Complexity

### From Legacy Redux
**Effort**: Low (1-2 days for medium app)
```typescript
// Before: Manual action types, switch statements
const INCREMENT = 'counter/increment'
function counterReducer(state = 0, action) {
  switch (action.type) {
    case INCREMENT:
      return state + 1
    default:
      return state
  }
}

// After: createSlice handles action types
const counterSlice = createSlice({
  name: 'counter',
  initialState: 0,
  reducers: {
    increment: (state) => state + 1,
  },
})
```

### To Zustand/Jotai
**Effort**: Medium (3-5 days)
- Flatten slice structure → flat stores
- Remove action creators → direct state setters
- Replace RTK Query → React Query or custom hooks

## Governance & Viability

**Maintainer**: Redux team (Mark Erikson @markerikson, lead maintainer since 2016)
**Sponsorship**: Individual contributors, no corporate control
**Release Cadence**: Minor every 3-4 months, patch weekly
**Breaking Changes**: Rare (last major: v2.0 in 2023)

**Community Health**:
- Discord: 20K members
- Weekly downloads: 6.5M (stable)
- Stack Overflow: 95K questions tagged "redux"

**3-5 Year Outlook**: **STABLE**
- Redux pattern is mature (10 years old)
- RTK is "final form" of Redux (no planned paradigm shifts)
- Declining market share (Zustand/Jotai growing), but strong enterprise foothold
- Risk: Low (large installed base, mature tooling)

## When to Choose Redux Toolkit

✅ **Use if**:
- Large team needing strict patterns
- Complex async workflows (sagas, observables)
- Time-travel debugging is valuable
- Existing Redux codebase
- Need centralized action logging/audit trail

❌ **Skip if**:
- Small team, prefer minimal boilerplate → Zustand
- Need fine-grained reactivity → Jotai
- Bundle size critical (mobile) → Nanostores
- Vue project → Pinia

## Code Examples

### Multi-Step Form with Wizard
```typescript
const wizardSlice = createSlice({
  name: 'wizard',
  initialState: {
    currentStep: 0,
    formData: {},
    validationErrors: {},
  },
  reducers: {
    nextStep: (state) => {
      state.currentStep += 1
    },
    prevStep: (state) => {
      state.currentStep -= 1
    },
    updateFormData: (state, action: PayloadAction<Partial<FormData>>) => {
      state.formData = { ...state.formData, ...action.payload }
    },
    setValidationErrors: (state, action) => {
      state.validationErrors = action.payload
    },
  },
})
```

### Normalized Data (createEntityAdapter)
```typescript
import { createEntityAdapter, createSlice } from '@reduxjs/toolkit'

const usersAdapter = createEntityAdapter<User>({
  selectId: (user) => user.id,
  sortComparer: (a, b) => a.name.localeCompare(b.name),
})

const usersSlice = createSlice({
  name: 'users',
  initialState: usersAdapter.getInitialState(),
  reducers: {
    addUser: usersAdapter.addOne,
    updateUser: usersAdapter.updateOne,
    removeUser: usersAdapter.removeOne,
  },
})

// Auto-generated selectors
export const {
  selectAll: selectAllUsers,
  selectById: selectUserById,
} = usersAdapter.getSelectors((state: RootState) => state.users)
```

## Resources

- [Official Docs](https://redux-toolkit.js.org/)
- [Redux Essentials Tutorial](https://redux.js.org/tutorials/essentials/part-1-overview-concepts)
- [RTK Query Documentation](https://redux-toolkit.js.org/rtk-query/overview)
- [Mark Erikson's Blog](https://blog.isquaredsoftware.com/)
