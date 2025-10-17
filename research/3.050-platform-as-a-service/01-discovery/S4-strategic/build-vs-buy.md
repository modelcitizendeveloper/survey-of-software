# Build vs Buy: DIY VPS vs PaaS Economics

**Experiment:** 3.050 Platform-as-a-Service
**Analysis Date:** 2025-10-09
**Question:** Should QRCards use PaaS or DIY deployment on VPS?

---

## Executive Summary

**Recommendation: START with PaaS (Render/PythonAnywhere), MIGRATE to DIY if needed**

**Key Finding:** PaaS saves 10-20 hours/month in DevOps time. For early-stage projects, time-to-market beats cost savings. DIY makes sense at scale or if acquisition risk materializes.

**Break-Even:** ~$100-150/month hosting spend (typically 500-1000 users)

---

## Option 1: PaaS (Render, Railway, PythonAnywhere)

### Cost Structure

**Small App (MVP/Testing):**
- Free tier: $0/month
- Limitations: Sleep after inactivity, limited resources

**Small Production (100-500 users):**
- Web service: $7-25/month
- Database: $7-20/month
- **Total: $15-45/month**

**Medium Production (500-2000 users):**
- Web service: $25-85/month
- Database: $20-90/month
- CDN/egress: $10-30/month
- **Total: $55-205/month**

**Large Production (2000+ users):**
- Web services (multiple): $100-300/month
- Database (HA): $90-200/month
- CDN/egress: $50-150/month
- **Total: $240-650/month**

### Time Investment

**Initial Setup:** 1-4 hours
- Connect GitHub repo
- Configure environment variables
- Deploy (usually automatic)
- Set up database
- Configure domain/SSL (automatic)

**Ongoing Maintenance:** 1-2 hours/month
- Monitor deployment (usually automatic)
- Update dependencies (git push)
- Review performance metrics
- Rotate secrets
- Check billing

**Time Saved vs DIY:** ~10-20 hours/month
- No server management
- No OS updates
- No SSL certificate renewal
- No load balancer config
- No database backups management
- No security patching

### Value Delivered by PaaS

**Included Features:**
- Automatic SSL certificates
- CDN/edge caching
- Zero-downtime deployments
- Automated backups
- Monitoring/logging
- DDoS protection
- Load balancing (automatic)
- Scaling (vertical/horizontal)
- Preview environments (PR-based)
- CI/CD pipeline built-in

**DevOps Equivalent:** Would cost $500-1000/month to build equivalent on AWS/DIY

---

## Option 2: DIY VPS (DigitalOcean, Linode, Vultr)

### Cost Structure

**Small Production (100-500 users):**
- VPS (2GB RAM, 2 vCPUs): $12-18/month
- Managed Database: $15-25/month (or DIY on same VPS for $0)
- Backups: $2-5/month
- CDN (Cloudflare): $0-20/month
- Monitoring (optional): $0-10/month
- **Total: $14-78/month**

**Medium Production (500-2000 users):**
- VPS (4GB RAM, 2 vCPUs): $24-36/month
- Managed Database: $30-50/month
- Load Balancer: $10-20/month (if needed)
- Backups: $5-10/month
- CDN: $10-30/month
- Monitoring: $10-20/month
- **Total: $89-166/month**

**Large Production (2000+ users):**
- VPS (8-16GB RAM, 4-8 vCPUs): $48-96/month
- Managed Database (HA): $60-120/month
- Load Balancer: $20-40/month
- Backups: $10-20/month
- CDN: $30-60/month
- Monitoring/logging: $20-50/month
- **Total: $188-386/month**

### Time Investment

**Initial Setup:** 16-40 hours
- Provision VPS (1-2 hours)
- Configure Ubuntu/Debian (2-4 hours)
- Install Docker/Docker Compose (1-2 hours)
- Configure Nginx reverse proxy (2-4 hours)
- Set up SSL (Let's Encrypt, certbot) (1-2 hours)
- Database setup (Postgres install, config) (2-4 hours)
- Deployment automation (GitHub Actions, Ansible) (4-8 hours)
- Monitoring setup (Prometheus, Grafana or SaaS) (2-4 hours)
- Backup automation (2-4 hours)
- Firewall/security hardening (2-4 hours)
- Testing and documentation (2-4 hours)

**Ongoing Maintenance:** 5-10 hours/month
- OS security updates (1-2 hours/month)
- SSL certificate renewal (automated, but monitor)
- Database maintenance (vacuum, analyze) (1 hour/month)
- Log management (rotation, analysis) (1-2 hours/month)
- Monitoring/alerting response (1-2 hours/month)
- Backup verification (1 hour/month)
- Deployment troubleshooting (1-2 hours/month)
- Capacity planning (1 hour/quarter)

**Additional Complexity:**
- Need Linux sysadmin skills
- On-call for outages (no 24/7 support)
- Security responsibility (patching, firewall)
- Scaling requires manual intervention

### What You Build

**Infrastructure:**
- Docker Compose setup (app + database)
- Nginx reverse proxy config
- SSL certificate automation
- Backup scripts
- Deployment pipeline (GitHub Actions → SSH deploy)
- Monitoring dashboard (Grafana or external SaaS)

**Skills Required:**
- Linux administration
- Docker/Docker Compose
- Nginx configuration
- SSL/TLS setup
- Database administration (Postgres)
- Firewall/security hardening
- CI/CD pipeline (GitHub Actions, Ansible)

---

## Break-Even Analysis

### Cost Comparison by Scale

| User Scale | PaaS Cost | DIY Cost | PaaS Premium | DIY Time Cost (10h/mo @ $50/h) |
|------------|-----------|----------|--------------|--------------------------------|
| MVP (Free) | $0/mo | $14/mo | -$14 | $500/mo |
| Small (100-500) | $15-45/mo | $14-78/mo | ~$0 | $500/mo |
| Medium (500-2000) | $55-205/mo | $89-166/mo | +$20/mo | $500/mo |
| Large (2000+) | $240-650/mo | $188-386/mo | +$127/mo | $500/mo |

**Key Insight:** PaaS is 20-50% more expensive at scale, but saves ~10 hours/month in DevOps time.

### Time Value Calculation

**If your time is worth $50/hour:**
- PaaS saves 10 hours/month = $500/month value
- PaaS premium at large scale: ~$127/month
- **Net benefit: $373/month** (even at scale, PaaS is cheaper when time is valued)

**If your time is worth $25/hour:**
- PaaS saves 10 hours/month = $250/month value
- PaaS premium at large scale: ~$127/month
- **Net benefit: $123/month** (still worth it)

**If your time is worth $10/hour:**
- PaaS saves 10 hours/month = $100/month value
- PaaS premium at large scale: ~$127/month
- **Net cost: -$27/month** (DIY becomes cheaper)

**Break-Even Point:**
- If your time is worth <$15/hour, DIY makes sense at large scale
- If your time is worth >$15/hour, PaaS is cheaper (even at scale)
- For early-stage projects, time-to-market > cost savings (use PaaS)

---

## Decision Matrix

### Use PaaS When:

1. **Early Stage** (MVP, testing, low traffic)
   - Time-to-market matters more than cost
   - 1-4 hour setup vs 16-40 hours DIY
   - Focus on product, not infrastructure

2. **Small Team** (1-3 developers, no dedicated DevOps)
   - No one wants to be on-call for infrastructure
   - DevOps skills limited
   - 10-20 hours/month saved = 1-2 developer weeks

3. **Moderate Scale** (<$200/month hosting spend)
   - Cost difference negligible ($20-50/month)
   - Time savings outweigh premium
   - PaaS features (SSL, CDN, backups) included

4. **Low Acquisition Risk Tolerance**
   - Can migrate to DIY if PaaS provider changes
   - 8-16 hour migration project vs 16-40 hour DIY setup
   - Keep low lock-in architecture (Render, Railway)

### Use DIY VPS When:

1. **Large Scale** (>$200/month hosting spend OR >2000 users)
   - Cost savings: $100-250/month
   - Infrastructure complexity justified by savings
   - Can hire/train DevOps engineer

2. **DevOps Expertise In-House**
   - Already know Linux, Docker, Nginx
   - Enjoy infrastructure control
   - 5-10 hours/month maintenance is acceptable

3. **Custom Requirements**
   - Need specific OS config (PaaS is opinionated)
   - Non-standard deployment (PaaS doesn't support)
   - Compliance requirements (data sovereignty, etc.)

4. **High Acquisition Risk**
   - PaaS provider acquired, repriced 5-10x
   - 8-16 hour migration from PaaS to DIY
   - Long-term cost control critical

5. **Budget-Constrained**
   - Literally can't afford $15-45/month PaaS
   - Time has low opportunity cost
   - Willing to learn sysadmin skills

---

## Hybrid Approach: Start PaaS, Migrate to DIY

### Recommended Strategy for QRCards

**Phase 1: MVP/Testing (2025-2026)**
- Deploy to PaaS (Render or PythonAnywhere)
- Use free tier for testing
- Focus on product development
- Cost: $0-15/month

**Phase 2: Early Growth (2026-2028)**
- Stay on PaaS, upgrade to paid tier
- Monitor hosting costs monthly
- Learn Docker/deployment skills in background
- Cost: $15-100/month

**Phase 3: Decision Point (2028-2029)**
- If hosting >$100/month, evaluate DIY migration
- If PaaS provider acquisition signals, prepare DIY migration
- If costs low, stay on PaaS (not worth migration)
- Cost: $50-200/month

**Phase 4: Scale or Migrate (2029-2030)**
- If hosting >$200/month, migrate to DIY VPS
- Or: Stay on PaaS if time-to-value justifies premium
- Or: Migrate due to PaaS acquisition/repricing
- Cost: $100-500/month (PaaS) or $50-300/month (DIY)

### Migration Path: PaaS → DIY

**Estimated Effort:** 16-24 hours

**Steps:**
1. Provision VPS (DigitalOcean $18/month droplet)
2. Docker Compose setup (app + database)
3. Nginx + SSL config
4. Export database from PaaS, import to VPS
5. GitHub Actions deploy pipeline
6. Monitoring setup (Uptime Robot + Sentry)
7. DNS cutover
8. Test and monitor

**Timeline:** 2-3 weekends or 1 focused week

**Risk Mitigation:** Keep PaaS running in parallel for 1 month (rollback option)

---

## Real-World Examples

### Scenario 1: Hobby Project (QRCards MVP)

**User:** Solo developer, building MVP, uncertain product-market fit

**Best Choice:** PaaS (Render free tier or PythonAnywhere free tier)
- **Cost:** $0/month
- **Time:** 2 hours setup, 1 hour/month maintenance
- **Rationale:** Focus on product, not infrastructure. Free tier perfect for testing.

### Scenario 2: Small SaaS (100 paying customers)

**User:** Solo founder, $1000/month revenue, limited technical time

**Best Choice:** PaaS (Render $25/month)
- **Cost:** $25-50/month
- **Time:** 2 hours/month maintenance
- **Rationale:** $25/month is negligible vs 10 hours/month DevOps time. Use PaaS, focus on customers.

### Scenario 3: Growing SaaS (1000 paying customers, $10k/month revenue)

**User:** 2-person team, $10k/month revenue, hosting $150/month on PaaS

**Best Choice:** Stay on PaaS (for now)
- **Cost:** $150/month PaaS vs $100/month DIY
- **Time:** 2 hours/month PaaS vs 8 hours/month DIY
- **Rationale:** $50/month savings not worth 6 hours/month. Wait until $300/month hosting or acquisition risk.

### Scenario 4: Scaled SaaS (5000 customers, $50k/month revenue)

**User:** 5-person team, $50k/month revenue, hosting $400/month on PaaS

**Best Choice:** Migrate to DIY VPS
- **Cost:** $400/month PaaS vs $250/month DIY ($150/month saved)
- **Time:** 8 hours/month DIY maintenance (hire part-time DevOps)
- **Rationale:** $150/month savings = $1800/year. Justify part-time DevOps hire. Control costs long-term.

### Scenario 5: Post-Acquisition Repricing

**User:** Established on PaaS, provider acquired, pricing increases 3x overnight

**Best Choice:** Emergency migration to DIY VPS
- **Cost:** $150/month → $450/month (PaaS repriced) vs $200/month DIY
- **Time:** 16-24 hours migration project (2-3 weekends)
- **Rationale:** Forced migration due to repricing. DIY now cheaper than repriced PaaS.

---

## DIY Setup Guide (High-Level)

For reference when migration becomes necessary:

### Infrastructure Stack

**VPS Provider:** DigitalOcean, Linode, Vultr, or Hetzner (Europe)
**OS:** Ubuntu 24.04 LTS
**Deployment:** Docker Compose
**Reverse Proxy:** Nginx
**SSL:** Let's Encrypt (Certbot)
**Database:** Postgres (managed OR Docker container)
**Monitoring:** Uptime Robot + Sentry (or self-hosted Prometheus/Grafana)
**Backups:** Daily DB dumps to S3/Backblaze B2

### Minimal Docker Compose Setup

```yaml
# docker-compose.yml
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/qrcards
    depends_on:
      - db

  db:
    image: postgres:16
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=secure_password

volumes:
  pgdata:
```

### Nginx Config

```nginx
# /etc/nginx/sites-available/qrcards
server {
    server_name qrcards.example.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/qrcards.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/qrcards.example.com/privkey.pem;
}
```

### GitHub Actions Deploy

```yaml
# .github/workflows/deploy.yml
name: Deploy to VPS
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy via SSH
        run: |
          ssh user@server "cd /app && git pull && docker-compose up -d --build"
```

**Total Setup Time:** 16-24 hours (first time), 8-12 hours (if experienced)

---

## Conclusion

### Strategic Recommendation for QRCards

**START with PaaS (Render or PythonAnywhere):**
1. Faster time-to-market (1-4 hours vs 16-40 hours)
2. Focus on product, not infrastructure
3. Free tier for MVP/testing
4. Low cost ($15-50/month) for early production
5. Time savings (10-20 hours/month) worth premium

**MIGRATE to DIY if/when:**
1. Hosting costs exceed $150-200/month (break-even point)
2. PaaS provider acquired and repriced (forced migration)
3. DevOps expertise developed in-house (maintenance manageable)
4. Custom requirements emerge (PaaS can't support)
5. Long-term cost control becomes critical (late-stage)

**Timeline:**
- **2025-2028:** PaaS (Render) - ideal for MVP and early growth
- **2028-2030:** Decision point - evaluate DIY if costs >$150/month OR acquisition risk materializes
- **2030+:** DIY likely if scaled (>2000 users) or PaaS repriced

**Bottom Line:** PaaS is the right choice for early-stage QRCards. Migrate to DIY only if scale or acquisition risk justifies the DevOps burden.

---

## Cost Summary Table

| Scenario | PaaS Cost | DIY Cost | Time (PaaS) | Time (DIY) | Best Choice |
|----------|-----------|----------|-------------|------------|-------------|
| MVP (Free tier) | $0 | $14/mo | 2h setup, 1h/mo | 20h setup, 5h/mo | PaaS |
| Small (100 users) | $15-45/mo | $14-78/mo | 1-2h/mo | 5-8h/mo | PaaS |
| Medium (500 users) | $55-205/mo | $89-166/mo | 2-3h/mo | 8-10h/mo | PaaS |
| Large (2000+ users) | $240-650/mo | $188-386/mo | 2-4h/mo | 10-15h/mo | DIY (if time-constrained: PaaS) |

**Break-Even:** ~$150-200/month hosting spend (typically 500-1000 users)
