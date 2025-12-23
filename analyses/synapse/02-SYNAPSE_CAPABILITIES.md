# 02: Synapse Capabilities Unlocked

**Date**: 2025-12-22
**Status**: Deployed (verification pending)
**Updated**: 2025-12-23 - MAS patched for email claims
**Related**: ADR-021 (Synapse over Dendrite), ADR-024 (MAS patch)

---

## Why Synapse?

Dendrite was our initial choice for its lightweight footprint (~100MB RAM). However, **MAS (Matrix Authentication Service) only supports Synapse**, blocking our OIDC integration for "Login with Matrix".

The trade-off: Higher resource usage unlocks significantly more capabilities.

---

## Capabilities Gained

### 1. Full OIDC/OAuth2 Integration (MAS)

| Feature | Description | Use Case |
|---------|-------------|----------|
| **Login with Matrix** | Users authenticate once, access all services | Vikunja, future apps |
| **SSO across projects** | Single identity for all bots and services | Unified user experience |
| **OAuth2 client management** | Register apps as OIDC clients | Third-party integrations |
| **Token-based auth** | JWT tokens for API access | Bot-to-service auth |
| **Account management UI** | Self-service password reset, email, sessions | Reduced support burden |

**Immediate impact**: Vikunja users can "Login with Matrix" instead of managing separate credentials.

---

### 2. Comprehensive Admin API

| Endpoint | Capability | Use Case |
|----------|------------|----------|
| `/_synapse/admin/v1/users` | List, create, modify, deactivate users | User management automation |
| `/_synapse/admin/v1/rooms` | Room management, purge, shutdown | Moderation, cleanup |
| `/_synapse/admin/v1/media` | Media quota, purge old media | Storage management |
| `/_synapse/admin/v1/registration_tokens` | Generate invite tokens | Controlled onboarding |
| `/_synapse/admin/v1/background_updates` | Monitor DB migrations | Operations visibility |

**Immediate impact**: Automated user provisioning for bots and services.

---

### 3. Application Services (Bots at Scale)

```yaml
# appservice-registration.yaml
id: vikunja-bot
url: http://bot-service:8080
as_token: <secret>
hs_token: <secret>
sender_localpart: vikunja
namespaces:
  users:
    - exclusive: true
      regex: "@vikunja_.*:factumerit.app"
  rooms:
    - exclusive: false
      regex: "#vikunja_.*:factumerit.app"
```

| Feature | Dendrite | Synapse |
|---------|----------|---------|
| AS registration | Limited | Full support |
| Virtual users | Basic | Full (thousands) |
| Event streaming | Polling | Push + bulk |
| Room aliasing | Manual | Automated |

**Future impact**: Bots can create virtual users, manage dedicated rooms, receive events efficiently.

---

### 4. Presence & Typing Indicators

| Feature | Description |
|---------|-------------|
| Online/offline status | Users see when bots are "active" |
| Typing indicators | Bot shows "typing..." while processing |
| Read receipts | Confirm message delivery |
| Last seen | Know when user was last active |

**UX impact**: Bots feel more responsive and alive.

---

### 5. Enhanced Federation

| Feature | Dendrite | Synapse |
|---------|----------|---------|
| Server ACLs | Basic | Full control |
| Key refresh | Manual | Automated |
| Backfill | Limited | Complete history |
| State resolution | v1/v2 | v2 + edge cases |

**Platform impact**: Better interoperability with matrix.org, Element, and corporate Matrix servers.

---

### 6. Media Management

| Feature | Description |
|---------|-------------|
| Thumbnailing | Auto-generate previews |
| URL previews | Rich link cards in messages |
| Media quarantine | Block malicious uploads |
| Storage quotas | Per-user limits |
| Remote media cache | Efficient federation |

**Future impact**: QR Cards bot can share generated images with previews.

---

### 7. Widgets & Integrations

| Feature | Description |
|---------|-------------|
| Widget API | Embed web apps in rooms |
| Integration manager | Connect to bridges, bots |
| Dimension support | Self-hosted integration UI |
| Jitsi integration | Video calls in rooms |

**Future impact**: Embed dashboards, forms, or tools directly in Matrix rooms.

---

## Resource Trade-offs

| Metric | Dendrite | Synapse | Impact |
|--------|----------|---------|--------|
| RAM (idle) | 50-100 MB | 300-500 MB | May need plan upgrade |
| RAM (active) | 100-200 MB | 500 MB - 2 GB | Monitor under load |
| Startup | 2-5 sec | 10-30 sec | Slower cold starts |
| DB queries | Light | Heavy | Needs good indexes |
| Python deps | None | Full stack | Larger image (~500MB) |

**Mitigation strategies**:
- Configure Synapse worker limits
- Use connection pooling
- Enable query caching
- Monitor with Render metrics

---

## Cost Projection

| Scenario | Plan | Monthly Cost |
|----------|------|--------------|
| MVP (low traffic) | Starter (512MB) | $7 |
| Growing (moderate) | Standard (2GB) | $25 |
| Production (high) | Pro (4GB) | $85 |

Current deployment: **$14/mo** (Starter + PostgreSQL basic)

---

## New Capabilities Roadmap

### Phase 1: Foundation (In Progress)
- [x] Deploy Synapse + MAS
- [x] Discover MAS email claims bug (solutions-55jz)
- [x] Patch MAS source code for email support
- [x] Deploy patched MAS to Render
- [ ] Verify MAS userinfo returns email claims
- [/] Test Vikunja OIDC login (via Authentik - working, testing direct)

### Phase 1.5: Architecture Simplification (Pending)
- [ ] Test direct Vikunja → MAS connection (solutions-hfes)
- [ ] If successful, deprecate Authentik (save $25/mo)
- [ ] Update architecture docs with final state

### Phase 2: Enhanced Bots
- [ ] Register Application Service for task bot
- [ ] Enable presence/typing for bot UX
- [ ] Implement virtual users for multi-project

### Phase 3: Federation & Growth
- [ ] Enable federation to matrix.org
- [ ] Configure server ACLs
- [ ] Set up media storage limits

### Phase 4: Advanced Features
- [ ] Widget integration for dashboards
- [ ] Cross-project room bridging
- [ ] Admin automation via API

---

## Summary

Synapse costs more resources but unlocks:

1. **OIDC** - "Login with Matrix" for all services
2. **Admin API** - Automated user/room management
3. **App Services** - Scalable bot architecture
4. **Presence** - Responsive bot UX
5. **Federation** - Full Matrix compatibility
6. **Media** - Rich content handling
7. **Widgets** - Embedded experiences

The ~4x RAM increase is justified by the capabilities gained for a multi-project platform.

---

## Related

- [01-PLATFORM_VISION.md](./01-PLATFORM_VISION.md) - Original platform vision
- ADR-021: Synapse over Dendrite
- [Synapse Admin API Docs](https://element-hq.github.io/synapse/latest/usage/administration/admin_api/index.html)
- [MAS Documentation](https://matrix-org.github.io/matrix-authentication-service/)
