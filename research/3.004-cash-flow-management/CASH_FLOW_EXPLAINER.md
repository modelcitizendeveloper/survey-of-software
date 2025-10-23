# Cash Flow Management: The Explainer

**Target Audience:** Tech founders, CTOs, and business operators new to formal financial planning
**Purpose:** Understand what cash flow management is, why it matters, and when spreadsheets stop working
**Date:** October 22, 2025

---

## What is Cash Flow Management?

**Simple definition:** Tracking money in and money out to make sure you don't run out of cash.

**Why it's not just "look at your bank account":** Your bank balance is a snapshot of RIGHT NOW. Cash flow management is about predicting the FUTURE:
- Will you have enough cash in 30 days when payroll is due?
- Can you afford to hire 2 engineers next quarter?
- If a customer doesn't pay for 60 days, will you run out of money?
- Should you take that $500K investment or can you bootstrap?

**The brutal truth:** Profitable companies can die from running out of cash (revenue booked ≠ cash collected). Unprofitable companies can survive for years with good cash flow planning.

---

## Core Concepts (Refresher)

### 1. Cash Flow vs. Profit

**Profit (Accrual Accounting):**
- You invoice customer $100K on January 1st → you're profitable in January
- Customer pays you in March → you have cash in March

**Cash Flow (Reality):**
- You have $0 in January (invoice sent but not paid)
- You have $100K in March (payment received)
- If payroll is $50K/month, you need a bridge from January → March

**Why this matters:** SaaS companies book annual contracts upfront (profitable on paper) but collect monthly (cash flow problem). You can be "profitable" and still run out of money.

---

### 2. Cash Runway

**Definition:** How many months until you run out of cash?

**Formula:**
```
Cash Runway = Cash in Bank / Monthly Burn Rate

Example:
$500K in bank / $50K/month burn = 10 months runway
```

**Founder anxiety levels:**
- 18+ months runway: Sleep well
- 12-18 months: Start thinking about fundraising
- 6-12 months: Actively fundraising
- 3-6 months: Panic mode
- <3 months: Emergency layoffs

**Why 18 months is the magic number:** Fundraising takes 6 months. You need 12 months operating runway + 6 months fundraising buffer.

---

### 3. Burn Rate

**Definition:** How much cash you're spending per month (ignoring revenue).

**Gross Burn Rate:** All expenses (payroll, SaaS tools, office, marketing)
**Net Burn Rate:** Expenses minus revenue

**Example:**
- Expenses: $100K/month
- Revenue: $30K/month
- Gross burn: $100K/month
- Net burn: $70K/month

**Why founders track both:**
- Gross burn = "how fast would we die if revenue stopped?"
- Net burn = "how fast are we losing money?"

**Typical burn rates by stage:**
- Pre-seed (5 people): $50K/month
- Seed (10 people): $100K/month
- Series A (30 people): $300K/month
- Series B (100 people): $1M+/month

---

### 4. The Three Financial Statements

Most cash flow platforms forecast all three (not just cash flow):

**Income Statement (P&L):**
- Revenue (what you earned)
- Expenses (what you spent)
- Profit/Loss (revenue - expenses)

**Balance Sheet:**
- Assets (what you own: cash, inventory, receivables)
- Liabilities (what you owe: loans, payables)
- Equity (assets - liabilities)

**Cash Flow Statement:**
- Operating activities (normal business)
- Investing activities (buying assets)
- Financing activities (raising capital, debt)

**Why all three matter:**
- P&L: Are we profitable? (accrual accounting)
- Balance Sheet: Do we have assets to cover liabilities?
- Cash Flow: Will we run out of cash? (reality check)

**Example of divergence:**
- P&L says you're profitable ($100K profit)
- But you bought $200K in inventory (cash went down)
- Cash flow statement shows you're cash-negative even though profitable

---

### 5. Cash Flow Forecasting

**Definition:** Predicting future cash position based on expected revenue and expenses.

**Simple forecast (3 months):**
```
Month 1:
Starting cash: $100K
Revenue collected: +$30K
Expenses paid: -$50K
Ending cash: $80K

Month 2:
Starting cash: $80K
Revenue collected: +$35K
Expenses paid: -$55K
Ending cash: $60K

Month 3:
Starting cash: $60K
Revenue collected: +$40K
Expenses paid: -$60K
Ending cash: $40K

Trend: Runway shrinking (6 months → 4 months → 2.7 months)
Action: Cut costs or raise money NOW
```

**Why forecasting matters more than actuals:**
- Actuals tell you what happened (too late to fix)
- Forecasts tell you what WILL happen (time to act)

---

### 6. Scenario Planning

**Definition:** Model multiple possible futures ("what if?").

**Example scenarios:**
- **Base case:** 10% monthly revenue growth, current expenses
- **Best case:** 20% growth, same expenses → runway extends
- **Worst case:** 0% growth, same expenses → runway shrinks fast
- **Fundraising scenario:** Raise $2M in 3 months, hire 10 people
- **Customer churn scenario:** Lose 2 big customers, revenue drops 30%

**Why founders love scenario planning:**
- "Should I hire 5 engineers or 3?" → Model both scenarios
- "Can I survive if big customer leaves?" → Model churn scenario
- "Do I need to fundraise or can I bootstrap?" → Model both paths

---

## When Spreadsheets Stop Working

### Stage 1: Spreadsheet is Fine (0-10 employees, <$1M revenue)

**What you're doing:**
- Simple Google Sheet with monthly revenue/expenses
- Bank balance + rough monthly burn = good enough
- Update monthly or quarterly

**Why it works:**
- Few variables (5-10 expense categories)
- Simple revenue model (handful of customers)
- Founder knows all numbers by heart

**Tools:** Google Sheets, Excel

---

### Stage 2: Spreadsheet Becomes Painful (10-50 employees, $1M-10M revenue)

**Pain points:**
- **Manual data entry:** Copy actuals from QuickBooks every month (2-4 hours)
- **Version hell:** "Which file is latest? v12_final_FINAL_v2?"
- **No collaboration:** Founder, CFO, board all want different views
- **Breaking formulas:** Change one cell, 10 formulas break
- **Scenario fatigue:** Copying tabs for 5 scenarios = maintenance nightmare

**Signs you need a tool:**
- Spending 4+ hours/month updating forecast
- Board asks "what's our runway?" and you need 2 days to answer
- Building hiring plans in separate sheets, can't connect to cash flow
- Fundraising soon, need professional investor reports

**Tools:** Cash flow SaaS platforms (Pulse, Finmark, etc.)

---

### Stage 3: Spreadsheet is Impossible (50-500 employees, $10M-100M revenue)

**Why spreadsheets fail:**
- **Multi-entity consolidation:** 3 legal entities = 3 spreadsheets to merge manually
- **Real-time needs:** Can't wait for month-end to update forecast
- **Complex dependencies:** Revenue model has 20 variables, expenses have 50 categories
- **Team collaboration:** Finance team of 5-10 people all editing same sheet = chaos
- **Audit requirements:** Need version control, change tracking, approval workflows

**You need enterprise FP&A:**
- Multi-user collaboration (not just "view-only")
- Real-time data integrations (QuickBooks, Xero, Stripe auto-sync)
- Scenario management (not copy-paste tabs)
- Professional reports (board deck, investor updates)
- Audit trails (who changed what, when)

**Tools:** Enterprise FP&A platforms (Causal, Mosaic, Dryrun, Anaplan)

---

## Types of Cash Flow Tools

### Type 1: Simple Cash Flow Visibility

**What it does:** Shows your cash position (past, present, future) in visual charts.

**Use case:** "Will I run out of money in the next 3-6 months?"

**Features:**
- Connect to QuickBooks/Xero (pull actuals automatically)
- Visual cash flow chart (line graph going up or down)
- Basic forecasting (repeat last month's pattern)
- Simple scenario modeling (toggle expenses on/off)

**Example platforms:** Pulse, Fathom (basic tier)

**When to use:** Small business (1-20 employees), need cash visibility, don't need complex modeling

**Cost:** $29-150/month

---

### Type 2: Full FP&A (Financial Planning & Analysis)

**What it does:** Forecast all 3 statements (P&L, balance sheet, cash flow) + hiring plans + scenarios.

**Use case:** "What happens if we hire 10 engineers next quarter?"

**Features:**
- 3-statement forecasting (income, balance, cash)
- Hiring and headcount planning (model new hires)
- Revenue forecasting (bottom-up by customer, product, channel)
- Budget vs. actuals (track performance vs. plan)
- Multi-scenario comparison (base, best, worst side-by-side)
- Integration with payroll/HRIS (Gusto, ADP auto-sync headcount costs)

**Example platforms:** Finmark, Jirav, Causal

**When to use:** Startup/SMB (20-100 employees), raising capital, need professional forecasts

**Cost:** $100-800/month

---

### Type 3: Strategic Finance / CFO-Grade

**What it does:** Everything in Type 2 + multi-entity consolidation + AI insights + data warehouse integration.

**Use case:** "Consolidate 5 subsidiaries, forecast by product line and geography, alert me to anomalies."

**Features:**
- Multi-entity consolidation (roll up subsidiaries)
- Currency conversion (international operations)
- Department-level budgeting (each department owns budget)
- AI-powered insights (anomaly detection, predictive forecasts)
- Data warehouse integration (Snowflake, BigQuery)
- Real-time dashboards (not monthly batch updates)
- 150+ pre-built metrics
- Enterprise ERP integration (NetSuite, Sage Intacct)

**Example platforms:** Mosaic, Dryrun

**When to use:** Mid-market (100-500 employees), finance team of 3-10 people, complex operations

**Cost:** $500-2,000/month

---

### Type 4: DIY (Build Your Own)

**What it does:** Custom-built cash flow analysis using libraries/code.

**Use case:** "Our business model is too unique for generic tools" or "We spend $2,000/month on SaaS, we can build for less."

**Tech stack:**
- Python + pandas (data manipulation)
- numpy-financial (financial calculations: NPV, IRR)
- Prophet or statsmodels (time series forecasting)
- PostgreSQL (store historical data)
- React or Plotly (visualization dashboard)
- QuickBooks API integration (pull actuals)

**Build effort:**
- Initial: 100-200 hours ($15K-30K at contractor rates)
- Maintenance: 20 hours/year ($3K/year)
- 3-year TCO: $27K-45K

**When to build:**
- SaaS cost >$1,000/month (DIY breaks even)
- Unique business model (real estate project finance, VC portfolio consolidation)
- Engineering team available (don't need to hire contractors)
- Strategic control matters (no vendor lock-in)

**When NOT to build:**
- You lack engineering resources
- Your needs are generic (most startups = generic)
- Time-to-value matters (build takes 2-4 months, SaaS takes 2 hours)

---

## Key Terms Reference

**Annual Recurring Revenue (ARR):** Yearly value of subscriptions (SaaS metric)
- Example: 10 customers × $100/month = $12K ARR

**Monthly Recurring Revenue (MRR):** Monthly value of subscriptions
- Example: 10 customers × $100/month = $1K MRR

**Churn Rate:** Percentage of customers who cancel per month/year
- Example: Lose 2 of 100 customers/month = 2% monthly churn

**Customer Acquisition Cost (CAC):** Cost to acquire one customer
- Formula: Marketing + Sales costs / New customers
- Example: Spend $10K on ads, get 100 customers = $100 CAC

**Lifetime Value (LTV):** Total revenue from one customer over their lifetime
- Formula: Average revenue per customer / Churn rate
- Example: $100/month customer, 5% monthly churn = $2,000 LTV

**Burn Multiple:** How much you spend to generate $1 of ARR
- Formula: Net burn / Net new ARR
- Example: Burn $100K/month, add $50K ARR/month = 2x burn multiple
- Good: <1.5x, Acceptable: 1.5-3x, Bad: >3x

**Rule of 40:** Growth rate + profit margin should equal 40%+
- Example: 50% growth + (-10% margin) = 40% (acceptable)
- Example: 20% growth + 25% margin = 45% (great)

**Payback Period:** Months to recover CAC
- Formula: CAC / (Monthly revenue per customer - Monthly cost to serve)
- Example: $1,200 CAC / $100/month gross profit = 12 months payback
- Good: <12 months, Acceptable: 12-18 months, Bad: >18 months

**Operating Cash Flow:** Cash from normal business operations (excluding investments, financing)

**Free Cash Flow:** Operating cash flow - capital expenditures
- Measures: "How much cash can we use for growth or return to shareholders?"

**Working Capital:** Current assets - current liabilities
- Measures: "Do we have enough short-term assets to cover short-term debts?"

---

## Common Questions

### Q: "I'm profitable, why do I need cash flow forecasting?"

**A:** Profit ≠ cash. You can be profitable on paper but run out of cash due to:
- Customers paying slowly (60-90 day payment terms)
- Inventory purchases (cash out before sale)
- Capital expenditures (buying equipment)
- Loan repayments (debt principal isn't an expense on P&L)

**Example:** SaaS company books $1M annual contract upfront (profitable!) but customer pays monthly ($83K/month). You need cash flow forecasting to survive the 12-month collection period.

---

### Q: "Can't I just check my bank balance?"

**A:** Bank balance is REACTIVE (tells you past), forecasting is PROACTIVE (tells you future).

**Example:**
- Bank balance today: $200K (looks fine!)
- But payroll next week: $150K
- And rent: $20K
- And AWS bill: $10K
- And customer payment delayed: -$50K expected
- Actual position: $20K left after obligations (not fine!)

Forecasting reveals problems BEFORE they happen.

---

### Q: "When should I switch from spreadsheet to cash flow tool?"

**Triggers:**
- Spending 4+ hours/month updating forecast
- Raising capital (need professional investor reports)
- Can't answer "what's our runway?" without 2 days of work
- Building hiring plans, can't connect to cash impact
- Multiple people need to collaborate (founder, CFO, finance team)
- Board wants monthly cash position reports

**Rule of thumb:**
- 0-10 employees: Spreadsheet fine
- 10-50 employees: Cash flow tool recommended
- 50+ employees: Cash flow tool mandatory

---

### Q: "What's the difference between cash flow tool and accounting software?"

**Accounting software (QuickBooks, Xero):**
- Records PAST transactions (actuals)
- Tracks what happened (invoices sent, bills paid)
- Compliance-focused (taxes, audits)
- Backward-looking

**Cash flow tool (Pulse, Finmark, Causal):**
- Forecasts FUTURE cash position
- Models scenarios ("what if we hire 5 people?")
- Decision-focused (should we hire, cut costs, fundraise?)
- Forward-looking

**They integrate:** Cash flow tool pulls actuals from accounting software, extends into future with forecasts.

---

### Q: "Which cash flow tool should I use?"

**Decision tree:**

**Do you use enterprise ERP or data warehouse?**
- NetSuite / Snowflake → Causal or Mosaic ONLY
- Sage Intacct → Dryrun or Mosaic ONLY
- QuickBooks / Xero → All platforms work

**What's your primary need?**
- Cash visibility only → Pulse ($29-89/mo)
- Full FP&A (3-statement, hiring plans) → Finmark or Jirav ($100-300/mo)
- CFO-grade (multi-entity, scenarios) → Dryrun or Causal ($500-1,000/mo)
- Strategic finance (AI, real-time, 25+ integrations) → Mosaic ($1,500-2,000/mo)

**What's your company size?**
- 1-20 employees → Pulse or Fathom
- 20-100 employees → Finmark, Jirav, or Causal
- 100-500 employees → Causal, Dryrun, or Mosaic

**What's your budget?**
- <$100/month → Pulse or Jirav Controller
- $100-500/month → Finmark, Jirav, Causal
- $500-2,000/month → Causal, Dryrun, Mosaic

See SYNTHESIS.md for detailed decision framework with 15 scenarios.

---

### Q: "Should I build my own cash flow tool?"

**Build if:**
- Current SaaS cost >$1,000/month (DIY breaks even at $750-1,250/mo)
- Unique business model (generic tools don't fit)
- Engineering team available (don't need contractors)
- Strategic control matters (no vendor lock-in)

**Buy SaaS if:**
- SaaS cost <$750/month (DIY doesn't break even)
- Generic needs (most startups)
- No engineering resources
- Time-to-value matters (SaaS = 2 hours, build = 2-4 months)

**Hybrid option:** Keep Excel + build automation scripts to pull from QuickBooks API ($3K-6K one-time, $1.5K/year maintenance)

---

### Q: "What about Excel + macros?"

**Pros:**
- Familiar tool (everyone knows Excel)
- Infinite flexibility (can model anything)
- One-time cost (no subscription)

**Cons:**
- Manual data entry (pulling from QuickBooks = copy-paste)
- Version control hell (which file is latest?)
- No collaboration (one person edits at a time)
- Breaking formulas (fragile, easy to break)
- No automatic reports (manual export to PDF for board)

**When Excel works:** Small business (<10 employees), update quarterly, single person owns finance

**When Excel breaks:** Startup (>20 employees), update monthly, multiple people need access, raising capital

---

### Q: "Do I need cash flow forecasting if I'm bootstrapped and profitable?"

**Yes, because:**

**Reason 1: Growth requires cash**
- Hire 3 engineers = $60K/month new expense
- They take 3-6 months to be productive
- You need cash buffer to fund growth investments

**Reason 2: Seasonality**
- E-commerce: 60% revenue in Q4, need cash to buy inventory in Q3
- B2B: Customers pay slow (60-90 days), need bridge financing

**Reason 3: Opportunity decisions**
- Customer wants $500K annual contract but pays quarterly
- Can you afford $375K cash delay waiting for payment?
- Forecast tells you: Yes (take deal) or No (require monthly billing)

**Bootstrapped ≠ no cash flow risk**. You just can't raise emergency capital if you miscalculate.

---

## When to Care About Cash Flow (By Stage)

### Pre-Revenue (Idea Stage)
**Cash flow priority:** Low
**Why:** Burning small amounts ($5K-10K/month), runway is obvious (bank balance / burn)
**Tool:** Simple spreadsheet

---

### Pre-Seed / Seed ($100K-2M raised)
**Cash flow priority:** Medium
**Why:** 12-18 month runway, need to plan hiring carefully
**Tool:** Cash flow visibility tool (Pulse) or simple FP&A (Finmark)
**Key question:** "Can we hire 5 people and still have 12 months runway?"

---

### Series A ($2M-10M raised)
**Cash flow priority:** High
**Why:** Scaling fast, hiring 20-50 people, investors want monthly reporting
**Tool:** Full FP&A platform (Finmark, Jirav, Causal)
**Key questions:**
- "What's our burn multiple?"
- "When do we run out of money at current growth rate?"
- "Can we get to profitability before next fundraise?"

---

### Series B+ ($10M+ raised)
**Cash flow priority:** Critical
**Why:** Finance team of 3-10 people, multi-entity operations, CFO needs real-time visibility
**Tool:** Strategic finance platform (Mosaic, Dryrun) or enterprise FP&A (Anaplan)
**Key questions:**
- "Consolidate 3 subsidiaries, show by product line and geography"
- "Real-time runway across all entities"
- "Department-level budget vs actuals"

---

### Profitable / Bootstrapped
**Cash flow priority:** Medium-High
**Why:** Can't raise emergency capital, must stay cash positive
**Tool:** Depends on size (1-20 employees = Pulse, 20-100 = Finmark, 100+ = Causal)
**Key questions:**
- "Can we fund growth from cash flow?"
- "What's our working capital buffer?"
- "Should we take debt financing for growth?"

---

## Summary: The Cash Flow Hierarchy of Needs

```
Level 5: Strategic Finance (Multi-entity, AI, Real-time)
         Tools: Mosaic, Anaplan
         Users: Mid-market (100-500 employees), finance team of 5-10

Level 4: CFO-Grade Forecasting (Scenarios, Multi-entity)
         Tools: Dryrun, Causal
         Users: Growing company (50-200 employees), professional CFO

Level 3: Full FP&A (3-statement, Hiring plans, Scenarios)
         Tools: Finmark, Jirav, Causal
         Users: Startup/SMB (20-100 employees), raising capital

Level 2: Cash Flow Visibility (Past + Future cash position)
         Tools: Pulse, Fathom
         Users: Small business (10-50 employees), need simple forecast

Level 1: Spreadsheet (Bank balance + rough burn rate)
         Tools: Google Sheets, Excel
         Users: Very small business (<10 employees), founder-only finance
```

**You start at Level 1 (spreadsheet), graduate to Level 2 (cash visibility), then Level 3 (full FP&A) as you grow.**

**Most companies never need Level 4-5** (only mid-market with complex operations).

---

## Next Steps

**If you're new to cash flow forecasting:**
1. Read SYNTHESIS.md for platform recommendations
2. Use S3-NEED-DRIVEN.md to find your scenario (15 scenarios mapped)
3. Check S2-COMPREHENSIVE.md for pricing and TCO comparison

**If you're evaluating platforms:**
1. Identify your constraint (NetSuite? Snowflake? QuickBooks?) - eliminates 6 of 8 platforms
2. Match your segment (1-20 employees? 20-100? 100-500?) - narrows to 2-3 platforms
3. Apply priorities (low lock-in? unlimited users? scenario modeling?) - picks final winner

**If you're not sure if you need a tool:**
- Spending 4+ hours/month updating forecast → You need a tool
- Raising capital soon → You need a tool (investors want professional reports)
- Can't answer "what's our runway?" instantly → You need a tool
- Still in spreadsheet and it's working fine → Keep using spreadsheet (don't fix what's not broken)

---

**Related Research:**
- **SYNTHESIS.md** - Unified platform recommendations across S1-S4
- **S3-NEED-DRIVEN.md** - 15 scenarios mapped to specific platforms
- **S2-COMPREHENSIVE.md** - Feature matrix, TCO analysis, lock-in spectrum
- **metadata.yaml** - Structured data on all 8 platforms

---

**Last Updated:** October 22, 2025
**Research:** 3.004 Cash Flow Management Platforms (MPSE v2.0)
