# Use Case: SaaS Real-Time Dashboard

## Scenario Definition

**Industry Examples**:
- Analytics platform (user behavior tracking)
- Business intelligence dashboards (sales metrics)
- System monitoring (server health, APM)
- Customer support platform (ticket queues)
- Marketing automation (campaign performance)
- E-commerce admin (order tracking, inventory)

**Core Requirement**: Push data updates to user dashboards in real-time, filtered by tenant/permissions, with acceptable latency for business decision-making.

## Requirement Analysis

### Scale Requirements

**Concurrent Connections**:
- Typical SaaS: 500-5,000 concurrent dashboard users
- Enterprise: 2,000-20,000 concurrent
- Peak load: 3x typical (during business hours, specific timezones)
- Per-tenant: 1-50 users per organization

**Message Patterns**:
- Per-user subscriptions (filtered data channels)
- Update frequency: 1-60 updates/minute per user
- Message size: 500 bytes - 5KB (dashboard widgets)
- Pattern: Database change → WebSocket push

**Geographic Distribution**:
- North America: 40-60% of users
- Europe: 25-35%
- Asia-Pacific: 10-20%
- Latency tolerance varies by region

### Performance Requirements

**Latency Targets**:
- **Desired**: <100ms (P95) for snappy UX
- **Acceptable**: <200ms (P95)
- **Maximum**: <500ms (P99) - still usable for dashboards
- **Tolerable**: 1-5 seconds for bulk data loads

**Consistency Model**:
- Eventual consistency (data can be 1-2 seconds stale)
- No ordering guarantees needed between different data types
- Idempotent updates (client can deduplicate)

**Uptime Requirements**:
- SLA: 99.9% (43 minutes downtime/month)
- Graceful degradation: Fall back to manual refresh
- No data loss (buffering acceptable)

### Cost Constraints

**SaaS Economics**:
- Subscription: $50-500/month per organization
- WebSocket cost target: <10% of subscription revenue
- Per-user cost: $0.50-5.00/month acceptable
- Infrastructure: $500-5,000/month at 5,000 concurrent users

**Optimization Priority**:
- Predictable monthly costs (not spiky)
- Cost scales linearly with revenue
- Avoid operational overhead (small team)

### Technical Constraints

**Database Integration**:
- Primary database: PostgreSQL, MySQL, or MongoDB
- Change Data Capture (CDC) requirements
- Query result caching (Redis)
- Multi-tenancy isolation

**Backend Stack**:
- REST API: Node.js, Python (Django/Flask), Ruby on Rails
- Authentication: JWT or session-based
- Authorization: Row-level security, tenant filtering

**Client Environment**:
- 90% desktop web (Chrome, Firefox, Safari)
- 10% mobile (responsive web, not native)
- Modern browsers only (WebSocket support guaranteed)

## Solution Evaluation

### Option 1: Supabase Realtime (Backend-Integrated)

**Architecture**:
- PostgreSQL + Realtime server (Elixir-based)
- Database change streams via logical replication
- Row-level security enforced at DB level
- Client subscribes to specific table/column filters

**Latency Analysis**:

Typical Case (database change → client):
- PostgreSQL WAL replication: 10-50ms
- Supabase Realtime processing: 20-50ms
- WebSocket delivery: 30-100ms
- **Total: 60-200ms (MEETS <200ms target)**

Best Case (same region):
- **Total: 60-120ms**

Worst Case (cross-region):
- **Total: 150-300ms (MARGINAL for <500ms)**

**Cost Modeling**:

Pricing: Database size + realtime connections

500 users:
- Pro plan: $25/month (500 realtime connections included)
- Database: 8GB included
- **Total: $25/month = $0.05/user**

5,000 users:
- Team plan: $599/month (5,000 connections)
- Database: 100GB included
- **Total: $599/month = $0.12/user**

20,000 users:
- Enterprise: Custom ($2,000-5,000/month estimate)

**Pros**:
- Integrated solution (DB + auth + realtime)
- Automatic tenant filtering (row-level security)
- PostgreSQL familiarity
- Zero separate infrastructure
- Excellent developer experience

**Cons**:
- Locked to PostgreSQL (migration difficult)
- Latency higher than pure WebSocket (DB overhead)
- Scaling limits at high connection counts
- Newer technology (less production validation)

**Verdict**: **Best for PostgreSQL-based SaaS, acceptable latency**

---

### Option 2: Ably (Managed WebSocket) + Manual DB Integration

**Architecture**:
- Ably for WebSocket connections
- Backend publishes to Ably on DB changes
- Custom change detection (DB triggers or application-level)
- Channel-based tenant isolation

**Latency Analysis**:

Typical Case (DB change → client):
- Application detects change: 10-100ms (depends on mechanism)
- Publish to Ably API: 20-50ms
- Ably fan-out: 30-60ms
- **Total: 60-210ms (MEETS <200ms)**

Best Case (optimized change detection):
- **Total: 60-110ms**

**Cost Modeling**:

Pricing: Connection-minutes + messages

500 users, 8 hours/day active:
- 500 connections × 480 min/day × 22 days = 5.28M connection-minutes
- Messages: 500 users × 10 msg/min × 480 min = 2.4M messages/day
- Ably Standard: $150/month base + overages
- **Total: $150-300/month = $0.30-0.60/user**

5,000 users:
- 52.8M connection-minutes/month
- Ably Pro: $750/month
- **Total: $750-1,200/month = $0.15-0.24/user**

**Pros**:
- Database-agnostic (works with any backend)
- Very low latency (60-110ms best case)
- Global edge network (multi-region automatic)
- Professional support + SLA (99.999%)

**Cons**:
- Requires custom change detection logic
- Higher cost than Supabase at small scale
- Operational complexity (DB → Ably integration)
- No built-in authorization (must implement)

**Verdict**: **Best for non-PostgreSQL backends, multi-region requirement**

---

### Option 3: Socket.IO (Self-Hosted) + Redis Pub/Sub

**Architecture**:
- Socket.IO servers (Node.js)
- Redis as pub/sub backplane
- Application publishes changes to Redis
- Socket.IO broadcasts to connected clients

**Latency Analysis**:

Typical Case:
- App publishes to Redis: 5-15ms
- Redis pub/sub: 1-5ms
- Socket.IO fan-out: 20-50ms
- WebSocket delivery: 30-100ms
- **Total: 56-170ms (MEETS <200ms)**

Best Case:
- **Total: 56-100ms**

**Cost Modeling**:

Infrastructure (5,000 connections):
- 3x c5.large Socket.IO servers ($180/month)
- Redis cluster ($50/month)
- Load balancer ($20/month)
- **Infrastructure: $250/month**

Operations:
- Setup: 30 hours ($600-1,500 one-time)
- Maintenance: 10 hours/month ($200-500)
- **Total: $450-750/month = $0.09-0.15/user**

**Pros**:
- Full control over infrastructure
- Low cost at scale ($0.09-0.15/user)
- Node.js ecosystem familiarity
- Automatic fallback (WebSocket → polling)

**Cons**:
- Operational overhead (DevOps required)
- No built-in multi-region
- Custom change detection needed
- Setup complexity (2-4 weeks)

**Verdict**: **Best for cost optimization with DevOps capacity**

---

### Option 4: Pusher Channels (Managed WebSocket)

**Architecture**:
- Pusher managed infrastructure
- Backend publishes via Pusher HTTP API
- Client subscribes to private channels (per tenant)
- Built-in authentication (signature validation)

**Latency Analysis**:

Typical Case:
- App publishes to Pusher: 30-80ms
- Pusher processing: 40-80ms
- Fan-out: 50-100ms
- **Total: 120-260ms (MARGINAL for <200ms)**

**Cost Modeling**:

500 users:
- Business plan: $299/month (unlimited messages, 500 connections)
- **Total: $299/month = $0.60/user**

5,000 users:
- Enterprise: ~$1,500/month (estimate)
- **Total: $1,500/month = $0.30/user**

**Pros**:
- Easiest setup (1-day integration)
- Great documentation
- Built-in private channels (authentication)
- Generous message limits

**Cons**:
- Higher latency than Ably (120-260ms)
- More expensive at scale
- Limited customization
- Less transparent pricing at enterprise scale

**Verdict**: **Only for rapid MVP, migrate to Ably/Supabase for production**

---

### Option 5: Firebase Realtime Database

**Architecture**:
- Firebase Realtime Database (NoSQL JSON tree)
- Client subscribes to specific database paths
- Automatic synchronization
- Built-in offline support

**Latency Analysis**:

Typical Case:
- Database write: 50-100ms
- Firebase sync: 50-150ms
- **Total: 100-250ms (MARGINAL)**

**Cost Modeling**:

500 users:
- 500 × 100KB storage × $5/GB = $0.25
- 500 × 10GB downloads/month × $1/GB = $50
- **Total: ~$50-100/month**

5,000 users:
- **Total: ~$500-1,000/month**

**Pros**:
- Excellent offline support
- Mobile-first design
- Automatic scaling
- NoSQL flexibility

**Cons**:
- Highest latency (100-250ms)
- Poor fit for relational data
- Vendor lock-in (Google)
- Not designed for dashboard use case

**Verdict**: **Not recommended for SaaS dashboards**

---

## Database Integration Patterns

### Pattern 1: PostgreSQL Logical Replication (Supabase)

**Mechanism**:
- PostgreSQL WAL (Write-Ahead Log) streaming
- Supabase Realtime server decodes WAL
- Filters by row-level security policies
- Pushes to subscribed clients

**Implementation**:
```sql
-- Client subscription (JavaScript)
supabase
  .from('orders')
  .on('*', payload => updateDashboard(payload))
  .filter('tenant_id', 'eq', currentUser.tenantId)
  .subscribe()
```

**Latency**: 60-200ms (DB write to client)

**Pros**: Zero application code, automatic filtering

**Cons**: PostgreSQL-only, scaling limits

---

### Pattern 2: Application-Level Change Detection

**Mechanism**:
- Application publishes to WebSocket service after DB write
- Manual channel/tenant filtering in app code
- Explicit control over what data is pushed

**Implementation**:
```javascript
// After database update
await db.query('UPDATE orders SET status = $1 WHERE id = $2', ['shipped', orderId])
await ably.channels.get(`tenant:${tenantId}:orders`).publish('update', orderData)
```

**Latency**: 60-150ms (depends on app efficiency)

**Pros**: Database-agnostic, full control

**Cons**: Manual implementation, potential for bugs

---

### Pattern 3: Database Triggers + Message Queue

**Mechanism**:
- PostgreSQL trigger writes to NOTIFY or external queue
- Background worker listens to queue
- Worker publishes to WebSocket service

**Implementation**:
```sql
-- PostgreSQL trigger
CREATE TRIGGER order_update_trigger
AFTER UPDATE ON orders
FOR EACH ROW
EXECUTE FUNCTION pg_notify('order_updates', row_to_json(NEW)::text);
```

**Latency**: 100-300ms (additional queue hop)

**Pros**: Decoupled from application logic

**Cons**: Higher latency, operational complexity

---

### Pattern 4: Change Data Capture (CDC) with Debezium

**Mechanism**:
- Debezium reads database transaction logs
- Publishes to Kafka/Redis Streams
- WebSocket server consumes stream
- Pushes to clients

**Latency**: 150-500ms (multiple hops)

**Pros**: Database-agnostic, event sourcing benefits

**Cons**: Complex infrastructure, overkill for simple dashboards

**Verdict**: Only for large-scale enterprise (>50K users)

---

## Multi-Tenancy & Authorization

### Challenge: Preventing Cross-Tenant Data Leaks

**Requirement**: User from Tenant A cannot receive data from Tenant B

### Approach 1: Database Row-Level Security (Supabase)

**Implementation**:
```sql
-- PostgreSQL RLS policy
CREATE POLICY tenant_isolation ON orders
FOR SELECT
USING (tenant_id = current_setting('app.current_tenant')::uuid);
```

**Security**: Enforced at database level (highest security)

**Performance**: No application-level filtering needed

---

### Approach 2: Application-Level Channel Filtering

**Implementation**:
```javascript
// Client subscribes to tenant-specific channel
const channel = ably.channels.get(`tenant:${tenantId}:orders`)

// Server validates tenant access before subscription
socket.on('subscribe', async (channelName) => {
  const tenantId = extractTenantId(channelName)
  if (!await userHasAccessToTenant(socket.user, tenantId)) {
    throw new Error('Unauthorized')
  }
  socket.join(channelName)
})
```

**Security**: Application must implement correctly (risk of bugs)

**Performance**: Flexible, can optimize per use case

---

### Approach 3: JWT Token Claims

**Implementation**:
```javascript
// JWT contains tenant_id claim
const token = jwt.sign({ userId, tenantId, permissions }, secret)

// Ably validates token before connection
const ably = new Ably.Realtime({
  authUrl: '/api/ably-token',
  authHeaders: { Authorization: `Bearer ${jwtToken}` }
})
```

**Security**: Strong if JWT validation is correct

**Performance**: Token validation adds 10-30ms latency

---

## Fallback Strategies

### Strategy 1: Manual Refresh Button

**Implementation**:
- Button: "Refresh" in dashboard UI
- On WebSocket failure, show indicator
- User clicks to trigger fresh API fetch

**UX Impact**: Minimal (users expect dashboards can refresh)

**Cost**: Free (standard REST API)

---

### Strategy 2: Automatic Polling Fallback

**Implementation**:
```javascript
let websocketConnected = false

websocket.on('connect', () => websocketConnected = true)
websocket.on('disconnect', () => {
  websocketConnected = false
  startPollingFallback() // Poll every 30 seconds
})

function startPollingFallback() {
  setInterval(async () => {
    if (!websocketConnected) {
      const data = await fetch('/api/dashboard-data')
      updateDashboard(data)
    }
  }, 30000)
}
```

**Latency**: 15 seconds average (30-second polling)

**Cost**: Minimal (1-2 requests/minute per disconnected user)

---

### Strategy 3: Service Worker Background Sync

**Implementation**:
- Service worker maintains state cache
- Background sync every 60 seconds
- Offline-first approach

**Browser Support**: Modern browsers only

**Complexity**: High (service worker debugging)

---

## Migration from Polling

### Current State: Frontend Polls Every 10 Seconds

**Problems**:
- Server load: 5,000 users × 6 requests/min = 30K req/min
- Database load: 30K queries/minute (even if no changes)
- Latency: 5-second average staleness
- User experience: Visible "flash" on updates

### Migration Strategy

**Phase 1: Add WebSocket Alongside Polling (2 weeks)**

Week 1: Infrastructure
- Deploy Supabase/Ably/Socket.IO infrastructure
- Configure database change detection
- Set up monitoring (latency, connection count)

Week 2: Client Integration
- Add WebSocket library to frontend
- Feature flag: 10% of users get WebSocket
- Keep polling as backup (reduce to 60-second interval)

**Phase 2: Gradual Rollout (2-4 weeks)**

Week 3: Expand to 50% of users
- Monitor error rates, latency distribution
- Tune connection handling (reconnect logic)

Week 4: Expand to 100% of users
- Polling now only backup (5-minute interval)
- Monitor cost (connection minutes, messages)

**Phase 3: Polling Deprecation (2 weeks)**

Week 6: Disable polling for modern browsers
- Keep for IE11 or legacy (if required)
- Remove polling code in next major release

### Risk Mitigation

**Feature Flag Control**:
```javascript
if (featureFlags.websocket && supportsWebSocket) {
  initializeWebSocket()
} else {
  initializePolling() // existing code path
}
```

**Monitoring Dashboards**:
- WebSocket connection success rate (target: >98%)
- Average latency (target: <200ms P95)
- Message delivery rate (target: 100%)
- Cost per user (target: <$0.30/user/month)

**Rollback Plan**:
- Instant feature flag disable (back to polling)
- No database migrations required
- No breaking changes to API

---

## Recommendation

### Primary: Supabase Realtime (for PostgreSQL-based SaaS)

**Rationale**:
- Best integration with PostgreSQL (zero custom code)
- Automatic tenant filtering (row-level security)
- Cost-effective ($25-599/month for 500-5,000 users)
- Latency acceptable (60-200ms)
- Includes full backend stack

**When to Choose**:
- Using PostgreSQL as primary database
- Team size: <10 engineers (low operational overhead)
- Budget: $500-1,000/month acceptable
- Latency: <200ms acceptable

**Deal-breakers**:
- Non-PostgreSQL database (choose Ably)
- >10K concurrent users (scaling concerns)
- <100ms latency requirement (choose Socket.IO)

---

### Alternative 1: Ably (for non-PostgreSQL or multi-region)

**Rationale**:
- Database-agnostic (MySQL, MongoDB, any backend)
- Global edge network (multi-region automatic)
- Lower latency than Supabase (60-110ms)
- Professional SLA (99.999%)

**When to Choose**:
- Using MySQL, MongoDB, or other database
- Global user base (need multi-region)
- <100ms latency desired
- Budget: $750-1,500/month at 5K users

**Deal-breakers**:
- PostgreSQL already in use (Supabase better fit)
- Budget <$500/month (Supabase cheaper)

---

### Alternative 2: Socket.IO (for cost optimization at scale)

**Rationale**:
- Lowest cost at scale ($450-750/month for 5K users)
- Full infrastructure control
- Latency: 56-170ms (excellent)

**When to Choose**:
- DevOps capacity available (10 hours/month)
- >5K users (cost savings justify complexity)
- Node.js expertise on team

**Deal-breakers**:
- Small team (<5 engineers)
- No DevOps expertise
- Launch timeline <4 weeks

---

## Decision Matrix

| Requirement | Supabase | Ably | Socket.IO | Pusher |
|-------------|----------|------|-----------|--------|
| **PostgreSQL** | ✓ Perfect | ✓ Works | ✓ Works | ✓ Works |
| **MySQL/MongoDB** | ✗ No | ✓ Yes | ✓ Yes | ✓ Yes |
| **<200ms latency** | ✓ Yes (60-200ms) | ✓ Yes (60-110ms) | ✓ Yes (56-170ms) | Marginal (120-260ms) |
| **500 users** | ✓ $25/mo | ✗ $150/mo | ✗ $450/mo | ✗ $299/mo |
| **5K users** | ✓ $599/mo | ✓ $750/mo | ✓ $450-750/mo | ✗ $1.5K/mo |
| **Zero ops** | ✓ Yes | ✓ Yes | ✗ No | ✓ Yes |
| **Multi-region** | Limited | ✓ Yes | Manual | ✓ Yes |
| **Setup time** | 3-5 days | 3-5 days | 2-4 weeks | 1-2 days |

**The Bottom Line**: For PostgreSQL-based SaaS with <5K users, Supabase offers the best cost-to-value. For larger scale or non-PostgreSQL, choose Ably (managed) or Socket.IO (self-hosted with DevOps).
