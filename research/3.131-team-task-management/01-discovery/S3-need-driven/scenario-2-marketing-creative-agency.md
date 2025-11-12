# S3 Scenario 2: Marketing/Creative Agency

**Date**: 2025-11-12
**Phase**: S3 Need-Driven
**Scenario**: Marketing/creative agency (8-20 people) managing client campaigns and internal projects

---

## 1. Team Profile

**Team size**: 8-20 people
- 1-2 agency owners/directors
- 2-4 account managers (client-facing)
- 3-6 content creators (writers, designers, video editors)
- 1-2 social media managers
- 1-2 project coordinators

**Industry/domain**: Marketing agency, creative agency, digital agency

**Budget constraints**: $10-15/user/month ($120-300/month for 15 people)

**Technical sophistication**: Medium (not engineers, but comfortable with SaaS tools, integrations)

**Current workflow pain points**:
- Work scattered across email, Slack, Google Drive, spreadsheets
- Client feedback lost in email threads ("Where did the client say to change the headline?")
- No visibility into team capacity ("Who can take on a new project?")
- Campaign timelines tracked in spreadsheets (manual updates, not real-time)
- Content approval bottlenecks ("Waiting for client approval, not sure what's the status")
- Missed deadlines (no alerts when tasks are overdue)

---

## 2. Requirements

### Must-Have Features (Deal-Breakers)
- ✅ **Client-facing boards**: Invite clients to specific projects (guest access, not full team access)
- ✅ **File attachments & proofing**: Attach designs, videos, docs — clients can comment, approve
- ✅ **Timeline/Gantt view**: Campaign timeline (launch dates, milestones)
- ✅ **Task dependencies**: "Social posts depend on blog post being published"
- ✅ **Email integration**: Create tasks from client emails, email notifications
- ✅ **Workload view**: See team capacity (who's overloaded, who can take new work)

### Important Features (Strong Preference)
- **Calendar view**: Content calendar (blog posts, social media, email campaigns)
- **Recurring tasks**: Weekly social posts, monthly reports, quarterly strategy reviews
- **Templates**: Campaign templates (product launch, webinar, email campaign)
- **Automation**: Auto-assign tasks, notify when task is complete, move tasks on due date
- **Custom fields**: Client name, campaign type, content type, approval status
- **Mobile app**: Account managers need mobile access (client meetings, on-the-go updates)

### Optional Features (Bonus)
- **Time tracking**: Track time spent per client (for billing, profitability analysis)
- **Reports/dashboards**: Client-specific dashboards (show progress to clients)
- **Integration with Google Drive/Dropbox**: Auto-attach files from Drive
- **Slack integration**: Notifications in Slack, create tasks from Slack

### Integration Needs (Critical)
- **Email** (must-have, used daily): Create tasks from emails, email notifications, reply-to-update
- **Google Drive** (must-have, used daily): Attach files from Drive, preview in-app
- **Slack** (important, used daily): Notifications, create tasks from Slack
- **Google Calendar** (important, used daily): Campaign deadlines, client meetings, due dates
- **Mailchimp** (optional, used weekly): Link email campaigns to tasks

### Permission Requirements
- **Client guest access**: Invite clients to specific projects (read-only or comment-only, not full edit)
- **Project-level permissions**: Clients can only see their projects (not other clients' work)
- **Role-based access**: Account managers (full access), content creators (edit tasks), clients (comment-only)

### Mobile Needs
- **Mobile-important**: 20-30% of work done on mobile (account managers in client meetings, on-the-go updates)
- **Push notifications**: Important (due date reminders, client comments, approval requests)
- **Offline mode**: Nice-to-have (not critical, most work done with internet)

---

## 3. Platform Recommendations

### Primary Recommendation: **Asana**

**Pricing**: $11/user/month (15 people = $165/month, $1,980/year)

**Why Asana?**
1. **Excellent client guest access** (S2 finding): Unlimited guests (free), project-level access — clients can view/comment on their projects only
2. **Timeline view** (S2 finding): Visual Gantt chart for campaign timelines — account managers can show clients "Here's the campaign timeline"
3. **Proofing/annotations** (S2 finding): Attach designs, clients can comment directly on images — eliminates "Where did client say to change X?" confusion
4. **Workload view** (S2 finding): See team capacity (who's overloaded, who can take new work) — critical for agencies juggling many clients
5. **Templates** (S2 finding): Campaign templates (product launch, webinar, content calendar) — save 1-2 hours per new campaign
6. **Email integration** (S2 finding): Create tasks from emails (x@mail.asana.com), reply-to-update — account managers can turn client emails into tasks instantly
7. **Calendar view**: Content calendar (blog posts, social media, email campaigns) — social media managers need this
8. **Cross-functional workflows** (S2 finding): Asana designed for marketing teams (vs Linear for dev teams) — features match agency workflows

**Implementation complexity**: Medium (2-3 weeks to full productivity, requires workflow design)

**Time to value**: 14-21 days (account managers adopt fast, content creators need 2 weeks training)

---

### Alternative 1: **Monday.com** (visual thinkers, CRM-heavy agencies)

**Pricing**: $12/user/month (15 people = $180/month, $2,160/year)

**When to choose Monday.com over Asana**:
- ✅ Team prefers visual boards (Monday.com is more colorful, visual than Asana)
- ✅ Agency uses CRM heavily (Monday.com has deeper Salesforce/HubSpot integration than Asana)
- ✅ Non-technical team (Monday.com is more visual, less structured than Asana)
- ✅ Want built-in client dashboards (Monday.com has better dashboard features for client-facing reports)

**Trade-offs**:
- ❌ Proofing weaker than Asana (Monday.com has file attachments, but not as good as Asana's proofing/annotations)
- ❌ Workload view limited (Monday.com workload view is Business tier $16/user, Asana includes in Premium $11/user)
- ❌ Timeline view less mature (Monday.com has Gantt, but Asana's Timeline view is more polished)
- ✅ More expensive ($12/user vs $11/user Asana)

---

### Alternative 2: **ClickUp** (budget-conscious, want more features)

**Pricing**: $7/user/month (15 people = $105/month, $1,260/year)

**When to choose ClickUp over Asana**:
- ✅ Budget priority ($7/user vs $11/user Asana — 36% cheaper)
- ✅ Want built-in time tracking (ClickUp native, Asana requires integrations like Harvest/Toggl)
- ✅ Want more customization (ClickUp most flexible, Asana more opinionated)
- ✅ Team is tech-savvy (ClickUp has more features, but steeper learning curve)

**Trade-offs**:
- ❌ More complex UI (ClickUp 7 roles, deep hierarchy — harder for non-technical teams)
- ❌ Higher training cost (S2 finding: ClickUp $8,000 training vs Asana $4,000 for 10 users over 3 years)
- ❌ Client guest access more limited (ClickUp free tier: 2 guests, Asana free tier: unlimited guests — Asana better for agencies with many clients)
- ❌ Proofing weaker than Asana (ClickUp has file attachments, but not as good as Asana's proofing/annotations)

---

## 4. Architecture Pattern

### Workspace/Organization Structure (Asana)

**Organization**: Agency name (e.g., "Acme Agency")

**Teams** (Asana concept = department):
- **Client Work** (main team, all agency staff + clients as guests)
- **Internal** (internal projects, not client-facing)
- **Leadership** (agency owners, directors only — private team)

**Projects** (per client or per campaign):
- **Client: Acme Corp** (all work for Acme Corp client)
  - **Q1 2025 Campaign** (product launch campaign)
  - **Blog Content** (ongoing blog posts)
  - **Social Media** (ongoing social posts)
- **Client: Beta Inc** (all work for Beta Inc client)
  - **Webinar Campaign** (webinar launch)
  - **Email Marketing** (ongoing email campaigns)
- **Internal: Marketing** (agency's own marketing)
- **Internal: Operations** (agency operations, hiring, onboarding)

**Sections** (within projects, Asana concept = workflow stages):
- **Backlog** (ideas, not yet scheduled)
- **To Do** (scheduled, not started)
- **In Progress** (content creator is working on it)
- **In Review** (account manager reviews before sending to client)
- **Client Review** (waiting for client approval)
- **Approved** (client approved, ready to publish)
- **Published** (live, campaign launched)

**Custom fields**:
- **Client**: Acme Corp, Beta Inc, Internal (dropdown)
- **Campaign**: Q1 Launch, Webinar, Blog, Social (dropdown)
- **Content Type**: Blog post, social post, email, video, design (dropdown)
- **Approval Status**: Pending, Approved, Revisions Needed (dropdown)
- **Priority**: High, Medium, Low (dropdown)

### Permission Boundaries

**Agency staff** (account managers, content creators, social media managers): Full access to all client projects (create, edit, comment)

**Clients** (invited as guests): Access to their projects only (e.g., Acme Corp guest can only see "Client: Acme Corp" projects, not "Client: Beta Inc")

**Guest permissions**: Comment-only (clients can comment, attach files, but cannot edit tasks or assign)

**Private projects**: Leadership team projects (agency strategy, financials) are private (only owners/directors can see)

### Integration Architecture

**Critical integrations** (enable immediately):
1. **Email**: Enable "Add task via email" (x@mail.asana.com) — account managers can forward client emails to Asana, creates task automatically
2. **Google Drive**: Connect Google Drive, enable file attachments from Drive (attach client briefs, designs, docs)
3. **Slack**: Connect Slack workspace, enable notifications (mention in Asana → notification in Slack), create tasks from Slack
4. **Google Calendar**: Connect Google Calendar, sync due dates (campaign launch dates appear in calendar)

**Optional integrations**:
- **Mailchimp**: Connect Mailchimp (if using), link email campaigns to Asana tasks
- **Zapier**: Automate workflows (e.g., "When task moved to 'Client Review', send email to client")

**Automation workflows**:
- **Auto-assign account manager**: When task created in "Client: Acme Corp" project, auto-assign account manager for Acme Corp
- **Notify in Slack**: When task moved to "Client Review", post to #client-work Slack channel ("Waiting for Acme Corp approval on blog post")
- **Due date reminders**: 2 days before due date, send Slack notification to assignee ("Reminder: Campaign launch due in 2 days")

---

## 5. Implementation Guide (30-90 day roadmap)

### Week 1-2: Setup & Configuration

**Day 1-2: Workspace setup**
- Create Asana workspace (agency name)
- Create "Client Work" team
- Invite 2-3 early adopters (1 agency owner + 1 account manager + 1 content creator)
- Configure team settings (workweek: Mon-Fri, start day: Monday)

**Day 3-4: Project setup**
- Create projects for top 2-3 clients (e.g., "Client: Acme Corp", "Client: Beta Inc")
- Create sections within projects (Backlog, To Do, In Progress, In Review, Client Review, Approved, Published)
- Create custom fields (Client, Campaign, Content Type, Approval Status, Priority)

**Day 5-7: Integration setup**
- Connect email: Set up "Add task via email" (x@mail.asana.com) — test by forwarding email, verify task created
- Connect Google Drive: Link Google Drive account, test file attachment from Drive
- Connect Slack: Link Slack workspace, configure notification settings
- Connect Google Calendar: Sync due dates to calendar

**Day 8-10: Create templates**
- Create campaign templates:
  - **Product Launch Campaign**: 20-30 tasks (brief, research, content creation, design, review, client approval, launch, post-launch analysis)
  - **Blog Post Template**: 10-15 tasks (topic brainstorm, outline, draft, edit, SEO, images, client review, publish)
  - **Social Media Campaign**: 15-20 tasks (calendar planning, content creation, image design, scheduling, posting, engagement tracking)

**Day 11-14: Pilot with early adopters**
- Pilot with 2-3 people (1 account manager + 1-2 content creators)
- Create 10-20 real tasks (ongoing client work)
- Invite 1 client as guest to their project (test client guest access)
- Track tasks through workflow (To Do → In Progress → In Review → Client Review → Approved → Published)
- Gather feedback: "What's working? What's confusing?"

### Week 3-4: Pilot Expansion (8-10 people)

**Week 3: Expand pilot to full team**
- Onboard all agency staff (8-10 people: account managers, content creators, social media managers, project coordinators)
- Training session (1 hour): Asana UI tour, create tasks, timeline view, workload view, email integration
- Hands-on exercise: Each person creates 3 tasks, assigns to themselves, moves through workflow

**Week 4: Invite clients as guests**
- Identify 2-3 clients for pilot (friendly clients, open to new tools)
- Invite clients as guests to their projects (explain: "This is our new collaboration tool, you can see campaign progress here")
- Training for clients (15 minutes): How to view tasks, comment, attach files, approve
- **Success metric**: 80%+ of agency staff using Asana daily, 2-3 clients actively using Asana

### Week 5-8: Rollout (All Clients)

**Week 5-6: Migrate all active work**
- Create projects for all clients (10-20 client projects)
- Migrate active campaigns from spreadsheets/email to Asana (copy tasks, due dates, status)
- Invite all clients as guests to their projects
- Send email to clients: "We've moved to Asana for better collaboration, you can track campaign progress here"

**Week 7-8: Establish workflow**
- Weekly planning meetings: Review workload view (who's overloaded, who can take new work)
- Daily check-ins: Account managers check "Client Review" section (what's waiting for client approval)
- Campaign launches: Use timeline view to show clients campaign schedule
- **Success metric**: 90%+ of agency staff using Asana daily, 50%+ of clients viewing Asana weekly

### Month 3: Optimization

**Optimize workflows**:
- Review task lifecycle: Are tasks moving smoothly? (To Do → In Progress → Published)
- Identify bottlenecks: Are tasks getting stuck in "Client Review"? (Add automation: send email reminder to client after 3 days)
- Add automation: Auto-assign tasks, notify in Slack, send due date reminders

**Add advanced features**:
- **Dashboards**: Create client-facing dashboards (show client their campaign progress: 10 tasks completed, 5 in progress, 2 waiting on client)
- **Workload view**: Review team capacity weekly (redistribute work if someone is overloaded)
- **Reports**: Monthly client reports (tasks completed, campaigns launched, upcoming deadlines)

**Success metrics** (Month 3):
- ✅ 95%+ agency staff adoption (daily active users)
- ✅ 60%+ client engagement (clients view Asana weekly, comment on tasks)
- ✅ 50%+ reduction in "Where's the status?" emails (clients can see status in Asana, no need to email account manager)
- ✅ Faster campaign launches (survey: "Did Asana reduce campaign launch time?" — 70%+ say yes)

---

## 6. TCO Analysis (3-year total cost, 15 people)

| Cost Component | Amount | Notes |
|----------------|--------|-------|
| **Subscription (3 years)** | $5,940 | $11/user/month × 15 people × 36 months |
| **Training** | $6,000 | 2 hours training + 3 weeks learning curve × 15 people × $80/hour |
| **Migration** | $4,500 | 2 weeks to migrate from spreadsheets/email × 1 project coordinator × $80/hour |
| **Support** | $0 | Asana support included (email, chat, docs) |
| **Productivity loss** | $12,000 | 3-week learning curve (reduced productivity) × 15 people × $80/hour |
| **Total 3-Year TCO** | **$28,440** | |

**Cost per person per month**: ~$52/month ($28,440 / 15 people / 36 months)

**Comparison to alternatives**:
- **Monday.com**: $32,640 (3-year, 15 people) — 15% more expensive than Asana
- **ClickUp**: $25,800 (3-year, 15 people) — 9% cheaper than Asana, but higher training cost offsets savings
- **Spreadsheets (free)**: $0 subscription, but high hidden cost (manual updates, no automation, no client collaboration)

**ROI**: Asana pays for itself if it saves **1-2 hours per person per month** (reduced time searching for client feedback, faster task creation, better visibility). At $80/hour agency staff cost, 1-2 hours saved = $80-160/month value per person → $1,200-2,400/year per person → $18,000-36,000/year for 15 people → $54,000-108,000 over 3 years.

---

## 7. Success Metrics

### Week 4 Metrics (Pilot Success)
- ✅ **80%+ daily active users** (agency staff using Asana daily)
- ✅ **90%+ work tracked in Asana** (not scattered in email, spreadsheets)
- ✅ **2-3 clients using Asana** (clients viewing tasks, commenting, approving)
- ✅ **Positive feedback** (agency staff reports "Asana is better than spreadsheets")

### Month 3 Metrics (Rollout Success)
- ✅ **90%+ daily active users** (all agency staff using Asana daily)
- ✅ **50%+ client engagement** (clients view Asana weekly, 30%+ clients comment on tasks)
- ✅ **95%+ work tracked in Asana** (all campaigns, tasks in Asana)
- ✅ **<5 "Where's the status?" emails per week** (clients can see status in Asana)

### Month 6 Metrics (Optimization Success)
- ✅ **95%+ agency staff adoption** (Asana is default tool, not optional)
- ✅ **60%+ client engagement** (clients actively use Asana, not just passive viewers)
- ✅ **50%+ reduction in status emails** ("Where's the status?" emails eliminated, clients check Asana)
- ✅ **Faster campaign launches** (survey: "Did Asana reduce campaign launch time by 20%+?" — 70%+ say yes)

---

## 8. Common Pitfalls

### Pitfall 1: **Inviting clients too early (before agency staff is trained)**
**Problem**: Clients invited before agency is comfortable with Asana → clients see incomplete tasks, messy projects → bad first impression
**Solution**:
- Train agency staff first (2-3 weeks pilot)
- Invite clients AFTER agency is comfortable (Week 4+)
- Clean up projects before inviting clients (complete tasks, add descriptions, attach files)

### Pitfall 2: **Not setting client expectations (clients don't understand Asana's purpose)**
**Problem**: Clients don't understand why they're invited to Asana → ignore notifications → don't comment/approve → agency still uses email
**Solution**:
- Onboarding email to clients: "We're using Asana for better collaboration. You can see campaign progress, comment on tasks, and approve work here."
- 15-minute training call: Show clients how to view tasks, comment, approve
- Set expectations: "Please check Asana 1-2x per week for updates, comment if you have feedback"

### Pitfall 3: **Creating too many projects (one project per task → overwhelming)**
**Problem**: Agency creates 100+ projects (one project per blog post, per social post) → overwhelming, hard to navigate
**Solution**:
- One project per client (e.g., "Client: Acme Corp"), not per campaign
- Use sections within projects for campaigns (e.g., "Q1 Launch", "Blog Content", "Social Media")
- Use custom fields to categorize (Campaign, Content Type) instead of creating separate projects

### Pitfall 4: **Not using templates (recreating same tasks every campaign)**
**Problem**: Agency recreates same 20-30 tasks for every product launch campaign → wastes 1-2 hours per campaign
**Solution**:
- Create templates for common campaigns (Product Launch, Webinar, Blog Post, Social Media Campaign)
- Use Asana's template feature (duplicate project → removes completed tasks, resets due dates)
- Update templates quarterly (add/remove tasks based on what worked/didn't work)

### Pitfall 5: **Not reviewing workload view (team capacity imbalance)**
**Problem**: Account managers don't check workload view → some content creators overloaded (20 tasks), others underutilized (3 tasks) → burnout + missed deadlines
**Solution**:
- Weekly planning meetings: Review workload view (15 minutes)
- Redistribute work: Move tasks from overloaded to underutilized team members
- Set capacity limits: "Each content creator should have 8-12 active tasks max"

---

## 9. Additional Resources

**Asana resources**:
- Asana for Agencies guide: https://asana.com/guide/agencies
- Asana templates (marketing): https://asana.com/templates/marketing
- Asana timeline view guide: https://asana.com/guide/help/premium/timeline
- Asana guest access guide: https://asana.com/guide/help/permissions/guests

**Community**:
- Asana Community Forum: https://forum.asana.com/
- Asana for Marketing Facebook group

---

**Last Updated**: 2025-11-12
**Phase**: S3 Need-Driven
**Scenario**: 2 of 5 (Marketing/Creative Agency)
