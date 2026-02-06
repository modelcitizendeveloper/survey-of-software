# Fly.io - Provider Analysis

**Platform Type:** Edge PaaS (VM-Based Global Deployment)
**Website:** https://fly.io/
**Founded:** 2017 (7+ years in market)
**Positioning:** "Deploy app servers close to your users"

## Overview & Positioning

Fly.io is a **global edge platform** that runs applications as **full VMs** (not containers) in **30+ regions worldwide**. Unlike traditional PaaS providers that run in 1-4 regions, Fly.io deploys your app **close to users globally** for sub-100ms latency.

**Key Innovation:**
- **Edge deployment:** Run in Sydney, São Paulo, Tokyo, Frankfurt simultaneously
- **Anycast routing:** Users connect to nearest region automatically
- **Full VMs:** Run any process, not just web servers
- **WireGuard VPN:** Private networking between regions

**Market Position:** Targets applications needing **global low-latency** (real-time apps, APIs, gaming, international services).

**Major 2024 Change:** **Eliminated free tier** for new organizations (legacy free users grandfathered).

---

## 1. Pricing Structure

### Free Tier
**ELIMINATED for new organizations** (2024)

Legacy users who created accounts before elimination may still have free allowances.

**For New Users:** No free tier - must pay for usage.

---

### Usage-Based Pricing (Pay-As-You-Go)

Fly.io charges **per-second** for provisioned resources.

**What You Pay For:**

**1. Virtual Machines (Fly Machines)**
- Billed per second while running
- Price varies by CPU/RAM preset and region
- Example pricing (us-central region):
  - shared-cpu-1x (256 MB): ~$2-3/month
  - shared-cpu-1x (512 MB): ~$4-5/month
  - shared-cpu-1x (1 GB): ~$7-8/month
  - performance-1x (2 GB): ~$25-30/month

**Regional Pricing Variance:** Some regions cost more (Asia, South America).

**2. Storage (Volumes)**
- $0.15/GB/month
- Persistent SSD storage

**3. Network Egress (Bandwidth)**
- $0.02/GB starting rate
- Varies by region
- Ingress is free

**4. IP Addresses**
- IPv6: Free
- IPv4 (shared): Free (limited)
- Dedicated IPv4: ~$2/month each

---

### Minimum Cost Estimate

**Minimal Flask App (Single Region):**
- 1x shared-cpu-1x (512 MB RAM): ~$5/month
- 1 GB storage: $0.15/month
- Minimal egress: ~$0.50/month
- **Total: ~$6/month**

**Global Flask App (Multi-Region):**
- 3x shared-cpu-1x (512 MB) in US/EU/Asia: ~$15/month
- 3 GB storage: $0.45/month
- Moderate egress: ~$5/month
- **Total: ~$20-25/month**

---

### No Fixed Tiers

Unlike Heroku/Render, Fly.io has **no fixed plans**:
- Pay only for provisioned resources
- Scale CPU/memory independently
- Billing granularity: per second

---

## 2. Deployment Methods

### Primary Method: Dockerfile + flyctl CLI

Fly.io is **Docker-native** - you MUST provide a Dockerfile or let Fly generate one.

#### Step-by-Step Flask Deployment

**Prerequisites:**
- Install `flyctl` CLI
- Docker installed (for local testing)
- Fly.io account

**1. Install flyctl:**
```bash
# macOS
brew install flyctl

# Linux
curl -L https://fly.io/install.sh | sh

# Authenticate
flyctl auth login
```

**2. Project Structure:**
```
flask-flyio-app/
├── app.py
├── requirements.txt
├── Dockerfile
└── .dockerignore
```

**3. Create Dockerfile:**

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
```

**requirements.txt:**
```
Flask==3.0.0
gunicorn==21.2.0
```

**4. Initialize Fly App:**
```bash
flyctl launch
```

This command:
- Detects Dockerfile
- Prompts for app name
- Asks which region(s) to deploy
- Generates `fly.toml` configuration file

**5. Deploy:**
```bash
flyctl deploy
```

Fly.io:
- Builds Docker image
- Pushes to Fly's registry
- Creates VMs in selected regions
- Deploys app

**Deployment Time:** 3-5 minutes (first deploy)

**6. Access App:**
```bash
flyctl open
```

App is live at `https://your-app.fly.dev`

---

### Auto-Generated Dockerfile

If you don't provide a Dockerfile, `flyctl launch` can generate one:

```bash
flyctl launch
# Detects Python app
# Generates Dockerfile automatically
# Creates fly.toml
```

Generated Dockerfile uses Python buildpack-like approach.

---

### Configuration File: fly.toml

`flyctl launch` creates `fly.toml`:

```toml
app = "flask-flyio-app"
primary_region = "iad"

[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "8080"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = false
  auto_start_machines = true
  min_machines_running = 1

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 512
```

---

### Multi-Region Deployment

Deploy to multiple regions for global coverage:

```bash
# Scale to 3 regions
flyctl regions add iad lhr sin

# Deploy creates VMs in all regions
flyctl deploy
```

Users automatically routed to nearest region via **Anycast**.

---

### CI/CD Integration

**GitHub Actions:**
```yaml
name: Deploy to Fly.io
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: superfly/flyctl-actions/setup-flyctl@master
      - run: flyctl deploy --remote-only
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

---

## 3. Features

### Auto-Scaling
**Automatic Machine Start/Stop:**
- Machines can auto-start on request
- Auto-stop when idle (configurable)
- Horizontal scaling: Add more machines manually

**NOT automatic load-based autoscaling** like Heroku Performance dynos.

### Custom Domains & SSL
- **Free SSL:** Automated certificates for all domains
- **Custom domains:** Unlimited
- **Setup:** `flyctl certs add yourdomain.com`
- **Wildcard domains:** Supported

### Database Add-Ons
**Fly Postgres (Managed by Fly, not fully managed):**
- Postgres running as Fly app (not external service)
- Deploy via `flyctl postgres create`
- HA configurations available
- YOU manage backups, scaling, etc.

**Fly Redis (Similar Model):**
- Redis as Fly app
- Upstash Redis integration available (external service)

**NO one-click databases** like Railway/Render - more DIY.

### Environment Management
**Secrets:**
```bash
flyctl secrets set DATABASE_URL=postgres://...
flyctl secrets set SECRET_KEY=xyz
```

**Environments:** No built-in staging/production - create separate apps.

### Monitoring & Logs
**Included:**
- `flyctl logs` - Real-time log streaming
- Fly.io dashboard - Basic metrics
- `flyctl status` - VM status

**Advanced Monitoring:** Integrate with Datadog, Prometheus, Grafana.

### CI/CD Integration
- **GitHub Actions:** Official action available
- **GitLab CI:** Supported via flyctl
- **API:** Full API for custom workflows

### Region/Edge Deployment
**THIS IS FLY.IO'S KILLER FEATURE**

**30+ Regions Worldwide:**
- North America: 10+ (US, Canada, Mexico)
- Europe: 10+ (UK, Germany, France, Amsterdam, etc.)
- Asia-Pacific: 10+ (Tokyo, Singapore, Sydney, India, etc.)
- South America: São Paulo
- Africa: Johannesburg

**Anycast Routing:** Users automatically connect to nearest region.

**Use Case:** Global SaaS, real-time apps, APIs serving international users.

### Background Workers
**Full VMs = Run Anything:**
- Web servers
- Background workers
- Cron jobs
- Long-running processes

Define multiple processes in `fly.toml`:
```toml
[processes]
  web = "gunicorn app:app"
  worker = "celery -A app worker"
```

---

## 4. Python/Flask Support

### Native Python Support
**Docker-Based** - No buildpack magic, must configure Dockerfile.

**Python Versions:** Any version you specify in Dockerfile (3.7-3.12+).

### Flask Deployment
**Requires:**
- Dockerfile
- Gunicorn or similar WSGI server
- Expose correct port (default 8080)

**No Flask-specific features** - treat like any Docker container.

### WSGI Server
**Gunicorn (Recommended):**
```dockerfile
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--workers", "4"]
```

**uWSGI:**
```dockerfile
CMD ["uwsgi", "--http", ":8080", "--wsgi-file", "app.py", "--callable", "app"]
```

### Package Managers
- **pip:** Standard (requirements.txt)
- **Pipenv:** Supported (copy Pipfile in Dockerfile)
- **Poetry:** Supported (install poetry in Dockerfile)

---

## 5. Pros & Cons

### Advantages

1. **Global Edge Deployment (30+ Regions)**
   - Sub-100ms latency worldwide
   - Anycast routing to nearest region
   - UNIQUE among PaaS providers

2. **Full VM Control**
   - Run any process, not just web apps
   - SSH access to VMs
   - Complete flexibility

3. **Pay-Per-Second Billing**
   - No wasted spend on idle resources
   - Transparent usage-based pricing

4. **Docker-Native**
   - Full control over environment
   - Easy migration to Kubernetes
   - Reproducible builds

5. **WireGuard Private Networking**
   - Secure inter-region communication
   - Build distributed systems

### Disadvantages

1. **NO Free Tier**
   - Must pay from day one
   - Minimum ~$5-6/month

2. **Requires Docker Knowledge**
   - Must write/maintain Dockerfile
   - Steeper learning curve than buildpack PaaS
   - Not beginner-friendly

3. **Database Management DIY**
   - Postgres is "run-it-yourself" on Fly
   - No fully managed database option
   - More DevOps burden

4. **Complexity**
   - fly.toml configuration
   - CLI-first (no GUI deployment wizard)
   - Multi-region complexity

5. **Cost Unpredictability**
   - Usage-based billing can surprise
   - Multi-region deployments multiply costs

6. **Smaller Ecosystem**
   - Less community knowledge than Heroku
   - Fewer tutorials/guides

---

## 6. Best Use Cases

### Ideal For:
- **Global applications** needing low latency worldwide
- **Real-time apps** (gaming, chat, collaboration tools)
- **International SaaS** serving users across continents
- **API-first products** with global customer base
- **Docker-savvy teams**
- **Distributed systems** (multi-region architecture)

### NOT Ideal For:
- **Beginners** (too complex)
- **Hobby projects** (no free tier, Docker required)
- **Single-region apps** (pay premium for unused global features)
- **Teams unfamiliar with Docker**
- **Budget-constrained projects** (Railway/Render/PythonAnywhere cheaper)

---

## 7. Comparison to Alternatives

### vs. PythonAnywhere
- **Global vs. Single Region:** Fly.io 30+ regions vs. US East only
- **Docker vs. WSGI:** More complex vs. simpler
- **More Expensive:** $6+ vs. $5/month
- **More Flexible:** Full VM control vs. Python-only

### vs. Heroku
- **Edge vs. Regional:** Fly.io global vs. 5 Heroku regions
- **Docker vs. Buildpacks:** More control vs. simpler
- **Similar Pricing:** Both ~$5-10/month minimum
- **Fly More Modern:** Newer architecture

### vs. Render
- **Global vs. Regional:** Fly.io 30+ vs. Render 4 regions
- **Docker-Required vs. Optional:** Fly mandates Docker
- **No Free Tier:** Both similar (Render free has sleep)
- **Fly Better for Global:** If you need worldwide deployment

### vs. Railway
- **Similar Pricing:** Both usage-based
- **Fly More Complex:** Dockerfile required vs. auto-detect
- **Fly More Global:** 30+ regions vs. 3
- **Railway Better DX:** Simpler UI, easier deployment

---

## 8. Flask Deployment Example

### Complete Flask App on Fly.io

**app.py:**
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Flask on Fly.io!'
```

**requirements.txt:**
```
Flask==3.0.0
gunicorn==21.2.0
```

**Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
```

**Deploy:**
```bash
flyctl launch
flyctl deploy
flyctl open
```

**Multi-Region:**
```bash
flyctl regions add lhr sin
flyctl deploy
```

App now runs in 3 regions (US, London, Singapore).

---

## 9. Summary Verdict

**Fly.io is the "global edge specialist"** - if you need sub-100ms latency worldwide, Fly.io is unmatched. But you pay for complexity and Docker requirement.

**Best For:** Global apps, real-time services, international SaaS, Docker-savvy teams
**Avoid For:** Beginners, hobby projects, single-region apps, teams unfamiliar with Docker

**For QRCards:**
- **Current Stage:** Overkill - QRCards likely doesn't need 30 regions
- **Cost:** More expensive than PythonAnywhere/Render for single-region
- **Complexity:** Docker requirement adds friction
- **Recommendation:** **Not recommended** unless QRCards goes global

**Fly.io's 2025 Position:** Best-in-class for global deployment, but niche use case. Most apps don't need 30 regions.
