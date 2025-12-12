# Redux Toolkit

> "The official, opinionated, batteries-included toolset for efficient Redux development"

## Quick Facts

| Metric | Value |
|--------|-------|
| GitHub Stars | 11,086 |
| npm Weekly Downloads | 6.5M |
| Bundle Size | ~33KB |
| License | MIT |
| Maintainer | Redux team (Mark Erikson) |
| Current Version | 2.9.0 |

## Why Redux Still Matters in 2025

Despite newer alternatives, Redux Toolkit remains the enterprise choice:

1. **Predictable State**: Single source of truth, unidirectional data flow
2. **DevTools Excellence**: Time-travel debugging, action logging
3. **RTK Query**: Built-in data fetching and caching
4. **Ecosystem**: Largest middleware and tools ecosystem
5. **Team Scale**: Enforced patterns help large teams

## Basic Usage

```javascript
import { configureStore, createSlice } from '@reduxjs/toolkit'
import { Provider, useSelector, useDispatch } from 'react-redux'

// Create slice (reducer + actions)
const counterSlice = createSlice({
  name: 'counter',
  initialState: { value: 0 },
  reducers: {
    increment: (state) => {
      state.value += 1  // Immer makes this safe
    },
    decrement: (state) => {
      state.value -= 1
    },
    incrementByAmount: (state, action) => {
      state.value += action.payload
    },
  },
})

// Export actions
export const { increment, decrement, incrementByAmount } = counterSlice.actions

// Create store
const store = configureStore({
  reducer: {
    counter: counterSlice.reducer,
  },
})

// Use in component
function Counter() {
  const count = useSelector((state) => state.counter.value)
  const dispatch = useDispatch()

  return (
    <div>
      <p>{count}</p>
      <button onClick={() => dispatch(increment())}>+</button>
      <button onClick={() => dispatch(decrement())}>-</button>
    </div>
  )
}

// Wrap app
function App() {
  return (
    <Provider store={store}>
      <Counter />
    </Provider>
  )
}
```

## Key Features

### RTK Query (Data Fetching)
```javascript
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

const api = createApi({
  baseQuery: fetchBaseQuery({ baseUrl: '/api' }),
  endpoints: (builder) => ({
    getPosts: builder.query({
      query: () => '/posts',
    }),
    addPost: builder.mutation({
      query: (body) => ({
        url: '/posts',
        method: 'POST',
        body,
      }),
    }),
  }),
})

export const { useGetPostsQuery, useAddPostMutation } = api

// In component - automatic caching, loading states, refetching
function Posts() {
  const { data, error, isLoading } = useGetPostsQuery()
  const [addPost] = useAddPostMutation()

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error!</div>

  return data.map(post => <Post key={post.id} {...post} />)
}
```

### Async Thunks
```javascript
import { createAsyncThunk, createSlice } from '@reduxjs/toolkit'

const fetchUser = createAsyncThunk(
  'users/fetchById',
  async (userId, thunkAPI) => {
    const response = await fetch(`/api/users/${userId}`)
    return response.json()
  }
)

const usersSlice = createSlice({
  name: 'users',
  initialState: { entities: [], loading: 'idle' },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchUser.pending, (state) => {
        state.loading = 'pending'
      })
      .addCase(fetchUser.fulfilled, (state, action) => {
        state.loading = 'idle'
        state.entities.push(action.payload)
      })
  },
})
```

### Entity Adapter (Normalized State)
```javascript
import { createEntityAdapter, createSlice } from '@reduxjs/toolkit'

const usersAdapter = createEntityAdapter({
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
} = usersAdapter.getSelectors((state) => state.users)
```

## When to Choose Redux Toolkit

**Choose Redux Toolkit when:**
- Building large enterprise applications
- Team needs enforced patterns and structure
- Need excellent debugging with DevTools
- Using RTK Query for data fetching
- Existing Redux codebase

**Consider alternatives when:**
- Small to medium projects → Zustand
- Bundle size is critical → Zustand (3KB vs 33KB)
- Want simpler mental model → Zustand
- Need atomic reactivity → Jotai

## Comparison

| Aspect | Redux Toolkit | Zustand | Jotai |
|--------|---------------|---------|-------|
| Bundle | 33KB | 3KB | 2KB |
| Boilerplate | Medium | Minimal | Minimal |
| DevTools | Excellent | Good | Good |
| Data fetching | RTK Query | Manual | Manual |
| Learning curve | Medium | Low | Low |
| Enterprise patterns | Enforced | Flexible | Flexible |

## Resources

- [Official Docs](https://redux-toolkit.js.org/)
- [GitHub](https://github.com/reduxjs/redux-toolkit)
- [RTK Query](https://redux-toolkit.js.org/rtk-query/overview)
