# State Management: Domain Explainer

## What Is State Management?

State management refers to how an application tracks, stores, and updates data that changes over time. In frontend applications, "state" is any data that affects what the user sees or can interact with.

### Examples of State

| State Type | Examples |
|------------|----------|
| UI State | Is the modal open? Which tab is selected? |
| Form State | What has the user typed? Are there validation errors? |
| Server Cache | Data fetched from APIs (users, products, etc.) |
| User Session | Is the user logged in? What are their permissions? |
| Application State | Shopping cart contents, notification queue |

### The Core Problem

As applications grow, managing state becomes complex:

```javascript
// Simple app: State lives in component
function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(count + 1)}>{count}</button>
}

// Complex app: Many components need the same data
// How does the Header know about the cart?
// How does Checkout access user data from Login?
// How does updating one thing notify all interested components?
```

## Key Concepts

### 1. Local vs Global State

**Local state**: Data that belongs to one component.
```javascript
// Local: Only this component cares about isOpen
const [isOpen, setIsOpen] = useState(false)
```

**Global state**: Data that multiple components need.
```javascript
// Global: Many components need user info
// - Header shows username
// - Settings shows preferences
// - API calls need auth token
```

**Rule of thumb**: Start local, lift to global only when needed.

### 2. State Paradigms

#### Flux Pattern (Redux, Zustand)
Unidirectional data flow: Actions → Store → View

```
User clicks button
    → Dispatch action { type: 'INCREMENT' }
    → Store processes action, updates state
    → Components subscribed to state re-render
```

**Characteristics**:
- Centralized store (single source of truth)
- Explicit updates via actions/reducers
- Predictable, debuggable
- More boilerplate

#### Atomic Pattern (Jotai, Recoil)
State as independent atoms that compose together.

```
countAtom: 0
doubleAtom: derives from countAtom → countAtom * 2
userAtom: { name: 'Alice' }
```

**Characteristics**:
- Bottom-up composition
- Fine-grained reactivity (per-atom re-renders)
- No central store
- Less boilerplate, different mental model

#### Reactive/Observable Pattern (MobX)
Automatic dependency tracking via observables.

```javascript
// When user.name changes, anything using it auto-updates
@observable user = { name: 'Alice' }
// MobX tracks which components read user.name
```

**Characteristics**:
- Automatic re-renders (no selectors)
- Mutable-looking syntax (actually tracked)
- Class-based or functional
- Less familiar to developers used to React patterns

### 3. Re-renders and Performance

The core performance challenge in React is unnecessary re-renders.

**Problem**: When state changes, React re-renders components. If global state lives in Context, ALL consumers re-render.

```javascript
// Context anti-pattern: Every consumer re-renders on ANY change
const AppContext = createContext({ user: null, theme: 'light', cart: [] })

// Header only needs user, but re-renders when cart changes
function Header() {
  const { user } = useContext(AppContext) // Re-renders on cart change!
}
```

**Solutions**:

| Approach | How It Works |
|----------|--------------|
| Selectors (Redux/Zustand) | `useSelector(state => state.user)` - only re-render if selected value changes |
| Atoms (Jotai) | Each atom is independent - only components using that atom re-render |
| Observables (MobX) | Automatic tracking - only re-render if observed values change |
| Memoization | `React.memo`, `useMemo`, `useCallback` - prevent re-computation |

### 4. Derived State (Computed Values)

State that's calculated from other state.

```javascript
// Base state
const items = [{ price: 10 }, { price: 20 }]
const taxRate = 0.1

// Derived state
const subtotal = items.reduce((sum, item) => sum + item.price, 0) // 30
const tax = subtotal * taxRate // 3
const total = subtotal + tax // 33
```

**Key question**: Store derived values or compute on demand?

| Approach | Pros | Cons |
|----------|------|------|
| Store computed | Fast reads | Can get out of sync |
| Compute on render | Always fresh | May be slow |
| Memoize | Best of both | Complexity |

State management libraries handle this differently:
- **Redux**: `createSelector` for memoized selectors
- **Jotai**: Derived atoms automatically memoize
- **MobX**: `@computed` decorators auto-cache
- **Zustand**: Manual or with middleware

### 5. Side Effects and Async

State management must handle async operations (API calls, timers).

```javascript
// The async challenge:
// 1. User clicks "Load Data"
// 2. Show loading spinner
// 3. Fetch from API
// 4. Handle success OR error
// 5. Update state accordingly
```

**Patterns**:

| Pattern | Used By | How It Works |
|---------|---------|--------------|
| Thunks | Redux | Actions that return functions |
| Sagas | Redux | Generator functions for complex flows |
| Async actions | Zustand/MobX | Just use async/await directly |
| Query libraries | TanStack Query | Separate cache for server state |

**Modern trend**: Separate "server state" (API data) from "client state" (UI). Use TanStack Query / SWR for server state, simpler library for client state.

### 6. DevTools and Debugging

State management libraries provide debugging tools:

| Tool | Features |
|------|----------|
| Redux DevTools | Action log, state diff, time-travel |
| React DevTools | Component tree, hooks inspection |
| MobX DevTools | Observable tracking, action log |
| Jotai DevTools | Atom values, dependency graph |

**Time-travel debugging**: Redux's killer feature - replay past actions to reproduce bugs.

## Common Patterns

### Provider Pattern
Wrap app in a Provider to make state available.

```jsx
// Required for: Redux, Recoil
<Provider store={store}>
  <App />
</Provider>

// Not required for: Zustand, Jotai (optional)
function App() {
  const state = useStore() // Just works
}
```

### Selector Pattern
Select only the state you need to minimize re-renders.

```javascript
// Bad: Subscribes to entire store
const state = useStore()
const user = state.user // Re-renders on ANY state change

// Good: Subscribes to specific slice
const user = useStore(state => state.user) // Only re-renders if user changes
```

### Normalization
Flatten nested data to avoid duplication.

```javascript
// Nested (problematic)
{
  posts: [
    { id: 1, author: { id: 1, name: 'Alice' }, comments: [...] }
  ]
}

// Normalized (better)
{
  posts: { 1: { id: 1, authorId: 1 } },
  users: { 1: { id: 1, name: 'Alice' } },
  comments: { ... }
}
```

Redux Toolkit's `createEntityAdapter` helps with this.

### Optimistic Updates
Update UI immediately, sync with server in background.

```javascript
// 1. User clicks "Like"
// 2. Immediately show liked state (optimistic)
// 3. Send request to server
// 4. If fails, revert to previous state
```

## When You Don't Need State Management

### React Context Is Enough When:
- Data changes rarely (theme, locale, auth status)
- Few consumers (<10 components reading)
- Not performance-critical
- Simple app (few global values)

### URL State (React Router)
Store in URL for shareable/bookmarkable state:
- Filters, pagination, search queries
- Selected tab, modal open state

### Form Libraries
Use React Hook Form, Formik instead of global state for forms.

### Server State Libraries
Use TanStack Query, SWR for API data instead of Redux/Zustand.

## The 2025 Landscape

### Trends

1. **Simpler is better**: Zustand's popularity shows developers want less boilerplate
2. **Separation of concerns**: Server state (TanStack Query) vs client state (Zustand)
3. **Signals emerging**: TanStack Store, Solid.js patterns influencing React
4. **TypeScript-first**: All major libraries have excellent TS support
5. **Bundle size matters**: Zustand (3KB) vs Redux (33KB) is significant

### The Server State Revolution

**Before** (2018-2020):
```javascript
// Redux for EVERYTHING
dispatch(fetchUserStart())
try {
  const user = await api.getUser()
  dispatch(fetchUserSuccess(user))
} catch (error) {
  dispatch(fetchUserError(error))
}
```

**After** (2022+):
```javascript
// TanStack Query for server state
const { data: user, isLoading, error } = useQuery({
  queryKey: ['user'],
  queryFn: api.getUser
})

// Zustand for client state only
const useStore = create(() => ({
  sidebarOpen: false,
  theme: 'dark'
}))
```

## Common Misconceptions

### "I need Redux for any serious app"
**False**: Many production apps use Zustand, Jotai, or even just Context. Redux is one option, not a requirement.

### "Context API is slow"
**Partially true**: Context itself isn't slow, but it causes re-renders for all consumers. Use selectors or split contexts to optimize.

### "More state management = better"
**False**: Start with local state (useState). Only add global state management when you have actual prop-drilling pain.

### "State should be immutable"
**Depends**: React expects immutable updates, but libraries like MobX and Immer let you write mutable-looking code that's actually immutable under the hood.

### "One library for everything"
**Outdated**: Modern pattern is specialized tools: TanStack Query for server state, Zustand/Jotai for client state, React Hook Form for forms.

## Glossary

| Term | Definition |
|------|------------|
| **Action** | Object describing what happened (Redux) |
| **Atom** | Independent piece of state (Jotai, Recoil) |
| **Derived state** | State computed from other state |
| **Dispatch** | Send an action to the store |
| **Hydration** | Restoring state on client (SSR) |
| **Middleware** | Intercept actions for logging, async, etc. |
| **Observable** | Value that notifies when changed (MobX) |
| **Reducer** | Pure function: (state, action) → newState |
| **Selector** | Function to extract slice of state |
| **Store** | Container holding application state |
| **Thunk** | Action that returns a function (async) |

---

**Last Updated**: 2025-12-12
**Related Research**: 1.110 (Frontend Frameworks), 1.113 (UI Components)
