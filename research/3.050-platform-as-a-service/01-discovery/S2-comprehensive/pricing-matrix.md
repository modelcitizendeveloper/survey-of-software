# PaaS Provider Pricing Matrix

**Experiment:** 3.050 Platform-as-a-Service
**Stage:** S2 Comprehensive Discovery
**Date:** 2025-10-09

---

## Quick Summary: Cost for Small Flask App (Web + Database)

| Provider | Free Tier | Entry Paid Tier | With Database | Notes |
|----------|-----------|----------------|---------------|-------|
| **PythonAnywhere** | $0 (limited, no custom domain) | $5/month | $5 (MySQL included) | Cheapest paid option |
| **Heroku** | NONE | $5/month (Eco) | $10/month (+$5 DB) | Eco dynos sleep |
| **Render** | $0 (sleeps, DB 90-day limit) | $7/month | $14/month (+$7 DB) | Free tier usable for demos |
| **Railway** | $5 trial (one-time) | $5/month + usage | ~$15-20/month | Usage-based, unpredictable |
| **Fly.io** | NONE | ~$5-6/month | ~$15/month (DIY DB) | Requires Docker |
| **DigitalOcean** | $0 (static only) | $5/month | $12/month (+$7 DB) | Solid middle ground |
| **Vercel** | $0 (100 GB bandwidth) | $20/month/user | N/A | NOT for Flask apps! |
| **Google Cloud Run** | $0 (2M req/month) | ~$0-5/month | ~$10-20/month | Serverless, cold starts |

---

## Detailed Pricing Breakdown

### 1. PythonAnywhere

#### Free Tier (Beginner Account)
- **Cost:** $0/month
- **Web Apps:** 1 app (subdomain only)
- **Storage:** ~500 MB
- **CPU:** 100 CPU-seconds/day (very limited)
- **Custom Domain:** NO
- **Database:** MySQL (in storage quota)
- **Outbound Internet:** Restricted (whitelist only)
- **SSH:** NO
- **Limitations:** Essentially unusable for real apps (internet restrictions, CPU limits)

#### Hacker Plan (Entry Paid)
- **Cost:** $5/month
- **Web Apps:** 1 app
- **Storage:** 1 GB
- **CPU:** 2,000 CPU-seconds/day
- **Custom Domain:** Unlimited with free SSL
- **Database:** MySQL included (in quota), Postgres +$7/month
- **Outbound Internet:** Unrestricted
- **SSH:** YES
- **Performance:** ~100K hits/day

#### Higher Tiers
- **Web Dev:** ~$12/month (3 apps, 3 GB storage)
- **Custom:** Up to $500/month

**Pricing Model:** Fixed monthly tiers

---

### 2. Heroku

#### Free Tier
- **Status:** ELIMINATED (Nov 2022)

#### Eco Dyno Plan
- **Cost:** $5/month subscription
- **Resources:** 1,000 dyno hours/month pool (shared across all Eco dynos)
- **Dyno Specs:** 512 MB RAM, shared CPU
- **Sleep:** YES (after 30 min inactivity)
- **Auto-Scaling:** NO
- **Database:** NOT included
- **Limitations:** Max 2 concurrent dynos, personal apps only

#### Basic Dyno
- **Cost:** $7/month per dyno
- **Specs:** 512 MB RAM, shared CPU
- **Sleep:** NO (always on)
- **Database:** NOT included

#### Performance Dynos
- **Standard-1X:** $25-50/month (512 MB, dedicated CPU)
- **Standard-2X:** $50-100/month (1 GB)
- **Performance-M:** $250/month (2.5 GB)

#### Database (Heroku Postgres)
- **Mini:** $5/month (1 GB storage)
- **Basic:** $9/month (10 GB)
- **Standard-0:** $50/month (64 GB, HA)

**Small Flask App Total:** $10/month (Eco $5 + DB $5)

**Pricing Model:** Fixed dyno tiers + database add-ons

---

### 3. Render

#### Free Tier
- **Cost:** $0/month (no credit card)
- **Web Service:** 512 MB RAM, shared CPU (0.1 CPU)
- **Sleep:** YES (after 15 min inactivity)
- **Bandwidth:** Limited
- **Build Minutes:** Limited monthly
- **Custom Domain:** YES (with free SSL)
- **Database:** Free Postgres (DELETED after 90 days!)
- **Limitations:** Cold starts 30-60 sec, database not persistent

#### Starter (Entry Paid Web Service)
- **Cost:** $7/month
- **Specs:** 512 MB RAM, 0.5 shared CPU
- **Sleep:** NO (always on)
- **Bandwidth:** 100 GB/month included
- **Build Minutes:** 500/month
- **Database:** NOT included

#### Standard
- **Cost:** $25/month
- **Specs:** 1 vCPU, 2 GB RAM
- **Bandwidth:** 400 GB/month
- **Auto-Scaling:** YES

#### Database (Postgres)
- **Starter:** $7/month (1 GB, 256 MB RAM)
- **Standard:** $20/month (10 GB, 1 GB RAM)
- **Pro:** $90/month (50 GB, 4 GB RAM, HA)

**Small Flask App Total:** $14/month (Starter $7 + DB $7)

**Pricing Model:** Fixed tiers + bandwidth/build minute overages

---

### 4. Railway

#### Trial
- **Cost:** $0 (one-time)
- **Credit:** $5 (expires in 30 days)
- **Not a recurring free tier**

#### Hobby Plan
- **Cost:** $5/month subscription + usage
- **Includes:** $5 of usage credits per month
- **How It Works:**
  - Usage ≤ $5 → Pay only $5
  - Usage > $5 → Pay $5 + (usage - $5)
- **Resource Limits:** 8 vCPU, 8 GB RAM, 5 GB storage per service

#### Usage Pricing
- **CPU:** $20/vCPU/month (~$0.67/day)
- **Memory:** $10/GB/month (~$0.33/day)
- **Network Egress:** $0.10/GB
- **Database:** Included in usage (storage + memory billed)

**Small Flask App Estimate:**
- 0.5 vCPU: $10/month
- 512 MB RAM: $5/month
- Small Postgres (500 MB): ~$2-3/month
- **Total: ~$17-20/month**

**Pricing Model:** Usage-based (per-minute billing)

---

### 5. Fly.io

#### Free Tier
- **Status:** ELIMINATED for new orgs (2024)

#### Usage-Based Pricing
- **Machines:** Billed per-second by CPU/RAM preset
  - shared-cpu-1x (256 MB): ~$2-3/month
  - shared-cpu-1x (512 MB): ~$4-5/month
  - shared-cpu-1x (1 GB): ~$7-8/month
- **Storage:** $0.15/GB/month
- **Network Egress:** $0.02/GB (starting rate)
- **IPv4:** Dedicated ~$2/month

**Regional Pricing Variance:** Some regions more expensive

**Small Flask App (Single Region):**
- 1x shared-cpu (512 MB): ~$5/month
- 1 GB storage: $0.15/month
- Minimal egress: ~$0.50/month
- **Total: ~$6/month**

**Multi-Region (3 regions):**
- 3x machines: ~$15/month
- **Total: ~$20-25/month**

**Database:** DIY (run Postgres as Fly app), not fully managed

**Pricing Model:** Usage-based (per-second)

---

### 6. DigitalOcean App Platform

#### Free Tier
- **Cost:** $0/month
- **Static Sites Only:** 3 free static apps
- **Web Services:** NOT free

#### Basic Web Service
- **Cost:** $5/month
- **Specs:** 512 MB RAM, shared vCPU
- **Bandwidth:** 40 GB/month included
- **Auto-Scaling:** NO
- **Containers:** 1

#### Professional Web Service
- **Cost:** $12/month
- **Specs:** 1 GB RAM, shared vCPU
- **Bandwidth:** 100 GB/month
- **Auto-Scaling:** YES (1-10 containers)

#### Database
- **Basic:** $7/month (10 GB storage, 1 GB RAM, 25 connections)
- **Professional:** $15/month (25 GB)

**Small Flask App Total:** $12/month (Basic $5 + DB $7)

**Pricing Model:** Fixed modular tiers

---

### 7. Vercel

#### Hobby Plan (Free)
- **Cost:** $0/month
- **Bandwidth:** 100 GB/month
- **Serverless Functions:** 100,000 invocations/month
- **Edge Functions:** 1,000,000/month
- **Custom Domains:** Unlimited with SSL
- **Limitations:** 1 team member, 10-sec function timeout

#### Pro Plan
- **Cost:** $20/month per user
- **Bandwidth:** 1 TB/month
- **Serverless Functions:** 1,000,000/month
- **Build Time:** 400 hours/month
- **Overages:**
  - Bandwidth: $40 per 100 GB (expensive!)
  - Functions: $2 per million

**NOT SUITABLE FOR TRADITIONAL FLASK APPS** - Serverless functions only

**Pricing Model:** Fixed plan + usage overages

---

### 8. Google Cloud Run

#### Free Tier (Always Free)
- **Cost:** $0/month (up to limits)
- **Requests:** 2,000,000/month
- **CPU:** 180,000 vCPU-seconds/month
- **Memory:** 360,000 GiB-seconds/month
- **Network Egress:** 1 GB/month (North America)

#### Usage-Based Pricing
- **vCPU-seconds:** ~$0.000024 per vCPU-sec
- **GiB-seconds (Memory):** ~$0.0000025 per GiB-sec
- **Requests:** $0.40 per million (after free tier)
- **Network Egress:** ~$0.12/GB

**Small Flask App (10K req/month):**
- Likely FREE (under 2M req limit)
- Estimated: $0.03/month

**Medium Flask App (100K req/month):**
- **Estimated: $0.30-$1/month**

**High Traffic (1M req/month):**
- **Estimated: $5-15/month** (varies by response time)

**Database (Cloud SQL):**
- **Basic:** $7-10/month
- **Production:** $50+/month

**Small Flask App Total:** ~$10-20/month (serverless + Cloud SQL)

**Pricing Model:** True usage-based (pay-per-request)

---

## Pricing Comparison Table

### Monthly Cost: Small Flask App (Always-On Web Service + Database)

| Provider | Free Option | Entry Cost | Always-On + DB | Auto-Scaling Tier |
|----------|-------------|------------|----------------|-------------------|
| **PythonAnywhere** | $0 (very limited) | $5 | $5 (MySQL incl.) | Not available |
| **Heroku** | NONE | $5 (sleeps) | $10 ($5+$5) | $75+ (Perf+DB) |
| **Render** | $0 (sleeps, 90-day DB) | $7 (no sleep) | $14 ($7+$7) | $45 ($25+$20) |
| **Railway** | $5 trial (once) | $5 + usage | ~$15-20 | N/A (manual) |
| **Fly.io** | NONE | ~$6 | ~$15 (DIY DB) | N/A (manual) |
| **DigitalOcean** | NONE (static only) | $5 | $12 ($5+$7) | $27 ($12+$15) |
| **Vercel** | $0 (not for Flask) | N/A | N/A | N/A |
| **Google Cloud Run** | $0 (low traffic) | ~$0-5 | ~$10-20 | Included |

---

## Key Pricing Insights

### Cheapest Options
1. **PythonAnywhere $5/month** - Fixed, predictable, MySQL included
2. **Heroku $10/month** - But Eco sleeps (frustrating)
3. **DigitalOcean $12/month** - Solid middle ground
4. **Render $14/month** - Modern, no sleep

### Best Value for Low Traffic
- **Google Cloud Run:** $0-1/month (but cold starts)
- **PythonAnywhere:** $5/month (simple, predictable)

### Best Value for Variable Traffic
- **Google Cloud Run:** Pay-per-request (scale to zero)
- **Railway:** Usage-based (but can be expensive)

### Most Expensive (Small Apps)
- **Vercel Pro:** $20/month per user (overkill for Flask)
- **Railway:** ~$15-20/month (usage-based)

### Free Tier Winners
1. **Render:** Free tier with custom domains (but sleeps + 90-day DB)
2. **Google Cloud Run:** 2M requests/month (but cold starts)
3. **Vercel:** 100 GB bandwidth (but not for Flask)

### Free Tier Losers
- **Heroku:** NONE
- **Fly.io:** NONE (new users)
- **Railway:** One-time $5 trial

---

## Pricing Models Summary

| Model | Providers | Pros | Cons |
|-------|-----------|------|------|
| **Fixed Tiers** | PythonAnywhere, Heroku, Render, DigitalOcean | Predictable | Pay for unused capacity |
| **Usage-Based** | Railway, Fly.io, Google Cloud Run | Pay only for actual usage | Unpredictable bills |
| **Hybrid** | Render, Vercel | Base + overages | Complexity |

---

## Recommendation by Budget

### $0/month (Free Only)
- **Render Free Tier** (accept 15-min sleep, 90-day DB limit)
- **Google Cloud Run** (if very low traffic, accept cold starts)

### $5-10/month
- **PythonAnywhere $5** (simplest, MySQL included)
- **Heroku $10** (Eco + DB, but sleeps)
- **Fly.io ~$6** (Docker required, DIY DB)

### $10-15/month
- **DigitalOcean $12** (solid, predictable)
- **Render $14** (modern, no sleep)
- **Railway ~$15** (usage-based, great DX)

### $20-30/month
- **Render Standard $45** (auto-scaling)
- **DigitalOcean Professional $27** (scaling)

### Variable Traffic (Pay-Per-Use)
- **Google Cloud Run** (best for spiky traffic)
- **Railway** (good DX, variable cost)

---

## For QRCards Current Stage

**Budget-Conscious:** PythonAnywhere $5 (current choice, good fit)
**Modernize:** Render $14 (git auto-deploy, no sleep)
**Flexibility:** Railway ~$15-20 (beautiful UI, usage-based)
**Free Demo:** Render free tier (accept sleep, 90-day DB)

**NOT Recommended:** Heroku (too expensive), Fly.io (too complex), Vercel (incompatible), Cloud Run (overkill)
