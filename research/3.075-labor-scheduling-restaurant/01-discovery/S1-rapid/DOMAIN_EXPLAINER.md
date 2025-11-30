# Labor Scheduling Domain Explainer

**Target Audience**: Restaurant operators evaluating scheduling platforms
**Purpose**: Explain technical concepts, compliance requirements, and optimization strategies
**Reading Time**: 15-20 minutes
**Last Updated**: 2025-11-30

---

## Table of Contents

1. [Fair Workweek Laws & Compliance](#fair-workweek-laws--compliance)
2. [AI & Optimization Technologies](#ai--optimization-technologies)
3. [Labor Cost Management](#labor-cost-management)
4. [System Integration & Data Flow](#system-integration--data-flow)
5. [Employee Features](#employee-features)
6. [Multi-Location Operations](#multi-location-operations)

---

## Fair Workweek Laws & Compliance

### Seattle Secure Scheduling Ordinance

**What it is**: A 2017 Seattle law requiring predictable work schedules for retail and food service employees. Restaurants with 500+ employees globally (including franchises) must comply.

**Key Requirements**:
1. **14-day advance notice**: Post schedules at least 14 days before the start of the work period
2. **Good faith estimate**: Provide new hires with estimated work hours and schedule
3. **Right to rest**: 10+ hours between shifts (or employee consent + premium pay)
4. **Predictability pay**: Compensate employees for last-minute schedule changes

**Penalties**: $500-2,000 per violation. Without automation, restaurants face $3,000-12,000/year in fines.

**Similar Laws**: San Francisco (2015), New York City (2017), Philadelphia (2019), Chicago (2020), Oregon statewide (2018).

---

### Predictability Pay

**What it is**: Financial compensation owed to employees when employers change schedules with short notice.

**Seattle Calculation**:
- **<24 hours notice**: $40 payment (or consent)
- **24-48 hours notice**: $20 payment
- **Adding hours**: $10-20 depending on notice
- **Canceling shift**: Pay 50% of scheduled hours

**Example**:
- **Tuesday 3pm**: Manager cancels Thursday evening shift (39 hours notice)
- **Owed**: $20 predictability pay + 50% of shift pay (e.g., 4 hours × $18/hr × 50% = $36)
- **Total**: $56 for a canceled shift

**Why automation matters**: Manual tracking misses violations. Platforms like HotSchedules and Deputy auto-calculate predictability pay when managers change schedules.

---

### Clopening

**What it is**: Scheduling an employee to close the restaurant (10pm-midnight) and then open it the next morning (6-8am). The term combines "closing" + "opening."

**Problem**:
- Employee gets <8 hours rest between shifts
- Violates Seattle ordinance (10+ hours required)
- Causes fatigue, turnover, safety issues

**Example Violation**:
- **Shift 1**: Server works Tuesday 4pm-11pm (close)
- **Shift 2**: Same server works Wednesday 7am-3pm (open)
- **Gap**: 8 hours (violates 10-hour rule)
- **Penalty**: $40 predictability pay (unless employee consents)

**Platform Prevention**:
- HotSchedules, Deputy, OR-Tools flag clopening during scheduling
- Auto-calculate rest period violations
- Warn managers before publishing schedules

---

### Break Compliance

**What it is**: State-specific laws requiring meal breaks (unpaid) and rest breaks (paid).

**Washington State (Example)**:
- **Meal break**: 30 minutes unpaid for shifts >5 hours
- **Rest break**: 10 minutes paid per 4 hours worked
- **Timing**: Meal break must occur between hour 2 and hour 5 of shift

**Why tracking matters**: Forgetting breaks = wage & hour violations. Employees can sue for missed breaks.

**Platform Features**:
- Auto-schedule breaks into shifts
- Alerts when breaks not taken (time-tracking integration)
- State-specific rules (CA different from WA)

---

## AI & Optimization Technologies

### AI-Based Demand Forecasting

**What it is**: Machine learning models predict customer traffic (covers, sales) based on historical data, weather, events, and seasonality.

**How it works**:
1. **Data inputs**: POS sales by 15-minute intervals, day of week, weather forecasts, local events (concerts, sports), holidays
2. **Model training**: AI analyzes 6-12 months of historical patterns
3. **Prediction output**: "Thursday 6-7pm: expect 45 covers, need 3 servers + 1 bartender"

**Example** (HotSchedules AI):
- **Historical data**: Past 8 Thursdays averaged 42 covers at 6pm
- **Weather forecast**: Sunny 75°F Thursday (vs rainy last month)
- **Event data**: Mariners game 7pm nearby (stadium API integration)
- **AI prediction**: 65 covers (55% increase due to game + weather)
- **Staffing recommendation**: Add 1 server (30 covers/server ratio)

**Accuracy**: 85-92% for established locations with 6+ months data. New restaurants need 3-6 months before forecasting is reliable.

**ROI**: Prevents overstaffing (2-3% labor cost reduction) and understaffing (lost sales, poor service).

---

### Constraint Programming (OR-Tools)

**What it is**: A mathematical optimization technique for scheduling that guarantees solutions satisfy all constraints (rules) while minimizing cost or maximizing fairness.

**How it differs from AI**:
- **AI**: Learns patterns, makes predictions (probabilistic)
- **Constraint programming**: Enforces hard rules, guarantees optimality (deterministic)

**Restaurant Scheduling Constraints**:
1. **Hard constraints** (must satisfy):
   - Each shift has exactly 1 server
   - No employee works >40 hours/week
   - Server shifts require Server skill
   - No clopening (<10 hours between shifts)
   - Employee availability windows

2. **Soft constraints** (optimize):
   - Minimize total labor cost
   - Maximize fairness (balance hours across employees)
   - Prefer senior staff for weekend shifts

**Example** (OR-Tools Python code):
```python
# Hard constraint: No employee works >40 hours/week
for employee in employees:
    total_hours = sum(shift.hours * assigned[employee, shift] for shift in shifts)
    model.Add(total_hours <= 40)

# Objective: Minimize labor cost
total_cost = sum(employee.hourly_rate * shift.hours * assigned[employee, shift])
model.Minimize(total_cost)
```

**Solve time**: <1 second for typical restaurant (30 employees, 7 days, 3 shifts/day). Enterprise schedulers (HotSchedules) use similar algorithms under the hood.

**When to use**: Custom constraints not supported by SaaS (e.g., "senior staff first pick of Friday night shifts" + "balance weekend shifts fairly" + "Seattle ordinance compliance").

---

### Auto-Scheduling

**What it is**: One-click schedule generation based on demand forecasts and constraints.

**How platforms implement it**:

**HotSchedules (AI + Rules)**:
1. AI forecasts demand: "Thursday 6-8pm: 50 covers"
2. Labor rules: "1 server per 30 covers = 2 servers needed"
3. Constraints: Employee availability, skills, overtime limits
4. Algorithm: Assign lowest-cost employees meeting constraints
5. Output: Complete schedule for next 2 weeks

**OR-Tools (DIY)**:
1. Define variables: `assigned[employee, shift] = 1 if assigned, 0 otherwise`
2. Add constraints: No clopening, max 40 hours, skill requirements
3. Set objective: Minimize labor cost
4. Solve: Optimal schedule in <1 second

**Manager override**: All platforms allow manual adjustments. AI suggestions are starting point, not final schedule.

---

## Labor Cost Management

### Labor Percentage (Labor %)

**What it is**: Labor cost as percentage of revenue. Primary metric for restaurant profitability.

**Calculation**: `Labor % = (Total Labor Cost / Total Revenue) × 100`

**Example**:
- **Revenue**: $10,000 (Friday night)
- **Labor cost**: $3,200 (server wages + benefits)
- **Labor %**: 32%

**Industry Benchmarks**:
- **Quick service**: 25-30%
- **Casual dining**: 30-35%
- **Fine dining**: 35-40%

**Why real-time tracking matters**:
- Without integration: Calculate labor % at end of week (too late to adjust)
- With POS integration: See labor % while scheduling ("Adding 4pm server increases labor % to 33%")

**Platform Features**:
- **Sling + Toast**: Real-time labor % during shift creation
- **HotSchedules**: Labor % forecasting based on predicted sales
- **7shifts**: Post-shift labor % reports (no real-time forecasting)

---

### Covers

**What it is**: Number of guests served. Used to calculate staffing needs.

**Staffing Ratios** (industry standards):
- **Servers**: 1 server per 20-30 covers (casual dining), 1 per 15-20 (fine dining)
- **Kitchen**: 1 cook per $500/hour sales
- **Bartenders**: 1 per 30-40 bar guests

**Example Calculation**:
- **Forecast**: 120 covers on Saturday 5-9pm (4 hours)
- **Ratio**: 1 server per 25 covers
- **Staffing need**: 120 ÷ 25 = 4.8 servers → Schedule 5 servers

**Platform Usage**:
- AI platforms (HotSchedules, Deputy) auto-calculate staffing from covers forecast
- Manual platforms (7shifts, When I Work) require manager to calculate ratios

---

### Overtime Prevention

**What it is**: Alerts when employees approach 40 hours/week (or state threshold like California 8 hours/day).

**Cost Impact**:
- **Regular pay**: $18/hour
- **Overtime pay**: $27/hour (1.5× for hours >40/week)
- **Unplanned OT**: Scheduling employee 42 hours costs extra $54/week

**How platforms prevent it**:
1. **Weekly hour tracking**: Sum all scheduled shifts
2. **Alerts**: Warn manager when adding shift pushes employee >40 hours
3. **Auto-suggestions**: Recommend alternative employee with <40 hours

**Example** (Deputy):
- **Tuesday**: Manager scheduling Friday shifts
- **Current hours**: Server A has 38 hours (Mon-Thu)
- **Friday shift**: 6-hour shift proposed
- **Alert**: "Server A will reach 44 hours (4 hours OT). Suggest Server B (32 hours)."

---

## System Integration & Data Flow

### POS Integration

**What it is**: Two-way data sync between Point-of-Sale system and scheduling platform.

**Data Flow**:

**POS → Scheduler**:
1. **Sales data**: Revenue by 15-minute intervals (for AI forecasting)
2. **Employee clock-ins**: Actual hours worked (for payroll)
3. **Employee roster**: Names, roles, pay rates (auto-sync)
4. **Historical covers**: Guest counts per shift (for staffing ratios)

**Scheduler → POS**:
1. **Published schedules**: Who's working when (for POS login access)
2. **Time-off approvals**: Blocked PTO dates (prevent clock-ins)
3. **Labor budgets**: Target labor % per shift (for real-time alerts)

**Native vs API Integration**:
- **Native** (Sling + Toast): Built by same company, zero setup, instant sync
- **API** (HotSchedules + Toast): Third-party integration, 2-4 weeks setup, 99% reliability

**Why it matters**:
- **Without integration**: Manually export timesheets, re-enter in payroll (2-5 hours/week)
- **With integration**: One-click timesheet export, auto-populated pay rates (15 minutes/week)

---

### Payroll Export

**What it is**: Transferring approved timesheets from scheduling platform to payroll system.

**Manual Process** (no integration):
1. Export timesheets as CSV from scheduling platform
2. Open payroll software (Gusto, ADP, Paychex)
3. Manually enter hours per employee
4. Verify totals, submit payroll
5. **Time**: 2-5 hours every 2 weeks

**Automated Process** (integration):
1. Click "Export to Payroll" in scheduling platform
2. Timesheets auto-populate in payroll system
3. Review and approve (verify overtime, tips)
4. Submit payroll
5. **Time**: 15-30 minutes every 2 weeks

**Supported Integrations**:
- **7shifts**: Gusto, ADP, Paychex, Toast Payroll
- **Deputy**: 40+ payroll systems
- **HotSchedules**: ADP, Paychex, Toast, Gusto
- **Sling**: Native Toast Payroll, limited third-party

---

## Employee Features

### Shift Swaps

**What it is**: Employee-initiated schedule changes where one worker trades their shift with another.

**How it works**:
1. **Employee A** (scheduled Friday): Requests swap via mobile app
2. **Platform**: Notifies eligible employees (same role, available Friday)
3. **Employee B**: Accepts swap offer
4. **Manager**: Approves or denies (automatic approval optional)
5. **Schedule**: Updates automatically, sends push notifications

**Business Rules**:
- **Skill matching**: Server can only swap with another server (not cook)
- **Overtime prevention**: Block swap if Employee B would exceed 40 hours
- **Manager approval**: Optional (auto-approve or require review)

**Benefits**:
- Reduces manager workload (no phone tag coordinating swaps)
- Employees control schedules (improves satisfaction)
- Maintains shift coverage (platform enforces skill/availability rules)

---

### Time-Off Requests

**What it is**: Formal PTO (Paid Time-Off) request and approval workflow.

**Traditional Process** (no platform):
1. Employee texts manager: "Can I take Dec 15 off?"
2. Manager checks schedule (paper or spreadsheet)
3. Approves verbally or via text
4. Manager forgets to block date in schedule
5. **Result**: Employee shows up expecting day off, shift uncovered

**Platform Process**:
1. Employee submits request in app (selects date, reason)
2. Manager receives push notification
3. Manager approves or denies (visible to all)
4. **Automatic blocking**: Platform prevents scheduling employee on approved PTO dates
5. **Accrual tracking**: Shows remaining PTO balance (e.g., "5 days left")

**Compliance Features**:
- **Blackout dates**: Block PTO during peak periods (New Year's Eve)
- **Minimum staffing**: Deny request if too many employees off same day
- **Audit trail**: Track all requests, approvals, denials (for labor disputes)

---

### Availability Management

**What it is**: Employee-declared windows when they can or cannot work.

**Types**:
1. **Recurring availability**: "Never schedule me Sundays" (weekly pattern)
2. **One-time availability**: "Can't work Dec 20-27" (vacation)
3. **Preferred shifts**: "Prefer 5-9pm Friday/Saturday" (not guaranteed)

**How platforms use it**:
- **Hard constraint**: Never schedule employee outside availability windows
- **Soft constraint**: Prefer scheduling during preferred times (if possible)
- **Auto-scheduling**: AI only assigns shifts matching availability

**Example** (7shifts):
- **Server A availability**: Mon-Thu 11am-9pm, Fri-Sat unavailable
- **Manager creates Friday shift**: Platform grays out Server A (unavailable)
- **Auto-schedule**: AI only considers Mon-Thu for Server A

---

## Multi-Location Operations

### Centralized Scheduling

**What it is**: Corporate office manages scheduling for multiple restaurant locations from single dashboard.

**Features**:
1. **Unified view**: See all 10 locations' schedules side-by-side
2. **Template push**: Corporate creates standard schedule, pushes to locations
3. **Local customization**: Location managers adjust for local needs
4. **Cross-location comparison**: "Location A has 32% labor %, Location B has 28%"

**Governance Models**:

**Fully Centralized**:
- Corporate schedules all locations
- Location managers cannot edit schedules
- **Use case**: Standardized operations (Starbucks)

**Hybrid**:
- Corporate sets labor budget and templates
- Location managers create schedules within budget
- **Use case**: Franchises (corporate guidelines, local execution)

**Fully Decentralized**:
- Location managers have full control
- Corporate has read-only visibility
- **Use case**: Independent locations with shared ownership

---

### Labor Pool Sharing

**What it is**: Moving employees between nearby locations to cover staffing shortages.

**Example Scenario**:
- **Location A** (Downtown): 2 servers called in sick Friday night
- **Location B** (Suburb, 15 min away): Fully staffed, slow night forecasted
- **Action**: Shift 2 servers from Location B to Location A
- **Result**: Location A fully staffed, Location B reduces labor % (slow night)

**Platform Features**:
- **Cross-location visibility**: See all locations' schedules + needs
- **Availability tracking**: Know which employees willing to work other locations
- **Travel compensation**: Auto-calculate mileage reimbursement (optional)
- **Compliance**: Ensure Seattle ordinance 14-day notice applies across locations

**Limitations**:
- Employees must consent to work other locations (contractual)
- Travel time counted as work hours (FLSA compliance)
- State laws differ (WA vs OR labor rules if locations cross state line)

---

## Key Takeaways

### For Small Restaurants (1 location, <20 employees):
- **Start with free tier**: 7shifts Comp (20 employees free) or Deputy Starter (100 shifts free)
- **Focus on time savings**: 2-5 hours/week saved vs paper schedules
- **Compliance optional**: Unless in Seattle/SF/NYC (then prioritize Deputy/HotSchedules)

### For Multi-Location Chains (3-10 locations):
- **AI forecasting ROI**: 2-3% labor cost reduction = $30K-90K/year savings
- **Centralized management**: Corporate visibility critical for standardization
- **Compliance automation**: Seattle/SF/NYC fines ($3K-12K/year) justify platform cost

### For DIY/Tech-Savvy (Python developer available):
- **OR-Tools**: Free, unlimited constraints, full customization
- **Break-even**: 18 months vs Deputy, Year 2+ cheaper than any SaaS
- **Custom compliance**: Implement exact Seattle ordinance rules (not approximations)

### For Toast POS Users:
- **Sling obvious choice**: Native integration, $1.70/user, real-time labor %
- **ROI**: 2,510% for Toast users (vs 856% without Toast integration)

---

## Glossary Quick Reference

| Term | Simple Definition |
|------|-------------------|
| **Clopening** | Closing + opening shifts <10 hours apart (illegal in Seattle) |
| **Predictability pay** | $10-40 owed for last-minute schedule changes |
| **Labor %** | Labor cost ÷ revenue × 100 (target: 30-35%) |
| **Covers** | Number of guests served (staffing ratio: 1 server per 25 covers) |
| **Constraint programming** | Math optimization guaranteeing rules satisfied (OR-Tools) |
| **AI forecasting** | Machine learning predicting sales/covers (HotSchedules) |
| **POS integration** | Automatic sync of sales data, timesheets, employee roster |
| **Auto-scheduling** | One-click schedule generation from AI + rules |
| **Shift swap** | Employee-initiated schedule trade (peer-to-peer) |
| **Availability** | Employee-declared work windows (hard constraint) |

---

## Further Reading

**Seattle Secure Scheduling Ordinance**:
- [Official Seattle.gov Summary](https://www.seattle.gov/laborstandards/ordinances/secure-scheduling)
- [Employer Compliance Guide](https://www.seattle.gov/laborstandards/ordinances/secure-scheduling/employers)

**OR-Tools Constraint Programming**:
- [Google OR-Tools Employee Scheduling Tutorial](https://developers.google.com/optimization/scheduling/employee_scheduling)
- [Constraint Programming Basics](https://developers.google.com/optimization/cp)

**Restaurant Labor Cost Optimization**:
- [National Restaurant Association: Controlling Labor Costs](https://restaurant.org/research/reports/labor-cost/)
- [Toast: How to Calculate Labor Cost Percentage](https://pos.toasttab.com/blog/labor-cost-percentage)
