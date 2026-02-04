# Supabase Realtime: Postgres-Integrated WebSocket Service

**Provider Type:** Managed Service (Postgres-Integrated)
**Date Reviewed:** December 3, 2025
**Category:** Database-Centric Real-Time Platform

## Overview

Supabase Realtime is a WebSocket server built with Elixir/Phoenix that provides three capabilities: Broadcast (ephemeral messaging), Presence (shared state tracking), and Postgres Changes (database change notifications). Tightly integrated with Supabase's Postgres database platform.

## Pricing Model

**Free Tier:**
- Generous limits for personal projects and MVPs
- Includes real-time messaging with quota limits
- 6 months duration for new accounts

**Paid Tiers:**
- **Messages:** $2.50 per 1 million messages (above quota)
- **Connections:** $10 per 1,000 peak concurrent connections (above quota)

**Pricing Philosophy:** Simple flat-rate pricing. Pay only for usage exceeding plan quotas. No complex tier structures or overage penalties.

**Cost Example:**
- 5M messages/month above quota: $12.50
- 3K peak connections above quota: $30
- Total overage: $42.50

**Advantage:** Predictable, transparent pricing. Among the cheapest managed WebSocket services for small-to-medium scale.

## Performance Characteristics

**Latency:**
- Built on Phoenix Framework (Elixir) - known for low latency
- Global distribution (CDN-like edge presence)
- No specific latency guarantees published

**Infrastructure:**
- Elixir/Phoenix backend (excellent concurrency characteristics)
- Globally distributed network
- Postgres-native change detection (no polling overhead)

**Scalability:**
- Phoenix handles millions of concurrent connections efficiently
- Designed for real-time database synchronization at scale

## Connection Limits

**Free Tier:** Quota-based (varies by plan)
**Paid Tiers:** $10 per 1,000 peak concurrent connections above quota
**No Hard Limits:** Scales with pricing

**Peak Connection Pricing:** Only charged for highest concurrent connection count in billing period (not total connections).

## Key Differentiator

**Postgres Change Streams + Real-Time Messaging**

Supabase's unique value is tight Postgres integration:

**Postgres Changes Feature:**
- Listen to database INSERT, UPDATE, DELETE events
- Row-level security applied to real-time subscriptions
- Automatic WebSocket push when database changes
- No manual publish/subscribe logic needed

**Broadcast Feature:**
- Ephemeral channel-based messaging (like Pusher/Socket.io)
- Low-latency message delivery
- Event filtering and flexible payloads

**Presence Feature:**
- Track online users and shared state
- Synchronize presence across clients
- Built-in conflict resolution

**Trade-off:** Best value when using Supabase Postgres. Standalone WebSocket use may find better alternatives.

## Strengths

- Lowest cost managed WebSocket service (for typical usage)
- Postgres change streams eliminate polling overhead
- Unified platform (database + real-time + auth + storage)
- Row-level security on real-time subscriptions
- Generous free tier for prototyping
- Simple, transparent pricing
- Open-source (self-hostable if needed)

## Limitations

- Best value only within Supabase ecosystem
- Postgres dependency (not general-purpose WebSocket server)
- Less mature than Pusher/Ably (newer platform)
- Limited enterprise features (SLAs, compliance certifications)
- Documentation emphasizes Supabase-first workflows

## Typical Use Cases

- Real-time dashboards showing live database data
- Chat applications with message persistence (Postgres storage)
- Collaborative tools syncing state via database
- Live notifications triggered by database changes
- Multiplayer games with game state in Postgres
- Activity feeds and user presence indicators
- Any application needing both database + WebSocket

## When to Choose Supabase Realtime

**Best fit when:**
- Already using (or planning to use) Supabase Postgres
- Need database change notifications over WebSocket
- Want unified platform (database + real-time + auth)
- Budget-conscious (cheapest managed option)
- Prototyping or MVP development (generous free tier)
- Open to Postgres-centric architecture

**Consider alternatives when:**
- Need general-purpose WebSocket (no database dependency)
- Require enterprise SLAs and compliance (HIPAA, SOC 2)
- Already invested in different database (not Postgres)
- Need maximum global performance (Ably's edge network)
- Self-hosted preferred without Postgres dependency

## Competitive Position

Supabase Realtime competes with:
- **Pusher:** Supabase cheaper, Pusher more mature, no database integration
- **Ably:** Ably has enterprise features, Supabase has Postgres integration
- **Socket.io:** Socket.io self-hosted, Supabase managed + Postgres
- **Firebase Realtime Database:** Similar database-centric model, different stack

## Unique Architecture

**Elixir/Phoenix Framework:**
- Functional programming language built on Erlang VM
- Legendary concurrency (millions of processes)
- Fault-tolerant supervision trees
- Battle-tested in telecom industry

**Protocol Support:**
- WebSocket (primary transport)
- JSON serialization (simple text frames)
- Versions 1.0.0 and 2.0.0 supported

---

**Summary:** Supabase Realtime offers the best value for Postgres-centric applications needing database change streams over WebSocket. The tight integration eliminates boilerplate publish/subscribe code and provides the lowest cost managed option. Choose when Postgres is your database; evaluate alternatives if you need general-purpose WebSocket without database dependency.
