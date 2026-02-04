# Platform: Odoo CRM

**Type**: Comprehensive Business Suite (CRM is one module)
**License**: LGPL-3.0 (Community), Proprietary (Enterprise)
**Maturity**: Mature (20+ years, v17 as of 2024)
**GitHub**: ~37K+ stars (full Odoo suite)

---

## Quick Overview

Odoo is a **complete business management suite** where CRM is just one of 30+ integrated apps (accounting, inventory, HR, manufacturing, etc.). Most powerful self-hosted option, but complexity matches scope.

**Best for**: All-in-one business suite, teams wanting CRM + ERP + more

---

## Tech Stack

- **Backend**: Python 3, PostgreSQL, Werkzeug (WSGI)
- **Frontend**: JavaScript (Owl framework), XML views
- **Deployment**: Docker, native (deb/rpm), Kubernetes
- **API**: XML-RPC, JSON-RPC, REST API (via modules)

---

## Deployment Complexity

**Skill Level**: Intermediate-to-Advanced

**Deployment Options**:
1. **Docker** (easiest): 30-60 minutes
   ```bash
   docker run -d -p 8069:8069 odoo:17
   ```
2. **VPS native** (Ubuntu/Debian): 1-3 hours
3. **Kubernetes**: 4-8 hours (Helm charts available)
4. **Odoo.sh** (managed hosting by Odoo): Minutes (hybrid model)

**Infrastructure Requirements**:
- **Minimum**: 4GB RAM, 2 vCPU, 20GB storage (CRM only)
- **Recommended**: 8GB RAM, 4 vCPU, 50GB+ (multiple apps)
- **Database**: PostgreSQL 12+

---

## Operational Requirements

**Time Commitment**:
- Initial setup: 4-16 hours (CRM only) to 40+ hours (full suite)
- Monthly maintenance: 3-8 hours (updates, module management, backups)

**Skills Needed**:
- Python basics (for customization)
- Docker OR Linux admin (depending on deployment)
- PostgreSQL administration
- Odoo-specific knowledge (module system, XML views)

---

## Cost Estimate (TCO)

**Community Edition** (LGPL-3.0):

**Infrastructure** (monthly):
- VPS: $40-200/month (8GB RAM, scales with modules)
- Backups: $10-30/month
- Monitoring: $0-50/month

**Operations** (monthly):
- DIY: 4-8 hours × $0 (your time)
- Outsourced: $500-2,000/month (Odoo consultant)

**Year 1 Total**: $5,000-25,000 (complex setup + 12 months ops)
**Year 2+ Total**: $3,000-18,000/year (ops only)

**Enterprise Edition** (proprietary add-ons):
- $24-100/user/month (Odoo.sh managed hosting)
- Additional features: Advanced reporting, studio, support
- **Hybrid model**: Managed by Odoo but you control data

**Breakeven vs Managed**: 10-20 users
- Managed alt (HubSpot): ~$1,600-3,000/month for 5-10 users
- Odoo self-hosted: ~$400-1,500/month (including ops)

---

## Features

**CRM Features**:
- ✅ Lead/opportunity management
- ✅ Pipeline visualization (kanban, list, calendar)
- ✅ Activities and tasks
- ✅ Email integration (IMAP/SMTP, email gateway)
- ✅ Phone integration (VoIP via modules)
- ✅ Custom fields and workflows
- ✅ Reporting and analytics

**Beyond CRM** (what makes Odoo unique):
- ✅ Sales (quotes, orders, invoicing)
- ✅ Accounting (full double-entry)
- ✅ Inventory & warehouse management
- ✅ Project management
- ✅ HR & recruitment
- ✅ Manufacturing (MRP)
- ✅ E-commerce (website builder + shop)
- ✅ Point of Sale

**Total**: 30+ business apps, all integrated

---

## Customization

**Depth**: Very High (unlimited via modules)

**Approaches**:
- **Odoo Studio** (Enterprise only): No-code app builder
- **Custom modules**: Python + XML (extensive documentation)
- **API integrations**: XML-RPC, JSON-RPC, REST
- **App store**: 30,000+ community and commercial modules

**Ecosystem**: Massive (largest self-hosted business app ecosystem)

---

## Strengths

✅ **All-in-one suite** - CRM + accounting + inventory + everything
✅ **Mature platform** - 20+ years, proven at enterprise scale
✅ **Huge ecosystem** - 30K+ modules, large consultant network
✅ **Highly customizable** - Module system allows unlimited extension
✅ **Good documentation** - Comprehensive official docs
✅ **Multi-company** - Native support for managing multiple entities
✅ **Active development** - Annual major releases, continuous updates

---

## Weaknesses

❌ **Complex** - Steep learning curve, many moving parts
❌ **Resource-heavy** - 4-8GB RAM minimum (grows with modules)
❌ **Python 3 required** - Custom development needs Python skills
❌ **UI can feel dated** - Improving but not as modern as Twenty
❌ **Version upgrades complex** - Major version migrations require planning
❌ **Community vs Enterprise split** - Best features require Enterprise license

---

## When to Choose Odoo CRM

**Choose if**:
- You need CRM + other business functions (accounting, inventory, etc.)
- You want "all-in-one" instead of stitching tools together
- You have intermediate-to-advanced technical team
- You need proven enterprise-scale stability
- You want massive customization potential
- You're OK with operational complexity for comprehensive features

**Avoid if**:
- You only need CRM (overkill, use Twenty or EspoCRM)
- You want simplicity over features
- Your team lacks Python/DevOps skills
- You need modern UX (Odoo improving but not cutting-edge)

---

## Deployment Models

**1. Self-Hosted Community (Full control)**:
- Free (LGPL-3.0)
- All features except Enterprise modules
- You manage everything

**2. Odoo.sh (Hybrid managed)**:
- $24-100/user/month
- Managed hosting by Odoo
- Includes Enterprise features
- You control data, Odoo handles ops
- **Note**: This blurs line between 1.130 and 3.501

**3. On-Premise Enterprise**:
- License fee (contact Odoo)
- Self-hosted with Enterprise modules
- Official support available

---

## Migration Path

**From Managed CRM**:
- CSV import (contacts, opportunities)
- Python scripts for complex data (Odoo has import framework)
- Rebuild workflows using Odoo's automation tools
- Estimate: 20-80 hours depending on complexity

**To Managed CRM**:
- PostgreSQL export → CSV
- Straightforward data ownership
- Lose integrated suite (accounting, inventory, etc.)

---

## Community & Support

- **Docs**: Excellent (https://www.odoo.com/documentation)
- **Community**: Very large (forums, Stack Overflow, meetups)
- **Updates**: Annual major releases (v17, v18, etc.)
- **Support**:
  - Community: Forums, consultants worldwide
  - Enterprise: Official Odoo support + consulting

---

## Odoo vs Twenty vs SuiteCRM

| Feature | Odoo | Twenty | SuiteCRM |
|---------|------|--------|----------|
| **Scope** | Full business suite | CRM only | CRM only |
| **Complexity** | High | Low | Medium |
| **Modern UX** | Good | Excellent | Fair |
| **Ecosystem** | Massive (30K+ modules) | Emerging | Medium |
| **TCO** | $5-25K year 1 | $2.5-8K year 1 | $4-16K year 1 |
| **Best for** | All-in-one business | Modern lightweight CRM | Salesforce alternative |

---

**Last Updated**: 2025-10-21
