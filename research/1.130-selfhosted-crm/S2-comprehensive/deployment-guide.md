# S2: Deployment Guide - Open Source CRM Platforms

**Goal**: Operational requirements across deployment models

---

## Deployment Model Overview

Three deployment models with different operational trade-offs:

1. **Pure Self-Hosted** - YOU run everything (no lock-in, highest ops burden)
2. **Managed Open Source** - THEY run infra, you control platform (low lock-in, minimal ops)
3. **Proprietary SaaS** - See 3.501 (high lock-in, zero ops)

---

## Pure Self-Hosted Deployment

### Option 1: Docker Compose (Recommended for Most)

**Best for**: Dev/test, small production (<50 users), teams comfortable with Docker

**Platforms Supported**: All four (Twenty, Odoo, SuiteCRM, EspoCRM)

**Infrastructure Requirements**:

| Platform | Min RAM | Rec RAM | CPU | Storage | Database |
|----------|---------|---------|-----|---------|----------|
| Twenty | 2GB | 4GB | 2 vCPU | 10GB | PostgreSQL 14+ |
| Odoo | 4GB | 8GB | 2-4 vCPU | 20GB | PostgreSQL 12+ |
| SuiteCRM | 2GB | 4GB | 2 vCPU | 10GB | MySQL/MariaDB |
| EspoCRM | 1GB | 2GB | 1-2 vCPU | 5GB | MySQL/MariaDB |

**Hosting Options**:
- **DigitalOcean**: $20-80/month (Droplets with backups)
- **Hetzner**: $10-50/month (best price/performance)
- **Linode**: $20-80/month (good support)
- **Vultr**: $10-60/month (competitive pricing)

**Setup Time**:
- Twenty: 30-60 min (simple docker-compose)
- Odoo: 1-2 hours (more configuration)
- SuiteCRM: 1-2 hours (LAMP setup OR docker)
- EspoCRM: 15-45 min (simplest)

**Initial Setup Steps** (Generic):
```bash
# 1. Provision VPS (Ubuntu 22.04 LTS recommended)
# 2. Install Docker + Docker Compose
sudo apt update && sudo apt install docker.io docker-compose -y

# 3. Clone/download platform
# (platform-specific)

# 4. Configure docker-compose.yml
# - Database credentials
# - Domain/SSL settings
# - Volume mounts for persistence

# 5. Start services
docker-compose up -d

# 6. Configure SSL (Let's Encrypt)
# - Nginx/Caddy reverse proxy
# - certbot for SSL certificates

# 7. Initial platform setup
# - Create admin user
# - Configure SMTP (email sending)
# - Import initial data
```

**Monthly Maintenance**:
- **Time**: 2-4 hours/month
- **Tasks**:
  - Update Docker images (monthly)
  - Database backups (automated, verify weekly)
  - Monitor disk/RAM usage
  - Security updates (OS level)
  - SSL certificate renewal (automated via certbot)

---

### Option 2: VPS Native Deployment

**Best for**: Traditional ops teams, PHP/Python comfort, maximum control

**Platforms**: Odoo (Python), SuiteCRM/EspoCRM (LAMP stack)

**NOT recommended for**: Twenty (Docker-native, complex dependencies)

**Setup Example - EspoCRM on LAMP**:
```bash
# 1. Install LAMP stack
sudo apt install apache2 mysql-server php php-mysql php-curl php-gd -y

# 2. Create database
mysql -u root -p
CREATE DATABASE espocrm;
CREATE USER 'espocrm'@'localhost' IDENTIFIED BY 'password';
GRANT ALL ON espocrm.* TO 'espocrm'@'localhost';

# 3. Download EspoCRM
wget https://www.espocrm.com/downloads/EspoCRM-X.X.X.zip
unzip EspoCRM-X.X.X.zip -d /var/www/html/espocrm

# 4. Set permissions
sudo chown -R www-data:www-data /var/www/html/espocrm

# 5. Configure Apache virtual host
# 6. Run web installer at https://yourdomain.com/install
```

**Setup Time**: 2-4 hours (LAMP config + platform install)

**Monthly Maintenance**:
- **Time**: 3-6 hours/month
- **Tasks**:
  - OS updates (Ubuntu LTS)
  - PHP version updates (compatibility testing needed)
  - MySQL/MariaDB tuning and backups
  - Platform updates (via web interface OR manual)
  - Apache/Nginx configuration

**Complexity**: Medium-High (requires Linux sysadmin skills)

---

### Option 3: Kubernetes (Enterprise Scale)

**Best for**: 100+ users, high availability, microservices teams

**Platforms**: Twenty (K8s-ready), Odoo (Helm charts available)

**NOT recommended for**: <50 users (overkill), small teams (too complex)

**Infrastructure Requirements**:
- Kubernetes cluster (GKE, EKS, DigitalOcean K8s, OR self-managed)
- Min 3 nodes, 8GB RAM each
- Load balancer
- Persistent storage (EBS, PD, etc.)

**Setup Time**: 4-16 hours (cluster setup + platform deployment)

**Monthly Maintenance**:
- **Time**: 4-12 hours/month
- **Tasks**:
  - Cluster updates (K8s version upgrades)
  - Node scaling (based on usage)
  - Helm chart updates
  - Monitoring (Prometheus, Grafana)
  - Backup strategy (PVC snapshots)

**Cost**: $100-500+/month (cluster + overhead)

**Complexity**: High (requires K8s expertise)

---

## Managed Open Source Deployment

### Option 4: Official Managed Services

**Best for**: Want open source benefits without ops burden

**No DevOps required** - vendor manages infrastructure

#### Odoo.sh (Official Odoo Managed Hosting)

**Pricing**: $24-100/user/month

**What's included**:
- Fully managed Odoo (community OR enterprise)
- Automatic updates
- Backups (automated)
- SSL certificates
- Staging environments
- 24/7 monitoring
- Official Odoo support (Enterprise plan)

**Setup Time**: 15-30 minutes (sign up, configure, import data)

**Monthly Maintenance**: **0-1 hours** (vendor manages everything)

**Lock-in Level**: **Low** (can export database, migrate to self-hosted Odoo)

**Migration to Self-Hosted**:
- Backup database from Odoo.sh
- Deploy self-hosted Odoo
- Restore database
- **Time**: 4-20 hours
- **Cost**: $500-2,000 (one-time migration)

---

#### EspoCRM Cloud (Official EspoCRM Managed)

**Pricing**: $15-69/user/month (3-5 user minimum)

**What's included**:
- Fully managed EspoCRM
- Advanced Pack included (workflows, BPM, reports)
- Automatic updates
- Backups
- SSL certificates
- Email support

**Setup Time**: 15-30 minutes

**Monthly Maintenance**: **0-1 hours**

**Lock-in Level**: **Low** (can migrate to self-hosted EspoCRM)

---

#### SuiteCRM On-Demand (Official SuiteCRM Managed)

**Pricing**: $30-100/user/month (estimated, contact SalesAgility)

**What's included**:
- Fully managed SuiteCRM
- Updates and security patches
- Backups
- Support from SalesAgility (creators)

**Setup Time**: Minutes

**Monthly Maintenance**: **0-1 hours**

**Lock-in Level**: **Low** (can migrate to self-hosted SuiteCRM)

---

### Option 5: Third-Party Managed Open Source

**Vendors**: CloudStation, Elest.io, others

**Twenty CloudStation**: $18/month flat (unlimited users)
**Elest.io** (any platform): Hourly billing, ~$20-50/month

**Setup Time**: 5-15 minutes (one-click deployment)

**Monthly Maintenance**: **0 hours** (vendor manages)

**Lock-in Level**: **Low** (open source platform, can self-host)

**Trade-off**: Third-party vs official hosting
- ✅ Often cheaper
- ❌ No official support from platform creators
- ⚠️ Verify vendor reliability

---

## Skill Level Requirements

### Pure Self-Hosted (Docker Compose)

**Minimum Skills**:
- [ ] Basic Linux command line
- [ ] Docker fundamentals (run, compose, logs)
- [ ] SSH access and security
- [ ] DNS configuration
- [ ] SSL/TLS basics (Let's Encrypt)

**Time to Learn (if starting from zero)**: 20-40 hours

**Recommended Prerequisites**:
- Comfortable with terminal/command line
- Can follow technical documentation
- Basic troubleshooting mindset

---

### Pure Self-Hosted (Native VPS)

**Minimum Skills**:
- [ ] Linux system administration (intermediate)
- [ ] LAMP/LEMP stack configuration
- [ ] MySQL/PostgreSQL administration
- [ ] Apache/Nginx configuration
- [ ] PHP version management (for LAMP)
- [ ] Server security hardening

**Time to Learn (if starting from zero)**: 40-80 hours

---

### Managed Open Source

**Minimum Skills**:
- [ ] Can fill out a web form
- [ ] Basic CRM configuration
- [ ] Data import/export (CSV)

**Time to Learn**: 0-4 hours (just the CRM itself, not infrastructure)

---

## Ongoing Time Commitment

| Deployment Model | Setup Time | Monthly Maintenance | Skill Level Required |
|------------------|------------|---------------------|----------------------|
| **Pure Self-Hosted (Docker)** | 1-4 hours | 2-4 hours | Intermediate |
| **Pure Self-Hosted (Native)** | 2-8 hours | 3-6 hours | Intermediate-Advanced |
| **Kubernetes** | 8-16 hours | 4-12 hours | Advanced |
| **Managed Open Source** | 0.25-1 hour | 0-1 hour | Beginner |

---

## Infrastructure Scaling Guide

### Small Team (3-10 users)

**Pure Self-Hosted**:
- **VPS**: $20-40/month (4GB RAM, 2 vCPU)
- **Platforms**: All four work well
- **Recommended**: EspoCRM (easiest) OR Twenty (modern)

**Managed Open Source**:
- **Cost**: $45-1,000/month ($15-100/user × 3-10)
- **Recommended**: EspoCRM Cloud (cheapest), Twenty CloudStation (flat pricing)

**Breakeven**: ~5-10 users (self-hosted becomes cheaper)

---

### Medium Team (10-50 users)

**Pure Self-Hosted**:
- **VPS**: $40-100/month (8GB RAM, 4 vCPU)
- **Platforms**: All four, Odoo for comprehensive needs
- **Recommended**: Odoo (if need suite), Twenty (if CRM-only)

**Managed Open Source**:
- **Cost**: $150-5,000/month
- **Recommended**: Odoo.sh (if can afford), self-hosted otherwise

**Breakeven**: ~10-20 users (self-hosted much cheaper)

---

### Large Team (50-200 users)

**Pure Self-Hosted**:
- **VPS**: $100-300/month (16-32GB RAM, 8 vCPU) OR Kubernetes
- **Platforms**: Odoo (proven scale), SuiteCRM (Salesforce alternative)
- **Recommended**: Odoo with dedicated ops person

**Managed Open Source**:
- **Cost**: $750-20,000/month
- **Consideration**: At this scale, self-hosted saves $5-15K/month

**Breakeven**: Already past breakeven, self-hosted clear winner on cost

---

### Enterprise (200+ users)

**Pure Self-Hosted**:
- **Infrastructure**: Kubernetes cluster OR high-availability VPS setup
- **Cost**: $200-1,000/month infrastructure + dedicated DevOps role
- **Platforms**: Odoo Enterprise (with support contract)

**Managed Open Source**:
- **Cost**: $3,000-20,000+/month
- **Consideration**: May need managed for support/SLA

**Decision**: Cost vs operational burden
- Self-hosted saves $30K-200K/year
- But requires dedicated DevOps team ($80K-120K/year)
- Breakeven: ~50-100 users (depending on DevOps cost)

---

## Backup Strategy

### Pure Self-Hosted

**Database Backups** (critical):
```bash
# PostgreSQL (Twenty, Odoo)
docker exec postgres pg_dump -U username dbname > backup.sql

# MySQL (SuiteCRM, EspoCRM)
docker exec mysql mysqldump -u username -p dbname > backup.sql
```

**Frequency**:
- Daily automated backups (cron job)
- Weekly backup testing (restore to staging)
- Monthly offsite backup (S3, Backblaze B2)

**Retention**:
- Daily: 7 days
- Weekly: 4 weeks
- Monthly: 12 months

**Tools**: restic, duplicity, borg, OR cloud provider snapshots

---

### Managed Open Source

**Included** - vendor handles backups

**Best Practice**:
- Export data monthly (CSV/API) as additional safety
- Store exports in separate location (S3, Google Drive)

---

## Security Considerations

### Pure Self-Hosted

**Checklist**:
- [ ] Firewall configured (ufw, iptables)
- [ ] SSH key-only (disable password auth)
- [ ] SSL/TLS enabled (Let's Encrypt)
- [ ] Database not exposed to internet
- [ ] Regular OS updates (unattended-upgrades)
- [ ] Application updates monthly
- [ ] Strong database passwords
- [ ] Two-factor authentication enabled (platform level)
- [ ] Backup encryption

**Tools**:
- **Firewall**: ufw (Ubuntu), firewalld (CentOS)
- **SSL**: certbot (Let's Encrypt)
- **Monitoring**: Netdata, Grafana
- **Intrusion Detection**: fail2ban

---

### Managed Open Source

**Vendor responsibility**: Infrastructure security, SSL, patches

**Your responsibility**: Platform-level security
- Strong passwords
- Two-factor authentication
- User permissions
- Data export/backup

---

## Summary Recommendations

| Team Size | Budget | DevOps Skills | Recommended Deployment |
|-----------|--------|---------------|------------------------|
| **3-10 users** | Low (<$500/yr) | Intermediate | Self-hosted EspoCRM (shared hosting OR Docker) |
| **3-10 users** | Medium ($500-2K/yr) | Beginner | Managed EspoCRM Cloud OR Twenty CloudStation |
| **10-50 users** | Low-Medium | Intermediate | Self-hosted Twenty/Odoo (Docker) |
| **10-50 users** | High (>$5K/yr) | Beginner | Managed Odoo.sh |
| **50-200 users** | Any | Advanced | Self-hosted Odoo (Docker OR K8s) + DevOps role |
| **200+ users** | High | Advanced | Odoo Enterprise (managed OR self-hosted with support) |

---

**Last Updated**: 2025-10-21
