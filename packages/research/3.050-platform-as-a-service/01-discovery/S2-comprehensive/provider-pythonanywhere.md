# PythonAnywhere - Provider Analysis

**Platform Type:** Python-Native PaaS
**Website:** https://www.pythonanywhere.com/
**Current Status:** QRCards' current hosting provider
**Founded:** 2012 (12+ years in market)

## Overview & Positioning

PythonAnywhere is a **Python-specific Platform-as-a-Service** designed exclusively for Python applications. Unlike general-purpose PaaS providers, PythonAnywhere is built from the ground up for Python developers, offering:

- Browser-based Python console and editor
- Native WSGI framework support (Flask, Django, web2py, Bottle)
- No Docker/containerization required
- Extremely simple deployment model
- Educational/beginner-friendly focus

**Market Position:** Positioned as the simplest way to host Python web apps, targeting beginners, educators, and small production apps that don't need container orchestration complexity.

**Unique Selling Point:** Zero DevOps - pure Python environment with web-based IDE and console.

---

## 1. Pricing Structure

### Free Tier (Beginner Account)

**Monthly Cost:** $0 (truly free, no credit card required)

**Included Resources:**
- **Web Apps:** 1 web app
- **Domain:** your-username.pythonanywhere.com (subdomain only)
- **Storage:** ~500 MB file storage
- **CPU:** 100 CPU-seconds/day for consoles and tasks (very limited)
- **Bandwidth:** Low bandwidth limits (not published exactly)
- **Consoles:** 2 interactive consoles
- **Scheduled Tasks:** 1 daily scheduled task
- **Python Versions:** All supported Python versions
- **SSL:** Free SSL for .pythonanywhere.com domains

**Limitations:**
- **NO custom domain support**
- **Restricted outbound internet access** (whitelist-only for external APIs)
- No SSH access
- No IPython/Jupyter notebooks
- App goes to sleep when inactive
- Cannot use many external APIs due to proxy restrictions

**Best For:** Learning Flask/Django, testing projects, portfolio sites, classroom demos

---

### Hacker Plan (Paid Entry Tier)

**Monthly Cost:** $5/month

**Included Resources:**
- **Web Apps:** 1 web app
- **Storage:** 1 GB disk space
- **CPU:** 2,000 CPU-seconds/day (20x more than free)
- **Custom Domains:** Unlimited custom domains with free SSL
- **Outbound Internet:** Unrestricted (can call any API)
- **SSH Access:** Full SSH terminal access
- **Consoles:** Unlimited
- **Scheduled Tasks:** Soft limit ~20 (can request more)
- **Always-On Tasks:** Supported (for background workers)
- **Database:** MySQL included (within storage quota)
- **PostgreSQL:** Available as add-on (+$7/month for 100MB)

**Performance Estimate:** Can handle ~100,000 hits/day website

**No-Quibble 30-Day Money-Back Guarantee**

---

### Higher Tiers

**Web Dev Plan:** ~$12/month
- 3 web apps
- 3 GB storage
- More CPU seconds

**Custom Plans:** Up to $500/month for high-traffic production sites

---

### Add-On Pricing

| Add-On | Cost |
|--------|------|
| PostgreSQL (100 MB) | +$7/month |
| Additional Storage (1 GB) | +$1/month per GB |
| Additional CPU-seconds | Contact for custom plan |
| More web apps | Upgrade to higher tier |

---

## 2. Deployment Methods

### Deployment Approach: Web-Based WSGI Configuration

PythonAnywhere uses a **unique web-based deployment model** unlike Git-push or Docker-based platforms.

#### Step-by-Step Flask Deployment

**Method 1: Quick Start Wizard (Simplest)**

1. **Clone/Upload Code:**
   - Use Git clone in browser-based Bash console
   - Or upload files via web interface
   - Or use SFTP (paid accounts)

2. **Create Virtual Environment:**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 myapp-venv
   pip install flask gunicorn
   pip install -r requirements.txt
   ```

3. **Create Web App via Web UI:**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose domain (yourname.pythonanywhere.com or custom)
   - Select "Manual configuration" (or Flask quickstart)
   - Choose Python version

4. **Configure WSGI File:**
   - Click link to WSGI configuration file
   - Edit the file to point to your Flask app:

   ```python
   import sys
   path = '/home/yourusername/myapp'
   if path not in sys.path:
       sys.path.append(path)

   from app import app as application  # Import your Flask instance
   ```

5. **Set Virtual Environment Path:**
   - In Web tab, under "Virtualenv" section
   - Enter: `/home/yourusername/.virtualenvs/myapp-venv`

6. **Reload Web App:**
   - Click big green "Reload" button
   - App is live immediately

**Deployment Time:** 5-10 minutes for first deployment

---

**Method 2: Git-Based Workflow (Recommended for Updates)**

```bash
# In PythonAnywhere Bash console
cd ~/myapp
git pull origin main
pip install -r requirements.txt  # if dependencies changed
# Then reload via Web tab
```

No CI/CD pipeline - manual reload required after git pull.

---

### Configuration Files

**Required:**
- `requirements.txt` - Python dependencies
- WSGI file (created/edited via web interface)

**NOT Required:**
- No Procfile
- No Dockerfile
- No render.yaml or railway.toml
- No buildpack configuration

---

### CLI Tools

**SSH Access:** Paid plans only
**API:** Limited API for task automation (not deployment)
**Web-Based Console:** Primary interface for all operations

---

## 3. Features

### Auto-Scaling
**NOT SUPPORTED**
- Single worker process per web app
- No horizontal scaling
- Must upgrade to higher tier for more resources

### Custom Domains & SSL
- **Free Tier:** NO custom domains
- **Paid Tiers:** Unlimited custom domains
- **SSL:** Free Let's Encrypt SSL for all domains (including custom)
- **Setup:** Via CNAME pointing to `webapp-XXXXX.pythonanywhere.com`

### Database Add-Ons
- **MySQL:** Included free (counts toward storage quota)
  - Accessible via console or code
  - Standard MySQL configuration
- **PostgreSQL:** +$7/month for 100 MB
  - Separate add-on purchase
  - Not included in base plans
- **SQLite:** Not recommended for web apps (file-based, concurrency issues)

### Environment Management
- **NO staging/production environments** built-in
- Can create multiple web apps (on higher tiers) for staging
- Environment variables set via web interface (not .env files)

### Monitoring & Logs
- **Access Logs:** Available via web interface, limited retention
- **Error Logs:** Real-time error log viewer in Web tab
- **Server Logs:** Limited access
- **No built-in monitoring dashboard** (no CPU/memory graphs)
- **No alerting system**

### CI/CD Integration
**NOT SUPPORTED**
- No GitHub Actions integration
- No automated deployment on git push
- Manual `git pull` + reload workflow

### Region/Edge Deployment
- **Single Region:** US East (AWS data center)
- **No multi-region** or edge deployment
- **No CDN** built-in for static assets

### Background Workers
- **Always-On Tasks:** Supported on paid plans
- **Scheduled Tasks:** Cron-like scheduling (1/day free, ~20/day paid)
- **Long-Running Processes:** Supported on paid plans with CPU-second limits

### Python-Specific Features
- **Browser-Based Python Console:** Interactive REPL
- **In-Browser Code Editor:** No need for local IDE
- **Pre-installed Libraries:** NumPy, pandas, matplotlib, etc.
- **Jupyter Notebooks:** Paid plans only

---

## 4. Python/Flask Support

### Native Python Support
**BEST IN CLASS** - This is PythonAnywhere's entire purpose.

**Python Versions Supported:**
- Python 2.7 (legacy)
- Python 3.6, 3.7, 3.8, 3.9, 3.10, 3.11 (latest)
- Can switch versions per web app

### Flask-Specific Features

**Quickstart Installer:**
- Click "Flask" in web app creation wizard
- Auto-generates basic Flask app structure
- Pre-configured WSGI file

**Flask Documentation:**
- Extensive help pages specifically for Flask
- Step-by-step tutorials
- Common gotchas documented

### WSGI Server Options

**Default:** Uses PythonAnywhere's custom WSGI server (based on uWSGI)
- Not Gunicorn
- Not uWSGI directly
- Proprietary server optimized for shared hosting

**Configuration:**
- No Gunicorn configuration needed
- No server tuning required
- Works out-of-the-box

### Package Manager Support
- **pip:** Full support (via virtualenv)
- **pipenv:** Not officially supported (workarounds exist)
- **poetry:** Not officially supported (workarounds exist)
- **conda:** NOT supported

### Flask Extensions Compatibility
- Flask-SQLAlchemy: YES
- Flask-Login: YES
- Flask-Mail: YES (paid plans - requires outbound internet)
- Flask-WTF: YES
- Most popular extensions: YES

---

## 5. Pros & Cons

### Advantages

1. **Simplest Deployment Model**
   - No Docker, no containers, no buildpacks
   - Point-and-click WSGI configuration
   - Beginner-friendly web UI

2. **Python-Native Environment**
   - Browser-based Python console
   - All Python versions readily available
   - No context-switching to containers

3. **Extremely Low Entry Price**
   - $5/month for custom domain + full features
   - Cheaper than Heroku Eco ($5 with limits), Railway ($5 credit), Render (free limited)

4. **Predictable Pricing**
   - Fixed monthly cost, no surprises
   - No per-second billing complexity
   - No bandwidth overages (within tier limits)

5. **Zero DevOps Required**
   - No CI/CD setup
   - No container orchestration
   - No infrastructure management

6. **Educational Focus**
   - Perfect for learning Flask/Django
   - Free tier sufficient for coursework
   - Extensive beginner documentation

### Disadvantages

1. **No Auto-Scaling**
   - Single process per app
   - Must manually upgrade tiers
   - Cannot handle traffic spikes elastically

2. **Limited Modern DevOps Integration**
   - No automated deployments
   - No CI/CD pipeline support
   - Manual reload after code changes

3. **Vendor Lock-In Risk**
   - Custom WSGI configuration
   - Not portable to Docker/containers
   - Migration requires reconfiguration

4. **Single Region**
   - US East only
   - No global edge deployment
   - Latency for international users

5. **Restrictive Free Tier**
   - Outbound internet restrictions make it nearly unusable for real apps
   - Only 100 CPU-seconds/day

6. **Limited Monitoring**
   - No performance metrics dashboard
   - No alerting
   - Basic logs only

7. **Resource Limits Hit Quickly**
   - 1 GB storage fills fast (for $5 tier)
   - 2,000 CPU-seconds/day can be limiting
   - Single web worker bottleneck

8. **Not Docker-Based**
   - Cannot use Docker for local dev parity
   - Cannot easily migrate to Kubernetes/other platforms
   - Limited to PythonAnywhere's Python environment

---

## 6. Best Use Cases

### Ideal For:
- **Flask/Django learning projects** (free tier)
- **Small production apps** (<10,000 daily users) on $5-12 plan
- **Portfolio websites** for Python developers
- **Classroom/educational projects**
- **Internal tools** with low traffic
- **Prototypes and MVPs** that don't need scaling

### NOT Ideal For:
- **High-traffic production apps** (no auto-scaling)
- **Microservices architectures** (single app focus)
- **Global applications** (single region)
- **DevOps-heavy teams** (limited CI/CD)
- **Container-based workflows** (no Docker)
- **Apps requiring <100ms latency worldwide** (no edge deployment)

---

## 7. Comparison to Alternatives

### vs. Heroku
- **Cheaper:** $5/month vs. Heroku's $7/month Eco (with sleep)
- **Simpler:** No Procfile, no buildpacks
- **Less Flexible:** No auto-scaling, single region
- **Python-Focused:** Better Python console experience

### vs. Render
- **Simpler:** No Docker/build configuration
- **Less Features:** No auto-deploy, no free tier with custom domain
- **Cheaper Entry:** $5 vs. Render's ~$7 for Starter

### vs. Railway
- **More Predictable Pricing:** Fixed $5 vs. usage-based metering
- **Simpler:** No Nixpacks/Docker knowledge needed
- **Less Scalable:** No auto-scaling, resource limits

### vs. Fly.io
- **Much Simpler:** No VMs, no Dockerfile
- **Cheaper Entry:** $5/month vs. no free tier
- **Less Global:** Single region vs. 30+ regions

---

## 8. Flask Deployment Example

### Minimal Flask App on PythonAnywhere

**app.py:**
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello from PythonAnywhere!'

if __name__ == '__main__':
    app.run()
```

**requirements.txt:**
```
Flask==3.0.0
```

**WSGI Configuration (via web UI):**
```python
import sys
path = '/home/yourusername/myflaskapp'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

**Deployment Steps:**
1. Upload files or `git clone` in Bash console
2. `mkvirtualenv myapp-venv`
3. `pip install -r requirements.txt`
4. Create web app in Web tab
5. Configure WSGI file (above)
6. Set virtualenv path
7. Reload
8. **App is live at yourname.pythonanywhere.com**

Total time: **5 minutes**

---

## 9. Current QRCards Status

**QRCards is currently hosted on PythonAnywhere** (based on experiment context).

**Likely Plan:** Free or $5 Hacker plan

**Benefits for QRCards:**
- Simple deployment for Flask app
- Low/no cost for early-stage project
- Easy to manage for solo developer

**Potential Issues:**
- Outbound internet restrictions on free tier (if using external APIs)
- No auto-scaling as traffic grows
- Limited CI/CD for rapid iteration

**Migration Consideration:** If QRCards grows beyond ~10K daily users or needs global deployment, migration to Render/Railway/Fly.io would be necessary.

---

## 10. Summary Verdict

**PythonAnywhere is the "training wheels" of PaaS** - it makes Python web hosting incredibly simple, but at the cost of modern DevOps features and scalability.

**Best For:** Beginners, small projects, educational use, simple Flask/Django apps
**Outgrown By:** Teams needing CI/CD, auto-scaling, global deployment, or Docker workflows

For QRCards at current stage: **Excellent fit** (low cost, simple, works)
For QRCards at 100K+ users: **Migration needed** (scaling limits, no edge deployment)
