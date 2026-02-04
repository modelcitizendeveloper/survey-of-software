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
- **Haiku only** (no Sonnet access)
- Cost to us: ~$0.05/month
- Purpose: Try before you buy, onboarding
- Converts to paid when limit reached

**Individual: $20/month**
- 500 queries/month
- **Haiku unlimited, 20 Sonnet queries/month**
- Per-query cap: $0.10 (prevents $0.30 queries)
- Cost to us: ~$2.50 (mostly Haiku) to ~$4 (with Sonnet)
- Margin: ~60% after overhead (Stripe fees, taxes)
- Target: Solo users, freelancers

**Team: $50/month**
- 2000 queries/month
- **Haiku unlimited, 100 Sonnet queries/month**
- Per-query cap: $0.15
- Cost to us: ~$10 (mostly Haiku) to ~$16 (with Sonnet)
- Margin: ~50% after overhead
- Target: 2-5 person teams

**Business: $150/month**
- Unlimited queries (fair use)
- **Haiku unlimited, 500 Sonnet queries/month**
- Per-query cap: $0.20
- Cost to us: ~$20-40 depending on usage
- Margin: ~60% after overhead
- Target: 10+ person teams

**Enterprise: Custom pricing**
- BYOK option (use their Anthropic key)
- Unlimited Sonnet access (they pay for it)
- White-label support
- SLA guarantees
- Dedicated support
- Pricing: $500-2000/month depending on size
- Revenue from: support, customization, not API usage

## Cost Analysis

### Per-Query Costs (By Model)

**Haiku (claude-3-5-haiku-20241022):**
```
Input: $0.25 per 1M tokens = $0.00025 per 1K tokens
Output: $1.25 per 1M tokens = $0.00125 per 1K tokens

Simple query (2K input, 500 output): $0.001
Complex query (10K input, 2K output): $0.005
```

**Sonnet (claude-3-5-sonnet-20241022):**
```
Input: $3 per 1M tokens = $0.003 per 1K tokens
Output: $15 per 1M tokens = $0.015 per 1K tokens

Simple query (2K input, 500 output): $0.014
Complex query (10K input, 2K output): $0.060
LARGE reorganization (50K input, 10K output): $0.30
```

### Monthly Cost Examples (Mixed Usage)
```
Free tier (10 Haiku queries): $0.05
Light user (100 Haiku, 10 Sonnet): $0.64
Medium user (400 Haiku, 100 Sonnet): $8.00
Heavy user (1500 Haiku, 500 Sonnet): $37.50
```

### Risk: Sonnet Abuse
A user could run 100 large Sonnet queries = $30 cost on a $20/month plan.

**Mitigation strategies:**
1. Free tier = Haiku only
2. Paid tiers = Per-query cost caps
3. Sonnet requires explicit opt-in per query
4. Monthly Sonnet query limits by tier

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

Bot: 👋 Welcome! You're on the FREE tier (10 Haiku queries/month).
     This will use 1 query. Continue? [Yes] [Learn More]

[After 10 queries]

Bot: 🎉 You've used all 10 free queries!

     Ready to upgrade?
     • Individual: $20/mo (500 queries + 20 Sonnet/mo)
     • Team: $50/mo (2000 queries + 100 Sonnet/mo)
     • Business: $150/mo (unlimited + 500 Sonnet/mo)

     [View Plans] [Contact Sales]
```

### Model Selection Flow
```
User: !model sonnet

Bot (Free tier): ❌ Sonnet requires a paid plan.
                 Upgrade to Individual ($20/mo) for 20 Sonnet queries/month.
                 [Upgrade]

Bot (Individual, 0/20 used): ✅ Model set to Sonnet.
                              You have 20 Sonnet queries remaining this month.
                              Resets Jan 1.

Bot (Individual, 20/20 used): ⚠️ You've used all 20 Sonnet queries.
                              Switched to Haiku (unlimited).
                              Upgrade to Team for 100 Sonnet/mo? [Upgrade]
```

### Per-Query Cost Cap
```
User: [sends massive reorganization request]

Bot: ⚠️ This query would cost $0.35 (exceeds $0.10 cap for Individual tier).

     Options:
     • Break into smaller queries (recommended)
     • Upgrade to Team ($50/mo, $0.15 cap)
     • Use BYOK (Enterprise tier)

     [Break Down] [Upgrade]
```

### Upgrade Flow
```
!upgrade individual

Bot: 💳 Subscribe to Individual ($20/month)

     ✅ 500 Haiku queries/month
     ✅ 20 Sonnet queries/month
     ✅ Per-query cap: $0.10
     ✅ Priority support
     ✅ Cancel anytime

     [Pay with Stripe] → Opens checkout
```

## Implementation Requirements

### Phase 1: Core Infrastructure
- [ ] User tier tracking in database
- [ ] Query counting per user per month (separate Haiku/Sonnet counters)
- [ ] Model restrictions by tier (Free = Haiku only)
- [ ] Sonnet query limits by tier
- [ ] Per-query cost estimation before execution
- [ ] Per-query cost cap enforcement
- [ ] Rate limiting by tier
- [ ] Usage dashboard (!usage command showing Haiku/Sonnet breakdown)
- [ ] Tier enforcement in LLM calls

### Phase 2: Payment Integration
- [ ] Stripe subscription setup
- [ ] Webhook handlers (payment success/failure)
- [ ] Upgrade/downgrade flows
- [ ] Billing portal integration
- [ ] Invoice generation

### Phase 3: Cost Control Features
- [ ] Pre-query cost estimation (show user before executing)
- [ ] Cost cap warnings ("This query exceeds your tier cap")
- [ ] Query breakdown suggestions (split large queries)
- [ ] Monthly cost alerts (80% of expected usage)
- [ ] Automatic Sonnet → Haiku fallback when limit reached

### Phase 4: Enterprise Features
- [ ] BYOK for Enterprise tier only
- [ ] White-label configuration
- [ ] SLA monitoring
- [ ] Dedicated support channels
- [ ] Custom Sonnet limits

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

## Technical Implementation: Cost Control

### Pre-Query Cost Estimation

```python
def estimate_query_cost(messages: list, model: str, tools: list) -> float:
    """Estimate cost before executing query."""
    # Count input tokens
    input_tokens = count_tokens(messages) + count_tokens(tools)

    # Estimate output tokens (conservative: 2K for complex, 500 for simple)
    has_tools = len(tools) > 0
    estimated_output = 2000 if has_tools else 500

    # Calculate cost
    if "haiku" in model:
        input_cost = input_tokens * 0.00025 / 1000
        output_cost = estimated_output * 0.00125 / 1000
    elif "sonnet" in model:
        input_cost = input_tokens * 0.003 / 1000
        output_cost = estimated_output * 0.015 / 1000

    return input_cost + output_cost

def check_cost_cap(user_tier: str, estimated_cost: float) -> tuple[bool, str]:
    """Check if query exceeds tier's per-query cost cap."""
    caps = {
        "free": 0.01,      # Haiku only, ~$0.01 max
        "individual": 0.10,
        "team": 0.15,
        "business": 0.20,
        "enterprise": None  # No cap (BYOK)
    }

    cap = caps.get(user_tier)
    if cap is None:
        return True, ""

    if estimated_cost > cap:
        return False, f"Query cost ${estimated_cost:.2f} exceeds tier cap ${cap:.2f}"

    return True, ""
```

### Model Restrictions

```python
def check_model_access(user_tier: str, model: str) -> tuple[bool, str]:
    """Check if user's tier allows this model."""
    if "sonnet" in model:
        if user_tier == "free":
            return False, "Sonnet requires a paid plan (Individual: $20/mo)"

        # Check Sonnet query limit
        sonnet_used = get_user_sonnet_count(user_id, current_month)
        sonnet_limits = {
            "individual": 20,
            "team": 100,
            "business": 500,
            "enterprise": None  # Unlimited
        }

        limit = sonnet_limits.get(user_tier)
        if limit and sonnet_used >= limit:
            return False, f"Sonnet limit reached ({limit}/month). Upgrade or use Haiku."

    return True, ""
```

### Usage Tracking

```python
# After each query
def track_usage(user_id: str, model: str, input_tokens: int, output_tokens: int, cost: float):
    """Track usage for billing and limits."""
    db.execute("""
        INSERT INTO usage_log (user_id, model, input_tokens, output_tokens, cost, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, model, input_tokens, output_tokens, cost, datetime.now()))

    # Update monthly counters
    if "haiku" in model:
        increment_counter(user_id, "haiku_queries", current_month)
    elif "sonnet" in model:
        increment_counter(user_id, "sonnet_queries", current_month)
```

## Next Steps

1. **Immediate**: Get BYOK working for test user (current blocker)
2. **Week 1**: Implement tier system and usage tracking
3. **Week 2**: Cost estimation and caps
4. **Week 3**: Stripe integration and upgrade flows
5. **Week 4**: Launch with Free + Individual tiers
6. **Month 2**: Add Team and Business tiers
7. **Month 3**: Enterprise tier with BYOK

## Decision

- ✅ Keep BYOK as Enterprise-only feature
- ✅ Implement tiered subscription model
- ✅ Free tier = Haiku only (prevent Sonnet abuse)
- ✅ Paid tiers = Sonnet limits + per-query cost caps
- ✅ Start with Free tier for testing
- ✅ Launch paid tiers after validation

