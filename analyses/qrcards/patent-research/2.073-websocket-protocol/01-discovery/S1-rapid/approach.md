# S1: Rapid Library Search - WebSocket Protocol & Managed Services

## Methodology Overview

**Core Philosophy**: Trust production validation and ecosystem adoption for real-time communication infrastructure.

**Time Budget**: 2-3 hours focused research

**Research Strategy**: Evaluate both protocol fundamentals and managed service options through lens of:
- Proven scale (documented concurrent connection limits)
- Measurable latency (real benchmarks, not marketing claims)
- Total cost of ownership (infrastructure + operational)

## Discovery Approach

### Phase 1: Protocol Foundation (30 minutes)
- IETF RFC 6455 WebSocket standard
- Browser/server implementation status
- Baseline latency characteristics (network overhead, handshake)

### Phase 2: Managed Services (90 minutes)
Evaluate market leaders across two categories:

**Pure WebSocket Services**:
- Pusher (market leader, extensive docs)
- Ably (enterprise focus, latency guarantees)

**Backend-Integrated Real-time**:
- Socket.IO (self-hosted, fallback mechanisms)
- Supabase Realtime (Postgres CDC)
- Firebase Realtime (Google infrastructure)
- Centrifugo (self-hosted, Go-based performance)

### Phase 3: Critical Analysis (30-60 minutes)
- Latency reality check: What's achievable at 1K/5K/10K connections?
- Cost modeling: Monthly infrastructure for different scales
- Build vs buy decision framework
- Production case study validation

## Research Questions Priority

1. **LATENCY BENCHMARKS** (highest priority)
   - Round-trip latency (client → server → client)
   - Fan-out latency (1 → 10K devices)
   - Real-world network variance (WiFi, 4G, 5G)
   - Geographic distribution impact

2. **SCALING LIMITS**
   - Concurrent connection ceiling per instance
   - Message throughput (messages/second)
   - Memory/CPU characteristics at scale

3. **COST ANALYSIS**
   - Per-connection pricing models
   - Per-message vs per-GB bandwidth
   - Self-hosted infrastructure costs
   - Operational overhead (DevOps burden)

4. **PRODUCTION VALIDATION**
   - Who uses what at scale?
   - Documented case studies (not testimonials)
   - Known limitations/failure modes

## Selection Criteria

**Must Have**:
- Documented latency benchmarks (not marketing claims)
- Proven at 1,000+ concurrent connections
- Clear pricing/cost model

**Nice to Have**:
- Open source option for self-hosting
- Geographic distribution/edge deployment
- Built-in fallback mechanisms
- Protocol extensions (presence, history)

## Information Sources

- GitHub repositories (stars, issues, real-world problems)
- Official documentation (benchmarks, architecture)
- Independent benchmark studies
- Stack Overflow (operational reality)
- Production case studies (Hacker News, engineering blogs)
- Academic papers (IETF RFCs, performance studies)

## Deliverable Structure

Each service evaluation includes:
1. Popularity/adoption metrics
2. **Latency benchmarks** (documented numbers)
3. Scaling characteristics (connection limits, throughput)
4. Cost model (1K/5K/10K device scenarios)
5. Self-hosted vs managed trade-offs
6. Production validation (real deployments)

## Success Criteria

Research complete when we can answer:
- What's realistic latency for real-time sync? (50ms? 100ms? 200ms?)
- What does it cost monthly for 1K/5K/10K concurrent connections?
- Should we build or buy?
- What are the technical constraints at scale?
