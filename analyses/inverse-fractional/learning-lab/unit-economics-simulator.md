# Learning Lab Experiment 2: Unit Economics Simulator

**Experiment**: Build interactive unit economics simulator with scenario analysis
**Research Source**: 1.120 Discrete Event Simulation, 1.122 Monte Carlo Simulation, 3.007 FP&A Platforms
**Timeline**: Month 3-4 (after Odoo implementation)
**Status**: 🚧 Planned

---

## Experiment Goals

### Primary Goal
Build a Python-based unit economics simulator to model Decision Analysis service under different scenarios, demonstrating build vs buy for FP&A tools.

**Business Value**:
- Answer questions like: "What if I only get 5 sessions/month?" or "What if I raise price to $250?"
- Model cash flow implications (not just economic profit)
- Test pricing strategies, cost structures, growth scenarios
- Create reusable tool for client Decision Analysis engagements

### Learning Objectives
- [ ] Practice Monte Carlo simulation (1.122) for uncertainty modeling
- [ ] Build driver-based financial model (sessions → revenue → costs → profit)
- [ ] Understand difference between economic profit and cash profit (CRITICAL for solo operators)
- [ ] Compare build vs buy: Custom Python vs FP&A SaaS ($50-200/month)
- [ ] Create content from implementation experience

### Business Objectives
- [ ] Get real-time answers to "what if" questions for Inverse Fractional
- [ ] Build portfolio showcase: "Here's my actual financial model"
- [ ] Generate 2-3 blog posts from implementation
- [ ] Create template for client Decision Analysis engagements
- [ ] Save $600-2,400/year vs FP&A platforms (Causal, Jirav, Mosaic)

---

## Build vs Buy Decision (Applied to Self)

### Decision Context

**Current State**: Unit economics tracked in static markdown document (unit-economics.md)
**Need**: Interactive scenario planning, sensitivity analysis, Monte Carlo uncertainty modeling
**Budget**: <$100/month preferred
**Technical Resources**: Yes (can code Python, Jupyter notebooks)
**Timeline**: 15-25 hours over 1-2 months

### Options Evaluated

| Option | Software Cost | Setup Time | Total (Year 1) | Pros | Cons |
|--------|---------------|------------|----------------|------|------|
| **Spreadsheet (Google Sheets)** | $0 | 2-4 hrs | **$0** | Fast, familiar, shareable | Manual, no Monte Carlo, brittle |
| **FP&A SaaS (Causal)** | $600/yr | 5-10 hrs | **$600** | Professional, hosted, charts | Overkill for solo, vendor lock-in |
| **FP&A SaaS (Jirav)** | $1,200/yr | 10-15 hrs | **$1,200** | Full-featured, integrations | Expensive, complex |
| **Custom Python + Jupyter** | $0 | 15-25 hrs | **$0** | Full control, learning value, portfolio | Time investment, maintenance |

### Decision: Custom Python + Jupyter Notebook (Build)

**Why Build Instead of Buy**:
1. **Learning value**: Practice Monte Carlo simulation (1.122), driver-based modeling
2. **Portfolio showcase**: "Here's how I model my own business" = authentic credibility
3. **Content generation**: 3 blog posts + reusable template = worth $5,000+ in content value
4. **Cost savings**: $600-1,200/year vs FP&A SaaS
5. **Reusable for clients**: Template for Decision Analysis engagements
6. **Research validation**: Test findings from 1.120-129 Simulation research

**When This Breaks Down**:
- If you need board-ready presentations (SaaS has better charts)
- If you need real-time integrations with accounting systems
- If setup time exceeds 30 hours (vs $600/year = $50/month)

**ROI Calculation**:
- **Investment**: 20 hours @ $100/hr = $2,000 opportunity cost
- **Return**:
  - Cost savings: $600/year × 5 years = $3,000
  - Content value: 3 blog posts → 10 Decision Analysis bookings = $2,000
  - Portfolio value: Win 1 consulting client = $10,000+
  - Reusable template: Use for client engagements = $5,000+
  - **Total**: $20,000+ over 2-3 years
- **ROI**: 10x ($20K ÷ $2K)

---

## Implementation Plan

### Phase 1: Core Model (Week 1-2, 10-15 hours)

**Goal**: Build baseline unit economics model with scenario analysis.

**Features**:
1. **Input variables**:
   - Sessions per month (range: 0-50)
   - Price per session (default: $200, test: $150-$300)
   - Square fee rate (2.9% + $0.30)
   - Hours per session (default: 2.5, test: 2-4)
   - Fixed costs per month (default: $225)
   - Fully loaded labor rate (default: $100/hr, test: $75-$150)

2. **Outputs**:
   - Gross revenue
   - Net revenue (after Square fees)
   - Variable costs (labor @ $100/hr)
   - Fixed costs
   - **Economic profit** (treats labor as cost)
   - **Cash profit** (actual cash take-home)
   - Effective hourly rate (economic)
   - Cash hourly rate
   - Break-even sessions

3. **Scenario analysis**:
   - Table: 5, 10, 20, 30, 40, 50 sessions/month
   - Charts: Revenue, profit, hourly rates by volume

**Tech Stack**:
- Python 3.11+
- Pandas (data manipulation)
- NumPy (calculations)
- Matplotlib/Plotly (visualizations)
- Jupyter Notebook (interactive exploration)

**Deliverable**: Jupyter notebook with interactive scenario analysis

**Time Tracking**: Target 10-15 hours

---

### Phase 2: Sensitivity Analysis (Week 3, 5-8 hours)

**Goal**: Understand which variables matter most to profitability.

**Features**:
1. **Tornado chart**: Show impact of ±20% change in each variable
2. **One-way sensitivity**: How profit changes with each variable
3. **Two-way sensitivity**: Price × Volume matrix

**Variables to test**:
- Sessions per month (most important!)
- Price per session ($150, $175, $200, $225, $250, $300)
- Hours per session (2.0, 2.5, 3.0, 3.5)
- Fixed costs ($150, $200, $225, $250, $300)
- Labor rate ($75, $100, $125, $150)

**Key Questions to Answer**:
- What's the minimum viable price to hit $50K profit? (at 43 sessions/month)
- How much does improving delivery time (2.5 hrs → 2 hrs) improve profit?
- What's the impact of reducing fixed costs by $50/month (Render migration)?

**Deliverable**: Sensitivity analysis notebook section + tornado chart

**Time Tracking**: Target 5-8 hours

---

### Phase 3: Monte Carlo Simulation (Week 4, 8-12 hours)

**Goal**: Model uncertainty in sessions/month and understand downside risk.

**Why Monte Carlo**:
- Sessions per month is UNCERTAIN (could be 3, could be 15)
- Fixed costs are CERTAIN ($225/month)
- What's the probability of hitting $50K profit? $100K?

**Approach**:
1. **Define distributions**:
   - Sessions/month: Triangular distribution (min=3, mode=10, max=25) for Year 1
   - Price: Fixed at $200 (Year 1), or Normal($200, $20) if testing price variability
   - Hours per session: Normal(2.5, 0.3) - slightly variable
   - Fixed costs: Fixed at $225

2. **Run simulation**:
   - 10,000 iterations
   - Each iteration samples from distributions
   - Calculate economic profit, cash profit for each scenario

3. **Analyze results**:
   - P50 (median) profit
   - P10 (downside case) profit
   - P90 (upside case) profit
   - Probability of break-even (profit > 0)
   - Probability of hitting $50K profit target
   - Histogram of outcomes

**Research Connection**:
- Apply 1.122 Monte Carlo Simulation research
- Test libraries: `scipy.stats`, `numpy.random`, `uncertainties`

**Key Questions to Answer**:
- What's the expected cash profit in Year 1? (P50)
- What's the downside risk? (P10)
- What's the probability I hit $50K economic profit?
- What's the probability I hit $100K cash profit?

**Deliverable**: Monte Carlo simulation notebook section + probability distributions

**Time Tracking**: Target 8-12 hours

---

### Phase 4: Multi-Year Projections (Week 5, 5-8 hours)

**Goal**: Model Years 1-3 with growth assumptions and revenue mix evolution.

**Features**:
1. **Year 1**: Decision Analysis only (base case)
2. **Year 2**: Decision Analysis + Consulting retainers
3. **Year 3**: Decision Analysis + Consulting + Premium frameworks + Courses

**Revenue Mix Evolution**:

| Revenue Stream | Year 1 | Year 2 | Year 3 |
|----------------|--------|--------|--------|
| Decision Analysis ($200/session) | 10/mo | 20/mo | 30/mo |
| Consulting retainers ($2-5K/mo) | 0 | 2 clients | 4 clients |
| Premium frameworks ($99) | 0 | 10/year | 30/year |
| Courses ($499) | 0 | 0 | 20/year |

**Cost Evolution**:
- Year 1: $225/mo fixed (current)
- Year 2: $345/mo (add Odoo $120/year = $10/mo)
- Year 3: $400/mo (add course hosting, email marketing)

**Key Questions to Answer**:
- What's realistic Year 2 and Year 3 revenue?
- When do I need to add leverage products (consulting, courses)?
- What's the path to $100K profit? $200K?

**Deliverable**: Multi-year projection notebook section

**Time Tracking**: Target 5-8 hours

---

### Phase 5: Pricing Strategy Analysis (Week 6, 5-8 hours)

**Goal**: Test alternative pricing models and find optimal price point.

**Pricing Scenarios**:

| Scenario | Price | Expected Impact on Demand | Break-Even Sessions |
|----------|-------|---------------------------|---------------------|
| Current | $200 | Baseline (10/mo target) | 3 sessions |
| Budget | $150 | +30% demand → 13/mo | 4 sessions |
| Premium | $250 | -20% demand → 8/mo | 2 sessions |
| Prestige | $300 | -40% demand → 6/mo | 2 sessions |
| Value | $99 | +100% demand → 20/mo | 5 sessions |

**Analysis**:
- Price elasticity modeling (how demand changes with price)
- Profit maximization (optimal price × volume)
- Cash profit comparison across scenarios
- Consider positioning implications (premium vs volume)

**Key Questions to Answer**:
- Is $200 the right price, or should I test $250?
- What if I offered a $99 "Quick Consult" (30 min + report)?
- At what price does profit start declining (too expensive, lose volume)?

**Deliverable**: Pricing analysis notebook section + recommendation

**Time Tracking**: Target 5-8 hours

---

### Phase 6: Documentation & Content Creation (Week 7-8, 10-15 hours)

**Implementation Documentation** (for 06-portfolio-showcase/):
- [ ] Write: "Unit Economics Simulator: Build vs Buy Analysis"
- [ ] Include: Code walkthrough, Monte Carlo explanation, results
- [ ] Document: Challenges, libraries used, lessons learned
- [ ] Provide: GitHub repo with open source notebook

**Blog Post #1: Build vs Buy**
- [ ] Title: "I Built My Own FP&A Tool Instead of Paying $1,200/year (Here's Why)"
- [ ] Content: Decision framework, ROI analysis, total cost comparison
- [ ] Audience: CFOs evaluating FP&A platforms
- [ ] SEO: "build vs buy fpa", "custom financial modeling", "causal alternatives"
- [ ] CTA: "Need help with YOUR build vs buy decision? Book Decision Analysis"

**Blog Post #2: Technical Tutorial**
- [ ] Title: "Unit Economics Modeling in Python: CFO's Guide to Monte Carlo Simulation"
- [ ] Content: Step-by-step Jupyter notebook walkthrough with code
- [ ] Audience: Technical CFOs, finance engineers
- [ ] SEO: "monte carlo python finance", "unit economics modeling", "financial simulation"
- [ ] CTA: "Want custom financial models? Framework Engagement"

**Blog Post #3: Insights from Model**
- [ ] Title: "Why Economic Profit ≠ Cash Profit: Lessons from Modeling My Business"
- [ ] Content: Explain economic vs cash profit distinction, show simulations
- [ ] Audience: Founders, CFOs, solo operators
- [ ] SEO: "economic profit vs cash profit", "unit economics for founders"
- [ ] CTA: "Get clarity on YOUR unit economics - Book Decision Analysis"

**Open Source Release**:
- [ ] Clean up notebook for public release
- [ ] Add README with setup instructions
- [ ] Create GitHub repo: `inverse-fractional/unit-economics-simulator`
- [ ] Share on LinkedIn, CFO communities
- [ ] License: MIT (open source)

**Deliverable**: 3 blog posts + portfolio documentation + GitHub repo

**Time Tracking**: Target 10-15 hours

---

## Success Metrics

### Implementation Metrics
- **Build time**: Target 40 hours total (vs 1 hour for spreadsheet, 10 hours for SaaS)
- **Cost**: $0 software (vs $600-1,200/year for FP&A SaaS)
- **Functionality**: Scenario analysis, sensitivity, Monte Carlo, multi-year projections

### Learning Metrics
- **CFO skills gained**: Monte Carlo simulation, driver-based modeling, scenario planning
- **Research validated**: 1.122 Monte Carlo, 1.120 Simulation, 3.007 FP&A
- **Content generated**: 3 blog posts + portfolio showcase + GitHub repo

### Business Impact Metrics
- **Cost savings**: $600/year vs Causal (5-year = $3,000)
- **Revenue from content**: 3-5 Decision Analysis bookings from blog posts ($600-1,000)
- **Portfolio value**: Showcase helps win 1 consulting client ($10K+)
- **Reusable template**: Use for 5+ client Decision Analysis engagements ($1,000+ value)

### ROI Calculation

**Investment**:
- Time: 40 hours @ $100/hr opportunity cost = $4,000
- Cash: $0 (all open source tools)
- **Total**: $4,000

**Return** (over 2 years):
- Cost savings: $600/year × 2 = $1,200
- Content → bookings: 5 sessions @ $200 = $1,000
- Portfolio → consulting: 1 client @ $10K = $10,000
- Reusable template: 5 client engagements @ $200 = $1,000
- **Total**: $13,200

**ROI**: 230% ($13,200 ÷ $4,000)
**Payback period**: 6-9 months

---

## Technical Details

### Python Libraries (All Open Source)

**Core**:
- `pandas`: Data manipulation and tables
- `numpy`: Numerical calculations
- `matplotlib` / `plotly`: Visualizations (charts, graphs)
- `jupyter`: Interactive notebook environment

**Simulation**:
- `scipy.stats`: Probability distributions (triangular, normal)
- `numpy.random`: Random number generation for Monte Carlo
- `uncertainties`: Error propagation (optional)

**Advanced** (if needed):
- `seaborn`: Statistical visualizations (tornado charts, heatmaps)
- `ipywidgets`: Interactive controls (sliders for scenarios)
- `voila`: Turn notebook into standalone app

### File Structure

```
/applications/inverse-fractional/05-learning-lab/
├── unit-economics-simulator.md (this file)
├── notebooks/
│   ├── 01-core-model.ipynb
│   ├── 02-sensitivity-analysis.ipynb
│   ├── 03-monte-carlo-simulation.ipynb
│   ├── 04-multi-year-projections.ipynb
│   ├── 05-pricing-strategy.ipynb
│   └── utils.py (helper functions)
├── data/
│   ├── unit-economics-inputs.csv
│   └── simulation-results.csv
└── outputs/
    ├── charts/ (PNG exports for blog posts)
    └── reports/ (Markdown exports)
```

---

## Risks & Mitigations

### Risk 1: Implementation Takes Longer Than Expected (40+ hours)

**Problem**: Monte Carlo simulation is complex, could take 60-80 hours

**Mitigation**:
- Start with Phase 1 only (core model = 15 hours)
- If Phase 3 (Monte Carlo) exceeds 20 hours, defer to Year 2
- Use simpler approach: sensitivity analysis (Phase 2) instead of Monte Carlo
- **Decision threshold**: If total time >60 hours, just use Google Sheets ($0)

---

### Risk 2: Python Skills Are Rusty

**Problem**: Haven't coded Python intensively in a while

**Mitigation**:
- Use Augment AI ($50/mo, already paying for) to accelerate coding
- Use Claude Max ($110/mo, already paying for) for code review and debugging
- Start with simple spreadsheet model, then port to Python (progressive complexity)
- **Fallback**: If coding is too painful, use Google Sheets + manual Monte Carlo (=RANDBETWEEN())

---

### Risk 3: Results Don't Provide New Insights

**Problem**: Model just confirms what we already know from unit-economics.md

**Mitigation**:
- Focus on Phase 3 (Monte Carlo) - this WILL provide new insights (probability distributions)
- Use model to test pricing strategies (Phase 5) - explores unknowns
- Share model with clients for Decision Analysis engagements (monetize immediately)
- **Still valuable**: Portfolio showcase + content creation justify investment

---

### Risk 4: Maintenance Burden (Keeping Model Updated)

**Problem**: Model becomes outdated as costs change, needs ongoing maintenance

**Mitigation**:
- Design model with CSV input file (easy to update costs without coding)
- Document assumptions clearly (future you will thank present you)
- Build once, update quarterly (not monthly)
- **Threshold**: If maintenance >2 hours/quarter, switch to FP&A SaaS

---

## Next Steps (Immediate)

### This Week
1. [ ] Review 1.120-129 Simulation research (understand Monte Carlo, discrete event simulation)
2. [ ] Review 3.007 FP&A Platforms research (understand build-vs-buy landscape)
3. [ ] Set up Jupyter notebook environment (test `pandas`, `numpy`, `matplotlib`)
4. [ ] Create Phase 1 core model (baseline scenario analysis)

### Next Week
1. [ ] Complete Phase 1 (core model with 5, 10, 20, 43 session scenarios)
2. [ ] Add charts (revenue, profit, hourly rates by volume)
3. [ ] Validate against unit-economics.md (ensure calculations match)
4. [ ] Share initial results (screenshot charts for newsletter?)

### Month 2
1. [ ] Complete Phase 2 (sensitivity analysis)
2. [ ] Complete Phase 3 (Monte Carlo simulation)
3. [ ] Document findings
4. [ ] Write blog post #1 (build vs buy)

### Month 3
1. [ ] Complete Phase 4 (multi-year projections)
2. [ ] Complete Phase 5 (pricing strategy)
3. [ ] Write blog posts #2 and #3
4. [ ] Open source GitHub release

---

## Key Insights

### Why This Matters (Economic vs Cash Profit Discovery)

**The Aha Moment**: Your question about "43 × $200 = $8,600 cash implications" revealed a critical distinction that most unit economics models ignore:

**Economic profit** (treats labor as cost @ $100/hr):
- 43 sessions/month = $50,052/year economic profit
- This is useful for **decision-making** (Is this worth my time?)

**Cash profit** (actual cash take-home):
- 43 sessions/month = $97,344/year CASH
- This is what you **actually earn** as a solo operator

**The $47K difference** is your imputed labor cost that stays with you as cash!

**Why this should be in the simulator**:
- EVERY solo founder/operator faces this confusion
- Being able to toggle "Show economic profit" vs "Show cash profit" is hugely valuable
- This is a DIFFERENTIATOR vs FP&A SaaS (they don't model this!)

### Connection to Research

This experiment directly applies:
- **1.120 Discrete Event Simulation**: Model sessions arriving over time
- **1.122 Monte Carlo Simulation**: Model uncertainty in session volume
- **3.007 FP&A Platforms**: Build vs buy decision for financial modeling tools

### Reusable for Clients

Once built, this simulator template can be adapted for:
- SaaS businesses (MRR × churn → revenue, CAC → customer acquisition)
- Professional services (hours × rate → revenue, capacity constraints)
- Product businesses (units × price → revenue, COGS × units → costs)
- Any unit economics scenario (freelancers, agencies, consultants)

**Value**: Offer customized unit economics simulator as part of Framework Engagement ($5K-12K) = high-value deliverable

---

## Related Resources

**Research**:
- `/research/1.120-simulation-libraries/` - Discrete event simulation
- `/research/1.122-monte-carlo/` - Monte Carlo methods
- `/research/3.007-fpa-platforms/` - FP&A build vs buy analysis

**Applications**:
- `../00-business-model/unit-economics.md` - Baseline calculations to model
- `../01-operations-requirements/OPERATIONAL_STACK_DECISION.md` - Context for build vs buy

**Portfolio**:
- `../06-portfolio-showcase/` - Where final case study will live

**Content**:
- `../03-content-creation/` - Blog post drafts from this implementation

---

## Time Tracking Log

| Date | Phase | Hours | Tasks Completed | Notes |
|------|-------|-------|-----------------|-------|
| TBD | Planning | 0 | Created this document | Starting experiment |
| | | | | |

**Total Hours**: 0 / 40 target

---

**Status**: 🚧 Ready to start (after Odoo implementation)
**Priority**: High (immediately useful for business + great portfolio piece)
**Next Action**: Review 1.120-129 and 3.007 research, set up Jupyter environment
**Timeline**: Start Month 3-4 (Year 1)
