# Use Case 3: Real-Time Collaboration (Chat, Live Editing)

## Scenario Profile

**Developer**: Building real-time collaborative app
**Tech Stack**: React, Vue, or Svelte frontend
**Experience**: Web development, need real-time features
**Priority**: Low latency, concurrent users, real-time updates

## Requirements (Scoring Criteria)

1. **Real-Time Latency** (Weight: High) - Sub-100ms WebSocket latency
2. **Concurrent Connections** (Weight: High) - Support 1K+ concurrent users
3. **Real-Time Features** (Weight: High) - Presence, broadcast, database subscriptions
4. **Developer Experience** (Weight: Medium) - Easy SDK integration, good docs
5. **Cost at Scale** (Weight: Medium) - Affordable at 10K-100K concurrent connections

## Provider Scoring

| Provider | Latency | Concurrent | RT Features | DX | Cost | **Total** |
|----------|---------|------------|-------------|-----|------|-----------|
| **Supabase** | 10 | 9 | 10 | 9 | 8 | **46/50** |
| **Firebase** | 8 | 9 | 9 | 8 | 6 | **40/50** |
| **Appwrite** | 7 | 7 | 7 | 7 | 7 | **35/50** |
| **Nhost** | 8 | 8 | 8 | 7 | 7 | **38/50** |
| **PocketBase** | 5 | 6 | 5 | 6 | 9 | **31/50** |
| **Xata** | 0 | 0 | 0 | 5 | 0 | **5/50** |

## Winner: Supabase (46/50)

**Why Supabase Wins:**
- **PostgreSQL CDC:** Real-time subscriptions built on PostgreSQL replication (50-100ms latency)
- **Three real-time types:** Database changes, presence channels, broadcast channels
- **10K concurrent connections** on Pro tier (scales horizontally)
- **Excellent DX:** Simple SDK, WebSocket auto-reconnect, TypeScript support
- **Affordable:** $25/month Pro tier includes 500 connections, $0.01 per additional connection

**Use Cases:** Chat apps, collaborative editing (Notion-like), live dashboards, multiplayer games

**Lock-In:** 75/100 (moderate, real-time API is Supabase-specific but migratable to Pusher/Ably in 40-80 hours)

## Runner-Up: Firebase (40/50)

**Why Second Place:**
- **Good latency:** 100-300ms (slightly higher than Supabase)
- **Unlimited connections:** Auto-scales (Google infrastructure)
- **Firestore listeners:** Real-time database subscriptions
- **Costs explode:** Per-read pricing ($0.60 per 1M reads, 1B real-time reads = $600/month)

**When to Choose:** Mobile-first real-time apps (iOS/Android offline sync + real-time)

## Summary

**Supabase** is the best choice for real-time collaboration on web apps (50-100ms latency, PostgreSQL, affordable). **Firebase** is better for mobile real-time apps (offline sync + real-time). **Xata** has NO real-time features (not suitable).
