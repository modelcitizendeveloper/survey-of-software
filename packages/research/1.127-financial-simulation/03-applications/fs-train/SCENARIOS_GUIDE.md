# fs-train Scenarios Guide

Complete training curriculum for financial analysis fluency.

## All Scenarios (10 Total)

### Beginner Level (2 scenarios)

#### 001 - TechStart: Simple Growth
**Concept:** Basic revenue growth and trend recognition
**Industry:** SaaS
**What to learn:** Identify growth trends, understand P&L basics
**Key insights:** Revenue growing steadily, healthy margins

#### 002 - CloudHost: Margin Squeeze
**Concept:** Margin compression from cost increases
**Industry:** Cloud Infrastructure
**What to learn:** Gross margin analysis, cost structure problems
**Key insights:** COGS rising faster than revenue, profitability at risk

---

### Intermediate Level (4 scenarios)

#### 003 - Acme Corp: Growth Investment
**Concept:** Trading profitability for growth
**Industry:** SaaS
**What to learn:** OpEx scaling, hiring signals, strategic trade-offs
**Key insights:** New hire in March, marketing acceleration, adequate runway

#### 004 - ConsultCo: Cash Timing Issue
**Concept:** Profitable but running out of cash (AR buildup)
**Industry:** B2B Services
**What to learn:** Working capital, DSO, cash vs profitability
**Key insights:** AR growing, cash declining despite profits, Net 60 terms

#### 007 - LeadGen: Scaling Efficiency
**Concept:** Unit economics improving with scale
**Industry:** Marketing SaaS
**What to learn:** CAC trends, operating leverage, path to profitability
**Key insights:** CAC improving, OpEx leverage, approaching break-even

#### 010 - FormBuilder: Breaking Even
**Concept:** Crossing profitability milestone
**Industry:** No-Code SaaS
**What to learn:** Sustainability metrics, cash inflection, Rule of 40
**Key insights:** Break-even in Oct, self-sustaining business model

---

### Advanced Level (4 scenarios)

#### 005 - RetailTech: Holiday Season
**Concept:** Don't confuse seasonality with decline
**Industry:** E-commerce SaaS
**What to learn:** Seasonal patterns, YoY analysis, Q4 dynamics
**Key insights:** Nov spike (Black Friday), Dec decline is normal

#### 006 - CloudSync: Runway Warning
**Concept:** Burn rate crisis requiring urgent action
**Industry:** Cloud Storage
**What to learn:** Runway calculation, burn rate, cost cutting decisions
**Key insights:** Only 3.5 months runway, need 40%+ OpEx cuts

#### 008 - DataTools: Pivot to Enterprise
**Concept:** Business model transition in progress
**Industry:** Data Analytics
**What to learn:** Look beneath volatility, segment analysis, lumpy revenue
**Key insights:** SMB declining, Enterprise growing, pivot working

#### 009 - VideoSaaS: Hidden Churn
**Concept:** High churn masked by acquisition
**Industry:** Video Platform
**What to learn:** Revenue quality, leaky bucket, LTV:CAC failure
**Key insights:** 35% monthly churn, acquisition masking retention problem

---

## Learning Path Recommendations

### Complete Beginner
Start here to learn P&L basics:
1. **001 - Simple Growth** (warm up)
2. **002 - Margin Compression** (introduce problems)
3. **003 - Growth Investment** (trade-offs)

### Intermediate Analyst
Ready for complexity:
1. **004 - Cash Crunch** (cash ≠ profit)
2. **007 - Unit Economics Win** (efficiency)
3. **010 - Profitability Milestone** (success story)
4. **005 - Seasonal Pattern** (timing matters)

### Advanced/Professional
Challenging scenarios:
1. **006 - Burn Rate Crisis** (urgent decisions)
2. **008 - Product Pivot** (messy but working)
3. **009 - Subscription Churn** (hidden problems)

## Concepts Covered

### Growth Analysis
- **Simple growth** (001)
- **Accelerating growth** (007)
- **Seasonal patterns** (005)
- **Revenue composition** (008, 009)

### Margin & Efficiency
- **Margin compression** (002)
- **Margin stability** (003, 007)
- **Gross margin excellence** (010)
- **Operating leverage** (007)

### Cash & Sustainability
- **Working capital** (004)
- **Runway management** (006)
- **Cash inflection** (010)
- **Burn rate** (006)

### Unit Economics
- **CAC trends** (007)
- **Churn impact** (009)
- **LTV:CAC ratio** (009)
- **Payback periods** (007)

### Strategy & Decisions
- **Growth vs profitability** (003)
- **Business model pivots** (008)
- **Cost cutting** (006)
- **Product-market fit** (007, 010)

## Difficulty Progression

### By Total Points Available
1. **001** - 75 points (easiest)
2. **002** - 95 points
3. **003** - 110 points
4. **010** - 180 points
5. **007** - 130 points
6. **004** - 125 points
7. **005** - 125 points
8. **008** - 160 points
9. **006** - 135 points
10. **009** - 180 points (hardest)

### By Concept Complexity
**Level 1:** P&L reading (001, 002)
**Level 2:** Multi-view analysis (003, 004, 007, 010)
**Level 3:** Underlying dynamics (005, 006, 008, 009)

## Usage Tips

### Quick Practice (15 min)
Pick any 2 scenarios and compare:
```bash
./run-fs-train 001
./run-fs-train 006
```

### Full Training Session (1 hour)
Complete a difficulty tier:
```bash
./run-fs-train 001  # Beginner
./run-fs-train 002  # Beginner
./run-fs-train 003  # Intermediate
./run-fs-train 007  # Intermediate
```

### Focused Learning
Target specific concepts:
- **Cash management:** 004 → 006 → 010
- **Growth quality:** 003 → 007 → 009
- **Strategic analysis:** 005 → 008 → 009

### With LLM Coaching
Enable LLM for jargon guidance:
```bash
./run-fs-train 004 --llm
```

## Success Metrics

### Beginner Level
- **Goal:** 50%+ score on scenarios 001-002
- **Milestone:** Identify trends and basic problems

### Intermediate Level
- **Goal:** 60%+ score on scenarios 003-004, 007, 010
- **Milestone:** Calculate ratios, understand trade-offs

### Advanced Level
- **Goal:** 70%+ score on scenarios 005-006, 008-009
- **Milestone:** Diagnose root causes, recommend actions

## Next Steps

After completing all 10 scenarios:
1. Review session logs in `training_sessions.jsonl`
2. Identify which concept areas need more practice
3. Retry scenarios where you scored < 60%
4. Try speed runs (complete scenario in < 5 minutes)

---

**Total Training Time:** ~2-3 hours for all 10 scenarios
**Recommended Pace:** 2-3 scenarios per session
**Repeat:** Practice each scenario 2-3 times for mastery
