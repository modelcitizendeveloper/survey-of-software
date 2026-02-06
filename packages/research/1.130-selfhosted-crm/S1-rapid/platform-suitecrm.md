# Platform: SuiteCRM

**Type**: Salesforce Alternative (Open Source)
**License**: AGPL-3.0
**Maturity**: Mature (forked from SugarCRM 2013, ~15 years lineage)
**GitHub**: ~4.5K+ stars

---

## Quick Overview

SuiteCRM is the **open-source alternative to Salesforce**, forked from SugarCRM Community Edition in 2013. Aims for feature parity with Salesforce at zero licensing cost.

**Best for**: Teams migrating from or replacing Salesforce, PHP shops

---

## Tech Stack

- **Backend**: PHP 7.4-8.2, MySQL/MariaDB
- **Frontend**: JavaScript (Backbone.js, jQuery), SuiteScript
- **Deployment**: LAMP stack (traditional), Docker
- **API**: REST API v8, SOAP (legacy), webhooks

---

## Deployment Complexity

**Skill Level**: Intermediate

**Deployment Options**:
1. **LAMP Stack** (traditional): 1-3 hours
   - Apache, MySQL, PHP on Ubuntu/CentOS
   - Shared hosting compatible (some providers)
2. **Docker**: 30-60 minutes
   ```bash
   docker run -d -p 8080:80 bitnami/suitecrm
   ```
3. **Cloud hosting**: Many SuiteCRM-specific hosts available

**Infrastructure Requirements**:
- **Minimum**: 2GB RAM, 2 vCPU, 10GB storage
- **Recommended**: 4GB RAM, 2-4 vCPU, 20GB+ storage
- **Database**: MySQL 5.7+ or MariaDB 10.3+
- **PHP**: 7.4, 8.0, or 8.1

---

## Operational Requirements

**Time Commitment**:
- Initial setup: 2-8 hours (LAMP stack configuration)
- Monthly maintenance: 2-6 hours (updates, PHP version compatibility, backups)

**Skills Needed**:
- LAMP stack administration (Apache, MySQL, PHP)
- Basic Linux server management
- SSL/Let's Encrypt configuration
- PHP basics (for customization)

---

## Cost Estimate (TCO)

**Infrastructure** (monthly):
- VPS (Linode/DigitalOcean): $30-100/month (4GB RAM)
- Backups: $10-20/month
- Monitoring: $0-30/month

**Operations** (monthly):
- DIY: 3-6 hours × $0 (your time)
- Outsourced: $300-1,200/month (SuiteCRM consultant)

**Year 1 Total**: $4,500-16,000 (setup + 12 months ops)
**Year 2+ Total**: $3,600-12,000/year (ops only)

**Breakeven vs Managed**: 8-15 users
- Managed alt (Salesforce $80-300/user): $7,680-43,200/year for 8-15 users
- SuiteCRM self-hosted: ~$4,500-16,000/year

**Massive savings at scale**:
- Salesforce 100 users × $150/user = $180,000/year
- SuiteCRM 100 users = ~$10,000-20,000/year (same infrastructure, no per-user cost)

---

## Features

**Core CRM** (Salesforce-like):
- ✅ Accounts, contacts, leads, opportunities
- ✅ Sales pipeline (multiple pipelines supported)
- ✅ Activities (calls, meetings, tasks)
- ✅ Email integration (IMAP, SMTP)
- ✅ Campaign management (marketing)
- ✅ Reporting and dashboards
- ✅ Workflow automation
- ✅ Custom modules and fields
- ✅ Role-based permissions (RBAC)

**Advanced Features**:
- ✅ Contract management
- ✅ Quote and invoice generation
- ✅ Project management (basic)
- ✅ Knowledge base
- ✅ Customer portal
- ✅ Mobile apps (iOS, Android)

**Missing** (vs Salesforce):
- ❌ No AppExchange equivalent (smaller plugin marketplace)
- ❌ No AI features (Einstein-like)
- ❌ Limited BI tools (vs Salesforce Reports)

---

## Customization

**Depth**: High (open source, mature plugin system)

**Approaches**:
- **Studio**: Built-in no-code customization tool (fields, modules, layouts)
- **Module Builder**: Create custom modules via UI
- **Custom code**: PHP hooks, logic hooks, custom APIs
- **Plugin marketplace**: Community and commercial add-ons

**Ecosystem**: Medium (smaller than Odoo, larger than Twenty)

---

## Strengths

✅ **Salesforce alternative** - Feature parity for <1% of cost
✅ **Mature platform** - 15+ years lineage, proven stability
✅ **Rich features** - Comprehensive CRM out-of-box
✅ **Good documentation** - Wiki, forums, guides
✅ **Mobile apps** - Native iOS/Android (some features limited)
✅ **Plugin marketplace** - Extensions available (commercial + free)
✅ **Professional support** - SalesAgility (creators) offers paid support

---

## Weaknesses

❌ **Legacy codebase** - PHP + jQuery (not modern stack)
❌ **UI feels dated** - Improving but not as polished as managed CRMs
❌ **LAMP stack maintenance** - PHP version upgrades can be tricky
❌ **Slower development** - Compared to Twenty (small core team)
❌ **Resource usage** - Can be heavy for larger datasets
❌ **Complex upgrades** - Major version migrations require testing

---

## When to Choose SuiteCRM

**Choose if**:
- You're replacing Salesforce and want feature parity
- You need comprehensive CRM features out-of-box
- Your team is comfortable with PHP/LAMP stack
- You want mature, proven platform (not cutting-edge)
- You need role-based permissions and complex workflows
- You want significant cost savings vs Salesforce (100+ users)

**Avoid if**:
- You want modern tech stack (use Twenty instead)
- You need lightweight CRM (use EspoCRM instead)
- You want rapid feature development (SuiteCRM slower)
- Your team unfamiliar with LAMP administration

---

## SuiteCRM Editions

**1. Community Edition** (AGPL-3.0):
- Free, open source
- Self-hosted, full features
- Community support

**2. SuiteCRM Packages**:
- **SuiteCRM On-Demand**: Managed hosting by SalesAgility (~$30-100/user/month)
- **SuiteCRM Enterprise**: Support packages ($2,500-25,000/year)

**Note**: On-Demand hosting blurs line between 1.130 (self-hosted) and 3.501 (managed)

---

## Migration Path

**From Salesforce**:
- Data export (CSV, API)
- SuiteCRM has Salesforce migration tools
- Rebuild custom logic (Apex → PHP)
- Estimate: 40-200 hours (depends on Salesforce customization depth)

**To Salesforce**:
- MySQL export → CSV → Salesforce import
- Lose cost savings, gain ecosystem
- Common trigger: Need AppExchange integrations or enterprise AI features

---

## Community & Support

- **Docs**: Good (https://docs.suitecrm.com)
- **Community**: Medium-large (forums, Stack Overflow)
- **Updates**: Regular releases (quarterly patches, annual feature releases)
- **Support**:
  - Community: Official forums, consultants worldwide
  - Professional: SalesAgility support packages available

---

## Version History

- **SuiteCRM 7.x**: Classic version (stable, most plugins)
- **SuiteCRM 8.x**: Modern rewrite (Symfony backend, Angular frontend)
  - More modern stack
  - Migration from 7.x requires planning
  - **Recommendation**: v7.x for stability, v8.x for greenfield projects

---

**Last Updated**: 2025-10-21
