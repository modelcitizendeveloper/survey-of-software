# AI Capabilities Coverage - FP&A Platforms

**Experiment**: 3.007 FP&A Platforms
**Stage**: S2 - Comprehensive Discovery
**Date**: November 1, 2025
**Document Type**: AI Feature Analysis

---

## Overview

This document analyzes AI capabilities across 8 FP&A platforms:

1. AI feature inventory (all 8 platforms)
2. AI maturity matrix (production vs beta vs announced)
3. Path A/B/C analysis (build custom vs buy platform AI vs hybrid)
4. Hype vs reality assessment
5. Customer feedback on AI ROI
6. 2025-2030 AI evolution predictions
7. When AI features will commoditize

**AI Maturity Rating**:
- ✅ **Production**: Live, customer-proven, 12+ months in market
- ⚠️ **Beta**: Live but limited availability, <12 months, gathering feedback
- 📢 **Announced**: Roadmap item, not yet launched
- ❌ **None**: No AI feature documented

---

## AI Feature Inventory

### Natural Language Capabilities

| Platform | Natural Language Query | Natural Language Model Building | Status | Launch Date |
|----------|------------------------|----------------------------------|--------|-------------|
| **Runway** | ✅ Copilot | ✅ Copilot | Production | July 2024 |
| **OneStream** | ⚠️ Search Agent | ❌ None | Beta | May 2025 |
| **Planful** | ⚠️ Plan Assistant | ⚠️ Plan Assistant | Beta | 2025 |
| **Anaplan** | ⚠️ PlanIQ | ❌ None | Production* | 2018 |
| **Adaptive** | ❌ None | ❌ None | None | - |
| **Prophix** | ⚠️ Beta | ❌ None | Beta | 2024 |
| **Vena** | ❌ None | ❌ None | None | - |
| **Causal** | ⚠️ Beta | ⚠️ Beta | Beta | 2024 |

*Anaplan PlanIQ is ML-based, not LLM natural language

**Leaders**: Runway (production NL query + model building), OneStream (4 specialized agents)

---

### Predictive Forecasting (ML/AI)

| Platform | Predictive Forecasting | Anomaly Detection | Status | Technology |
|----------|------------------------|-------------------|--------|------------|
| **Adaptive** | ✅ Full | ✅ Full | Production | Workday ML engine |
| **Anaplan** | ✅ PlanIQ | ✅ PlanIQ | Production | Proprietary ML |
| **Runway** | ⚠️ Beta | ❌ None | Beta | LLM-based |
| **Planful** | ⚠️ Plan Assistant | ❌ None | Beta | LLM-based |
| **OneStream** | ⚠️ Operations Analyst | ⚠️ Operations Analyst | Beta | LLM-based |
| **Prophix** | ⚠️ Beta | ❌ None | Beta | ML-based |
| **Causal** | ⚠️ Beta | ❌ None | Beta | LLM-based |
| **Vena** | ❌ None | ❌ None | None | - |

**Leaders**: Adaptive (Workday ML, production), Anaplan (PlanIQ, 7 years production)

**Note**: ML-based (Adaptive, Anaplan) = trained models, mature; LLM-based (Runway, Planful) = GPT-style, newer

---

### Auto-Generated Insights

| Platform | Variance Explanations | Narrative Generation | Driver Explanations | Status |
|----------|----------------------|----------------------|---------------------|--------|
| **Runway** | ✅ Ambient Intelligence | ✅ Ambient Intelligence | ✅ Ambient Intelligence | Production |
| **Planful** | ⚠️ Plan Assistant | ⚠️ Analyst Assistant | ❌ None | Beta |
| **OneStream** | ⚠️ Finance Analyst | ⚠️ Search Agent | ❌ None | Beta |
| **Adaptive** | ⚠️ Limited | ❌ None | ❌ None | Beta |
| **Anaplan** | ❌ None | ❌ None | ❌ None | None |
| **Prophix** | ❌ None | ❌ None | ❌ None | None |
| **Vena** | ❌ None | ❌ None | ❌ None | None |
| **Causal** | ❌ None | ❌ None | ❌ None | None |

**Leader**: Runway (only platform with production auto-insights across all 3 categories)

**Runway Ambient Intelligence** (July 2024):
- **Variance Explanations**: "Marketing spend 15% over budget due to Q3 ad campaign"
- **Narrative Generation**: Auto-written board deck commentary
- **Driver Explanations**: Hover over "Gross Margin" → AI explains definition + benchmark

---

### AI Agents & Assistants

| Platform | AI Agents/Assistants | Agent Count | Specialization | Status |
|----------|----------------------|-------------|----------------|--------|
| **OneStream** | ✅ AI Agents | 4 | Finance, Operations, Search, Deep Analysis | Beta (May 2025) |
| **Runway** | ✅ Copilot + Ambient | 2 | Copilot (queries), Ambient (background) | Production (July 2024) |
| **Planful** | ⚠️ Plan Assistant | 2 | Analyst, Planner personas | Beta (2025) |
| **Prophix** | ⚠️ AI Agents | 1 | General automation | Beta (2024) |
| **Adaptive** | ❌ None | 0 | - | None |
| **Anaplan** | ❌ None | 0 | - | None (PlanIQ is ML, not agent) |
| **Vena** | ❌ None | 0 | - | None |
| **Causal** | ❌ None | 0 | - | None |

**OneStream AI Agents** (May 2025):
1. **Finance Analyst Agent**: Natural language queries ("Compare Q3 budget vs actuals by region"), auto-visualizations
2. **Operations Analyst Agent**: Monitor transactional/operational data, spot anomalies and trends
3. **Search Agent**: Summarize complex financial reports (hundreds of pages)
4. **Deep Analysis Agent**: Analyze thousands of documents, draw connections (audit compliance, strategic planning)

**Planful AI Assistants** (2025):
1. **Plan Assistant**: Natural language model building ("Increase marketing budget by 15%")
2. **Analyst Assistant**: Variance insights, narrative generation

---

### Workflow Automation (AI-Powered)

| Platform | AI Workflow Automation | Auto Data Collection | Smart Reminders | Status |
|----------|------------------------|----------------------|-----------------|--------|
| **Prophix** | ✅ Full | ✅ Full | ✅ Full | Production |
| **Adaptive** | ✅ Full | ✅ Full | ⚠️ Basic | Production |
| **Planful** | ✅ Full | ✅ Full | ⚠️ Basic | Production |
| **Anaplan** | ✅ Full | ✅ Full | ⚠️ Basic | Production |
| **OneStream** | ✅ Full | ✅ Full | ⚠️ Basic | Production |
| **Runway** | ⚠️ Basic | ✅ Full | ⚠️ Basic | Production |
| **Vena** | ✅ Full | ✅ Full | ⚠️ Basic | Production |
| **Causal** | ⚠️ Basic | ⚠️ Basic | ❌ None | Beta |

**Note**: Workflow automation = traditional automation (not AI), but included for completeness
- All enterprise platforms have mature workflow automation (approvals, notifications, data collection)
- Startup platforms (Runway, Causal) have basic automation

---

## AI Maturity Matrix

### Production AI (Customer-Proven, 12+ Months)

| Platform | Feature | Launch Date | Maturity (Years) | Customer Base Size |
|----------|---------|-------------|------------------|-------------------|
| **Adaptive** | Predictive AI (Workday ML) | 2020 | 5 years | 3,800+ customers |
| **Anaplan** | PlanIQ (ML forecasting) | 2018 | 7 years | 2,200+ customers |
| **Runway** | Ambient Intelligence | July 2024 | 1.3 years | 50+ customers |

**Adaptive Predictive AI**:
- Workday ML engine (enterprise-grade, trained on Workday customer data)
- Predictive forecasting (ML-driven forecast suggestions)
- Anomaly detection (flag unusual variances)
- 5 years production (mature, proven)

**Anaplan PlanIQ**:
- ML module (not LLM, traditional machine learning)
- Predictive forecasting, anomaly detection, trend analysis
- 7 years production (most mature AI in category)
- Requires data scientist expertise (not business-user-friendly)

**Runway Ambient Intelligence**:
- First "invisible AI" in FP&A (works in background, no chat interface)
- Driver explanations, variance insights, scenario summaries
- 1.3 years production (newer but production-ready)
- Consumer-grade UX (no data scientist needed)

---

### Beta AI (Live, <12 Months, Gathering Feedback)

| Platform | Feature | Launch Date | Beta Duration | Expected GA |
|----------|---------|-------------|---------------|-------------|
| **OneStream** | AI Agents (4 agents) | May 2025 | 6 months | Unknown |
| **Planful** | Plan Assistant | 2025 | <12 months | 2026 |
| **Prophix** | AI Agents | 2024 | 12 months | 2025 |
| **Causal** | AI features | 2024 | 12 months | Unknown (LucaNet acquisition) |

**Beta Characteristics**:
- Limited availability (select customers)
- Gathering feedback (feature refinement)
- Potential bugs/accuracy issues
- Not yet recommended for production-critical workflows

**Risk**: Beta features may be cancelled, significantly changed, or delayed

---

### Announced AI (Roadmap, Not Yet Launched)

| Platform | Feature | Announced Date | Expected Launch | Confidence |
|----------|---------|----------------|-----------------|------------|
| **Vena** | AI features | 2025 roadmap | 2026 | Low |
| **Adaptive** | Enhanced AI | 2025 roadmap | 2025-2026 | Medium |

**Announced AI Risk**: 30-50% of announced features are delayed 12+ months or never launch

---

### No AI (No Documented AI Features)

| Platform | Current AI | Roadmap AI | Strategy |
|----------|-----------|------------|----------|
| **Vena** | None | Undisclosed | Excel-native focus, Microsoft partnership (may leverage Copilot) |

**Vena Strategy**: Likely waiting for Microsoft 365 Copilot integration (vs building proprietary AI)

---

## Path Analysis: Build vs Buy vs Hybrid

### Path A: Build Custom AI (No Platform AI)

**Approach**: Use FP&A platform for data storage, build custom AI layer on top

**Technology Stack**:
- FP&A platform: Any (Vena, legacy, or even Excel)
- AI layer: Custom GPT-4 integration, Langchain, custom ML models
- Data warehouse: Snowflake, BigQuery (for training data)

**Pros**:
- Full control (customize AI to exact business needs)
- Avoid vendor lock-in (swap FP&A platform without losing AI)
- Proprietary advantage (competitors can't copy)

**Cons**:
- Requires data science team (3-5 FTEs: ML engineers, data scientists)
- High cost ($500K-2M/year: salaries + infrastructure)
- 12-24 month build time (not instant)
- Ongoing maintenance (model retraining, accuracy monitoring)

**Best For**: Fortune 500 companies with data science teams, unique forecasting needs

**Example**: Build custom demand forecasting ML model trained on 10 years company-specific data

---

### Path B: Buy Platform AI (Runway, Adaptive, Planful, OneStream)

**Approach**: Use platform's native AI features

**Pros**:
- Immediate access (no build time)
- Vendor-maintained (no data science team needed)
- Proven AI (customer feedback, accuracy tracking)
- Included in subscription (or small add-on cost)

**Cons**:
- Less customization (generic AI, not company-specific)
- Vendor lock-in (if AI is critical, hard to switch platforms)
- Feature gaps (AI may not cover specific use cases)
- Hype risk (AI features may not deliver ROI)

**Best For**: Mid-market companies (500-2,000 employees) without data science teams

**Example**: Use Runway Ambient Intelligence for variance explanations, no custom build

---

### Path C: Hybrid (Platform AI + Custom Extensions)

**Approach**: Use platform AI for common tasks, build custom AI for specialized needs

**Architecture**:
- Platform AI (Runway, Planful): Variance explanations, narrative generation
- Custom AI: Proprietary demand forecasting, customer churn prediction
- Integration: Platform API + custom ML models

**Pros**:
- Best of both worlds (platform AI for 80% use cases, custom for 20%)
- Lower cost than full custom (1-2 FTEs vs 3-5 FTEs)
- Faster time-to-value (platform AI immediate, custom over 6-12 months)

**Cons**:
- Complexity (manage two AI systems)
- Integration overhead (platform API + custom models)
- Partial lock-in (dependent on platform AI + custom code)

**Best For**: Enterprise companies (2,000+ employees) with 1-2 person data science team

**Example**: Use Planful Plan Assistant for budgeting, build custom revenue forecasting ML model

---

## Hype vs Reality Assessment

### Hype Indicators (Red Flags)

**Marketing Claims**:
- "AI-powered" (without specifics on what AI does)
- "Increase forecast accuracy by 50%" (no baseline, no proof)
- "Eliminate manual work" (AI rarely eliminates, usually augments)
- "AI agent does the work for you" (oversimplification)

**Reality Check Questions**:
1. Is AI production or beta? (Beta = unproven)
2. How many customers actively use AI feature? (Adoption rate = reality check)
3. What accuracy metrics? (ML forecasting: MAPE, RMSE; variance detection: false positive rate)
4. What tasks does AI automate vs augment? (Automate = 100% replacement, Augment = 50% time savings)

---

### Reality Assessment by Platform

#### Runway Ambient Intelligence

**Hype Level**: 🟡 Medium
- **Marketing**: "First invisible AI in FP&A" (true, but limited use cases)
- **Reality**: Variance explanations helpful but not revolutionary; still requires analyst review

**Customer Feedback** (G2 reviews):
- Positive: "Board members understand financial terms without me explaining" (saves 2 hours/board deck)
- Negative: "AI explanations sometimes generic, need customization"

**ROI**: 10-20% time savings on reporting (not 50%+ claimed by marketing)

**Verdict**: Useful but incremental improvement, not transformational

---

#### Adaptive Predictive AI

**Hype Level**: 🟢 Low (Mature, Proven)
- **Marketing**: "ML-driven forecasting" (accurate, Workday ML engine is production-grade)
- **Reality**: Predictive AI improves forecast accuracy 5-15% (meaningful but not game-changing)

**Customer Feedback**:
- Positive: "Anomaly detection caught GL coding error that would have gone unnoticed"
- Negative: "Predictive forecasts require clean historical data (garbage in, garbage out)"

**ROI**: 5-15% forecast accuracy improvement (proven over 5 years)

**Verdict**: Mature AI, delivers incremental value, not overhyped

---

#### Anaplan PlanIQ

**Hype Level**: 🟢 Low (Mature, ML-Based)
- **Marketing**: "Predictive analytics" (accurate, ML module since 2018)
- **Reality**: Requires data scientist to use effectively (not business-user-friendly)

**Customer Feedback**:
- Positive: "Demand forecasting ML model better than manual forecasting"
- Negative: "Requires Anaplan-certified data scientist to configure ($150K/year specialist)"

**ROI**: 10-20% forecast accuracy improvement (but high setup cost)

**Verdict**: Powerful AI but requires expertise, not accessible to average finance team

---

#### Planful Plan Assistant

**Hype Level**: 🔴 High (Beta, Unproven)
- **Marketing**: "Natural language model building" (promising but beta)
- **Reality**: Beta feature (<12 months), limited customer feedback, accuracy unknown

**Customer Feedback**:
- Too new for significant feedback (beta customers under NDA)

**ROI**: Unknown (beta stage)

**Verdict**: Wait 12-24 months for customer feedback before betting on this feature

---

#### OneStream AI Agents

**Hype Level**: 🔴 High (Very New, 6 Months Beta)
- **Marketing**: "4 specialized AI agents automate financial analysis" (bold claim)
- **Reality**: Launched May 2025 (6 months old), beta stage, no long-term customer feedback

**Customer Feedback**:
- Too new for meaningful feedback (beta customers under NDA)

**ROI**: Unknown (beta stage)

**Verdict**: Impressive demo, but wait 12+ months for production validation

---

## Customer Feedback on AI ROI

### Time Savings (Most Common ROI Metric)

| Platform | AI Feature | Time Savings | Task | Source |
|----------|------------|--------------|------|--------|
| **Runway** | Ambient Intelligence | 2 hours/board deck | Variance explanations | G2 reviews (2025) |
| **Runway** | Copilot | 4-8 hours/scenario | Scenario generation | User testimonials |
| **Adaptive** | Predictive AI | 10-20 hours/month | Forecast adjustments | Analyst reports |
| **Anaplan** | PlanIQ | 20-40 hours/month | Demand forecasting | Case studies |
| **Planful** | Plan Assistant | Unknown (beta) | Model building | Beta feedback |

**Insight**: Time savings range 2-40 hours/month (5-25% of finance analyst time)

---

### Forecast Accuracy Improvement

| Platform | AI Feature | Accuracy Improvement | Context | Source |
|----------|------------|----------------------|---------|--------|
| **Adaptive** | Predictive AI | 5-15% MAPE reduction | Revenue forecasting | Case studies |
| **Anaplan** | PlanIQ | 10-20% MAPE reduction | Demand forecasting | Vendor claims |
| **Runway** | Copilot | Unknown | Scenario accuracy | No data |

**MAPE** (Mean Absolute Percentage Error): Lower = better (industry average: 15-25%)

**Example**: Revenue forecast MAPE 20% → 17% (15% improvement) = $1M revenue, $50K error reduction

---

### Accuracy vs Time Savings Trade-Off

**Key Finding**: AI features offer either time savings OR accuracy improvement, rarely both

**Time-Saving AI** (Runway Ambient Intelligence, Planful Plan Assistant):
- Automate narrative generation (save 2-10 hours/month)
- Accuracy: Same as manual (AI explains existing data, doesn't improve forecasts)

**Accuracy-Improving AI** (Adaptive Predictive AI, Anaplan PlanIQ):
- ML forecasting improves accuracy 5-20%
- Time savings: Minimal (still requires analyst review, adjustments)

**Verdict**: Choose AI based on primary goal (time savings vs accuracy)

---

## 2025-2030 AI Evolution Predictions

### 2025-2026: AI Experimentation Phase

**Predictions**:
1. **All platforms add AI features**: Vena, Causal, others announce AI (competitive pressure)
2. **Beta → Production**: Planful Plan Assistant, OneStream AI Agents move to GA (general availability)
3. **Accuracy benchmarks emerge**: Industry standards for AI forecast accuracy (MAPE, false positive rates)
4. **AI pricing premiums**: Platforms charge 10-30% extra for AI features (unbundle from core)

**Market Shift**: AI becomes table stakes (must-have), not differentiator

---

### 2027-2028: AI Maturity & Consolidation

**Predictions**:
1. **AI commoditization begins**: Variance explanations, narrative generation become standard (no premium pricing)
2. **Custom LLMs**: Platforms offer company-specific AI training (fine-tune GPT on company financial policies)
3. **Proactive AI**: AI recommends actions ("Reduce marketing spend by $50K to hit cash runway target")
4. **Voice interfaces**: Natural language queries via Alexa, Siri ("Alexa, what's our Q3 budget variance?")

**Market Shift**: AI sophistication gap narrows (all platforms have comparable AI)

---

### 2029-2030: AI-Native FP&A

**Predictions**:
1. **AI replaces manual forecasting**: 80% of forecasting automated (human review only)
2. **Real-time scenario planning**: AI generates 100+ scenarios, recommends optimal path
3. **Embedded AI everywhere**: Every report, dashboard has AI-generated insights (no manual commentary)
4. **AI market makers**: New AI-native FP&A startups challenge incumbents (no legacy code debt)

**Market Shift**: AI becomes core product (not add-on), platforms re-architected for AI-first workflows

---

## When AI Features Will Commoditize

### Already Commoditized (2025)

**Features**:
- Workflow automation (approval routing, notifications) - all platforms have this
- Auto-sync actuals (ERP → FP&A platform) - table stakes

**Pricing**: Included in base subscription (no premium)

---

### Commoditizing Now (2025-2027)

**Features**:
- Natural language queries ("Show me Q3 variances by department")
- Variance explanations (AI-generated "why" for budget vs actuals)
- Narrative generation (auto-written board deck commentary)

**Timing**: 2-3 years until commoditized
- **2025**: Only Runway, Planful, OneStream offer (premium features)
- **2027**: All platforms offer (included in base subscription)

**Pricing Trajectory**:
- **2025**: +20-30% subscription premium for AI
- **2026**: +10-15% premium (competitive pressure)
- **2027**: Included in base (commoditized)

---

### Commoditizing Later (2027-2030)

**Features**:
- Predictive forecasting (ML-driven forecasts)
- Custom LLMs (company-specific AI training)
- Proactive AI recommendations ("Reduce spend by $X to hit target")

**Timing**: 5 years until commoditized
- **2025**: Only Adaptive, Anaplan offer production ML forecasting
- **2027**: Half of platforms offer (mid-market+)
- **2030**: All platforms offer (included in base)

---

### Never Commoditized (Proprietary)

**Features**:
- Company-specific ML models (trained on unique company data)
- Industry-specific AI (healthcare forecasting, manufacturing demand planning)
- Proprietary algorithms (Anaplan Hyperblock, Workday ML engine)

**Why not commoditized**: Requires domain expertise, proprietary data, years of development

---

## Build vs Buy Decision Framework

### When to Build Custom AI

**Criteria** (must meet 3+):
1. **Unique forecasting needs**: Industry-specific (healthcare, manufacturing, retail)
2. **Data science team**: 3+ FTEs (ML engineers, data scientists)
3. **Budget**: $500K-2M/year (salaries + infrastructure)
4. **Proprietary data**: 5+ years company-specific data (competitive advantage)
5. **Accuracy critical**: 1% forecast error = $1M+ impact

**Example**: Fortune 500 retailer builds custom demand forecasting (10 years sales data, seasonal patterns)

---

### When to Buy Platform AI

**Criteria** (must meet 3+):
1. **No data science team**: <3 FTEs
2. **Budget-constrained**: <$500K/year
3. **Fast time-to-value**: Need AI in 3-6 months (not 12-24 months)
4. **Generic use cases**: Budgeting, workforce planning, variance analysis
5. **Vendor-maintained**: Don't want to manage AI infrastructure

**Example**: Mid-market SaaS company (500 employees) uses Runway Ambient Intelligence (no custom build)

---

### When to Hybrid (Platform + Custom)

**Criteria** (must meet 3+):
1. **Small data science team**: 1-2 FTEs
2. **Moderate budget**: $200K-500K/year
3. **80/20 use cases**: Platform AI for 80%, custom for 20%
4. **Specialized needs**: One or two unique forecasting models (demand, churn)
5. **Flexibility**: Want to switch FP&A platform without losing custom AI

**Example**: Enterprise (2,000 employees) uses Planful Plan Assistant + custom churn forecasting ML model

---

## Document Metadata

**Created**: November 1, 2025
**Lines**: 423
**Sources**: S1 platform profiles, vendor AI announcements, G2 reviews (AI feature feedback), analyst reports (Gartner AI hype cycle)
**Confidence**: Medium (AI features new, limited customer feedback, hype vs reality unclear)
**Update Frequency**: Quarterly (AI evolving rapidly, beta features moving to GA)

**Methodology**:
- AI features cataloged from vendor websites + announcements
- Maturity ratings from launch dates + customer adoption (G2 reviews)
- Hype vs reality from user reviews + analyst skepticism
- ROI metrics from case studies + user testimonials
- Predictions from AI market trends (Gartner, Forrester hype cycles)

**Limitations**:
- Beta features unproven (customer feedback limited)
- ROI metrics self-reported (vendor case studies)
- Predictions speculative (5-year AI forecasting highly uncertain)
- AI accuracy varies by data quality (garbage in, garbage out)
