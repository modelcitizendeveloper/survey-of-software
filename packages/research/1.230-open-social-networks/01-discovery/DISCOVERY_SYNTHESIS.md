# 1.230 Open Social Networks & Protocols - Discovery Synthesis

**Date**: 2025-12-22
**Status**: S1-S4 Complete
**Category**: 1.230 (Self-Operated Tools - Open Social Networks)

## Executive Summary

Open social network protocols provide decentralized alternatives to proprietary platforms. Four major protocols dominate the landscape:

1. **ActivityPub** (W3C standard) - Largest network (~10M users), federated servers, powers Mastodon/Fediverse
2. **AT Protocol** (Bluesky) - Best UX (~15-20M users), portable identities, federation coming 2025
3. **Matrix** - E2E encrypted team chat, excellent bridges, government adoption
4. **Nostr** - Simplest protocol, native payments (Lightning), strongest censorship resistance

**Key Finding**: No single protocol dominates all use cases. Protocol choice depends on: encryption requirements, payment needs, network size priority, and self-hosting requirements.

## Discovery Documents

| Phase | Document | Key Deliverable |
|-------|----------|-----------------|
| S1 | [1.230-activitypub.md](S1-rapid/1.230-activitypub.md) | ActivityPub deep-dive |
| S1 | [1.231-atprotocol-bluesky.md](S1-rapid/1.231-atprotocol-bluesky.md) | AT Protocol deep-dive |
| S1 | [1.232-matrix-protocol.md](S1-rapid/1.232-matrix-protocol.md) | Matrix deep-dive |
| S1 | [1.233-nostr.md](S1-rapid/1.233-nostr.md) | Nostr deep-dive |
| S2 | [feature-matrix.md](S2-comprehensive/feature-matrix.md) | Protocol comparison |
| S3 | [business-scenarios.md](S3-need-driven/business-scenarios.md) | Use case implementations |
| S4 | [vendor-viability.md](S4-strategic/vendor-viability.md) | 5-10 year outlook |

## Top-Line Recommendations

### By Use Case

| Use Case | Recommended | Runner-up |
|----------|-------------|-----------|
| Task management bot | Matrix | Nostr |
| Public community | ActivityPub | AT Protocol |
| Privacy-first chat | Matrix | - |
| Creator monetization | Nostr | - |
| Twitter alternative | AT Protocol | ActivityPub |
| Self-hosted social | ActivityPub | Matrix |
| Platform bridges | Matrix | - |

### By Priority

| Priority | Recommended |
|----------|-------------|
| Encryption | Matrix |
| Largest network | ActivityPub |
| Best UX | AT Protocol |
| Micropayments | Nostr |
| Simplest implementation | Nostr |
| Platform bridges | Matrix |
| W3C standard | ActivityPub |
| Censorship resistance | Nostr |

## Protocol Summary Cards

### ActivityPub (1.230)
- **Strength**: W3C standard, largest network (10M users), 27K+ instances
- **Weakness**: Moderation complexity, no encryption, instance fragmentation
- **Best for**: Public communities, Twitter alternatives
- **Avoid if**: Need encryption, need payments

### AT Protocol / Bluesky (1.231)
- **Strength**: Best UX, portable identities, clean API
- **Weakness**: Single company control, federation not yet enabled
- **Best for**: Consumer social networking, Twitter migration
- **Avoid if**: Need full decentralization now

### Matrix (1.232)
- **Strength**: E2E encryption, excellent bridges, government adoption
- **Weakness**: Resource-intensive (Synapse), complexity
- **Best for**: Privacy-first teams, bridging legacy platforms
- **Avoid if**: Need social networking features

### Nostr (1.233)
- **Strength**: Simplest protocol, native Lightning payments, censorship-resistant
- **Weakness**: Key management UX, smaller network (1.18M active)
- **Best for**: Creator economy, Bitcoin community, censorship resistance
- **Avoid if**: Need mainstream UX, need encryption

## Strategic Insights

### 5-Year Survival Probability

| Protocol | 5-Year | 10-Year | Rationale |
|----------|--------|---------|-----------|
| ActivityPub | 99% | 99% | W3C standard, massive adoption |
| Matrix | 99% | 95% | Open protocol, government backing |
| Nostr | 95% | 90% | Simple protocol, Dorsey funding |
| AT Protocol | 90% | 80% | Bluesky-dependent |

### Protocol Independence Score

1. **Nostr** ⭐⭐⭐⭐⭐ - Self-sovereign keys, works everywhere
2. **Matrix** ⭐⭐⭐⭐⭐ - Open protocol, bridges, federation
3. **ActivityPub** ⭐⭐⭐⭐ - W3C standard, but instance-dependent
4. **AT Protocol** ⭐⭐⭐ - Portable DIDs, Bluesky-dominated

## Next Steps

### For Application-Specific Analysis

This research is "hardware store" (generic). For project-specific decisions:

1. Map project requirements to S3 scenarios
2. Score protocols against specific needs
3. Build proof-of-concept on top 2 candidates
4. Evaluate migration/exit strategy

### Related Research

- **3.023**: Team Chat & Collaboration Platforms (Slack, Discord, Matrix managed)
- **1.132**: Self-hosted collaboration (Mattermost, Rocket.Chat)
- **2.074-079**: AI Agent Communication Standards (MCP, A2A)

## Sources

All sources documented in individual S1-S4 documents. Key references:
- [ActivityPub W3C Specification](https://www.w3.org/TR/activitypub/)
- [AT Protocol Documentation](https://docs.bsky.app)
- [Matrix.org](https://matrix.org/)
- [Nostr Protocol](https://nostr.com/)
