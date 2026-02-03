# Supabase Realtime: Postgres Change Data Capture

**Category**: Managed Service (Postgres-coupled)
**Provider**: Supabase
**Primary Use Case**: Database change streaming via WebSockets
**Date Compiled**: December 3, 2025

## Architecture Overview

Supabase Realtime is fundamentally different from general-purpose WebSocket platforms. It streams Postgres database changes (INSERT, UPDATE, DELETE) to connected clients in real-time, built on top of Postgres logical replication.

### Core Components

**Realtime Server** (Elixir):
- Built on Phoenix Framework channels
- Listens to Postgres Write-Ahead Log (WAL)
- Broadcasts database changes to subscribed WebSocket clients
- Supports presence tracking (Phoenix Presence)

**Channels**:
- **Database changes**: Subscribe to table changes (realtime:public:table_name)
- **Presence**: Track online users (presence channel)
- **Broadcast**: Client-to-client messaging (ephemeral, not persisted)

**Client Libraries**:
- JavaScript/TypeScript (supabase-js)
- Flutter (supabase-flutter)
- Swift (supabase-swift)
- Python (supabase-py, realtime-py)

## Feature Analysis

### Database Change Streaming
- **Change types**: INSERT, UPDATE, DELETE (via Postgres triggers)
- **Filtering**: Row-level security (RLS) policies enforced
- **Granularity**: Table-level or filtered subscriptions
- **Data format**: JSON with old/new values for UPDATE
- **Latency**: Near real-time (depends on Postgres replication lag)

### Presence System
- **Phoenix Presence**: Distributed presence tracking (CRDT-based)
- **User tracking**: Online/offline status with custom metadata
- **Synchronization**: Automatic presence state sync across servers

### Broadcast (Ephemeral Messaging)
- **Client-to-client**: Direct messaging without database persistence
- **Use case**: Cursor positions, typing indicators, transient state
- **Delivery**: Best-effort, not persisted

### Advanced Features
- **Row-level security**: Database policies enforced on subscriptions
- **Postgres filters**: Filter subscriptions with SQL-like expressions
- **Multi-table subscriptions**: Listen to multiple tables simultaneously
- **Private channels**: Authenticated access with JWT tokens

## Portability Assessment

### Lock-in Risk: HIGH

**Vendor-Specific Elements**:
1. **Postgres dependency**: Tightly coupled to Postgres database (non-portable)
2. **Supabase ecosystem**: Auth, Storage, Edge Functions integration
3. **Realtime protocol**: Phoenix Channels protocol (non-standard WebSocket)
4. **Change data format**: Supabase-specific envelope structure

**Migration Path Complexity**:
- **To other managed service**: Very High (fundamentally different architecture)
- **To self-hosted Realtime**: Moderate (can self-host Supabase, but complex)
- **To generic WebSocket**: High (rebuild change streaming, lose RLS integration)
- **Database migration**: High (need Postgres, schema, RLS policies)

**Portable Elements**:
- Postgres database (standard, exportable)
- Client-side application logic (event handlers reusable)
- JWT authentication (industry standard)

### Data Portability
- **Database**: Full Postgres export (pg_dump)
- **Realtime events**: Ephemeral (not persisted by Realtime service)
- **Configuration**: Postgres RLS policies, schema migrations
- **No vendor lock for data**, but **high lock for real-time mechanism**

## Latency Benchmarks

### Vendor-Published Data

**Infrastructure** (2025):
- Hosted on AWS (multiple regions available)
- Shared infrastructure on free tier
- Dedicated compute on paid tiers

**Published Latency Targets**:
- Database change → client notification: 50-200ms (median)
- Presence updates: 100-300ms
- Broadcast messages: 30-100ms (no database involved)

**Latency factors**:
- Postgres replication lag: 10-50ms
- WAL processing: 20-100ms
- Network delivery: 20-50ms

### Community-Reported Performance

**Database Change Streaming** (typical use case):
- Median: 80-150ms (INSERT → client notification)
- P95: 200-400ms
- **Slower than direct WebSocket** due to database intermediation

**Presence System**:
- Join/leave events: 100-200ms
- Presence state sync: 150-300ms
- **Phoenix Presence overhead**: CRDT synchronization adds latency

**Broadcast Messages**:
- Median: 40-80ms (similar to Socket.io, bypasses database)
- P95: 100-200ms
- **Fastest mode** in Supabase Realtime

**Geographic Performance**:
- Single-region deployment (most Supabase projects)
- Cross-region: Not applicable (no multi-region realtime yet)
- Latency tied to Postgres region

### Performance Limitations

**Scaling challenges**:
- **Postgres bottleneck**: High write volume can delay replication
- **Connection limits**: Postgres connection pooling limits concurrent subscriptions
- **Free tier**: Shared resources, no performance guarantees

**Performance tuning**:
- Optimize Postgres queries and indexes
- Use Broadcast for ephemeral data (bypass database)
- Filter subscriptions to reduce unnecessary events
- Upgrade to dedicated compute (reduces noisy neighbor issues)

## Cost Analysis

### Pricing Model (2025)

**Free Tier**:
- 500MB database
- 2GB bandwidth/month
- 50,000 monthly active users
- Shared compute (paused after inactivity)
- Realtime included (no separate charge)

**Pro** ($25/month per project):
- 8GB database (included)
- 250GB bandwidth (included)
- No pausing
- Dedicated compute (1 CPU, 4GB RAM)
- Daily backups
- Email support

**Team** ($599/month flat fee):
- All Pro features for all projects
- Collaboration tools
- Priority support

**Enterprise** (Custom pricing):
- Custom infrastructure
- SLA, compliance (SOC2, HIPAA)
- Dedicated support

**Overages** (Pro tier):
- Database: $0.125/GB/month
- Bandwidth: $0.09/GB
- No separate Realtime charges (included with database)

### Cost Scenarios

**Scenario 1: Small Event** (1,000 concurrent, 2 hours, 20,000 messages)
- Plan: Pro ($25/month - ongoing project assumption)
- Database: Minimal (change events lightweight)
- Bandwidth: ~20MB (20K × 1KB) = negligible
- **Monthly cost**: $25 (if already using Supabase for database)
- **Realtime marginal cost**: $0 (included)

**Scenario 2: Medium SaaS Dashboard** (5,000 concurrent, 4.8M messages/day)
- Plan: Pro ($25/month base)
- Database: Depends on data retention (assume 2GB = $0.25)
- Bandwidth: ~150GB/month (4.8M/day × 1KB × 30) = $13.50 overage
- **Monthly cost**: $38.75
- **Note**: Exceptionally cheap if using Supabase database already

**Scenario 3: Large Platform** (10,000 concurrent, 72M messages/day)
- Plan: Pro or Enterprise
- Bandwidth: ~2,160GB/month = $194.40 overage
- Database: Depends on data (assume 10GB) = $1.25
- **Monthly cost**: $220 (Pro) or Enterprise negotiation
- **Risk**: May hit Postgres connection limits, need connection pooling

### Hidden Costs
- **Postgres connection limits**: May need connection pooling (pgBouncer)
- **Database writes**: If using Realtime to sync state, write costs (compute)
- **Bandwidth**: Can grow quickly with large payloads or high message volume

### Value Proposition
**Extremely cost-effective IF**:
- Already using Supabase for database
- Real-time needs are database-centric (change notifications)
- Bandwidth stays within limits

**Expensive IF**:
- Need real-time but not database-driven (paying for unused database)
- High bandwidth (overage fees accumulate)

## Operational Considerations

### Developer Experience
**Strengths**:
- Seamless integration with Supabase ecosystem
- Automatic RLS policy enforcement (security built-in)
- Simple subscription API (supabase.channel('table').on('INSERT', ...))
- Minimal backend code (database handles logic)

**Weaknesses**:
- Limited to Postgres-backed use cases
- Less flexible than general-purpose WebSocket platforms
- Debugging Postgres triggers and RLS policies complex
- Presence/Broadcast features less mature than dedicated platforms

### Scalability
**Database-bound**:
- Realtime scalability tied to Postgres write throughput
- High write volume (100K+ writes/sec) can overwhelm replication
- Connection pooling required for large concurrent user counts

**Horizontal scaling**:
- Realtime server scales automatically (managed)
- Postgres scaling: Vertical (larger instance) or read replicas (doesn't help Realtime)

**Recommended scale**: Up to 10,000 concurrent connections on Pro tier

### Monitoring & Observability
- **Supabase Dashboard**: Connection counts, bandwidth usage
- **Postgres logs**: Query performance, replication lag
- **Limited Realtime-specific metrics**: Less observability than dedicated platforms
- **No built-in latency metrics**: Manual instrumentation required

## Security & Compliance

### Authentication
- **JWT tokens**: Supabase Auth integration (OAuth, magic links, etc.)
- **Anonymous access**: Supported with RLS policies
- **Row-level security**: Database policies enforced on subscriptions

### Encryption
- **TLS in transit**: Standard on all connections
- **At-rest**: Postgres encryption (Enterprise tier)

### Compliance
- **SOC 2**: Yes (Supabase platform)
- **GDPR**: Compliant
- **HIPAA**: Enterprise tier with BAA

## Comparison to Alternatives

**vs. Pusher/Ably**:
- Supabase: Database-centric, extremely cheap if using Supabase DB, higher latency
- Pusher/Ably: General-purpose, lower latency, database-agnostic, more expensive

**vs. Socket.io**:
- Supabase: Managed, database-driven, no ops required
- Socket.io: Self-hosted, flexible, requires ops, not database-native

**vs. Firebase**:
- Supabase: Open source, Postgres-based, can self-host
- Firebase: Proprietary, NoSQL, tighter Google ecosystem lock-in

## Recommendation Context

**Best For**:
- Applications already using Supabase for database
- Database change notifications as primary real-time need
- Teams wanting minimal backend code (leverage database RLS)
- Cost-sensitive projects with database-centric real-time
- Rapid prototyping with Supabase ecosystem

**Not Ideal For**:
- Low-latency requirements (<50ms)
- Real-time needs unrelated to database (chat, multiplayer games)
- Non-Postgres databases
- Very high concurrent connection counts (>10K without Enterprise)
- Applications needing message persistence/history (not Realtime's job)

## Migration Considerations

**Exiting Supabase Realtime**:
1. Replace database change subscriptions with polling or triggers → message queue
2. Migrate Postgres to another host (or keep Supabase DB, drop Realtime)
3. Implement alternative WebSocket solution for Presence/Broadcast
4. Rebuild RLS logic in application layer (if migrating away from Postgres)
5. Update client code to new SDK

**Estimated effort**: 3-8 weeks (depends on RLS complexity, alternative platform choice)

**Entering Supabase Realtime** (from generic WebSocket):
1. Migrate database to Postgres (if not already)
2. Set up Supabase project
3. Configure RLS policies for security
4. Replace WebSocket subscription code with Supabase channels
5. Migrate presence/broadcast logic (if applicable)

**Estimated effort**: 2-4 weeks (depends on database migration needs)

## Unique Considerations

### When Supabase Realtime Shines
- **Greenfield projects**: Starting fresh with Supabase stack
- **Admin dashboards**: Showing live database changes
- **Collaborative editing**: Document changes synced via database
- **Inventory systems**: Real-time stock updates

### When It Doesn't Fit
- **High-frequency trading**: Latency too high (database intermediation)
- **Multiplayer games**: Game state not database-appropriate
- **Pure chat applications**: Database overhead unnecessary
- **Existing non-Postgres systems**: Migration cost prohibitive

## References & Resources

- Official documentation: https://supabase.com/docs/guides/realtime
- Pricing: https://supabase.com/pricing
- GitHub: https://github.com/supabase/realtime
- Self-hosting guide: https://supabase.com/docs/guides/self-hosting
- Community: Discord, GitHub Discussions, Stack Overflow
- Performance considerations: Supabase blog, community reports
