# Use Case: Real-Time Collaborative Applications

**Last Updated**: 2026-01-16
**Complexity**: High
**Target**: Collaborative editors, multiplayer tools, live dashboards

## Scenario

Building a collaborative whiteboard/document editor with:
- Multiple users editing simultaneously
- Live cursors (show other users' positions)
- WebSocket sync (bidirectional updates)
- Optimistic updates with conflict resolution
- Presence indicators (who's online)
- High-frequency state updates (50-200/sec)

## Top Recommendations

### 1. Valtio (Best for Real-Time)

**Why**: Mutable API perfect for rapid WebSocket updates

```typescript
import { proxy, useSnapshot } from 'valtio'

const documentState = proxy({
  content: '',
  cursors: new Map(), // userId -> { x, y }
  users: new Map(),   // userId -> { name, color }
})

// WebSocket handler
ws.onmessage = (event) => {
  const update = JSON.parse(event.data)

  // Direct mutation (Valtio tracks it)
  if (update.type === 'cursor') {
    documentState.cursors.set(update.userId, update.position)
  }

  if (update.type === 'content') {
    documentState.content = update.content
  }
}

// Component
function CollaborativeEditor() {
  const snap = useSnapshot(documentState)

  return (
    <>
      <Editor content={snap.content} />
      {Array.from(snap.cursors).map(([userId, pos]) => (
        <Cursor key={userId} position={pos} color={snap.users.get(userId).color} />
      ))}
    </>
  )
}
```

**Pros**: Fast mutations, efficient for high-frequency updates
**Bundle**: 3.5KB

### 2. Jotai (Alternative)

```typescript
const documentAtom = atom({ content: '' })
const cursorsAtom = atom(new Map())
const usersAtom = atom(new Map())

// WebSocket integration with atom updates
const syncAtom = atom(null, (get, set, update) => {
  if (update.type === 'cursor') {
    const cursors = new Map(get(cursorsAtom))
    cursors.set(update.userId, update.position)
    set(cursorsAtom, cursors)
  }
})
```

**Pros**: Fine-grained subscriptions, good for complex derived state
**Cons**: Requires immutable updates (more overhead than Valtio)

## Recommendation

**Primary: Valtio**

- Mutable API matches real-time update patterns
- Efficient proxy tracking for rapid changes
- Clean WebSocket integration

**Alternative**: Preact Signals (if need zero re-renders)

**Last Updated**: 2026-01-16
