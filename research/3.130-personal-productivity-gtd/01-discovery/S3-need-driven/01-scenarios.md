# S3: Business Scenarios for Personal Productivity GTD

**Need-Driven Analysis**
**Date:** 2025-11-09

---

## Overview

This document presents 6 real-world scenarios showing how different user types should choose and implement GTD tools based on their specific needs, constraints, and workflows.

---

## Scenario 1: Solo Consultant / Freelancer

### Profile
- **Name:** Sarah, Management Consultant
- **Devices:** MacBook Pro (work), iPhone (personal)
- **Workload:** 3-5 client projects simultaneously, 30-50 active tasks
- **Needs:**
  - Track multiple client projects separately
  - Capture ideas during client meetings
  - Review weekly to ensure nothing falls through cracks
  - Professional appearance (clients sometimes see screen)
- **Budget:** $50-100/year acceptable (business expense)
- **Technical Skill:** Moderate (comfortable with apps, not developer)

### Recommended Solution: Things 3

**Why Things 3:**
1. **Apple ecosystem** matches her devices
2. **Beautiful interface** - professional when visible to clients
3. **Areas** for client separation (Client A, Client B, etc.)
4. **When dates** for scheduling client follow-ups
5. **Today view** for daily focus
6. **No subscription** - one-time $60 ($50 Mac + $10 iPhone)
7. **Offline-first** - works during flights to client sites

**Setup Guide:**

```
Areas (Clients):
- Client A Corp
- Client B LLC
- Client C Industries
- Business Development
- Personal

Projects (by Area):
Client A Corp:
  - Strategy Workshop Prep
  - Implementation Roadmap
  - Monthly Check-ins

Tags (Contexts):
- @computer (deep work)
- @phone (calls to clients)
- @meeting (in-person items)
- @waiting (delegated to clients)
- @email

Daily Workflow:
1. Morning: Review "Today" + add new items to Today
2. After meetings: Quick capture to Inbox via iPhone
3. Evening: Process Inbox, assign to projects/areas
4. Friday: Weekly review of each client area
```

**Cost Analysis:**
- Year 1: $60 (Mac $50 + iPhone $10)
- Years 2-5: $0
- **Total 5-year TCO: $60**

**Alternative if Windows Needed:**
If Sarah gets a Windows work laptop:
- **Switch to Todoist Pro** ($48/year)
- Cross-platform capability
- Natural language for quick capture
- **5-year TCO: $240**

---

## Scenario 2: Corporate Knowledge Worker

### Profile
- **Name:** Marcus, Product Manager at Tech Company
- **Devices:** Windows laptop (corporate), Android phone (personal)
- **Workload:** 50-100 tasks, 10+ projects, cross-functional collaboration
- **Needs:**
  - Works on Windows + Android (company won't buy Mac)
  - Quick capture during meetings
  - Integration with Outlook calendar
  - Share tasks with team occasionally
- **Budget:** Personal tool ($0-50/year), won't expense
- **Technical Skill:** High (developer background)

### Recommended Solution: Todoist Pro

**Why Todoist Pro:**
1. **Cross-platform** - Windows laptop + Android phone
2. **Natural language** - fast capture in meetings ("Follow up with engineering Friday at 2pm")
3. **Calendar integration** - see Outlook meetings + tasks
4. **Affordable** - $48/year personal expense
5. **AI assistant** (2025) - helps prioritize competing demands
6. **Team features** - can share specific projects with colleagues

**Setup Guide:**

```
Projects:
- Inbox
- Product Roadmap
- Engineering Coordination
- Marketing Collaboration
- Stakeholder Management
- 1:1 Meetings
- Personal

Labels (Contexts + Priorities):
- @computer
- @meeting
- @email
- @waiting_for
- High_Impact (custom filter)

Filters (Saved Views):
- Next Actions: no due date & !@waiting_for
- High Priority: (priority 1 | #High_Impact) & today
- Waiting For: @waiting_for
- This Week: due before: +7 days

Daily Workflow:
1. Morning: Check "Today" view + calendar
2. Meetings: Quick add via Android ("p Roadmap Follow up on API design @meeting")
3. Afternoon: Process inbox, use AI to prioritize
4. End of day: Review "This Week" filter
5. Friday: Review all projects
```

**Cost Analysis:**
- Year 1-5: $48/year
- **Total 5-year TCO: $240**

**Why Not Free Options:**
- **Notion Free:** Slower capture, not optimized for quick meetings
- **Obsidian:** Overkill, requires setup time Marcus doesn't have

**ROI Justification:**
- Marcus's salary: ~$120,000 (PM at tech company) = $57/hour
- Todoist saves 1 hour/month (conservative) = $684/year value
- $48 cost vs $684 value = **1,325% ROI**

---

## Scenario 3: Graduate Student / Researcher

### Profile
- **Name:** Priya, PhD Candidate
- **Devices:** Linux laptop (research), Android phone
- **Workload:** Research tasks, coursework, teaching duties, paper deadlines
- **Needs:**
  - Task management + extensive note-taking (research papers, ideas)
  - Link tasks to research notes
  - Free or very cheap (student budget)
  - Data ownership (academic work can't be in proprietary cloud)
- **Budget:** $0-20/year maximum
- **Technical Skill:** Very high (CS PhD student)

### Recommended Solution: Obsidian (Free)

**Why Obsidian:**
1. **Free** - critical for student budget
2. **Local markdown files** - owns her research data
3. **Tasks + notes unified** - research notes can contain tasks, tasks can link to notes
4. **Cross-platform** - Linux laptop + Android phone
5. **Git for sync** - free, version control for academic work
6. **Extensible** - can customize for research workflow

**Setup Guide:**

```
Vault Structure:
/Inbox.md
/Daily Notes/
/Research/
  Papers-to-Read.md
  Dissertation-Outline.md
  Experiment-Results.md
/Teaching/
  TA-Duties.md
  Office-Hours.md
/Projects/
  Dissertation.md
  Paper-NeurIPS.md
  Course-CS101.md
/Archive/

Plugins:
- Tasks (task management)
- Dataview (queries)
- Calendar (daily notes)
- Templater (templates)
- Git (version control + sync)

Task Format:
- [ ] Task description #context/lab #project/dissertation 📅 2025-11-15

Dataview Queries:
# Next Actions
\`\`\`dataview
TASK
WHERE !completed AND !contains(text, "waiting")
GROUP BY file.folder
\`\`\`

Daily Workflow:
1. Morning: Open daily note (template)
2. Research: Take notes in Obsidian, add tasks inline
3. Meetings: Quick capture to Inbox.md
4. Evening: Process inbox, update project notes
5. Sunday: Weekly review of all project notes
```

**Cost Analysis:**
- Year 1-5: $0 (free sync via Git)
- **Total 5-year TCO: $0**

**Alternative if Easier Setup Needed:**
- **Notion Free:** All-in-one workspace, easier than Obsidian
- Tradeoff: Proprietary format, cloud-dependent
- Still $0, but less data ownership

**Why Obsidian Over Notion for Priya:**
- Linux support (Notion web-only on Linux)
- Git version control (critical for dissertation work)
- Markdown = future-proof academic writing
- Can generate papers from same notes (Pandoc integration)

---

## Scenario 4: Apple Power User

### Profile
- **Name:** David, Graphic Designer
- **Devices:** iMac (studio), MacBook Pro (portable), iPad Pro (client meetings), iPhone
- **Workload:** 5-10 client projects, creative tasks, administrative work
- **Needs:**
  - Beautiful interface (aesthetic matters to designer)
  - Works across all Apple devices seamlessly
  - No subscription fatigue (already paying Adobe, Dropbox, etc.)
  - Simple but powerful
- **Budget:** Willing to pay upfront, hates recurring charges
- **Technical Skill:** Moderate

### Recommended Solution: Things 3 (All Devices)

**Why Things 3:**
1. **Award-winning design** - matches David's aesthetic standards
2. **All Apple devices** - iMac, MacBook, iPad, iPhone
3. **One-time purchase** - $80 total, no subscription
4. **Things Cloud sync** - free, automatic iCloud-based
5. **When/Deadline distinction** - critical for client deadlines vs work planning
6. **Handoff** - start task on iMac, continue on iPad at client site

**Setup Guide:**

```
Areas:
- Client Work
- Business Operations
- Personal
- Learning & Development

Projects (Client Work):
- Brand Identity - Acme Corp
- Website Redesign - XYZ LLC
- Print Collateral - Local Business

Projects (Business):
- Marketing & Outreach
- Portfolio Updates
- Administrative

Tags:
- @computer (design work)
- @ipad (client reviews)
- @email
- @errands
- @planning (creative planning)
- High-Energy (creative work)
- Low-Energy (admin work)

Daily Workflow:
1. Morning: iMac - Review "Today", drag tasks from "Anytime"
2. Client Meeting: iPad - Show project progress, capture feedback
3. Afternoon: iMac - Deep creative work on high-energy tasks
4. Evening: iPhone - Quick capture of ideas
5. Friday: Weekly review using "Upcoming" timeline view
```

**Cost Analysis:**
- Year 1: $80 (Mac $50 + iPhone $10 + iPad $20)
- Years 2-10: $0
- **Total 10-year TCO: $80**

**vs Subscription Alternative (Todoist):**
- Todoist Pro: $48/year × 10 years = $480
- **Things 3 saves $400 over 10 years**

**Psychological Value:**
- No subscription burden (David already stressed by Adobe $60/month)
- "Buy once, own forever" matches David's values
- Beautiful design daily joy (vs purely functional tool)

---

## Scenario 5: Privacy-Conscious Minimalist

### Profile
- **Name:** Elena, Writer & Privacy Advocate
- **Devices:** Linux laptop (primary), Android phone
- **Workload:** Writing projects, freelance articles, personal life
- **Needs:**
  - **Maximum privacy** - no cloud, local-first
  - Data ownership (writing is intellectual property)
  - Minimal subscriptions (digital minimalist philosophy)
  - Open source preferred
- **Budget:** $0 preferred, up to $50/year if necessary
- **Technical Skill:** High (comfortable with command line, Git)

### Recommended Solution: Obsidian + Self-Hosted Sync

**Why Obsidian:**
1. **Local markdown files** - never leaves her devices
2. **Open plugin ecosystem** - community-driven
3. **Free forever** - no subscription
4. **Git sync** - encrypted, self-hosted
5. **Writing + tasks unified** - drafts and to-dos in same system
6. **No vendor lock-in** - plain text, future-proof

**Setup Guide:**

```
Vault Structure:
/Inbox.md
/Writing/
  Novel-Draft.md
  Articles/
    Article-Privacy-Tech.md
/Projects/
  Book-Proposal.md
  Website-Redesign.md
/Reference/
  Research/
  Quotes.md
/Daily/
  2025-11-09.md

Sync Setup:
1. Git repository (private GitHub or self-hosted GitLab)
2. Automatic commits via Git plugin
3. Encrypted repository (git-crypt)
4. Syncthing (alternative: peer-to-peer sync, no central server)

Plugins:
- Tasks (task management)
- Dataview (queries)
- Git (version control)
- Templater (templates)
- Kanban (optional visual board)

Privacy Configuration:
- Disable telemetry
- Use self-hosted sync (Git or Syncthing)
- Encrypt vault (VeraCrypt container)
- No cloud services

Daily Workflow:
1. Morning: Open daily note, review tasks
2. Writing: Work in Writing/ folder, inline tasks for edits
3. Ideas: Quick capture to Inbox.md
4. Evening: Process inbox, commit to Git
5. Sunday: Review all project files
```

**Cost Analysis:**
- Year 1-10: $0 (free app, self-hosted sync)
- **Total 10-year TCO: $0**

**Privacy Advantages:**
- Data never touches third-party servers (Git self-hosted)
- Markdown = human-readable, no proprietary lock-in
- Can delete all copies, truly erase data
- No tracking, no telemetry, no user profiling

**Why Not Cloud Options:**
- **Todoist:** Cloud-dependent, user tracking
- **Notion:** Proprietary format, cloud-only, VC-funded (privacy risk)
- **Things 3:** iCloud (Apple access), not Linux-compatible

**Elena's Values Alignment:**
- Digital minimalism ✅ (one tool for notes + tasks)
- Privacy ✅ (local-first, encrypted)
- Open source ✅ (community plugins)
- No subscriptions ✅ (free forever)

---

## Scenario 6: Busy Parent + Professional

### Profile
- **Name:** Jason, Engineering Manager + Father of 2
- **Devices:** iPhone (primary), iPad (home), Work MacBook (locked down by IT)
- **Workload:**
  - Work: 40+ tasks, 5-7 projects, team management
  - Personal: Kids' schedules, household tasks, personal goals
- **Needs:**
  - Fast capture (kids interrupt constantly)
  - Separate work/personal clearly
  - Works on personal iPhone (can't install on work laptop)
  - Calendar integration (kids' activities + work meetings)
- **Budget:** $50-100/year acceptable
- **Technical Skill:** Moderate

### Recommended Solution: Things 3 (iPhone + iPad)

**Why Things 3:**
1. **iPhone-first** - primary device for capture
2. **Quick Entry** - capture in seconds during interruptions
3. **Areas** - separate Work vs Family clearly
4. **iPad at home** - review/planning on couch after kids sleep
5. **Calendar integration** - see kids' soccer games + work deadlines
6. **Widget** - glance at Today from home screen

**Setup Guide:**

```
Areas:
- Work (Engineering Team)
- Family
- Household
- Personal Growth

Projects (Work):
- Q4 Planning
- Team 1:1s
- Hiring Pipeline

Projects (Family):
- Kids School Events
- Weekend Activities
- Vacation Planning

Projects (Household):
- Home Maintenance
- Meal Planning
- Errands

Tags:
- @work (work hours only)
- @home
- @errands
- @weekend
- @kids
- Quick (< 5 min tasks for gaps)

Daily Workflow:
Morning (7am):
1. Check "Today" on iPhone while kids eat breakfast
2. Add any urgent work items

Workday:
3. Capture work tasks on iPhone (can't use work laptop)
4. Process during lunch break

Evening (8pm - kids asleep):
5. iPad - Weekly planning on couch
6. Review "Upcoming" for week ahead
7. Add family tasks for weekend

Sunday:
8. Full review of Work + Family areas
9. Plan upcoming week
```

**Cost Analysis:**
- Year 1: $30 (iPhone $10 + iPad $20)
- Years 2-5: $0
- **Total 5-year TCO: $30**

**Why Not Todoist:**
- Things 3: $30 one-time vs Todoist: $48/year × 5 = $240
- Things 3 saves $210 over 5 years
- iPhone widget better than Todoist for quick glance

**Work Laptop Constraint:**
- IT locks down work laptop (can't install apps)
- Things 3 on iPhone sufficient (always with him)
- Can access iCloud from personal iPad at home

**Family Benefit:**
- Share iPad with spouse (Family Sharing)
- Spouse can see "Family" area tasks
- One $30 purchase serves both parents

---

## Scenario Comparison Matrix

| Scenario | User | Tool | Cost (5yr) | Key Driver |
|----------|------|------|------------|------------|
| **Solo Consultant** | Sarah | Things 3 | $60 | Apple ecosystem, professional appearance |
| **Corporate PM** | Marcus | Todoist Pro | $240 | Cross-platform (Windows+Android) |
| **PhD Student** | Priya | Obsidian | $0 | Free, data ownership, Linux |
| **Designer** | David | Things 3 | $80 | Beautiful design, no subscription |
| **Privacy Advocate** | Elena | Obsidian | $0 | Privacy, local-first, open source |
| **Busy Parent** | Jason | Things 3 | $30 | iPhone-first, quick capture |

---

## Decision Framework

### Choose **Todoist Pro** if:
- ✅ Windows or Android devices (cross-platform required)
- ✅ Need natural language ("tomorrow at 3pm")
- ✅ Want AI assistant (2025 feature)
- ✅ Comfortable with $48/year subscription
- ✅ Value speed and integrations

**Scenarios:** Corporate PM, cross-platform consultant

### Choose **Things 3** if:
- ✅ All Apple devices (Mac, iPhone, iPad)
- ✅ Hate subscriptions (prefer one-time purchase)
- ✅ Value beautiful design
- ✅ Want when/deadline distinction
- ✅ Prefer simple, focused tool

**Scenarios:** Solo consultant (Apple), designer, busy parent

### Choose **Obsidian** if:
- ✅ Want free forever ($0 budget)
- ✅ Need tasks + extensive notes unified
- ✅ Value data ownership (markdown files)
- ✅ Privacy-conscious (local-first)
- ✅ Technical skill (comfortable with plugins)

**Scenarios:** PhD student, writer, privacy advocate

### Choose **OmniFocus** if:
- ✅ Serious GTD practitioner (read David Allen's book)
- ✅ Need Review Mode for weekly review discipline
- ✅ Want maximum power (custom perspectives)
- ✅ Apple ecosystem
- ✅ Willing to invest time learning

**Scenarios:** GTD expert, complex multi-project management

### Choose **Notion** if:
- ✅ Want all-in-one (tasks + notes + docs + wiki)
- ✅ Need collaboration features
- ✅ Value flexibility over speed
- ✅ Free tier adequate (personal use)

**Scenarios:** Team lead, content creator, startup founder

---

## Implementation Patterns

### Pattern 1: Quick Start (1-2 hours)
**Best for:** Todoist, Things 3
1. Download app
2. Create basic project structure
3. Add contexts/tags
4. Start capturing tasks
5. Refine over first week

**Users:** Busy professionals, parents, anyone needing immediate productivity

### Pattern 2: Template-Based (4-6 hours)
**Best for:** Notion
1. Find GTD template (community or paid)
2. Duplicate to your workspace
3. Customize fields/views
4. Learn database basics
5. Populate with current tasks

**Users:** Users wanting all-in-one workspace, comfortable with learning curve

### Pattern 3: DIY Build (10-15 hours)
**Best for:** Obsidian, OmniFocus
1. Study GTD methodology
2. Research optimal setup (forums, YouTube)
3. Configure plugins/perspectives
4. Build custom workflow
5. Iterate based on usage

**Users:** Technical users, customization enthusiasts, privacy-focused

---

## TCO Comparison by Scenario

| Scenario | Tool | 1 Year | 5 Years | 10 Years |
|----------|------|--------|---------|----------|
| **Solo Consultant** | Things 3 | $60 | $60 | $60 |
| **Corporate PM** | Todoist Pro | $48 | $240 | $480 |
| **PhD Student** | Obsidian | $0 | $0 | $0 |
| **Designer** | Things 3 | $80 | $80 | $80 |
| **Privacy Advocate** | Obsidian | $0 | $0 | $0 |
| **Busy Parent** | Things 3 | $30 | $30 | $30 |

**Insight:** One-time purchase (Things 3) and free tools (Obsidian) dominate long-term TCO.

---

## S3 Conclusions

### Key Insights

1. **Platform Determines Choice:**
   - Windows/Android → Todoist (only full-featured option)
   - Apple ecosystem → Things 3 or OmniFocus
   - Linux → Obsidian (only option)

2. **Budget Matters Less Than Expected:**
   - Free options (Obsidian) excellent for technical users
   - $30-80 one-time (Things 3) beats $48-100/year long-term
   - Even $100/year OmniFocus = $8.33/month (negligible for professionals)

3. **Use Case Trumps Features:**
   - Busy parent: iPhone-first (Things 3) beats more powerful tools
   - Privacy advocate: Local-first (Obsidian) non-negotiable
   - Corporate: Cross-platform (Todoist) mandatory

4. **Subscription Fatigue Real:**
   - Users with many subscriptions prefer Things 3 one-time
   - Digital minimalists prefer Obsidian free forever
   - Subscription-comfortable users fine with Todoist

5. **Technical Skill Gateway:**
   - Low-moderate skill: Todoist or Things 3 (plug-and-play)
   - High skill: Obsidian or OmniFocus (customizable)

### Implementation Success Factors

**Quick Adoption:**
- Choose tool matching devices/platform
- Start simple (10-15 projects maximum)
- Use templates/guides rather than building from scratch
- Commit to 2-week trial before judging

**Long-Term Success:**
- Weekly review habit (regardless of tool)
- Keep system simple (resist over-organizing)
- Capture everything (trust the system)
- Iterate quarterly (adjust based on usage)

---

## Next: S4 Strategic Analysis

S3 explored HOW different users should choose tools based on scenarios. S4 will analyze:

1. **Individual vs Team GTD** - When personal tools insufficient
2. **Ecosystem Lock-In** - Long-term risks and mitigation
3. **AI Integration Trajectory** - Future of AI-powered productivity
4. **Market Evolution** - Where is personal GTD heading?
5. **LLM-Powered GTD Opportunity** - Product gap for AI-first GTD

S4 will tie together findings from S1-S3 into strategic insights for:
- **Users:** Long-term tool selection strategy
- **Product builders:** Market opportunities and gaps
- **Investors:** Personal productivity market trends
