# Use Case: Collaborative Document Editing

## Scenario Definition

**Industry Examples**:
- Collaborative text editor (Google Docs-style)
- Design/whiteboard tools (Figma, Miro)
- Code collaboration (CodeSandbox, Replit)
- Spreadsheet editing (Google Sheets)
- Presentation builders (Pitch, Gamma)
- Markdown/wiki editors (Notion, Confluence)

**Core Requirement**: Multiple users edit same document simultaneously with conflict-free merging, low latency for responsive UX, and session persistence across network interruptions.

## Requirement Analysis

### Scale Requirements

**Concurrent Editors per Document**:
- Typical: 2-10 simultaneous editors
- Maximum: 20-50 editors (design/whiteboard sessions)
- Edge case: 100+ viewers (presentation mode, read-only)
- Document count: 1,000-100,000 active documents

**Total Concurrent Connections**:
- Small SaaS: 500-2,000 connections (100-1,000 active documents)
- Medium SaaS: 5,000-20,000 connections
- Enterprise: 50,000-500,000 connections

**Message Patterns**:
- Operational Transform (OT) operations: 10-100 ops/minute per active editor
- Cursor position updates: 2-10/second during active typing
- Presence updates: 1-5/minute (user joins/leaves)
- Message size: 50-500 bytes per operation

**Session Duration**:
- Average: 15-45 minutes per editing session
- Long sessions: 2-8 hours (deep work)
- Idle time: 30-60 minutes (stepped away, document open)

### Performance Requirements

**Latency Targets**:
- **Critical**: <100ms (P95) for keystroke propagation (UX requirement)
- **Acceptable**: <200ms (P99)
- **Maximum**: <500ms before users notice lag
- **Cursor movement**: <50ms desired (visual feedback)

**Conflict Resolution**:
- **Algorithm**: Operational Transform (OT) or CRDT (Conflict-free Replicated Data Types)
- **Convergence**: All clients must reach identical state
- **Ordering**: Server-authoritative or distributed consensus
- **Complexity**: Document structure dependent (text vs rich formatting)

**Reliability**:
- **No data loss**: All operations must eventually apply
- **Eventual consistency**: 1-5 second delay acceptable
- **Offline support**: Buffer operations during disconnect
- **Recovery**: Resume session after network interruption

### Cost Constraints

**SaaS Pricing Model**:
- Typical: $10-50/user/month
- WebSocket cost target: <5% of revenue = $0.50-2.50/user/month
- Document storage separate from real-time costs

**Infrastructure Budget**:
- Startup: $200-1,000/month (500-2,000 connections)
- Growth stage: $1,000-5,000/month (5,000-20,000 connections)
- Enterprise: $5,000-20,000/month (50K+ connections)

### Technical Constraints

**Conflict Resolution Architecture**:
- **Server-authoritative**: Server applies operations in sequence (simpler)
- **Distributed**: Clients apply locally, sync later (faster UX, complex)
- **Hybrid**: Optimistic local apply + server validation

**Backend Stack**:
- Language: Node.js (most OT libraries), Go (performance), Elixir (concurrency)
- State storage: Redis (in-memory document state), PostgreSQL (persistence)
- History: Need 100-1,000 recent operations for late joiners

**Client Environment**:
- 70% desktop web (Chrome, Firefox, Safari)
- 20% mobile web (responsive)
- 10% native apps (Electron, mobile)

## Solution Evaluation

### Option 1: Socket.IO + ShareDB (Self-Hosted OT Framework)

**Architecture**:
- ShareDB: Operational Transform server (Node.js)
- MongoDB or PostgreSQL for document persistence
- Redis for real-time operation queue
- Socket.IO for WebSocket transport

**Latency Analysis**:

Best Case (same region, 2-5 editors):
- Client → server: 20-40ms
- ShareDB operation apply: 5-15ms
- Server → other clients: 20-40ms
- **Total: 45-95ms (MEETS <100ms target)**

Typical Case (10 editors, mixed network):
- Client → server: 30-80ms
- ShareDB processing: 10-30ms (more concurrent ops)
- Broadcast to 9 clients: 30-80ms
- **Total: 70-190ms (MEETS <200ms P99)**

Worst Case (50 editors, complex document):
- **Total: 150-400ms (MARGINAL)**

**Cost Modeling**:

Infrastructure (5,000 connections, ~500 active documents):
- 2x c5.large Node.js servers ($120/month)
- Redis cluster ($50/month)
- MongoDB Atlas or PostgreSQL ($30-100/month)
- Load balancer ($20/month)
- **Subtotal: $220-290/month**

Operations:
- Setup: 40-60 hours ($800-3,000 one-time, includes OT integration)
- Maintenance: 10-15 hours/month ($200-750)
- **Total: $420-1,040/month = $0.08-0.21/user**

**Pros**:
- Battle-tested OT implementation (used by production apps)
- Full control over conflict resolution logic
- Low cost at scale
- Open source (no vendor lock-in)

**Cons**:
- Complex setup (OT requires deep understanding)
- Operational overhead (monitoring document state)
- 40-60 hour initial integration
- No built-in offline sync (must implement)

**Verdict**: **Best for production collaborative editing, if DevOps capacity available**

---

### Option 2: Yjs + WebRTC (CRDT, Peer-to-Peer)

**Architecture**:
- Yjs: CRDT library (JavaScript)
- WebRTC for peer-to-peer sync (optional)
- WebSocket server for signaling + fallback
- Local-first architecture (offline by default)

**Latency Analysis**:

Best Case (P2P WebRTC connection):
- Direct peer connection: 10-30ms
- CRDT merge: 1-5ms
- **Total: 11-35ms (EXCEPTIONAL, <50ms)**

Fallback Case (via WebSocket server):
- Client → server: 20-40ms
- CRDT broadcast: 5-15ms
- Server → peers: 20-40ms
- **Total: 45-95ms (MEETS <100ms)**

**Cost Modeling**:

Infrastructure (5,000 connections):
- Lightweight signaling server: 1x c5.large ($60/month)
- TURN server for WebRTC relay: $50-100/month (for NAT traversal)
- Optional: Document sync server ($30-60/month)
- **Total: $140-220/month = $0.03-0.04/user**

Operations:
- Setup: 20-40 hours ($400-2,000)
- Maintenance: 5-10 hours/month ($100-500)
- **Total: $240-720/month**

**Pros**:
- Lowest latency (11-35ms P2P)
- Offline-first architecture (works without server)
- Lowest infrastructure cost
- CRDT eliminates complex OT logic

**Cons**:
- WebRTC unreliable (NAT, firewall issues)
- P2P not always possible (corporate networks)
- Newer technology (less production validation)
- Debugging difficult (distributed state)

**Verdict**: **Best for lowest latency, offline-first design**

---

### Option 3: Ably (Managed) + Custom OT Logic

**Architecture**:
- Ably for WebSocket transport + message ordering
- Custom OT/CRDT implementation in application
- Redis or backend database for document state
- Ably History for operation replay

**Latency Analysis**:

Typical Case:
- Client → Ably: 20-50ms
- Ably routing: 20-40ms
- Ably → other clients: 20-50ms
- **Total: 60-140ms (MEETS <200ms)**

Best Case (same region):
- **Total: 60-90ms (MEETS <100ms)**

**Cost Modeling**:

Pricing: Connection-minutes + message count

5,000 connections, 30-minute avg session:
- 5,000 × 30 min × 22 days/month = 3.3M connection-minutes
- 5,000 users × 50 ops/session × 22 days = 5.5M messages/month
- Ably Standard: $150/month base
- Overages: ~$50-100/month
- **Total: $200-300/month = $0.04-0.06/user**

20,000 connections:
- **Total: $750-1,200/month = $0.04-0.06/user**

**Pros**:
- Zero infrastructure operations
- Message ordering guaranteed (critical for OT)
- Built-in message history (operation replay)
- Global edge network

**Cons**:
- Must implement OT/CRDT yourself (complex)
- No document state management (build separately)
- Higher cost than Socket.IO at small scale
- Vendor lock-in for transport layer

**Verdict**: **Best for global users, managed infrastructure, if willing to build OT logic**

---

### Option 4: Firepad (Firebase + Operational Transform)

**Architecture**:
- Firebase Realtime Database for document storage
- Firepad library (open source, built on Firebase)
- Operational Transform built-in
- Automatic offline sync

**Latency Analysis**:

Typical Case:
- Client → Firebase: 50-100ms
- Firebase processing: 30-80ms
- Firebase → other clients: 50-100ms
- **Total: 130-280ms (FAILS <200ms P99)**

Best Case:
- **Total: 130-180ms (MARGINAL)**

**Cost Modeling**:

Pricing: Database operations + bandwidth

5,000 connections, 50 operations/session:
- Database writes: 5,000 × 50 × 22 = 5.5M writes/month
- Database reads: 5.5M × 5 (fan-out) = 27.5M reads/month
- Firebase Blaze (pay-as-you-go): ~$0.10/100K operations
- **Total: ~$330/month = $0.07/user**

**Pros**:
- Complete solution (OT + transport + storage)
- Offline sync built-in
- Easy integration (Firepad library)
- Automatic scaling

**Cons**:
- Highest latency (130-280ms)
- Vendor lock-in (Google)
- Limited customization
- Firepad maintenance uncertain (community project)

**Verdict**: **Not recommended (latency too high, maintenance concerns)**

---

### Option 5: Automerge (CRDT) + Custom Sync Server

**Architecture**:
- Automerge: Pure CRDT library (JSON document merging)
- Custom WebSocket server (Node.js or Go)
- Document sync via network protocol
- Optional: S3 for document snapshots

**Latency Analysis**:

Typical Case:
- Client → server: 20-40ms
- Automerge CRDT merge: 5-20ms
- Server → clients: 20-40ms
- **Total: 45-100ms (MEETS <100ms)**

Large Document (10MB+):
- CRDT merge can be 50-200ms (complex)
- **Total: 90-280ms (MARGINAL)**

**Cost Modeling**:

Infrastructure (5,000 connections):
- 2x c5.large servers ($120/month)
- S3 storage: $10-30/month
- Redis (optional): $30-50/month
- **Total: $160-200/month = $0.03-0.04/user**

Operations:
- Setup: 60-80 hours ($1,200-4,000) - building custom protocol
- Maintenance: 15-20 hours/month ($300-1,000)
- **Total: $460-1,200/month**

**Pros**:
- CRDT eliminates OT complexity
- Offline-first architecture
- Full control over protocol
- Low infrastructure cost

**Cons**:
- No standard sync protocol (must build)
- Large documents can be slow (CRDT overhead)
- Significant engineering investment
- Less production validation than ShareDB

**Verdict**: **Best for advanced teams building highly custom solutions**

---

## Operational Transform vs CRDT Trade-offs

### Operational Transform (OT)

**How it Works**:
- Client sends operation (e.g., "insert 'h' at position 5")
- Server transforms operation against concurrent operations
- Server broadcasts transformed operation to clients
- Clients apply transformed operation

**Example**: ShareDB, Firepad

**Pros**:
- Smaller message size (send operations, not state)
- Server-authoritative (easier to reason about)
- Proven in production (Google Docs uses OT)

**Cons**:
- Complex transformation functions (bug-prone)
- Server must maintain operation history
- Difficult to scale (server bottleneck)

**Best For**: Text editing, server-authoritative architecture

---

### Conflict-free Replicated Data Types (CRDT)

**How it Works**:
- Each client maintains full document state
- Clients merge states using mathematical properties
- Convergence guaranteed (no conflicts)
- Server optional (can be peer-to-peer)

**Example**: Yjs, Automerge

**Pros**:
- No conflict resolution logic needed
- Offline-first by design
- Peer-to-peer possible
- Simpler reasoning (no transform functions)

**Cons**:
- Larger message size (send state deltas)
- Slower with large documents (merge overhead)
- Newer technology (less production validation)

**Best For**: Offline-first apps, complex data structures (not just text)

---

## Offline Support Strategies

### Strategy 1: Operation Queueing (OT/CRDT)

**Implementation**:
- Buffer all user operations locally during disconnect
- On reconnect, replay operations to server
- Server validates and broadcasts

**Data Loss Risk**: Low (operations persisted in IndexedDB)

**UX**: Optimistic (user sees changes immediately)

**Complexity**: Medium (queue management, deduplication)

---

### Strategy 2: Full Document Sync on Reconnect

**Implementation**:
- On disconnect, freeze editing
- On reconnect, fetch latest document state
- Discard local changes (or show conflict UI)

**Data Loss Risk**: High (user loses offline work)

**UX**: Poor (frustrating for users)

**Complexity**: Low (simple implementation)

**Only Use For**: Read-heavy documents, non-critical edits

---

### Strategy 3: CRDT Automatic Merge

**Implementation**:
- CRDT continues working offline
- On reconnect, sync CRDT state
- Automatic merge (no conflicts)

**Data Loss Risk**: None (CRDT guarantees convergence)

**UX**: Best (seamless offline/online transition)

**Complexity**: High (CRDT implementation)

---

## Session Recovery & Late Joiners

### Challenge 1: User Joins Document with 1,000 Existing Operations

**Problem**: New user needs document state, not full history

**Solution 1**: Snapshot + Recent Operations
- Server maintains snapshots every 100 operations
- Send snapshot + operations since snapshot
- Client applies operations to reach current state

**Cost**: 1-2 seconds load time, acceptable

---

**Solution 2**: Full State Sync (CRDT)
- Send entire CRDT state to new user
- User merges with empty state (becomes current)

**Cost**: Depends on document size (10KB-1MB typical)

---

### Challenge 2: User Disconnects for 5 Minutes

**Problem**: 100+ operations occurred during disconnect

**Solution**: Replay Operations from Timestamp
- Client sends "last seen operation ID"
- Server sends all operations since that ID
- Client applies operations in order

**Risk**: Operation history must be retained (Redis or DB)

---

## Cursor Position & Presence

### Real-Time Cursor Sharing

**Requirements**:
- <50ms latency desired (visual feedback)
- High frequency: 2-10 updates/second per user
- Not critical (can drop messages)

**Implementation**:
```javascript
// Throttle cursor updates to 100ms
let lastCursorUpdate = 0
editor.on('cursorMove', (position) => {
  const now = Date.now()
  if (now - lastCursorUpdate > 100) {
    socket.emit('cursor', { position, userId })
    lastCursorUpdate = now
  }
})

// Receive cursor updates (don't apply all, only latest)
socket.on('cursor', ({ position, userId }) => {
  updateCursorUI(userId, position)
})
```

**Bandwidth**: 10 users × 10 updates/sec × 50 bytes = 5KB/sec (minimal)

---

### Presence (Join/Leave)

**Requirements**:
- 1-5 second latency acceptable
- Low frequency: On join, leave, idle

**Implementation**:
```javascript
// Join
socket.emit('join', { userId, userName, color })

// Heartbeat every 30 seconds
setInterval(() => socket.emit('heartbeat'), 30000)

// Server marks user offline after 60 seconds no heartbeat
```

---

## Migration Path (Greenfield vs Retrofit)

### Scenario 1: Greenfield (New Collaborative Feature)

**Recommended Approach**: Yjs (CRDT) + WebSocket

**Timeline**: 4-8 weeks
- Week 1-2: Yjs integration, basic text editing
- Week 3-4: Offline support, cursor sharing
- Week 5-6: Presence, user avatars
- Week 7-8: Testing, performance optimization

**Cost**: $240-720/month ongoing

---

### Scenario 2: Retrofit Existing Editor

**Recommended Approach**: Socket.IO + ShareDB (OT)

**Timeline**: 8-12 weeks
- Week 1-3: ShareDB integration, document model mapping
- Week 4-6: Conflict resolution testing
- Week 7-9: Migration of existing documents
- Week 10-12: Rollout, monitoring

**Cost**: $420-1,040/month ongoing

**Complexity**: High (must map existing data model to OT operations)

---

## Recommendation

### Primary: Socket.IO + ShareDB (for production-grade collaboration)

**Rationale**:
- Proven OT implementation (battle-tested)
- 45-95ms latency (MEETS <100ms requirement)
- Cost-effective ($0.08-0.21/user/month)
- Full control over document state

**When to Choose**:
- Building production collaborative editor
- Need server-authoritative conflict resolution
- Team has DevOps capacity (10-15 hours/month)
- Budget: $500-1,500/month at 5K users

**Deal-breakers**:
- No DevOps expertise (choose Ably + custom OT)
- Offline-first requirement (choose Yjs)
- <4 week timeline (choose Ably + simpler sync)

---

### Alternative 1: Yjs (for offline-first, peer-to-peer)

**Rationale**:
- Lowest latency (11-35ms P2P, 45-95ms via server)
- Offline-first architecture (best UX)
- CRDT simplicity (no OT complexity)
- Lowest cost ($240-720/month)

**When to Choose**:
- Offline support critical
- Advanced engineering team (CRDT experience)
- <100ms latency requirement
- Want peer-to-peer option

**Deal-breakers**:
- Server-authoritative requirement (OT better)
- Large documents (>10MB, CRDT slow)
- Need proven production validation (Yjs newer)

---

### Alternative 2: Ably + Custom OT (for managed, global)

**Rationale**:
- Zero infrastructure operations
- Global edge network (multi-region automatic)
- Message ordering guarantees (critical for OT)
- 60-140ms latency (acceptable)

**When to Choose**:
- Global user base (need multi-region)
- Small team (<5 engineers, no DevOps)
- Willing to build OT logic
- Budget: $750-1,200/month at 20K users

**Deal-breakers**:
- Budget <$500/month (Socket.IO cheaper)
- Need complete OT solution (ShareDB better)

---

## Decision Matrix

| Requirement | ShareDB | Yjs | Ably + OT | Firepad |
|-------------|---------|-----|-----------|---------|
| **<100ms latency** | ✓ Yes (45-95ms) | ✓ Excellent (11-95ms) | ✓ Yes (60-90ms) | ✗ No (130-180ms) |
| **Offline support** | Manual (complex) | ✓ Built-in | Manual | ✓ Built-in |
| **OT built-in** | ✓ Yes | N/A (CRDT) | ✗ No (build yourself) | ✓ Yes |
| **5K users** | ✓ $420-1,040/mo | ✓ $240-720/mo | ✓ $200-300/mo | ✓ $330/mo |
| **20K users** | ✓ $600-1,500/mo | ✓ $400-1,000/mo | ✓ $750-1,200/mo | ✓ $1,320/mo |
| **Zero ops** | ✗ No | ✗ No | ✓ Yes | ✓ Yes |
| **Setup time** | 8-12 weeks | 4-8 weeks | 4-8 weeks | 2-4 weeks |
| **Production validation** | ✓ High | Medium | Medium | Low (maintenance?) |

**The Bottom Line**: For production collaborative editing, ShareDB (OT) is the safest choice. For offline-first or lowest latency, Yjs (CRDT) is optimal. Avoid Firepad due to latency and maintenance concerns.
