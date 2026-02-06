# Platform: Twenty CRM

**Type**: Modern Open Source CRM
**License**: AGPL-3.0
**Maturity**: Emerging (launched 2023)
**GitHub**: ~15K+ stars

---

## Quick Overview

Twenty CRM is the **modern alternative** to legacy self-hosted CRMs. Built with TypeScript, React, and GraphQL, it offers a clean UX and developer-friendly architecture.

**Best for**: Technical teams wanting lightweight CRM with modern stack

---

## Tech Stack

- **Backend**: TypeScript, Node.js, NestJS, PostgreSQL
- **Frontend**: React, GraphQL, Apollo Client
- **Deployment**: Docker, Docker Compose, Kubernetes-ready
- **API**: GraphQL (primary), REST (limited)

---

## Deployment Complexity

**Skill Level**: Intermediate

**Deployment Options**:
1. **Docker Compose** (recommended for most): 10-30 minutes
   ```bash
   git clone https://github.com/twentyhq/twenty
   cd twenty && docker-compose up -d
   ```
2. **Kubernetes**: 2-4 hours (for production)
3. **Bare metal**: Not recommended (complex dependencies)

**Infrastructure Requirements**:
- **Minimum**: 2GB RAM, 2 vCPU, 10GB storage
- **Recommended**: 4GB RAM, 2 vCPU, 20GB storage
- **Database**: PostgreSQL 14+

---

## Operational Requirements

**Time Commitment**:
- Initial setup: 1-4 hours (including learning)
- Monthly maintenance: 1-3 hours (updates, backups, monitoring)

**Skills Needed**:
- Docker fundamentals
- Basic Linux administration
- PostgreSQL basics
- SSL/reverse proxy (Nginx/Caddy)

---

## Cost Estimate (TCO)

**Infrastructure** (monthly):
- VPS (DigitalOcean/Hetzner): $20-40/month (4GB RAM Droplet)
- Backups: $5-10/month (automated snapshots)
- Monitoring: $0-20/month (optional)

**Operations** (monthly):
- DIY: 2-4 hours × $0 (your time)
- Outsourced: $200-500/month (consultant retainer)

**Year 1 Total**: $2,500-8,000 (setup + 12 months ops)
**Year 2+ Total**: $2,000-7,000/year (ops only)

**Breakeven vs Managed**: 5-10 users
- Managed alt (Pipedrive $29/user): $1,740/year for 5 users
- Twenty self-hosted: ~$2,500/year (including ops time)

---

## Features

**Core CRM**:
- ✅ Contact management
- ✅ Deal pipeline (kanban view)
- ✅ Task management
- ✅ Notes and activities
- ✅ Custom fields
- ✅ Email integration (IMAP)

**Missing** (compared to managed CRMs):
- ❌ Built-in calling features
- ❌ Marketing automation
- ❌ Extensive integration marketplace (few native integrations)
- ❌ Mobile apps (web-first)

---

## Customization

**Depth**: High (open source, modern codebase)

**Approaches**:
- GraphQL API for custom integrations
- Fork and modify (TypeScript/React)
- Custom entities and fields (via UI)

**Ecosystem**: Emerging (active community, growing plugin system)

---

## Strengths

✅ **Modern stack** - TypeScript, React, GraphQL (developer-friendly)
✅ **Clean UX** - Best UI among self-hosted CRMs
✅ **Active development** - Rapid feature additions
✅ **API-first** - GraphQL makes integrations easier
✅ **Lightweight** - Low resource requirements
✅ **Docker-native** - Easy containerized deployment

---

## Weaknesses

❌ **Young platform** - Still maturing, some features missing
❌ **Limited integrations** - Must build custom via API
❌ **Smaller community** - Compared to Odoo/SuiteCRM
❌ **No enterprise support** - Community-driven (consultants available)
❌ **Documentation gaps** - Improving but not comprehensive

---

## When to Choose Twenty CRM

**Choose if**:
- You have intermediate DevOps skills
- You value modern tech stack (TypeScript/React)
- You need lightweight CRM without bloat
- You're comfortable with API-driven integrations
- You want the "best UX" among self-hosted options

**Avoid if**:
- You need extensive pre-built integrations
- You require marketing automation (not core focus)
- You need proven enterprise-scale stability (too new)
- Your team is unfamiliar with Docker

---

## Migration Path

**From Managed CRM**:
- Export contacts/deals as CSV
- Import via Twenty's import tool (basic)
- Rebuild automations via custom code/webhooks

**To Managed CRM**:
- PostgreSQL export → CSV
- Import to managed platform
- Straightforward (owns your data)

---

## Community & Support

- **Docs**: Good (https://twenty.com/developers)
- **Community**: Discord (active), GitHub Discussions
- **Updates**: Weekly releases, very active development
- **Support**: Community-driven, consultants available

---

**Last Updated**: 2025-10-21
