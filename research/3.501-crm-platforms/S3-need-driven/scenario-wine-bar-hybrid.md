# Scenario: Wine Bar with Hybrid B2C + B2B Model

**Business Pattern**: Wine bar with retail customers (B2C) + wholesale distribution (B2B)

---

## Context

**Customer Base**:
- B2C: 200+ regular retail customers (walk-in, tastings, bottle sales)
- B2B: 10-50 wholesale accounts (restaurants, hotels, corporate clients)

**Tech Stack**:
- POS system handles B2C (loyalty, transactions, inventory)
- Need CRM for B2B wholesale pipeline

**Team**: 1-3 people (owner + sommelier/sales)

**Budget**: <$50/month for CRM

**Sales Motion**:
- B2C: Handled by POS loyalty features
- B2B: Relationship-based, proposals, follow-ups, contract tracking

---

## Recommended Platform

### Primary: Zoho Bigin Premier ($12/user/month)

**Why**:
- ✅ **Affordable**: $12-36/month for 1-3 users
- ✅ **Built-in calling**: Wholesale follow-ups without extra cost
- ✅ **Simple pipeline**: 6 pipelines sufficient for wholesale stages
- ✅ **Workflow automation**: Follow-up reminders, task assignment
- ✅ **Upgrade path**: Can move to Zoho CRM if wholesale grows to 200+ accounts

**Matches this pattern because**:
- Small B2B account count (10-50) doesn't justify expensive CRM
- Budget-conscious (startup/small business phase)
- Need professional pipeline management without complexity

---

## Alternative Options

### Alternative 1: Pipedrive Essential ($14/user/month)

**When to choose**:
- Value visual pipeline over cost savings ($2/user premium)
- Team coordination important (2-3 people managing accounts)
- Want best-in-class UX

**Trade-off**: $14 vs $12/user, but no built-in calling (need integration)

---

### Alternative 2: Spreadsheet+ (Airtable, Notion)

**When to choose**:
- Extremely budget-constrained (<$20/month total)
- Very simple sales process
- <20 wholesale accounts

**Trade-off**: Manual vs automated, no calling, limited pipeline features

---

## Avoid

❌ **Close CRM** ($75/month minimum for 3 users)
- Overkill for 10-50 accounts
- Calling features wasted (not making >30 calls/day)

❌ **HubSpot**
- Marketing automation not needed (B2C handled by POS)
- Expensive once you outgrow free tier

❌ **Salesforce**
- Massive overkill for small wholesale operation

---

## Migration Path

**Year 1-2** (10-50 accounts):
- Zoho Bigin Premier ($12/user)
- OR Pipedrive Essential ($14/user)

**Year 2-3** (50-200 accounts):
- Upgrade to Zoho CRM Standard ($14/user) - seamless from Bigin
- OR Pipedrive Advanced ($29/user) if staying with Pipedrive

**Year 3+** (200+ accounts, adding marketing):
- HubSpot Professional (if need marketing automation)
- OR stay with Zoho CRM/Pipedrive (if pure sales focus)

---

## Implementation Notes

**POS Integration**:
- B2C customers stay in POS (Square, Toast, etc.)
- B2B wholesale accounts in CRM
- Use Zapier if need to sync wholesale purchases from POS to CRM

**Typical Pipeline Stages**:
1. Lead (initial contact)
2. Qualified (tasting scheduled)
3. Proposal Sent (pricing, terms)
4. Negotiation (volume, delivery)
5. Contract Signed
6. Active Account (ongoing orders)

**Automation Examples**:
- Lead created → Auto-assign to salesperson
- Proposal sent → Follow-up task in 3 days
- No activity in 30 days → Re-engagement email

---

## Applies To

- Wine bars, tasting rooms, wineries
- Specialty food/beverage retailers with wholesale
- Boutique shops with B2C retail + B2B corporate sales
- Coffee roasters with cafe (B2C) + wholesale (B2B)
- Artisan producers with dual sales channel

**Pattern**: Any small business with <100 B2B accounts + separate B2C channel handled by POS

---

**Last Updated**: 2025-10-21
**Generic Pattern**: Reusable for any similar hybrid retail + wholesale business
