# MobX

> "Simple, scalable state management"

## Quick Facts

| Metric | Value |
|--------|-------|
| GitHub Stars | 28,103 |
| npm Weekly Downloads | 2.3M |
| Bundle Size | ~16KB |
| License | MIT |
| Current Version | 6.15.0 |
| Paradigm | Reactive/Observable |

## Core Philosophy

MobX is fundamentally different from Redux-style libraries. It uses **reactive programming** with observables:

- **Redux/Zustand**: Actions → Reducers → State → View
- **MobX**: Observables → Reactions → View (automatic)

"MobX is a signal based, battle-tested library that makes state management simple and scalable by transparently applying functional reactive programming."

## Basic Usage

### Class-based (Traditional)
```javascript
import { makeAutoObservable } from 'mobx'
import { observer } from 'mobx-react-lite'

class TodoStore {
  todos = []
  filter = 'all'

  constructor() {
    makeAutoObservable(this)
  }

  get filteredTodos() {
    if (this.filter === 'all') return this.todos
    return this.todos.filter(t => t.completed === (this.filter === 'completed'))
  }

  addTodo(text) {
    this.todos.push({ text, completed: false })
  }

  toggleTodo(index) {
    this.todos[index].completed = !this.todos[index].completed
  }
}

const todoStore = new TodoStore()

// Observer component - auto-rerenders on observable changes
const TodoList = observer(() => (
  <ul>
    {todoStore.filteredTodos.map((todo, i) => (
      <li
        key={i}
        onClick={() => todoStore.toggleTodo(i)}
        style={{ textDecoration: todo.completed ? 'line-through' : 'none' }}
      >
        {todo.text}
      </li>
    ))}
  </ul>
))
```

### Functional Style
```javascript
import { makeAutoObservable } from 'mobx'

function createTodoStore() {
  return makeAutoObservable({
    todos: [],
    filter: 'all',
    get filteredTodos() {
      // computed automatically
      return this.filter === 'all'
        ? this.todos
        : this.todos.filter(t => t.completed === (this.filter === 'completed'))
    },
    addTodo(text) {
      this.todos.push({ text, completed: false })
    },
  })
}

const store = createTodoStore()
```

## Key Features

### Automatic Tracking
```javascript
// MobX automatically tracks which observables are used
const TodoCount = observer(() => {
  // Only re-renders when todos.length changes
  return <span>{todoStore.todos.length} todos</span>
})
```

### Computed Values
```javascript
class Store {
  price = 100
  quantity = 2

  constructor() {
    makeAutoObservable(this)
  }

  // Automatically cached and updated
  get total() {
    return this.price * this.quantity
  }
}
```

### Reactions (Side Effects)
```javascript
import { reaction, autorun } from 'mobx'

// Run whenever observable changes
autorun(() => {
  console.log('Todos count:', store.todos.length)
})

// Run when specific data changes
reaction(
  () => store.todos.length,
  (length) => {
    console.log('Length changed to:', length)
    localStorage.setItem('todoCount', length)
  }
)
```

### Async Actions
```javascript
class UserStore {
  user = null
  loading = false

  constructor() {
    makeAutoObservable(this)
  }

  async fetchUser(id) {
    this.loading = true
    try {
      this.user = await api.getUser(id)
    } finally {
      this.loading = false
    }
  }
}
```

## MobX-State-Tree (MST)

For larger applications, MST adds structure on top of MobX:

```javascript
import { types } from 'mobx-state-tree'

const Todo = types.model({
  text: types.string,
  completed: false,
})

const TodoStore = types
  .model({
    todos: types.array(Todo),
  })
  .actions((self) => ({
    addTodo(text) {
      self.todos.push({ text })
    },
  }))
```

MST provides:
- Runtime type checking
- Snapshots and time travel
- Middleware support
- Better DevTools

## Comparison with Alternatives

| Aspect | MobX | Redux Toolkit | Zustand |
|--------|------|---------------|---------|
| Paradigm | Reactive | Flux | Flux-like |
| Boilerplate | Minimal | Medium | Minimal |
| Learning curve | Different paradigm | Familiar | Easy |
| Re-renders | Automatic | Manual selectors | Manual selectors |
| Async | Native | Thunks/RTK Query | Native |
| DevTools | Good | Excellent | Good |

## When to Choose MobX

**Choose MobX when:**
- Team prefers reactive/observable patterns
- Want automatic dependency tracking
- Coming from MVVM frameworks (Angular, Vue)
- Building apps with complex derived state
- Prefer class-based architecture

**Consider alternatives when:**
- Team prefers explicit state updates → Redux/Zustand
- Need smallest bundle → Zustand (3KB vs 16KB)
- Want simpler mental model → Zustand
- Need atomic state → Jotai

## Resources

- [Official Docs](https://mobx.js.org/)
- [GitHub](https://github.com/mobxjs/mobx)
- [MobX-State-Tree](https://mobx-state-tree.js.org/)
- [mobx-react-lite](https://github.com/mobxjs/mobx/tree/main/packages/mobx-react-lite)
