# Scenario: Simple Self-Hosting - Minimal DevOps, Maximum Savings

**Business Pattern**: Small business, limited budget, basic technical capability, want to self-host

---

## Context

**Team Size**: 3-15 people

**Customer Count**: 50-500

**Budget**: <$500/year for CRM (very tight)

**Technical Capability**: Beginner-to-intermediate
- Can use cPanel/web hosting
- Comfortable following tutorials
- No Docker/Kubernetes experience
- May have one "tech-savvy" person on team

**Priority**: Absolute lowest cost while maintaining functionality

---

## Recommended Solution

### Primary: **EspoCRM (Self-Hosted on Shared Hosting)**

**Deployment Model**: Pure self-hosted on LAMP shared hosting

**Why EspoCRM**:
- ✅ Runs on shared hosting ($5-15/month) - no VPS needed
- ✅ Point-and-click installer - no command line required
- ✅ Lowest resource requirements (1GB RAM sufficient)
- ✅ Beginner-friendly interface
- ✅ Core CRM features sufficient for small teams
- ✅ Easy updates (web interface)

---

## Implementation

**Hosting Options**:
1. **Shared LAMP Hosting** (easiest):
   - Namecheap Shared Hosting: $10/month
   - Hostinger Business: $12/month
   - SiteGround StartUp: $15/month
   - Includes: cPanel, MySQL, PHP, SSL, backups

2. **Small VPS** (if comfortable):
   - Hetzner VPS: $5-10/month
   - DigitalOcean Droplet (2GB): $18/month
   - Linode Nanode: $5/month

**Recommended**: Start with shared hosting (easiest)

---

**Setup Process (Shared Hosting)**:

1. **Purchase hosting** ($10/month plan)
2. **Point domain** to hosting (via DNS)
3. **Download EspoCRM** (from espocrm.com)
4. **Upload via cPanel File Manager** OR FTP
5. **Create MySQL database** via cPanel
6. **Run web installer**: https://yourdomain.com/install
   - Enter database credentials
   - Create admin account
   - Click through wizard (5-10 minutes)
7. **Configure SMTP** for email sending (Gmail/SendGrid)
8. **Import contacts** via CSV

**Total Setup Time**: 1-3 hours (first time)
- Most time is reading docs, not technical complexity

**No command line required** - everything via web interface

---

## TCO (3 Users, 3 Years)

**Infrastructure**:
- Shared hosting: $10/month × 12 = **$120/year**
- Domain: $15/year
- Total: **$135/year**

**Setup**:
- Time: 2 hours × $0 (DIY)
- OR hire consultant: $250 one-time (if completely stuck)

**Maintenance** (monthly):
- Updates: 15 minutes (click update button)
- Backups: Automated by hosting provider
- Total: **~3 hours/year**

**Extensions** (optional):
- Advanced Pack (workflows): $60 one-time (for 3 users)
- Sales Pack (quotes): $80 one-time (if needed)
- Total: **$0-140 one-time**

**Year 1 Total**: $135-525 (depending on extensions)
**Year 2-3**: $135/year each

**3-Year Total**: $405-795

**Per User**: $45-88/user over 3 years

---

**vs Managed Alternatives**:

| Option | 3-Year Cost (3 users) | Lock-in | Ops Burden |
|--------|----------------------|---------|------------|
| EspoCRM self-hosted | **$405-795** | None | 3 hrs/yr |
| EspoCRM Cloud | $1,620 ($15/user × 3) | Low | 0 hrs |
| Zoho Bigin | $1,296 ($12/user × 3) | Low-Med | 0 hrs |
| Pipedrive | $3,132 ($29/user × 3) | Medium | 0 hrs |

**Savings**: $900-2,700 over 3 years vs cheapest managed option

---

## Why This Works

**Shared hosting is underrated**:
- PHP/MySQL apps (like EspoCRM) run perfectly on shared hosting
- No Docker knowledge needed
- cPanel makes it point-and-click
- Backups included
- SSL/security handled by host

**EspoCRM is designed for this**:
- Unlike Twenty (needs Docker) or Odoo (needs Python/PostgreSQL)
- LAMP stack = widely compatible
- Low resource usage
- Web-based updates

**Time commitment is minimal**:
- 3 hours/year = 15 minutes/month
- No DevOps knowledge needed
- Web interface for everything

---

## Limitations

**When this doesn't work**:
- ❌ Need advanced features (complex workflows, BPM) → requires Advanced Pack ($60-250)
- ❌ Need modern UI/UX → EspoCRM is functional but not cutting-edge
- ❌ Need extensive integrations → limited ecosystem vs Odoo/SuiteCRM
- ❌ Team grows beyond 20 users → may need more robust hosting

**Migration triggers**:
- Team grows to 15-20+ users → upgrade to VPS hosting ($20-40/month)
- Need advanced features → buy Advanced Pack OR migrate to Odoo
- Want zero ops burden → migrate to EspoCRM Cloud ($15/user)

---

## Step-by-Step for Complete Beginners

**Week 1: Learn & Decide**
- Watch EspoCRM tutorial videos (YouTube, 2-3 hours)
- Read documentation (docs.espocrm.com)
- Sign up for shared hosting trial

**Week 2: Deploy**
- Follow shared hosting deployment guide
- Import test data (10 contacts)
- Configure email integration
- Test basic workflows

**Week 3: Team Rollout**
- Import full contact list
- Train team (2-4 hours)
- Set up pipelines and custom fields
- Go live

**Ongoing**:
- Monthly: Check for updates (15 min)
- Quarterly: Review backup integrity (30 min)
- Annually: Evaluate if still meets needs (1 hour)

---

## Alternative: **Managed Open Source (if ops is too much)**

**If shared hosting setup feels overwhelming**:

**EspoCRM Cloud** ($15/user × 3 = $540/year):
- Zero setup (15 minutes to sign up)
- Zero maintenance
- Includes Advanced Pack
- **Trade-off**: $540 vs $135/year (+$405/year for zero ops)

**Decision point**: Is $405/year worth avoiding 3 hours/year of work?
- For completely non-technical team: Probably yes
- For team with one tech-savvy person: Probably no (good learning experience)

---

## Applies To

- Very small businesses (sole proprietor to 15 people)
- Service businesses (consultants, freelancers, small agencies)
- Non-profits with limited budget
- Family businesses
- Businesses replacing spreadsheets/Airtable with "real CRM"
- Teams with <$1,000/year software budget

**Common traits**:
- Extremely budget-conscious
- Have one "tech-savvy" person (even if not professional IT)
- Willing to invest time to save money
- Don't need cutting-edge features
- 50-500 customers (not enterprise scale)
- Can tolerate 1-2 hours setup time

---

**Last Updated**: 2025-10-21
