# S3 Scenario 3: Sales/Customer Success Team

**Date**: 2025-11-12
**Phase**: S3 Need-Driven
**Scenario**: Sales/customer success team (8-15 people) managing sales pipeline, onboarding, and customer success activities

---

## 1. Team Profile

**Team size**: 8-15 people
- 1-2 sales managers
- 4-6 account executives (AEs)
- 2-4 customer success managers (CSMs)
- 1-2 sales development reps (SDRs)

**Industry/domain**: B2B SaaS, tech sales, professional services

**Budget constraints**: $10-15/user/month ($120-225/month for 12 people)

**Technical sophistication**: Medium (not engineers, but comfortable with CRM, SaaS tools)

**Current workflow pain points**:
- Sales activities tracked in Salesforce/HubSpot (CRM), but post-sale onboarding/CS work scattered across email, spreadsheets
- Onboarding tasks manual (no automation, CSM creates same tasks for every new customer)
- Customer requests lost in email ("Customer asked for X feature, where did that conversation go?")
- No visibility into CSM workload ("Which CSM can take on a new customer?")
- Handoff chaos: AE closes deal → CSM takes over → information lost in transition
- Renewal risk tracking manual (spreadsheets, not proactive)

---

## 2. Requirements

### Must-Have Features (Deal-Breakers)
- ✅ **Salesforce/HubSpot integration**: Sync deals, contacts, accounts from CRM to task manager
- ✅ **Templates**: Onboarding templates (same 20-30 tasks for every new customer)
- ✅ **Workload view**: See CSM capacity (who can take new customer, who's overloaded)
- ✅ **Custom fields**: Customer name, deal size, renewal date, CSM owner, health score
- ✅ **Email integration**: Create tasks from customer emails, email notifications
- ✅ **Recurring tasks**: Quarterly business reviews (QBRs), monthly check-ins, weekly renewals review

### Important Features (Strong Preference)
- **Automation**: Auto-create onboarding tasks when deal closes, auto-assign CSM based on territory/size
- **Timeline/Gantt view**: Onboarding timeline (30-60-90 day plan)
- **Task dependencies**: "Training session depends on account setup completion"
- **Dashboards**: CSM dashboard (customer health, renewal risk, overdue tasks)
- **Calendar view**: Upcoming renewals, QBRs, check-in meetings
- **Mobile app**: AEs/CSMs need mobile access (client meetings, on-the-go updates)

### Optional Features (Bonus)
- **Time tracking**: Track time spent per customer (for capacity planning, profitability)
- **Reporting**: Customer success metrics (onboarding time, renewal rate, health score trends)
- **Integrations**: Slack (notifications), Zoom (meeting links), Intercom (support tickets)

### Integration Needs (Critical)
- **Salesforce or HubSpot** (must-have, used daily): Sync deals, contacts, accounts — when deal closes, auto-create onboarding tasks
- **Email** (must-have, used daily): Create tasks from customer emails, email notifications
- **Google Calendar** (important, used daily): Sync renewal dates, QBR meetings, check-ins
- **Slack** (important, used daily): Notifications, create tasks from Slack
- **Zoom** (optional, used 2-3x/week): Auto-add meeting links to onboarding tasks

### Permission Requirements
- **Team-level permissions**: Sales team sees pipeline tasks, CS team sees onboarding/CS tasks (not fully siloed, some overlap)
- **Guest access**: Occasionally invite customers to onboarding projects (show progress: "Here's your onboarding checklist")
- **Project-level permissions**: Some customers are confidential (enterprise deals) — need private projects

### Mobile Needs
- **Mobile-important**: 30-40% of work done on mobile (AEs in client meetings, CSMs traveling to customer sites)
- **Push notifications**: Critical (renewal alerts, customer requests, overdue tasks)
- **Offline mode**: Nice-to-have (not critical, most work done with internet)

---

## 3. Platform Recommendations

### Primary Recommendation: **Monday.com**

**Pricing**: $12/user/month (12 people = $144/month, $1,728/year)

**Why Monday.com?**
1. **Best Salesforce/HubSpot integration** (S2 finding): Bidirectional sync, deep CRM integrations — when deal closes in Salesforce, auto-create onboarding tasks in Monday.com
2. **Visual boards** (S2 finding): Colorful, visual UI (good for non-technical sales/CS teams) — easier to adopt than Linear (developer-focused)
3. **Templates** (S2 finding): Onboarding templates (20-30 tasks per new customer) — save 1-2 hours per new customer
4. **Workload view** (S2 finding): See CSM capacity (who's overloaded, who can take new customer) — critical for CS managers assigning accounts
5. **Automation** (S2 finding): Auto-create tasks when deal closes, auto-assign CSM based on deal size/territory — reduce manual work
6. **Dashboards** (S2 finding): Customer health dashboards (show renewal risk, overdue tasks, health scores) — CS managers can see at-a-glance status
7. **Custom fields** (S2 finding): Customer name, deal size, renewal date, health score — track customer-specific data

**Implementation complexity**: Medium (2-3 weeks to full productivity, CRM integration setup requires 1 week)

**Time to value**: 14-21 days (sales team adopts fast, CS team needs 2-3 weeks training)

---

### Alternative 1: **Asana** (if CRM integration not critical, more balanced features)

**Pricing**: $11/user/month (12 people = $132/month, $1,584/year)

**When to choose Asana over Monday.com**:
- ✅ CRM integration not critical (if using lightweight CRM or no CRM)
- ✅ Team wants more structured workflows (Asana is more task-management focused, Monday.com is more visual/flexible)
- ✅ Cheaper ($11/user vs $12/user Monday.com — 8% cheaper)
- ✅ Need workload view at lower price point (Asana Premium $11/user includes workload, Monday.com Pro $12/user includes workload)

**Trade-offs**:
- ❌ Salesforce integration weaker than Monday.com (Asana has Salesforce integration, but not as deep — basic linking only)
- ❌ Visual boards less mature (Asana boards are good, but Monday.com is more visual, colorful)
- ❌ Dashboards less advanced (Asana has dashboards, but Monday.com's are more powerful — better for CS managers)
- ✅ Better for cross-functional teams (if sales/CS team also works with marketing, product — Asana is better cross-functional tool)

---

### Alternative 2: **Airtable** (database-centric, advanced CRM sync)

**Pricing**: $20/user/month (12 people = $240/month, $2,880/year)

**When to choose Airtable over Monday.com**:
- ✅ Team manages complex customer data (beyond tasks) — Airtable is database + task manager hybrid
- ✅ Need advanced Salesforce sync (Airtable has bidirectional sync with custom field mapping — deeper than Monday.com)
- ✅ Team comfortable with spreadsheets (Airtable looks like Excel/Google Sheets — easier for teams who love spreadsheets)
- ✅ Building custom CS tools (Airtable has best API — can build custom dashboards, integrations)

**Trade-offs**:
- ❌ Most expensive ($20/user vs $12/user Monday.com — 67% more expensive)
- ❌ Not optimized for task management (Airtable is database first, task manager second — missing features like Timeline view, Gantt)
- ❌ Weakest mobile app (S2 finding: Airtable 4.2★ iOS, 70% feature parity — Monday.com 4.6★ iOS, 80% parity)
- ✅ Best for data-heavy CS teams (e.g., tracking customer health score, usage data, NPS scores in database)

---

## 4. Architecture Pattern

### Workspace/Organization Structure (Monday.com)

**Account**: Company name (e.g., "Acme Sales")

**Workspaces** (Monday.com concept = department):
- **Sales** (pipeline, deals, pre-sale activities)
- **Customer Success** (onboarding, renewals, CS activities)
- **Shared** (handoff tasks, cross-team visibility)

**Boards** (per customer segment or per workflow):

**Sales workspace boards**:
- **Pipeline** (deals in progress, synced from Salesforce)
- **Closed Deals** (won deals, ready for CS handoff)

**Customer Success workspace boards**:
- **Onboarding** (new customers, 30-60-90 day onboarding)
- **Active Customers** (ongoing CS activities, check-ins, QBRs)
- **Renewals** (upcoming renewals, 90-60-30 days before renewal date)
- **Churn Risk** (at-risk customers, need proactive outreach)

**Board groups** (Monday.com concept = workflow stages):
- **Onboarding board groups**: Week 1 (kickoff), Week 2-4 (setup), Week 5-8 (training), Week 9-12 (adoption)
- **Renewals board groups**: 90 Days Out, 60 Days Out, 30 Days Out, Renewed, Churned

**Custom columns** (Monday.com concept = custom fields):
- **Customer**: Customer name (text)
- **Deal Size**: $10K, $50K, $100K+ (dropdown)
- **CSM Owner**: Assigned CSM (person)
- **Renewal Date**: Date (date field)
- **Health Score**: Green (healthy), Yellow (at-risk), Red (churn risk) (status)
- **Onboarding Stage**: Kickoff, Setup, Training, Adoption, Complete (status)

### Permission Boundaries

**Sales team**: Full access to Sales workspace, read-only access to Customer Success workspace (see customer status after handoff)

**CS team**: Full access to Customer Success workspace, read-only access to Sales workspace (see pipeline, upcoming deals)

**Guests** (customers): Occasional access to onboarding boards (show customer their onboarding checklist: "Here's your 30-60-90 day plan")

**Private boards**: Enterprise deals (confidential customers) are private boards (only assigned AE + CSM can see)

### Integration Architecture

**Critical integrations** (enable immediately):
1. **Salesforce/HubSpot**: Connect CRM, sync deals, contacts, accounts — when deal status changes to "Closed Won", trigger automation in Monday.com (create onboarding board for customer)
2. **Email**: Create items from emails (forward customer request to Monday.com email address)
3. **Google Calendar**: Sync renewal dates, QBR meetings, check-ins to calendar
4. **Slack**: Notifications (mention in Monday.com → Slack notification), create items from Slack

**Optional integrations**:
- **Zoom**: Auto-add Zoom meeting links to onboarding tasks (kickoff call, training sessions)
- **Intercom**: Sync support tickets to Monday.com (customer requests from support → CS tasks)

**Automation workflows**:
- **Auto-create onboarding board**: When deal closes in Salesforce (status = "Closed Won"), create onboarding board in Monday.com, auto-assign CSM based on deal size/territory
- **Auto-assign CSM**: When new onboarding board created, auto-assign CSM (rule: deal size $0-50K → CSM A, $50-100K → CSM B, $100K+ → CSM C)
- **Renewal alerts**: 90 days before renewal date, create task "Start renewal conversation", assign to CSM
- **Notify in Slack**: When customer health score changes to "Red" (churn risk), post to #customer-success Slack channel

---

## 5. Implementation Guide (30-90 day roadmap)

### Week 1-2: Setup & Configuration

**Day 1-2: Workspace setup**
- Create Monday.com account
- Create "Sales" and "Customer Success" workspaces
- Invite 2-3 early adopters (1 sales manager + 1 CSM + 1 AE)

**Day 3-5: CRM integration**
- Connect Salesforce/HubSpot to Monday.com
- Sync deals, contacts, accounts from CRM
- Test workflow: Close deal in Salesforce → Verify deal appears in Monday.com "Closed Deals" board

**Day 6-7: Create onboarding template**
- Create "Onboarding" board template (30-60-90 day plan):
  - Week 1: Kickoff call, account setup, welcome email
  - Week 2-4: Product training, data migration, integrations setup
  - Week 5-8: User training, adoption tracking, check-ins
  - Week 9-12: QBR prep, success metrics review, optimization
- Add custom columns: Customer, Deal Size, CSM Owner, Onboarding Stage, Health Score

**Day 8-10: Automation setup**
- Create automation: When deal closes in Salesforce, create onboarding board from template, auto-assign CSM
- Create automation: 90 days before renewal date, create renewal task, assign to CSM
- Test automations with dummy data

**Day 11-14: Pilot with early adopters**
- Pilot with 2-3 people (1 CSM + 1-2 AEs)
- Create onboarding boards for 2-3 real customers (use template)
- Track onboarding tasks through workflow (Week 1 → Week 12)
- Gather feedback: "What's working? What's missing?"

### Week 3-4: Pilot Expansion (6-8 people)

**Week 3: Expand pilot to half the team**
- Onboard half the team (3-4 AEs + 2-3 CSMs)
- Training session (1 hour): Monday.com UI tour, CRM sync, onboarding templates, automations
- Demo workflow: Close deal in CRM → Onboarding board auto-created → CSM assigns tasks → Customer onboards

**Week 4: Gather feedback, iterate**
- Weekly CS team meeting: Review onboarding boards, identify bottlenecks
- Iterate on template: Add/remove tasks based on what's working
- **Success metric**: 80%+ of pilot team using Monday.com daily

### Week 5-8: Rollout (Full Team)

**Week 5: Full team onboarding**
- Onboard full team (8-12 people: all AEs, CSMs, SDRs, sales managers)
- Training session (1.5 hours): Monday.com UI, CRM sync, onboarding templates, renewals board, dashboards

**Week 6-7: Migrate existing customers**
- Create onboarding/active customer boards for all existing customers (10-50 customers)
- Backfill data: Renewal dates, health scores, recent activities
- Update CRM: Link Monday.com boards to Salesforce/HubSpot records

**Week 8: Establish workflow**
- Weekly CS meeting: Review renewals board (90-60-30 days out), churn risk board
- Daily check-ins: CSMs update health scores, onboarding status
- Handoff process: AE closes deal → CSM takes over → information in Monday.com (not email)
- **Success metric**: 90%+ team adoption, 95%+ customer data in Monday.com

### Month 3: Optimization

**Optimize workflows**:
- Review onboarding time: Avg time to onboard customer (goal: <60 days)
- Identify bottlenecks: Are customers getting stuck at training stage? (Add resources, more training sessions)
- Refine health score: Update health score criteria (usage data, NPS, support tickets)

**Add dashboards**:
- **CSM dashboard**: Show CSM workload (# active customers, # onboarding, # renewals upcoming)
- **Renewal dashboard**: Show upcoming renewals (90-60-30 days out), renewal rate, churn rate
- **Onboarding dashboard**: Show onboarding in progress, avg onboarding time, completion rate

**Success metrics** (Month 3):
- ✅ 95%+ team adoption (daily active users)
- ✅ 50%+ reduction in handoff errors (AE → CSM transition smooth, no information lost)
- ✅ Proactive renewal outreach (90%+ of renewals have outreach task 90 days before renewal date)
- ✅ Improved renewal rate (5-10% improvement due to proactive outreach)

---

## 6. TCO Analysis (3-year total cost, 12 people)

| Cost Component | Amount | Notes |
|----------------|--------|-------|
| **Subscription (3 years)** | $5,184 | $12/user/month × 12 people × 36 months |
| **Training** | $4,800 | 1.5 hours training + 2 weeks learning curve × 12 people × $80/hour |
| **Migration** | $3,000 | 2 weeks CRM integration + data migration × 1 sales ops person × $80/hour |
| **Support** | $0 | Monday.com support included (email, chat, docs) |
| **Productivity loss** | $10,000 | 2-week learning curve × 12 people × $80/hour |
| **Total 3-Year TCO** | **$22,984** | |

**Cost per person per month**: ~$53/month ($22,984 / 12 people / 36 months)

**Comparison to alternatives**:
- **Asana**: $21,195 (3-year, 12 people) — 8% cheaper than Monday.com, but weaker CRM integration
- **Airtable**: $34,560 (3-year, 12 people) — 50% more expensive than Monday.com, but deeper CRM sync + database capabilities
- **Spreadsheets (free)**: $0 subscription, but high hidden cost (manual onboarding, no automation, renewal risk)

**ROI**: Monday.com pays for itself if it **improves renewal rate by 5%**. Example: If company has $1M ARR, 5% renewal rate improvement = $50K additional revenue/year → $150K over 3 years (vs $22,984 TCO = **6.5x ROI**).

---

## 7. Success Metrics

### Week 4 Metrics (Pilot Success)
- ✅ **80%+ daily active users** (pilot team using Monday.com daily)
- ✅ **CRM sync working** (deals auto-sync from Salesforce to Monday.com)
- ✅ **2-3 onboarding boards created** (using template)
- ✅ **Positive feedback** (pilot team reports "Monday.com better than spreadsheets")

### Month 3 Metrics (Rollout Success)
- ✅ **90%+ daily active users** (all sales/CS team using Monday.com daily)
- ✅ **95%+ customer data in Monday.com** (all customers have onboarding/CS boards)
- ✅ **50%+ reduction in handoff errors** (AE → CSM transition smooth)
- ✅ **Proactive renewal outreach** (90%+ renewals have outreach 90 days before)

### Month 6 Metrics (Optimization Success)
- ✅ **95%+ team adoption** (Monday.com is default tool)
- ✅ **5-10% renewal rate improvement** (proactive outreach reduces churn)
- ✅ **Faster onboarding** (avg onboarding time reduces from 90 days to 60 days)
- ✅ **Better CSM capacity planning** (workload view eliminates overload, balanced assignments)

---

## 8. Common Pitfalls

### Pitfall 1: **CRM sync issues (duplicates, missing data, wrong field mapping)**
**Problem**: CRM integration creates duplicate records, or wrong fields sync (deal name → customer name) → manual cleanup required
**Solution**:
- Test CRM sync with dummy data first (before production)
- Map fields carefully (Salesforce Account Name → Monday.com Customer column)
- Deduplicate: Set unique identifier (Salesforce Account ID) to prevent duplicates

### Pitfall 2: **Onboarding template too rigid (every customer is different)**
**Problem**: Template has 30 tasks, but some customers don't need all tasks → CSM manually deletes 10 tasks per customer → wasted time
**Solution**:
- Create multiple templates (Small Customer Onboarding, Enterprise Onboarding) based on customer segment
- Make template flexible (mark optional tasks with "[Optional]" label — CSM can delete if not needed)
- Review template quarterly (remove tasks that are rarely used)

### Pitfall 3: **Health score manual (CSMs don't update regularly → stale data)**
**Problem**: Health score is manual dropdown → CSMs forget to update → dashboard shows outdated data → CS manager can't trust data
**Solution**:
- Automate health score (integrate with product usage data, support tickets, NPS scores — auto-calculate health score)
- Weekly reminder: Slack bot reminds CSMs "Update customer health scores" every Friday
- Make it easy: Health score should be 1 click (dropdown: Green/Yellow/Red), not 10 fields to update

### Pitfall 4: **Renewal alerts too early or too late (90 days too early for small customers, 30 days too late for enterprise)**
**Problem**: Small customers don't need 90-day renewal outreach (too early, customer forgets by renewal date) — Enterprise customers need 120+ days (procurement, contracts)
**Solution**:
- Segment renewal alerts by deal size:
  - Small ($0-25K): 30 days before renewal
  - Medium ($25-100K): 60 days before renewal
  - Enterprise ($100K+): 120 days before renewal
- Create separate automations per segment

### Pitfall 5: **Monday.com becomes CRM replacement (scope creep)**
**Problem**: Sales team tries to use Monday.com as CRM (track all deals, contacts, pipeline) → duplicates Salesforce → confusion about single source of truth
**Solution**:
- Clarify purpose: **Salesforce/HubSpot is CRM** (source of truth for deals, contacts), **Monday.com is task manager** (onboarding, CS activities)
- Use Monday.com for post-sale activities only (onboarding, renewals, CS tasks) — NOT for pipeline management
- Sync CRM → Monday.com (one-way or bidirectional), but Salesforce is master

---

## 9. Additional Resources

**Monday.com resources**:
- Monday.com for Sales guide: https://monday.com/solutions/sales-crm
- Monday.com Salesforce integration: https://monday.com/integrations/salesforce
- Monday.com automations guide: https://monday.com/automations

**Community**:
- Monday.com Community Forum: https://community.monday.com/
- Monday.com for Sales/CS best practices

---

**Last Updated**: 2025-11-12
**Phase**: S3 Need-Driven
**Scenario**: 3 of 5 (Sales/Customer Success Team)
