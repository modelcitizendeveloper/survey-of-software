# Real-World Decision: Distribution Center Capacity Planning

## The Business Problem

**Scenario**: You run a regional distribution center (150k sq ft, 40 order pickers, 8 loading docks). Q4 peak season is approaching. Last year, you fell behind during Cyber Week—orders backed up 72 hours, missed SLAs cost $400k in penalties and lost customers.

**The Question**: Do you expand capacity? Add shifts? Optimize current operations? How much will it cost, and will it actually solve the problem?

**Stakes**:
- Lease overflow warehouse: $180k for 3 months (50k sq ft @ $1.20/sq ft/month)
- Add evening shift (4pm-12am): $240k (20 additional workers × $30/hr loaded × 400 hours)
- Do nothing and risk repeating last year: $400k+ in penalties

**You currently have**:
- Warehouse Management System (WMS) - like Infor, Manhattan, or HighJump
- Historical order data (2 years of timestamps, SKUs, pick times, ship times)
- Peak season forecast from sales (40% volume increase expected)

## The Decision Tree

### Option 1: Do Nothing (Spreadsheet Analysis)

**What you'd do**: Export WMS data to Excel, calculate "orders per hour × hours available = capacity."

**Example calc**:
- Current: 500 orders/day ÷ 10 hours = 50 orders/hour
- Peak forecast: 700 orders/day
- Required capacity: 70 orders/hour
- Deficit: 20 orders/hour → "Need 40% more capacity"

**Cost**: $0 (internal time only)

**Fatal flaw**:
- **Ignores queuing dynamics**: Orders don't arrive uniformly. Spreadsheet assumes steady flow.
- **Reality**: Orders spike 9-11am (40% of daily volume) after overnight batch from e-commerce. Pickers are idle 6-8am, slammed 9am-12pm, moderate 1-5pm.
- **What you miss**: Bottleneck isn't total capacity—it's peak-hour congestion. Adding evening shift won't help if orders arrive in the morning.

**Verdict**: ❌ Too simplistic for systems with variability and queuing.

---

### Option 2: Upgrade WMS to One with Built-In Capacity Planning

**Example vendors**:
- Manhattan Active WMS (capacity planning module)
- Blue Yonder (JDA) with simulation features
- Oracle WMS Cloud with analytics

**Cost**:
- Software: $500k-$2M (enterprise WMS replacement)
- Implementation: 12-18 months
- Training/change management: $100k-$300k

**What you get**:
- Pre-built dashboards
- Integration with existing systems
- Vendor support

**Fatal flaw**:
- **Timeline**: You need an answer in 6 weeks, not 18 months.
- **Overkill**: You're not replacing WMS; you just need to model Q4 peak.
- **Lock-in**: Captive to vendor's modeling assumptions. Can't customize for your specific bottleneck.

**Verdict**: ❌ Strategic project, not tactical solution for Q4.

---

### Option 3: Commercial Discrete Event Simulation Software

**Options**:
- **AnyLogic** ($15k-$50k/year + consulting)
- **Arena** (Rockwell Automation, ~$10k-$30k + training)
- **Simul8** (~$5k-$15k + consulting)
- **FlexSim** (~$30k-$60k, 3D visualization)

**What you get**:
- GUI-based modeling (drag-and-drop)
- Built-in distributions, animation, reporting
- Consulting/training from vendor

**Cost breakdown** (AnyLogic example):
- Software license: $15k/year (Professional Edition)
- Consulting for model build: $50k-$100k (2-4 weeks @ $10k-$15k/week)
- Training: $5k (2-day workshop)
- **Total Year 1: $70k-$120k**

**Pros**:
- Turnkey solution
- Professional animation for stakeholder presentations
- Support included

**Cons**:
- Expensive (especially if one-time analysis)
- Still requires learning vendor's paradigm
- Consultant dependency (you don't own the expertise)
- Licensing lock-in (annual renewal)

**Verdict**: ⚠️ Good for recurring use or large-scale projects. Overkill for one-time Q4 analysis.

---

### Option 4: Python Script with Discrete Event Simulation Library

**Approach**: Export data from WMS (CSV), build custom simulation in Python, run scenarios, present results.

**Cost**:
- Software: $0 (open-source: SimPy, salabim, Ciw)
- Developer time: 2-3 weeks (1 FTE @ $80-$120/hr loaded = $6,400-$14,400)
- **Total: $6k-$15k**

**What you get**:
- Custom model tailored to your specific bottleneck
- Full control and transparency (Python code you own)
- Reusable for future analyses (next year's peak, new facility design)
- Integration with existing data pipeline (pandas for WMS CSV import)

**Which Python library?**

#### Decision Tree (1.120 Framework):

**Q1: Agent-based or process-based?**
→ Process-based (orders flow through pick → pack → ship)

**Q2: Primarily a queueing network?**
→ **YES** - Orders wait for pickers, wait for packing stations, wait for loading docks.

**Recommendation: Ciw** (specialized queueing library)

**Alternative: SimPy** (if you need more flexibility beyond queues)

---

## Why Ciw Wins Here

### Your System as a Queueing Network:

```
Orders arrive → Queue 1 (wait for picker) → Pick station (μ₁=8 picks/hr per picker)
              → Queue 2 (wait for packer) → Pack station (μ₂=12 packs/hr per packer)
              → Queue 3 (wait for dock) → Load dock (μ₃=20 trucks/hr per dock)
```

**Parameters from WMS data**:
- λ (arrival rate): Varies by hour (see WMS timestamp data)
  - 6-9am: λ=20 orders/hr
  - 9-12pm: λ=180 orders/hr (peak!)
  - 12-5pm: λ=60 orders/hr
- μ₁ (pick rate): 8 picks/hr per picker (from labor time studies)
- μ₂ (pack rate): 12 packs/hr per packer
- μ₃ (dock rate): 20 loads/hr per dock

**Ciw advantages**:
1. **Queueing-native abstractions**: Define arrival distributions, service distributions, routing in 20 lines of code.
2. **Built-in statistics**: Automatically tracks wait times, queue lengths, utilization.
3. **Minimal learning curve**: If you understand queueing notation (λ, μ, ρ), Ciw maps directly.

**Code structure** (conceptual):
```python
import ciw
import pandas as pd

# Import WMS data
orders = pd.read_csv('wms_orders_2023.csv')
arrivals_by_hour = orders.groupby('hour').size()

# Define network
N = ciw.create_network(
    arrival_distributions=[ciw.dists.Empirical(arrivals_by_hour)],
    service_distributions=[
        ciw.dists.Exponential(8),   # Picking
        ciw.dists.Exponential(12),  # Packing
        ciw.dists.Exponential(20)   # Loading
    ],
    number_of_servers=[40, 10, 8]  # 40 pickers, 10 packers, 8 docks
)

# Run simulation
Q = ciw.Simulation(N)
Q.simulate_until_max_time(24 * 90)  # 90 days
records = Q.get_all_records()

# Analyze results
wait_times = [r.waiting_time for r in records]
print(f"Average wait: {sum(wait_times)/len(wait_times):.1f} hrs")
print(f"95th percentile wait: {sorted(wait_times)[int(0.95*len(wait_times))]:.1f} hrs")
```

**Outputs you need for CFO**:
- Current system: Avg wait 3.2 hours, 95th percentile 8.4 hours (unacceptable)
- Add evening shift: Avg wait 3.1 hours (minimal improvement—problem is morning peak!)
- Add 10 pickers (morning shift only): Avg wait 1.8 hours, 95th percentile 4.2 hours
- Recommendation: Add 10 pickers to morning shift ($60k for Q4) instead of leasing warehouse ($180k)

---

## Integration with Your WMS

### Data Export (One-Time Setup):

**From WMS** (example: Infor WMS):
1. Report: "Order timestamps by hour (past 2 years)"
   - Columns: `order_id`, `created_timestamp`, `picked_timestamp`, `packed_timestamp`, `shipped_timestamp`
2. Export as CSV

**From labor system** (Kronos, ADP, etc.):
1. Report: "Average pick time by SKU category"
   - Used to calculate μ (service rate)

### Python Pipeline:

```python
import pandas as pd

# Load WMS data
orders = pd.read_csv('wms_export.csv', parse_dates=['created_timestamp'])

# Calculate interarrival times (for arrival distribution)
orders['hour'] = orders['created_timestamp'].dt.hour
arrivals = orders.groupby('hour').size()

# Calculate service times (for service distribution)
orders['pick_duration'] = (orders['picked_timestamp'] - orders['created_timestamp']).dt.seconds / 3600
pick_rate = 1 / orders['pick_duration'].mean()  # μ = 1/avg_service_time

# Feed into Ciw simulation (see above)
```

**No integration required**: This is a one-way export, not a live integration. You're not modifying WMS or pushing data back.

---

## ROI Calculation

### Investment Options:

| Option | Cost | Outcome |
|--------|------|---------|
| **Do nothing** | $0 | Repeat last year: $400k penalties |
| **Lease overflow warehouse** | $180k | Solves space, not labor bottleneck: Still $200k penalties |
| **Add evening shift** | $240k | Wrong shift (orders arrive in morning): $300k penalties |
| **SimPy/Ciw analysis → targeted solution** | $10k dev + $60k (10 pickers, morning shift) | Solves bottleneck: $0 penalties |

**Net benefit**: $400k (avoided penalties) - $70k (analysis + labor) = **$330k saved**

**ROI**: 330k / 70k = **4.7x return**

---

## Deliverables (What You Present to CFO)

### 1. Baseline Analysis (Current State):
- "With current resources (40 pickers), peak wait time is 8.4 hours (95th percentile). This violates our 4-hour SLA."

### 2. Scenario Comparison:
| Scenario | Cost | Avg Wait | 95th % Wait | SLA Violations |
|----------|------|----------|-------------|----------------|
| **Current (baseline)** | $0 | 3.2 hrs | 8.4 hrs | 42% |
| **Lease warehouse** | $180k | 3.1 hrs | 8.2 hrs | 40% |
| **Add evening shift** | $240k | 3.0 hrs | 8.0 hrs | 38% |
| **+10 morning pickers** | $60k | 1.8 hrs | 4.2 hrs | 8% |

### 3. Recommendation:
- "Add 10 pickers to morning shift (6am-2pm). This targets the 9-12pm bottleneck. Cost: $60k for Q4. Expected savings: $330k (avoided penalties + customer retention)."

### 4. Visualization (Python/matplotlib):
- Time-series chart: Queue length over 24 hours (show morning spike)
- Histogram: Wait time distribution (show 95th percentile)

### 5. Sensitivity Analysis:
- "If order volume increases 50% (vs forecasted 40%), we need 12 additional pickers, not 10. Cost increases to $72k."

---

## Why This Approach Wins

### vs. Spreadsheet:
✅ Models queuing dynamics (morning peak, not just total capacity)
✅ Captures randomness (orders don't arrive like clockwork)
✅ Statistical confidence (run 100 replications, report 95% CI)

### vs. WMS Upgrade:
✅ Timeline: 2-3 weeks, not 18 months
✅ Cost: $10k, not $500k+
✅ Flexibility: Custom model for your specific bottleneck

### vs. Commercial DES Software:
✅ Cost: $10k, not $70k-$120k
✅ Ownership: You own the code, not locked into vendor
✅ Reusability: Next year, next facility, next problem—same Python skills

---

## Implementation Timeline

### Week 1: Data & Setup
- Export WMS data (1 day)
- Install Python, Ciw, pandas (1 hour)
- Exploratory data analysis (2 days)

### Week 2: Model Build
- Build baseline Ciw model (2 days)
- Validate against historical data (2 days)
- Refine distributions (1 day)

### Week 3: Scenarios & Reporting
- Run scenario experiments (1 day)
- Statistical analysis (1 day)
- Build visualizations (1 day)
- Prepare CFO presentation (1 day)

**Total: 15 working days = 3 weeks**

---

## Required Skills

### Must-have:
- **Python fundamentals**: Functions, loops, pandas DataFrames
- **Basic statistics**: Mean, percentiles, confidence intervals
- **Domain knowledge**: Understand your warehouse operations (pick/pack/ship flow)

### Nice-to-have (but not required):
- Advanced Python (generators, OOP): Ciw hides this complexity
- Queueing theory (M/M/c): Helpful for validation, but Ciw handles the math
- Visualization (matplotlib, seaborn): Can outsource to analyst

### Learning resources:
- **Ciw docs**: https://ciw.readthedocs.io/ (2-hour read)
- **Queueing theory primer**: "Introduction to Queueing Theory" (Sundarapandian) - Ch 1-3
- **Pandas for data wrangling**: "Python for Data Analysis" (McKinney) - Ch 5-7

---

## What Could Go Wrong?

### Risk 1: Garbage In, Garbage Out
**Problem**: WMS data is incomplete (missing timestamps, outliers).
**Mitigation**: Data cleaning step. Remove outliers (>99th percentile). Validate sample size (need 1000+ orders for stable distributions).

### Risk 2: Model Doesn't Match Reality
**Problem**: Simulation predicts 1.8 hrs avg wait, but real-world is 2.5 hrs.
**Mitigation**: Validation phase (Week 2). Compare simulation to historical data. If mismatch, refine distributions or add complexity (e.g., picker fatigue, equipment breakdowns).

### Risk 3: Stakeholder Skepticism
**Problem**: CFO doesn't trust "a Python script."
**Mitigation**:
- Validate against queueing theory (M/M/c formula for simple case)
- Show animation (salabim if needed for presentation)
- Run sensitivity analysis (show robustness to assumptions)

### Risk 4: Peak is More Extreme Than Forecasted
**Problem**: Sales forecasts 40% increase, reality is 60%.
**Mitigation**: Scenario planning. Run simulation at 40%, 50%, 60% to show "if volume is X, we need Y pickers."

---

## When to Use Each Approach

### Use Spreadsheet:
- Deterministic system (no randomness)
- Simple capacity calculation (no queues)
- Quick back-of-envelope estimate

### Use Python/Ciw:
- **This scenario** (queuing, randomness, moderate complexity)
- One-time or annual analysis
- You have developer resources (in-house or consultant)

### Use Commercial DES Software:
- Recurring analyses (monthly capacity reviews)
- Need professional animation for board presentations
- Budget allows ($50k-$100k+)
- Lack internal Python expertise

### Use WMS Upgrade:
- Strategic overhaul (not just capacity planning)
- Multi-year timeline
- Budget allows ($500k-$2M)

---

## Parallel to Your QuickBooks/Tariff Example

| Your Example | This Example |
|--------------|--------------|
| **You have**: QuickBooks | **You have**: Warehouse Management System |
| **Question**: Tariff impact on margins | **Question**: Q4 capacity planning |
| **Option 1**: Buy FP&A software (Adaptive, Anaplan) | **Option 1**: Upgrade WMS (Manhattan, Blue Yonder) |
| **Option 2**: Upgrade to NetSuite/Sage | **Option 2**: Commercial DES software (AnyLogic, Arena) |
| **Option 3**: Export QB data → Python script | **Option 3**: Export WMS data → Python script (Ciw/SimPy) |
| **Decision**: Which library? (pandas, numpy, scikit) | **Decision**: Which library? (Ciw, SimPy, salabim) |
| **Research**: "Do I need optimization (scipy.optimize)?" | **Research**: "Do I need queueing (Ciw) or general DES (SimPy)?" |

**Same decision pattern**:
1. Real business problem with financial stakes
2. Data locked in existing system (QuickBooks / WMS)
3. Options span spectrum (expensive turnkey → custom script)
4. Python wins on cost, flexibility, timeline
5. Library choice matters (pandas vs. scikit vs. pulp vs. Ciw vs. SimPy)

---

## Next Steps

### If you're in this scenario right now:

1. **Export WMS data** (1 day):
   - Order timestamps (created, picked, packed, shipped)
   - Historical volume by hour

2. **Install Ciw** (1 hour):
   ```bash
   pip install ciw pandas matplotlib
   ```

3. **Run tutorial** (2 hours):
   - https://ciw.readthedocs.io/en/latest/Tutorial-I/
   - Adapt to your data

4. **Build minimal model** (1 week):
   - Single queue (picking only)
   - Validate against historical avg wait time

5. **Expand to full system** (1 week):
   - Multi-stage (pick → pack → load)
   - Run scenario experiments

6. **Present results** (1 day):
   - Scenario comparison table
   - Recommendation with ROI

**Total timeline: 3 weeks from start to CFO presentation.**

---

## Further Reading

### For this specific scenario:
- **Ciw docs**: https://ciw.readthedocs.io/
- **Queueing theory**: Gross & Harris, "Fundamentals of Queueing Theory" (Ch 2: M/M/c)
- **Warehouse optimization**: Tompkins et al., "Facilities Planning" (Ch 9: Order picking)

### For general DES decision-making:
- S1-rapid/recommendation.md (library selection)
- S3-need-driven/integration-patterns.md (data pipelines)
- S3-need-driven/use-cases.md (other industries)

### For ROI justification:
- Law, "Simulation Modeling and Analysis" (Ch 12: Output analysis, confidence intervals)
- Kelton et al., "Simulation with Arena" (Ch 10: Comparing alternatives)
