# S3 Scenario 5: Small Consulting Firm

**Date**: 2025-11-12
**Phase**: S3 Need-Driven
**Scenario**: Small consulting firm (5-12 consultants) managing client projects, deliverables, time tracking, and billing

---

## 1. Team Profile

**Team size**: 5-12 consultants
- 1-2 partners/directors (owners)
- 3-8 consultants (senior, mid-level, junior)
- 1-2 operations staff (admin, finance)

**Industry/domain**: Management consulting, strategy consulting, technology consulting, professional services

**Budget constraints**: $5-12/user/month ($50-150/month for 10 consultants)

**Technical sophistication**: Medium (not engineers, but comfortable with SaaS tools, Excel, PowerPoint)

**Current workflow pain points**:
- **Client projects scattered**: Work tracked in spreadsheets, email, shared drives — no single source of truth
- **Time tracking manual**: Consultants log time in Excel at end of week → inaccurate, time-consuming
- **Deliverables tracking**: "What deliverables are due this week?" requires checking email, Slack, spreadsheets
- **Capacity planning guesswork**: "Who can take on a new client?" requires asking everyone → no visibility
- **Client communication**: Client feedback lost in email chains → hard to find decisions
- **Budget/profitability blind spots**: No visibility into time spent vs budget → projects go over budget

---

## 2. Requirements

### Must-Have Features (Deal-Breakers)
- ✅ **Time tracking (native or integration)**: Track time per client, per project (for billing, capacity planning)
- ✅ **Client-level organization**: One project per client, all deliverables/tasks under client
- ✅ **Templates**: Project templates (engagements, workshops, reports) — consultants deliver similar projects repeatedly
- ✅ **Workload view**: See consultant capacity (who's overloaded, who can take new client)
- ✅ **Task dependencies**: "Report deliverable depends on data analysis completion"
- ✅ **Email integration**: Create tasks from client emails, email notifications

### Important Features (Strong Preference)
- **Timeline/Gantt view**: Project timeline (engagement timeline, deliverables schedule)
- **Recurring tasks**: Weekly status reports, monthly invoices, quarterly reviews
- **Custom fields**: Client name, project budget, time budget, consultant rate, deliverable type
- **Calendar view**: Upcoming deliverables, client meetings, deadlines
- **Guest access**: Invite clients to specific projects (show progress, get feedback)
- **Mobile app**: Consultants need mobile access (client sites, travel)

### Optional Features (Bonus)
- **Reports/dashboards**: Project profitability (time spent vs budget), utilization rate (billable hours %)
- **File attachments**: Attach deliverables (PowerPoint, Excel, reports)
- **Automation**: Auto-assign consultants, notify when deliverable is due
- **Integrations**: Slack (notifications), Google Drive (attach files), QuickBooks (export time for invoicing)

### Integration Needs (Critical)
- **Time tracking** (must-have, used daily): Native time tracking (ClickUp) OR integration with Harvest/Toggl (Asana, Linear)
- **Email** (must-have, used daily): Create tasks from emails, email notifications
- **Google Drive** (important, used daily): Attach deliverables, client documents
- **Calendar** (important, used daily): Sync deliverable due dates, client meetings
- **QuickBooks/Xero** (optional, used monthly): Export time tracking data for invoicing

### Permission Requirements
- **Simple permissions**: Flat team structure (all consultants have equal access)
- **Client guest access**: Occasionally invite clients to project (show deliverables progress)
- **Private projects**: Some projects confidential (M&A, strategy) — need private projects

### Mobile Needs
- **Mobile-important**: 30-40% of work done on mobile (consultants at client sites, travel)
- **Push notifications**: Important (deliverable due dates, client comments)
- **Offline mode**: Nice-to-have (consultants travel, but most work requires internet for files)

---

## 3. Platform Recommendations

### Primary Recommendation: **Asana**

**Pricing**: $11/user/month (10 consultants = $110/month, $1,320/year)

**Why Asana?**
1. **Workload view** (S2 finding): See consultant capacity (billable hours, utilization) — critical for partners assigning projects
2. **Templates** (S2 finding): Engagement templates (workshops, reports, strategy projects) — save 1-2 hours per new engagement
3. **Timeline view** (S2 finding): Visual Gantt chart for engagement timelines, deliverables schedule
4. **Time tracking integrations** (S2 finding): Integrates with Harvest, Toggl, Everhour — consultants can track time per task (Asana doesn't have native time tracking, but integrations are excellent)
5. **Client guest access** (S2 finding): Unlimited guests (free), project-level access — invite clients to show deliverables progress
6. **Cross-functional workflows** (S2 finding): Works for consulting (mix of strategy, analysis, deliverables) — not specialized for one function
7. **Excellent mobile app** (S2 finding): 4.7★ iOS, 90% feature parity — consultants can update on client sites

**Implementation complexity**: Medium (2-3 weeks to full productivity, requires workflow design + time tracking integration)

**Time to value**: 14-21 days (consultants adopt in 2 weeks, time tracking integration takes 1 week)

---

### Alternative 1: **ClickUp** (budget-conscious, want native time tracking)

**Pricing**: $7/user/month (10 consultants = $70/month, $840/year)

**When to choose ClickUp over Asana**:
- ✅ Budget priority ($7/user vs $11/user Asana — 36% cheaper)
- ✅ Want native time tracking (ClickUp has built-in time tracking — no integration needed)
- ✅ Want more customization (ClickUp most flexible, Asana more opinionated)
- ✅ Team is tech-savvy (ClickUp has more features, but steeper learning curve)

**Trade-offs**:
- ❌ More complex UI (ClickUp 7 roles, deep hierarchy — harder for non-technical consultants)
- ❌ Higher training cost (S2 finding: ClickUp $8,000 training vs Asana $4,000 for 10 users over 3 years)
- ❌ Client guest access more limited (ClickUp free tier: 2 guests, Asana free tier: unlimited guests)
- ❌ Mobile app slower (ClickUp 4.7★ iOS vs Asana 4.7★, but ClickUp users report slower performance)

---

### Alternative 2: **Trello** (simplest, cheapest, but limited features)

**Pricing**: $5/user/month (10 consultants = $50/month, $600/year) or **Free tier** (10 users)

**When to choose Trello over Asana**:
- ✅ Budget priority ($5/user vs $11/user Asana — 55% cheaper, or FREE for 10 users)
- ✅ Team wants simplicity (Trello 2 roles, board-only view — simplest among all platforms)
- ✅ Projects are simple (no dependencies, no Gantt, no advanced features needed)
- ✅ Small firm (5-8 consultants) — Trello scales poorly beyond 10 people

**Trade-offs**:
- ❌ No native time tracking (requires Power-Ups like Harvest, Toggl)
- ❌ No workload view (can't see consultant capacity — partners must track manually)
- ❌ No timeline/Gantt view (limited calendar Power-Up, no visual engagement timeline)
- ❌ Limited features (Trello 39/64 features vs Asana 54/64 — missing dependencies, timeline, workload)

---

## 4. Architecture Pattern

### Workspace/Organization Structure (Asana)

**Organization**: Consulting firm name (e.g., "Acme Consulting")

**Teams** (Asana concept = department):
- **Client Projects** (main team, all consultants + clients as guests)
- **Internal** (internal projects, firm operations, not client-facing)
- **Leadership** (partners/directors only — private team for sensitive projects)

**Projects** (per client):
- **Client: Acme Corp - Strategy Project** (all work for Acme Corp engagement)
  - Deliverables: Market analysis, Competitive landscape, Strategy recommendations
- **Client: Beta Inc - Workshop** (workshop engagement)
  - Deliverables: Workshop prep, Facilitation, Post-workshop report
- **Internal: Marketing** (firm's own marketing, website, content)
- **Internal: Operations** (hiring, onboarding, finance, admin)

**Sections** (within projects, Asana concept = workflow stages):
- **Backlog** (ideas, not yet scheduled)
- **To Do** (scheduled, not started)
- **In Progress** (consultant is working on it)
- **In Review** (partner reviews before sending to client)
- **Client Review** (waiting for client feedback)
- **Complete** (deliverable sent to client, engagement complete)

**Custom fields**:
- **Client**: Acme Corp, Beta Inc, Internal (dropdown)
- **Project Budget**: $50K, $100K, $200K (number)
- **Time Budget**: 100 hours, 200 hours, 500 hours (number)
- **Deliverable Type**: Report, Presentation, Workshop, Analysis (dropdown)
- **Consultant**: Assigned consultant (person)
- **Hourly Rate**: $150/hour, $200/hour, $250/hour (number) — for profitability tracking

### Permission Boundaries

**Consultants**: Full access to client projects (create, edit, comment, track time)

**Clients** (invited as guests): Access to their projects only (e.g., Acme Corp guest can only see "Client: Acme Corp" projects)

**Guest permissions**: Comment-only (clients can comment, attach files, but cannot edit tasks)

**Private projects**: Leadership team projects (M&A, strategy, financials) are private (only partners/directors can see)

### Integration Architecture

**Critical integrations** (enable immediately):
1. **Harvest or Toggl** (time tracking): Connect time tracking tool, enable time tracking per task — consultants track time as they work
2. **Email**: Enable "Add task via email" (x@mail.asana.com) — consultants can forward client emails to Asana, creates task automatically
3. **Google Drive**: Connect Google Drive, attach deliverables (PowerPoint, Excel, reports)
4. **Google Calendar**: Sync deliverable due dates, client meetings to calendar

**Optional integrations**:
- **Slack**: Notifications (mention in Asana → Slack notification), create tasks from Slack
- **QuickBooks/Xero**: Export time tracking data for invoicing (via Harvest/Toggl → QuickBooks integration)

**Automation workflows**:
- **Auto-assign partner review**: When deliverable moved to "In Review", auto-assign partner for review
- **Notify before deadline**: 3 days before deliverable due date, send notification to assigned consultant
- **Weekly time tracking reminder**: Slack bot posts "Log your time in Asana" every Friday at 5pm

---

## 5. Implementation Guide (30-90 day roadmap)

### Week 1-2: Setup & Configuration

**Day 1-2: Workspace setup**
- Create Asana workspace (firm name)
- Create "Client Projects" team
- Invite 2-3 early adopters (1 partner + 1-2 consultants)

**Day 3-5: Project setup**
- Create projects for active clients (2-3 client projects)
- Create sections (Backlog, To Do, In Progress, In Review, Client Review, Complete)
- Create custom fields (Client, Project Budget, Time Budget, Deliverable Type, Hourly Rate)

**Day 6-7: Time tracking integration**
- Connect Harvest or Toggl to Asana
- Enable time tracking per task (Harvest/Toggl timer appears in Asana task)
- Test workflow: Start timer in Asana task → Track 30 minutes → Stop timer → Verify time logged in Harvest/Toggl

**Day 8-10: Create templates**
- Create engagement templates:
  - **Strategy Engagement**: Kickoff, Research, Analysis, Recommendations, Presentation (10-15 tasks)
  - **Workshop Engagement**: Prep, Facilitation, Post-workshop report (5-8 tasks)
  - **Report Deliverable**: Outline, Draft, Review, Client review, Final report (5-7 tasks)

**Day 11-14: Pilot with early adopters**
- Pilot with 2-3 people (1 partner + 1-2 consultants)
- Create 5-10 real tasks (ongoing client work)
- Track time on tasks (start timer, work, stop timer)
- Invite 1 client as guest (test client guest access)
- Gather feedback: "Is Asana easier than spreadsheets? Is time tracking seamless?"

### Week 3-4: Pilot Expansion (6-8 people)

**Week 3: Expand pilot to full team**
- Onboard all consultants (6-8 people)
- Training session (1 hour): Asana UI tour, create tasks, timeline view, time tracking, workload view
- Hands-on exercise: Each consultant creates 3 tasks, assigns to themselves, tracks time

**Week 4: Invite clients as guests**
- Identify 1-2 clients for pilot (friendly clients)
- Invite clients as guests to their projects ("This is our new collaboration tool, you can see project progress here")
- Training for clients (10 minutes): How to view tasks, comment, review deliverables

### Week 5-8: Rollout (All Clients)

**Week 5-6: Migrate all active projects**
- Create projects for all active clients (5-15 client projects)
- Migrate tasks from spreadsheets/email to Asana (copy deliverables, due dates, status)
- Invite all clients as guests to their projects

**Week 7-8: Establish workflow**
- Weekly planning meetings: Review workload view (who's overloaded, who can take new client)
- Time tracking enforcement: Partners check "Did everyone log time this week?" — send reminders if needed
- Deliverables tracking: Use timeline view to show clients engagement schedule
- **Success metric**: 90%+ consultants using Asana daily, 80%+ time tracked in Asana (not Excel)

### Month 3: Optimization

**Optimize workflows**:
- Review engagement lifecycle: Are projects completing on time? On budget?
- Identify bottlenecks: Are deliverables getting stuck in "In Review"? (Add automation: notify partner after 2 days)
- Refine time tracking: Are consultants logging time daily? (Send daily reminder: "Log your time before end of day")

**Add dashboards**:
- **Utilization dashboard**: Show billable hours % per consultant (target: 70-80% utilization)
- **Project profitability dashboard**: Show time spent vs budget per client (flag projects over budget)
- **Deliverables dashboard**: Show upcoming deliverables (next 7 days, next 30 days)

**Success metrics** (Month 3):
- ✅ 95%+ consultant adoption (daily active users)
- ✅ 90%+ time tracked in Asana (not Excel at end of week)
- ✅ 50%+ client engagement (clients view Asana weekly, comment on deliverables)
- ✅ Improved project profitability (10-15% improvement due to better time tracking, capacity planning)

---

## 6. TCO Analysis (3-year total cost, 10 consultants)

| Cost Component | Amount | Notes |
|----------------|--------|-------|
| **Subscription (3 years)** | $3,960 | $11/user/month × 10 consultants × 36 months |
| **Time tracking subscription** | $1,440 | Harvest $12/user/month × 10 consultants × 12 months (year 1), then $720/year (assume 5 active users) |
| **Training** | $4,000 | 1.5 hours training + 2 weeks learning curve × 10 consultants × $100/hour |
| **Migration** | $2,000 | 1 week to migrate from spreadsheets × 1 operations person × $80/hour |
| **Support** | $0 | Asana + Harvest support included |
| **Productivity loss** | $8,000 | 2-week learning curve × 10 consultants × $100/hour |
| **Total 3-Year TCO** | **$19,400** | |

**Cost per consultant per month**: ~$54/month ($19,400 / 10 consultants / 36 months)

**Comparison to alternatives**:
- **ClickUp** (with native time tracking): $15,120 (3-year, 10 consultants, no time tracking integration needed) — 22% cheaper than Asana + Harvest
- **Trello** (with Harvest integration): $13,800 (3-year, 10 consultants) — 29% cheaper than Asana, but limited features (no workload view, no timeline)
- **Spreadsheets (free)**: $0 subscription, but high hidden cost (manual time tracking, no capacity planning, over-budget projects)

**ROI**: Asana + time tracking pays for itself if it **improves project profitability by 10%**. Example: If firm has $1M revenue, 10% profitability improvement = $100K additional profit/year → $300K over 3 years (vs $19,400 TCO = **15.5x ROI**).

---

## 7. Success Metrics

### Week 4 Metrics (Pilot Success)
- ✅ **80%+ daily active users** (pilot team using Asana daily)
- ✅ **Time tracking working** (consultants track time in Asana via Harvest/Toggl)
- ✅ **1-2 clients using Asana** (clients viewing deliverables, commenting)
- ✅ **Positive feedback** (consultants report "Asana + Harvest easier than Excel")

### Month 3 Metrics (Rollout Success)
- ✅ **90%+ daily active users** (all consultants using Asana daily)
- ✅ **90%+ time tracked in Asana** (not Excel at end of week — track time as you work)
- ✅ **50%+ client engagement** (clients view Asana weekly, 30%+ comment on deliverables)
- ✅ **All active projects in Asana** (5-15 client projects tracked in Asana, not spreadsheets)

### Month 6 Metrics (Optimization Success)
- ✅ **95%+ consultant adoption** (Asana is default tool, not optional)
- ✅ **95%+ time tracked in Asana** (real-time time tracking, not weekly batch)
- ✅ **60%+ client engagement** (clients actively use Asana, not just passive viewers)
- ✅ **10-15% profitability improvement** (better time tracking, capacity planning, fewer over-budget projects)

---

## 8. Common Pitfalls

### Pitfall 1: **Time tracking at end of week (inaccurate, time-consuming)**
**Problem**: Consultants track time in Excel at end of week → inaccurate ("Was that 2 hours or 3 hours on Monday?") → 30-60 minutes wasted reconstructing week
**Solution**:
- Track time as you work (start timer when starting task, stop timer when done)
- Daily reminder: Slack bot posts "Log your time before end of day" at 5pm
- Partners enforce: "No invoicing until time is logged" (link invoicing to time tracking compliance)

### Pitfall 2: **Not using templates (recreating same tasks every engagement)**
**Problem**: Consultants create same 10-15 tasks for every strategy engagement → wastes 30-60 minutes per new project
**Solution**:
- Create templates for common engagements (Strategy, Workshop, Report)
- Use Asana's template feature (duplicate project → removes completed tasks, resets due dates)
- Update templates quarterly (add/remove tasks based on what worked)

### Pitfall 3: **Workload view ignored (capacity planning manual)**
**Problem**: Partners don't check workload view → some consultants overloaded (80 billable hours/week), others underutilized (20 hours) → burnout + missed revenue
**Solution**:
- Weekly planning meetings: Review workload view (15 minutes)
- Redistribute work: Move projects from overloaded to underutilized consultants
- Set capacity targets: "Each consultant should have 28-35 billable hours/week (70-80% utilization of 40-hour week)"

### Pitfall 4: **Projects go over budget (no profitability tracking)**
**Problem**: Consultants track time, but partners don't monitor time vs budget → projects go 20-50% over budget → unprofitable engagements
**Solution**:
- Add custom field: "Time Budget" (e.g., 100 hours) per project
- Weekly review: Compare "Time Spent" (sum of tracked time) vs "Time Budget"
- Alert when 80% of budget consumed: "Project is 80% over budget, review scope or upsell client"

### Pitfall 5: **Clients don't engage with Asana (still use email for feedback)**
**Problem**: Clients invited to Asana, but don't use it → consultants still get feedback via email → defeats collaboration purpose
**Solution**:
- Onboarding call with client: 10-minute demo ("This is how you view deliverables, comment, approve")
- Set expectations: "Please provide feedback in Asana, not email — keeps everything in one place"
- Lead by example: Partners ask clients "Can you comment in Asana?" (redirect from email to Asana)

---

## 9. Additional Resources

**Asana resources**:
- Asana for Professional Services guide: https://asana.com/guide/professional-services
- Asana time tracking integrations: https://asana.com/guide/integrations/time-tracking
- Asana workload view: https://asana.com/guide/help/premium/workload

**Time tracking tools**:
- Harvest: https://www.getharvest.com/ (Recommended: Best Asana integration, invoicing features)
- Toggl: https://toggl.com/ (Alternative: Simpler, cheaper than Harvest)
- Everhour: https://everhour.com/ (Alternative: Built for Asana, native-like integration)

**Community**:
- Asana Community Forum: https://forum.asana.com/
- Asana for Consulting best practices

---

**Last Updated**: 2025-11-12
**Phase**: S3 Need-Driven
**Scenario**: 5 of 5 (Small Consulting Firm)
