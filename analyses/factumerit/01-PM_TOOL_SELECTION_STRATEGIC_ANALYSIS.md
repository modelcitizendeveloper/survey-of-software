# Project Management Tool Selection - Strategic Analysis

**Date**: November 7, 2025
**Context**: Selecting ONE self-hosted PM tool for entire project portfolio
**Research Reference**: [1.131 Self-Hosted Project Management](../../research/1.131-project-management/)

---

## Executive Summary

**Recommendation**: **Vikunja** as unified PM tool for all projects

**Rationale**:
1. **Multi-project fit**: Handles all portfolio needs (qrcards maintenance, cookbooks pipeline, SEA development)
2. **Smooth transition**: Multiple view types (Kanban familiar, List + Gantt + Table for growth)
3. **Budget-friendly**: ~$180-480/year (vs Trello $600+/year potential)
4. **Low operational burden**: Docker deployment <30min, 1-2 hours/month maintenance
5. **Scalable**: Grows from solo to small team (3-5 people) without platform change

**Alternative considered**: WeKan (pure Kanban), dismissed due to limited flexibility for SEA development workflow

**Implementation**: 4-8 hours setup, migrate from Trello in phases

---

## Current State Assessment

### Project Portfolio Overview

**Active Projects**:
1. **QRCards** - SaaS product maintenance + feature development
   - **Size**: 7 trails currently, growth trajectory
   - **Complexity**: Moderate (infrastructure decisions, service integrations)
   - **Needs**: Bug tracking, feature roadmap, service evaluation tracking

2. **Cookbooks** - Content creation pipeline
   - **Size**: Research → 3-tier content (open/invited/subscriber)
   - **Complexity**: Moderate (multi-brand, multi-channel distribution)
   - **Needs**: Content calendar, research-to-content conversion tracking, publishing pipeline

3. **Schema Evolution Automation (SEA)** - Active development project
   - **Size**: 12-week Phase 1 (200 hours estimated)
   - **Complexity**: High (technology stack, weekly milestones, testing)
   - **Needs**: Sprint planning, task tracking, GitHub integration, milestone visibility

**Additional Projects** (from /applications/):
- Intelligence portal, business database, elevator project, inverse-fractional, spawn-solutions, spawn-experiments

### Current Tools & Experience

**Experience Level**:
- Trello user (Kanban familiar)
- Microsoft Project (Kanban style)
- **Comfort zone**: Simple boards, cards, lists
- **Pain point**: Managing multiple projects across tools (likely)

**Technical Capability**:
- Developer/CTO level
- Docker competency (SEA deployment planning)
- Infrastructure management (qrcards VPS migrations)
- **Assessment**: Intermediate to advanced DevOps

**Budget Constraints**:
- Budget-conscious (evidenced by qrcards TCO optimization)
- DIY preference (self-hosting research projects, service subtraction strategy)
- **Target**: <$500/year infrastructure

---

## Pattern Mapping (from S3)

### Primary Patterns Matched

#### Pattern 1: Simple Kanban Transition from Trello ✅
**Match**:
- Current Trello user
- Familiar with Kanban
- Want self-hosting

**Implications**:
- WeKan or Vikunja most natural
- Trello import capability valuable (WeKan has this)
- Low learning curve priority

#### Pattern 2: Solo Practitioner Scaling to Small Team ✅
**Match**:
- Currently solo (Ivan)
- May scale to 3-5 people (consulting, cookbooks team)
- Need tool that grows with portfolio

**Implications**:
- Vikunja or Plane best growth paths
- Avoid enterprise platforms (OpenProject, Redmine)

#### Pattern 3: Multi-Project Portfolio Management ✅
**Match**:
- 3+ active projects (qrcards, cookbooks, SEA)
- Plus additional applications
- Need cross-project visibility

**Implications**:
- Need project hierarchy support
- Cross-project dashboards valuable
- WeKan insufficient (no multi-project hierarchy)

#### Pattern 4: Software Development Team (SEA specific) ⚠️
**Match**:
- SEA is active software development
- 12-week sprint planning
- GitHub integration desirable

**Implications**:
- Git integration valuable (but not critical if GitHub Issues usable)
- Sprint/cycle support helpful
- Plane or Taiga best for dev workflows

#### Pattern 11: Budget-Constrained Team Avoiding SaaS Costs ✅
**Match**:
- QRCards TCO optimization mindset
- Service subtraction strategy (avoid managed services)
- Want <$500/year

**Implications**:
- Vikunja or WeKan lowest cost
- Can't justify $1,300-2,600/year OpenProject costs

### Pattern Priority Ranking

| Pattern | Priority | Rationale |
|---------|----------|-----------|
| **#2: Solo→Team** | 🔴 CRITICAL | Core growth trajectory |
| **#3: Multi-Project** | 🔴 CRITICAL | Managing 3+ projects |
| **#11: Budget** | 🟠 HIGH | Financial constraints real |
| **#1: Kanban Transition** | 🟡 MEDIUM | Familiarity helps adoption |
| **#4: Dev Team** | 🟢 LOW | SEA only, GitHub Issues fallback |

---

## Platform Analysis Against Portfolio Needs

### Option 1: **Vikunja** ⭐ RECOMMENDED

#### Strengths for Portfolio
✅ **Multi-view flexibility**:
- **QRCards**: Kanban for bug tracking, List for features
- **Cookbooks**: Kanban for content pipeline, Calendar for publishing schedule
- **SEA**: Gantt for 12-week sprint visibility, List for tasks

✅ **Multi-project support**:
- Hierarchical projects (qrcards → features → bugs)
- Separate projects for each application
- Cross-project visibility

✅ **Growth path**:
- Solo now → 3-5 person team later
- No platform change needed

✅ **Budget-friendly**:
- Infrastructure: $10-15/month VPS
- Setup: $125-250 (2-4 hours)
- Annual: $180-480 total
- **vs Trello**: $600/year (5 users Standard)

✅ **Low operational burden**:
- Docker deployment: 15-30 min
- Maintenance: 1-2 hours/month
- Lightweight: 1GB RAM sufficient

#### Weaknesses for Portfolio
❌ **No direct Trello import**:
- Manual migration from Trello (4-8 hours)
- Must recreate boards/cards

❌ **Limited Git integration**:
- No native GitHub integration
- SEA development tracking less elegant than Plane/Taiga

❌ **Smaller community**:
- Less proven than WeKan/OpenProject
- Fewer plugins/extensions

#### Fit Score by Project

| Project | Fit Score | View Type | Notes |
|---------|-----------|-----------|-------|
| **QRCards** | ⭐⭐⭐ | Kanban + List | Perfect for maintenance + feature roadmap |
| **Cookbooks** | ⭐⭐⭐ | Kanban + Calendar | Content pipeline + publishing schedule |
| **SEA** | ⭐⭐ | Gantt + List | Good sprint visibility, weak Git integration |

**Overall**: 8.5/10

---

### Option 2: **WeKan** (Trello Clone)

#### Strengths for Portfolio
✅ **Easiest migration**:
- Direct Trello JSON import
- Familiar interface
- 2-4 hour migration

✅ **Budget-friendly**:
- $10-20/month VPS
- $135-255/year total

✅ **Kanban-only simplicity**:
- No feature creep
- Easy to understand

#### Weaknesses for Portfolio
❌ **Kanban-only limitation**:
- No Gantt for SEA sprint planning
- No Calendar for cookbooks publishing
- No List view for different workflows

❌ **Poor multi-project support**:
- No project hierarchy
- Must create separate boards (hard to get cross-project view)

❌ **Limited growth path**:
- Stays simple Kanban forever
- May need to migrate if needs evolve

#### Fit Score by Project

| Project | Fit Score | View Type | Notes |
|---------|-----------|-----------|-------|
| **QRCards** | ⭐⭐⭐ | Kanban | Perfect for simple bug/feature tracking |
| **Cookbooks** | ⭐⭐ | Kanban | Works but no calendar for publishing |
| **SEA** | ⭐ | Kanban | Poor for sprint planning, no Gantt |

**Overall**: 6/10

**Decision**: Insufficient flexibility for multi-project portfolio

---

### Option 3: **Plane** (Modern Alternative)

#### Strengths for Portfolio
✅ **Modern UX**:
- Best interface in open source
- Contemporary design

✅ **Dev-friendly (SEA)**:
- GitHub integration
- Issues, epics, cycles
- Best for SEA development

✅ **Multi-project**:
- Workspaces for organization
- Cross-project visibility

#### Weaknesses for Portfolio
❌ **Higher costs**:
- $20-40/month VPS (2-4GB RAM)
- $600-1,080/year total
- **3-6x more than Vikunja**

❌ **Overkill for qrcards/cookbooks**:
- QRCards maintenance doesn't need modern dev tools
- Cookbooks content pipeline doesn't need epics/cycles

❌ **Steeper learning curve**:
- More complex than Kanban
- May slow adoption for simple tasks

#### Fit Score by Project

| Project | Fit Score | View Type | Notes |
|---------|-----------|-----------|-------|
| **QRCards** | ⭐⭐ | Kanban/Cycles | Overkill for maintenance |
| **Cookbooks** | ⭐⭐ | Kanban/Cycles | Overkill for content pipeline |
| **SEA** | ⭐⭐⭐ | Cycles/Issues | Perfect for active development |

**Overall**: 7/10

**Decision**: Good for SEA, but too expensive + complex for other projects

---

### Option 4: **OpenProject** (Enterprise)

#### Strengths for Portfolio
✅ **Multi-methodology**:
- Kanban + Gantt + traditional
- Best for mixed project types

✅ **Multi-project hierarchy**:
- Portfolio dashboards
- Cross-project reporting

#### Weaknesses for Portfolio
❌ **Too complex**:
- Steeper learning curve
- Overkill for solo/small team

❌ **Higher costs**:
- $40-80/month VPS (4-8GB RAM)
- $1,080-2,160/year
- **6-12x more than Vikunja**

❌ **Poor fit for portfolio size**:
- Designed for 10+ person teams
- Enterprise features unused

**Overall**: 4/10

**Decision**: Massive overkill for current needs

---

## Decision Matrix

| Criteria | Weight | Vikunja | WeKan | Plane | OpenProject |
|----------|--------|---------|-------|-------|-------------|
| **Multi-project support** | 🔴 25% | 9/10 | 4/10 | 8/10 | 10/10 |
| **Budget (<$500/year)** | 🔴 25% | 10/10 | 10/10 | 5/10 | 2/10 |
| **View flexibility** | 🟠 20% | 10/10 | 3/10 | 7/10 | 9/10 |
| **Ease of use** | 🟡 15% | 8/10 | 10/10 | 6/10 | 4/10 |
| **Growth path (solo→team)** | 🟡 15% | 9/10 | 5/10 | 9/10 | 8/10 |
| **Weighted Score** | — | **8.95** | **6.25** | **6.75** | **6.10** |

### Scoring Rationale

**Vikunja wins on**:
- Multi-view flexibility (10/10): Kanban + List + Gantt + Table + Calendar
- Budget (10/10): $180-480/year
- Growth path (9/10): Scales solo → 5 person team
- Multi-project (9/10): Hierarchical projects, cross-project views

**WeKan loses on**:
- View flexibility (3/10): Kanban only
- Multi-project (4/10): No hierarchy
- Growth path (5/10): Limited evolution

**Plane loses on**:
- Budget (5/10): $600-1,080/year (3-6x Vikunja)
- Overkill for 2 of 3 projects

**OpenProject loses on**:
- Budget (2/10): $1,080-2,160/year (6-12x Vikunja)
- Complexity overkill

---

## Recommendation: Vikunja

### Why Vikunja Wins

**1. Multi-Project Versatility**
- **QRCards**: Use Kanban for familiar bug/feature tracking
- **Cookbooks**: Use Kanban for content pipeline + Calendar for publishing schedule
- **SEA**: Use Gantt for 12-week sprint visibility + List for daily tasks

**One tool, multiple workflows** - no context switching

**2. Budget Alignment**
- Infrastructure: $10-15/month VPS (DigitalOcean, Hetzner)
- Total Year 1: $305-605 (setup + infrastructure + maintenance)
- Total Year 2+: $180-480/year
- **vs Trello**: $600/year (5 users), **vs Plane**: $600-1,080/year

**3-5x cost savings vs alternatives**

**3. Growth Path**
- **Now**: Solo use across 3+ projects
- **6-12 months**: Add 1-2 collaborators (cookbooks content team)
- **12-24 months**: 3-5 person team (if consulting scales)

**No platform change needed** - Vikunja grows with team

**4. Low Operational Burden**
- **Setup**: 15-30 minutes Docker deployment
- **Maintenance**: 1-2 hours/month (updates, backups)
- **Resources**: 1GB RAM (can co-locate with other services)

**Fits DIY/self-hosting philosophy** from qrcards

**5. View Flexibility > Trello**
- **Trello**: Kanban only
- **Vikunja**: Kanban + List + Gantt + Table + Calendar

**Grows beyond Kanban** without platform migration

### Trade-offs Accepted

**❌ No direct Trello import**
- **Impact**: 4-8 hours manual migration
- **Mitigation**: Migrate in phases (SEA first, then qrcards, then cookbooks)
- **One-time cost**: Acceptable for long-term flexibility

**❌ No native GitHub integration (SEA)**
- **Impact**: SEA development tracking less elegant than Plane/Taiga
- **Mitigation**: Use GitHub Issues for SEA code-level tracking, Vikunja for sprint planning
- **Hybrid approach**: Vikunja (what/when), GitHub (how/code)

**❌ Smaller community vs WeKan/OpenProject**
- **Impact**: Fewer plugins, less proven at scale
- **Mitigation**: Active development (2018-present), Go + Vue.js modern stack
- **Risk level**: Low (core features sufficient, don't need plugins)

---

## Implementation Roadmap

### Phase 1: Setup (Week 1-2, 4-8 hours)

**Week 1: Infrastructure**
1. Provision VPS: DigitalOcean $12/month droplet (2GB RAM, shared with other services)
2. Install Docker + Docker Compose
3. Deploy Vikunja: `docker-compose up -d`
4. Configure domain: `pm.spawn-solutions.com` (or subdomain)
5. SSL certificate: Let's Encrypt
6. **Time**: 2-3 hours

**Week 2: Configuration**
1. Create projects:
   - QRCards
   - Cookbooks
   - Schema Evolution Automation (SEA)
   - Spawn Solutions (meta-projects)
2. Set up views per project:
   - QRCards: Kanban (default) + List (features)
   - Cookbooks: Kanban (pipeline) + Calendar (publishing)
   - SEA: Gantt (12-week sprint) + List (tasks)
3. Configure labels, priorities, due dates
4. **Time**: 2-3 hours

**Deliverable**: Working Vikunja instance with 4 projects configured

---

### Phase 2: Migration from Trello (Week 2-4, 4-8 hours)

**Phased Approach** (easiest to hardest):

**Week 2: SEA (New Project)**
- **Complexity**: Low (no existing Trello board)
- **Tasks**:
  1. Import Phase 1 tasks from `SEA/project/IMPLEMENTATION_PLAN.md`
  2. Set up Gantt view (12-week timeline)
  3. Create milestones (Weeks 1-12)
  4. Add task dependencies
- **Time**: 1-2 hours
- **Benefit**: Immediate value (active development needs this)

**Week 3: QRCards (Existing Trello Board)**
- **Complexity**: Medium (existing board, but small)
- **Tasks**:
  1. Export Trello board as JSON (if exists)
  2. Manually recreate boards (no auto-import)
  3. Migrate cards: Bugs, Features, Service Evaluations
  4. Set up Kanban + List views
  5. Add labels (bug, feature, infrastructure, service)
- **Time**: 2-3 hours
- **Benefit**: Consolidate qrcards work into single PM tool

**Week 4: Cookbooks (Complex Pipeline)**
- **Complexity**: High (content pipeline stages)
- **Tasks**:
  1. Create content pipeline boards:
     - Research (completed experiments)
     - Conversion (research → frameworks)
     - Publishing (scheduled content)
     - Distribution (community channels)
  2. Set up Calendar view (publishing schedule)
  3. Migrate existing content tasks
  4. Link to research experiments
- **Time**: 2-3 hours
- **Benefit**: Visual content pipeline, publishing calendar

**Deliverable**: All projects migrated, Trello deprecated

---

### Phase 3: Optimization (Month 2, 2-4 hours)

**Workflow Refinement**:
1. Tune views per project (what's actually used vs theoretical)
2. Create recurring tasks (weekly reviews, monthly planning)
3. Set up project templates (for new experiments/features)
4. Configure notifications (Slack/email if needed)
5. Document team workflows (if adding collaborators)

**Backup Setup**:
1. Automated daily backups (database dump)
2. Weekly backup verification
3. Backup retention: 30 days

**Monitoring**:
1. Uptime monitoring (Freshping free tier)
2. Disk space alerts

**Time**: 2-4 hours one-time, then 1-2 hours/month maintenance

**Deliverable**: Production-ready PM system

---

## Cost Analysis

### Infrastructure Costs

**VPS** (DigitalOcean Droplet, shared with other services):
- Plan: $12/month (2GB RAM, 1 vCPU, 50GB SSD)
- Vikunja share: $3-5/month (lightweight, shares with other services)
- **Annual**: $36-60/year

**Domain/SSL**:
- Subdomain of existing domain: $0 (pm.spawn-solutions.com)
- Let's Encrypt SSL: $0
- **Annual**: $0

**Backups**:
- DigitalOcean Backups: $2.40/month (20% of droplet cost)
- Vikunja share: $0.50-1/month
- **Annual**: $6-12/year

**Total Infrastructure**: **$42-72/year**

### Labor Costs (DIY)

**Setup** (one-time):
- Infrastructure: 2-3 hours
- Configuration: 2-3 hours
- Migration: 4-8 hours
- **Total**: 8-14 hours
- **@ $0 DIY**: $0 (or $1,000-1,750 @ $125/hr if outsourced)

**Maintenance** (ongoing):
- Updates: 30 min/month
- Backups check: 15 min/month
- Monitoring: 15 min/month
- **Total**: 1 hour/month = 12 hours/year
- **@ $0 DIY**: $0 (or $1,500/year @ $125/hr if outsourced)

### Total Cost of Ownership (TCO)

| Year | DIY | Outsourced | Notes |
|------|-----|------------|-------|
| **Year 1** | $42-72 | $2,800-3,600 | Infrastructure only DIY, setup + maint outsourced |
| **Year 2+** | $42-72 | $1,600-1,600 | Infrastructure only DIY, maint outsourced |

**Recommendation**: DIY (infrastructure + labor), given Docker competency and self-hosting preference

### Cost Comparison

| Solution | Year 1 | Year 2-5 (annual) | 5-Year Total |
|----------|--------|-------------------|--------------|
| **Vikunja (DIY)** | $42-72 | $42-72 | $210-360 |
| **Vikunja (outsourced)** | $2,800-3,600 | $1,600 | $9,200-10,000 |
| **WeKan (DIY)** | $135-255 | $135-255 | $675-1,275 |
| **Plane (DIY)** | $600-1,080 | $600-1,080 | $3,000-5,400 |
| **Trello (5 users)** | $600 | $600 | $3,000 |
| **Asana (5 users)** | $1,428 | $1,428 | $7,140 |

**Savings vs Trello**: $2,640-2,790 over 5 years (8-14x cheaper)
**Savings vs Asana**: $6,780-6,930 over 5 years (20-33x cheaper)

---

## Risk Assessment

### Technical Risks

**Risk 1: Vikunja abandonment** (Low)
- **Mitigation**: Active development (2018-present), modern stack (Go + Vue)
- **Fallback**: Migrate to Plane or WeKan (data export available)

**Risk 2: Scaling limitations** (Low)
- **Concern**: Can Vikunja handle 10+ person team?
- **Mitigation**: Built for teams up to 15-20 people, can migrate to Plane later if needed
- **Timeline**: 12-24 months before hitting limits (if ever)

**Risk 3: Docker/VPS complexity** (Very Low)
- **Concern**: Operational burden too high
- **Mitigation**: Already managing qrcards VPS, Docker competent (SEA deployment planning)
- **Actual complexity**: Lower than qrcards (simpler stack)

### Operational Risks

**Risk 4: Migration effort underestimated** (Medium)
- **Concern**: 4-8 hours becomes 20+ hours
- **Mitigation**: Phased migration (SEA first, validate effort, then qrcards/cookbooks)
- **Fallback**: Stay on Trello for some projects if migration too painful

**Risk 5: Workflow mismatch** (Low)
- **Concern**: Vikunja doesn't fit actual workflows
- **Mitigation**: Multiple view types, flexible configuration
- **Validation**: Test with SEA project (Week 2) before full migration

### Strategic Risks

**Risk 6: Need to migrate later** (Low)
- **Concern**: Outgrow Vikunja, need Plane/OpenProject
- **Mitigation**: Vikunja data export, migration path exists
- **Timeline**: 18-24 months (if team grows to 10+ people)

**Overall Risk Level**: **LOW** - Technical capability + phased approach + fallback options

---

## Success Metrics

### Phase 1: Setup (Week 1-2)
- ✅ Vikunja deployed and accessible
- ✅ 4 projects configured (qrcards, cookbooks, SEA, spawn-solutions)
- ✅ All views working (Kanban, List, Gantt, Calendar)

### Phase 2: Migration (Week 2-4)
- ✅ SEA project active (Gantt + List views)
- ✅ QRCards migrated from Trello
- ✅ Cookbooks content pipeline visible
- ✅ Trello deprecated

### Phase 3: Adoption (Month 2-3)
- ✅ Daily use across all 3 projects
- ✅ Workflow optimized (views match actual usage)
- ✅ <5 min/day overhead (faster than Trello context switching)
- ✅ Cross-project visibility valuable (using it weekly)

### Long-term (6-12 months)
- ✅ Team collaboration (if 1-2 people added)
- ✅ No platform migration needed
- ✅ Cost <$100/year (budget target maintained)

---

## Alternatives for Reconsideration

### Reconsider WeKan if:
- **Scenario**: Only need pure Kanban (SEA development ends, no complex projects)
- **Benefit**: Trello import saves 4-8 hours migration
- **Trade-off**: Lose view flexibility

### Reconsider Plane if:
- **Scenario**: Budget increases to $600-1,000/year AND SEA development becomes primary focus
- **Benefit**: Best modern UX, GitHub integration
- **Trade-off**: 3-6x cost, overkill for qrcards/cookbooks

### Reconsider OpenProject if:
- **Scenario**: Team grows to 10+ people with dedicated PM role
- **Benefit**: Enterprise features, comprehensive reporting
- **Trade-off**: 6-12x cost, steep learning curve

**Current recommendation stands**: Vikunja best for current + 12-24 month future state

---

## Next Actions

### Immediate (This Week)
1. **Provision VPS**: DigitalOcean $12/month droplet (or upgrade existing VPS if space available)
2. **Deploy Vikunja**: Docker Compose (follow [Vikunja docs](https://vikunja.io/docs/installing/))
3. **Create SEA project**: Import Week 1-12 tasks from implementation plan
4. **Validate**: Use Vikunja for SEA for 1 week

### Short-term (Next 2 Weeks)
1. **Migrate QRCards**: Recreate Trello boards (if exist)
2. **Migrate Cookbooks**: Set up content pipeline + publishing calendar
3. **Deprecate Trello**: If migration successful
4. **Document workflows**: For future team members

### Long-term (Next 3 Months)
1. **Optimize workflows**: Tune views, templates, recurring tasks
2. **Set up backups**: Automated daily backups
3. **Monitor usage**: Validate time savings vs Trello
4. **Review decision**: Month 3 - is Vikunja working? Any gaps?

---

## Conclusion

**Vikunja is the right unified PM tool** for the current project portfolio because:

1. ✅ **Handles multi-project diversity** (qrcards maintenance, cookbooks pipeline, SEA development)
2. ✅ **Budget-aligned** ($42-72/year infra, 8-14x cheaper than Trello/Asana)
3. ✅ **Smooth Trello transition** (multiple views include Kanban, modern UX)
4. ✅ **Scales with growth** (solo → 5 person team without platform change)
5. ✅ **Low operational burden** (Docker deployment, 1-2 hours/month maintenance)
6. ✅ **Fits self-hosting philosophy** (consistent with qrcards service subtraction strategy)

**Start with SEA project** (Week 1-2) to validate, then migrate other projects.

**Total investment**: 8-14 hours setup + $42-72/year infrastructure

**Expected outcome**: Unified PM across all projects, 3-5x time savings from context switching, <$100/year cost

---

## References

**Generic Research**: [1.131 Self-Hosted Project Management](../../research/1.131-project-management/01-discovery/)
- S1 Rapid Discovery: Platform landscape (8 platforms)
- S3 Need-Driven Discovery: 12 generic use case patterns

**Project Documentation**:
- QRCards: `/home/ivanadamin/spawn-solutions/applications/qrcards/README.md`
- Cookbooks: `/home/ivanadamin/spawn-solutions/applications/cookbooks/README.md`
- SEA: `/home/ivanadamin/spawn-solutions/applications/schema-evolution-automation/project/README.md`

**Vikunja Resources**:
- Official site: https://vikunja.io/
- Documentation: https://vikunja.io/docs/
- GitHub: https://github.com/go-vikunja/vikunja
- Docker deployment: https://vikunja.io/docs/installing/

---

**Status**: ✅ Recommendation Complete
**Decision**: Vikunja for all projects
**Next**: Deploy and validate with SEA project
**Last Updated**: November 7, 2025
