# S2 Comprehensive Discovery: Team Chat Feature Matrix

**Date**: 2025-12-22
**Methodology**: S2 - Feature-by-feature comparison across providers
**Category**: 3.023 (Managed Services)

## Bot API Capabilities

### Core Messaging Features

| Feature | Slack | Discord | Telegram | Matrix | Mattermost |
|---------|-------|---------|----------|--------|------------|
| Send messages | ✅ | ✅ | ✅ | ✅ | ✅ |
| Rich text/Markdown | ✅ mrkdwn | ✅ Markdown | ✅ Markdown/HTML | ✅ Markdown | ✅ Markdown |
| File attachments | ✅ | ✅ 25MB (500MB Nitro) | ✅ 2GB | ✅ | ✅ |
| Reactions/Emoji | ✅ | ✅ | ✅ | ✅ | ✅ |
| Threads | ✅ | ✅ Forum channels | ❌ Reply-to only | ✅ | ✅ |
| Edit messages | ✅ | ✅ | ✅ | ✅ | ✅ |
| Delete messages | ✅ | ✅ | ✅ | ✅ (redaction) | ✅ |
| Message scheduling | ✅ | ❌ | ✅ | ❌ | ❌ |

### Interactive Components

| Feature | Slack | Discord | Telegram | Matrix | Mattermost |
|---------|-------|---------|----------|--------|------------|
| Buttons | ✅ Block Kit | ✅ Components | ✅ Inline keyboards | ✅ Widgets | ✅ |
| Select menus | ✅ | ✅ | ✅ | ⚠️ Limited | ✅ |
| Text inputs | ✅ Modals | ✅ Modals | ❌ | ❌ | ✅ |
| Date pickers | ✅ | ❌ | ✅ | ❌ | ❌ |
| Multi-select | ✅ | ✅ | ❌ | ❌ | ✅ |
| Modals/Dialogs | ✅ | ✅ | ❌ | ❌ | ✅ |
| Ephemeral messages | ✅ | ✅ | ❌ | ❌ | ✅ |

### Command & Event Handling

| Feature | Slack | Discord | Telegram | Matrix | Mattermost |
|---------|-------|---------|----------|--------|------------|
| Slash commands | ✅ | ✅ | ✅ /command | ✅ !command | ✅ |
| Command autocomplete | ✅ | ✅ | ✅ | ⚠️ Client-dependent | ✅ |
| Webhooks (incoming) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Webhooks (outgoing) | ✅ | ❌ | ❌ | ⚠️ Via appservice | ✅ |
| Event subscriptions | ✅ Events API | ✅ Gateway/HTTP | ✅ Webhooks | ✅ Sync API | ✅ |
| Real-time events | ✅ Socket Mode | ✅ Gateway | ✅ Long polling/WH | ✅ Sync | ✅ WebSocket |
| HTTP-only mode | ✅ | ✅ Interactions | ✅ Webhooks | ❌ | ✅ |

### User & Channel Management

| Feature | Slack | Discord | Telegram | Matrix | Mattermost |
|---------|-------|---------|----------|--------|------------|
| List users | ✅ | ✅ | ⚠️ Group members | ✅ | ✅ |
| List channels | ✅ | ✅ | ❌ | ✅ | ✅ |
| Create channels | ⚠️ Scopes | ✅ | ✅ Groups | ✅ | ✅ |
| Join/Leave channels | ✅ | ✅ | ✅ | ✅ | ✅ |
| Invite users | ⚠️ Scopes | ✅ | ✅ | ✅ | ✅ |
| Kick/Ban users | ⚠️ Scopes | ✅ | ✅ | ✅ | ✅ |
| User presence | ✅ | ✅ | ❌ | ✅ | ✅ |
| User profiles | ✅ | ✅ | ✅ | ✅ | ✅ |

### Advanced Features

| Feature | Slack | Discord | Telegram | Matrix | Mattermost |
|---------|-------|---------|----------|--------|------------|
| Voice/Video calls | ✅ Huddles | ✅ Native | ✅ | ✅ VoIP/Jitsi | ✅ |
| Screen sharing | ✅ | ✅ | ❌ | ✅ | ✅ |
| Mini Apps/Embeds | ✅ Workflow Builder | ❌ | ✅ Mini Apps | ✅ Widgets | ✅ Plugins |
| Payments | ❌ | ❌ | ✅ Telegram Stars | ❌ | ❌ |
| Bot mentions | ✅ @bot | ✅ @bot | ✅ @bot | ✅ @bot:server | ✅ @bot |
| DM with users | ✅ | ✅ | ✅ | ✅ | ✅ |

## Authentication & Security

| Feature | Slack | Discord | Telegram | Matrix | Mattermost |
|---------|-------|---------|----------|--------|------------|
| OAuth 2.0 | ✅ | ✅ | ❌ (token only) | ✅ | ✅ |
| Bot tokens | ✅ | ✅ | ✅ | ✅ | ✅ |
| User tokens | ✅ | ✅ | ❌ | ✅ | ✅ |
| Webhook secrets | ✅ Signing | ✅ Signature | ✅ Secret token | N/A | ✅ |
| E2E encryption | ❌ | ❌ | ⚠️ Secret chats | ✅ Megolm | ⚠️ Enterprise |
| SSO/SAML | ✅ Enterprise | ❌ | ❌ | ✅ | ✅ |
| 2FA enforcement | ✅ | ✅ | ✅ | ✅ | ✅ |

## Platform & Infrastructure

| Feature | Slack | Discord | Telegram | Matrix | Mattermost |
|---------|-------|---------|----------|--------|------------|
| Self-hostable | ❌ | ❌ | ❌ | ✅ | ✅ |
| Open source | ❌ | ❌ | ❌ (clients only) | ✅ | ✅ |
| Open protocol | ❌ | ❌ | ❌ | ✅ | ❌ |
| Federation | ❌ | ❌ | ❌ | ✅ | ❌ |
| Data export | ✅ | ✅ | ✅ | ✅ | ✅ |
| API rate limits | 1 req/sec (tier 1) | 50/sec global | 30 msg/sec | Server-dependent | Configurable |
| Uptime SLA | 99.99% (Enterprise) | 99.9% | None published | Self-managed | Self-managed |

## SDK & Developer Experience

| Feature | Slack | Discord | Telegram | Matrix | Mattermost |
|---------|-------|---------|----------|--------|------------|
| Official Python SDK | ✅ slack-sdk | ❌ (community) | ✅ python-telegram-bot | ✅ matrix-nio | ✅ |
| Official JS/TS SDK | ✅ @slack/bolt | ✅ discord.js | ❌ (community) | ✅ matrix-bot-sdk | ✅ |
| Official Go SDK | ✅ | ❌ | ❌ | ✅ | ✅ |
| Official Rust SDK | ❌ | ❌ | ❌ | ✅ matrix-rust-sdk | ❌ |
| Interactive playground | ✅ Block Kit Builder | ❌ | ❌ | ❌ | ❌ |
| Documentation quality | Excellent | Excellent | Excellent | Good | Good |
| Example bots | ✅ | ✅ | ✅ | ✅ | ✅ |

## Pricing Comparison

### Per-User Pricing (Business/Team Plans)

| Provider | Free Tier | Paid (per user/month) | Notes |
|----------|-----------|----------------------|-------|
| **Slack** | 90-day history, 10 integrations | $8.75-15 | Enterprise Grid for admin APIs |
| **Discord** | Full features | N/A (free) | Nitro $10/month (cosmetic) |
| **Telegram** | Full features | N/A (free) | Premium $5/month (cosmetic) |
| **Matrix** | Self-host free | Element Pro ~$5 | Or self-host Synapse |
| **Mattermost** | Self-host free | $10 (Pro) | Enterprise custom |
| **Teams** | Limited | $4-12.50 | Usually bundled with M365 |

### Bot/API Costs

| Provider | API Access Cost | Rate Limit Upgrades | Notes |
|----------|-----------------|---------------------|-------|
| **Slack** | Free | Enterprise only | App Directory listing requires review |
| **Discord** | Free | Verified bot status | >100 servers requires verification |
| **Telegram** | Free | 30 msg/sec base, paid for more | Broadcast >30/sec costs 0.1 Stars/msg |
| **Matrix** | Free | Server-dependent | Self-host = no limits |
| **Mattermost** | Free | Configurable | Self-host = no limits |

## Mobile Experience

| Feature | Slack | Discord | Telegram | Matrix (Element) | Mattermost |
|---------|-------|---------|----------|------------------|------------|
| iOS app quality | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Android app quality | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Push notifications | ✅ | ✅ | ✅ | ✅ | ✅ |
| Offline support | ⚠️ Limited | ⚠️ Limited | ✅ | ⚠️ Limited | ⚠️ Limited |
| Bot interactions | ✅ | ✅ | ✅ | ✅ | ✅ |

## Bridging Capabilities (Matrix-specific)

Matrix can bridge to other platforms, enabling multi-platform bots:

| Bridge Target | Maturity | Features Supported |
|---------------|----------|-------------------|
| Slack | ✅ Stable | Messages, reactions, threads |
| Discord | ✅ Stable | Messages, reactions, embeds |
| Telegram | ✅ Stable | Messages, media, reactions |
| IRC | ✅ Stable | Messages |
| WhatsApp | ⚠️ Beta | Messages, media (via mautrix) |
| Signal | ⚠️ Beta | Messages, media (via mautrix) |
| SMS | ⚠️ Beta | Messages (via bridges) |

## Sources

- [Slack API Reference](https://api.slack.com/reference)
- [Discord Developer Portal](https://discord.com/developers/docs)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Matrix Specification](https://spec.matrix.org/latest/)
- [Mattermost Developer Documentation](https://developers.mattermost.com/)
- [Element Pricing](https://element.io/pricing)
