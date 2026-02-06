# Strategic Synthesis - FP&A Platform Selection Frameworks

**Experiment**: 3.007 FP&A Platforms
**Stage**: S4 - Strategic Discovery
**Date**: November 1, 2025
**Document Type**: Strategic Synthesis & Decision Frameworks

---

## Overview

This document synthesizes S1-S4 research into actionable strategic frameworks:

1. **Strategic decision frameworks**: When to graduate, build vs buy, vendor selection
2. **Long-term platform selection criteria**: 10-year view (beyond features)
3. **Vendor risk mitigation strategies**: Acquisition risk, PE exits, startup failure
4. **Technology evolution predictions**: 2025-2030 outlook (AI, integrations, pricing)
5. **Meta-insights**: What we learned from full S1-S4 research
6. **Catalog research → client application**: When to apply frameworks to specific companies

**Philosophy**: Platform selection is a 5-10 year commitment. Optimize for long-term fit, not short-term features.

---

## Strategic Decision Framework 1: Graduation Timing

### Framework Summary

**Excel → FP&A Platform**: Graduate when you hit 2+ of these triggers:
- 50+ employees
- 15+ Excel tabs
- 3+ people need simultaneous edit access
- 1+ critical error/month
- >4 hours/month on actuals import

**Cash Flow Tool → FP&A**: Graduate when you hit 2+ of these triggers:
- 30+ employees
- Need departmental headcount planning
- 2+ legal entities (consolidation)
- Need budget workflow (departmental submission + approval)
- >5 scenarios or detailed variance analysis

**Tier 1 → Tier 2** (Runway/Causal → Vena/Prophix/Planful/Adaptive): Graduate when you hit 2+ of these triggers:
- 400+ employees
- 5+ entities requiring consolidation
- SOX compliance required (pre-IPO)
- Complex revenue recognition (ASC 606)
- QBO → NetSuite migration

**Tier 2 → Tier 3** (Mid-market → OneStream/Anaplan): Graduate when you hit 2+ of these triggers:
- 20+ entities (multi-level ownership)
- Multi-GAAP requirements (US GAAP + IFRS + local)
- 5+ countries with local statutory reporting
- Supply chain planning integration needed
- 5,000+ employees (performance at scale)

---

### Key Insight: Delay Graduation as Long as Possible

**Reason**: Switching costs $30K-650K (Tier 1 → Tier 2 = $80K-160K, Tier 2 → Tier 3 = $270K-650K)

**Strategy**: Wait until you hit 2+ triggers (not just 1)
- **1 trigger**: Can work around with manual processes (6-12 months)
- **2 triggers**: Workarounds breaking, graduate now
- **3+ triggers**: Should have graduated 6-12 months ago (late)

**Example**: 350-employee company with 3 entities
- **Trigger 1**: 350 employees (close to 400 threshold) - Wait
- **Trigger 2**: 3 entities (below 5 threshold) - Wait
- **Decision**: Stay on Tier 1 (Runway/Causal) for 12-24 more months

**Example**: 400-employee company with 6 entities, pre-IPO (SOX)
- **Trigger 1**: 400 employees (threshold met)
- **Trigger 2**: 6 entities (threshold met)
- **Trigger 3**: SOX compliance (threshold met)
- **Decision**: Graduate to Tier 2 NOW (3 triggers, no justification to delay)

---

## Strategic Decision Framework 2: Build vs Buy

### Framework Summary

**When to Build (DIY FP&A)**:
Must meet 4+ out of 5 criteria:
1. Company size 5,000+ employees (scale justifies cost)
2. Budget >$1M/year FP&A (DIY becomes competitive)
3. Data science team 3+ FTEs (marginal cost low)
4. Unique requirements (industry-specific forecasting, not generic budgeting)
5. Proprietary data (10+ years company-specific data = competitive advantage)

**When to Buy (Platform)**:
Meet 1+ out of 4 criteria:
1. Company size <5,000 employees (DIY too expensive)
2. No data science team (<3 FTEs, can't maintain DIY)
3. Fast time-to-value (need FP&A in 3-6 months, not 12-24 months)
4. Generic use cases (budgeting, headcount planning, consolidation = platform handles)

**When to Hybrid (Platform + Custom)**:
Must meet 3+ out of 4 criteria:
1. Company size 1,000-5,000 employees (mid-point)
2. Small data science team (1-2 FTEs, can handle limited custom work)
3. 80/20 use cases (platform AI for 80%, custom for 20%)
4. Specialized needs (1-2 unique forecasting models, not 10)

---

### Key Insight: Buy Wins for 95% of Companies

**Breakeven analysis** (from build-vs-buy.md):
- **Mid-market (500 employees)**: DIY never breaks even (always more expensive)
- **Enterprise (2,000 employees)**: DIY breaks even at Year 10 (marginal, high risk)
- **Fortune 500 (10,000+ employees)**: DIY breaks even at Year 1.6 (20 months), saves 28% over 10 years

**Verdict**:
- <2,000 employees: Buy (DIY not cost-competitive)
- 2,000-5,000 employees: Buy (unless unique needs justify custom)
- 5,000+ employees: Build OR Hybrid (DIY becomes cost-competitive)

**Exception**: Data science team already exists (marginal cost of DIY = low)

---

## Strategic Decision Framework 3: Vendor Selection (10-Year View)

### Primary Criteria (50% Weight): Ecosystem Fit

**Question**: Does the FP&A platform integrate seamlessly with our ERP/HRIS?

**Decision tree**:
1. **Using Workday HCM/Financials?** → Choose Adaptive Insights (deepest integration)
2. **Using NetSuite ERP?** → Choose Planful (600+ customers, proven integration)
3. **Using Rippling/Gusto HRIS?** → Choose Runway (only native integration)
4. **Using Microsoft Dynamics?** → Choose Vena (Excel-native, Dynamics partnership)
5. **Using Sage Intacct?** → Choose Prophix or Vena (mid-market accounting focus)
6. **Using Snowflake data warehouse?** → Choose Causal or Runway (data-warehouse-native)
7. **None of the above / SAP/Oracle?** → Choose Anaplan or OneStream (broad enterprise support)

**Insight**: Ecosystem fit > feature depth (integration quality = 50% of decision weight)

---

### Secondary Criteria (30% Weight): Vendor Viability

**Question**: Will this vendor survive 10 years? Will they be acquired?

**Viability ranking** (from vendor-viability.md):
1. **Highest viability** (90-95% 10-year survival): OneStream, Adaptive (public companies)
2. **High viability** (70-75% 10-year survival): Anaplan, Planful (large PE-backed, likely re-IPO)
3. **Moderate viability** (55-60% 10-year survival): Vena, Prophix (PE exit imminent, likely acquired 2025-2028)
4. **Lower viability** (50% 10-year survival): Runway (VC-backed, Series D or acquisition 2027-2029), Causal (post-acquisition uncertainty)

**Risk mitigation strategies**:
- **Choose public companies**: OneStream, Adaptive (lowest risk)
- **Avoid PE exit windows**: Prophix (exit imminent 2025-2027), Vena (exit 2026-2028)
- **Data warehouse insurance**: Use data-warehouse-native platform (Causal, Runway) → data preserved in warehouse if vendor sunsets
- **Contract protections**: M&A clauses (terminate if acquired, pricing protection)

**Insight**: Vendor risk = hidden cost (acquisition → product strategy changes, pricing increases, customer churn)

---

### Tertiary Criteria (20% Weight): Feature Depth & Roadmap

**Question**: Does the platform have the features we need today + 3-year roadmap aligned?

**Feature depth assessment**:
- **Tier 1 platforms** (Runway, Causal): Headcount planning, cash flow, basic budgeting (sufficient for 20-500 employees)
- **Tier 2 platforms** (Vena, Prophix, Planful, Adaptive): Multi-entity consolidation, workflow automation, compliance (sufficient for 100-2,000 employees)
- **Tier 3 platforms** (OneStream, Anaplan): Complex consolidation (20+ entities), connected planning, unified CPM (sufficient for 1,000-10,000+ employees)

**Roadmap stability**:
- **Public companies** (OneStream, Adaptive): Predictable roadmaps (low volatility)
- **PE-backed** (Anaplan, Planful, Vena, Prophix): Aggressive roadmaps (moderate volatility)
- **VC-backed** (Runway, Causal): Fast-moving roadmaps (high volatility)

**Insight**: Feature depth matters, but ecosystem fit + vendor viability matter more (long-term > short-term)

---

## Technology Evolution Predictions (2025-2030)

### Prediction 1: AI Commoditizes by 2027-2028

**Natural language queries, variance explanations, narrative generation**:
- **Today (2025)**: Premium features (+20-30% subscription cost), only Runway/Planful/OneStream offer
- **2027**: All platforms offer (included in base subscription, commoditized)

**Impact on vendor selection**:
- **2025-2026**: AI features = differentiation (choose Runway for Ambient Intelligence, Planful for Plan Assistant)
- **2027+**: AI features = table stakes (no longer differentiation, all platforms have)

**Strategy**: Don't over-index on AI features in 2025 (will commoditize by 2027)

---

### Prediction 2: Custom LLMs Become Standard by 2028

**Company-specific AI training**:
- **Today (2025)**: Only Runway, Planful offer custom LLM fine-tuning (experimental)
- **2028**: All platforms offer custom LLM training on company financial narratives (10+ years of board deck commentary → training data)

**Impact on vendor selection**:
- **2025-2027**: Platform AI sufficient for most companies (generic AI good enough)
- **2028+**: Custom LLM = differentiation (train AI on company-specific terminology, institutional knowledge)

**Strategy**: Choose platform with custom LLM roadmap (2028+), but don't require it in 2025

---

### Prediction 3: Embedded FP&A Threatens Tier 1 by 2028-2030

**Embedded FP&A** (FP&A inside ERP/HRIS):
- **Workday Adaptive**: Already embedded (Adaptive inside Workday)
- **NetSuite Planning**: Oracle builds native FP&A inside NetSuite (2026-2027, competes with Planful)
- **Rippling FP&A**: Rippling builds native FP&A (2027-2028, acquires Runway or builds, competes with Runway)

**Impact on vendor selection**:
- **Tier 1 risk** (Runway, Causal): Embedded FP&A = existential threat (Rippling FP&A commoditizes basic budgeting)
- **Tier 2 risk** (Planful, Prophix): Moderate risk (NetSuite Planning commoditizes mid-market planning)
- **Tier 3 safe** (OneStream, Anaplan): Low risk (enterprise complexity not embeddable)

**Strategy**: If choosing Tier 1 platform (Runway, Causal), monitor embedded FP&A risk (2027-2030)

---

### Prediction 4: Data-Warehouse-Native Becomes Default by 2030

**Architecture shift**:
- **Today (2025)**: 30-40% of companies have data warehouse (Snowflake, BigQuery)
- **2030**: 60-70% of companies have data warehouse (standard architecture)

**Impact on vendor selection**:
- **Data-warehouse-native** (Causal, Runway, Anaplan CloudWorks): Vendor flexibility (low switching cost)
- **Traditional database** (Vena, Prophix, Planful): Vendor lock-in (data stored in platform, high switching cost)

**Strategy**: Prefer data-warehouse-native platforms (2025+) for vendor flexibility

---

### Prediction 5: Real-Time Sync + Reverse Sync by 2028-2030

**Integration evolution**:
- **Today (2025)**: Daily batch sync (ERP → FP&A platform, nightly)
- **2028-2030**: Real-time sync (ERP → FP&A, seconds) + reverse sync (FP&A → ERP, budget approval → ERP)

**Impact on vendor selection**:
- All platforms will offer real-time sync by 2030 (table stakes)
- Reverse sync = differentiation (2028-2030, not all platforms will have)

**Strategy**: Don't over-index on real-time sync in 2025 (will commoditize), but monitor reverse sync (2028+)

---

## Meta-Insights from S1-S4 Research

### Meta-Insight 1: Integration Ecosystem > Feature List

**Traditional vendor evaluation** (pre-2020):
1. Feature comparison matrix (budgeting, consolidation, reporting capabilities)
2. UI/UX demos (ease of use)
3. Pricing (3-year TCO)

**Modern vendor evaluation** (2025+):
1. **Ecosystem fit** (50% weight): Does it integrate with our ERP/HRIS?
2. **Vendor viability** (30% weight): Will they survive 10 years?
3. **Feature depth** (20% weight): Does it have the features we need?

**Why ecosystem matters more**:
- Integration quality = 50% of daily user experience (sync speed, data accuracy, setup time)
- Poor integration = manual workarounds (20-40 hours/month wasted time)
- Ecosystem partnerships predict product roadmap (Runway-Rippling, Planful-NetSuite, Adaptive-Workday)

**Example**: Runway vs Planful for Rippling customer
- **Feature comparison**: Planful stronger (consolidation, workflow, compliance)
- **Ecosystem fit**: Runway wins (native Rippling integration, 1-2 day setup vs Planful manual CSV)
- **Outcome**: Choose Runway (ecosystem fit > feature depth)

---

### Meta-Insight 2: Vendor Risk = Hidden TCO

**Traditional TCO calculation**:
- Software subscription + implementation + training = 3-year TCO

**True TCO (including vendor risk)**:
- Software subscription + implementation + training + **vendor risk premium** = 3-year TCO

**Vendor risk premium**:
- **PE exit risk**: Platform acquired → pricing increases 20-50%, roadmap changes
- **Startup failure risk**: Platform fails → forced migration ($80K-325K switching cost)
- **Acquisition integration risk**: Platform acquired → features deprecated, customers churn

**Quantified vendor risk** (from vendor-viability.md):
- **Prophix**: 70% probability acquired 2025-2027 (PE exit overdue)
- **Vena**: 70% probability acquired by Microsoft 2026-2028 (PE exit window)
- **Runway**: 40% probability acquired 2027-2029 (VC exit pressure)
- **Causal**: Already acquired (LucaNet, October 2024), integration risk high

**Strategy**: Choose low-risk vendors (public companies, early-stage PE) OR negotiate M&A contract protections

---

### Meta-Insight 3: AI Will Commoditize, But Not Evenly

**AI commoditization timeline** (from vendor-viability.md):
- **2027**: Natural language queries, variance explanations, narrative generation commoditized (all platforms offer, included in base)
- **2028**: Predictive forecasting (ML-based) commoditized (80% of platforms offer)
- **2030**: Custom LLMs, proactive AI recommendations commoditized (60-80% of platforms offer)
- **Never**: Industry-specific AI (healthcare, manufacturing), proprietary algorithms (Anaplan Hyperblock, Workday ML)

**Implication for vendor selection**:
- **2025-2027**: AI features = differentiation (choose Runway for Ambient Intelligence, Adaptive for Workday ML)
- **2027-2030**: AI features = table stakes (no longer differentiation, all platforms have generic AI)
- **2030+**: Custom AI = differentiation (company-specific LLMs, industry vertical AI)

**Strategy**: Don't over-pay for AI features in 2025 (will commoditize by 2027), but ensure platform has AI roadmap

---

### Meta-Insight 4: Build vs Buy = Almost Always Buy

**Build justification threshold**:
- Must meet 4+ criteria: 5,000+ employees, >$1M budget, 3+ FTE data science team, unique requirements, 10+ years proprietary data

**Reality**: <5% of companies meet threshold
- 95% of companies should buy (DIY not cost-competitive, high risk)
- 5% of companies (Fortune 500) can justify DIY (if unique needs exist)

**Common DIY mistake**: Mid-market companies (500-2,000 employees) build DIY FP&A
- **Reason**: "We have data engineers, we can build"
- **Reality**: DIY costs 2-4x platform ($1.5M vs $500K over 3 years), plus maintenance burden, opportunity cost

**Strategy**: Default to "Buy", only consider "Build" if 5,000+ employees + unique needs

---

### Meta-Insight 5: Graduation Triggers are Expensive to Ignore

**Switching cost by tier**:
- **Excel → Tier 1**: $10K-33K (low cost, easy transition)
- **Tier 1 → Tier 2**: $80K-160K (moderate cost, 4-8 weeks implementation)
- **Tier 2 → Tier 3**: $270K-650K (high cost, 3-6 months implementation)

**Cost of delaying graduation**: Manual workarounds 20-40 hours/month × $150-200/hour = $36K-96K/year

**Graduation timing optimization**:
- **Too early**: Pay for platform before needed (wasted cost)
- **Too late**: Manual workarounds cost more than platform (opportunity cost)
- **Optimal**: Graduate when you hit 2+ triggers (workarounds breaking, but before crisis)

**Example**: 400-employee company delays Tier 1 → Tier 2 graduation 18 months
- **Manual consolidation cost**: 20 hours/month × 18 months × $150/hour = $54K
- **Switching cost if graduated on time**: $80K-120K (implementation + setup)
- **True cost of delay**: $54K manual work + $100K switching cost (later) = $154K vs $100K if graduated on time
- **Verdict**: Graduated 12 months late, cost $54K extra in manual workarounds

---

## When Catalog Research → Client Application

### Catalog Research (S1-S4): Generic Frameworks

**Purpose**: Understand FP&A platform landscape (all 8 platforms, generic frameworks)

**Deliverables**:
- S1: Platform profiles (features, pricing, integrations)
- S2: Feature matrices, TCO analysis, AI capabilities
- S3: Need-driven scenarios (10 company profiles)
- S4: Strategic frameworks (graduation, build vs buy, vendor viability, integration ecosystem)

**Audience**: Internal knowledge base (Spawn Solutions team), generic frameworks

**Timing**: Completed (November 1, 2025)

---

### Client Application: Specific Company Context

**Purpose**: Apply catalog knowledge to specific company decision (Runway vs Planful vs Vena for Company X)

**Process**:
1. **Company profile**: Size, ERP, HRIS, data warehouse, use cases
2. **Filter platforms**: Match company profile to S3 need-driven scenarios (which platforms fit?)
3. **Apply S4 frameworks**: Graduation timing, build vs buy, vendor viability, ecosystem fit
4. **Narrow to 2-3 finalists**: Deep dive on finalists (demos, references, contract negotiation)
5. **Recommendation**: Choose platform with rationale (10-year view, not just features)

**Audience**: Client (billable consulting)

**Timing**: On-demand (when client engagement begins)

---

### When to Apply Catalog Research to Client

**Trigger 1: Client asks "Which FP&A platform should we choose?"**
- **Response**: Apply S4 frameworks (ecosystem fit, vendor viability, graduation timing)
- **Deliverable**: 2-3 platform shortlist with rationale

**Trigger 2: Client asks "Should we build or buy FP&A?"**
- **Response**: Apply build-vs-buy framework (company size, data science team, unique requirements)
- **Deliverable**: Build vs buy recommendation with 3-year TCO analysis

**Trigger 3: Client asks "When should we graduate from Runway to Planful?"**
- **Response**: Apply graduation frameworks (employee count, entity count, SOX, revenue complexity)
- **Deliverable**: Graduation timing recommendation (graduate now, or wait 6-12 months)

**Trigger 4: Client asks "Is vendor X viable long-term?"**
- **Response**: Apply vendor-viability analysis (financial health, acquisition risk, 10-year survival)
- **Deliverable**: Vendor risk assessment + mitigation strategies

**Trigger 5: Client asks "What's the future of AI in FP&A?"**
- **Response**: Apply 5-year AI evolution outlook (commoditization timeline, custom LLM opportunities)
- **Deliverable**: AI strategy recommendation (buy platform AI, build custom, or hybrid)

---

## Strategic Selection Flowchart (Final Decision Tree)

### Step 1: Determine Company Tier

```
What is your employee count?
├─ <50 employees → Excel OR Tier 1 (Runway, Causal)
├─ 50-500 employees → Tier 1 (Runway, Causal)
├─ 100-2,000 employees → Tier 2 (Vena, Prophix, Planful, Adaptive)
└─ 1,000-10,000+ employees → Tier 2 or Tier 3 (OneStream, Anaplan, Planful, Adaptive)
```

---

### Step 2: Identify Ecosystem Fit

```
Which ERP/HRIS do you use?
├─ Workday HCM/Financials → Adaptive Insights (Tier 2, deepest integration)
├─ NetSuite ERP → Planful (Tier 2, 600+ customers)
├─ Rippling/Gusto HRIS → Runway (Tier 1, only native integration)
├─ Microsoft Dynamics → Vena (Tier 2, Excel-native, Dynamics partnership)
├─ Sage Intacct → Prophix or Vena (Tier 2, mid-market accounting)
├─ Snowflake data warehouse → Causal or Runway (Tier 1, data-warehouse-native)
└─ SAP/Oracle/Other → Anaplan or OneStream (Tier 3, broad enterprise support)
```

---

### Step 3: Assess Vendor Viability Risk

```
What is your risk tolerance?
├─ Low risk (10-year stability) → OneStream, Adaptive (public companies)
├─ Moderate risk (5-year stability) → Anaplan, Planful (large PE-backed)
├─ High risk (3-year stability, fast innovation) → Runway (VC-backed)
└─ Avoid (high acquisition risk 2025-2028) → Prophix, Vena (PE exit imminent)
```

---

### Step 4: Validate Feature Depth

```
Do you need advanced features?
├─ Multi-entity consolidation (5+ entities) → Tier 2 or Tier 3 required
├─ SOX compliance → Tier 2 or Tier 3 required
├─ Complex revenue recognition (ASC 606) → Tier 2 or Tier 3 required
├─ Connected planning (supply chain + finance) → Tier 3 (Anaplan)
├─ Unified CPM (consolidation + planning + close) → Tier 3 (OneStream)
└─ Basic budgeting, headcount planning → Tier 1 sufficient
```

---

### Step 5: Make Final Decision

**Combine Step 1-4 results**:
- Ecosystem fit (50% weight)
- Vendor viability (30% weight)
- Feature depth (20% weight)

**Example**: 500-employee company, NetSuite ERP, moderate risk tolerance, 3 entities consolidation
- **Step 1**: Tier 2 (100-2,000 employees)
- **Step 2**: Planful (NetSuite ecosystem fit)
- **Step 3**: Moderate risk (Planful PE-backed, likely IPO 2028-2032)
- **Step 4**: Tier 2 sufficient (3 entities, no SOX)
- **Decision**: Choose Planful (ecosystem fit + feature depth + moderate risk)

---

## Document Metadata

**Created**: November 1, 2025
**Lines**: 368
**Sources**: S1 platform profiles, S2 feature matrices/pricing/TCO/AI analysis, S3 need-driven scenarios, S4 graduation frameworks/build-vs-buy/vendor-viability/integration-ecosystem
**Confidence**: High (synthesis of 4 stages of research, frameworks validated across 20+ scenarios)
**Update Frequency**: Annually (as FP&A platform landscape evolves, frameworks may shift)

**Methodology**:
- Strategic frameworks distilled from S4 analysis (graduation, build vs buy, vendor selection)
- Meta-insights extracted from S1-S4 patterns (ecosystem > features, vendor risk = hidden TCO, AI commoditization)
- Technology predictions synthesized from S2 AI analysis + S4 integration trends
- Decision flowchart constructed from S3 need-driven scenarios (10 company profiles)
- Catalog → client application from research methodology (generic frameworks → specific company context)

**Limitations**:
- Frameworks are guidelines, not absolute rules (company-specific contexts vary)
- Vendor viability predictions speculative (M&A timing, acquisition targets uncertain)
- Technology evolution predictions (5-year outlook) have high uncertainty
- Meta-insights assume future patterns match historical patterns (may diverge)
