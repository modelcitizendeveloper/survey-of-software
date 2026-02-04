# Firebase Realtime Database & Firestore

## Overview

**Category**: Google-managed real-time database with sync
**Origin**: Firebase (acquired by Google 2014)
**Focus**: Mobile-first, offline-capable data synchronization

## Popularity Metrics

**Massive Adoption**:
- 3+ million apps use Firebase
- De facto standard for mobile real-time apps
- npm downloads: ~4M/week (firebase SDK)

**Production Usage**:
- Alibaba, Duolingo, The New York Times, Venmo
- Dominant in mobile app development

## Latency Benchmarks

**Published Numbers** (Google Cloud documentation):
- **Realtime Database**:
  - Median latency: **100-200ms** (write → sync)
  - 95th percentile: **300-500ms**
- **Firestore**:
  - Median latency: **200-300ms** (write → listener)
  - 95th percentile: **400-700ms**

**Geographic Distribution**:
- Multi-region: us-central1, europe-west1, asia-southeast1
- Cross-region sync: +100-300ms
- No edge deployment (data stored in regional clusters)

**Fan-out Performance**:
- Realtime Database: Optimized for fan-out (1 → 10K in ~200ms)
- Firestore: Not optimized for fan-out (1 → 10K in 500ms+)

**Reality Check**: Firebase optimizes for offline-first sync and data persistence, not for ultra-low-latency messaging. The database write is the bottleneck.

## Scaling Characteristics

**Realtime Database**:
- 100K concurrent connections per database instance
- 1K writes/second per database
- Multiple database sharding required for scale

**Firestore**:
- 1M concurrent connections (global)
- 10K writes/second per database
- Better scaling than Realtime Database

**Throughput Limits**:
- Realtime Database: 1K operations/sec per database
- Firestore: 10K writes/sec, 50K reads/sec

## Cost Model

**Pricing Structure** (Firestore - as of 2024):

**Spark (Free)**:
- 50K document reads/day
- 20K document writes/day
- 1GB storage
- 10GB bandwidth/month

**Blaze (Pay-as-you-go)**:
- $0.06 per 100K document reads
- $0.18 per 100K document writes
- $0.18/GB storage per month
- $0.12/GB bandwidth

**Cost Scenarios** (approximate):

**1,000 devices, 1 update/minute (24/7)**:
- Writes: 1K × 60 × 24 × 30 = 43.2M writes/month = $77.76
- Reads (each device): 1K × 60 × 24 × 30 = 43.2M reads/month = $25.92
- Storage: ~1GB = $0.18
- **Total: ~$104/month**

**5,000 devices**: ~$520/month
**10,000 devices**: ~$1,040/month

**Realtime Database Pricing**:
- $1 per GB stored
- $1 per GB downloaded
- Typically more expensive than Firestore for reads

**Hidden Costs**:
- Every listener counts as reads
- Offline clients re-sync on reconnect (burst reads)
- Bandwidth for initial data load

## Self-Hosted vs Managed

**Managed Only**: No self-hosted option (proprietary Google infrastructure)

**Trade-offs**:
- **Pro**: Zero infrastructure management, automatic scaling, global network, offline-first SDK
- **Con**: Complete vendor lock-in, no control over latency, unpredictable costs with scale, data residency in Google Cloud

## Production Validation

**Known Deployments**:
- **Duolingo**: Real-time leaderboards
- **Venmo**: Transaction feeds
- **NPR**: Live election results
- **Mobile games**: Countless real-time multiplayer games

**Community Reports**:
- Excellent mobile SDK experience
- Offline capabilities best-in-class
- Latency acceptable for mobile apps (200-500ms normal)
- Cost predictability issues at scale
- Not suitable for low-latency use cases

## Technical Architecture

**Realtime Database**:
- JSON tree structure
- WebSocket synchronization
- Optimistic local updates + server reconciliation
- No query capabilities (full tree or specific paths)

**Firestore**:
- Document-based (like MongoDB)
- Better query support
- Weaker real-time performance than Realtime Database
- More scalable architecture

**Offline-First**:
- Local cache on client
- Automatic sync when online
- Conflict resolution built-in

## Features

**Client SDKs**: JavaScript, iOS, Android, Unity, C++
**Authentication**: Firebase Auth integration (seamless)
**Security**: Declarative security rules (server-enforced)
**Offline**: Automatic local persistence and sync
**Queries**: Firestore supports complex queries; Realtime Database limited

## Limitations

**Latency Floor**:
- 100-200ms minimum (database write overhead)
- Not designed for <50ms messaging

**Vendor Lock-In**:
- Proprietary protocol and SDK
- Data migration challenging at scale

**Cost Unpredictability**:
- Per-operation pricing can explode with listeners
- Offline sync causes read bursts

**Geographic Options**:
- Limited regional choices
- No edge deployment

**Realtime Database Scaling**:
- Manual sharding required beyond 100K connections
- No automatic horizontal scaling

## Verdict for Low-Latency Use Cases

**Can Firebase achieve <50ms sync?**
- **Realtime Database**: No (100-200ms minimum)
- **Firestore**: Definitely no (200-300ms minimum)
- **Any configuration**: No (database persistence is bottleneck)

**Best For**:
- Mobile-first applications (iOS/Android)
- Offline-capable apps (critical requirement)
- Teams wanting full Firebase ecosystem (Auth, Storage, Functions)
- Prototypes needing instant backend

**Not Ideal For**:
- Low-latency requirements (<100ms)
- Cost-sensitive high-throughput apps
- Backend-first architectures (web/server-driven)
- Teams requiring data sovereignty/self-hosting
- Use cases needing pure messaging (not data sync)
