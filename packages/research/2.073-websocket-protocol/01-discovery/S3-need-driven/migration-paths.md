# WebSocket Migration Paths

## Overview

This document maps realistic migration scenarios between different real-time communication approaches, including cost analysis, timeline estimates, and risk mitigation strategies.

## Migration Scenarios

1. **Polling → WebSocket**: Most common (reducing server load, improving latency)
2. **WebSocket Self-Hosted → Managed Service**: Reducing operational overhead
3. **Managed Service → Self-Hosted**: Cost optimization at scale
4. **Provider A → Provider B**: Vendor change, feature requirements, pricing changes

## Migration 1: HTTP Polling → WebSocket

### When to Migrate

**Migrate when**:
- Polling interval <10 seconds (server inefficiency)
- User count >1,000 (connection overhead significant)
- Latency requirement <5 seconds (user experience)
- Server costs >$500/month on polling alone

**Don't migrate when**:
- Polling interval >60 seconds (WebSocket overkill)
- User count <100 (cost not justified)
- Updates infrequent (<1/minute per user)
- Team lacks WebSocket expertise (learning curve not justified)

### Current State Analysis

**Typical Polling Setup**:
```javascript
// Client polls every 5 seconds
setInterval(async () => {
  const data = await fetch('/api/updates')
  updateUI(data)
}, 5000)
```

**Problems**:
- Server load: N users × (3600/interval) requests/hour
- Database load: Query on every request (even if no changes)
- Latency: Average (interval/2) staleness
- Inefficiency: 95%+ requests return "no changes"

**Example**: 5,000 users, 5-second polling
- Requests: 5,000 × 720 = 3.6M requests/hour
- Database queries: 3.6M queries/hour
- Server cost: $500-2,000/month (depending on backend)

### Migration Strategy

**Phase 1: Infrastructure Setup (Week 1-2)**

Deploy WebSocket infrastructure alongside existing polling:

**Option A: Managed Service (Pusher/Ably)**
```javascript
// Add Pusher SDK
npm install pusher-js

// Initialize
const pusher = new Pusher('app-key', { cluster: 'us2' })
const channel = pusher.subscribe('updates')
channel.bind('new-data', data => updateUI(data))
```

**Setup time**: 1-2 days
**Cost**: $0-299/month (depends on scale)

**Option B: Self-Hosted (Socket.IO)**
```javascript
// Server setup
npm install socket.io redis
const io = require('socket.io')(server)
const redisAdapter = require('socket.io-redis')
io.adapter(redisAdapter({ host: 'localhost', port: 6379 }))

// Client
npm install socket.io-client
const socket = io('wss://your-domain.com')
socket.on('update', data => updateUI(data))
```

**Setup time**: 1-2 weeks
**Cost**: $200-500/month (infrastructure)

---

**Phase 2: Hybrid Implementation (Week 2-4)**

Run WebSocket and polling simultaneously:

```javascript
// Feature flag determines connection type
const useWebSocket = featureFlags.enabled('websocket') &&
                      typeof WebSocket !== 'undefined'

if (useWebSocket) {
  initializeWebSocket()
} else {
  initializePolling() // Existing code
}

function initializeWebSocket() {
  const socket = io('wss://api.example.com')

  socket.on('connect', () => {
    console.log('WebSocket connected, stopping polling')
    stopPolling()
  })

  socket.on('disconnect', () => {
    console.log('WebSocket disconnected, falling back to polling')
    startPollingFallback()
  })

  socket.on('update', data => updateUI(data))
}

function startPollingFallback() {
  // Reduced frequency (30s instead of 5s)
  pollingInterval = setInterval(fetchUpdates, 30000)
}
```

**Rollout**:
- Week 2: 10% of users on WebSocket
- Week 3: 50% of users
- Week 4: 100% of users

**Monitoring**:
- WebSocket connection success rate (target: >95%)
- Average latency improvement (expect 50-90% reduction)
- Server cost reduction (expect 30-70% decrease)
- Error rates (watch for WebSocket failures)

---

**Phase 3: Polling Reduction (Week 5-6)**

Keep polling only as fallback:

```javascript
// Polling now only for WebSocket failures
if (websocketConnected) {
  // No polling
} else {
  // Poll every 30-60 seconds (was 5 seconds)
  setInterval(fetchUpdates, 30000)
}
```

**Server-side optimization**:
- Reduce database polling (publish on change instead)
- Implement pub/sub pattern
- Cache frequently accessed data

---

**Phase 4: Complete Migration (Week 7-8)**

Remove polling entirely (optional):

```javascript
// Remove polling code
// WebSocket only (with reconnection logic)

socket.on('disconnect', () => {
  // Show UI indicator
  showOfflineBanner('Connection lost, reconnecting...')

  // Automatic reconnection (Socket.IO built-in)
  // On reconnect, fetch latest state
  socket.on('connect', async () => {
    const latestData = await fetch('/api/sync')
    updateUI(latestData)
  })
})
```

**Keep polling for**:
- Legacy browsers (IE11 if required)
- Environments blocking WebSocket (corporate firewalls)
- Automatic fallback (transparent to user)

### Cost Analysis

**Before Migration** (5,000 users, 5-second polling):
- Server cost: $500-2,000/month
- Database load: 3.6M queries/hour
- Average latency: 2.5 seconds

**After Migration (WebSocket)**:

**Managed Service (Pusher)**:
- Service cost: $299-999/month
- Server cost reduction: -$300-1,500/month (fewer API requests)
- Database cost reduction: -$100-500/month (pub/sub pattern)
- **Net cost**: Similar or 20-40% lower
- **Latency improvement**: <200ms (10x better)

**Self-Hosted (Socket.IO)**:
- Infrastructure: $200-500/month
- Operations: $200-500/month (DevOps)
- Server cost reduction: -$300-1,500/month
- **Net cost**: 40-70% lower
- **Latency improvement**: <200ms (10x better)

### Risk Mitigation

**Risk 1: WebSocket Connection Failures**

**Mitigation**:
- Feature flag for instant rollback
- Automatic polling fallback
- Client-side reconnection logic
- Monitor connection success rate

---

**Risk 2: Increased Server Load (Connection Overhead)**

**Mitigation**:
- Gradual rollout (10% → 50% → 100%)
- Pre-scale infrastructure
- Load testing before full rollout
- Sticky sessions (load balancer)

---

**Risk 3: Data Synchronization Issues**

**Mitigation**:
- Full state sync on connect
- Message deduplication (client-side)
- Idempotent updates
- Versioning/timestamps

### Timeline Summary

| Phase | Duration | Key Activities | Risk Level |
|-------|----------|----------------|------------|
| **Setup** | 1-2 weeks | Infrastructure, SDK integration | Low |
| **Hybrid** | 2-3 weeks | Feature flag rollout, monitoring | Medium |
| **Reduction** | 1-2 weeks | Polling fallback only | Low |
| **Complete** | 1-2 weeks | Remove polling (optional) | Medium |
| **Total** | **6-9 weeks** | Full migration | **Medium** |

---

## Migration 2: Self-Hosted → Managed Service

### When to Migrate

**Migrate when**:
- DevOps burden >20 hours/month
- Team size shrinking (can't sustain operations)
- Multi-region expansion needed (infrastructure complexity)
- Outages costing more than managed service price
- Opportunity cost: Engineers should focus on product

**Don't migrate when**:
- Managed service cost >3x self-hosted total cost
- Latency requirements only met by self-hosted
- Vendor lock-in unacceptable
- Infrastructure customization critical

### Current State Analysis

**Self-Hosted (Socket.IO + Redis)**:
- Monthly infrastructure: $300-800
- Monthly operations: $500-2,000 (DevOps time)
- **Total: $800-2,800/month**

**Pain points**:
- On-call burden (nights/weekends)
- Scaling complexity (manual provisioning)
- Security updates (ongoing maintenance)
- Single region (global latency issues)

### Migration Strategy

**Phase 1: Proof of Concept (Week 1-2)**

Deploy managed service alongside self-hosted:

```javascript
// Test Ably with 5% of traffic
if (userId % 20 === 0) {
  connectToAbly()
} else {
  connectToSocketIO() // Existing
}

function connectToAbly() {
  const ably = new Ably.Realtime({ authUrl: '/api/ably-token' })
  const channel = ably.channels.get('updates')
  channel.subscribe(data => updateUI(data))
}
```

**Test metrics**:
- Latency comparison (Ably vs Socket.IO)
- Connection success rate
- Cost per user (actual vs projected)
- Feature parity (ensure all features work)

---

**Phase 2: Dual Publishing (Week 3-4)**

Publish to both systems during transition:

```javascript
// Backend publishes to both
async function publishUpdate(data) {
  // Existing Socket.IO
  io.emit('update', data)

  // New Ably
  await ablyRest.channels.get('updates').publish('update', data)
}
```

**Gradual migration**:
- Week 3: 25% of users on managed service
- Week 4: 75% of users on managed service

---

**Phase 3: Complete Migration (Week 5-6)**

Move 100% to managed service:

```javascript
// Remove Socket.IO client code
// All users on Ably

function connectToAbly() {
  const ably = new Ably.Realtime({
    authUrl: '/api/ably-token',
    recover: (lastConnectionDetails, cb) => {
      // Resume connection after disconnect
      cb(true)
    }
  })

  // Subscribe to channels
  const channel = ably.channels.get(`user:${userId}`)
  channel.subscribe('update', data => updateUI(data))
}
```

**Deprecation**:
- Week 5: Stop accepting new Socket.IO connections
- Week 6: Shutdown Socket.IO infrastructure
- Redirect all users to managed service

---

**Phase 4: Decommission (Week 7-8)**

Remove self-hosted infrastructure:

- Terminate EC2 instances
- Remove Redis cluster
- Archive logs (compliance)
- Delete load balancers
- Update DNS (if applicable)

**Documentation**:
- Update architecture diagrams
- Remove operational runbooks
- Document new managed service setup
- Train team on new tooling

### Cost Analysis

**Before Migration** (5,000 users, self-hosted):
- Infrastructure: $300-800/month
- Operations: $500-2,000/month
- **Total: $800-2,800/month**

**After Migration** (5,000 users, Ably):
- Service cost: $750-1,500/month
- Operations: $0-200/month (monitoring only)
- **Total: $750-1,700/month**

**Savings**: $50-1,100/month (depends on operational costs)

**Intangible benefits**:
- Reduced on-call burden
- Team focuses on product (not infrastructure)
- Multi-region automatic
- Professional SLA (99.999% uptime)

### Risk Mitigation

**Risk 1: Vendor Lock-In**

**Mitigation**:
- Abstract WebSocket layer (adapter pattern)
- Keep publish logic portable
- Plan for future migration if needed

```javascript
// Abstraction layer
class RealtimeService {
  async publish(channel, data) {
    // Currently Ably, but could swap
    await this.provider.publish(channel, data)
  }
}
```

---

**Risk 2: Cost Overruns**

**Mitigation**:
- Set billing alerts
- Monitor connection-minutes daily
- Optimize message frequency
- Tier users (active vs passive)

---

**Risk 3: Feature Regression**

**Mitigation**:
- Feature parity checklist
- End-to-end testing
- Shadow mode (dual publish)
- Gradual rollout with monitoring

### Timeline Summary

| Phase | Duration | Key Activities | Risk Level |
|-------|----------|----------------|------------|
| **PoC** | 1-2 weeks | Test managed service | Low |
| **Dual Publish** | 2-3 weeks | Gradual migration | Medium |
| **Complete** | 2-3 weeks | 100% on managed | Medium |
| **Decommission** | 1-2 weeks | Shutdown self-hosted | Low |
| **Total** | **6-10 weeks** | Full migration | **Medium** |

---

## Migration 3: Managed Service → Self-Hosted

### When to Migrate

**Migrate when**:
- Monthly cost >$2,000 and growing linearly
- DevOps capacity available (10-20 hours/month)
- Need <100ms latency (managed services add overhead)
- Want infrastructure customization
- Multi-project cost amortization (shared infrastructure)

**Don't migrate when**:
- Team size <5 engineers (operational burden)
- Current cost <$1,000/month (savings not worth complexity)
- Lack infrastructure expertise
- Need global multi-region (expensive to self-host)

### Migration Strategy

**Phase 1: Infrastructure Setup (Week 1-4)**

Deploy self-hosted infrastructure in parallel:

**Option A: Centrifugo + Redis**
```bash
# Docker compose setup
docker-compose up -d

services:
  centrifugo:
    image: centrifugo/centrifugo:latest
    ports:
      - "8000:8000"
    environment:
      CENTRIFUGO_TOKEN_HMAC_SECRET_KEY: secret
      CENTRIFUGO_ADMIN_PASSWORD: admin
      CENTRIFUGO_ADMIN_SECRET: admin_secret

  redis:
    image: redis:latest
    ports:
      - "6379:6379"
```

**Option B: Socket.IO + Redis**
```javascript
// Server setup
const io = require('socket.io')(server)
const redisAdapter = require('socket.io-redis')

io.adapter(redisAdapter({
  host: process.env.REDIS_HOST,
  port: 6379
}))

io.on('connection', socket => {
  socket.on('subscribe', channel => {
    socket.join(channel)
  })
})
```

**Setup time**: 2-4 weeks (includes testing, monitoring)
**Initial cost**: $300-800/month

---

**Phase 2: Parallel Running (Week 5-8)**

Publish to both managed and self-hosted:

```javascript
// Backend publishes to both
async function publishUpdate(channel, data) {
  // Existing Pusher
  await pusher.trigger(channel, 'update', data)

  // New Centrifugo
  await centrifugo.publish(channel, data)
}

// Client connects based on feature flag
if (featureFlags.selfHosted) {
  connectToCentrifugo()
} else {
  connectToPusher()
}
```

**Gradual migration**:
- Week 5-6: 10% on self-hosted (monitor closely)
- Week 7: 50% on self-hosted
- Week 8: 100% on self-hosted

---

**Phase 3: Managed Service Shutdown (Week 9-10)**

Decommission managed service:

- Stop publishing to managed service
- Cancel subscription
- Archive configuration
- Update documentation

**Cost savings realized**: Month 3 onward

### Cost Analysis

**Before Migration** (10,000 users, Pusher):
- Service cost: $2,000-5,000/month
- **Total: $2,000-5,000/month**

**After Migration** (10,000 users, Centrifugo):
- Infrastructure: $400-800/month
- Operations: $500-1,500/month (DevOps)
- **Total: $900-2,300/month**

**Savings**: $1,100-2,700/month

**Break-even**: Month 2-3 (after initial setup investment)

### Timeline Summary

| Phase | Duration | Key Activities | Risk Level |
|-------|----------|----------------|------------|
| **Setup** | 2-4 weeks | Infrastructure, monitoring | Medium |
| **Parallel** | 4 weeks | Gradual migration | High |
| **Shutdown** | 2 weeks | Cancel managed service | Low |
| **Total** | **8-10 weeks** | Full migration | **High** |

---

## Migration 4: Provider A → Provider B

### When to Migrate

**Migrate when**:
- Pricing changes make Provider B cheaper (30%+ savings)
- Provider A lacks critical features
- Reliability issues with Provider A
- Geographic expansion needs (Provider B has better coverage)

**Don't migrate when**:
- Savings <20% (not worth migration risk)
- Both providers meet needs (avoid churn)
- Migration cost >6 months of savings

### Example: Pusher → Ably

**Reason**: Need better latency SLA, similar cost

**Phase 1: Compatibility Analysis (Week 1)**

Map features:

| Feature | Pusher | Ably | Migration Complexity |
|---------|--------|------|---------------------|
| Channels | `pusher.subscribe('channel')` | `ably.channels.get('channel')` | Low (similar API) |
| Private channels | Built-in signature | Token-based auth | Medium (auth change) |
| Presence | Built-in | Built-in | Low |
| Client events | Supported | Supported | Low |
| Webhooks | Built-in | Built-in | Low (URL change) |

**Estimated complexity**: Medium (2-4 weeks)

---

**Phase 2: Client SDK Migration (Week 2-3)**

Update client code:

```javascript
// Before (Pusher)
const pusher = new Pusher('app-key', { cluster: 'us2' })
const channel = pusher.subscribe('my-channel')
channel.bind('my-event', data => handleData(data))

// After (Ably)
const ably = new Ably.Realtime({ authUrl: '/api/ably-token' })
const channel = ably.channels.get('my-channel')
channel.subscribe('my-event', data => handleData(data))
```

**Abstraction layer** (recommended):
```javascript
// RealtimeAdapter (works with both)
class RealtimeAdapter {
  constructor(provider) {
    this.provider = provider === 'pusher' ? new PusherProvider() : new AblyProvider()
  }

  subscribe(channel, event, callback) {
    return this.provider.subscribe(channel, event, callback)
  }
}

// Switch providers via config
const realtime = new RealtimeAdapter(process.env.REALTIME_PROVIDER)
```

---

**Phase 3: Backend Migration (Week 3-4)**

Update publish logic:

```javascript
// Before (Pusher)
await pusher.trigger('my-channel', 'my-event', data)

// After (Ably)
await ablyRest.channels.get('my-channel').publish('my-event', data)
```

**Dual publishing during transition**:
```javascript
async function publishUpdate(channel, event, data) {
  if (process.env.DUAL_PUBLISH) {
    await pusher.trigger(channel, event, data)
    await ablyRest.channels.get(channel).publish(event, data)
  } else {
    await ablyRest.channels.get(channel).publish(event, data)
  }
}
```

---

**Phase 4: Gradual Rollout (Week 4-6)**

- Week 4: 10% of users on Ably
- Week 5: 50% of users on Ably
- Week 6: 100% on Ably, shutdown Pusher

### Cost Comparison

**Pusher** (5,000 users):
- $299/month (Business plan)

**Ably** (5,000 users):
- $150-300/month (Standard plan)

**Savings**: $0-150/month (similar cost, but better SLA)

**Migration cost**: $2,000-5,000 (engineering time)

**Break-even**: 13-33 months (long payback, only migrate if feature/SLA driven)

### Timeline Summary

| Phase | Duration | Key Activities | Risk Level |
|-------|----------|----------------|------------|
| **Analysis** | 1 week | Feature mapping | Low |
| **Client Migration** | 2 weeks | SDK updates | Medium |
| **Backend Migration** | 1-2 weeks | Publish logic | Medium |
| **Rollout** | 2-3 weeks | Gradual migration | Medium |
| **Total** | **6-8 weeks** | Full migration | **Medium** |

---

## General Migration Best Practices

### 1. Feature Flags

Always use feature flags for gradual rollout:

```javascript
if (featureFlags.enabled('new-websocket-provider')) {
  useNewProvider()
} else {
  useOldProvider()
}
```

**Benefits**:
- Instant rollback
- A/B testing
- Gradual rollout (10% → 50% → 100%)

---

### 2. Monitoring

Track key metrics during migration:

- **Connection success rate**: Target >95%
- **Latency distribution**: P50, P95, P99
- **Message delivery rate**: Target 100%
- **Error rates**: <1% acceptable
- **Cost per user**: Track daily

---

### 3. Dual Running Period

Always run old and new systems in parallel:

- Publish to both (1-4 weeks)
- Monitor for discrepancies
- Compare latency, reliability
- Verify feature parity

---

### 4. Rollback Plan

Always have instant rollback:

```javascript
// Config-driven
const provider = config.websocketProvider // 'old' or 'new'

// Feature flag (instant disable)
if (featureFlags.enabled('new-provider')) {
  connectToNew()
} else {
  connectToOld()
}
```

---

### 5. Communication

Inform users during migration:

- Status page updates
- In-app banners (if downtime expected)
- Email notifications (if breaking changes)
- Transparent timeline

---

## Migration Cost Summary

| Migration Type | Timeline | Complexity | Cost (Engineering) | Risk Level |
|----------------|----------|------------|--------------------|------------|
| **Polling → WebSocket** | 6-9 weeks | Medium | $5K-15K | Medium |
| **Self-Hosted → Managed** | 6-10 weeks | Medium | $8K-20K | Medium |
| **Managed → Self-Hosted** | 8-10 weeks | High | $10K-30K | High |
| **Provider A → Provider B** | 6-8 weeks | Medium | $5K-15K | Medium |

**Key Insight**: All migrations take 6-10 weeks for safe, gradual rollout. Rushing increases risk.

**Recommendation**: Budget 2-3 months for any WebSocket migration, including testing, rollout, and monitoring period.
