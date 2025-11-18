# fs-train: Financial Analysis Fluency Trainer

**Design Specification v1.0**
**Date**: 2025-01-18
**Pattern**: Apply latin-train methodology to financial statement analysis

---

## 🎯 Design Philosophy

**Goal**: Teach users to **read and analyze financial statements fluently**

Just as latin-train teaches grammar pattern recognition through rapid repetition, fs-train teaches financial pattern recognition through guided exploration.

**NOT**: A spreadsheet replacement (that's Excel)
**NOT**: Automated analysis (that's AI tools)
**IS**: Interactive exploration with intelligent feedback

---

## 🏗️ Architecture Overview

### Core Components

```
┌─────────────────────────────────────────┐
│      Training Scenario (YAML)           │
│  - Company data                         │
│  - Key insights (ground truth)          │
│  - Difficulty level                     │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│         View Engine                     │
│  - Pre-calculate all views              │
│  - [default], [mom], [margin], etc.     │
│  - Dynamic comparisons                  │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│      Interactive Session                │
│  - Display views on request             │
│  - Capture user observations            │
│  - Track exploration path               │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│         LLM Scorer                      │
│  - Parse observations                   │
│  - Score against ground truth           │
│  - Generate feedback                    │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│      Results & Analytics                │
│  - What user caught                     │
│  - What user missed                     │
│  - Time spent, depth reached            │
└─────────────────────────────────────────┘
```

---

## 📊 View System

### Standard Views (Pre-Calculated)

#### 1. [default] - Absolute Values
```
── Income Statement ────────────────────────
                        Jan      Feb      Mar
Revenue               $75,000  $82,000  $90,000
COGS                  $22,500  $24,600  $27,000
Gross Profit          $52,500  $57,400  $63,000
Operating Expenses    $53,000  $55,000  $62,000
Operating Income      -$2,500     $450  -$1,100
```

#### 2. [%] - Percentage of Revenue
```
── % of Revenue ────────────────────────────
                        Jan      Feb      Mar
Revenue              100.0%   100.0%   100.0%
COGS                  30.0%    30.0%    30.0%
Gross Profit          70.0%    70.0%    70.0%
Operating Expenses    70.7%    67.1%    68.9%
Operating Income      -3.3%    +0.5%    -1.2%
```

#### 3. [mom] - Month-over-Month Growth
```
── Month-over-Month Growth (%) ─────────────
                     Jan→Feb  Feb→Mar  Q1 Avg
Revenue               +9.3%    +9.8%   +9.5%
COGS                  +9.3%    +9.8%   +9.5%
Gross Profit          +9.3%    +9.8%   +9.5%
Operating Expenses    +3.8%   +12.7%   +8.2%
  Salaries               0%   +12.5%   +6.3%
  Marketing          +25.0%   +20.0%  +22.5%
  Rent                   0%       0%      0%
```

#### 4. [margin] - Margin Analysis
```
── Margin Trends ───────────────────────────
                        Jan      Feb      Mar    Trend
Gross Margin          70.0%    70.0%    70.0%    →
Operating Margin      -3.3%    +0.5%    -1.2%    ↓
Net Margin            -3.6%    +0.3%    -1.4%    ↓

💡 Stable gross margin = good pricing power
⚠️ Declining operating margin = expense growth outpacing revenue
```

#### 5. [detail] - Full Line-Item Breakdown
```
── Detailed P&L ────────────────────────────
Revenue
  Product Sales      $50,000  $55,000  $60,000
  Consulting         $25,000  $27,000  $30,000
Total Revenue        $75,000  $82,000  $90,000

Cost of Goods Sold
  Product Costs      $15,000  $16,500  $18,000
  Service Delivery    $7,500   $8,100   $9,000
Total COGS          $22,500  $24,600  $27,000

Operating Expenses
  Salaries           $40,000  $40,000  $45,000
  Marketing           $8,000  $10,000  $12,000
  Rent                $5,000   $5,000   $5,000
  Software            $1,200   $1,200   $1,200
  Office Supplies       $800     $750     $900
Total OpEx          $55,000  $56,950  $64,100

Other Income/Expense
  Interest Expense      $200     $200     $200
```

#### 6. [cash] - Cash Flow & Runway
```
── Cash Flow Analysis ──────────────────────
                        Jan      Feb      Mar
Operating Income     -$2,500     $450  -$1,100
Cash from Ops        -$2,500     $450  -$1,100

Starting Cash       $100,000  $97,500  $97,950
Ending Cash          $97,500  $97,950  $96,850

Burn Rate            -$2,500     +$450  -$1,100
Runway (months)          ~40      N/A      ~88

⚠️ March burn resuming after Feb profitability
💡 Still plenty of runway but trend concerning
```

#### 7. [ratios] - Key Financial Ratios
```
── Financial Ratios ────────────────────────
                        Jan      Feb      Mar
CAC Payback (months)    2.4      2.8      3.0  ↑
LTV/CAC Ratio           3.2      2.9      2.7  ↓
Rule of 40             35.0%    39.5%    38.3%
Magic Number            1.1      1.3      1.1

💡 CAC payback increasing = marketing efficiency declining
⚠️ LTV/CAC below 3.0 is concerning for SaaS
```

### Dynamic Views (On Demand)

#### [compare X Y] - Compare Two Line Items
```
> compare revenue marketing

── Revenue vs Marketing ────────────────────
                        Jan      Feb      Mar
Revenue               $75,000  $82,000  $90,000
Marketing              $8,000  $10,000  $12,000
Marketing % of Rev     10.7%    12.2%    13.3%  ↑

💡 Marketing growing faster than revenue
   Jan→Feb: Mkt +25%, Rev +9.3%
   Feb→Mar: Mkt +20%, Rev +9.8%

⚠️ If this trend continues, CAC will become unsustainable
```

#### [trend X] - Focus on Single Item
```
> trend salaries

── Salary Trend Analysis ───────────────────
                        Jan      Feb      Mar
Salaries           $40,000  $40,000  $45,000
Change                  --       $0   +$5,000
% Change                --       0%   +12.5%

💡 March spike suggests new hire
   At $5K/month = ~$60K annual salary
   Likely mid-level role (engineer, sales, etc.)

❓ Question to investigate:
   Will this hire drive revenue growth to justify cost?
```

### View Constraints (Prevent Excel Creep)

**✅ Allowed**:
- Pre-defined financial views
- Common ratio calculations
- Simple comparisons (2 items max)
- Trend analysis for single items

**❌ Not Allowed**:
- Arbitrary formulas
- Multi-step calculations
- Cell-level editing
- Custom charts/graphs
- Pivot tables

**Philosophy**: Provide analyst tools, not spreadsheet tools. Keep focus on pattern recognition and insight generation.

---

## 🤖 LLM Integration

### Scoring System

**Hybrid Approach**:
1. **Keyword matching** for common patterns (fast, reliable)
2. **LLM evaluation** for nuanced observations (flexible, contextual)

### Pre-Defined Insights (Ground Truth)

Each scenario has known insights:

```yaml
key_insights:
  - id: revenue_growth
    pattern: "revenue.*grow.*|growth.*revenue"
    points: 15
    category: trend_analysis

  - id: margin_stability
    pattern: "gross.*margin.*stable|margin.*constant"
    points: 10
    category: efficiency

  - id: hiring_spike
    pattern: "salary.*increase|new.*hire|salaries.*jump"
    points: 20
    category: operational_change

  - id: cash_burn
    pattern: "cash.*burn|unprofitable|losing.*money"
    points: 10
    category: sustainability
```

### LLM Prompt Template (Observation Scoring)

```
You are a financial analysis instructor evaluating a student's observation.

Financial Statement Summary:
{statement_data}

Known Key Insights (ground truth):
{key_insights}

Student Observation:
"{user_observation}"

Evaluate this observation:

1. Accuracy (0-10): Is it factually correct?
2. Insight Level (0-10): Does it identify something important?
3. Connections (0-10): Does it relate multiple data points?

Match to ground truth insights:
- Which key insights does this observation touch on?
- Are there nuances or connections the student made beyond the ground truth?

Return JSON:
{
  "accuracy_score": 0-10,
  "insight_score": 0-10,
  "connection_score": 0-10,
  "matched_insights": ["revenue_growth", "margin_stability"],
  "bonus_points": 0-10,
  "feedback": "2-3 sentence explanation"
}
```

### LLM Prompt Template (Missing Insights)

```
You are a financial analysis instructor creating constructive feedback.

What the student observed:
{caught_insights}

What the student missed:
{missed_insights}

Generate friendly, educational feedback explaining:
1. Why the missed insights matter
2. How to spot these patterns in future
3. Connections between metrics

Keep it concise (3-4 bullet points) and encouraging.
```

---

## 🎮 User Interaction Flow

### Session Structure

```
1. Display Initial View (default)
2. Show Available Commands
3. Wait for User Input:

   a) View request → Show requested view, return to #3
   b) Observation → Score it, give feedback, return to #3
   c) Prompt request (?) → Show hint, return to #3
   d) Done (Enter) → Generate final score

4. Final Scoring:
   - What user caught (with points)
   - What user missed (with explanations)
   - Total score (0-100)
   - Depth level achieved (Beginner/Intermediate/Advanced)
   - Time spent

5. Next scenario or exit
```

### Difficulty Levels

#### Beginner
- **Prompts**: 3 hints offered automatically
- **Views**: Suggest relevant views ("Try 'show mom'")
- **Insights**: 3-5 obvious patterns
- **Scoring**: Partial credit for correct direction

#### Intermediate
- **Prompts**: Available on request (?)
- **Views**: No suggestions (user explores)
- **Insights**: 5-7 patterns, some subtle
- **Scoring**: Must be specific

#### Advanced
- **Prompts**: Minimal or none
- **Views**: User must know what to request
- **Insights**: 7-10 patterns, requires deep analysis
- **Scoring**: Expected to connect multiple metrics

---

## 📚 Training Scenario Structure

### Scenario Definition (YAML)

```yaml
scenario_id: saas_growth_001
name: "Acme Corp - Growing SaaS Startup"
industry: SaaS
stage: Early Growth
difficulty: beginner
duration_months: 3

company_context:
  description: "B2B SaaS company selling project management software"
  employees: 12
  founded: "2 years ago"
  funding: "Seed round, $500K"

financial_data:
  revenue:
    jan: 75000
    feb: 82000
    mar: 90000

  cogs:
    jan: 22500
    feb: 24600
    mar: 27000

  opex:
    salaries:
      jan: 40000
      feb: 40000
      mar: 45000
    marketing:
      jan: 8000
      feb: 10000
      mar: 12000
    rent:
      jan: 5000
      feb: 5000
      mar: 5000

  cash:
    starting: 100000

key_insights:
  - id: revenue_growth
    description: "Revenue growing consistently at ~9-10% MoM"
    importance: high
    points: 15
    category: growth

  - id: margin_stability
    description: "Gross margin stable at 70%"
    importance: medium
    points: 10
    category: efficiency

  - id: hiring_spike
    description: "March salary increase of $5K indicates new hire"
    importance: high
    points: 20
    category: operational

  - id: marketing_acceleration
    description: "Marketing spend growing faster than revenue (CAC concern)"
    importance: high
    points: 20
    category: efficiency

  - id: unprofitable
    description: "Company still unprofitable despite growth"
    importance: medium
    points: 10
    category: sustainability

  - id: cash_adequate
    description: "Cash runway still healthy (~88 months at Mar burn)"
    importance: low
    points: 5
    bonus: true

  - id: unit_economics_deteriorating
    description: "Feb was profitable but Mar returned to losses (hiring impact)"
    importance: high
    points: 15
    category: trend

prompts:
  beginner:
    - "What do you notice about revenue trends?"
    - "How do the margins look?"
    - "What changed in March?"

  intermediate:
    - "What's happening with expenses?"
    - "Is this company sustainable?"

advanced_bonus:
  - "Calculate CAC payback period trend"
  - "Estimate time to profitability given current trajectory"
  - "Analyze unit economics deterioration"

suggested_views:
  beginner:
    - "Try: show mom"
    - "Try: show margin"
    - "Try: show detail"

story:
  setup: "Acme Corp raised a seed round 6 months ago and has been growing steadily."
  challenge: "They're investing heavily in marketing and just hired a new engineer."
  question: "Can they achieve profitability before running out of cash?"
```

---

## 🎯 Scoring Methodology

### Point Distribution (100 points total)

**Major Insights** (15-20 points each):
- Critical business trends
- Strategic concerns
- Operational changes

**Medium Insights** (10 points each):
- Important metrics
- Efficiency patterns
- Sustainability indicators

**Minor Insights** (5 points each):
- Supporting details
- Context observations

**Advanced Bonus** (5-10 points):
- Connections between metrics
- Strategic implications
- Predictive insights

### Depth Levels

**Surface (0-30 points)**:
- Noticed 1-2 obvious trends
- No exploration beyond default view
- Time: <1 minute

**Basic (31-60 points)**:
- Identified 3-4 key insights
- Used 2-3 views
- Time: 1-2 minutes

**Intermediate (61-80 points)**:
- Caught 5-6 insights
- Explored multiple views
- Made some connections
- Time: 2-4 minutes

**Advanced (81-100 points)**:
- Caught 7+ insights
- Deep exploration
- Connected multiple metrics
- Strategic thinking
- Time: 3-5+ minutes

---

## 📦 Implementation Plan

### Phase 1: Core Engine
1. View Engine (pre-calculate all views)
2. Simple scoring (keyword matching)
3. Basic UI (terminal display)
4. 3 training scenarios

### Phase 2: LLM Integration
1. Observation parsing
2. LLM-based scoring
3. Feedback generation
4. 7 training scenarios

### Phase 3: Polish
1. Progressive difficulty
2. User statistics tracking
3. Improvement over time
4. 15 training scenarios

### Phase 4: Advanced
1. Real company data integration
2. Industry-specific scenarios
3. Competitive analysis
4. Custom scenario creation

---

## 🎓 Educational Progression

### Scenario Sequence (Recommended)

**Week 1: Fundamentals**
1. Simple growth (revenue up, everything else stable)
2. Simple decline (revenue down, fixed costs hurt)
3. Margin compression (revenue flat, costs rising)

**Week 2: Complexity**
4. Growth with investment (hiring, marketing)
5. Profitability vs growth trade-off
6. Seasonal patterns

**Week 3: Nuance**
7. Multiple issues (growth + margin + cash)
8. Strategic pivots (product mix changes)
9. Industry-specific patterns

**Week 4: Real World**
10. Actual company data
11. Competitive comparison
12. Custom analysis

---

## 🔧 Technical Details

### Data Storage

**Scenarios**: YAML files in `scenarios/` directory
**User Progress**: JSONL (append-only log)
**Analytics**: SQLite database (optional)

### Performance

**View Pre-Calculation**: <100ms per scenario
**LLM Scoring**: <2s per observation (batched)
**Total Session**: ~5 minutes per scenario

### Dependencies

**Core**:
- pandas (financial calculations)
- PyYAML (scenario loading)
- blessed (terminal UI)

**LLM**:
- requests (Ollama API)
- ollama-python (optional)

**Optional**:
- sqlite3 (progress tracking)
- matplotlib (future: visual charts)

---

## 🎨 UI/UX Principles

1. **Fast feedback**: Instant view changes, <2s LLM scoring
2. **Clear hierarchy**: Bold headers, subtle hints, emphasized insights
3. **Progressive disclosure**: Start simple, reveal complexity on demand
4. **Encouraging tone**: Celebrate catches, gently note misses
5. **No dead ends**: Always suggest next step

---

**Status**: Design complete, ready for implementation
**Next**: Create 5-10 synthetic training scenarios
