# Factumerit Pricing Strategy: API Resell Model

## Executive Summary

Replace BYOK (Bring Your Own Key) with a tiered subscription model where users pay Factumerit for Claude access. BYOK remains available only for Enterprise tier.

## Problem with Current BYOK Approach

### Security Issues
- Users must paste API keys in chat (bad security practice)
- Keys visible in Matrix/Slack history
- No guidance on key permissions/spending limits
- Users don't understand what key will be used for
- Trust barrier: "Why should I give you my API key?"

### Business Issues
- No revenue from API usage
- Support burden for key management issues
- Users need Anthropic accounts (friction)
- Unpredictable costs for users

## Proposed Solution: Tiered Subscription Model

### Pricing Tiers

**Free Tier: $0/month**
- 10 queries/month
- Cost to us: ~$0.05/month
- Purpose: Try before you buy, onboarding
- Converts to paid when limit reached

**Individual: $20/month**
- 500 queries/month
- Cost to us: ~$2.50
- Margin: ~60% after overhead (Stripe fees, taxes)
- Target: Solo users, freelancers

**Team: $50/month**
- 2000 queries/month
- Cost to us: ~$10
- Margin: ~50% after overhead
- Target: 2-5 person teams

**Business: $150/month**
- Unlimited queries (fair use ~5K/month)
- Cost to us: ~$20-30
- Margin: ~60% after overhead
- Target: 10+ person teams

**Enterprise: Custom pricing**
- BYOK option (use their Anthropic key)
- White-label support
- SLA guarantees
- Dedicated support
- Pricing: $500-2000/month depending on size
- Revenue from: support, customization, not API usage

## Cost Analysis

### Per-Query Costs (Worst Case)
```
Complex query with tools:
- Input: 10K tokens (system + tools + history) = $0.0025
- Output: 2K tokens (response + tool calls) = $0.0025
- Total: ~$0.005 per query

Simple query:
- Input: 2K tokens = $0.0005
- Output: 500 tokens = $0.0006
- Total: ~$0.001 per query
```

### Monthly Cost Examples
```
Light user (100 queries): $0.50
Medium user (500 queries): $2.50
Heavy user (2000 queries): $10.00
Power user (5000 queries): $25.00
```

### Overhead Calculations
```
$20 Individual subscription:
- Anthropic cost: $2.50
- Stripe fees (2.9% + $0.30): $0.88
- Taxes (30%): $6.00
- Net profit: $10.62 (53% margin)
```

## Value Proposition

Users aren't just paying for API access, they're paying for:

1. **Vikunja Integration** - Natural language → task management
2. **Zero Setup** - No Anthropic account needed
3. **Multi-Platform** - Works in Matrix + Slack
4. **Context Awareness** - Conversation memory
5. **Tool Ecosystem** - 58 Vikunja tools integrated
6. **Predictable Costs** - No surprise bills
7. **Support** - We handle issues, not them

## Competitive Pricing

- Notion AI: $10/user/month
- ClickUp AI: $5/user/month
- Asana AI: $10/user/month
- Motion: $34/user/month
- **Factumerit Individual: $20/month** (competitive)

## User Experience

### Onboarding Flow
```
User: hey what's my day look like

Bot: 👋 Welcome! You're on the FREE tier (10 queries/month).
     This will use 1 query. Continue? [Yes] [Learn More]

[After 10 queries]

Bot: 🎉 You've used all 10 free queries!
     
     Ready to upgrade?
     • Individual: $20/mo (500 queries)
     • Team: $50/mo (2000 queries)
     • Business: $150/mo (unlimited)
     
     [View Plans] [Contact Sales]
```

### Upgrade Flow
```
!upgrade individual

Bot: 💳 Subscribe to Individual ($20/month)
     
     ✅ 500 queries/month
     ✅ Priority support
     ✅ Cancel anytime
     
     [Pay with Stripe] → Opens checkout
```

## Implementation Requirements

### Phase 1: Core Infrastructure
- [ ] User tier tracking in database
- [ ] Query counting per user per month
- [ ] Rate limiting by tier
- [ ] Usage dashboard (!usage command)
- [ ] Tier enforcement in LLM calls

### Phase 2: Payment Integration
- [ ] Stripe subscription setup
- [ ] Webhook handlers (payment success/failure)
- [ ] Upgrade/downgrade flows
- [ ] Billing portal integration
- [ ] Invoice generation

### Phase 3: Enterprise Features
- [ ] BYOK for Enterprise tier only
- [ ] White-label configuration
- [ ] SLA monitoring
- [ ] Dedicated support channels

## Migration Strategy

### For Existing Users
- Current BYOK users → Grandfathered or migrated to Enterprise
- New users → Start on Free tier
- Clear communication about change

### For First Test User
- Grant unlimited free access via admin command
- `!admin grant-unlimited @user:factumerit.app`
- Collect feedback before launching paid tiers

## Revenue Projections

### Conservative (Year 1)
```
10 Individual users: $2,400/year
5 Team users: $3,000/year
2 Business users: $3,600/year
1 Enterprise user: $6,000/year
Total: $15,000/year
Costs: ~$3,000/year
Net: ~$12,000/year
```

### Growth (Year 2)
```
50 Individual: $12,000/year
20 Team: $12,000/year
10 Business: $18,000/year
5 Enterprise: $30,000/year
Total: $72,000/year
Costs: ~$15,000/year
Net: ~$57,000/year
```

## Next Steps

1. **Immediate**: Get BYOK working for test user (current blocker)
2. **Week 1**: Implement tier system and usage tracking
3. **Week 2**: Stripe integration and upgrade flows
4. **Week 3**: Launch with Free + Individual tiers
5. **Month 2**: Add Team and Business tiers
6. **Month 3**: Enterprise tier with BYOK

## Decision

- ✅ Keep BYOK as Enterprise-only feature
- ✅ Implement tiered subscription model
- ✅ Start with Free tier for testing
- ✅ Launch paid tiers after validation

