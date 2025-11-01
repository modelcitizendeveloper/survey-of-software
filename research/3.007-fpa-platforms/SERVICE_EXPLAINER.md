# FP&A Platforms - Service Explainer

**Experiment**: 3.007
**Category**: Business Platforms (Tier 3)
**Audience**: Business decision-makers, CFOs, finance leaders
**Purpose**: Explain FP&A domain concepts for non-specialists

---

## What is FP&A?

**FP&A** = **Financial Planning & Analysis**

The strategic finance function responsible for budgeting, forecasting, and financial decision-making. FP&A teams answer questions like:
- "How much can we afford to spend on hiring next quarter?"
- "What happens to our cash runway if revenue drops 20%?"
- "Should we invest in Product A or Product B?"

---

## Core FP&A Activities

### 1. Budgeting
Creating annual/quarterly spending plans across departments.

**Example**: Engineering department gets $2M budget for Q1 (salaries, tools, contractors).

**Timeframe**: Annual (reviewed quarterly)

### 2. Forecasting
Predicting future financial outcomes based on current trends.

**Example**: "Based on current growth, we'll reach $10M ARR in 18 months."

**Timeframe**: Rolling 12-18 months (updated monthly)

### 3. Workforce Planning
Modeling headcount changes, compensation, and hiring timelines.

**Example**: "Hire 5 engineers starting July 1, average salary $150K, ramp to productivity in 3 months."

**Timeframe**: Quarterly hiring plans

### 4. Scenario Modeling
Comparing "what-if" financial strategies.

**Example**: Compare 3 scenarios:
- **Optimistic**: Revenue grows 50%, hire aggressively
- **Base**: Revenue grows 30%, moderate hiring
- **Pessimistic**: Revenue grows 10%, hiring freeze

**Timeframe**: Strategic planning (annual), crisis planning (ad-hoc)

### 5. Financial Consolidation
Rolling up multi-entity financial results into unified reports.

**Example**: Parent company owns 3 subsidiaries in different countries → consolidate to single P&L with currency translation and intercompany eliminations.

**Timeframe**: Monthly close process

### 6. Variance Analysis
Comparing actuals vs budget/forecast, explaining differences.

**Example**: "Marketing spent $50K over budget because we launched unexpected campaign."

**Timeframe**: Monthly

---

## FP&A vs Related Functions

| Function | Focus | Output | Owner |
|----------|-------|--------|-------|
| **FP&A** | Strategic planning, forecasting | Budgets, scenarios, board decks | Finance team |
| **Accounting** | Historical recording, compliance | Financial statements, tax returns | Controllers |
| **Treasury** | Cash management, liquidity | Cash flow monitoring, banking | Treasurer |
| **Corporate Finance** | Capital allocation, M&A | Investment analysis, deal models | CFO |

**Overlap**: FP&A uses accounting data (actuals) and informs treasury (cash forecasts).

---

## FP&A Tools Evolution

### Stage 1: Spreadsheets (1-50 employees)
**Tool**: Excel or Google Sheets

**Strengths**:
- Free (or cheap)
- Familiar to everyone
- Infinite flexibility

**Limitations**:
- Manual data entry (copy-paste from accounting system)
- Version control chaos ("Budget_v3_final_FINAL.xlsx")
- No audit trail (who changed what?)
- Breaks easily (circular references, broken formulas)

**Breaking Point**: 50+ employees, multiple departments, complex hiring plans

---

### Stage 2: Cash Flow Tools (50-200 employees)
**Examples**: Pulse, Fathom, Finmark (see 3.004 Cash Flow research)

**Strengths**:
- Auto-sync with accounting (QuickBooks, Xero)
- Cash runway tracking
- Simple scenario modeling

**Limitations**:
- Limited workforce planning (can't model complex org charts)
- No consolidation (multi-entity companies)
- No departmental budgeting workflows
- Read-only integrations (don't push budgets back to systems)

**Breaking Point**: 200+ employees, need workforce planning, multi-entity structure

---

### Stage 3: FP&A Platforms (200+ employees)
**Examples**: Runway, Planful, Anaplan (this research)

**Strengths**:
- Full workforce planning (org charts, compensation bands, hiring timelines)
- Departmental budgets with approval workflows
- Multi-scenario modeling (3-10 scenarios in parallel)
- Consolidation (multi-entity, multi-currency)
- Two-way integrations (pull actuals from accounting, push headcount to HRIS)

**Limitations**:
- Expensive ($5K-500K/year)
- Implementation complexity (1 week to 12 months)
- Vendor lock-in (migration = 20-200 hours)

**Graduation Trigger**: When Excel models exceed 50 tabs or workforce planning requires dedicated tool.

---

## Key FP&A Concepts

### Driver-Based Planning
Linking business metrics to financial outcomes.

**Example**:
- **Driver**: "Number of sales reps"
- **Financial outcome**: Each rep generates $500K revenue, costs $120K salary
- **Model**: 10 reps → $5M revenue, $1.2M expense

**Benefit**: Change one assumption (15 reps), model automatically recalculates ($7.5M revenue, $1.8M expense).

### Rolling Forecasts
Continuously updated forecasts (vs static annual budgets).

**Traditional Budget**: Set Jan 1, locked for 12 months
**Rolling Forecast**: Update monthly, always looking 12-18 months ahead

**Benefit**: Reflects current reality, not outdated January assumptions.

### Scenario Planning
Modeling multiple futures simultaneously.

**Example**: 3 revenue scenarios (optimistic/base/pessimistic) × 3 hiring scenarios (aggressive/moderate/freeze) = 9 total scenarios

**Benefit**: Prepare contingency plans before crisis hits.

### Consolidation
Combining financial results from multiple entities.

**Challenges**:
- **Currency translation**: Subsidiary reports in EUR, parent needs USD
- **Intercompany eliminations**: Subsidiary A sells $1M to Subsidiary B → eliminate to avoid double-counting
- **Different GAAP**: US GAAP vs IFRS differences

**Why it matters**: Public companies required to consolidate; private equity portfolios need unified view.

---

## FP&A Platform Categories

### Tier 1: Startup FP&A ($3K-30K/year)
- **Target**: 20-500 employees
- **Setup**: 1-4 weeks
- **Use case**: Headcount planning, department budgets, basic scenarios
- **Examples**: Runway, Causal, Finmark (overlaps with 3.004 cash flow tools)

### Tier 2: Mid-Market ($15K-100K/year)
- **Target**: 250-2000 employees
- **Setup**: 1-3 months
- **Use case**: Driver-based planning, workforce planning, consolidation
- **Examples**: Vena, Prophix, Adaptive Insights

### Tier 3: Enterprise CPM ($50K-500K/year)
- **Target**: 2000+ employees
- **Setup**: 3-12 months
- **Use case**: Connected planning (finance + sales + supply chain), complex consolidation, predictive analytics
- **Examples**: Planful, Anaplan, OneStream

**CPM** = Corporate Performance Management (broader than FP&A, includes operational planning)

---

## Integration Requirements

FP&A platforms must integrate with:

### Accounting Systems (Pull Actuals)
- QuickBooks, Xero, NetSuite, Sage Intacct
- **Data flow**: General ledger actuals → FP&A (for variance analysis)

### HRIS (Pull Headcount, Push Plans)
- Rippling, Gusto, Workday, ADP
- **Data flow**: Employee data (salary, title, start date) → FP&A for workforce planning
- **Reverse flow**: Hiring plan → HRIS (optional)

### CRM (Pull Pipeline)
- Salesforce, HubSpot
- **Data flow**: Sales pipeline → FP&A for revenue forecasting

### Data Warehouses (Pull Custom Metrics)
- Snowflake, BigQuery, Redshift
- **Data flow**: Product analytics, usage data → FP&A for unit economics

**Integration Quality Matters**: Poor integration = manual data entry = defeats purpose of FP&A platform.

---

## When Do You Need FP&A Platform?

### You DON'T need FP&A platform if:
- ❌ Under 50 employees (Excel sufficient)
- ❌ Single founder/finance person (no collaboration needed)
- ❌ Simple business model (no departments, no hiring plan)
- ❌ Stable headcount (not hiring)

**Recommendation**: Stay in Excel or use cash flow tool (3.004).

---

### You MIGHT need FP&A platform if:
- ⚠️ 50-200 employees
- ⚠️ Multiple departments with separate budgets
- ⚠️ Hiring 5-10 people per quarter
- ⚠️ Board requires scenario analysis

**Recommendation**: Evaluate Tier 1 startup FP&A platforms (Runway, Causal, Finmark).

---

### You DEFINITELY need FP&A platform if:
- ✅ 200+ employees
- ✅ Complex hiring plans (50+ hires/year across departments)
- ✅ Multi-entity structure (need consolidation)
- ✅ Excel model has 50+ tabs or breaks frequently
- ✅ Multiple people collaborating on budget (need version control, workflows)

**Recommendation**: Tier 1-3 FP&A platform depending on company size.

---

## Build vs Buy

### When to Build Custom FP&A System
**Almost never.**

**Exceptions**:
- Large data engineering team (10+ engineers)
- Unique business model not supported by platforms
- Budget >$250K/year for FP&A platform (DIY 3-year TCO may be lower)

**Typical DIY Cost**: $30K-60K initial build + $10K-20K/year maintenance = $50K-100K over 3 years.

**Breakeven**: Only economical if platform costs >$2K/month ($24K/year).

---

### When to Buy FP&A Platform
**Almost always** for companies 50+ employees.

**Why**:
- Workforce planning logic is complex (org charts, compensation bands, benefits)
- Consolidation is non-trivial (currency, GAAP differences)
- Collaboration features hard to build (audit trails, approval workflows)
- Finance teams don't want to debug code

---

## Common Misconceptions

### "FP&A platforms replace accountants"
**False.** FP&A platforms consume accounting data (actuals), don't replace accounting function.

### "FP&A = forecasting"
**Partial.** Forecasting is one activity; also includes budgeting, workforce planning, scenario analysis, consolidation.

### "We can do this in Excel"
**True for small companies (<50 employees).** False when:
- Multiple collaborators (version control nightmare)
- Complex workforce planning (org charts with 100+ employees)
- Multi-entity consolidation (currency, eliminations)

### "FP&A platforms are expensive"
**True** ($5K-500K/year), but compare to:
- Finance team salaries ($150K-300K per person)
- Excel errors costing incorrect decisions ($100K-1M+ in bad hires, overspending)
- Board/investor confidence (worth the investment)

### "Implementation is quick"
**Sometimes.** Tier 1 platforms (Runway): 1-2 weeks. Enterprise (Anaplan): 3-12 months.

---

## FP&A Maturity Model

### Level 1: Excel-Based (1-50 employees)
- **Budget**: Annual budget in Excel
- **Forecast**: Quarterly updates (if at all)
- **Scenarios**: None (or 1 best-guess)
- **Headcount**: Hiring ad-hoc, no formal plan

### Level 2: Cash Flow Tools (50-200 employees)
- **Budget**: Auto-sync with accounting for actuals
- **Forecast**: Monthly updates
- **Scenarios**: 2-3 scenarios (optimistic/base/pessimistic)
- **Headcount**: Simple headcount plan (count + salary)

### Level 3: FP&A Platform (200-2000 employees)
- **Budget**: Departmental budgets with approval workflows
- **Forecast**: Rolling forecasts updated monthly
- **Scenarios**: 5-10 scenarios modeled in parallel
- **Headcount**: Full workforce planning (org chart, comp bands, ramp time)

### Level 4: Enterprise CPM (2000+ employees)
- **Budget**: Connected planning (finance + sales + supply chain + HR)
- **Forecast**: Real-time updates, predictive AI
- **Scenarios**: Monte Carlo simulation, sensitivity analysis
- **Headcount**: Workforce analytics (turnover prediction, succession planning)

---

## Document Status

**Created**: November 1, 2025
**Purpose**: Explain FP&A concepts for business decision-makers
**Audience**: CFOs, finance leaders, non-finance executives evaluating FP&A platforms
**Related Research**: 3.004 (Cash Flow Tools), 3.503 (HRIS - provides headcount data to FP&A)
