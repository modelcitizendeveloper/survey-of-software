# 21: Matrix Platform Recommendation for Factumerit

**Date**: 2025-12-22
**Status**: DECIDED
**Decision**: Self-host Dendrite on existing Render ($0 additional)
**Context**: Slack bot platform evaluation for Vikunja integration
**Research**: 3.023 Team Chat, 1.230 Open Social Networks

---

## Executive Summary

**Recommendation**: Adopt Matrix/Element as the primary communication platform for Factumerit, replacing Slack.

**Rationale**:
1. Vikunja (our task backend) uses Matrix for community - natural ecosystem fit
2. E2E encryption for privacy-conscious users
3. Bridges enable gradual migration from Slack
4. Self-hostable or managed (Element Cloud $100/mo)
5. No per-user costs at scale
6. Strong bot SDK ecosystem

---

## Decision Context

### Current State
- Slack bot proof-of-concept complete
- Bot works but mobile experience broken
- Concerns: TOS risk, gated admin API, Salesforce ick factor
- App not showing in api.slack.com/apps (bead solutions-4elo)

### Constraints
- Existing Render infrastructure ($9/mo Vikunja + $9/mo bot)
- No desire for additional $9/mo server
- 3-day decision window
- User rejected Telegram (ick factor)
- User rejected Discord (gaming ick factor for professional use)

### Requirements
- Task management bot (slash commands, interactive buttons)
- Mobile-friendly
- Low/no per-user cost
- Platform independence
- Professional positioning

---

## Why Matrix

### 1. Vikunja Ecosystem Alignment

Vikunja's official community channels:
- **Matrix**: Primary chat platform
- **Mastodon**: Social presence

This alignment means:
- Shared user base potential
- Familiar platform for Vikunja power users
- Direct line to Vikunja developers for integration questions
- Possible future native Matrix integration in Vikunja

### 2. Technical Strengths

| Feature | Matrix | Slack |
|---------|--------|-------|
| **E2E Encryption** | Yes (Megolm/Olm) | No (TLS only) |
| **Self-Hosting** | Yes (Synapse/Dendrite) | No |
| **Per-User Cost** | $0 (self-host) or $100/mo flat | $8.75/user/mo |
| **Bot SDK** | Excellent (matrix-nio, matrix-bot-sdk) | Good |
| **Bridges** | Slack, Discord, Telegram, IRC | None |
| **Admin API** | Full access | Gated (Enterprise Grid) |
| **Data Ownership** | Complete | Salesforce |

### 3. Architecture (Simplified)

Single-user deployment (no bridges needed):

```
┌─────────────────────────────────────────────────┐
│              Factumerit Matrix Room             │
│                                                 │
│       User ←→ Matrix Bot ←→ Vikunja API        │
│                                                 │
└─────────────────────────────────────────────────┘
                      │
              ┌───────▼───────┐
              │    Dendrite   │
              │   (Render)    │
              └───────────────┘
```

Note: Bridges available later if multi-platform needed (mautrix-slack, mautrix-discord).

### 4. Government/Enterprise Precedent

Matrix adoption by governments validates enterprise-readiness:
- **France**: DINUM (inter-ministry communication)
- **Germany**: Bundeswehr evaluation
- **NATO**: Exploring for sovereign infrastructure
- **UK NHS**: Healthcare trusts

### 5. Bot Development Experience

**matrix-nio (Python)** - Recommended for Vikunja bot:
```python
from nio import AsyncClient, RoomMessageText

client = AsyncClient("https://matrix.example.com", "@bot:example.com")

@client.event_callback(RoomMessageText)
async def message_callback(room, event):
    if event.body.startswith("/tasks"):
        tasks = await vikunja_api.get_tasks(event.sender)
        await client.room_send(
            room.room_id,
            "m.room.message",
            {"msgtype": "m.text", "body": format_tasks(tasks)}
        )

await client.sync_forever()
```

**Time to MVP**: 4-8 hours (vs 4-8 hours for Slack)
**Complexity**: Similar to Slack bot development

---

## Implementation Plan

### Phase 1: Setup (Day 1)

1. **Choose hosting**:
   - Option A: Element Cloud ($100/mo, managed)
   - Option B: Self-host Dendrite on existing Render ($0 additional)

2. **Create Factumerit space**:
   - #general
   - #tasks (bot commands)
   - #announcements

3. **Port existing bot**:
   - Replace Slack SDK with matrix-nio
   - Same Vikunja API integration
   - Same command structure

### Phase 2: Bridge (Day 2)

1. **Setup mautrix-slack bridge** (if keeping Slack users):
   - Connect existing Slack workspace
   - Map channels to rooms
   - Test bidirectional messaging

2. **Test bot commands** through bridge:
   - Verify /tasks works from Slack side
   - Verify responses appear in both

### Phase 3: Migration (Day 3+)

1. **Invite users to Matrix**:
   - Existing Slack users see Matrix messages via bridge
   - New users join Matrix directly

2. **Gradual Slack sunset**:
   - Keep bridge running 30-60 days
   - Monitor adoption
   - Sunset Slack when <10% traffic

---

## Hosting Decision

**Decision**: Self-host Dendrite on existing Render

**Why Dendrite**:
- $0 additional cost (use existing Render allocation)
- Full data control
- Lighter than Synapse (Go vs Python)
- Good for single-user/small deployments

**Render deployment**:
- Add Dendrite as new service (~256MB RAM)
- PostgreSQL: share existing or add free tier
- Persistent disk for media (optional)

**Not considered**:
- Element Cloud ($100/mo) - over budget
- matrix.org (free) - no custom domain, no SLA

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Users resist migration | Medium | High | Bridge enables gradual transition |
| Matrix UX confuses users | Medium | Medium | Provide onboarding guide |
| Dendrite stability issues | Low | High | Start with Element Cloud |
| Bridge breaks | Low | Medium | Direct Matrix access works |
| Element company fails | Very Low | Low | Protocol survives, self-host |

---

## Cost Comparison

| Platform | Monthly | Notes |
|----------|---------|-------|
| **Current Slack** | $0 | Free tier, limited |
| **Dendrite (self-host)** | $0 | Existing Render allocation |
| **Element Cloud** | $100 | Not considered |

**Result**: $0 additional cost for Matrix migration

---

## Decision

**Decided Path**:

1. **Week 1**: Self-host Dendrite on existing Render
   - $0 additional cost
   - Full data control
   - Deploy alongside existing Vikunja + bot services

2. **Week 2**: Port bot to matrix-nio
   - Replace Slack SDK with matrix-nio
   - Same Vikunja API integration
   - Test E2EE verification flow

3. **Week 3+**: Go live on Matrix
   - No bridge needed (single Slack user migrates directly)
   - Decommission Slack bot

---

## Next Steps

1. [ ] Deploy Dendrite on Render
2. [ ] Create Factumerit space structure (#general, #tasks)
3. [ ] Port Slack bot to matrix-nio
4. [ ] Test E2EE device verification
5. [ ] Go live, decommission Slack

---

## Related Documents

- [3.023 Team Chat Research](../../research/3.023-team-chat/)
- [1.230 Open Social Networks Research](../../research/1.230-open-social-networks/)
- [21-SLACKBOT_EFFICIENCY_OPPORTUNITIES.md](21-SLACKBOT_EFFICIENCY_OPPORTUNITIES.md)
- [20-BEADS_VIKUNJA_SYNC_OPPORTUNITIES.md](20-BEADS_VIKUNJA_SYNC_OPPORTUNITIES.md)

---

## Sources

- Matrix.org specification
- Element Cloud pricing
- Vikunja community channels
- 3.023 and 1.230 MPSE research
