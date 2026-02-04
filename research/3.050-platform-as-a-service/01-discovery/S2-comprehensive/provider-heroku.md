# Heroku - Provider Analysis

**Platform Type:** Classic PaaS (Pioneer)
**Website:** https://www.heroku.com/
**Parent Company:** Salesforce (acquired 2010)
**Founded:** 2007 (17+ years in market)

## Overview & Positioning

Heroku is the **original Platform-as-a-Service** that popularized the "git push to deploy" model and buildpack architecture. It's the industry standard reference point for PaaS platforms.

**Key Innovation:** Introduced the concept of:
- Buildpacks (language-agnostic deployment)
- Add-on marketplace (databases, monitoring, etc.)
- Procfile-based process management
- Dyno architecture (containerized app instances)

**Market Position:** Premium PaaS targeting professional developers and teams. Known for developer experience and extensive add-on ecosystem, but **significantly more expensive** since removing free tier in 2022.

**Major 2022 Change:** Eliminated free tier, causing mass exodus to alternatives (Render, Railway, Fly.io).

---

## 1. Pricing Structure

### Free Tier
**ELIMINATED in November 2022**

Previously offered free dynos and databases - no longer available.

---

### Eco Dyno Plan (Lowest Paid Tier)

**Monthly Cost:** $5/month subscription

**What $5 Gets You:**
- **Pool of 1,000 Eco dyno hours/month** (shared across all Eco dynos)
- **Example:** Can run ONE dyno 24/7 (730 hours/month) + partial second dyno
- **OR:** Run multiple apps part-time that sum to 1,000 hours

**Eco Dyno Specifications:**
- **CPU:** Shared CPU (not dedicated) - CPU-share basis
- **Memory:** 512 MB RAM
- **Processes/Threads:** Max 256 concurrent
- **Scaling Limit:** 1 dyno per process type (web/worker)
- **Max Concurrent Dynos:** 2 total per app

**Sleep Behavior:**
- If Eco web dyno receives **no traffic for 30 minutes**, it sleeps
- Sleeping dynos **do not consume Eco hours** (cost savings)
- Worker dynos also sleep when web dyno sleeps
- Cold start when traffic resumes (slower first request)

**Limitations:**
- **NO auto-scaling** (Eco dynos don't support autoscaling)
- **Personal apps only** (not for Heroku Teams/Enterprise)
- Must manually scale up to Performance dynos for production

---

### Basic Dyno Plan

**Monthly Cost:** $7/month per dyno

**Specifications:**
- **CPU:** Shared CPU
- **Memory:** 512 MB RAM
- **Sleep:** Never sleeps (always on)
- **Scaling:** Can scale horizontally (multiple dynos)

**Better for:** Apps needing guaranteed uptime without sleep

---

### Performance Dynos (Production)

**Standard-1X:** $25-50/month per dyno
- **CPU:** Dedicated CPU core
- **Memory:** 512 MB RAM
- **Auto-scaling:** Supported

**Standard-2X:** $50-100/month per dyno
- **Memory:** 1 GB RAM
- **CPU:** 2x performance

**Performance-M:** $250/month per dyno
- **Memory:** 2.5 GB RAM
- **CPU:** High performance

**Performance-L:** $500/month per dyno
- **Memory:** 14 GB RAM
- **CPU:** Highest performance

---

### Database Add-Ons (Heroku Postgres)

**Mini:** $5/month
- 1 GB storage
- 20 connections
- No followers (no read replicas)

**Basic:** $9/month
- 10 GB storage
- 20 connections
- Automated backups

**Standard-0:** $50/month
- 64 GB storage
- 120 connections
- High availability, automated failover

**Premium Plans:** $200-$5,000+/month for production databases

---

### Additional Costs

| Resource | Cost |
|----------|------|
| SSL Certificates | Free (automated SSL) |
| Custom Domains | Free (unlimited) |
| Bandwidth | Included (no overage charges) |
| Build Minutes | Included |
| Dyno hours (Eco) | $5 for 1,000 hours |
| Redis (Mini) | $3/month |
| Scheduler (cron jobs) | Free add-on |

---

### Total Cost Example (Small Flask App)

**Minimal Setup:**
- 1 Eco dyno (web): $5/month (1,000 hours pool)
- Heroku Postgres Mini: $5/month
- **Total: $10/month**

**Production Setup:**
- 2 Standard-1X dynos (web): $50-100/month
- Heroku Postgres Standard-0: $50/month
- Redis Mini: $3/month
- **Total: ~$103-153/month**

---

## 2. Deployment Methods

### Primary Method: Git Push Deployment

Heroku pioneered the **"git push to deploy"** workflow that's now industry standard.

#### Step-by-Step Flask Deployment

**Prerequisites:**
- Heroku CLI installed
- Git repository
- Heroku account with payment method

**1. Project Structure:**
```
myflaskapp/
├── app.py
├── requirements.txt
├── Procfile
├── runtime.txt (optional)
└── .gitignore
```

**2. Create Files:**

**app.py:**
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello from Heroku!'

if __name__ == '__main__':
    app.run()
```

**requirements.txt:**
```
Flask==3.0.0
gunicorn==21.2.0
```

**Procfile** (REQUIRED):
```
web: gunicorn app:app
```

**runtime.txt** (optional - specifies Python version):
```
python-3.11.5
```

**3. Deployment Commands:**

```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create my-flask-app

# Add Postgres database (if needed)
heroku addons:create heroku-postgresql:mini

# Deploy
git add .
git commit -m "Initial deployment"
git push heroku main

# App is live at https://my-flask-app.herokuapp.com

# View logs
heroku logs --tail

# Scale dynos
heroku ps:scale web=1

# Open in browser
heroku open
```

**Deployment Time:** 2-5 minutes (after buildpack downloads)

---

### Buildpack System

Heroku uses **buildpacks** to detect language and install dependencies.

**Python Buildpack Auto-Detection:**
- Looks for `requirements.txt`, `Pipfile.lock`, `poetry.lock`, or `uv.lock`
- Automatically installs Python and dependencies
- Runs `pip install -r requirements.txt`

**Supported Dependency Managers:**
- pip (requirements.txt)
- Pipenv (Pipfile.lock)
- Poetry (poetry.lock)
- uv (uv.lock)

**Supported Python Versions:**
- Python 3.8, 3.9, 3.10, 3.11, 3.12
- Specify in `runtime.txt` or use latest

---

### Docker Deployment (Alternative)

Heroku also supports **container-based deployment** using Docker.

```bash
# Build container
heroku container:push web

# Release container
heroku container:release web
```

Requires `Dockerfile` instead of buildpack.

---

### CI/CD Integration

**GitHub Integration:**
- Connect repo to Heroku app
- Auto-deploy on push to main branch
- Wait for CI to pass before deploy
- Review apps for pull requests

**GitLab CI/CD:** Supported via Heroku API
**Heroku Pipelines:** Built-in staging → production promotion

---

### Configuration Files

**Required:**
- `Procfile` - Process types (web, worker, etc.)
- `requirements.txt` (or Pipfile/poetry.lock)

**Optional:**
- `runtime.txt` - Python version
- `app.json` - App metadata for Review Apps
- `heroku.yml` - Container builds

---

## 3. Features

### Auto-Scaling
**ONLY on Performance Dynos** ($25+/month)

- Horizontal scaling: Add/remove dynos based on load
- Configured via CLI or web dashboard
- NOT available on Eco or Basic dynos

### Custom Domains & SSL
- **Unlimited custom domains:** Free
- **Automated SSL certificates:** Free (Let's Encrypt)
- **SNI SSL:** Free
- **Setup:** Add domain in dashboard, configure DNS CNAME

### Database Add-Ons
**Heroku Postgres (First-Class):**
- Fully managed PostgreSQL
- Automated backups (paid plans)
- High availability (Standard+ plans)
- Direct database access via `DATABASE_URL` env var

**Redis:** Heroku Redis add-on ($3-$500/month)
**MySQL:** Third-party add-ons (ClearDB, JawsDB)

### Environment Management
**Heroku Pipelines:**
- Staging → Production workflows
- Review Apps (ephemeral apps for PRs)
- Promotion between stages
- Excellent for team collaboration

**Config Vars:**
- Environment variables via CLI/dashboard
- Secure secrets management
- Auto-injected into app environment

### Monitoring & Logs
**Included (All Plans):**
- Real-time log streaming via CLI
- 1,500 log lines retained
- Basic metrics (response times, throughput)

**Heroku Metrics (Paid Apps):**
- Dyno load, memory, response times
- Historical data (2 hours to 30 days depending on plan)

**Add-On Ecosystem:**
- Papertrail (advanced logging)
- New Relic (APM)
- Sentry (error tracking)
- 200+ monitoring add-ons

### CI/CD Integration
**Best-in-Class:**
- GitHub auto-deploy
- Review Apps for PRs
- Heroku Pipelines
- Heroku CI (test runner)
- Pre/post-deploy hooks

### Region/Edge Deployment
**Regions:**
- US (Virginia, Oregon)
- Europe (Dublin, Frankfurt)
- Asia-Pacific (Tokyo, Sydney)

**NOT edge deployment** - Choose one region per app, no automatic global distribution

### Background Workers
**Worker Dynos:**
- Defined in Procfile: `worker: python worker.py`
- Scheduled tasks via Heroku Scheduler add-on (free)
- Long-running processes supported
- Separate dyno types (same pricing as web dynos)

---

## 4. Python/Flask Support

### Native Python Support
**Excellent** - Heroku has **first-class Python support** via official buildpack.

**Python Versions Supported:**
- Python 3.8, 3.9, 3.10, 3.11, 3.12
- Specify in `runtime.txt` or defaults to latest stable

### Flask-Specific Features

**Official Documentation:**
- Comprehensive Flask deployment guide
- Flask + Postgres tutorials
- Best practices for Gunicorn configuration

**Recommended Stack:**
- Flask framework
- Gunicorn WSGI server
- Heroku Postgres database
- WhiteNoise for static files

**Example Procfile for Flask:**
```
web: gunicorn app:app --log-file -
worker: python worker.py
release: python manage.py db upgrade
```

### WSGI Server Options

**Recommended: Gunicorn**
```
web: gunicorn app:app
web: gunicorn app:app --workers 4 --timeout 30
```

**Alternative: uWSGI**
```
web: uwsgi --http :$PORT --wsgi-file app.py --callable app
```

**Flask Development Server NOT RECOMMENDED for production**

### Package Manager Support
- **pip:** Full support (requirements.txt)
- **Pipenv:** Full support (Pipfile + Pipfile.lock)
- **Poetry:** Full support (poetry.lock)
- **uv:** Full support (uv.lock)

Buildpack auto-detects which package manager to use.

### Flask Extensions Compatibility
**All major Flask extensions work:**
- Flask-SQLAlchemy (with Heroku Postgres)
- Flask-Login
- Flask-Mail (via SendGrid add-on)
- Flask-Migrate
- Flask-WTF
- Flask-CORS

---

## 5. Pros & Cons

### Advantages

1. **Industry-Standard Developer Experience**
   - Git push to deploy (pioneered this model)
   - Buildpack system (no Docker knowledge required)
   - Procfile simplicity

2. **Massive Add-On Ecosystem**
   - 200+ add-ons (databases, monitoring, caching, etc.)
   - One-click provisioning
   - Integrated billing

3. **Excellent Documentation**
   - Comprehensive guides for Flask/Django
   - Years of community knowledge
   - Dev Center articles for every use case

4. **Enterprise-Grade Features**
   - Heroku Pipelines (staging/production)
   - Review Apps (PR previews)
   - Heroku Teams & Enterprise plans
   - SOC2, HIPAA compliance options

5. **Auto-Scaling** (on Performance dynos)
   - Horizontal scaling
   - Metrics-based autoscaling
   - Handle traffic spikes

6. **Mature Platform**
   - 17+ years in production
   - Battle-tested infrastructure
   - Owned by Salesforce (stability)

### Disadvantages

1. **NO Free Tier**
   - Removed in November 2022
   - Minimum $5/month (Eco) + $5 database = $10/month minimum
   - Caused mass migration to Render/Railway

2. **Expensive for Production**
   - Performance dynos: $25-500/month each
   - Production database: $50+/month
   - Typical production app: $100-300/month minimum

3. **Eco Dyno Limitations**
   - Sleeps after 30 min inactivity (slow cold starts)
   - Shared CPU (performance inconsistent)
   - No auto-scaling
   - Max 2 dynos per app

4. **Vendor Lock-In**
   - Procfile specific to Heroku/compatible platforms
   - Add-ons tied to Heroku ecosystem
   - DATABASE_URL pattern specific

5. **Not Cost-Effective for Small Projects**
   - PythonAnywhere $5/month is cheaper (no separate DB cost)
   - Render free tier beats Eco for hobby projects
   - Railway usage-based can be cheaper

6. **Dyno Sleeping** (Eco tier)
   - 30-minute inactivity → sleep
   - Cold start latency (5-30 seconds)
   - Frustrating for low-traffic apps

---

## 6. Best Use Cases

### Ideal For:
- **Professional/enterprise applications** with budget for infrastructure
- **Team projects** needing pipelines, review apps, collaboration
- **Production apps** requiring auto-scaling and high availability
- **Startups with funding** (not bootstrapped)
- **Apps using add-on ecosystem** (Postgres, Redis, monitoring, etc.)
- **Developers comfortable with git-based workflows**

### NOT Ideal For:
- **Hobby projects** (too expensive without free tier)
- **Bootstrapped startups** (cheaper alternatives exist)
- **Learning/educational projects** ($10/month vs. free alternatives)
- **Cost-sensitive deployments** (Railway/Render/PythonAnywhere cheaper)
- **Always-on low-traffic apps** (Eco dyno sleep frustrating)

---

## 7. Comparison to Alternatives

### vs. PythonAnywhere
- **More Expensive:** $10/month (Eco + DB) vs. $5/month PythonAnywhere
- **More Features:** Auto-deploy, pipelines, add-ons vs. manual reload
- **More Complex:** Procfile, buildpacks vs. WSGI config
- **Production-Ready:** Scaling, teams, enterprise vs. single-app focus

### vs. Render
- **More Expensive:** Eco $5 + sleep vs. Render free tier (no sleep on paid)
- **More Mature:** 17 years vs. 5 years
- **Better Add-Ons:** 200+ vs. limited
- **Less Modern:** Older stack vs. Docker-native

### vs. Railway
- **Fixed Pricing:** $5 Eco hours vs. usage-based metering
- **More Predictable:** No surprise bills vs. pay-per-second
- **Less Flexible:** Dyno tiers vs. custom resource allocation
- **More Expensive:** $10/month minimum vs. $5 Railway credit

### vs. Fly.io
- **Simpler:** Buildpacks vs. Dockerfile required
- **More Regions:** Heroku has regions, Fly.io has 30+ edge locations
- **More Expensive:** $10/month vs. no free tier on Fly (similar)
- **Less Global:** Regional vs. true edge deployment

---

## 8. Flask Deployment Example

### Complete Flask + Postgres App on Heroku

**Project Structure:**
```
flask-heroku-demo/
├── app.py
├── requirements.txt
├── Procfile
├── runtime.txt
└── .env (local only, not committed)
```

**app.py:**
```python
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

@app.route('/')
def hello():
    return 'Flask + Heroku + Postgres!'

if __name__ == '__main__':
    app.run()
```

**requirements.txt:**
```
Flask==3.0.0
gunicorn==21.2.0
Flask-SQLAlchemy==3.0.5
psycopg2-binary==2.9.7
```

**Procfile:**
```
web: gunicorn app:app
release: python -c "from app import db; db.create_all()"
```

**runtime.txt:**
```
python-3.11.5
```

**Deployment:**
```bash
heroku login
heroku create flask-demo-app
heroku addons:create heroku-postgresql:mini
git add .
git commit -m "Deploy to Heroku"
git push heroku main
heroku open
```

**Result:** App live with Postgres database in ~5 minutes

---

## 9. Migration Considerations

### Moving FROM Heroku (Why Devs Left in 2022)

**Primary Reason:** Free tier removal

**Common Migrations:**
- **Render:** Free tier with no sleep, similar buildpack model
- **Railway:** Usage-based pricing, modern DX
- **Fly.io:** Global edge, Docker-based
- **PythonAnywhere:** Simpler, cheaper for Python-only apps

**Migration Effort:** Low to Medium
- Procfile → render.yaml or Dockerfile
- DATABASE_URL environment variable portable
- Add-ons require replacement (Postgres, Redis, etc.)

### Moving TO Heroku (Why Choose Heroku in 2025)

**Reasons to Choose Heroku:**
1. Enterprise features (Teams, Pipelines, compliance)
2. Mature add-on ecosystem
3. Team already knows Heroku
4. Budget not a constraint
5. Need proven, battle-tested platform

---

## 10. Summary Verdict

**Heroku remains the "gold standard" PaaS** - polished, feature-rich, reliable - but **too expensive for hobbyists and small projects** since free tier removal.

**Best For:** Professional teams with budget, enterprise apps, projects using add-on ecosystem
**Avoid For:** Hobby projects, bootstrapped startups, learning/educational use

**For QRCards:**
- **Current Stage:** Overpriced at $10/month minimum (vs. $5 PythonAnywhere or free Render)
- **Future Stage (funded):** Excellent choice for team collaboration and scaling
- **Recommendation:** Not cost-effective until QRCards has revenue/funding

**Heroku's 2025 Position:** Premium PaaS for professional developers, not the "easy free hosting" it once was.
