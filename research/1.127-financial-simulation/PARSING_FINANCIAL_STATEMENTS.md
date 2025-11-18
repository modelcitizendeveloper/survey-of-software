# Parsing Financial Statements: The XPOS Problem

**Question:** Is there a parser that turns financial statements into XPOS-style tagged JSON?

**Short Answer:** Not really - but we can build one by combining:
1. **XBRL parsers** (SEC filings - complex but standardized)
2. **pandas** (CSV/Excel - flexible but unstandardized)
3. **Custom mapping** (QuickBooks/Xero exports - vendor-specific)

---

## The Analogy to Latin Parsing

### Latin (CLTK):
- **Input:** Raw text ("Puella in via ambulat")
- **Parser:** CLTK NLP pipeline (Stanza models)
- **Output:** Tagged JSON with grammar codes (XPOS: `A1|grn1|casA|gen2`)

### Financial Statements:
- **Input:** Raw financial data (CSV, Excel, XBRL)
- **Parser:** ??? (no universal standard)
- **Output:** Tagged JSON with account metadata

**The problem:** There's no "CLTK for financial statements" because:
1. **No universal grammar** - Unlike Latin (6 cases, 5 declensions), accounting varies by:
   - Country (US GAAP vs IFRS vs local GAAP)
   - Industry (SaaS vs retail vs construction)
   - Company (custom chart of accounts)

2. **Multiple formats:**
   - XBRL (SEC filings - XML, structured but complex)
   - CSV exports (QuickBooks, Xero - unstructured)
   - Excel (manual - no standards)
   - APIs (Plaid, Stripe - vendor-specific)

3. **Semantic ambiguity:**
   - "Revenue" might be:
     - Operating revenue
     - Total revenue (including interest income)
     - Gross revenue (before returns)
   - Parser needs context to classify correctly

---

## Approach 1: XBRL (SEC Filings - Public Companies)

### What is XBRL?

**XBRL (eXtensible Business Reporting Language)** = Financial statement markup language

**Example (simplified):**
```xml
<xbrl>
  <gaap:Revenue contextRef="2024Q1" unitRef="USD" decimals="-3">
    1250000
  </gaap:Revenue>
  <gaap:CostOfRevenue contextRef="2024Q1" unitRef="USD" decimals="-3">
    375000
  </gaap:Revenue>
  <gaap:GrossProfit contextRef="2024Q1" unitRef="USD" decimals="-3">
    875000
  </gaap:GrossProfit>
</xbrl>
```

**Pros:**
- Standardized (required for SEC filings)
- Semantic tags (gaap:Revenue vs gaap:CostOfRevenue)
- Machine-readable

**Cons:**
- **Complex** (1,000+ page specification)
- **Only for public companies** (private companies don't use XBRL)
- **Overkill** for small businesses

**Parser:** python-xbrl library

```bash
pip install python-xbrl
```

```python
from xbrl import XBRLParser

parser = XBRLParser()
xbrl_data = parser.parse("apple_10k.xml")

# Extract tagged data
revenue = xbrl_data.find_fact("us-gaap:Revenues")
# → {"value": 1250000, "context": "2024Q1", "unit": "USD"}
```

---

## Approach 2: CSV/Excel (QuickBooks/Xero Exports)

### The Problem: No Standards

**QuickBooks P&L Export:**
```csv
Account,Jan 2024,Feb 2024,Mar 2024
Income,,,
  Product Sales,50000,55000,60000
  Service Revenue,25000,27000,30000
Total Income,75000,82000,90000
Expenses,,,
  Salaries,40000,40000,45000
  Rent,5000,5000,5000
  Marketing,8000,10000,12000
Total Expenses,53000,55000,62000
Net Income,22000,27000,28000
```

**Xero P&L Export (different format!):**
```csv
Category,Amount,Period
Revenue - Product Sales,50000,2024-01
Revenue - Services,25000,2024-01
Expense - Payroll,40000,2024-01
Expense - Occupancy,5000,2024-01
```

**The Challenge:**
- Different vendors = different formats
- No semantic tags ("Product Sales" vs "Sales - Products")
- Need custom mapping for each source

### Solution: Custom Parser with Mapping

**Step 1: Define canonical schema**
```json
{
  "period": "2024-01",
  "account": {
    "category": "revenue",           # Top level: revenue, expense, asset, liability
    "subcategory": "product_sales",  # Specific type
    "account_type": "operating"      # Classification: operating, non-operating, etc.
  },
  "amount": 50000,
  "currency": "USD",
  "metadata": {
    "source": "quickbooks",
    "export_date": "2024-01-15"
  }
}
```

**Step 2: Create mapping file**
```yaml
# qb_mapping.yaml
mappings:
  "Product Sales":
    category: revenue
    subcategory: product_sales
    account_type: operating

  "Service Revenue":
    category: revenue
    subcategory: services
    account_type: operating

  "Salaries":
    category: expense
    subcategory: payroll
    account_type: operating

  "Marketing":
    category: expense
    subcategory: marketing
    account_type: operating
```

**Step 3: Parser with fallback rules**
```python
def parse_csv_with_mapping(csv_file, mapping_file):
    """Parse CSV and apply mapping to canonical schema"""

    # Load mapping
    mapping = yaml.safe_load(open(mapping_file))

    # Parse CSV
    df = pd.read_csv(csv_file)

    results = []
    for idx, row in df.iterrows():
        account_name = row['Account']

        # Try exact match
        if account_name in mapping['mappings']:
            canonical = mapping['mappings'][account_name]
        else:
            # Fallback: pattern matching
            canonical = guess_category(account_name)

        results.append({
            'period': parse_period(row),
            'account': canonical,
            'amount': row['Jan 2024'],  # Or dynamic column
            'currency': 'USD',
        })

    return results

def guess_category(account_name):
    """Fallback: guess category from account name"""
    # Simple heuristics
    if any(word in account_name.lower() for word in ['sales', 'revenue', 'income']):
        return {'category': 'revenue', 'subcategory': 'unknown'}
    elif any(word in account_name.lower() for word in ['expense', 'cost', 'salary', 'rent']):
        return {'category': 'expense', 'subcategory': 'unknown'}
    else:
        return {'category': 'unknown', 'subcategory': 'unknown'}
```

---

## Approach 3: The "XPOS for Finance" We Need to Create

### Inspiration from Latin XPOS

**Latin XPOS:** `A1|grn1|casA|gen2`
- Position 1: Declension (A=1st)
- Position 2: Number (1=singular)
- Position 3-4: Gender, Case, etc.

**Financial "XPOS"** (proposed):
```
R.OP.PROD|2024-01|USD|50000
│  │   │     │     │    │
│  │   │     │     │    └─ Amount
│  │   │     │     └────── Currency
│  │   │     └──────────── Period
│  │   └────────────────── Subcategory (product sales)
│  └────────────────────── Account type (operating)
└───────────────────────── Category (R=revenue)
```

**Category codes:**
- R = Revenue
- E = Expense
- A = Asset
- L = Liability
- Q = Equity

**Account type codes:**
- OP = Operating
- NO = Non-operating
- FI = Financing
- IN = Investing

**Example tagged statement:**
```jsonl
{"code": "R.OP.PROD", "period": "2024-01", "amount": 50000, "account": "Product Sales"}
{"code": "R.OP.SERV", "period": "2024-01", "amount": 25000, "account": "Service Revenue"}
{"code": "E.OP.PAYR", "period": "2024-01", "amount": 40000, "account": "Salaries"}
{"code": "E.OP.MRKT", "period": "2024-01", "amount": 8000, "account": "Marketing"}
{"code": "E.OP.RENT", "period": "2024-01", "amount": 5000, "account": "Rent"}
```

**Benefits:**
- **Grep-friendly:** `grep "^R\." statements.jsonl` → all revenue accounts
- **Aggregatable:** Sum by category code prefix
- **Standardized:** Same schema across all sources

---

## Concrete Example: Sample Company

### Input: QuickBooks Export (CSV)

**file: `acme_corp_2024.csv`**
```csv
Account,Jan,Feb,Mar
Revenue,,,
  Product Sales,50000,55000,60000
  Consulting Services,25000,27000,30000
Total Revenue,75000,82000,90000
Cost of Goods Sold,,,
  Product Costs,15000,16500,18000
  Service Delivery,7500,8100,9000
Total COGS,22500,24600,27000
Gross Profit,52500,57400,63000
Operating Expenses,,,
  Salaries,40000,40000,45000
  Rent,5000,5000,5000
  Marketing,8000,10000,12000
Total Operating Expenses,53000,55000,62000
Operating Income,-500,2400,1000
Interest Expense,200,200,200
Net Income,-700,2200,800
```

### Step 1: Parse with fs-parse

```bash
fs-parse acme_corp_2024.csv --mapping qb_standard.yaml > acme_parsed.jsonl
```

**Output: `acme_parsed.jsonl`**
```jsonl
{"code":"R.OP.PROD","period":"2024-01","amount":50000,"account":"Product Sales","category":"revenue","subcategory":"product_sales"}
{"code":"R.OP.SERV","period":"2024-01","amount":25000,"account":"Consulting Services","category":"revenue","subcategory":"consulting"}
{"code":"E.CG.PROD","period":"2024-01","amount":15000,"account":"Product Costs","category":"expense","subcategory":"cogs_product"}
{"code":"E.CG.SERV","period":"2024-01","amount":7500,"account":"Service Delivery","category":"expense","subcategory":"cogs_service"}
{"code":"E.OP.PAYR","period":"2024-01","amount":40000,"account":"Salaries","category":"expense","subcategory":"payroll"}
{"code":"E.OP.RENT","period":"2024-01","amount":5000,"account":"Rent","category":"expense","subcategory":"rent"}
{"code":"E.OP.MRKT","period":"2024-01","amount":8000,"account":"Marketing","category":"expense","subcategory":"marketing"}
{"code":"E.FI.INTR","period":"2024-01","amount":200,"account":"Interest Expense","category":"expense","subcategory":"interest"}
```

### Step 2: Create Scenario (Higher Uncollectable Accounts)

**Scenario: Increase bad debt from 2% to 5% of revenue**

```bash
fs-scenario acme_parsed.jsonl --output scenarios.jsonl
```

**Interactive:**
```
> Create new scenario
Name: Higher Bad Debt
Description: Increase uncollectable accounts from 2% to 5%

> Which account to modify?
Search: revenue
Found: R.OP.PROD (Product Sales), R.OP.SERV (Consulting Services)

> How to modify?
Options:
  1) Add new expense account (bad debt)
  2) Reduce revenue accounts directly
  3) Add percentage adjustment

Choice: 1

> Add expense account
Account name: Bad Debt Expense
Code: E.OP.BADD
Formula: (R.OP.PROD + R.OP.SERV) * 0.05

Baseline bad debt (2%): $1,500/month
New bad debt (5%): $3,750/month
Increase: $2,250/month

Save scenario? y
```

**Output: `scenarios.jsonl`**
```jsonl
{
  "scenario_id": "baseline",
  "name": "Baseline (2% Bad Debt)",
  "adjustments": [
    {"code": "E.OP.BADD", "formula": "(R.OP.PROD + R.OP.SERV) * 0.02"}
  ]
}
{
  "scenario_id": "high_bad_debt",
  "name": "Higher Bad Debt (5%)",
  "adjustments": [
    {"code": "E.OP.BADD", "formula": "(R.OP.PROD + R.OP.SERV) * 0.05"}
  ]
}
```

### Step 3: Compare Scenarios

```bash
fs-analyze scenarios.jsonl --baseline acme_parsed.jsonl
```

**Output:**
```
═══════════════════════════════════════════════════════════════
SCENARIO COMPARISON: Acme Corp (Q1 2024)
═══════════════════════════════════════════════════════════════

Account               Baseline    High Bad Debt    Delta
─────────────────────────────────────────────────────────────
Revenue                $75,000       $75,000         $0
COGS                   -$22,500      -$22,500        $0
Gross Profit            $52,500       $52,500        $0
Operating Expenses     -$53,000      -$53,000        $0
Bad Debt Expense        -$1,500       -$3,750    -$2,250  ⚠️
Operating Income         -$500        -$2,750    -$2,250
Interest Expense          -$200          -$200        $0
─────────────────────────────────────────────────────────────
Net Income               -$700        -$2,950    -$2,250

═══════════════════════════════════════════════════════════════
KEY INSIGHTS
═══════════════════════════════════════════════════════════════

⚠️  Net income deteriorates from -$700 to -$2,950 (4.2x worse)
⚠️  Additional monthly cash burn: $2,250
⚠️  Annual impact: -$27,000 (assumes 3% bad debt increase)

RECOMMENDATION: Monitor accounts receivable aging closely
  - Current 90+ days: [need data]
  - Industry average bad debt: 2.5%
  - Action: Tighten credit policies if >3% realized
```

### Step 4: Extend Scenario (12-month projection)

```bash
fs-forecast scenarios.jsonl --periods 12 --method linear
```

**Output:**
```
Cash Flow Projection (12 months)

                Baseline    High Bad Debt
Month 1         -$700       -$2,950
Month 2         +$2,200     -$50
Month 3         +$800       -$1,450
Month 4         +$1,500     -$750
Month 5         +$2,200     +$50
Month 6         +$3,000     +$750
...
Month 12        +$5,000     +$2,750

Cumulative:
  Baseline:       +$18,000
  High Bad Debt:  -$9,000
  Delta:          -$27,000  ⚠️ Critical difference!

Break-even:
  Baseline:       Month 2
  High Bad Debt:  Month 5 (3 months later)
```

---

## Key Research Questions

### 1. Is there a standard parser?
**Answer:** No universal standard, but:
- **XBRL** for public companies (complex)
- **pandas** for CSV/Excel (flexible)
- **We need to build** mapping layer (like we did with XPOS codes)

### 2. What format should we use?
**Proposal:** JSONL with semantic codes (our "financial XPOS")
```jsonl
{"code":"R.OP.PROD","period":"2024-01","amount":50000}
```

**Benefits:**
- Grep-friendly (`grep "^R\."` → all revenue)
- Standardized (works across vendors)
- Git-friendly (line-based diffs)

### 3. How do scenarios modify baseline?
**Two approaches:**

**Approach A: Direct modification**
```json
{
  "scenario": "high_bad_debt",
  "modify": {
    "E.OP.BADD": {"amount": 3750}  // Was 1500, now 3750
  }
}
```

**Approach B: Formula-based**
```json
{
  "scenario": "high_bad_debt",
  "formulas": {
    "E.OP.BADD": "(R.OP.PROD + R.OP.SERV) * 0.05"
  }
}
```

**Approach B is better** because:
- Adapts to revenue changes
- More explicit (shows reasoning)
- Easier to audit

### 4. What other questions can this answer?

**Revenue Scenarios:**
- "What if we raise prices 10%?"
- "What if we lose our biggest customer?"
- "What if growth accelerates to 30%?"

**Expense Scenarios:**
- "What if we hire 2 more engineers?"
- "What if marketing budget doubles?"
- "What if rent increases 20%?"

**Timing Scenarios:**
- "What if customers pay 60 days instead of 30?"
- "What if we delay that equipment purchase?"
- "What if we front-load marketing spend?"

**Combination Scenarios:**
- "What if revenue grows 25% AND we hire 5 people?"
- "What if we cut marketing 50% AND growth slows to 10%?"

---

## Implementation Roadmap

### Phase 1: Parser (fs-parse)
1. CSV parser with mapping files
2. QuickBooks/Xero export support
3. Generate semantic codes (R.OP.PROD)
4. Output JSONL

### Phase 2: Scenario Builder (fs-scenario)
1. Interactive TUI for defining scenarios
2. Formula support (revenue * 0.05)
3. Scenario comparison
4. Save to JSONL

### Phase 3: Analysis (fs-analyze)
1. Compare scenarios side-by-side
2. 12-month projections
3. Sensitivity analysis
4. Export to charts

### Phase 4: Advanced
1. Monte Carlo (uncertainty)
2. Prophet forecasting (seasonal patterns)
3. Multi-year projections
4. Break-even analysis

---

## Next Steps

**Should we:**
1. Create sample financial data (Acme Corp)?
2. Build MVP parser (CSV → JSONL)?
3. Test scenario modification?
4. Compare to SaaS capabilities?

**Let me know which direction to explore next!**
