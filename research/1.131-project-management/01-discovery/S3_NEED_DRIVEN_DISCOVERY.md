# 1.131: Self-Hosted Project Management Platforms - S3 Need-Driven Discovery

**Research Date**: November 7, 2025
**Category**: 1.130-139 Business Application Platforms (Self-Hosted)
**Methodology**: MPSE S3 (Need-Driven Discovery - Generic Use Case Patterns)

## Document Purpose

This document provides **generic use case PATTERNS** for selecting self-hosted project management platforms. These are parameterized patterns that ANY team can map their situation to - not specific recommendations.

**Hardware Store Model**: This is the catalog of "what tool for what job." Application-specific analysis belongs in `applications/{app}/`.

---

## Pattern Index

1. [Simple Kanban Transition from Trello](#pattern-1-simple-kanban-transition-from-trello)
2. [Solo Practitioner Scaling to Small Team](#pattern-2-solo-practitioner-scaling-to-small-team)
3. [Multi-Project Portfolio Management](#pattern-3-multi-project-portfolio-management)
4. [Software Development Team with Git Integration](#pattern-4-software-development-team-with-git-integration)
5. [Small Team with Limited DevOps Capability](#pattern-5-small-team-with-limited-devops-capability)
6. [Scaling Beyond Basic Boards](#pattern-6-scaling-beyond-basic-boards)
7. [Mixed Methodology Requirements](#pattern-7-mixed-methodology-requirements)
8. [Agency Managing Multiple Client Projects](#pattern-8-agency-managing-multiple-client-projects)
9. [Enterprise with Compliance Requirements](#pattern-9-enterprise-with-compliance-requirements)
10. [Technical Team Needing Deep Customization](#pattern-10-technical-team-needing-deep-customization)
11. [Budget-Constrained Team Avoiding SaaS Costs](#pattern-11-budget-constrained-team-avoiding-saas-costs)
12. [Modern UX Expectations (Linear/Notion Style)](#pattern-12-modern-ux-expectations-linearnotion-style)

---

## Pattern 1: Simple Kanban Transition from Trello

### Team Characteristics
- **Size**: 1-10 people
- **Current Tool**: Trello (or similar simple Kanban)
- **Skills**: Basic tech literacy, minimal DevOps
- **Budget**: $0-100/month
- **Pain Points**: Trello costs ($5-17.50/user/month), data ownership concerns, need self-hosting

### Project Characteristics
- **Count**: 1-5 active projects
- **Complexity**: Low to moderate
- **Methodology**: Pure Kanban (boards, lists, cards)
- **Features Needed**: Drag-drop, labels, due dates, attachments, basic checklists
- **Features NOT Needed**: Gantt charts, resource management, time tracking, complex workflows

### Platform Recommendations

#### Primary Option: **WeKan**
**Why**:
- Closest Trello clone (direct import from Trello)
- MIT license (permissive)
- Swimlanes (Trello lacks this)
- Lightweight (1-2GB RAM)
- 60 language support
- GDPR-compliant when self-hosted

**Trade-offs**:
- ✅ Familiar Trello-like interface
- ✅ Easiest migration path (Trello JSON import)
- ✅ No Docker expertise required (can run on simple VPS)
- ❌ Limited to Kanban (no Gantt, no Scrum sprints)
- ❌ Smaller feature set than full PM platforms
- ❌ Meteor.js stack may be unfamiliar

**Deployment**:
- Docker: 15-30 minutes
- Infrastructure: $10-20/month VPS (DigitalOcean, Linode)
- Maintenance: 1-2 hours/month

**Breakeven vs Trello**: 2-4 users (Trello Standard $5/user = $120-240/year for 2-4 users)

#### Alternative Option: **Vikunja**
**Why**:
- Multiple view types (List, Kanban, Gantt, Table)
- Very lightweight (Raspberry Pi capable)
- Modern Go + Vue.js stack
- Simple Docker deployment

**Trade-offs**:
- ✅ More view flexibility than WeKan
- ✅ Extremely lightweight
- ✅ Modern tech stack
- ❌ Less Trello-like (steeper learning curve for Trello users)
- ❌ No direct Trello import
- ❌ More task-focused than project-focused

**When to choose Vikunja over WeKan**:
- Want multiple view types (not just Kanban)
- Need very lightweight deployment
- Prefer modern tech stack (Go/Vue vs Meteor)
- Okay with manual migration from Trello

#### Alternative Option: **Focalboard**
**Why**:
- Backed by Mattermost (enterprise chat platform)
- MIT license
- Notion-like flexibility (Kanban, table, gallery, calendar views)
- React + Go stack

**Trade-offs**:
- ✅ Notion-like flexibility
- ✅ Multiple view types
- ✅ Modern stack
- ❌ Best value when paired with Mattermost (added complexity)
- ❌ Less mature than WeKan (launched 2021)
- ❌ No Trello import

**When to choose Focalboard over WeKan**:
- Already using or planning to use Mattermost
- Want Notion-like flexibility beyond Kanban
- Prefer React + Go stack

### Decision Criteria

**Choose WeKan if**:
- Pure Kanban is sufficient
- Want easiest migration from Trello
- Familiar interface is priority
- Team is non-technical

**Choose Vikunja if**:
- Want multiple view types (Kanban + List + Gantt)
- Need very lightweight deployment
- Modern tech stack preferred

**Choose Focalboard if**:
- Using/planning Mattermost
- Want Notion-like flexibility
- React + Go stack familiar

### Migration Path

**From Trello to WeKan**:
1. Export Trello board as JSON
2. Deploy WeKan via Docker
3. Import Trello JSON into WeKan
4. Verify cards, labels, attachments
5. Train team on WeKan (1-2 hours, very similar to Trello)

**Estimated Migration Time**: 4-8 hours

**Migration Risks**:
- Custom Power-Ups from Trello won't migrate
- Some formatting may need adjustment
- Automations must be recreated (Butler → WeKan Triggers)

### Cost Comparison

| Solution | Setup Cost | Monthly Cost | Annual Cost | 3-Year Total |
|----------|------------|--------------|-------------|--------------|
| Trello (5 users, Standard) | $0 | $25 | $300 | $900 |
| WeKan self-hosted | $125-250 (2-4 hrs setup) | $10-20 (VPS) | $120-240 | $485-970 |
| Vikunja self-hosted | $125-250 | $10-15 (VPS) | $120-180 | $485-790 |

**Breakeven**: 1-2 years for self-hosted vs Trello Standard

---

## Pattern 2: Solo Practitioner Scaling to Small Team

### Team Characteristics
- **Current Size**: 1 person
- **Growth Trajectory**: 1 → 3-5 people over 12-24 months
- **Current Tool**: Personal task list, Notion, or nothing formal
- **Skills**: Technical proficiency (developer, designer, consultant)
- **Budget**: Minimal ($0-50/month)

### Project Characteristics
- **Count**: 3-10 active projects (personal + client work)
- **Complexity**: Low to moderate (solo work, small deliverables)
- **Methodology**: Flexible (task lists now, may need Kanban/sprints later)
- **Features Needed**: Task lists, due dates, hierarchical projects
- **Future Needs**: Collaboration, team assignments, client project separation

### Platform Recommendations

#### Primary Option: **Vikunja**
**Why**:
- Scales from personal use to small team
- Multiple view types (start with lists, add Kanban/Gantt later)
- Very lightweight (can run on existing server/Raspberry Pi)
- Free and open source
- Simple Docker deployment

**Growth Path**:
- **Month 1-6** (solo): Use as personal task manager
- **Month 6-12** (1-2 people): Share projects, assign tasks
- **Month 12-24** (3-5 people): Use team collaboration features, project hierarchies

**Trade-offs**:
- ✅ Grows with you (personal → team)
- ✅ Multiple view types
- ✅ Very low cost ($10-15/month VPS)
- ❌ Less feature-rich than full PM platforms (no resource management, limited reporting)
- ❌ May need to migrate later if team grows beyond 10-15 people

#### Alternative Option: **Plane**
**Why**:
- Modern interface
- Designed for technical teams
- AI-assisted planning
- Scales from small to medium teams (10-50+)

**Trade-offs**:
- ✅ Better for larger team growth (10-50+ people)
- ✅ Modern UX
- ✅ AI features
- ❌ Overkill for solo use initially
- ❌ Higher resource requirements (2-4GB RAM)
- ❌ More complexity than needed for solo practitioner

**When to choose Plane over Vikunja**:
- Expect rapid growth to 10+ person team
- Technical team (developers, designers)
- Value modern UX and AI features
- Can handle higher infrastructure costs

### Decision Criteria

**Choose Vikunja if**:
- Solo now, slow growth to 3-5 people
- Budget-conscious ($10-15/month)
- Need lightweight deployment
- Task management > project management

**Choose Plane if**:
- Expect rapid growth to 10+ person technical team
- Value modern UX
- Can handle $20-40/month infrastructure costs
- Project management > task management

### Cost Comparison

| Solution | Setup Cost | Monthly Cost (Solo) | Monthly Cost (5 people) | 3-Year Total (5 people) |
|----------|------------|---------------------|-------------------------|-------------------------|
| Vikunja | $125 (2 hrs) | $10-15 | $15-20 | $665-845 |
| Plane | $250 (4 hrs) | $20-30 | $30-40 | $1,330-1,690 |
| Asana (reference) | $0 | $0 (free tier) | $54 (Premium) | $1,944 |

---

## Pattern 3: Multi-Project Portfolio Management

### Team Characteristics
- **Size**: 3-15 people
- **Structure**: Managing 5-20 concurrent projects
- **Skills**: Intermediate technical capability
- **Budget**: $50-200/month
- **Pain Point**: Need project hierarchy, cross-project visibility, resource allocation

### Project Characteristics
- **Count**: 5-20 active projects simultaneously
- **Complexity**: Moderate to high
- **Methodology**: Mixed (some Kanban, some waterfall, some ad-hoc)
- **Features Needed**:
  - Project/subproject hierarchy
  - Cross-project dashboards
  - Resource allocation visibility
  - Portfolio-level reporting
  - Multi-project search

### Platform Recommendations

#### Primary Option: **OpenProject**
**Why**:
- Designed for multi-project management
- Project hierarchy (projects + subprojects)
- Portfolio dashboards
- Free Community edition (unlimited projects)
- Gantt charts for waterfall projects
- Boards for agile projects

**Trade-offs**:
- ✅ Best multi-project support in open source
- ✅ Free Community edition very capable
- ✅ Mixed methodology support (Kanban + Gantt + traditional)
- ✅ Cross-project reporting
- ❌ Steeper learning curve
- ❌ Higher resource requirements (4-8GB RAM)
- ❌ More complex deployment

**Deployment**:
- Docker: 1-2 hours
- Infrastructure: $40-80/month VPS
- Maintenance: 3-5 hours/month

#### Alternative Option: **Redmine**
**Why**:
- Mature multi-project hierarchy (19 years old)
- Subproject nesting
- Cross-project issues
- Vast plugin ecosystem for custom needs

**Trade-offs**:
- ✅ Very mature multi-project support
- ✅ Extremely customizable via plugins
- ✅ Cross-project features well-developed
- ❌ Dated UI/UX
- ❌ Requires Ruby on Rails expertise
- ❌ Complex deployment (4+ hours)

**When to choose Redmine over OpenProject**:
- Have Ruby on Rails expertise
- Need vast plugin ecosystem
- Legacy integrations important
- Okay with dated UI for functionality

#### Alternative Option: **Plane**
**Why**:
- Modern multi-project support
- Workspaces for project organization
- Cross-project visibility

**Trade-offs**:
- ✅ Modern UX
- ✅ Simpler deployment than OpenProject
- ❌ Newer platform (less proven for large portfolios)
- ❌ Less robust hierarchy than OpenProject/Redmine
- ❌ Limited portfolio reporting

**When to choose Plane over OpenProject**:
- UX is priority over feature depth
- Portfolio < 10 projects
- Team is technical (developers)
- Modern stack preferred

### Decision Criteria

**Choose OpenProject if**:
- 10+ concurrent projects
- Need mixed methodologies (Kanban + Gantt)
- Portfolio reporting critical
- Can handle deployment complexity

**Choose Redmine if**:
- Very complex project hierarchies (deep nesting)
- Ruby on Rails expertise available
- Need extensive customization via plugins
- UI/UX not priority

**Choose Plane if**:
- <10 concurrent projects
- Modern UX critical for team adoption
- Technical team (developers)
- Simpler deployment preferred

### Architecture Pattern: Project Hierarchy

**OpenProject Structure**:
```
Organization
├── Product Line A
│   ├── Project A1
│   │   ├── Sprint 1
│   │   └── Sprint 2
│   └── Project A2
├── Product Line B
│   ├── Project B1
│   └── Project B2
└── Internal Operations
    ├── HR
    └── Finance
```

**Key Capabilities**:
- Cross-project Gantt charts
- Portfolio dashboards
- Resource allocation across projects
- Milestone tracking across portfolio

---

## Pattern 4: Software Development Team with Git Integration

### Team Characteristics
- **Size**: 3-20 developers
- **Current Tool**: GitHub/GitLab Issues, Trello, or JIRA
- **Skills**: High technical capability (developers)
- **Budget**: $50-200/month
- **Pain Point**: Need tight Git integration, issue tracking tied to commits/PRs

### Project Characteristics
- **Count**: 2-10 active codebases
- **Complexity**: Moderate to high (software projects)
- **Methodology**: Agile (Scrum or Kanban)
- **Features Needed**:
  - Git integration (GitHub, GitLab, Bitbucket)
  - Issue tracking linked to commits/PRs
  - Sprint planning
  - Burndown charts
  - Code review workflow integration

### Platform Recommendations

#### Primary Option: **Plane**
**Why**:
- Designed for technical teams (modern stack)
- GitHub/GitLab integration
- Issues, epics, cycles (sprints)
- Modern UX developers expect (Linear-like)
- API-first architecture

**Trade-offs**:
- ✅ Best modern UX for developers
- ✅ GitHub/GitLab integration
- ✅ Developer-friendly (keyboard shortcuts, CLI)
- ✅ React + Django stack familiar to devs
- ❌ Newer platform (less proven than JIRA/Redmine)
- ❌ Smaller plugin ecosystem

**Deployment**:
- Docker: 15-30 minutes
- Infrastructure: $20-40/month VPS
- Maintenance: 2-3 hours/month

**Breakeven vs JIRA**: 3-5 users (JIRA $8-16/user/month = $288-960/year for 3-5 users)

#### Alternative Option: **Taiga**
**Why**:
- Agile-native (Scrum/Kanban)
- GitHub/GitLab integration pre-configured
- Sprint boards with swimlanes
- Burndown charts
- Beautiful UI

**Trade-offs**:
- ✅ Excellent Scrum/Kanban implementation
- ✅ GitHub/GitLab integration built-in
- ✅ Beautiful UI developers like
- ❌ Less modern than Plane (2014 vs 2022)
- ❌ Python + Angular stack less trendy

**When to choose Taiga over Plane**:
- Pure agile team (Scrum or Kanban, not hybrid)
- Beautiful UI more important than cutting-edge
- Established platform preferred (2014 vs 2022)

#### Alternative Option: **Redmine**
**Why**:
- Deep Git integration (Git, SVN, Mercurial)
- Issue linking to commits
- Mature development workflow
- Vast plugin ecosystem

**Trade-offs**:
- ✅ Most mature Git integration (19 years)
- ✅ Plugin ecosystem for any custom need
- ✅ Deep VCS integration (beyond just Git)
- ❌ Dated UI (2006-era)
- ❌ Rails deployment complex
- ❌ Developers may resist old-looking UI

**When to choose Redmine over Plane**:
- Legacy codebases (SVN, Mercurial)
- Ruby on Rails expertise
- Need extensive customization
- UI/UX not critical for team adoption

### Decision Criteria

**Choose Plane if**:
- Modern developer team
- GitHub/GitLab primary VCS
- UX important for adoption
- Want Linear/JIRA alternative

**Choose Taiga if**:
- Pure agile (Scrum/Kanban)
- Beautiful UI critical
- GitHub/GitLab integration needed
- Established platform preferred

**Choose Redmine if**:
- Legacy VCS (SVN, Mercurial)
- Rails expertise available
- Deep customization needed
- UI not critical

### Integration Architecture

**Plane + GitHub**:
```
GitHub PR #123
  ↓ (references)
Plane Issue #456
  ↓ (tracked in)
Sprint 3 (Cycle)
  ↓ (part of)
Epic: User Authentication
```

**Workflow**:
1. Create issue in Plane
2. Create branch: `feature/PLANE-456-oauth-login`
3. Commit with message: `Implement OAuth login (PLANE-456)`
4. Open PR referencing PLANE-456
5. Plane automatically links PR to issue
6. Merge PR → Plane marks issue "Done"

---

## Pattern 5: Small Team with Limited DevOps Capability

### Team Characteristics
- **Size**: 2-8 people
- **Skills**: Non-technical to beginner technical (designers, marketers, small business)
- **DevOps Capability**: Minimal (can follow tutorials, no Rails/K8s expertise)
- **Budget**: $20-100/month
- **Pain Point**: Want self-hosting benefits without operational complexity

### Project Characteristics
- **Count**: 2-8 projects
- **Complexity**: Low to moderate
- **Methodology**: Flexible (Kanban or simple task lists)
- **Features Needed**: Basic PM, easy deployment, minimal maintenance

### Platform Recommendations

#### Primary Option: **Vikunja**
**Why**:
- Simplest Docker deployment (docker-compose up -d)
- Very lightweight (1GB RAM sufficient)
- Modern UI (easy for non-technical users)
- Multiple view types (List, Kanban, Gantt)

**Trade-offs**:
- ✅ Easiest deployment (15 minutes)
- ✅ Minimal maintenance (1-2 hours/month)
- ✅ Very low cost ($10-15/month VPS)
- ❌ Limited advanced features
- ❌ May need to migrate if team grows significantly

**Deployment Steps**:
1. Rent $10/month VPS (DigitalOcean, Linode)
2. Install Docker
3. Run `docker-compose up -d` with Vikunja config
4. Point domain to VPS
5. Done (15-30 minutes total)

#### Alternative Option: **WeKan**
**Why**:
- Simple Docker deployment
- Familiar Kanban interface
- Lightweight

**Trade-offs**:
- ✅ Trello-like (familiar)
- ✅ Easy deployment
- ❌ Kanban-only (less flexible than Vikunja)

**When to choose WeKan over Vikunja**:
- Kanban is sufficient (no need for Gantt/Table views)
- Trello familiarity important

#### Option to Avoid: **Redmine, OpenProject**
**Why NOT**:
- Redmine requires Rails expertise
- OpenProject requires 4-8GB RAM, more complex deployment
- Both have steeper learning curves
- Overkill for small teams with limited DevOps

### Decision Criteria

**Choose Vikunja if**:
- Want easiest deployment
- Multiple view types needed
- Very budget-conscious

**Choose WeKan if**:
- Kanban-only sufficient
- Trello familiarity important

**Avoid if**:
- Limited DevOps: Redmine (complex), OpenProject (resource-heavy)

### Managed Alternatives (If Self-Hosting Too Complex)

If even Docker is too complex:
- **Vikunja Cloud**: Hosted Vikunja (pricing varies)
- **WeKan Cloud**: Third-party WeKan hosting
- **Taiga Cloud**: $10/month for small teams
- **OpenProject Cloud**: $7.25-19.50/user/month

**Trade-off**: Pay for convenience ($10-100/month) vs self-hosting ($10-20/month infra)

---

## Pattern 6: Scaling Beyond Basic Boards

### Team Characteristics
- **Current Tool**: Basic Kanban (Trello, WeKan, Vikunja)
- **Size**: 5-20 people
- **Growth**: Team has outgrown simple boards
- **Pain Point**: Need resource management, Gantt charts, time tracking, advanced reporting

### Project Characteristics
- **Complexity**: Increasing (simple Kanban insufficient)
- **Methodology**: Evolving from pure Kanban to mixed (Kanban + Gantt + sprints)
- **Features Needed**:
  - Gantt charts (waterfall projects)
  - Resource allocation
  - Time tracking
  - Advanced reporting
  - Dependencies between tasks

### Platform Recommendations

#### Primary Option: **OpenProject**
**Why**:
- Supports Kanban (familiar) + Gantt + traditional PM
- Resource management
- Time tracking built-in
- Advanced reporting
- Free Community edition

**Migration Path from Basic Kanban**:
1. Deploy OpenProject
2. Create projects with Work Packages (like cards)
3. Set up Boards view (like Kanban)
4. Gradually add Gantt charts for waterfall projects
5. Add time tracking as needed
6. Build reports once data accumulates

**Trade-offs**:
- ✅ Smooth transition (has Kanban boards)
- ✅ Grows with team (Kanban → full PM)
- ✅ Free Community edition very capable
- ❌ Steeper learning curve
- ❌ Higher infrastructure costs ($40-80/month)

#### Alternative Option: **Plane**
**Why**:
- Modern alternative
- Cycles (sprints) for more structure
- Roadmaps for planning
- Analytics

**Trade-offs**:
- ✅ Modern UX (easier adoption)
- ✅ Less complex than OpenProject
- ❌ No Gantt charts (Kanban + Cycles only)
- ❌ Limited resource management

**When to choose Plane over OpenProject**:
- Don't need Gantt charts
- Modern UX critical for adoption
- Agile-only (no waterfall)

### Decision Criteria

**Stick with Basic Kanban (WeKan/Vikunja) if**:
- Team < 5 people
- Projects simple (no dependencies, no resource conflicts)
- Kanban methodology sufficient

**Move to OpenProject if**:
- Team 10+ people
- Need Gantt charts for waterfall projects
- Resource management needed
- Time tracking required
- Complex dependencies

**Move to Plane if**:
- Team 5-20 technical people
- Need more structure (cycles/sprints) but not full PM
- Modern UX critical
- Agile-only

---

## Pattern 7: Mixed Methodology Requirements

### Team Characteristics
- **Size**: 5-50 people
- **Structure**: Different teams use different methodologies
- **Example**: Dev team (Agile) + Marketing (Kanban) + Construction projects (Waterfall)

### Project Characteristics
- **Methodology Mix**:
  - Some projects: Agile/Scrum (sprints, backlogs)
  - Some projects: Kanban (continuous flow)
  - Some projects: Waterfall (Gantt charts, dependencies)
- **Features Needed**: Platform supporting ALL methodologies

### Platform Recommendations

#### Primary Option: **OpenProject**
**Why**:
- Explicitly supports multiple methodologies
- Kanban boards for agile teams
- Gantt charts for waterfall teams
- Scrum-style backlogs available
- Each project can choose methodology

**Methodology Support**:
- **Agile**: Work packages → Backlogs → Sprint boards
- **Kanban**: Work packages → Kanban boards → WIP limits
- **Waterfall**: Work packages → Gantt charts → Dependencies

**Trade-offs**:
- ✅ Best multi-methodology support
- ✅ Free Community edition
- ✅ Each team can use their preferred method
- ❌ Complexity (learning curve for each methodology)
- ❌ May feel "jack of all trades, master of none"

#### Alternative Option: **Plane**
**Why**:
- Flexible views (Kanban, Lists, Cycles)
- Can approximate multiple methodologies

**Trade-offs**:
- ✅ Modern UX
- ✅ Simpler than OpenProject
- ❌ No true Gantt charts (limited waterfall support)
- ❌ Best for agile variations, not waterfall

**When to choose Plane over OpenProject**:
- "Mixed" = Kanban + Scrum (both agile)
- Don't need true waterfall (Gantt)
- Modern UX priority

### Decision Criteria

**Choose OpenProject if**:
- Need TRUE mixed methodologies (Agile + Kanban + Waterfall)
- Gantt charts required for some projects
- Resource management across methodologies
- Complex dependencies

**Choose Plane if**:
- "Mixed" = agile variations (Kanban + Scrum)
- No waterfall/Gantt needed
- Modern UX critical

---

## Pattern 8: Agency Managing Multiple Client Projects

### Team Characteristics
- **Size**: 5-25 people
- **Structure**: Agency/consultancy with multiple clients
- **Pain Point**: Need client project separation, reporting per client, time tracking for billing

### Project Characteristics
- **Count**: 10-50 client projects (varying sizes)
- **Isolation**: Clients must NOT see each other's projects
- **Billing**: Time tracking needed for hourly billing
- **Reporting**: Per-client reports for billing/transparency

### Platform Recommendations

#### Primary Option: **OpenProject**
**Why**:
- Strong multi-project hierarchy
- Time tracking built-in (billable hours)
- Cost tracking
- Per-project permissions (client isolation)
- Client can be given read-only access to their project only

**Agency Architecture**:
```
OpenProject Instance
├── Client A
│   ├── Project A1
│   └── Project A2
├── Client B
│   ├── Project B1
│   └── Project B2
└── Internal
    └── Agency Operations
```

**Permissions**:
- Agency staff: See all projects
- Client A: See ONLY Client A projects (read-only or limited)
- Client B: See ONLY Client B projects

**Trade-offs**:
- ✅ Excellent multi-project + permissions
- ✅ Time tracking for billing
- ✅ Cost reports per client
- ❌ No true multi-tenancy (single instance, permission-based separation)
- ❌ Complex permission setup

#### Alternative Option: **Redmine**
**Why**:
- Mature multi-project hierarchy
- Time tracking plugins
- Billing plugins available
- Can create per-client parent projects

**Trade-offs**:
- ✅ Very mature multi-project support
- ✅ Extensive plugins for agency needs
- ❌ Dated UI (may not impress clients)
- ❌ Rails expertise needed

**When to choose Redmine over OpenProject**:
- Rails expertise available
- Need specific agency plugins
- Okay with dated UI

#### Multi-Tenancy Pattern (Advanced)

If TRUE multi-tenancy needed (separate databases per client):
- Deploy multiple instances of Plane/Taiga/Vikunja (one per client)
- Use Docker containers with separate databases
- More complex infrastructure but TRUE isolation

**When multi-tenancy needed**:
- High-security clients (government, healthcare)
- Data MUST be isolated (not just permission-based)
- Clients demand dedicated instances

**Cost**: Higher (multiple VPS or K8s cluster)

### Decision Criteria

**Choose OpenProject if**:
- Permission-based separation sufficient
- Time tracking for billing critical
- Need per-client reporting

**Choose Redmine if**:
- Rails expertise available
- Need extensive plugins for agency workflows

**Choose multi-tenancy (multiple instances) if**:
- High-security requirements
- True data isolation required (separate DBs)
- Budget allows ($100-500/month for multiple instances)

---

## Pattern 9: Enterprise with Compliance Requirements

### Team Characteristics
- **Size**: 20-500+ people
- **Industry**: Healthcare, finance, government, regulated industries
- **Requirements**:
  - Audit logging (who changed what, when)
  - Role-based access control (RBAC)
  - GDPR/HIPAA/SOC2 compliance
  - SSO (LDAP, SAML)
  - Data encryption (at rest, in transit)

### Project Characteristics
- **Complexity**: High (enterprise-grade)
- **Compliance**: Critical (audit trails, data sovereignty)
- **Scale**: 100s-1000s of users

### Platform Recommendations

#### Primary Option: **OpenProject Enterprise**
**Why**:
- Commercial support available
- LDAP/SAML authentication
- Audit logging (Enterprise edition)
- RBAC
- Can be deployed on-premise (data sovereignty)
- SOC2/ISO27001 compliance possible

**Compliance Features**:
- Audit logs: All changes tracked
- SSO: LDAP, SAML, OAuth
- Encryption: SSL/TLS, database encryption
- RBAC: Fine-grained permissions
- Data sovereignty: Self-hosted = data stays in your jurisdiction

**Trade-offs**:
- ✅ Enterprise-ready
- ✅ Commercial support available
- ✅ Compliance features built-in (Enterprise edition)
- ❌ Enterprise edition costs ($405/5 users/year, scales up)
- ❌ Community edition lacks some compliance features

**Cost**:
- Community: Free (but limited audit logging)
- Enterprise: $405/5 users/year to $10K+/year for large deployments

#### Alternative Option: **Redmine**
**Why**:
- Can be deployed on-premise
- LDAP authentication built-in
- Audit plugins available
- Mature (trusted in enterprises)

**Trade-offs**:
- ✅ Free and open source
- ✅ LDAP built-in
- ✅ Audit plugins available
- ❌ No commercial support (unless third-party)
- ❌ Audit features require plugins (not built-in)
- ❌ Dated UI

**When to choose Redmine over OpenProject**:
- Budget-constrained (no money for Enterprise support)
- Rails expertise available
- Plugins acceptable for compliance features

### Decision Criteria

**Choose OpenProject Enterprise if**:
- Budget exists for commercial support ($5K-50K/year)
- Need compliance certifications (SOC2, ISO27001)
- Audit logging critical
- SSO required (SAML, LDAP)

**Choose OpenProject Community if**:
- Budget-constrained
- Basic RBAC sufficient
- Can implement some compliance features manually

**Choose Redmine if**:
- Free and open source requirement
- Rails expertise available
- Plugins acceptable for compliance

### Compliance Checklist

| Requirement | OpenProject Enterprise | OpenProject Community | Redmine |
|-------------|------------------------|----------------------|---------|
| Audit Logging | ✅ Built-in | ⚠️ Limited | 🔌 Plugin |
| LDAP/SSO | ✅ LDAP, SAML | ✅ LDAP | ✅ LDAP |
| RBAC | ✅ Fine-grained | ✅ Basic | ✅ Basic |
| Encryption | ✅ SSL/TLS, DB | ✅ SSL/TLS | ✅ SSL/TLS |
| Data Sovereignty | ✅ Self-hosted | ✅ Self-hosted | ✅ Self-hosted |
| Commercial Support | ✅ Yes | ❌ No | ⚠️ Third-party |
| SOC2/ISO27001 | ✅ Possible | ⚠️ Harder | ⚠️ Harder |

---

## Pattern 10: Technical Team Needing Deep Customization

### Team Characteristics
- **Size**: 5-50 technical people
- **Skills**: Developers, DevOps engineers
- **Pain Point**: SaaS PM tools don't fit workflows; need custom fields, workflows, integrations
- **Budget**: $50-500/month (labor + infrastructure)

### Project Characteristics
- **Complexity**: High (custom workflows, unique processes)
- **Integration Needs**: Custom APIs, webhooks, third-party tools
- **Customization Depth**: Extensive (custom fields, states, automations)

### Platform Recommendations

#### Primary Option: **Plane**
**Why**:
- Modern tech stack (React + Django)
- API-first architecture (GraphQL + REST)
- Open source (AGPL-3.0, can fork and customize)
- TypeScript/Python codebase familiar to developers

**Customization Depth**:
- Custom fields: Via API
- Custom workflows: Via API
- Custom integrations: REST/GraphQL API
- Custom UI: Fork and modify (React)

**Trade-offs**:
- ✅ Modern stack developers love
- ✅ API-first (easy to extend)
- ✅ Can fork and customize
- ✅ GraphQL for flexible queries
- ❌ Newer (less community plugins than Redmine)
- ❌ Requires dev time to customize

#### Alternative Option: **Redmine**
**Why**:
- 1000+ plugins available
- Mature plugin API
- Can customize extensively via plugins
- Ruby on Rails (full control)

**Customization Depth**:
- Custom fields: Built-in + plugins
- Custom workflows: Workflow plugins
- Custom integrations: 1000+ plugins
- Custom UI: Rails views, theming

**Trade-offs**:
- ✅ Vast plugin ecosystem
- ✅ Proven customization platform
- ✅ Don't need to build everything (plugins exist)
- ❌ Dated tech stack (Rails)
- ❌ Plugin quality varies

**When to choose Redmine over Plane**:
- Rails expertise available
- Plugin ecosystem more valuable than modern stack
- Don't want to build custom features (use plugins)

#### Alternative Option: **Taiga**
**Why**:
- Python + Angular
- REST API + webhooks
- Open source (can customize)

**Trade-offs**:
- ✅ Python + Angular (modern but not cutting-edge)
- ✅ Good API
- ❌ Smaller plugin ecosystem than Redmine
- ❌ Less customizable than Plane (less API-first)

### Decision Criteria

**Choose Plane if**:
- Want modern stack (TypeScript, React, Django, GraphQL)
- API-first architecture critical
- Willing to build custom features
- Small team of developers

**Choose Redmine if**:
- Want to use existing plugins (not build)
- Rails expertise available
- Vast plugin ecosystem valuable

**Choose Taiga if**:
- Python + Angular stack preferred
- Agile-focused
- Moderate customization needs

### Customization Examples

**Plane + Custom Integration**:
```typescript
// Custom webhook handler
app.post('/webhook/plane', async (req, res) => {
  const issue = req.body.issue

  // Custom logic
  if (issue.priority === 'critical') {
    await sendPagerDutyAlert(issue)
  }

  // Update custom system
  await updateCustomDashboard(issue)
})
```

**Redmine + Plugin**:
```ruby
# Install existing plugin
gem install redmine_agile

# Or build custom plugin
class CustomWorkflowHooksListener < Redmine::Hook::ViewListener
  def controller_issues_new_after_save(context={})
    # Custom logic when issue created
  end
end
```

---

## Pattern 11: Budget-Constrained Team Avoiding SaaS Costs

### Team Characteristics
- **Size**: 3-15 people
- **Budget**: Minimal (<$50/month total)
- **Pain Point**: SaaS costs $500-2,000/year for team, want <$500/year total
- **Skills**: Willing to learn Docker, basic DevOps

### Project Characteristics
- **Count**: 2-10 projects
- **Complexity**: Low to moderate
- **Methodology**: Flexible (Kanban or simple PM)

### Cost Comparison Reference

| SaaS Tool (10 users) | Monthly Cost | Annual Cost |
|----------------------|--------------|-------------|
| Trello Standard | $50 | $600 |
| Asana Premium | $119 | $1,428 |
| Monday.com Standard | $90 | $1,080 |
| JIRA Software | $80-160 | $960-1,920 |

**Target**: <$500/year (<$42/month)

### Platform Recommendations

#### Ultra-Budget Option: **Vikunja**
**Infrastructure Cost**:
- VPS: $10-15/month (DigitalOcean, Linode, Hetzner)
- Domain: $10-15/year
- **Total**: ~$135-195/year

**Savings vs SaaS**: $400-1,700/year (vs $600-1,920 SaaS alternatives)

**Trade-offs**:
- ✅ Lowest cost self-hosted option
- ✅ Very lightweight (512MB-1GB RAM)
- ✅ Simple deployment
- ❌ Limited advanced features
- ❌ 2-4 hours setup + 1-2 hours/month maintenance

**Breakeven**: Immediate (Year 1: $300-400 total vs $600+ SaaS)

#### Budget Option: **WeKan**
**Infrastructure Cost**:
- VPS: $10-20/month
- Domain: $10-15/year
- **Total**: ~$135-255/year

**Savings vs SaaS**: $345-1,665/year

**Trade-offs**:
- ✅ Low cost
- ✅ Familiar Trello-like interface
- ❌ Kanban-only

#### Mid-Budget Option: **Plane**
**Infrastructure Cost**:
- VPS: $20-40/month (higher RAM needed)
- Domain: $10-15/year
- **Total**: ~$255-495/year

**Savings vs SaaS**: $105-1,425/year

**Trade-offs**:
- ✅ Modern features
- ✅ Better for larger teams (10-20 people)
- ✅ More robust than Vikunja
- ❌ Higher infrastructure costs
- ❌ Higher maintenance time

### Decision Criteria

**Choose Vikunja if**:
- Absolute minimal budget (<$200/year)
- Small team (3-8 people)
- Simple needs (task lists + basic Kanban)

**Choose WeKan if**:
- Budget <$300/year
- Kanban sufficient
- Trello-like interface important

**Choose Plane if**:
- Budget <$500/year
- Larger team (10-15 people)
- Need modern features
- Can justify higher infra costs for better UX

### Hidden Costs to Consider

**Time Investment**:
- Initial setup: 2-8 hours ($250-1,000 @ $125/hr if outsourced)
- Monthly maintenance: 1-3 hours ($125-375/month if outsourced)

**If outsourcing DevOps**:
- Year 1: $1,500-5,000 (setup + maintenance)
- **Breakeven shifts to 15-30 users vs SaaS**

**DIY DevOps recommendation**: Learn Docker yourself (20-40 hour learning curve) to keep costs minimal

### Budget Optimization Strategies

1. **Use cheapest VPS** (Hetzner €4/month, Contabo, DigitalOcean $6/month droplet)
2. **Avoid managed services** (Managed K8s = 3-5x infrastructure cost)
3. **Choose lightweight platform** (Vikunja over OpenProject)
4. **Learn Docker** (avoid outsourcing setup/maintenance)
5. **Use free domain** (Subdomain from existing domain, or Cloudflare free tier)

---

## Pattern 12: Modern UX Expectations (Linear/Notion Style)

### Team Characteristics
- **Size**: 5-30 people
- **Culture**: Design-conscious, modern tech expectations
- **Current Tools**: Linear, Notion, or considering them
- **Pain Point**: Want self-hosting BUT cannot tolerate "ugly" open source tools
- **Budget**: $50-200/month

### Project Characteristics
- **Complexity**: Moderate
- **Methodology**: Agile (modern style, not traditional JIRA)
- **Features Needed**:
  - Beautiful, modern interface
  - Keyboard shortcuts
  - Fast performance
  - Multiple views (Kanban, List, etc.)
  - Clean, minimal design

### Platform Recommendations

#### Primary Option: **Plane**
**Why**:
- Explicitly designed as Linear alternative
- Modern React UI
- Keyboard shortcuts (vim-like)
- Fast, responsive
- Multiple views
- AI features

**UX Characteristics**:
- Clean, minimal design (like Linear)
- Dark mode
- Keyboard-first navigation
- Fast (no page reloads)
- Modern color scheme

**Trade-offs**:
- ✅ Best modern UX in open source PM
- ✅ Comparable to Linear/Notion
- ✅ Team will actually want to use it
- ❌ Newer platform (2022)
- ❌ Smaller feature set than established tools

**Deployment**:
- Docker: 15-30 minutes
- Infrastructure: $20-40/month
- Maintenance: 2-3 hours/month

**Comparison to Linear**:
| Feature | Plane | Linear |
|---------|-------|--------|
| Modern UI | ✅ | ✅ |
| Keyboard shortcuts | ✅ | ✅ |
| Fast performance | ✅ | ✅ |
| Self-hostable | ✅ | ❌ |
| Cost (10 users) | ~$300/year | $960/year |

#### Alternative Option: **Taiga**
**Why**:
- Beautiful, design-focused UI
- Created by designers
- Modern (but 2014, not 2022)

**UX Characteristics**:
- Beautiful UI (focus on design)
- Colorful, vibrant
- Good UX (not quite Linear-level)

**Trade-offs**:
- ✅ Beautiful UI (better than most open source)
- ✅ Agile-focused
- ❌ Not quite as modern as Plane
- ❌ Python + Angular (less trendy than React)

**When to choose Taiga over Plane**:
- Prefer colorful, vibrant UI over minimal
- Agile-only (Scrum/Kanban)
- Established platform preferred (2014 vs 2022)

#### Options to Avoid: **Redmine, OpenProject**

**Why NOT for modern UX expectations**:
- Redmine: 2006-era UI (dated, functional but not beautiful)
- OpenProject: Traditional enterprise UI (not modern/minimal)

**Team adoption risk**: Design-conscious teams may resist ugly tools

### Decision Criteria

**Choose Plane if**:
- Modern UX non-negotiable
- Want Linear-style interface
- Keyboard shortcuts important
- Fast, minimal design preferred

**Choose Taiga if**:
- Beautiful UI important (but not necessarily minimal)
- Colorful, vibrant design preferred
- Agile-focused

**Avoid if modern UX critical**:
- Redmine (dated UI)
- OpenProject (traditional enterprise UI)
- WeKan (functional but basic)

### UX Comparison Matrix

| Platform | UI Style | Modern Score (1-10) | Best For |
|----------|----------|---------------------|----------|
| **Plane** | Minimal, Linear-like | 9/10 | Modern tech teams |
| **Taiga** | Colorful, vibrant | 7/10 | Design-conscious agile teams |
| **Vikunja** | Clean, simple | 6/10 | Personal productivity |
| **WeKan** | Trello-like | 5/10 | Kanban simplicity |
| **Focalboard** | Notion-like | 7/10 | Mattermost users |
| **OpenProject** | Traditional enterprise | 4/10 | Enterprises (UX not priority) |
| **Redmine** | 2006-era | 2/10 | Functionality over UX |

---

## Cross-Pattern Decision Tree

### Start Here: What's Your Primary Constraint?

#### Constraint 1: **Budget** (<$300/year total)
→ **Vikunja** (ultra-budget) or **WeKan** (budget Kanban)

#### Constraint 2: **DevOps Skills** (minimal/none)
→ **Vikunja** (simplest) or consider **managed alternatives** (Taiga Cloud $10/month)

#### Constraint 3: **UX** (must be modern/beautiful)
→ **Plane** (Linear-like) or **Taiga** (design-focused)

#### Constraint 4: **Methodology** (mixed Agile/Kanban/Waterfall)
→ **OpenProject** (multi-methodology support)

#### Constraint 5: **Scale** (10+ concurrent projects)
→ **OpenProject** (portfolio management) or **Redmine** (complex hierarchies)

#### Constraint 6: **Compliance** (GDPR/HIPAA/SOC2)
→ **OpenProject Enterprise** (audit logging, SSO) or **Redmine** (plugins)

#### Constraint 7: **Customization** (API-first, extensible)
→ **Plane** (modern API) or **Redmine** (vast plugins)

#### Constraint 8: **Simplicity** (just need Kanban, nothing more)
→ **WeKan** (Trello clone) or **Vikunja** (lightweight)

---

## Migration Cheat Sheet

### From Trello
**Best Target**: WeKan (direct import) or Vikunja (manual migration)
**Migration Time**: 2-8 hours
**Complexity**: Low

### From JIRA
**Best Target**: Plane (modern alternative) or OpenProject (feature parity)
**Migration Time**: 20-80 hours (depends on JIRA complexity)
**Complexity**: High

### From Asana
**Best Target**: Plane (modern UX) or Taiga (agile-focused)
**Migration Time**: 10-40 hours
**Complexity**: Medium

### From Linear
**Best Target**: Plane (explicit Linear alternative)
**Migration Time**: 10-30 hours
**Complexity**: Medium

### From Notion
**Best Target**: Focalboard (Notion-like) or Plane (modern alternative)
**Migration Time**: Varies (Notion is very flexible)
**Complexity**: Medium to High

### From Spreadsheets
**Best Target**: Vikunja (simplest) or WeKan (familiar Kanban)
**Migration Time**: 4-12 hours
**Complexity**: Low to Medium

---

## Total Cost of Ownership (TCO) Summary by Pattern

| Pattern | Platform | Setup | Monthly Infra | Monthly Maint | Year 1 Total | Year 2+ Total |
|---------|----------|-------|---------------|---------------|--------------|---------------|
| **Simple Kanban** | WeKan | $125-250 | $10-20 | $15-30 | $430-790 | $300-600 |
| **Solo→Team** | Vikunja | $125 | $10-15 | $15-25 | $305-605 | $180-480 |
| **Multi-Project** | OpenProject | $250-500 | $40-80 | $50-100 | $1,330-2,660 | $1,080-2,160 |
| **Dev Team** | Plane | $250 | $20-40 | $30-50 | $850-1,330 | $600-1,080 |
| **Limited DevOps** | Vikunja | $125 | $10-15 | $15-25 | $305-605 | $180-480 |
| **Scaling Beyond** | OpenProject | $250-500 | $40-80 | $50-100 | $1,330-2,660 | $1,080-2,160 |
| **Mixed Method** | OpenProject | $250-500 | $40-80 | $50-100 | $1,330-2,660 | $1,080-2,160 |
| **Agency** | OpenProject | $500-1000 | $80-200 | $100-200 | $2,660-5,400 | $2,160-4,800 |
| **Enterprise** | OpenProject Ent | $1,000+ | $100-500 | $200-1,000 | $4,800-19,000 | $3,600-18,000 |
| **Customization** | Plane | $500-2,000 | $20-40 | $50-200 | $1,340-4,880 | $840-2,880 |
| **Ultra-Budget** | Vikunja | $125 | $10-15 | $15-25 | $305-605 | $180-480 |
| **Modern UX** | Plane | $250 | $20-40 | $30-50 | $850-1,330 | $600-1,080 |

**Notes**:
- Setup: One-time (hours @ $125/hr, or DIY time)
- Monthly Infra: VPS, domain, backups
- Monthly Maint: Updates, monitoring (hours @ $125/hr, or DIY time)
- Actual costs may be $0 if DIY (just infrastructure)

---

## Platform Selection Matrix (Quick Reference)

| Use Case | Vikunja | WeKan | Plane | Taiga | Worklenz | Focalboard | OpenProject | Redmine |
|----------|---------|-------|-------|-------|----------|------------|-------------|---------|
| **Simple Kanban** | ⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐ | ⭐⭐ | ⭐ | ❌ |
| **Solo→Team** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐ | ⭐ | ⭐ | ❌ | ❌ |
| **Multi-Project** | ❌ | ❌ | ⭐⭐ | ⭐ | ⭐ | ❌ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Dev Team** | ⭐ | ❌ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐ | ⭐⭐ | ⭐⭐ |
| **Limited DevOps** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐ | ⭐⭐ | ❌ | ❌ |
| **Scaling Beyond** | ❌ | ❌ | ⭐⭐ | ⭐ | ⭐ | ❌ | ⭐⭐⭐ | ⭐⭐ |
| **Mixed Method** | ❌ | ❌ | ⭐ | ❌ | ⭐ | ❌ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Agency** | ❌ | ❌ | ⭐ | ⭐ | ⭐ | ❌ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Enterprise** | ❌ | ❌ | ⭐ | ⭐ | ❌ | ❌ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Customization** | ⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐ |
| **Ultra-Budget** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐ | ⭐ | ⭐⭐ | ❌ | ❌ |
| **Modern UX** | ⭐⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐ | ❌ |

**Legend**:
- ⭐⭐⭐ = Excellent fit
- ⭐⭐ = Good fit
- ⭐ = Possible but not ideal
- ❌ = Poor fit / avoid

---

## Appendix: Pattern Combinations

### Real-World Scenario: Multi-Pattern Teams

Many teams match MULTIPLE patterns. Example:

**Scenario**: 8-person software development agency
- Pattern 3: Multi-project (5 client projects)
- Pattern 4: Dev team (Git integration needed)
- Pattern 8: Agency (client separation)
- Pattern 11: Budget-conscious (<$500/year)

**Analysis**:
- Patterns 3, 8 → **OpenProject** (multi-project + agency features)
- Pattern 4 → **Plane** (modern dev team)
- Pattern 11 → **Vikunja** (ultra-budget)

**Trade-off**:
- OpenProject fits Patterns 3, 8 BUT violates Pattern 11 (costs $1,300-2,600/year)
- Vikunja fits Pattern 11 BUT poor for Patterns 3, 8 (limited multi-project)
- Plane middle ground: Fits Pattern 4, moderate for Patterns 3, 8, moderate cost

**Decision**: Prioritize patterns by importance
- If budget is #1 constraint → Vikunja (compromise on multi-project)
- If multi-project is #1 constraint → OpenProject (compromise on budget)
- If modern dev UX is #1 constraint → Plane (compromise on agency features)

### Pattern Priority Framework

1. Identify ALL matching patterns
2. Rank patterns by business criticality
3. Find platform matching top 2-3 patterns
4. Accept trade-offs on lower-priority patterns

---

## S3 Status and Next Steps

**S3 Status**: ✅ Complete - 12 generic use case patterns documented

**What S3 Provides**:
- Generic decision frameworks (hardware store catalog)
- Parameterized patterns (team size, budget, skills, etc.)
- Platform recommendations BY PATTERN (not by specific user)
- Trade-off analysis for each pattern
- TCO summaries
- Migration guidance

**What S3 Does NOT Provide**:
- Specific recommendations for YOUR projects (that's `applications/` folder)
- Application-specific ROI calculations
- Implementation roadmaps for specific teams
- Migration guides for specific SaaS → self-hosted transitions

**Next Steps**:

1. **For Application-Specific Analysis** → Create `applications/project-management/` with:
   - Analysis of ALL your projects (SEA, cookbooks, qrcards, etc.)
   - Map your portfolio to patterns from S3
   - Select ONE platform for entire portfolio
   - Implementation roadmap

2. **For S2 Comprehensive Discovery** → Performance benchmarks, detailed feature matrix, security analysis

3. **For S4 Strategic Discovery** → Vendor viability, community health, technology evolution

---

**Document Complete**: S3 Need-Driven Discovery (Generic Use Case Patterns)
**Last Updated**: November 7, 2025
