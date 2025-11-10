# S4: Build vs Buy Analysis

**Methodology**: MPSE v3.0 - S4 (Strategic Analysis)
**Focus**: When to DIY vs use SaaS (Motion/Reclaim)
**Date**: 2025-11-09

---

## Executive Summary

**Key Finding**: Buy SaaS for <100 users, consider building custom for >100 users (if privacy-critical or unique workflow).

**Build effort**: 200-500 hours (2-6 months) = $50-150k engineering cost
**Build ongoing**: $50-200/month LLM API + $5-10k/year maintenance
**Buy cost**: $8-34/user/month = $96-408/user/year

**Break-even**: ~50-150 users (depends on engineering cost, workflow uniqueness)

**Recommendation**:
- **<50 users**: Buy SaaS (Motion/Reclaim) - fast time-to-value, low cost
- **50-100 users**: Evaluate (cost neutral zone, depends on custom needs)
- **>100 users**: Consider building IF privacy-critical or unique workflow
- **>500 users**: Strong build case (SaaS cost = $48-204k/year vs $50-150k one-time build)

---

## Build Cost Analysis

### Phase 1: MVP (200-300 hours = $50-75k)

**Core features** (minimum viable AI scheduler):
1. **Calendar integration** (50h): Google Calendar API, OAuth, bidirectional sync
2. **Task management** (80h): CRUD operations, task model (duration, deadline, priority)
3. **Basic AI scheduler** (100h):
   - Constraint solver (work hours, meetings, deadlines)
   - Calendar slot finder
   - Auto-scheduling logic
4. **Web UI** (70h): React/Next.js app, calendar view, task list

**Engineering cost**: 200-300h × $150-250/hour (contractor) = **$30-75k**
- Or: 3-6 months internal engineer time (salary + benefits = $50-75k)

**Trade-offs**:
- ✅ Custom to your workflow
- ✅ Full data control (privacy)
- ❌ Basic AI (no pattern learning, no project dependencies)
- ❌ No mobile app (web only)
- ❌ 3-6 month build time (vs 15-30 min SaaS setup)

---

### Phase 2: Advanced AI (200-300 hours = $50-75k)

**Advanced features** (parity with Motion/Reclaim):
1. **Pattern learning** (80h): ML models for duration estimation, priority scoring
2. **Habit optimization** (60h): Recurring task scheduler (like Reclaim habits)
3. **Project dependencies** (100h): DAG scheduler, deadline propagation (like Motion)
4. **Mobile app** (200h): iOS + Android native apps

**Total build**: Phase 1 + Phase 2 = 400-600 hours = **$100-150k**

**Trade-offs**:
- ✅ Feature parity with Motion/Reclaim
- ✅ Custom workflow support
- ❌ 6-12 month build time
- ❌ Ongoing ML model training cost ($50-200/month LLM API)
- ❌ Maintenance burden (5-10k/year bug fixes, updates)

---

### Phase 3: Team Features (100-200 hours = $25-50k)

**Team features** (if building for 20+ users):
1. **Shared projects** (60h): Team visibility, task assignment
2. **Workload balancing** (80h): AI distributes tasks across team
3. **Team calendar** (40h): See everyone's availability
4. **Admin panel** (60h): User management, billing, analytics

**Total build**: Phase 1 + Phase 2 + Phase 3 = 500-800 hours = **$125-200k**

**Trade-offs**:
- ✅ Custom team workflow
- ✅ Data control (no third-party SaaS)
- ❌ 12-18 month build time
- ❌ Ongoing maintenance (5-15k/year)

---

## Buy Cost Analysis (SaaS)

### Reclaim.ai: $8-12/user/month

**10 users**: $80-120/month = $960-1,440/year
**50 users**: $400-600/month = $4,800-7,200/year
**100 users**: $800-1,200/month = $9,600-14,400/year
**500 users**: $4,000-6,000/month = $48,000-72,000/year

**Features included**:
- ✅ AI scheduling (habit optimization, calendar analysis)
- ✅ Mobile app (iOS + Android)
- ✅ Integrations (Todoist, Asana, Linear, Slack)
- ✅ Instant setup (15-30 minutes)
- ✅ No maintenance burden (Reclaim handles updates)

---

### Motion: $34/user/month

**10 users**: $340/month = $4,080/year
**50 users**: $1,700/month = $20,400/year
**100 users**: $3,400/month = $40,800/year
**500 users**: $17,000/month = $204,000/year

**Features included**:
- ✅ Advanced AI (project dependencies, deadline propagation)
- ✅ All-in-one (tasks + calendar + projects)
- ✅ Mobile app (iOS + Android)
- ✅ Team features (workload balancing, capacity planning)
- ✅ Instant setup (30-60 minutes)
- ✅ No maintenance burden

---

## Break-Even Analysis

### Scenario 1: Simple AI Scheduler (Phase 1 MVP)

**Build cost**: $50-75k one-time + $5k/year maintenance
**Buy cost** (Reclaim): $8-12/user/month

**Break-even**:
- **50 users**: Reclaim = $4,800-7,200/year, Build = $50-75k one-time (break-even year 7-15)
- **100 users**: Reclaim = $9,600-14,400/year, Build = $50-75k one-time (break-even year 3-7)
- **500 users**: Reclaim = $48,000-72,000/year, Build = $50-75k one-time (break-even year 1)

**Verdict**: Build justified at >100-150 users (if simple AI sufficient)

---

### Scenario 2: Advanced AI Scheduler (Phase 1 + 2)

**Build cost**: $100-150k one-time + $10k/year maintenance + $50-200/month LLM API
**Buy cost** (Motion): $34/user/month

**Break-even**:
- **50 users**: Motion = $20,400/year, Build = $100-150k one-time (break-even year 5-7)
- **100 users**: Motion = $40,800/year, Build = $100-150k one-time (break-even year 2.5-3.5)
- **500 users**: Motion = $204,000/year, Build = $100-150k one-time (break-even year <1)

**Verdict**: Build justified at >100 users (if advanced AI needed)

---

### Scenario 3: Team Features (Phase 1 + 2 + 3)

**Build cost**: $125-200k one-time + $15k/year maintenance
**Buy cost** (Motion Teams): $34/user/month

**Break-even**:
- **50 users**: Motion = $20,400/year, Build = $125-200k one-time (break-even year 6-10)
- **100 users**: Motion = $40,800/year, Build = $125-200k one-time (break-even year 3-5)
- **500 users**: Motion = $204,000/year, Build = $125-200k one-time (break-even year <1)

**Verdict**: Build justified at >100-200 users (if team features critical)

---

## When to Build Custom

### Build IF:

**1. Privacy-Critical Use Case**
- **Example**: Healthcare, finance, legal (can't share calendar/task data with SaaS)
- **Justification**: Compliance (HIPAA, GDPR) requires on-prem or private cloud
- **Build cost**: $100-200k worth it to avoid regulatory risk

**2. Unique Workflow (SaaS Doesn't Fit)**
- **Example**: Manufacturing (shop floor scheduling), field services (technician routing)
- **Justification**: Motion/Reclaim built for knowledge workers (not specialized workflows)
- **Build cost**: Custom AI scheduling for domain-specific constraints

**3. Large User Base (>100-500 users)**
- **Example**: Enterprise (1,000+ employees)
- **Justification**: SaaS cost = $96k-408k/year vs $100-200k one-time build
- **Build cost**: Amortizes across large user base (break-even <2 years)

**4. Integration-Heavy (Proprietary Systems)**
- **Example**: Custom ERP, legacy CRM, proprietary project management
- **Justification**: SaaS integrations limited (Todoist, Asana, Linear only)
- **Build cost**: Custom connectors required anyway (build scheduler too)

**5. Competitive Advantage (Proprietary AI)**
- **Example**: Startup building productivity-as-a-feature (not core product)
- **Justification**: AI scheduling = differentiator (can't use off-the-shelf)
- **Build cost**: R&D investment (productize custom AI)

---

### Buy (SaaS) IF:

**1. Standard Workflow (Knowledge Workers)**
- **Example**: Software engineering team, marketing team, sales team
- **Justification**: Motion/Reclaim designed for this use case (90% fit)
- **SaaS cost**: $8-34/user/month vs $100k+ build (no-brainer)

**2. Small User Base (<50-100 users)**
- **Example**: Startup, small business, department within larger org
- **Justification**: Build cost ($100k+) doesn't amortize
- **SaaS cost**: $480-20,400/year vs $100k build (5-200× cheaper)

**3. Fast Time-to-Value Needed**
- **Example**: Urgent productivity crisis, team scaling fast
- **Justification**: SaaS = 15-30 min setup vs 6-12 month build
- **SaaS cost**: Opportunity cost of waiting 6-12 months = $50k-500k (lost productivity)

**4. No Engineering Resources**
- **Example**: Non-tech company, lean startup
- **Justification**: No in-house engineers to build + maintain
- **SaaS cost**: $8-34/user/month vs hiring engineer ($150k/year salary)

**5. Vendor Lock-In Acceptable**
- **Example**: Low switching cost (2-4 hours, see S3 migration guides)
- **Justification**: If vendor dies, migrate in 2-4 hours (moderate risk)
- **SaaS cost**: Lock-in risk < build cost ($100k+)

---

## Hybrid Approach: Buy Then Build

**Strategy**: Start with SaaS (Motion/Reclaim), build custom later if justified

### Phase 1: Buy SaaS (Year 1-2)
- **Why**: Fast time-to-value, prove ROI, learn requirements
- **Cost**: $8-34/user/month for 10-50 users = $960-20,400/year
- **Outcome**: Validate productivity gain (10-20× ROI), understand workflow

### Phase 2: Evaluate Build (Year 2-3)
- **Trigger**: User base >100, unique workflow needs emerge, privacy concerns
- **Decision**: Build vs continue SaaS
- **Cost**: $100-200k build if justified

### Phase 3: Build Custom (Year 3+)
- **Why**: SaaS cost >$40k/year, custom needs justify build
- **Migration**: Export data from SaaS (CSV), import to custom system
- **Outcome**: Lower long-term cost, full control

**Example**: 500-person company
- Year 1-2: Use Reclaim ($48k/year) - prove ROI
- Year 2: Evaluate build ($100k one-time)
- Year 3+: Switch to custom system (save $38k/year ongoing)
- **Break-even**: Year 5 (recoup $100k build cost via $38k/year savings)

---

## Build Technology Stack (If Building)

### Backend:
- **Language**: Python (ML-friendly) or TypeScript (full-stack JS)
- **Framework**: FastAPI (Python) or Next.js (TypeScript)
- **Database**: PostgreSQL (relational) + Redis (caching)
- **Calendar API**: Google Calendar API, Microsoft Graph API (Outlook)
- **Scheduler**: Custom constraint solver (OR-Tools, PuLP) or simple greedy algorithm

### AI/ML:
- **LLM (optional)**: OpenAI GPT-4, Anthropic Claude (for NLP task parsing)
- **ML models**: XGBoost (duration estimation), policy gradients (habit optimization)
- **Embeddings**: Sentence-BERT (task similarity, deduplication)

### Frontend:
- **Web**: React + Next.js (server-side rendering)
- **Mobile**: React Native (iOS + Android from single codebase) or Flutter

### Infrastructure:
- **Cloud**: AWS, GCP, or Azure
- **Cost**: $50-200/month (10-100 users), $500-2,000/month (500+ users)

### Total build time:
- **MVP**: 3-6 months (200-300 hours)
- **Advanced AI**: 6-12 months (400-600 hours)
- **Team features**: 12-18 months (500-800 hours)

---

## Verdict: Build vs Buy Decision Matrix

| Factor | Build | Buy (SaaS) |
|--------|-------|-----------|
| **User count** | >100-500 | <100 |
| **Workflow** | Unique (manufacturing, field services) | Standard (knowledge work) |
| **Privacy** | Critical (HIPAA, GDPR) | Acceptable (SaaS trusted) |
| **Budget** | $100-200k available | <$50k/year |
| **Time-to-value** | 6-12 months acceptable | Urgent (need now) |
| **Engineering** | In-house team available | No engineering resources |
| **Competitive advantage** | AI = differentiator | AI = productivity tool |

**Recommendation**:
- **80-90% of companies**: Buy SaaS (Motion/Reclaim) - standard workflow, <100 users
- **10-20% of companies**: Build custom - >100 users, privacy-critical, unique workflow
- **Hybrid approach**: Buy SaaS (year 1-2), build custom later if justified (year 3+)

---

## Key Insights

1. **Break-even ~100 users**: Below 100 users, SaaS cheaper; above 100, build may be justified
2. **Time-to-value critical**: 6-12 month build vs 30-min SaaS setup (opportunity cost huge)
3. **Maintenance burden**: Build = $5-15k/year ongoing vs SaaS = vendor handles updates
4. **Feature parity hard**: Building Motion-level AI = $100-150k (complex constraint solver)
5. **Hybrid approach best**: Buy SaaS first, validate ROI, build later if justified

**Bottom line**: Most companies should buy SaaS (Motion/Reclaim), only build custom if >100 users + privacy-critical + unique workflow
