# Scenario: Technical Startup - Control & Customization

**Business Pattern**: SaaS startup with technical team, want full control and custom workflows

---

## Context

**Team Size**: 5-20 people (including 2-5 technical/DevOps)

**Customer Count**: 50-2,000 (growing fast)

**Budget**: $500-5,000/year for CRM infrastructure

**Technical Capability**: Intermediate-to-advanced (comfortable with Docker, APIs, databases)

**Priority**: Platform control, customization, API-first, modern stack

---

## Recommended Solution

### Primary: **Twenty CRM (Self-Hosted via Docker Compose)**

**Deployment Model**: Pure self-hosted on VPS

**Why Twenty**:
- ✅ Modern tech stack (TypeScript, React, GraphQL) - familiar to startup devs
- ✅ Best API quality (GraphQL) - easy to build custom integrations
- ✅ Docker-native - aligns with startup DevOps practices
- ✅ Can customize deeply (open source, clean codebase)
- ✅ Lightweight - low infrastructure cost
- ✅ Active development - features improving rapidly

---

## Implementation

**Infrastructure**:
- VPS: DigitalOcean Droplet (4GB RAM, $40/month)
- Database: PostgreSQL (included)
- Backups: Automated snapshots ($10/month)
- Total: **$600/year**

**Setup**:
```bash
# Clone Twenty
git clone https://github.com/twentyhq/twenty.git
cd twenty

# Configure environment
cp .env.example .env
# Edit .env with database credentials, domain, etc.

# Deploy
docker-compose up -d

# Configure SSL (Caddy/nginx + Let's Encrypt)
# Point DNS to VPS
```

**Time**: 2-4 hours initial setup

**Monthly Maintenance**: 2-3 hours
- Update Docker images (monthly)
- Monitor backups
- Review logs

---

## TCO (3 Years, 10 Users)

**Year 1**:
- Infrastructure: $600
- Setup labor: 4 hours × $0 (in-house technical team)
- Maintenance: 36 hours/year × $0 (team capacity)
- **Total: $600**

**Year 2-3**: $600/year each

**3-Year Total: $1,800**

**Per User**: $60/user over 3 years

**vs Managed Alternative**:
- Pipedrive (managed SaaS): $10,440 over 3 years
- **Savings**: $8,640 over 3 years

---

## Why Not Managed?

**Team has technical capability** - ops burden is minimal for skilled team

**Custom integrations needed** - GraphQL API makes this easy, better to control infrastructure

**Cost-sensitive startup** - $600/year vs $3,000-10,000/year managed options

**Learning investment pays off** - 2-4 hour setup is one-time cost

---

## Migration Triggers

**When to reconsider**:
- Team loses DevOps capability (key person leaves)
- Scale exceeds single VPS (>1,000 concurrent users)
- Need extensive native integrations (Twenty ecosystem still growing)
- Operational burden becomes >5 hours/month

**Likely migration path**:
- **If need more features**: Add custom integrations via GraphQL API (stay self-hosted)
- **If lose DevOps**: Migrate to Twenty CloudStation ($216/year, minimal change)
- **If need comprehensive suite**: Evaluate Odoo (self-hosted OR managed)

---

## Alternative: **Odoo CRM (Self-Hosted)**

**When to choose Odoo instead**:
- Need CRM + accounting + inventory + project management (not just CRM)
- Comfortable with Python (for customization)
- Have more DevOps capacity (Odoo more complex)

**TCO**: $8,200 year 1, $7,200 year 2+ (but replaces 3-5 separate tools)

---

## Applies To

- Technical SaaS startups (B2B software)
- Developer tool companies
- API-first product companies
- Startups with technical founders
- Teams migrating from Airtable/Notion to "real CRM"

**Common traits**:
- Have engineering team (2-10 developers)
- Docker/DevOps practices already in use
- Value control and customization
- Budget-conscious (pre-Series A typically)
- API integrations important (product-led growth)

---

**Last Updated**: 2025-10-21
