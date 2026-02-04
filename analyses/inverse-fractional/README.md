# Inverse Fractional: Operations & CFO Learning Laboratory

**Business**: Inverse Fractional - CFO Decision Analysis & Research-Backed Frameworks
**Owner**: Ivan Schneider
**Created**: November 2, 2025
**Purpose**: Document operational requirements + CFO skills development through hands-on implementation

---

## Overview

This folder serves dual purposes:

1. **Operational Requirements**: Document what systems/tools Inverse Fractional actually needs to operate
2. **CFO Learning Laboratory**: Use the business as a training ground to practice CFO skills and test solutions researched in `research/3.XXX/`

**Philosophy**: "Hardware Store for Software" - Build modular solutions using open source + selective managed services, document every build vs buy decision, turn implementation into content.

---

## Business Model Summary

**Core Offering**: CFO Decision Analysis ($200/50-min session)
- Vendor selection (POS, CRM, HRIS, FP&A, payments)
- Technology architecture decisions (build vs buy, integration)
- Operations optimization (capacity, resources, scheduling)

**Deliverable**: Expert-led, AI-augmented analysis → detailed report (24hr) → 14-day email support

**Revenue Streams**:
1. Decision Analysis sessions ($200 each)
2. Premium Decision Frameworks (paid content)
3. Consulting (ongoing engagements)

**Content Marketing**:
- Free articles (CFO Cookbook blog)
- Research-backed frameworks
- Real-world case studies

---

## Folder Structure

### `00-business-model/`
Financial model, unit economics, projections
- What revenue streams exist?
- What costs does the business have?
- What's the contribution margin per Decision Analysis?
- Year 1-3 financial projections

### `01-operations-requirements/`
**Core Question**: What systems does Inverse Fractional ACTUALLY need to operate?
- Scheduling/booking (Calendly? Acuity? Custom?)
- Payment processing (Stripe? → Apply 3.001 research)
- Invoicing/billing (Wave? Odoo? → Apply 3.006 research)
- CRM/pipeline (Odoo CRM? HubSpot? → Apply 3.501 research)
- Document management (contracts, reports, proposals)
- Email communication (transactional, marketing)
- Time tracking (billable vs non-billable)

### `02-financial-operations/`
**Core Question**: How to run the financials for this business?
- Accounting system (Odoo? Wave? → Apply 3.006 research)
- Cash flow forecasting (Build custom? → Apply 3.004 research + 1.127 financial simulation)
- Financial dashboards (Metabase? Superset? → Apply 3.044 data warehouse concepts)
- KPI tracking (MRR, CAC, LTV, contribution margin)
- Tax compliance (sales tax on digital services, quarterly estimates)

### `03-content-creation/`
Turn research and experience into content
- Blog/CMS (Ghost? Hugo? → Apply 3.100 research)
- Case study template (document each Decision Analysis)
- Research-to-content pipeline (spawn-solutions → blog posts)
- Email newsletter (ConvertKit? Substack?)

### `04-delivery-execution/`
How to deliver Decision Analysis service
- Decision Analysis workflow (interview → report → support)
- Interview framework (what questions to ask?)
- Report template (structure for deliverable)
- Knowledge management (capture learnings from each engagement)

### `05-learning-lab/` ⭐ **THE CFO TRAINING GROUND**
**Core Purpose**: Use Inverse Fractional as a simulated company to:
- Practice CFO skills on a real business (your own)
- Test every tool you research (hands-on experience)
- Implement "hardware store for software" approach
- Document build vs buy decisions
- Create authentic content from real implementations

**Key Experiments**:
- Odoo implementation (Community vs Enterprise? Full setup notes)
- Custom FP&A stack (cash flow forecasting, scenario modeling, driver-based planning)
- BI/analytics (Metabase/Superset for financial dashboards)
- Custom tools (Python scripts, LLM-augmented analysis)
- Open source alternatives to expensive SaaS

### `06-portfolio-showcase/`
Public documentation of your actual stack
- Technology stack (what Ivan actually uses and why)
- Build vs buy decisions (document each decision, show your work)
- Cost breakdown (transparency: here's what it costs to run this business)
- ROI analysis (was it worth building X vs buying Y?)

---

## The "Learning Lab" Concept

**Problem**: You're advising CFOs on vendor selection and technology decisions, but need to retrain yourself as a CFO and gain hands-on experience.

**Solution**: Use Inverse Fractional as a **living laboratory**:

1. **Research** solutions in `research/3.XXX-managed-services/` (e.g., 3.004 cash flow management)
2. **Experiment** with them in `05-learning-lab/` (implement Odoo + custom FP&A stack)
3. **Document** outcomes in `06-portfolio-showcase/` (here's what worked, costs, ROI)
4. **Create content** in `03-content-creation/` (blog posts, case studies from real experience)
5. **Deliver better advice** in `04-delivery-execution/` (authentic expertise from hands-on practice)

**This is NOT a simulated company** - Inverse Fractional is a REAL business, so this is **actual CFO practice**, not theoretical.

---

## "Hardware Store for Software" Approach

Instead of buying expensive SaaS for everything, build modular solutions:

**Buy (Managed Services - 3.XXX)**:
- Stripe for payment processing (infrastructure, not worth building)
- ConvertKit for email marketing (established, reliable)
- Calendly for scheduling (cheap, works)

**Build (Algorithms + Open Source - 1.XXX + 2.XXX)**:
- Odoo Community for ERP (open source, free)
- Custom FP&A tools (Python + LLMs, using 1.127 financial simulation research)
- Metabase for BI dashboards (open source alternative to Tableau)
- Custom cash flow forecasting (apply 1.127 + 3.004 research)

**Evaluate**:
- When does building make sense vs buying? (ROI threshold)
- What's the break-even point? (time, cost, maintenance)
- What are the switching costs? (lock-in analysis)

---

## Research-to-Practice Pipeline

**Example Flow**:

1. **Research Phase**: Complete 3.004 Cash Flow & Financial Planning research
   - Evaluate Pulse, Fathom, Finmark, Jirav, Causal
   - Understand features, pricing, when to buy vs build

2. **Decision Phase**: Apply Decision Analysis to your own business
   - Do I need cash flow forecasting? (Yes - $200K/year revenue target)
   - Should I buy Causal ($60/mo) or build custom? (Build - good learning + content)
   - Document decision in `01-operations-requirements/cash-flow-forecasting.md`

3. **Implementation Phase**: Build it in `05-learning-lab/`
   - Set up Odoo Community (free ERP)
   - Build Python script using 1.127 financial simulation libraries
   - Connect to Metabase for dashboards
   - Document setup in `05-learning-lab/fpa-stack.md`

4. **Portfolio Phase**: Showcase in `06-portfolio-showcase/`
   - Document: "Why I built cash flow forecasting vs buying Causal"
   - Show ROI: $720/year savings (Causal cost) vs 20 hours build time
   - Provide code: Share Python script on GitHub

5. **Content Phase**: Turn into blog post
   - Article: "When Custom Cash Flow Forecasting Beats Buying Software"
   - Real numbers, real experience, not theoretical
   - Builds credibility for Decision Analysis service

---

## Integration with Spawn Solutions Research

**Directly Apply These Research Categories**:

| Research Category | Application to Inverse Fractional |
|-------------------|-----------------------------------|
| 3.001 Payment Processing | Choose Stripe vs PayPal vs Square for Decision Analysis payments |
| 3.004 Cash Flow Management | Build custom vs buy Causal/Runway for financial forecasting |
| 3.006 Accounting Software | Choose Odoo vs Wave vs QuickBooks for bookkeeping |
| 3.020 Email Communication | Choose ConvertKit vs Mailchimp for marketing emails |
| 3.062 Web Analytics | Choose Google Analytics vs Plausible for website tracking |
| 3.100 CMS | Choose Ghost vs Hugo vs WordPress for CFO Cookbook blog |
| 3.501 CRM Platforms | Choose Odoo CRM vs HubSpot vs Pipedrive for lead tracking |
| 1.127 Financial Simulation | Build custom cash flow forecasting using Monte Carlo simulation |
| 1.139 Self-Hosted Business Apps | Evaluate Odoo Community vs managed services |

**Every research category becomes a real-world build vs buy decision for Inverse Fractional.**

---

## Success Metrics

**Operational Metrics**:
- Decision Analysis sessions per month (target: 10/month = $2K MRR)
- Customer acquisition cost (CAC)
- Customer lifetime value (LTV)
- Time per Decision Analysis (target: 3 hours total - 50 min + 2 hr report)

**Learning Lab Metrics**:
- Solutions implemented (Odoo, custom FP&A, Metabase, etc.)
- Build vs buy decisions documented
- Blog posts created from implementations
- Time saved vs SaaS cost (ROI of building)

**Content Metrics**:
- Blog traffic (CFO Cookbook)
- Email subscribers
- Case studies published
- Research papers converted to blog posts

---

## Next Steps

1. **Document operational requirements** (`01-operations-requirements/`)
   - What systems do you ACTUALLY need to run Inverse Fractional?
   - For each system, apply your own Decision Analysis framework

2. **Set up Learning Lab** (`05-learning-lab/`)
   - Install Odoo Community (free, self-hosted or Odoo.sh)
   - Set up basic financials (chart of accounts, invoices, bank reconciliation)
   - Build custom cash flow forecasting tool (Python + 1.127 research)

3. **Build portfolio** (`06-portfolio-showcase/`)
   - Document your actual stack publicly
   - Show build vs buy decisions
   - Provide cost transparency

4. **Create content** (`03-content-creation/`)
   - Turn each implementation into a blog post
   - Share learnings, code, templates
   - Build authority through authentic experience

---

## Why This Works

**Authenticity**: Can't credibly advise CFOs without being a CFO yourself
**Portfolio**: Show, don't tell - "Here's my actual stack running my $200K business"
**Content**: Every implementation = blog post + case study
**Skills**: Forces you to actually USE the tools, not just research them
**ROI**: Inverse Fractional becomes both a business AND a R&D laboratory

**The Ultimate Goal**: When a CFO asks "Should I build or buy cash flow forecasting?", you can say:
"I researched 8 platforms (3.004), implemented custom solution for my own business (05-learning-lab), and here's the ROI analysis (06-portfolio-showcase). Here's what I recommend for YOUR situation..."

That's authentic expertise, not theoretical advice.

---

**Related Research**:
- See `research/3.006-accounting-software/` for accounting system selection
- See `research/3.004-cash-flow-management/` for FP&A platform evaluation
- See `research/3.501-crm-platforms/` for CRM selection
- See `experiments/1.127-financial-simulation/` for building custom FP&A tools
- See `experiments/1.139-self-hosted-business-apps/` for open source alternatives
