# GTD & Project Management Research Categories
## Proposed additions to spawn-solutions research roadmap

**Context:** Product opportunity assessment for LLM-powered GTD interface built on Vikunja

**Goal:** Map competitive landscape systematically using S1-S4 MPSE methodology

---

## Proposed New Categories

### Tier 1: Open Source / Self-Hosted (1.xxx range)

**1.130 - Task Management Libraries**
- **Scope:** Open source task/todo libraries and data structures
- **Examples:** Python task queue libraries, to-do list data structures, task scheduling algorithms
- **Value:** DIY foundation for custom task management
- **Estimated hours:** 4-6 hours
- **Status:** Not started

**1.131 - Project Management** ✅ **COMPLETED**
- Vikunja integration suite (API wrapper, populate, export)
- GTD workflow documentation
- OODA loop integration

**1.132 - Self-hosted Collaboration** (already in PLANNED-RESEARCH.yaml)
- Nextcloud, Mattermost, Rocket.Chat, Zulip
- Team communication platforms

**1.133 - Self-hosted Documentation** (already in PLANNED-RESEARCH.yaml)
- BookStack, Wiki.js, Outline, Docusaurus
- Knowledge management platforms

### Tier 3: Managed Services (3.xxx range)

**3.130 - Personal Productivity Tools (GTD)**
- **Scope:** Individual task management and GTD methodology tools
- **S1 targets:** Todoist, Things 3, OmniFocus, Notion (personal use), Obsidian, Bear
- **S2 deep dive:** Feature comparison, GTD methodology support, pricing, mobile apps
- **S3 need-driven:** "GTD for solo practitioners", "Personal task management with AI"
- **S4 strategic:** Individual vs team focus, open vs closed ecosystems, AI integration
- **Why this matters:** Direct competitors for individual tier of LLM-GTD product
- **Estimated hours:** 8-10 hours
- **Priority:** **HIGH** - core competitive analysis

**3.131 - Team Task Management**
- **Scope:** Small team task management (3-20 people)
- **S1 targets:** Asana (team tier), ClickUp, Monday.com, Airtable, Trello, Linear
- **S2 deep dive:** Team collaboration features, permission models, pricing per seat
- **S3 need-driven:** "Task management for consulting teams", "Dev team task tracking"
- **S4 strategic:** PM vs task management positioning, integration ecosystems
- **Why this matters:** Competitors for team tier of LLM-GTD product
- **Estimated hours:** 10-12 hours
- **Priority:** **HIGH** - team product opportunity

**3.132 - Enterprise Project Management**
- **Scope:** Full-featured PM platforms (20+ users, enterprise features)
- **S1 targets:** Jira, Microsoft Project, Smartsheet, Wrike, Workfront, Basecamp
- **S2 deep dive:** Enterprise features (SSO, compliance, reporting), pricing, customization
- **S3 need-driven:** "Enterprise project portfolio management", "Scaled agile frameworks"
- **S4 strategic:** Enterprise sales model, lock-in risks, self-hosted options
- **Why this matters:** Understand upmarket opportunity / competitive threats
- **Estimated hours:** 12-15 hours
- **Priority:** MEDIUM - future expansion opportunity

**3.133 - AI-Powered Productivity**
- **Scope:** AI-first productivity tools and assistants
- **S1 targets:** Motion, Reclaim.ai, Trevor AI, Akiflow, Sunsama, Amie
- **S2 deep dive:** AI features (scheduling, prioritization, suggestions), LLM usage, pricing
- **S3 need-driven:** "AI task management", "Automated scheduling with AI"
- **S4 strategic:** LLM API costs, AI feature differentiation, user trust in AI
- **Why this matters:** **DIRECT competitors** - AI-native productivity tools
- **Estimated hours:** 8-10 hours
- **Priority:** **CRITICAL** - these are closest competitors to LLM-GTD concept

**3.134 - Collaboration & Workspace Platforms**
- **Scope:** All-in-one workspace tools (task + docs + communication)
- **S1 targets:** Notion, Coda, ClickUp (full suite), Monday.com (full suite), Airtable
- **S2 deep dive:** Workspace features, extensibility, database capabilities
- **S3 need-driven:** "All-in-one workspace for teams", "Collaborative knowledge base"
- **S4 strategic:** Platform vs point solution, feature creep risks, pricing complexity
- **Why this matters:** Competitors offering task management as part of larger platform
- **Estimated hours:** 10-12 hours
- **Priority:** MEDIUM - adjacent competitors

**3.135 - Knowledge Management & Note-Taking**
- **Scope:** Note-taking and personal knowledge management
- **S1 targets:** Obsidian, Roam Research, Logseq, Notion (notes), Evernote, OneNote
- **S2 deep dive:** Linking/graph features, sync, markdown support, extensibility
- **S3 need-driven:** "Personal knowledge management", "Zettelkasten implementation"
- **S4 strategic:** Notes vs tasks boundary, local-first vs cloud, graph databases
- **Why this matters:** Overlap with GTD "reference" material, integration opportunity
- **Estimated hours:** 6-8 hours
- **Priority:** LOW - adjacent space, potential integration

**3.136 - Time Tracking & Productivity Analytics**
- **Scope:** Time tracking and productivity measurement tools
- **S1 targets:** RescueTime, Toggl, Clockify, Harvest, Timely, Timing
- **S2 deep dive:** Automatic tracking, billing features, team analytics
- **S3 need-driven:** "Automatic time tracking", "Consultant billing integration"
- **S4 strategic:** Privacy concerns, billing vs analytics focus
- **Why this matters:** Integration opportunity (track time on tasks), velocity measurement
- **Estimated hours:** 6-8 hours
- **Priority:** LOW - feature addition opportunity

---

## Research Execution Priority

### Phase 1: Core Competitive Analysis (20-24 hours, Week 1-2)

**Must do before building product:**

1. **3.133 - AI-Powered Productivity** (8-10 hours) - CRITICAL
   - Motion, Reclaim.ai, Trevor AI
   - What AI features do they have?
   - How are they positioning AI?
   - What's their pricing?
   - **Output:** Understand direct AI-native competitors

2. **3.130 - Personal Productivity (GTD)** (8-10 hours) - HIGH
   - Todoist, Things, OmniFocus
   - What GTD features exist?
   - How do they handle capture/organize?
   - **Output:** Feature gap analysis for individual tier

3. **3.131 - Team Task Management** (4-6 hours, S1 only) - HIGH
   - Asana, ClickUp, Linear
   - Team features overview
   - Pricing models
   - **Output:** Understand team tier competitive landscape

### Phase 2: Strategic Analysis (10-12 hours, Week 3-4)

**If GO decision on product:**

4. **3.131 - Team Task Management** (6-8 hours, S2-S4) - HIGH
   - Deep dive on team features
   - Permission models
   - Integration ecosystems
   - **Output:** Feature roadmap for team tier

5. **3.134 - Collaboration Platforms** (4-6 hours, S1-S2) - MEDIUM
   - Notion, Coda overview
   - Platform vs point solution
   - **Output:** Positioning strategy

### Phase 3: Expansion Research (12-18 hours, Month 2-3)

**If product gains traction:**

6. **3.132 - Enterprise PM** (8-10 hours)
7. **3.135 - Knowledge Management** (4-6 hours)
8. **3.136 - Time Tracking** (4-6 hours)

---

## Integration with spawn-analysis

**After research Phase 1:**

1. **Export portfolio state** (your current Vikunja portfolio)
2. **Run decision cards:**
   - The Strategist: Does this align with long-term positioning?
   - Capability Auditor: Do I have capacity to build this? (reality check)
   - Optimizer: ROI analysis (product vs consulting)
   - Economizer: What's the minimum viable version?
   - Experience-Based: What have I learned from past projects?
3. **Decision:** GO / PIVOT to consulting / DEFER

---

## Numbering Rationale

### Why 3.130-3.136?

Looking at existing 3.xxx categories:
- **3.100-3.199:** Content & Collaboration
  - 3.100 CMS (exists in PLANNED-RESEARCH)
  - 3.130-3.136: **Productivity & Collaboration** (new cluster)
- **3.200-3.299:** AI Services
  - 3.200 LLM APIs (exists)
  - 3.201 Computer Vision (in PLANNED-RESEARCH)
  - 3.202 Speech & Audio (in PLANNED-RESEARCH)
- **3.300-3.399:** Developer Tools
  - 3.300 Feature Flags (in PLANNED-RESEARCH)
  - 3.301 API Management (in PLANNED-RESEARCH)
- **3.400-3.499:** Backend/Infrastructure
  - 3.400 BaaS (exists)
  - 3.401 E-Commerce (in PLANNED-RESEARCH)
  - 3.402 Integration Platforms (in PLANNED-RESEARCH)
- **3.500-3.599:** Business Applications
  - 3.501 CRM (exists)
  - 3.502 ERP (exists)
  - 3.503 HRIS (exists)

**Proposal:** Create **3.130-3.139 as "Productivity & Collaboration" cluster**

---

## Next Actions

1. **Add to PLANNED-RESEARCH.yaml** (5 min)
   - 3.130 through 3.136
   - Plus 1.130

2. **Add to RESEARCH-PRIORITIES.yaml** (5 min)
   - Priority order: 3.133 → 3.130 → 3.131

3. **Create research directories** (10 min)
   ```bash
   mkdir -p research/3.130-personal-productivity-gtd
   mkdir -p research/3.131-team-task-management
   mkdir -p research/3.132-enterprise-project-management
   mkdir -p research/3.133-ai-powered-productivity
   mkdir -p research/3.134-collaboration-platforms
   mkdir -p research/3.135-knowledge-management
   mkdir -p research/3.136-time-tracking-analytics
   mkdir -p research/1.130-task-management-libraries
   ```

4. **Run S1 on 3.133 AI-Powered Productivity** (2-3 hours)
   - Start with closest competitors
   - Motion, Reclaim.ai, Trevor AI, Akiflow

5. **Decision:** After 3.133 + 3.130 research, run spawn-analysis

---

**Status:** Proposal ready for review
**Date:** 2025-11-09
**Next:** Add to PLANNED-RESEARCH.yaml and RESEARCH-PRIORITIES.yaml
