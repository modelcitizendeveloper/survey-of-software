# Unix-Style Financial Scenario Tools

**Research:** 1.127 - Financial Simulation
**Date:** 2025-01-18
**Approach:** Apply Unix philosophy to cash flow scenario analysis

---

## Inspiration: Latin Trainer Pattern

### What Worked for Language Learning

**Three composable utilities:**

1. **latin-parse** - Text → JSONL (one-time, slow, cached)
2. **latin-train** - Interactive practice (fast, real-time feedback)
3. **latin-analyze** - Statistics & patterns

**Key principles:**
- Files are the database (JSONL, not PostgreSQL)
- Composable (pipe to jq, grep, awk)
- Pre-compute slow operations (parsing)
- Fast interactive loops
- Append-only history (never overwrite)

---

## Financial Scenario Tools (Proposed)

### Three Core Utilities

**1. fs-parse** - Financial Statements → JSONL
**2. fs-scenario** - Interactive Scenario Builder
**3. fs-analyze** - Comparison & Sensitivity Analysis

---

## 1. fs-parse (Parser)

### Purpose
Convert financial statements (CSV, Excel, QuickBooks export, API) into structured JSONL format

### Input Formats
```bash
# From CSV (exported from accounting software)
fs-parse statements.csv > company_2024.jsonl

# From Excel (multi-sheet workbook)
fs-parse financial_model.xlsx --sheet "Balance Sheet" > bs_2024.jsonl

# From QuickBooks API (future)
fs-parse --source quickbooks --company acme > acme_2024.jsonl

# From stdin (pipe from other tools)
cat raw_data.csv | fs-parse > parsed.jsonl
```

### Output Format (JSONL)
```json
{"period": "2024-01", "category": "revenue", "subcategory": "software_licenses", "amount": 125000, "currency": "USD"}
{"period": "2024-01", "category": "expense", "subcategory": "salaries", "amount": 80000, "currency": "USD"}
{"period": "2024-01", "category": "expense", "subcategory": "rent", "amount": 5000, "currency": "USD"}
```

**Why JSONL?**
- One line per transaction/account (easy to grep, awk)
- Human-readable for debugging
- Git-friendly (line-based diffs)
- Fast to parse (no loading entire file in memory)

### Features
- **Auto-detect format** - Sniff CSV structure, Excel layout
- **Category mapping** - Map "Wages" → "salaries", "Subscriptions" → "saas_tools"
- **Currency normalization** - Convert to USD/base currency
- **Validation** - Check that debits = credits, flag anomalies
- **Metadata extraction** - Period, company name, fiscal year

### Example Output Structure
```bash
$ fs-parse qb_export.csv | head -3
{"period":"2024-01","category":"revenue","subcategory":"consulting","amount":45000}
{"period":"2024-01","category":"expense","subcategory":"marketing","amount":8000}
{"period":"2024-01","category":"expense","subcategory":"hosting","amount":1200}

$ fs-parse qb_export.csv | jq -r '.category' | sort | uniq -c
    24 revenue
    45 expense
     8 asset
     3 liability
```

---

## 2. fs-scenario (Interactive Scenario Builder)

### Purpose
Interactive tool to define scenarios, modify assumptions, run what-if analysis

### Usage
```bash
# Create new scenario from baseline
fs-scenario baseline_2024.jsonl --output scenarios.jsonl

# Resume editing existing scenarios
fs-scenario scenarios.jsonl --resume
```

### Interactive Interface (TUI)

```
╔══════════════════════════════════════════════════════════════╗
║ FINANCIAL SCENARIO BUILDER                                   ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║ Current Scenario: "High Growth Case"                         ║
║                                                              ║
║ Assumptions:                                                 ║
║   [1] Revenue Growth Rate:           25% YoY                 ║
║   [2] Gross Margin:                  75%                     ║
║   [3] Marketing % of Revenue:        20%                     ║
║   [4] Headcount Growth:              +5 employees/quarter    ║
║   [5] Average Salary:                $120,000                ║
║                                                              ║
║ Commands:                                                    ║
║   1-9    Edit assumption                                     ║
║   c      Create new scenario (copy current)                  ║
║   d      Delete scenario                                     ║
║   r      Run projection                                      ║
║   s      Save & exit                                         ║
║   q      Quit without saving                                 ║
╚══════════════════════════════════════════════════════════════╝
```

### Scenario Types

**1. Growth Assumptions**
```bash
# Edit assumption: Revenue growth rate
> 1
Current: 25% YoY
New value: 30
Saved: Revenue Growth → 30% YoY
```

**2. Expense Assumptions**
```bash
# Edit: Marketing spend
> 3
Current: 20% of revenue
Options:
  a) Percentage of revenue (current)
  b) Fixed amount per month
  c) Growth curve (start low, ramp up)
Choice: c
```

**3. Timing Assumptions**
```bash
# Edit: When does hiring happen?
> 4
Current: +5 employees/quarter
New timing:
  Q1: +2
  Q2: +3
  Q3: +5
  Q4: +5
```

### Output Format (Scenarios JSONL)
```json
{
  "scenario_id": "baseline",
  "name": "Baseline Case",
  "created": "2025-01-18T10:00:00",
  "assumptions": {
    "revenue_growth_rate": 0.15,
    "gross_margin": 0.70,
    "marketing_pct_revenue": 0.15,
    "headcount_growth_quarterly": 3,
    "avg_salary": 100000
  }
}
{
  "scenario_id": "high_growth",
  "name": "High Growth Case",
  "created": "2025-01-18T10:15:00",
  "assumptions": {
    "revenue_growth_rate": 0.30,
    "gross_margin": 0.75,
    "marketing_pct_revenue": 0.20,
    "headcount_growth_quarterly": 5,
    "avg_salary": 120000
  }
}
```

---

## 3. fs-analyze (Analysis & Comparison)

### Purpose
Compare scenarios, run sensitivity analysis, generate insights

### Usage
```bash
# Compare scenarios
fs-analyze scenarios.jsonl --baseline baseline_2024.jsonl

# Sensitivity analysis
fs-analyze scenarios.jsonl --sensitivity revenue_growth_rate

# Export to charts
fs-analyze scenarios.jsonl --export charts/ --format png

# Text summary
fs-analyze scenarios.jsonl --summary
```

### Output Examples

**Scenario Comparison:**
```
═══════════════════════════════════════════════════════════════
SCENARIO COMPARISON
═══════════════════════════════════════════════════════════════

Metric                    Baseline    High Growth    Conservative
───────────────────────────────────────────────────────────────
Revenue (12 months)        $1.2M       $1.8M          $900K
Cash Burn (monthly)        -$45K       -$65K          -$30K
Runway (months)              18          12             24
Break-even Month           Aug 2025    Jun 2025       Dec 2025
Headcount (end of year)      25          35             20
───────────────────────────────────────────────────────────────

Key Differences:
  • High Growth: +50% revenue BUT burns cash faster
  • Conservative: Longer runway BUT slower growth
  • Baseline: Middle ground (recommended)
```

**Sensitivity Analysis:**
```bash
$ fs-analyze scenarios.jsonl --sensitivity revenue_growth_rate

═══════════════════════════════════════════════════════════════
SENSITIVITY ANALYSIS: Revenue Growth Rate
═══════════════════════════════════════════════════════════════

Test Range: 10% to 40% (5% increments)

Growth Rate    Cash at 12mo    Break-even    Runway (months)
──────────────────────────────────────────────────────────────
   10%          -$150K         Never           14
   15%           -$80K         Month 18        16
   20%            $20K         Month 14        18
   25%           $120K         Month 11        20+
   30%           $250K         Month  9        20+
   35%           $400K         Month  7        20+
   40%           $580K         Month  6        20+
──────────────────────────────────────────────────────────────

Critical Insight:
  ⚠️  Below 20% growth: Company does not reach profitability
  ✓  Above 25% growth: Strong cash position enables hiring
```

**Cash Flow Projection Chart (ASCII)**
```
Cash Balance Over Time (3 Scenarios)

 $600K ┤                                         ╭─── High Growth
       │                                     ╭───╯
 $400K ┤                                 ╭───╯
       │                             ╭───╯
 $200K ┤                         ╭───╯    Baseline ───╮
       │                     ╭───╯                    │
    $0 ┼─────────────────╭───╯                        ╰───╮
       │             ╭───╯                                 ╰─
-$200K ┤         ╭───╯
       │     ╭───╯  Conservative ───────────────────────────
-$400K ┼─────╯
       └┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬
        Jan  Mar  May  Jul  Sep  Nov  Jan  Mar  May  Jul  Sep
```

---

## Workflow Example: Startup Cash Flow Planning

### Scenario: SaaS startup planning next 18 months

**Step 1: Parse historical data**
```bash
# Export from QuickBooks → CSV
fs-parse qb_2024.csv > baseline_2024.jsonl

# Verify data
cat baseline_2024.jsonl | jq '.category' | sort | uniq -c
```

**Step 2: Create scenarios**
```bash
fs-scenario baseline_2024.jsonl --output scenarios.jsonl

# Interactive prompts:
> Create new scenario
Name: Conservative Case
Revenue growth: 10%
Marketing budget: $5K/month
Hiring plan: Freeze until break-even
Save? y

> Create new scenario
Name: Aggressive Growth
Revenue growth: 40%
Marketing budget: $25K/month
Hiring plan: +2 engineers/quarter
Save? y
```

**Step 3: Analyze scenarios**
```bash
# Compare all scenarios
fs-analyze scenarios.jsonl

# Test sensitivity
fs-analyze scenarios.jsonl --sensitivity revenue_growth_rate

# What if marketing budget changes?
fs-analyze scenarios.jsonl --sensitivity marketing_budget

# Export charts for board deck
fs-analyze scenarios.jsonl --export board_deck/ --format png
```

**Step 4: Refine & iterate**
```bash
# Resume scenario editing
fs-scenario scenarios.jsonl --resume

# Adjust based on analysis
> Edit scenario: Aggressive Growth
Assumption to change: marketing_budget
New value: $20K/month (was $25K - save $5K)
```

**Step 5: Generate final report**
```bash
fs-analyze scenarios.jsonl --summary > board_report.txt
```

---

## Advanced Features

### 1. Monte Carlo Simulation
```bash
# Add uncertainty to assumptions
fs-scenario scenarios.jsonl --monte-carlo

# Interactive:
> Which assumption has uncertainty?
1) Revenue growth (currently: 25%)
Choice: 1

> Define distribution:
Type: normal
Mean: 25%
Std Dev: 5%
(95% of outcomes: 15%-35%)

Save? y
```

**Run simulations:**
```bash
fs-analyze scenarios.jsonl --monte-carlo --runs 10000

# Output:
Monte Carlo Results (10,000 runs)
═══════════════════════════════════
Cash at 12 months:
  5th percentile:   -$80K  (worst case)
  25th percentile:   $50K
  Median:           $150K
  75th percentile:  $280K
  95th percentile:  $420K  (best case)

Probability of running out of cash: 12%
```

### 2. Forecasting Integration (Prophet)
```bash
# Use historical data to forecast
fs-forecast baseline_2024.jsonl --method prophet --periods 12

# Output: forecasted_2025.jsonl
# Uses seasonal patterns, trends from historical data
```

### 3. Comparison to Actuals
```bash
# Compare scenario to what actually happened
fs-analyze scenarios.jsonl --actual actual_2024.jsonl

# Shows variance:
Metric              Projected    Actual     Variance
────────────────────────────────────────────────────
Revenue (Q1)         $300K       $280K      -6.7%
Marketing Spend       $15K        $18K     +20.0%
Headcount               8           7       -12.5%
```

---

## File Structure

```
~/financial-planning/
├── data/
│   ├── qb_2024.csv              # Raw export from QuickBooks
│   └── baseline_2024.jsonl      # Parsed historical data (read-only)
├── scenarios/
│   ├── scenarios_2025.jsonl     # All scenario definitions
│   └── forecasts_2025.jsonl     # Generated forecasts
├── analysis/
│   └── sensitivity_revenue.txt  # Analysis outputs
└── reports/
    └── board_deck/
        ├── scenario_comparison.png
        ├── cash_flow_chart.png
        └── sensitivity_analysis.png
```

---

## Technical Implementation

### Libraries Used (from 1.127 research)

**Core:**
- **pandas** - Data manipulation (99% survival rate)
- **numpy-financial** - NPV, IRR, PMT calculations
- **Prophet** - Time series forecasting (optional)

**Advanced:**
- **scipy.stats** - Monte Carlo distributions
- **matplotlib/plotly** - Charts (if not ASCII)

### Why Not SaaS?

**From 1.127 research:**
- SaaS breakpoint: $800/month
- Below $800/month → Buy SaaS (Pulse, Finmark)
- Above $800/month → DIY competitive

**Our tools target:**
1. **DIY enthusiasts** who want full control
2. **Companies >$800/month SaaS** (Causal, Mosaic too expensive)
3. **Custom models** not available in SaaS

**Cost comparison (from research):**
- SaaS ($800/mo): $9,600/year, $96K 10-year TCO
- DIY (pandas + numpy-financial): $11.4K 3-year TCO
- **Our tools: FREE (just libraries)**

---

## Comparison to Excel

### What Excel Does Well
- Quick prototyping
- Visual formulas (see cell references)
- Familiar to non-technical users
- Pivot tables, charts built-in

### What Excel Struggles With
- **Version control** (email attachments, lost changes)
- **Reproducibility** (hard to audit complex formulas)
- **Scalability** (crashes at 50MB+)
- **Automation** (running 1,000 scenarios manually = painful)

### What Our Tools Add
- **Version control** (git-friendly JSONL)
- **Reproducibility** (scenarios are code, not hidden formulas)
- **Automation** (run 10,000 Monte Carlo simulations instantly)
- **Composability** (pipe to other Unix tools)

---

## Design Principles

### 1. Files are the Database
- No PostgreSQL/SQLite required
- Human-readable JSONL
- Git-friendly (diff scenarios)

### 2. Pre-compute Slow Operations
- Parse once (fs-parse), use many times
- Cache forecasts, reuse for multiple scenarios

### 3. Interactive where it matters
- Scenario builder = interactive (rapid what-if)
- Analysis = batch (run overnight, export charts)

### 4. Composable
```bash
# Example: Find highest revenue scenario
cat scenarios.jsonl | jq -r '.assumptions.revenue_growth_rate' | sort -n | tail -1

# Example: Export to CSV for Excel users
cat baseline_2024.jsonl | jq -r '[.period, .category, .amount] | @csv' > export.csv

# Example: Filter to Q1 only
cat baseline_2024.jsonl | jq 'select(.period | startswith("2024-0"))' > q1.jsonl
```

### 5. Fast Feedback Loops
- Scenario editing: instant (just update assumptions)
- Analysis: seconds (pandas vectorized operations)
- Charts: optional (ASCII for speed, PNG for presentations)

---

## Next Steps

### Phase 1: MVP (2-3 days)
1. **fs-parse** - CSV → JSONL parser
2. **fs-scenario** - Simple TUI for editing assumptions
3. **fs-analyze** - Basic comparison table

**Test with:** Real QuickBooks export, 3 scenarios (baseline, conservative, aggressive)

### Phase 2: Forecasting (1 week)
1. Add Prophet integration
2. Monte Carlo simulation support
3. Sensitivity analysis automation

### Phase 3: Polish (1 week)
1. Better TUI (blessed library, like latin-train)
2. Chart generation (matplotlib/plotly)
3. Export to Excel/Google Sheets
4. Documentation & examples

---

## Open Questions

1. **Input format standardization:**
   - Should we support multiple accounting software exports?
   - Or require manual CSV mapping?

2. **Scenario complexity:**
   - How many assumptions should we support?
   - Start simple (5-10) or comprehensive (50+)?

3. **Forecasting method:**
   - Always use Prophet? Or user-configurable (ARIMA, linear regression)?

4. **Monte Carlo:**
   - Always stochastic? Or deterministic by default?

5. **Chart output:**
   - ASCII for terminal users? PNG for presentations? Both?

---

## Conclusion

**Unix philosophy applies to financial analysis:**
- Small, composable tools
- Files as database
- Fast feedback loops
- Automation-friendly

**Advantages over SaaS:**
- Free (library costs only)
- Full control (custom models)
- Git-friendly (version control)
- Composable (pipe to other tools)

**Advantages over Excel:**
- Reproducible (no hidden formulas)
- Scalable (handles large datasets)
- Automatable (run 10,000 scenarios)

**When to use:**
- SaaS >$800/month (too expensive)
- Custom models needed (SaaS can't do it)
- Technical team available (Python proficiency)
- Existing data infrastructure (warehouse, pipelines)

**Novel approach:**
- Most financial tools are SaaS or Excel
- Very few use Unix CLI philosophy
- We're pioneering: financial analysis as composable tools
