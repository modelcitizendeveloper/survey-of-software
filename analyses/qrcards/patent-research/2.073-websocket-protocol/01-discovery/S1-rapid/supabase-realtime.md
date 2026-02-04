# Supabase Realtime

## Overview

**Category**: Postgres-based real-time messaging
**Origin**: Elixir-based server (inspired by Phoenix Channels)
**Focus**: Database change streaming + broadcast channels

## Popularity Metrics

**Adoption**:
- Part of Supabase ecosystem (200K+ projects)
- GitHub stars: ~8K (realtime repository standalone)
- Tight integration with Postgres makes it popular for database-driven apps

**Production Usage**:
- Used by Supabase platform users
- Growing adoption in full-stack JavaScript ecosystem

## Latency Benchmarks

**Published Numbers** (Supabase documentation):
- Median latency: **100-200ms** (Postgres CDC events)
- Broadcast channel: **50-100ms** (direct WebSocket)
- Presence: **50-100ms**

**Postgres CDC Overhead**:
- Logical replication: +30-50ms
- Trigger-based: +50-100ms
- Row-level security checks: +10-50ms

**Fan-out Performance**:
- Limited public benchmarks available
- Elixir BEAM VM generally efficient at fan-out
- Estimated: 1 → 1,000 subscribers in 80-150ms

**Reality Check**: Database change events inherently slower than direct messaging due to:
1. Database write latency
2. Replication lag
3. Change detection overhead

## Scaling Characteristics

**Connection Limits**:
- Free tier: 200 concurrent connections
- Pro: 2,000 concurrent connections (can be increased)
- Self-hosted: Limited by server resources

**Postgres CDC Limitations**:
- Replication slot overhead
- Increased database load with many subscribers
- WAL (Write-Ahead Log) size grows with lag

**Throughput**:
- Broadcast channels: High throughput (1,000+ msg/sec)
- Database changes: Limited by Postgres write speed

## Cost Model

**Managed (Supabase Cloud)**:

**Free Tier**:
- 200 concurrent connections
- 2GB database
- $0/month

**Pro ($25/month)**:
- 2,000 concurrent connections
- 8GB database
- Includes database, auth, storage, realtime

**Team ($599/month)**:
- 5,000+ concurrent connections
- Higher compute resources

**Cost Scenarios**:
- **1,000 devices**: $25/month (if database fits in Pro tier)
- **5,000 devices**: $599/month
- **10,000 devices**: Custom enterprise pricing

**Note**: Cost includes entire Supabase backend (database, auth, storage), not just realtime.

**Self-Hosted Costs**:
- Server: $50-200/month (depending on scale)
- Postgres: $30-100/month (managed) or included in same server
- **Total: $50-300/month** (but requires DevOps expertise)

## Self-Hosted vs Managed

**Open Source**: Fully self-hostable (Apache 2.0 license)

**Trade-offs**:
- **Managed Pro**: Includes full backend stack, easy scaling, managed Postgres
- **Self-Hosted Pro**: Full control, lower cost at scale, requires Elixir/Postgres expertise
- **Managed Con**: Limited customization, connection limits per tier
- **Self-Hosted Con**: Need to manage Postgres + Elixir cluster

## Production Validation

**Known Deployments**:
- Primarily Supabase platform users
- Growing presence in Next.js/React ecosystem
- Limited public case studies at >10K connections

**Community Reports**:
- Excellent for database-driven apps (natural fit)
- CDC latency acceptable for most use cases
- Connection scaling concerns raised occasionally
- Elixir/BEAM reliability praised

## Technical Architecture

**Server**: Elixir (Phoenix Channels pattern)
**Database**: Postgres with logical replication
**Protocol**: WebSocket (with Phoenix protocol)

**Three Channel Types**:

1. **Broadcast**: Direct pub/sub (like Socket.IO rooms)
   - Lowest latency
   - Server-memory based

2. **Presence**: User presence tracking
   - Built into Phoenix Channels
   - CRDT-based synchronization

3. **Postgres Changes**: Database CDC
   - Listens to WAL (Write-Ahead Log)
   - Row-level security enforced
   - Highest latency (database overhead)

## Features

**Postgres Integration**:
- Subscribe to INSERT/UPDATE/DELETE
- Row-level security applied to subscriptions
- Filter by table, schema, column values

**Authorization**:
- JWT-based authentication
- RLS (Row Level Security) policies enforced
- User-level filtering built-in

**Elixir BEAM Benefits**:
- Excellent concurrency model
- Fault tolerance (supervision trees)
- Hot code reloading

## Limitations

**Postgres CDC Latency**:
- Not suitable for ultra-low-latency (<50ms)
- Database events 2-5x slower than direct broadcast

**Connection Limits**:
- Tied to Postgres connection pooling
- Each realtime server connection consumes Postgres resources

**Protocol Lock-In**:
- Phoenix Channels protocol (not standard WebSocket)
- Requires Supabase client library

**Scaling Complexity**:
- Self-hosted clustering requires Elixir expertise
- Postgres replication adds operational complexity

## Verdict for Low-Latency Use Cases

**Can Supabase Realtime achieve <50ms sync?**
- **Broadcast channels, same region**: Possible (50-100ms)
- **Postgres CDC**: No (100-200ms minimum)
- **Cross-region**: No (network + database lag)
- **Large fan-out**: Unknown (limited benchmarks)

**Best For**:
- Database-centric applications (changes feed critical)
- Full-stack JavaScript/TypeScript projects using Supabase
- Teams wanting integrated backend (DB + auth + realtime)
- Applications where 100-200ms latency is acceptable

**Not Ideal For**:
- Ultra-low-latency requirements (<50ms)
- Non-database event sources
- Teams not using Postgres
- Applications needing proven >10K connection scaling
