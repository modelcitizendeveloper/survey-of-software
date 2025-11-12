# S3 Scenario 1: Software Development Team

**Date**: 2025-11-12
**Phase**: S3 Need-Driven
**Scenario**: Software development team (5-15 engineers) building a SaaS product

---

## 1. Team Profile

**Team size**: 5-15 engineers
- 1-2 engineering managers
- 3-10 software engineers (full-stack, frontend, backend)
- 1-2 product managers (optional, may overlap with eng managers)

**Industry/domain**: Technology (SaaS, B2B software)

**Budget constraints**: $5-15/user/month ($40-180/month for 10 engineers)

**Technical sophistication**: Very high (engineers, comfortable with APIs, automation, keyboard shortcuts)

**Current workflow pain points**:
- Using GitHub Issues (limited features, no roadmap view, weak mobile app)
- Work scattered across GitHub, Slack, Notion docs
- No visibility: "What's everyone working on?"
- Context switching: GitHub (code) → Slack (status) → Notion (specs) → Calendar (meetings)
- Missing sprint planning features (velocity, estimation, burndown)

---

## 2. Requirements

### Must-Have Features (Deal-Breakers)
- ✅ **Deep GitHub integration**: Auto-close issues from commits, branch creation, PR linking, issue references in code
- ✅ **Keyboard shortcuts**: Fast navigation (engineers hate using mouse)
- ✅ **Sprint planning**: Sprints, estimation (story points), velocity tracking
- ✅ **Roadmap view**: Timeline of epics, releases (product manager needs this)
- ✅ **Fast task creation**: <5 seconds to create issue (engineers won't use slow tools)
- ✅ **Slack integration**: Notifications, create issues from Slack

### Important Features (Strong Preference)
- **Subtasks/nested issues**: Break epics into features into tasks
- **Issue dependencies**: "Task B blocked by Task A"
- **Custom fields**: Priority, severity, component, release version
- **Mobile app**: Good mobile app (on-call engineers need mobile access)
- **Search**: Fast full-text search (find issues by keyword)
- **Filtering**: Filter by assignee, label, status, sprint

### Optional Features (Bonus)
- **Time tracking**: Estimate vs actual time (nice-to-have, not critical)
- **Workload view**: See team capacity, who's overloaded
- **Automation**: Auto-assign issues, notify on status change
- **API**: Custom integrations (internal tools, monitoring)

### Integration Needs (Critical)
- **GitHub** (must-have, used daily): Auto-close issues, branch creation, commit references
- **Slack** (must-have, used daily): Notifications, create issues from Slack, daily standups
- **Figma** (important, used 2-3x/week): Link designs to issues
- **Sentry** (important, used weekly): Auto-create issues from errors
- **Calendar** (important, used daily): Sprint planning meetings, due dates

### Permission Requirements
- **Simple permissions**: Flat team structure (all engineers have equal access)
- **Guest access**: Occasional external stakeholders (investors, advisors) need read-only access
- **Private teams**: Some projects may be confidential (not visible to all engineers)

### Mobile Needs
- **Mobile-first**: 30-40% of work done on mobile (on-call, commuting, quick updates)
- **Offline mode**: Would be nice (on-call engineers in poor connectivity)
- **Push notifications**: Critical (on-call alerts, deployment notifications)

---

## 3. Platform Recommendations

### Primary Recommendation: **Linear**

**Pricing**: $8/user/month (10 engineers = $80/month, $960/year)

**Why Linear?**
1. **Best GitHub integration** (S2 finding): Auto-close from commits, branch creation, PR linking — exactly what dev teams need
2. **Keyboard-driven UX** (S2 finding): Fastest navigation (Cmd+K, vim-like shortcuts) — engineers love this
3. **Mobile-first design** (S2 finding): 4.9★ iOS rating, best mobile app among all platforms — perfect for on-call engineers
4. **Fast task creation** (S2 finding): 3 taps, ~5 seconds — engineers will actually use it
5. **Sprint planning built-in**: Sprints, estimation, velocity, burndown charts
6. **Roadmap view**: Timeline of epics, cycles, releases (product manager needs this)
7. **Clean, minimal UI**: Not cluttered with features dev teams don't need (vs ClickUp complexity)
8. **Read-only guest access**: Investors, advisors can view projects (free, unlimited guests)

**Implementation complexity**: Low (fast onboarding, intentionally minimal, 1-2 weeks to full productivity)

**Time to value**: 7-14 days (engineers adopt fast, keyboard shortcuts reduce friction)

---

### Alternative 1: **Asana** (if cross-functional team, not just engineering)

**Pricing**: $11/user/month (10 people = $110/month, $1,320/year)

**When to choose Asana over Linear**:
- ✅ Team is cross-functional (engineering + marketing + ops), not just engineers
- ✅ Need more integrations beyond dev tools (Asana has 200+ native, 2,000+ Zaps vs Linear 20-30 native)
- ✅ Product managers need advanced portfolio features (Asana Portfolio view vs Linear basic roadmap)
- ✅ Team already uses Asana (switching cost high)

**Trade-offs**:
- ❌ GitHub integration weaker than Linear (Asana has GitHub integration, but not as deep — no branch creation from UI)
- ❌ Slower than Linear (Linear is fastest app, Asana is very good but not as fast)
- ❌ Not keyboard-driven (Asana has some shortcuts, but not Linear-level)
- ✅ More features (Asana 54/64 features vs Linear 42/64 — but dev teams don't need most extra features)

---

### Alternative 2: **ClickUp** (budget-conscious, want more features)

**Pricing**: $7/user/month (10 engineers = $70/month, $840/year)

**When to choose ClickUp over Linear**:
- ✅ Budget priority ($7/user vs $8/user Linear, $11/user Asana)
- ✅ Want built-in time tracking (ClickUp native, Linear requires integration)
- ✅ Team wants customization (ClickUp most flexible, Linear is intentionally minimal)
- ✅ Need advanced automation (ClickUp has more automation than Linear)

**Trade-offs**:
- ❌ Slower than Linear (ClickUp is feature-rich, but slower mobile app, lower ratings: 4.7★ iOS vs Linear 4.9★)
- ❌ More complex UI (ClickUp 7 roles, deep hierarchy — overkill for small dev teams)
- ❌ GitHub integration not as good as Linear (ClickUp has GitHub integration, but Linear purpose-built for dev teams)
- ❌ Higher training cost (S2 finding: ClickUp $8,000 training cost vs Linear $2,000 for 10 users over 3 years)

---

## 4. Architecture Pattern

### Workspace/Organization Structure (Linear)

**Organization**: Company name (e.g., "Acme Inc.")

**Teams** (Linear concept = department/product area):
- **Engineering** (main team, all engineers)
- **Product** (product managers, optional)
- **Infrastructure** (if you have DevOps/SRE team)

**Projects** (Linear concept = epic/feature area):
- **Frontend** (React, UI work)
- **Backend** (API, services)
- **Infrastructure** (DevOps, monitoring)
- **Mobile** (iOS, Android)
- **Releases** (release planning, versioning)

**Labels** (for categorization):
- Priority: P0 (critical), P1 (high), P2 (medium), P3 (low)
- Type: bug, feature, improvement, tech-debt
- Component: auth, payments, notifications, etc.
- Status: backlog, todo, in-progress, in-review, done

**Cycles** (Linear concept = sprints, 1-2 weeks):
- Cycle 1 (Nov 12-25, 2025)
- Cycle 2 (Nov 26 - Dec 9, 2025)
- ...

### Permission Boundaries

**All engineers**: Full access to Engineering team (create, edit, delete issues)

**Product managers**: Admin access (can manage projects, roadmaps, but not delete workspace)

**Guests** (investors, advisors): Read-only access to specific projects (via share links or guest invites)

**Private projects**: If confidential projects exist (e.g., unannounced features), create as private (only invited members can see)

### Integration Architecture

**Critical integrations** (enable immediately):
1. **GitHub**: Connect GitHub org, enable auto-close from commits, branch creation, PR linking
2. **Slack**: Connect Slack workspace, enable notifications, issue creation from Slack
3. **Figma**: Connect Figma account, link designs to issues
4. **Sentry** (if using): Enable Sentry integration, auto-create issues from errors

**Custom integrations** (via Linear API):
- CI/CD notifications: Update issue status when deployment completes (via webhook)
- Internal monitoring: Create issues from custom monitoring alerts (via API)

**Automation workflows**:
- **Auto-assign on-call issues**: When issue labeled "incident", auto-assign to on-call engineer (use Linear automation or Slack workflow)
- **Notify team in Slack**: When issue moved to "In Review", post to #engineering Slack channel
- **Daily standup bot**: Slack bot posts "What did you work on yesterday?" — replies auto-link to Linear issues

---

## 5. Implementation Guide (30-90 day roadmap)

### Week 1-2: Setup & Configuration

**Day 1-2: Workspace setup**
- Create Linear workspace (company name)
- Create "Engineering" team
- Invite 2-3 early adopters (engineering managers + 1-2 engineers)
- Configure team settings (cycles: 2-week sprints, estimation: story points)

**Day 3-4: GitHub integration**
- Connect GitHub organization to Linear
- Enable auto-close from commits (configure commit keywords: "Fixes LIN-123", "Closes LIN-123")
- Enable branch creation from Linear UI
- Test workflow: Create issue → Create branch from Linear → Commit with "Fixes LIN-123" → Verify issue auto-closes

**Day 5-7: Slack integration**
- Connect Slack workspace to Linear
- Configure notification settings (per-engineer: mentions, assignments, status changes)
- Enable issue creation from Slack (slash command: `/linear Create issue: Fix login bug`)
- Test workflow: Create issue from Slack → Verify issue appears in Linear

**Day 8-10: Import existing work**
- Export GitHub Issues (if using): Use Linear's GitHub import tool (automatic import)
- Create initial projects (Frontend, Backend, Infrastructure, Mobile)
- Create labels (Priority: P0-P3, Type: bug/feature, Component: auth/payments/etc.)
- Create first cycle (current 2-week sprint)

**Day 11-14: Pilot with early adopters**
- Pilot with 2-3 engineers (engineering managers + 1-2 engineers)
- Create 10-20 real issues (mix of bugs, features, tech-debt)
- Assign issues to pilot team
- Track issues through workflow (todo → in-progress → in-review → done)
- Gather feedback: What's working? What's confusing?

### Week 3-4: Pilot Expansion (5-7 people)

**Week 3: Expand pilot to half the team**
- Onboard 3-5 more engineers (half the team)
- Training session (30 minutes): Linear UI tour, keyboard shortcuts (Cmd+K, C to create, / to search)
- Demo GitHub integration: Show auto-close from commits, branch creation
- Demo Slack integration: Create issues from Slack, notifications

**Week 4: Gather feedback, iterate**
- Daily standups: Check Linear adoption ("Did you update your issues yesterday?")
- Identify friction points: "What's annoying about Linear?"
- Iterate on workflow: Adjust labels, cycles, projects based on feedback
- **Success metric**: 80%+ of pilot team using Linear daily (check activity feed)

### Week 5-8: Rollout (Full Team)

**Week 5: Full team onboarding**
- Onboard remaining engineers (full team)
- Training session (1 hour): Linear UI, keyboard shortcuts, GitHub integration, Slack integration
- Hands-on exercise: Each engineer creates 3 issues, assigns to themselves, moves through workflow

**Week 6: Migrate remaining work**
- Migrate all active work from GitHub Issues to Linear (use import tool)
- Deprecate GitHub Issues: Post notice "We've moved to Linear, please use Linear for new issues"
- Update team guidelines: "All bugs, features tracked in Linear (not Slack, email, Notion)"

**Week 7-8: Establish workflow**
- Sprint planning: Use Linear's cycle feature (2-week sprints)
- Daily standups: Reference Linear issues ("I worked on LIN-234 yesterday, today I'm working on LIN-235")
- Sprint retrospectives: Review velocity, burndown chart, identify blockers
- **Success metric**: 90%+ of team using Linear daily, 95%+ of active work tracked in Linear

### Month 3: Optimization

**Optimize workflows**:
- Review issue lifecycle: Are issues moving smoothly? (todo → in-progress → in-review → done)
- Identify bottlenecks: Are issues getting stuck in "in-review"? (Add automation: notify reviewer in Slack)
- Add custom fields: Release version, severity, customer impact (if needed)

**Add advanced features**:
- Roadmap view: Create roadmap for next quarter (product manager needs this)
- Project milestones: Set milestones for major releases (e.g., "v2.0 launch")
- Workload view: Check team capacity, redistribute work if someone is overloaded

**Automation**:
- Auto-assign on-call issues: When issue labeled "incident", auto-assign to on-call engineer
- Auto-notify in Slack: When issue moved to "In Review", post to #engineering channel
- Weekly summary: Slack bot posts "This week's completed issues" every Friday

**Success metrics** (Month 3):
- ✅ 95%+ team adoption (daily active users)
- ✅ 50%+ reduction in "What's your update?" meetings (async status updates via Linear)
- ✅ Engineers report faster issue tracking (survey: "Is Linear faster than GitHub Issues?")

---

## 6. TCO Analysis (3-year total cost, 10 engineers)

| Cost Component | Amount | Notes |
|----------------|--------|-------|
| **Subscription (3 years)** | $2,880 | $8/user/month × 10 engineers × 36 months |
| **Training** | $2,000 | 1 hour training session + 2 weeks learning curve × 10 engineers × $100/hour |
| **Migration** | $2,000 | 1 week to migrate from GitHub Issues (export + import + cleanup) |
| **Support** | $0 | Linear support included (email, docs, community) |
| **Productivity loss** | $10,000 | 2-week learning curve (reduced velocity) × 10 engineers × $100/hour |
| **Total 3-Year TCO** | **$16,880** | |

**Cost per engineer per month**: ~$47/month ($16,880 / 10 engineers / 36 months)

**Comparison to alternatives**:
- **Asana**: $23,595 (3-year, 10 people) — 40% more expensive than Linear
- **ClickUp**: $17,200 (3-year, 10 people) — similar to Linear, but higher training cost
- **GitHub Issues (free)**: $0 subscription, but limited features (no sprint planning, weak mobile, no roadmap)

**ROI**: Linear pays for itself if it saves **1-2 hours per engineer per month** (reduced time finding issues, faster task creation, better visibility). At $100/hour engineering cost, 1-2 hours saved = $100-200/month value → $1,200-2,400/year → $3,600-7,200 over 3 years.

---

## 7. Success Metrics

### Week 4 Metrics (Pilot Success)
- ✅ **80%+ daily active users** (pilot team using Linear daily)
- ✅ **90%+ work tracked in Linear** (not scattered in GitHub, Slack, email)
- ✅ **<5 minutes avg time to create issue** (fast task entry, no friction)
- ✅ **Positive feedback** (pilot team reports "Linear is faster than GitHub Issues")

### Month 3 Metrics (Rollout Success)
- ✅ **90%+ daily active users** (full team using Linear daily)
- ✅ **95%+ work tracked in Linear** (all bugs, features, tech-debt in Linear)
- ✅ **<3 support questions per week** (low friction, intuitive UX)
- ✅ **GitHub integration working** (issues auto-close from commits)

### Month 6 Metrics (Optimization Success)
- ✅ **95%+ team adoption** (Linear is default tool, not optional)
- ✅ **50%+ reduction in status meetings** ("What's your update?" meetings eliminated, async status via Linear)
- ✅ **Measurable productivity gain** (survey: "Do you spend less time on project management overhead?" — 80%+ say yes)
- ✅ **Improved velocity** (sprint velocity increases 10-20% as team eliminates friction)

---

## 8. Common Pitfalls

### Pitfall 1: **Over-customization (adding too many fields, labels, projects)**
**Problem**: Engineers create 50+ labels, 20+ projects, 30+ custom fields → Linear becomes complex, overwhelming
**Solution**:
- Start minimal: 5-10 labels max (Priority P0-P3, Type: bug/feature, Component: top 3 areas)
- Add fields only when needed (if you're not using a field for 80%+ of issues, delete it)
- Review quarterly: Prune unused labels, projects, fields

### Pitfall 2: **Not configuring GitHub auto-close keywords (issues don't auto-close from commits)**
**Problem**: Engineers commit with "Fixed the bug" (no issue reference) → Linear issue doesn't auto-close → manual cleanup required
**Solution**:
- Document commit keywords: "Fixes LIN-123", "Closes LIN-123", "Resolves LIN-123"
- Post in #engineering Slack: "Always reference Linear issue in commit message: 'Fixes LIN-123'"
- Review pull requests: Remind engineers to reference Linear issues in PR description

### Pitfall 3: **Trying to replace all tools with Linear (overreach)**
**Problem**: Team tries to use Linear for specs, docs, meeting notes → Linear is not designed for this → poor experience
**Solution**:
- Use Linear for issue tracking ONLY (bugs, features, tasks)
- Use Notion for specs, docs, meeting notes (link Notion docs to Linear issues)
- Use Slack for communication (link Slack threads to Linear issues)
- Use Figma for designs (link Figma files to Linear issues)
- **Linear is the hub** (all work tracked), but **not the content store** (specs live in Notion, designs live in Figma)

### Pitfall 4: **Not training team on keyboard shortcuts (engineers use mouse)**
**Problem**: Engineers don't learn keyboard shortcuts → slow navigation → Linear feels slow → lower adoption
**Solution**:
- Training session: 10 minutes on keyboard shortcuts (Cmd+K to search, C to create, / to filter)
- Post cheat sheet in Slack: "Linear keyboard shortcuts" (pin to #engineering channel)
- Lead by example: Engineering managers use keyboard shortcuts in demos, standups

### Pitfall 5: **Slack notification overload (too many notifications → engineers disable)**
**Problem**: Default Linear notifications are too noisy (every comment, mention, status change) → engineers disable → miss critical updates
**Solution**:
- Configure notification settings per engineer (Preferences → Notifications):
  - Enable: Mentions (@yourname), Assignments (assigned to you), Status changes (on your issues)
  - Disable: Comments (unless you're mentioned), Issue created (unless assigned to you)
- Use Slack threads: Reply to Linear issue notifications in Slack threads (keeps #engineering channel clean)

---

## 9. Additional Resources

**Linear resources**:
- Linear Docs: https://linear.app/docs
- Linear API: https://developers.linear.app/docs/graphql/working-with-the-graphql-api
- Linear keyboard shortcuts: https://linear.app/docs/keyboard-shortcuts
- Linear GitHub integration guide: https://linear.app/docs/github

**Community**:
- Linear Discord: https://discord.gg/linear
- Linear Twitter: @linear

---

**Last Updated**: 2025-11-12
**Phase**: S3 Need-Driven
**Scenario**: 1 of 5 (Software Development Team)
