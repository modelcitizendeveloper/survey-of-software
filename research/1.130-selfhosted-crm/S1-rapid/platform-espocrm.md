# Platform: EspoCRM

**Type**: Lightweight Open Source CRM
**License**: AGPL-3.0
**Maturity**: Mature (10+ years, stable releases)
**GitHub**: ~1.7K+ stars

---

## Quick Overview

EspoCRM is the **easiest self-hosted CRM to deploy** - runs on shared hosting, requires minimal resources, beginner-friendly. Think "WordPress-level simplicity" for CRM.

**Best for**: Small teams, limited DevOps, budget-conscious, shared hosting

---

## Tech Stack

- **Backend**: PHP 8.0+, MySQL/MariaDB
- **Frontend**: Backbone.js, JavaScript
- **Deployment**: Shared hosting, VPS, Docker
- **API**: REST API, webhooks

---

## Deployment Complexity

**Skill Level**: Beginner-to-Intermediate (easiest of the four)

**Deployment Options**:
1. **Shared Hosting** (simplest): 10-30 minutes
   - Upload via FTP/cPanel
   - Point-and-click installer
   - Works on standard LAMP hosting ($5-10/month)

2. **VPS** (recommended): 30-60 minutes
   - LAMP stack setup
   - Download, extract, configure

3. **Docker**: 15-30 minutes
   ```bash
   docker run -d -p 8080:80 espocrm/espocrm
   ```

**Infrastructure Requirements** (lowest of the four):
- **Minimum**: 1GB RAM, 1 vCPU, 5GB storage
- **Recommended**: 2GB RAM, 2 vCPU, 10GB storage
- **Database**: MySQL 5.7+ or MariaDB 10.1+
- **PHP**: 8.0, 8.1, or 8.2

---

## Operational Requirements

**Time Commitment** (lowest burden):
- Initial setup: 1-3 hours (including learning)
- Monthly maintenance: 1-3 hours (updates, backups)

**Skills Needed** (minimal):
- Basic cPanel/shared hosting OR basic Linux
- FTP/file upload (for shared hosting)
- MySQL basics (backups, restores)
- Optional: Docker basics

---

## Cost Estimate (TCO) - LOWEST

**Shared Hosting Option**:
- Hosting: $5-15/month (shared LAMP hosting)
- Backups: Included in hosting
- Total: $60-180/year

**VPS Option**:
- Infrastructure: $10-40/month (2GB RAM Droplet)
- Backups: $5-10/month
- Total: $180-600/year

**Operations**:
- DIY: 1-3 hours/month × $0 (minimal complexity)
- Outsourced: $100-400/month (if needed)

**Year 1 Total**: $2,000-8,000 (setup + 12 months ops)
**Year 2+ Total**: $1,500-6,000/year (ops only)

**Breakeven vs Managed**: 3-5 users
- Managed alt (Zoho Bigin $12/user): $432/year for 3 users
- EspoCRM shared hosting: ~$60-180/year
- **Savings**: 60-80% even at small scale

---

## Features

**Core CRM**:
- ✅ Accounts, contacts, leads, opportunities
- ✅ Sales pipeline (kanban, list views)
- ✅ Activities (calls, meetings, tasks, emails)
- ✅ Email integration (IMAP/SMTP, personal accounts)
- ✅ Calendar and scheduling
- ✅ Document management
- ✅ Reporting (basic)
- ✅ Workflow automation (Advanced Pack extension)
- ✅ Custom entities and fields (Entity Manager)

**Extensions Available**:
- Advanced Pack: Workflows, BPM, reports ($60-250 one-time)
- Sales Pack: Quotes, invoices, products
- Google Integration: Calendar, Contacts sync
- VoIP Integration: Asterisk, Twilio
- Outlook Integration

**Missing** (vs enterprise platforms):
- ❌ Limited marketing automation (basic campaigns only)
- ❌ No mobile apps (responsive web only)
- ❌ Smaller feature set vs Odoo/SuiteCRM
- ❌ Basic reporting (no advanced BI)

---

## Customization

**Depth**: Medium-High (good for size)

**Approaches**:
- **Entity Manager**: No-code custom entities, fields, relationships
- **Layout Manager**: Customize UI layouts via drag-and-drop
- **Formula scripts**: Custom business logic (no PHP needed)
- **Extensions**: Official store + custom development (PHP)
- **API**: REST API for integrations

**Ecosystem**: Small but sufficient (official extensions + community)

---

## Strengths

✅ **Easiest to deploy** - Runs on shared hosting, point-and-click installer
✅ **Lowest cost** - $60-600/year possible (shared hosting)
✅ **Low resources** - 1-2GB RAM sufficient
✅ **Beginner-friendly** - Minimal DevOps knowledge required
✅ **Entity Manager** - Create custom modules without code
✅ **Clean UI** - Better than SuiteCRM, adequate UX
✅ **Active development** - Regular updates, responsive maintainers
✅ **Formula scripts** - Custom logic without PHP

---

## Weaknesses

❌ **Limited features** - Smaller scope than Odoo/SuiteCRM
❌ **Smaller ecosystem** - Fewer extensions vs competitors
❌ **No mobile apps** - Responsive web only (works on mobile browser)
❌ **Basic reporting** - Limited BI capabilities
❌ **Smaller community** - Less Stack Overflow presence
❌ **Extensions cost money** - Advanced Pack ($60-250), others extra

---

## When to Choose EspoCRM

**Choose if**:
- You have **limited DevOps skills** (can use shared hosting)
- You need **lowest cost** self-hosted option
- You have **small team** (3-20 users)
- You want **easy deployment and maintenance**
- You need **core CRM features** without bloat
- You have **low budget** (<$500/year infrastructure)

**Avoid if**:
- You need comprehensive features (use Odoo)
- You need modern tech stack (use Twenty)
- You need Salesforce replacement (use SuiteCRM)
- You need extensive integrations (limited ecosystem)
- You require advanced reporting/BI

---

## Pricing Model (Extensions)

EspoCRM uses **freemium** model:

**Community Edition** (AGPL-3.0):
- Free, open source
- Core CRM features
- Self-hosted

**Extensions** (one-time purchase):
- **Advanced Pack**: $60-250 (workflows, BPM, reports) - **highly recommended**
- **Sales Pack**: $80-250 (quotes, invoices, products)
- **Google Integration**: $40-150
- **VoIP Integration**: $60-250
- **Outlook Integration**: $40-150

**Pricing tiers**:
- Small business (up to 10 users): Lower tier
- Medium business (10-50 users): Mid tier
- Large business (50+ users): Higher tier

**Total cost with extensions**: $200-1,000 one-time + $60-600/year hosting

**Still cheaper than managed CRM**: $500-1,500 year 1 vs $3,000-10,000/year managed

---

## Migration Path

**From Managed CRM**:
- CSV import (contacts, accounts, opportunities)
- Built-in import tool (guided wizard)
- Easiest migration among self-hosted options
- Estimate: 4-20 hours

**To Managed CRM**:
- MySQL export → CSV
- Simple data structure (easy to export)
- Common trigger: Need advanced features or mobile apps

---

## Community & Support

- **Docs**: Good (https://docs.espocrm.com)
- **Community**: Small-to-medium (official forum, some Stack Overflow)
- **Updates**: Regular releases (monthly patches, feature updates)
- **Support**:
  - Community: Official forum (responsive)
  - Professional: EspoCRM team offers paid support ($200-800/month)

---

## EspoCRM vs Competition

| Feature | EspoCRM | Twenty | SuiteCRM | Odoo |
|---------|---------|--------|----------|------|
| **Deployment Complexity** | Easiest | Easy | Medium | Medium-Hard |
| **Shared Hosting Support** | ✅ Yes | ❌ No | ⚠️ Limited | ❌ No |
| **Minimum RAM** | 1GB | 2GB | 2GB | 4GB |
| **Year 1 TCO** | $2-8K | $2.5-8K | $4-16K | $5-25K |
| **Feature Scope** | Medium | Medium | High | Very High |
| **Modern Stack** | ❌ PHP/Backbone | ✅ TypeScript/React | ❌ PHP/jQuery | ⚠️ Python |
| **Best for** | Easy + cheap | Modern CRM | Salesforce alt | All-in-one |

---

**Last Updated**: 2025-10-21
