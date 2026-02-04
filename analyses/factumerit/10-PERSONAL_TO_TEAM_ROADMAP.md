# From Personal GTD to Team Product: Transition Roadmap

**Key Insight:** You've built GTD-with-LLM for yourself. The product opportunity is **teams who want this without the technical barrier**.

---

## The Gap: What You Have vs. What Teams Need

### What You Have (Personal Use)

**Architecture:**
- Single Vikunja instance (your account)
- Python scripts (CLI-based)
- Manual YAML editing (or Claude Code assistance)
- Local .env configuration
- Command-line execution

**Works great for:**
- ✅ You (technical user)
- ✅ Claude Code users
- ✅ Power users comfortable with CLI/YAML

**Doesn't work for:**
- ❌ Non-technical GTD practitioners
- ❌ Teams (no multi-user support)
- ❌ People who need "click a button" UX
- ❌ Organizations (no auth, permissions, audit logs)

### What Teams Need (Product)

**Must-have:**
1. **Web UI** - No CLI, no terminal, just browser
2. **Multi-user** - Each person has their own tasks
3. **Shared projects** - Team can see/assign work
4. **Permissions** - Manager sees team tasks, members see own tasks
5. **Simple onboarding** - "Sign up, start chatting with AI"

**Nice-to-have:**
6. **Mobile app** - Capture on-the-go
7. **Email integration** - Forward emails → tasks
8. **Slack/Teams integration** - Capture from chat
9. **Analytics dashboard** - Team velocity, burndown charts
10. **API** - For integrations/automation

---

## The Opportunity: "A Few Steps Away from Multi-User"

You said: **"we're a few steps away from making it multi-user"**

Let's map those steps:

### Step 1: User Authentication (1-2 weeks)

**What it enables:**
- Multiple people can sign up
- Each has their own account
- Separate Vikunja instances per user

**Technical:**
- [ ] Web framework (FastAPI or Django)
- [ ] User model (email, password hash, created_at)
- [ ] Registration flow
- [ ] Login/logout
- [ ] Password reset
- [ ] JWT tokens for API auth

**Keep simple:**
- Email/password only (no OAuth yet)
- No email verification (manually approve beta users)
- Store Vikunja API token per user in database

**Outcome:** 10 beta users, each with isolated Vikunja instance

### Step 2: Web Chat Interface (2-3 weeks)

**What it enables:**
- Users capture tasks via chat (not CLI)
- LLM responds in real-time
- Tasks created in their Vikunja automatically

**Technical:**
- [ ] Chat UI (React/Next.js with Tailwind)
- [ ] WebSocket or Server-Sent Events for streaming
- [ ] LLM integration (Claude API)
- [ ] Prompt: Natural language → YAML → Vikunja API
- [ ] Task creation feedback ("✅ Created: Follow up with WeRise")

**Keep simple:**
- Text only (no voice yet)
- Single chat session (no history yet)
- Basic prompts (refine later)

**Outcome:** Users can capture tasks without writing YAML

### Step 3: Shared Projects (2-3 weeks)

**What it enables:**
- Team lead creates project
- Invites team members
- Everyone sees shared task list
- Assign tasks to team members

**Technical:**
- [ ] Team model (team_id, name, owner_id)
- [ ] Team membership (user_id, team_id, role)
- [ ] Shared Vikunja projects (team-level, not user-level)
- [ ] Task assignment (assigned_to user_id)
- [ ] Permissions (owner can invite, members can view/update)

**Keep simple:**
- Single team per user (no multiple teams yet)
- Basic roles: owner, member (no custom roles)
- In-app invitations only (no email invites yet)

**Outcome:** 2-3 teams (5-10 people each) using for real work

### Step 4: Analysis & Recommendations (1-2 weeks)

**What it enables:**
- "What should we prioritize this week?" → Team-level analysis
- Velocity tracking (team + individual)
- Portfolio export → spawn-analysis style insights

**Technical:**
- [ ] Reuse your export_vikunja.py logic
- [ ] Generate team portfolio state
- [ ] LLM analysis prompt (your spawn-analysis patterns)
- [ ] Weekly email digest (optional)

**Keep simple:**
- Manual trigger ("Analyze portfolio" button)
- Text output (no fancy charts yet)
- Same spawn-analysis methodologies you use personally

**Outcome:** Teams get data-driven prioritization recommendations

### Step 5: Polish & Launch (2-3 weeks)

**What it enables:**
- Public beta launch
- Payment processing
- Scalable infrastructure

**Technical:**
- [ ] Stripe integration ($12/user/mo)
- [ ] Billing management (add/remove seats)
- [ ] Usage limits (free tier: 50 tasks, paid: unlimited)
- [ ] Deployment (Railway/Render for auto-scaling)
- [ ] Monitoring (Sentry for errors, Plausible for analytics)
- [ ] Landing page + docs

**Outcome:** 10-20 paying teams (50-100 users, $500-1,200 MRR)

---

## Timeline: 10-14 Weeks to Beta Launch

**Month 1: Auth + Chat UI**
- Weeks 1-2: User auth
- Weeks 3-4: Chat interface
- **Milestone:** 5-10 solo beta users capturing tasks via chat

**Month 2: Team Features**
- Weeks 5-7: Shared projects + permissions
- Week 8: Analysis & recommendations
- **Milestone:** 2-3 teams testing (10-20 users)

**Month 3: Polish + Launch**
- Weeks 9-11: Stripe, deployment, monitoring
- Weeks 12-14: Beta launch (Product Hunt, GTD communities)
- **Milestone:** 5-10 paying teams ($500-1,200 MRR)

**Total effort:** 280-400 hours (10-15 hours/week pace)

---

## Why Teams Will Pay

### Individual Contributor: "GTD for Me"

**Pain:**
- Hate manual tagging/organizing
- Want LLM to do the thinking
- Need data-driven prioritization

**Value:**
- Save 30-60 min/day on GTD overhead
- Better focus (work on right things)

**Willingness to pay:** $8-15/mo (competes with Todoist/Things)

### Team Manager: "GTD for My Team"

**Pain:**
- Team uses different systems (spreadsheets, Notion, Asana, post-its)
- No visibility into what everyone's working on
- Can't track velocity or identify blockers
- Manual status updates waste time

**Value:**
- Team alignment (everyone in one system)
- Automatic velocity tracking
- Easy delegation (LLM helps assign tasks)
- Weekly insights ("What's blocked? What's overdue?")

**Willingness to pay:** $15-30/user/mo (competes with Asana/ClickUp)

### Consulting Firm: "GTD for Client Projects"

**Pain:**
- Managing multiple client projects
- Each consultant has their own system
- No firm-wide visibility
- Can't measure utilization or profitability per client

**Value:**
- Client-based project organization
- Time tracking → billing automation
- Portfolio view across all clients
- Partner/manager visibility

**Willingness to pay:** $30-50/user/mo (competes with Harvest/Productive)

**Key insight:** Team pricing is 2-4x individual pricing, same LLM costs

---

## Competitive Positioning for Teams

### vs. Asana/ClickUp (Project Management)

**They win on:**
- Rich features (Gantt, timelines, automations)
- Mature product (integrations, mobile apps)
- Enterprise-ready (SSO, compliance)

**You win on:**
- LLM interface (no manual data entry)
- GTD methodology (opinionated workflow)
- Simplicity (not overwhelming)
- Speed (capture → task in seconds)

**Target:** Teams who find Asana "too much" but Todoist "too little"

### vs. Motion/Reclaim.ai (AI Scheduling)

**They win on:**
- Calendar integration (auto-scheduling)
- Meeting optimization

**You win on:**
- Task management focus (they're calendar-first)
- GTD methodology (clear workflow)
- Team features (they're individual-focused)
- Capture interface (voice/chat, not forms)

**Target:** Teams who need task management + AI, not just calendar blocking

### vs. Todoist/Things (Individual GTD)

**They win on:**
- Individual user experience
- Native apps (iOS, Android)
- Offline mode

**You win on:**
- Team features (shared projects, delegation)
- LLM interface (no manual organizing)
- Analysis (data-driven prioritization)

**Target:** GTD teams who need collaboration

**Sweet spot:** **5-20 person teams who want GTD without the overhead**

---

## Pricing Strategy for Teams

### Tier 1: Individual ($12/mo)

**For:**
- Solo consultants
- Freelancers
- GTD practitioners

**Features:**
- Unlimited personal tasks
- LLM capture interface
- Weekly portfolio analysis
- Voice input
- Email integration

**Limit:** 1 user

### Tier 2: Team ($20/user/mo, min 3 users)

**For:**
- Small teams (3-10 people)
- Startups
- Consulting pods

**Features:**
- Everything in Individual
- Shared projects
- Task delegation
- Team velocity analytics
- Manager dashboard

**Minimum:** $60/mo (3 users)

### Tier 3: Business ($35/user/mo, min 10 users)

**For:**
- Consulting firms
- Agencies
- Departments

**Features:**
- Everything in Team
- Multiple teams/projects
- Client-based organization
- Time tracking
- Custom roles/permissions
- API access
- Priority support

**Minimum:** $350/mo (10 users)

**Revenue potential:**
- 10 teams x 5 users x $20 = $1,000/mo
- 5 teams x 10 users x $35 = $1,750/mo
- **Total: $2,750 MRR** with just 15 customers

---

## Go-to-Market: Team Focus

### Beachhead Market: Consulting Firms (Recommended)

**Why consultants:**
- You understand them (you're a consultant)
- They manage multiple client projects (pain is clear)
- They pay for tools ($20-35/user/mo is acceptable)
- WeRise case study is proof (you used GTD-LLM for client work)

**Target:**
- 3-10 person consulting firms
- Tech consultants, strategy consultants, fractional execs
- Solo → small team transition (growing, need systems)

**Message:**
- "GTD for consulting teams - capture client work via AI, track velocity per client, never lose a follow-up"

**Channels:**
- LinkedIn (target "Founder" + "Consulting")
- Consulting communities (r/consulting, Indie Consulting)
- Case study content (WeRise, showcase client project management)

### Alternative: Dev Teams (Good Second Target)

**Why developers:**
- Already use CLI/APIs (less onboarding)
- Familiar with AI tools (GitHub Copilot, Cursor)
- Need better task management (Jira is too heavy, Todoist too light)

**Target:**
- 5-15 person dev teams
- Startups, agencies, remote-first teams

**Message:**
- "GTD for dev teams - capture TODOs from code/Slack, LLM organizes automatically, integrate with GitHub"

**Channels:**
- Hacker News (Show HN)
- Dev communities (r/programming, dev.to)
- Product Hunt (tech audience)

### Strategy: Start with Consultants

**Phase 1 (Months 1-3):** Launch for individuals + consulting teams
- Build MVP (10-14 weeks)
- Target: 5-10 consulting firms (20-50 users)
- Learn: What features do they need?

**Phase 2 (Months 4-6):** Add dev team features
- GitHub integration (capture TODOs from commits)
- Slack integration (capture from channels)
- Target: 5-10 dev teams (25-75 users)

**Phase 3 (Months 7-12):** Expand to general teams
- More integrations (Notion, Asana import)
- Mobile apps
- Target: 20-30 teams total (100-200 users)

---

## Critical Success Factors

### 1. Nail the LLM Capture Experience

**User expectation:**
- "Call John about WeRise contract" → Task created
- No follow-up questions
- Inferred: Project (WeRise), Type (follow-up), Priority (normal)

**If this doesn't work smoothly:**
- Users will revert to manual entry
- Product has no differentiation
- Just becomes "another task manager"

**How to succeed:**
- Test prompts with 100+ real capture scenarios
- Fine-tune: When to ask clarifying questions vs. infer
- Show confidence: "I think this belongs in Project X (edit if wrong)"

### 2. Multi-User Without Chaos

**Challenge:**
- Shared project = potential conflicts
- Who can edit what?
- How to handle notifications?

**Solutions:**
- Clear ownership (each task has an owner)
- Simple permissions (owner/member, not 10 roles)
- Smart notifications (only when assigned or mentioned)
- Undo/history (if someone deletes by accident)

**How to succeed:**
- Test with real teams (not just beta testers)
- Watch for frustration points
- Iterate quickly (weekly deploys)

### 3. Pricing That Works

**Challenge:**
- Too cheap → can't cover LLM costs
- Too expensive → no one pays
- Free tier → abuse risk

**Sweet spot:**
- $20/user/mo for teams (75-80% gross margin after LLM costs)
- Free tier with strict limits (50 tasks max, 10 AI captures/month)
- Trial: 14 days, unlimited features (prove value fast)

**How to succeed:**
- Track unit economics from day 1
- Adjust pricing after 50-100 users (real data)
- Survey: "What would you pay for this?"

---

## Risks & Mitigations

### Risk 1: Building the Wrong Thing

**Scenario:** You build team features, but users want individual use

**Mitigation:**
- Launch Individual tier first (validate core LLM experience)
- Add team features only if 3+ users ask for it
- Keep both tiers (don't force team model)

### Risk 2: LLM Costs Explode

**Scenario:** Heavy users send 100+ messages/day, costs exceed revenue

**Mitigation:**
- Rate limits (10 LLM captures/hour for free, unlimited for paid)
- Prompt caching (reuse system prompts)
- Batch processing (queue tasks, process together)
- Monitor per-user costs (flag outliers)

### Risk 3: Vikunja Can't Scale

**Scenario:** Vikunja API is slow/unreliable at 100+ users

**Mitigation:**
- **Phase 1:** Use Vikunja (fast to market)
- **Phase 2:** Abstract storage layer (keep Vikunja as option)
- **Phase 3:** Build own task storage (SQLite/PostgreSQL)
- Keep Vikunja UI patterns (users won't notice backend change)

### Risk 4: Competition Moves Fast

**Scenario:** Todoist adds LLM capture, Motion adds GTD features

**Mitigation:**
- **Speed advantage:** Ship in 10-14 weeks (they take 6-12 months)
- **Focus advantage:** GTD-specific (they're general-purpose)
- **Data moat:** Learn from usage, personalize over time

**Accept:** You can't out-feature them. Compete on speed + focus.

### Risk 5: Can't Find Paying Customers

**Scenario:** People love the idea, but won't pay $20/mo

**Mitigation:**
- **Validation:** 50-100 waitlist signups before building
- **Early access:** Charge $99 lifetime deal (10-20 customers = validation)
- **Pivot:** If no one pays → Open source + consulting model

**Red flag:** If <5 people pay after 100 signups, reconsider

---

## Decision Framework: Should You Build This?

### ✅ Build if:

1. **Market validation:** 50+ waitlist signups in 2 weeks
2. **Time commitment:** You have 10-15 hours/week for 3-6 months
3. **Risk tolerance:** You're okay with $0-5K investment (hosting, tools, time)
4. **Complementary:** This feeds ivantohelpyou.com (leads, case studies, reputation)
5. **Enjoyable:** You actually want to build a product (not just consult)

### ❌ Don't build if:

1. **No validation:** Can't get 20+ waitlist signups
2. **No time:** Already overbooked with consulting
3. **No interest:** Would rather just use it yourself (perfectly valid!)
4. **Better opportunities:** Other projects with clearer ROI

### 🤔 Alternative: Open Source First

**Consider this:**
- Release on GitHub (MIT license)
- Write great docs
- Build community
- Offer paid support/hosting

**Benefits:**
- Lower commitment (community-driven)
- Reputation building (you're "the GTD-LLM expert")
- Consulting leads (enterprises want custom deployments)
- Option to commercialize later (if traction is strong)

**Revenue:**
- Consulting: $150-250/hr for custom GTD-LLM setups
- Support contracts: $500-2,000/mo for teams
- Workshops: $2,000-5,000 for training sessions

**This might be better fit if:**
- You prefer consulting to product
- You want leads for ivantohelpyou.com
- You're unsure about market demand

---

## Recommended Next Steps (30-Day Plan)

### Week 1: Validation

**Goal:** Confirm people will pay for this

**Actions:**
- [ ] Write landing page copy (30 min)
- [ ] Post in r/gtd: "LLM-powered GTD for teams - would you use this?" (15 min)
- [ ] Post in r/consulting: "How do you track client work?" (15 min)
- [ ] LinkedIn post: "I built GTD with AI - early access?" (15 min)
- [ ] Create Typeform waitlist: Name, email, team size, pain points (30 min)

**Success criteria:** 50+ waitlist signups OR 10+ "I'd pay for this" DMs

**Effort:** 2-3 hours

### Week 2: Technical Spike

**Goal:** Prove you can build the core experience

**Actions:**
- [ ] FastAPI hello world + user auth (2 hours)
- [ ] Simple chat UI (React) (3 hours)
- [ ] LLM prompt: "Create task" → YAML (1 hour)
- [ ] Integrate with your Vikunja instance (1 hour)
- [ ] Test with 3-5 capture scenarios (1 hour)

**Success criteria:** Can capture task via chat, creates in Vikunja

**Effort:** 8-10 hours

### Week 3: Beta Invites

**Goal:** Get real users testing

**Actions:**
- [ ] Invite top 10 waitlist signups (30 min)
- [ ] Onboarding doc: How to connect Vikunja (30 min)
- [ ] Weekly check-in: "What's working? What's broken?" (1 hour)
- [ ] Iterate on LLM prompts based on feedback (2 hours)

**Success criteria:** 3-5 daily active users, positive feedback

**Effort:** 4-6 hours + iteration

### Week 4: Decision Point

**If validation succeeded (50+ signups, 3-5 active beta users):**
- ✅ **GO:** Commit to 10-14 week roadmap
- Build out multi-user, shared projects, billing
- Target: Launch beta with pricing in 3 months

**If validation failed (<20 signups, no engagement):**
- 🔄 **PIVOT:** Open source + consulting model
- Release on GitHub, write blog post
- Offer consulting ($150-250/hr) for custom setups
- Generate leads for ivantohelpyou.com

**If uncertain (20-50 signups, some interest):**
- 🤔 **TEST PRICING:** Offer lifetime deal ($99-199)
- If 10+ people pay → GO (you have validated demand)
- If <5 people pay → PIVOT (not enough willingness to pay)

---

## Final Thought: The Meta Opportunity

**What you're really building:**

Not just "another task manager." You're building:

1. **A methodology** (GTD with LLM assistance)
2. **A case study** (WeRise shows it works)
3. **A platform** (others can use it)
4. **A consulting practice** (setup/training/support)
5. **A reputation** ("the GTD-LLM expert")

**Even if the product doesn't scale to $100K MRR:**
- You've systematized your own workflow (valuable!)
- You have a portfolio piece (credibility)
- You can consult on this (revenue)
- You can teach this (workshops/courses)
- You can write about this (content/SEO)

**The product is the smallest version of the opportunity.**

**The real opportunity is positioning yourself as the expert who solved GTD overhead with LLMs.**

---

**Next Action:** Post in r/gtd + r/consulting for validation
**Timeline:** 1 week
**Investment:** 2-3 hours
**Decision:** If 50+ signups → Build MVP, if not → Open source + consult

**Date:** November 9, 2025
**Status:** Ready for validation
