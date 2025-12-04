# WebSocket Protocol: A Technical Guide for Decision Makers

**Research Code**: 2.073
**Domain**: Real-Time Communication Protocols
**Audience**: CTOs, Engineering Managers, Technical PMs
**Date**: December 3, 2025

---

## What This Document Covers

This explainer provides foundational knowledge about WebSocket and real-time communication concepts. It does NOT compare specific providers—see the `01-discovery/` research for implementation comparisons.

---

## What is WebSocket?

WebSocket is a communication protocol that provides full-duplex (two-way) communication over a single TCP connection. Unlike HTTP, which follows request-response patterns, WebSocket keeps a persistent connection open for instant bidirectional messaging.

### The HTTP Problem

Traditional HTTP works like postal mail:

1. Client sends request
2. Server processes request
3. Server sends response
4. Connection closes

For real-time updates, clients must repeatedly ask "anything new?" (polling). This wastes resources and adds latency.

### The WebSocket Solution

WebSocket works like a phone call:

1. Initial handshake (HTTP upgrade)
2. Connection stays open
3. Either side can send messages anytime
4. Connection persists until explicitly closed

---

## Glossary of Real-Time Terms

### Protocol Concepts

**Full-Duplex**
Both parties can send and receive simultaneously. Like a phone conversation, not a walkie-talkie.

**Half-Duplex**
Only one party can transmit at a time. HTTP is effectively half-duplex (request, wait, response).

**Persistent Connection**
The connection stays open after the initial handshake. No reconnection overhead for each message.

**WebSocket Handshake**
The initial HTTP request with `Upgrade: websocket` header. If accepted, the protocol switches from HTTP to WebSocket.

**Frame**
A WebSocket message unit. Can be text, binary, or control frames (ping/pong, close).

### Architecture Concepts

**Pub/Sub (Publish-Subscribe)**
A messaging pattern where senders (publishers) broadcast to channels, and receivers (subscribers) listen to channels. Decouples sender from receiver.

**Channel/Room**
A named group of connections. Messages sent to a channel reach all subscribers. Common for chat rooms, live updates.

**Presence**
Tracking who is connected. "Alice joined" / "Bob left" notifications. Requires server-side connection tracking.

**Broadcast**
Sending a single message to multiple connections simultaneously. The foundation of real-time updates.

### Performance Concepts

**Latency**
Time from message sent to message received. Measured in milliseconds. Sub-50ms is "real-time" for human perception.

**P50/P95/P99 Latency**
Percentile measurements. P95 = 95% of messages arrive within this time. P99 matters for worst-case experience.

**Concurrent Connections**
Number of simultaneous open WebSocket connections. A key scaling metric. 1K concurrent = 1,000 open sockets.

**Message Throughput**
Messages processed per second. Different from connections—one connection can send many messages.

### Reliability Concepts

**Delivery Guarantee**
Whether messages are guaranteed to arrive. Options: at-most-once, at-least-once, exactly-once.

**Message Ordering**
Whether messages arrive in the order sent. FIFO (first-in-first-out) ordering is not automatic at scale.

**Reconnection**
Automatic reconnection when connection drops. Critical for mobile users and unstable networks.

**Message Buffering**
Storing messages during disconnection for delivery upon reconnection. Prevents message loss.

---

## WebSocket vs Alternatives

### HTTP Long Polling

**How it works**: Client sends request, server holds response until data available, client immediately reconnects.

**Use when**: WebSocket not supported, simple use case, infrequent updates.

**Avoid when**: Need true real-time, high message frequency, bidirectional communication.

### Server-Sent Events (SSE)

**How it works**: HTTP connection stays open, server pushes events to client. One-way only.

**Use when**: Server→client updates only, text data, HTTP/2 available.

**Avoid when**: Need client→server messages, binary data, bidirectional.

### WebTransport

**How it works**: Next-generation protocol over HTTP/3 with unreliable/reliable streams.

**Use when**: Ultra-low latency needed, can accept data loss, cutting-edge applications.

**Avoid when**: Browser support needed today (limited), reliability required.

### Comparison Table

| Protocol | Direction | Latency | Complexity | Browser Support |
|----------|-----------|---------|------------|-----------------|
| HTTP Polling | Bidirectional | 1-30s | Low | Universal |
| Long Polling | Bidirectional | 100ms-1s | Medium | Universal |
| SSE | Server→Client | 50-200ms | Low | 96%+ |
| WebSocket | Bidirectional | 10-100ms | Medium | 100% |
| WebTransport | Bidirectional | 5-50ms | High | ~70% |

---

## Scaling WebSocket: The Challenges

### The Connection Problem

Each WebSocket connection consumes:
- A TCP socket (OS limit: ~65K per IP)
- Memory (~10-50KB per connection)
- CPU for heartbeats and message handling

**At scale**: 10K connections = 100-500MB RAM just for sockets.

### The Distribution Problem

With multiple servers, how does Server A send a message to User B on Server C?

**Solutions**:
- **Sticky sessions**: Same user always hits same server (limited scaling)
- **Pub/Sub backend**: Redis, NATS, or similar to broadcast across servers
- **Managed service**: Pusher, Ably handle distribution for you

### The Persistence Problem

If a user reconnects to a different server, how do they get missed messages?

**Solutions**:
- **Message buffering**: Store recent messages, replay on reconnect
- **Event sourcing**: Store all events, replay from checkpoint
- **Managed service**: Built-in message history and replay

---

## The Physics of Latency

### What's Achievable

**Same datacenter**: 1-5ms
**Same region**: 10-30ms
**Cross-continent**: 50-150ms
**Global (worst case)**: 200-300ms

**Speed of light limit**: ~67ms London→Sydney (physical minimum)

### The "<50ms" Claim

For 1,000 users in the same region to ALL receive a message in <50ms:
- **Streaming delivery**: First user gets it in <50ms ✓
- **Simultaneous delivery**: Last user gets it in 77-135ms ✗

**Honest expectation**: P50 <100ms, P95 <150ms for global real-time applications.

---

## Self-Hosted vs Managed Services

### Self-Hosted (Socket.io, Centrifugo)

**Pros**:
- Full control over infrastructure
- No per-message or per-connection fees
- Can optimize for specific use case
- No vendor lock-in

**Cons**:
- Requires DevOps expertise
- Scaling is your problem
- On-call for outages
- Must build reconnection, presence, etc.

### Managed Services (Pusher, Ably)

**Pros**:
- Zero infrastructure management
- Built-in scaling, global distribution
- Presence, history, channels included
- SLAs and support

**Cons**:
- Per-message or per-connection costs
- Less control over behavior
- Vendor lock-in risk
- May not support custom requirements

### Cost Crossover Point

Self-hosted typically becomes cheaper at 5,000+ concurrent connections IF you have DevOps capacity. Below 5K, managed services often have better TCO.

---

## Common Misconceptions

### "WebSocket is always better than HTTP"

WebSocket adds complexity. For infrequent updates (every 30s+), simple polling is often simpler and sufficient.

### "WebSocket solves all latency problems"

WebSocket eliminates connection overhead but cannot defeat physics. Cross-continent latency is 100ms+ regardless of protocol.

### "We need exactly-once delivery"

Exactly-once is expensive and often unnecessary. At-least-once + idempotent operations is simpler and usually sufficient.

### "Managed services are too expensive"

At small scale (<1K connections), managed services often cost $25-100/month. The engineering time to build equivalent functionality costs far more.

---

## Build vs Buy Decision Framework

### Build (Self-Hosted) When:

- **Scale**: >5K concurrent connections
- **Latency**: Need <20ms (Centrifugo territory)
- **Control**: Custom protocol requirements
- **Team**: Have DevOps capacity
- **Cost**: Can amortize infrastructure investment

### Buy (Managed) When:

- **Speed**: Need to ship quickly
- **Scale**: <5K concurrent connections
- **Team**: No dedicated DevOps
- **Reliability**: Need SLAs without on-call burden
- **Features**: Need presence, history, channels out-of-box

---

## Key Trade-offs

### Latency vs Cost

- <20ms requires self-hosted + dedicated infrastructure
- <100ms achievable with managed services
- <200ms achievable with any solution

### Reliability vs Complexity

- At-most-once: Simple but may lose messages
- At-least-once: Must handle duplicates
- Exactly-once: Complex, expensive, rarely needed

### Control vs Convenience

- Self-hosted: Maximum control, maximum responsibility
- Managed: Constrained options, zero ops burden

---

## Metrics That Matter

### Meaningful Metrics

- **P95 message latency**: User experience metric
- **Connection success rate**: Are users connecting?
- **Reconnection time**: How fast do dropped connections recover?
- **Message delivery rate**: Are messages getting through?

### Vanity Metrics

- **Raw throughput** (without latency): Fast but laggy is useless
- **Peak connections** (without retention): Spikes don't matter if users leave
- **Uptime** (without latency SLA): "Up but slow" is effectively down

---

## Summary: What Decision Makers Should Know

1. **WebSocket is mature**: RFC 6455 is 14 years old, 100% browser support.
2. **Physics sets limits**: <50ms to ALL users globally is not achievable.
3. **Scale drives decisions**: <5K → managed, >5K → consider self-hosted.
4. **Latency costs money**: <20ms requires dedicated infrastructure.
5. **Build vs buy**: DevOps capacity is the deciding factor, not technical capability.

---

**Research Disclaimer**: This explainer provides educational context for real-time communication concepts. For specific provider comparisons and recommendations, see the S1-S4 discovery research.
