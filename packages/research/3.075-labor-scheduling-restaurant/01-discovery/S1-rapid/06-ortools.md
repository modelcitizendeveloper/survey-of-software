# OR-Tools - DIY Constraint Solver for Custom Scheduling

**Category**: Open Source - Constraint Programming Library (DIY)
**Target Market**: Tech-savvy restaurants, custom constraint needs, budget <$100/month long-term
**Pricing**: Free (open source), development cost only
**Developer**: Google
**Status**: Active, maintained by Google Optimization Team

---

## Overview

OR-Tools is Google's open-source constraint programming and optimization library for Python (also C++, Java, C#). For restaurant scheduling, it enables unlimited custom constraints ("no clopening", "max 5 consecutive days", "senior staff first pick of weekend shifts", "skill-based assignment") and optimization objectives (minimize labor cost, maximize fairness, balance workload). It's a DIY solution requiring Python development but offers complete flexibility impossible in SaaS platforms.

## Pricing

**Software**: Free (Apache 2.0 license)

**Development Cost** (one-time):
- **DIY (in-house developer)**: 10-40 hours initial setup
  - Basic scheduling: 10-15 hours
  - Complex constraints (Seattle ordinance, skills, preferences): 20-30 hours
  - UI/mobile app: +20-40 hours if needed
- **Consultant**: $2,000-5,000 one-time (Upwork, Fiverr, local dev)

**Ongoing Maintenance**:
- **DIY**: 2-5 hours/month (bug fixes, constraint updates, new features)
- **Consultant**: $500-1,500/year retainer

**Infrastructure** (if hosting web UI):
- **Cloud server**: $5-20/month (DigitalOcean, AWS Lightsail)
- **Domain**: $12/year (optional)

**Total Year 1 Cost**:
- **DIY**: $3,000-5,000 (dev time) + $60-240 (hosting) = $3,060-5,240
- **Consultant**: $2,000-5,000 (setup) + $500/year (maintenance) + $240 (hosting) = $2,740-5,740

**Ongoing Annual Cost**:
- **DIY**: $600-1,500 (maintenance time) + $60-240 (hosting) = $660-1,740/year
- **Consultant**: $500-1,500/year (maintenance) + $240 (hosting) = $740-1,740/year

## Capabilities

### Unlimited Custom Constraints

**Example 1: Seattle Secure Scheduling Ordinance**
```python
# No clopening: 8+ hours between shifts or $40 penalty
for employee in employees:
    for shift1, shift2 in consecutive_shift_pairs:
        model.Add(shift2.start - shift1.end >= 8_hours).OnlyEnforceIf(both_assigned)
```

**Example 2: Skill-Based Assignment**
```python
# Server shifts require Server skill
for shift in server_shifts:
    model.Add(assigned_employee.has_skill('Server'))
```

**Example 3: Fairness & Preferences**
```python
# Balance weekend shifts fairly across team
weekend_shifts_per_employee = [...]
model.Minimize(max(weekend_shifts_per_employee) - min(weekend_shifts_per_employee))

# Senior staff gets first pick of preferred shifts
model.Add(senior_employees_assigned_to_preferred_shifts).Priority(weight=10)
```

### Optimization Objectives

**Minimize Labor Cost**:
```python
total_labor_cost = sum(employee.hourly_rate * shift.hours for assigned shifts)
model.Minimize(total_labor_cost)
```

**Maximize Fairness**:
```python
# Minimize variance in hours worked across employees
hours_per_employee = [...]
model.Minimize(variance(hours_per_employee))
```

**Multi-Objective Optimization**:
```python
# Minimize cost (weight=0.7) + maximize fairness (weight=0.3)
model.Minimize(0.7 * labor_cost + 0.3 * unfairness_penalty)
```

### Solver Performance

**Typical Restaurant Scenario**:
- **30 employees × 7 days × 3 shifts/day = 630 possible assignments**
- **Constraints**: No clopening, max 40 hours/week, availability, skills, fairness
- **Solve Time**: <1 second on laptop
- **Optimality**: Guaranteed optimal solution or proof of infeasibility

**Complex Scenarios** (100+ employees, multi-week planning):
- **Solve Time**: 1-10 seconds
- **Heuristic Mode**: Sub-optimal solutions in milliseconds if needed

## Strengths

✅ **Free and open source**: Zero software licensing costs
✅ **Unlimited constraint complexity**: Any business rule imaginable
✅ **Full customization**: Tailor to exact workflow, no vendor limitations
✅ **Fast optimization**: <1 second for typical restaurant (30 employees)
✅ **No vendor lock-in**: Own the code, switch providers anytime
✅ **Seattle ordinance support**: Implement exact legal requirements, not approximations
✅ **Integration flexibility**: Connect to any POS, payroll, or custom system

## Limitations

❌ **Requires Python development**: 10-40 hours setup (significant barrier)
❌ **No UI out-of-box**: Must build interface (web app, spreadsheet, or CLI)
❌ **Ongoing maintenance**: Code updates, bug fixes, new features required
❌ **No mobile app**: Unless custom-built (additional 20-40 hours)
❌ **Steeper learning curve**: Constraint programming concepts unfamiliar to non-developers
❌ **No vendor support**: Community forums only (vs paid SaaS support)

## Best For

- **Tech-savvy restaurants**: Python developer on staff or budget for consultant
- **Unique constraints**: Seattle ordinance + custom fairness rules + skill requirements (SaaS can't handle)
- **Budget <$100/month long-term**: Free software + $60/year hosting (vs $420-3,600/year SaaS)
- **Vendor independence**: Avoid lock-in, own scheduling logic
- **Complex multi-objective optimization**: Minimize cost + maximize fairness simultaneously

## Not Ideal For

- Non-technical teams (no Python developer, budget <$2K for consultant)
- Need mobile app (custom development expensive)
- Want turnkey solution (SaaS 1-week setup vs DIY 1-2 months)
- Prioritize vendor support over cost (SaaS support vs community forums)

## Decision Factors

**Choose OR-Tools if**:
- Python developer available (in-house or consultant relationship)
- Unique constraints not supported by SaaS (complex fairness, custom legal requirements)
- Budget <$100/month long-term (Year 2+ cheaper than any SaaS)
- Want complete control over scheduling logic
- Multi-location with standardized constraints (amortize dev cost across locations)

**Skip OR-Tools if**:
- No technical resources (can't code or hire consultant)
- Need mobile app (custom build too expensive)
- Want 1-week deployment (SaaS faster than DIY 1-2 months)
- Prefer vendor support over community forums
- Budget allows SaaS ($420-1,800/year acceptable)

## ROI Potential

**Scenario**: 30-employee restaurant, Seattle Secure Scheduling Ordinance

**Year 1**:
- **Development**: $3,000 (consultant, 30 hours setup)
- **Hosting**: $240 (cloud server + domain)
- **Total Year 1**: $3,240

**Ongoing** (Year 2+):
- **Maintenance**: $500/year (consultant retainer)
- **Hosting**: $240/year
- **Total Annual**: $740/year

**SaaS Comparison** (Deputy):
- **Year 1**: $1,620 (30 employees × $4.50/mo × 12)
- **Ongoing**: $1,620/year

**Break-Even**: Year 2
- **OR-Tools cumulative**: $3,240 + $740 = $3,980 (2 years)
- **Deputy cumulative**: $1,620 + $1,620 = $3,240 (2 years)
- **Break-even**: ~18 months

**Year 5 TCO**:
- **OR-Tools**: $3,240 + ($740 × 4) = $6,200
- **Deputy**: $1,620 × 5 = $8,100
- **Savings**: $1,900 over 5 years (23% cheaper)

**Caveat**: ROI assumes successful implementation and ongoing maintenance. Failed DIY projects common without proper planning.

## Implementation Example

**Official Tutorial**: [Google OR-Tools Employee Scheduling](https://developers.google.com/optimization/scheduling/employee_scheduling)

**Basic Seattle Restaurant Schedule** (simplified):
```python
from ortools.sat.python import cp_model

# Define employees, shifts, constraints
model = cp_model.CpModel()

# Variables: shift_assignments[employee][shift] = 1 if assigned
shift_assignments = {}
for employee in employees:
    for shift in shifts:
        shift_assignments[(employee, shift)] = model.NewBoolVar(f'{employee}_{shift}')

# Constraint: Each shift has exactly 1 server
for shift in server_shifts:
    model.Add(sum(shift_assignments[(e, shift)] for e in servers) == 1)

# Constraint: No employee works >40 hours/week
for employee in employees:
    total_hours = sum(shift.hours * shift_assignments[(employee, shift)] for shift in shifts)
    model.Add(total_hours <= 40)

# Constraint: No clopening (8+ hours between shifts)
for employee in employees:
    for shift1, shift2 in consecutive_shifts:
        # If assigned to both, ensure 8+ hour gap
        model.Add(shift2.start - shift1.end >= 8).OnlyEnforceIf([
            shift_assignments[(employee, shift1)],
            shift_assignments[(employee, shift2)]
        ])

# Objective: Minimize total labor cost
total_cost = sum(employee.hourly_rate * shift.hours * shift_assignments[(employee, shift)]
                 for employee in employees for shift in shifts)
model.Minimize(total_cost)

# Solve
solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    print("Optimal schedule found in", solver.WallTime(), "seconds")
    # Output schedule...
```

**Result**: Optimal schedule in <1 second, guaranteed to satisfy all constraints and minimize cost.

## Resources

**Official Documentation**:
- [OR-Tools Employee Scheduling Guide](https://developers.google.com/optimization/scheduling/employee_scheduling)
- [OR-Tools Python Documentation](https://developers.google.com/optimization/introduction/python)
- [Constraint Programming Basics](https://developers.google.com/optimization/cp)

**Tutorials**:
- [Towards Data Science: Restaurant Scheduling with OR-Tools](https://towardsdatascience.com/data-driven-approach-for-schedule-optimizations-60fdcba1376e/)
- [Supply Chain Data Analytics: Work Scheduling Example](https://www.supplychaindataanalytics.com/constraint-programming-for-work-scheduling-with-google-or-tools/)
- [Real Python Community Examples](https://stackoverflow.com/questions/tagged/or-tools)

## Sources

- [Google OR-Tools Official](https://developers.google.com/optimization)
- [OR-Tools Employee Scheduling](https://developers.google.com/optimization/scheduling/employee_scheduling)
- [Towards Data Science Tutorial](https://towardsdatascience.com/data-driven-approach-for-schedule-optimizations-60fdcba1376e/)
- [Constraint Programming Guide](https://www.supplychaindataanalytics.com/constraint-programming-for-work-scheduling-with-google-or-tools/)
