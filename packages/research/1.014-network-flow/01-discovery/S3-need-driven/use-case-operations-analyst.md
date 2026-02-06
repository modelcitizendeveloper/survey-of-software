# Use Case: Operations Analyst

## Who Needs This

**Persona**: Jessica, Operations Analyst at hospital network

**Context**:
- Managing nurse staffing for 8 hospitals in metro area
- 400 nurses, 200+ shifts per week
- Team: Jessica + 2 junior analysts, reporting to Operations Director
- Current system: Excel spreadsheets + manual assignment
- Regulations: Nurse-to-patient ratios, skill requirements, union rules

**Current situation**:
- Weekly nurse scheduling takes 12 hours
- Assignments made by "best guess" + spreadsheet sorting
- Frequent overstaffing (expensive) or understaffing (quality issues)
- Nurses complain about unfair shift distribution
- Hospital administrators pressure to reduce overtime costs
- No way to model "what-if" scenarios for staffing changes

## Pain Points

### 1. Suboptimal Assignments Cost Money
- Overstaffing common (safer but expensive)
- Overtime costs high ($2M/year excess)
- Can't balance staffing across all hospitals simultaneously
- **Cost impact**: $2M annual overtime, $1M feasible with better scheduling

### 2. Manual Process Error-Prone
- Spreadsheet formulas break when hospitals added
- Miss constraint violations (skill mismatch, ratio violations)
- Discover problems after schedule published (re-work)
- **Quality risk**: Unsafe nurse-patient ratios discovered post-facto

### 3. Fairness Complaints
- Nurses perceive favoritism in assignments
- No transparent rationale for shift distribution
- Union grievances: "Why does Sarah get more weekend shifts?"
- **Employee satisfaction**: High turnover from unfair scheduling

### 4. Can't Plan Ahead
- What if we hire 20 more nurses? Where should they go?
- What if hospital A closes an ICU ward?
- What if we open urgent care center?
- **Strategic paralysis**: Can't model staffing impact of changes

## Why Network Flow Libraries Matter

**The assignment opportunity:**

Current state (manual):
- 400 nurses → 200 shifts
- Constraints: Skills, ratios, preferences, hours
- Jessica's process: Sort by seniority, assign manually
- Result: Suboptimal, takes 12 hours, errors common

With min-cost assignment (bipartite matching):
- Model as min-cost flow: Nurses (sources) → Shifts (sinks)
- Capacity constraints: Nurse hours, shift requirements
- Costs: Overtime cost, skill mismatch penalty, preference violations
- **Result: Optimal assignment in 2 minutes**

**Concrete example:**

```
Before (manual):
Hospital A: 45 nurses scheduled, need 40 (overstaffed)
Hospital B: 38 nurses scheduled, need 40 (understaffed, pay overtime)
Total cost: $48K for week (overtime + overstaffing)

After (optimized assignment):
Hospital A: 40 nurses (exactly needed)
Hospital B: 40 nurses (exactly needed)
Total cost: $42K for week
Savings: $6K/week = $312K/year
```

**Fairness and transparency:**

Manual: "Jessica decides" (opaque)
Optimized: "Algorithm minimizes cost while respecting constraints"
→ Transparent rules, objective assignments
→ Union satisfied: Fair distribution

## Requirements

### Must-Have
1. **Handles constraints**: Skills, ratios, hours, preferences
2. **Minimizes cost**: Overtime + overstaffing costs
3. **Fast enough for weekly use**: Solution in < 10 minutes
4. **Easy to explain**: Jessica can show administrators the logic
5. **Excel integration**: Import nurse data, export schedules

### Nice-to-Have
1. Scenario analysis (compare 3-4 staffing plans)
2. Preference optimization (nurse shift preferences)
3. Historical analysis (identify chronic understaffing)
4. Visualization (schedules, assignments)

### Don't Care About
1. Real-time optimization (weekly planning is fine)
2. Fancy UI (Excel export is sufficient)
3. Million-node scale (400 nurses max)

## Decision Criteria

**Jessica evaluates options by asking**:

1. **Will this reduce overtime costs?**
   - Proven in healthcare/workforce scheduling
   - Can model complex constraints (skills, ratios)
   - Confident assignments are correct (no violations)

2. **Can I actually use it?**
   - Jessica has Excel/Python skills, not CS degree
   - Documentation for assignment problems
   - Examples similar to nurse scheduling

3. **Will management buy in?**
   - Can explain the logic (not black box)
   - Can show cost savings in pilot
   - Integrates with existing Excel workflows

4. **Will nurses trust it?**
   - Transparent constraint rules
   - Respects preferences where possible
   - Fair distribution (provably optimal, not subjective)

## Recommended Solution

**NetworkX** (for initial prototype) → **OR-Tools** (for production)

### Why This Progression

**Phase 1: NetworkX prototype (Week 1-2)**
- Jessica learns network flow concepts
- Builds simple assignment model (50 nurses, 30 shifts)
- Validates against manual assignments
- **Goal**: Prove concept works, build confidence

**Phase 2: OR-Tools production (Week 3-6)**
- Scale to full 400 nurses, 200 shifts
- Add all constraints (skills, ratios, preferences)
- Integrate with Excel (import/export)
- **Goal**: Replace manual scheduling

### Why NetworkX First

1. **Gentler learning curve**: Jessica is analyst, not programmer
   - Python-first API (readable code)
   - Good documentation with examples
   - Can prototype in Jupyter notebook

2. **Validates the approach**:
   - Runs small pilot (50 nurses)
   - Shows management the concept
   - Builds confidence before production investment

3. **Quick win**:
   - 2 weeks to working prototype
   - Demonstrates feasibility
   - Secures buy-in for OR-Tools investment

### Why OR-Tools for Production

1. **Handles full scale**: 400 nurses, 200 shifts, complex constraints
   - NetworkX too slow for production (15+ minutes)
   - OR-Tools: 2-3 minutes (fast enough for weekly use)

2. **Constraint modeling**: Built for assignment problems
   - Nurse skills → shift requirements (bipartite matching)
   - Capacity constraints (hours, ratios)
   - Cost optimization (minimize overtime)

3. **Production reliability**:
   - Battle-tested in workforce scheduling
   - Correct solutions (no constraint violations)
   - Used by other healthcare systems

### Implementation Reality

**Week 1-2: NetworkX pilot**
- Jessica learns network flow basics (8 hours)
- Builds prototype with 50 nurses, 30 shifts (12 hours)
- Test vs. manual assignment: 5% cost reduction
- **Demo to management**: "This works, let's scale it"

**Week 3-4: OR-Tools learning**
- Learn OR-Tools constraint API (12 hours)
- Port NetworkX prototype to OR-Tools (8 hours)
- Add full constraints (skills, ratios, preferences) (12 hours)
- Result: Production-ready solver

**Week 5: Excel integration**
- Build import pipeline (nurse data from Excel)
- Build export pipeline (schedule to Excel)
- Test with historical data (validate correctness)
- Result: End-to-end system

**Week 6: Pilot run**
- Run OR-Tools for one week's schedule
- Compare vs. manual: 12% cost reduction
- No constraint violations
- Management approves full rollout

**Month 2+: Production use**
- Weekly scheduling: 12 hours manual → 30 minutes automated
- Jessica freed up to analyze trends, not create schedules
- Overtime costs down 15% ($300K/year savings)
- Nurse satisfaction up (fairer shift distribution)

### ROI

**Development cost**:
- Jessica's time: 80 hours @ $60/hr = $4,800
- OR-Tools: Free (Apache 2.0 license)
- **Total investment: $4,800**

**Annual savings**:
- Overtime reduction: 15% of $2M = $300,000/year
- Overstaffing reduction: 10% of $1M = $100,000/year
- Jessica's time savings: 12 hours/week → 30 min/week
  - 11.5 hours/week @ $60/hr = $690/week = $36K/year
- **Total savings: $436K/year**

**ROI: 9,000% first year**
- $4.8K investment → $436K annual savings
- Payback period: 4 days

**Non-financial benefits**:
- Nurse satisfaction (fair scheduling)
- Union satisfaction (transparent process)
- Compliance confidence (constraint violations eliminated)
- Strategic planning (can model "what-if" scenarios)

## Success Looks Like

**6 months after adoption**:

- Weekly nurse scheduling fully automated (12 hours → 30 minutes)
- Overtime costs down 15% ($300K/year savings)
- No constraint violations (skills, ratios always met)
- Nurse complaints down 60% (fairer distribution)
- Union satisfied with transparent process
- Jessica doing strategic analysis, not manual scheduling

**Strategic wins**:

- "What-if" analysis for expansion:
  - Modeled opening urgent care center (20 nurses needed)
  - Optimized nurse hiring across all hospitals
  - Data-driven staffing decisions

- Performance improvements:
  - Identified chronic understaffing in ICU (hire 8 more nurses)
  - Identified overstaffing in outpatient (reduce 5 nurses)
  - Rebalanced $150K in annual costs

**Career impact for Jessica**:

- Presented at hospital network leadership meeting
- Promoted to Senior Operations Analyst
- Leading rollout to other hospital networks (company has 50 networks)
- Demonstrable $436K cost savings on resume
