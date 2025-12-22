# S2 Comprehensive Discovery: Open Social Networks Feature Matrix

**Date**: 2025-12-22
**Methodology**: S2 - Comprehensive multi-provider comparison
**Category**: 1.230 (Open Social Networks & Protocols)

## Protocol Comparison Matrix

### Identity & Architecture

| Feature | ActivityPub | AT Protocol | Matrix | Nostr |
|---------|-------------|-------------|--------|-------|
| **Identity Model** | Server-based (@user@domain) | DIDs (portable) | Server-based (@user:domain) | Cryptographic keys (pubkey) |
| **Identity Portability** | Limited (followers don't migrate) | Full (DID survives PDS change) | Limited (but bridges help) | Full (key works everywhere) |
| **Architecture** | Federated servers | Client-server + relay | Federated homeservers | Client-relay |
| **Decentralization** | Moderate | Moderate (single relay now) | Moderate | High |
| **Self-Hosting** | Yes (any instance) | Yes (PDS, complex) | Yes (homeserver) | Yes (relay, easy) |
| **W3C Standard** | Yes (2018) | No | No | No |

### Federation & Interoperability

| Feature | ActivityPub | AT Protocol | Matrix | Nostr |
|---------|-------------|-------------|--------|-------|
| **Federation Status** | Production | Not yet (Q1-Q2 2025) | Production | N/A (relays) |
| **Cross-Platform** | Good (Mastodon↔Pixelfed) | N/A | Good (bridges) | N/A |
| **Bridge Ecosystem** | None needed | None | Excellent (Slack, Discord, Telegram, IRC) | None |
| **Protocol Simplicity** | Complex (JSON-LD, signatures) | Moderate | Complex (DAG, state resolution) | Simple |

### Encryption & Security

| Feature | ActivityPub | AT Protocol | Matrix | Nostr |
|---------|-------------|-------------|--------|-------|
| **E2E Encryption** | No | No | Yes (Megolm/Olm) | No (plaintext to relays) |
| **Message Signing** | HTTP Signatures (RSA) | EdDSA | Events signed | Schnorr (secp256k1) |
| **Key Recovery** | Server-dependent | Built-in (recovery keys) | Device-based | None (user responsibility) |
| **Censorship Resistance** | Moderate (instance-dependent) | Moderate | Moderate | Strong |

### Content Features

| Feature | ActivityPub | AT Protocol | Matrix | Nostr |
|---------|-------------|-------------|--------|-------|
| **Text Posts** | Yes | Yes | Yes | Yes |
| **Media Sharing** | Yes | Yes (limited) | Yes | Yes |
| **Long-form Content** | Varies by platform | Yes | Yes | Yes (kind 23) |
| **Threading** | Yes | Yes | Yes | Yes |
| **Reactions** | Varies | Yes | Yes | Yes |
| **Direct Messages** | Varies | Limited (beta) | Yes (E2EE) | Yes (NIP-17) |

### Ecosystem

| Feature | ActivityPub | AT Protocol | Matrix | Nostr |
|---------|-------------|-------------|--------|-------|
| **Active Users** | ~10 million | ~15-20 million | ~3-5 million | ~1.18 million |
| **Platforms/Clients** | 48+ (Mastodon, Lemmy, etc.) | 1 main (Bluesky) + clients | 5+ homeservers, 10+ clients | 140+ clients |
| **Instance/Relay Count** | 27,000+ | Single relay (now) | Unknown (federated) | 800+ |
| **Library Support** | Excellent (Ruby, Python, Go, JS) | Good (TypeScript, Go) | Excellent (JS, Rust, Python) | Good (JS, Rust, Python) |

### Payments & Economics

| Feature | ActivityPub | AT Protocol | Matrix | Nostr |
|---------|-------------|-------------|--------|-------|
| **Native Payments** | No | No | No | Yes (Lightning zaps) |
| **Creator Monetization** | None built-in | None built-in | None built-in | Native (zaps) |
| **Spam Prevention** | Instance moderation | Unknown | Homeserver moderation | Paid relays, proof-of-work |
| **Running Costs** | Server hosting | PDS hosting | Homeserver hosting | Relay hosting |

### Developer Experience

| Feature | ActivityPub | AT Protocol | Matrix | Nostr |
|---------|-------------|-------------|--------|-------|
| **Spec Documentation** | Good (W3C) | Improving | Good | Good (NIPs) |
| **SDK Quality** | Variable by language | Good (TypeScript) | Excellent | Good |
| **Time to MVP** | 2-6 months | 2-4 weeks | 4-16 hours (bot) | 2-4 hours |
| **Learning Curve** | Steep | Moderate | Moderate | Low |

---

## Platform Scores (1-5 scale)

| Criteria | ActivityPub | AT Protocol | Matrix | Nostr |
|----------|-------------|-------------|--------|-------|
| **Decentralization** | 3 | 2 | 3 | 5 |
| **User Privacy** | 3 | 3 | 5 | 3 |
| **Censorship Resistance** | 3 | 3 | 3 | 5 |
| **Developer Experience** | 3 | 4 | 4 | 5 |
| **User Experience** | 4 | 4 | 3 | 2 |
| **Maturity** | 5 | 3 | 4 | 3 |
| **Ecosystem Size** | 5 | 4 | 3 | 2 |
| **Interoperability** | 4 | 2 | 5 | 1 |
| **Self-Hosting Ease** | 3 | 2 | 3 | 4 |
| **Payments** | 1 | 1 | 1 | 5 |
| **TOTAL** | **34** | **28** | **34** | **35** |

---

## Use Case Fit Matrix

| Use Case | ActivityPub | AT Protocol | Matrix | Nostr |
|----------|-------------|-------------|--------|-------|
| **Task Management Bot** | Medium | Low | High | Medium |
| **Public Community** | High | Medium | Medium | Medium |
| **Private Team Chat** | Low | Low | High | Low |
| **Creator Economy** | Low | Low | Low | High |
| **Privacy-First** | Medium | Medium | High | Medium |
| **Mobile-First** | Medium | High | Medium | Medium |
| **Enterprise** | Medium | Low | High | Low |
| **Self-Hosted** | High | Low | High | High |

---

## Recommendation by Priority

| If You Value... | Choose |
|-----------------|--------|
| **Largest network** | ActivityPub (Mastodon) |
| **Best UX** | AT Protocol (Bluesky) |
| **E2E Encryption** | Matrix |
| **Censorship resistance** | Nostr |
| **Platform bridges** | Matrix |
| **Micropayments** | Nostr |
| **Standards compliance** | ActivityPub |
| **Simplest implementation** | Nostr |
| **Team chat replacement** | Matrix |
| **Twitter alternative** | AT Protocol or ActivityPub |

---

## Sources

- Individual S1 research documents (1.230-1.233)
- Protocol specifications
- Ecosystem documentation
