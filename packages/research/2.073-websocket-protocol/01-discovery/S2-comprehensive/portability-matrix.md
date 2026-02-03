# WebSocket Implementation Portability Matrix

**Research Tier**: S2 Comprehensive Portability Analysis
**Date Compiled**: December 3, 2025

## Overview

This matrix evaluates feature parity and portability across managed and self-hosted WebSocket implementations. Portability assessment considers both technical migration complexity and vendor lock-in risk.

## Feature Comparison Matrix

### Connection Management

| Feature | Pusher | Ably | Socket.io | Supabase | Centrifugo |
|---------|--------|------|-----------|----------|------------|
| **Auto-reconnection** | Yes (SDK) | Yes (SDK) | Yes (SDK) | Yes (SDK) | Yes (SDK) |
| **Connection recovery** | No | Yes | No | No | Yes (offset-based) |
| **Fallback transports** | HTTP polling | SSE, Comet | HTTP polling | No | SockJS, SSE |
| **TLS/SSL** | Standard | Standard | DIY/Proxy | Standard | DIY/Proxy |
| **Max connections (single server)** | N/A | N/A | 10-20K | N/A | 100K+ |
| **Connection limits** | Plan-based | Plan-based | Hardware | Postgres pool | Hardware |

**Portability Impact**:
- Auto-reconnection: All platforms provide, but SDK-specific (need to replace client code)
- Connection recovery: Ably and Centrifugo have proprietary state recovery mechanisms
- Fallback transports: Less relevant in 2025 (WebSocket widely supported)

### Message Delivery

| Feature | Pusher | Ably | Socket.io | Supabase | Centrifugo |
|---------|--------|------|-----------|----------|------------|
| **Delivery guarantee** | At-most-once | Configurable | At-most-once | At-most-once | Configurable |
| **Message ordering** | Per channel | Per channel | Per connection | Per table | Per channel |
| **Max message size** | 10 KB | 64 KB | Unlimited | Unlimited | 64 KB (config) |
| **Message persistence** | No | Yes (2min-365d) | No (DIY) | No (DB only) | Yes (config) |
| **Message history API** | No | Yes | No (DIY) | No | Yes |
| **Acknowledgments** | No | Yes | Yes (callback) | No | No |
| **Binary support** | No | Yes | Yes | Yes | Yes |

**Portability Impact**:
- Delivery guarantees: Ably and Centrifugo offer at-least-once; migrating to/from best-effort requires application changes
- Message persistence: Ably and Centrifugo lock-in via proprietary history APIs
- Binary support: Interoperable (standard formats)

### Pub/Sub Architecture

| Feature | Pusher | Ably | Socket.io | Supabase | Centrifugo |
|---------|--------|------|-----------|----------|------------|
| **Channels/Topics** | Channels | Channels | Rooms | Tables + Topics | Channels |
| **Private channels** | Yes (prefix) | Yes (tokens) | No (DIY auth) | Yes (RLS) | Yes (tokens) |
| **Presence tracking** | Yes (100 max) | Yes (1000s) | No (DIY) | Yes (Phoenix) | Yes (config) |
| **Pattern subscriptions** | No | No | No | No | Yes (wildcards) |
| **Namespaces** | No | No | Yes | No | Yes |
| **User-specific channels** | No | No | No | No | Yes |

**Portability Impact**:
- Channel concepts: Similar across platforms (high portability)
- Private channel auth: Different mechanisms (Pusher signatures vs. Ably tokens vs. Supabase RLS) - moderate lock-in
- Presence: Different implementations (low portability for presence features)

### Authentication & Authorization

| Feature | Pusher | Ably | Socket.io | Supabase | Centrifugo |
|---------|--------|------|-----------|----------|------------|
| **Auth method** | HMAC signature | JWT + capabilities | Custom middleware | Supabase JWT | JWT |
| **Token expiration** | No | Yes | Custom | Yes | Yes |
| **Token refresh** | No | Yes | Custom | Yes | Yes |
| **Row-level security** | No | No | No | Yes (Postgres RLS) | No |
| **Granular permissions** | No | Yes (capabilities) | Custom | Yes (RLS) | Yes (claims) |

**Portability Impact**:
- Pusher's HMAC signature is proprietary (moderate lock-in)
- JWT-based: Ably, Supabase, Centrifugo (higher portability with standard claims)
- Socket.io custom auth: Most portable (you control logic)
- Supabase RLS: High lock-in to Postgres/Supabase ecosystem

### Horizontal Scaling

| Feature | Pusher | Ably | Socket.io | Supabase | Centrifugo |
|---------|--------|------|-----------|----------|------------|
| **Multi-server support** | Managed | Managed | Redis adapter | Managed | Redis/Nats |
| **Sticky sessions required** | No | No | Yes | No | No |
| **State synchronization** | Automatic | Automatic | Redis pub/sub | Automatic | Redis/Nats |
| **Geographic distribution** | Yes (9 clusters) | Yes (15 regions) | DIY | Limited | DIY |
| **Automatic failover** | Yes | Yes | No (DIY) | Yes | No (DIY) |

**Portability Impact**:
- Managed services: Automatic scaling, but black-box (no portability)
- Self-hosted: Redis/Nats adapters are similar patterns (moderate portability)
- Sticky sessions: Socket.io lock-in to load balancer configuration

### Monitoring & Observability

| Feature | Pusher | Ably | Socket.io | Supabase | Centrifugo |
|---------|--------|------|-----------|----------|------------|
| **Built-in dashboard** | Yes | Yes | No | Yes | Yes (admin UI) |
| **Metrics API** | Yes | Yes | DIY | Limited | Prometheus |
| **Webhooks** | Yes | Yes | DIY | Limited | DIY |
| **Real-time stats** | Yes | Yes | No | Yes | Yes |
| **Log export** | Limited | Yes | DIY | Limited | DIY |
| **Debugging tools** | Debug console | Protocol inspector | DIY | Limited | Admin UI |

**Portability Impact**:
- Metrics export: Ably and Centrifugo (Prometheus) more portable
- Webhooks: Different event formats (moderate lock-in)
- Custom instrumentation needed for self-hosted (Socket.io)

### Developer Experience

| Feature | Pusher | Ably | Socket.io | Supabase | Centrifugo |
|---------|--------|------|-----------|----------|------------|
| **Client SDKs** | 40+ platforms | 25+ platforms | 10+ platforms | 5+ platforms | 10+ platforms |
| **Server libraries** | 8+ languages | 10+ languages | Node.js only | JavaScript/Python | Any (HTTP/GRPC) |
| **Documentation quality** | Excellent | Excellent | Good | Good | Excellent |
| **Examples/tutorials** | Extensive | Extensive | Extensive | Good | Good |
| **Community size** | Large | Medium | Very large | Large | Small |

**Portability Impact**:
- More SDKs = deeper lock-in (client code in more places)
- Socket.io's large community = more migration resources available
- Centrifugo's language-agnostic server API = higher portability

## Portability Assessment Summary

### Lock-in Risk Ranking (Low to High)

1. **Socket.io** - LOW
   - Open source, self-hosted
   - Custom auth logic (you own it)
   - Large community, many migration guides
   - Standard WebSocket underneath

2. **Centrifugo** - LOW
   - Open source, self-hosted
   - Standard JWT authentication
   - Language-agnostic API
   - Single binary, no runtime dependencies

3. **Ably** - MEDIUM
   - Token-based auth (standard JWT)
   - Proprietary connection recovery
   - Message history lock-in
   - Good data export capabilities

4. **Pusher** - MEDIUM-HIGH
   - Proprietary HMAC signature auth
   - Channel naming conventions
   - No message persistence (easier to exit)
   - Limited data export

5. **Supabase Realtime** - HIGH
   - Deeply coupled to Postgres
   - Supabase ecosystem lock-in
   - RLS policies non-portable
   - Database portability is separate concern

### Migration Complexity Matrix

| From → To | Pusher | Ably | Socket.io | Supabase | Centrifugo |
|-----------|--------|------|-----------|----------|------------|
| **Pusher** | - | Medium | Medium | High | Medium |
| **Ably** | Medium | - | Medium | High | Low-Med |
| **Socket.io** | Low-Med | Low-Med | - | High | Low |
| **Supabase** | High | High | High | - | High |
| **Centrifugo** | Medium | Low-Med | Low | High | - |

**Complexity factors**:
- **Low**: Similar architecture, minimal refactoring
- **Medium**: Auth changes, channel mapping, client SDK replacement
- **High**: Fundamental architecture differences, extensive refactoring

### Feature Portability by Category

**High Portability** (Easy to migrate):
- Basic pub/sub messaging
- Channel/room concepts
- Binary message payloads
- Connection lifecycle events
- TLS encryption

**Medium Portability** (Requires adaptation):
- Private channel authentication
- Presence tracking
- Message batching
- Webhook event formats
- Client SDK API patterns

**Low Portability** (Significant re-implementation):
- Guaranteed delivery semantics (Ably)
- Connection state recovery (Ably, Centrifugo)
- Message history/persistence (Ably, Centrifugo)
- Row-level security (Supabase)
- Database change streaming (Supabase)

## Vendor Lock-in Risk Mitigation Strategies

### Abstraction Layer Pattern
Create an internal wrapper around WebSocket provider:

```
Application Code → Internal Real-time API → Provider SDK
```

**Benefits**:
- Swap providers by changing one implementation
- Test with mock providers
- Gradual migration possible

**Costs**:
- Additional development time
- Potential performance overhead
- May not cover all provider-specific features

### Multi-Provider Strategy
Use different providers for different use cases:

- **Broadcast notifications**: Simple provider (Pusher)
- **Guaranteed delivery**: Robust provider (Ably)
- **Database changes**: Database-native (Supabase)

**Benefits**: Right tool for each job
**Costs**: Multiple integrations, complexity

### Exit Planning
For critical applications, maintain:
- **Architecture documentation**: How real-time system works
- **Migration playbook**: Steps to migrate to alternative
- **Test self-hosted option**: Ensure Socket.io or Centrifugo could work

## Recommendations by Portability Priority

### Maximum Portability (minimize lock-in)
**Recommended**: Socket.io or Centrifugo
- Open source, self-hosted
- Standard protocols underneath
- Can migrate between them relatively easily
- Complete data/infrastructure control

### Balanced Portability & Features
**Recommended**: Ably
- Good export capabilities
- Standard JWT authentication
- Strong features without excessive proprietary lock-in
- Clear migration paths documented

### Portability Secondary to Speed
**Recommended**: Pusher or Supabase
- Fastest to integrate
- Optimize for current problem, accept future migration cost
- Pusher: General-purpose, simple
- Supabase: If already using Supabase database

## Conclusion

No WebSocket implementation is truly portable without refactoring, but the degree of lock-in varies significantly:

- **Self-hosted options** (Socket.io, Centrifugo) offer greatest portability and control
- **Managed services** trade portability for operational convenience
- **Database-coupled solutions** (Supabase) have highest lock-in but solve specific use cases elegantly

Choose based on:
1. Your team's operational capacity (self-hosted vs. managed)
2. Required features (presence, history, guarantees)
3. Exit strategy importance (critical system = prioritize portability)
