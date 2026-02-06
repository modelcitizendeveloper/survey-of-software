# Deployment Methods Comparison

**Experiment:** 3.050 Platform-as-a-Service
**Stage:** S2 Comprehensive Discovery
**Date:** 2025-10-09

---

## Deployment Methods Overview

| Provider | Primary Method | Auto-Deploy | Docker | Buildpacks | Config Files | Time to Deploy |
|----------|---------------|-------------|--------|------------|--------------|----------------|
| **PythonAnywhere** | Web UI (manual) | NO | NO | NO | WSGI file (web UI) | 5-10 min |
| **Heroku** | Git push | YES | YES | YES | Procfile, requirements.txt | 5-10 min |
| **Render** | Git push | YES | YES | YES | render.yaml (optional) | 5-10 min |
| **Railway** | Git push | YES | YES | Railpack | Procfile (optional) | 3-5 min |
| **Fly.io** | CLI (flyctl) | NO (CLI) | REQUIRED | NO | fly.toml, Dockerfile | 10-15 min |
| **DigitalOcean** | Git push | YES | YES | YES | .do/app.yaml (optional) | 5-10 min |
| **Vercel** | Git push | YES | NO | NO | vercel.json | 2-5 min |
| **Cloud Run** | CLI (gcloud) | Via CI/CD | REQUIRED | NO | Dockerfile | 10-15 min |

---

## Detailed Deployment Method Analysis

### 1. PythonAnywhere - Web UI Manual Configuration

**Deployment Model:** Manual WSGI configuration via web interface

**Step-by-Step:**
1. **Upload Code:**
   - Git clone in Bash console
   - Or upload files via web UI
   - Or SFTP (paid accounts)

2. **Create Virtual Environment:**
   ```bash
   mkvirtualenv myapp-venv
   pip install -r requirements.txt
   ```

3. **Create Web App:**
   - Web tab → "Add a new web app"
   - Choose domain
   - Select Python version
   - Choose "Manual configuration" or "Flask"

4. **Configure WSGI:**
   - Click WSGI config file link
   - Edit to import Flask app:
   ```python
   import sys
   path = '/home/username/myapp'
   if path not in sys.path:
       sys.path.append(path)
   from app import app as application
   ```

5. **Set Virtualenv:** Enter path in Web tab

6. **Reload:** Click green "Reload" button

**Updates/Redeployment:**
```bash
cd ~/myapp
git pull
# Then manually click "Reload" in Web tab
```

**Configuration Files:**
- `requirements.txt` (dependencies)
- WSGI config (via web UI)
- NO Procfile, Dockerfile, YAML

**Pros:**
- Simplest for beginners
- No Git/CLI knowledge required
- Visual interface

**Cons:**
- Manual reload after changes
- No CI/CD integration
- Not portable to other platforms

**Time to First Deploy:** 5-10 minutes

---

### 2. Heroku - Git Push with Buildpacks

**Deployment Model:** Git push + buildpack auto-detection

**Step-by-Step:**
1. **Install Heroku CLI:**
   ```bash
   brew install heroku  # macOS
   ```

2. **Login:**
   ```bash
   heroku login
   ```

3. **Create Files:**

**Procfile:**
```
web: gunicorn app:app
```

**requirements.txt:**
```
Flask==3.0.0
gunicorn==21.2.0
```

**runtime.txt (optional):**
```
python-3.11.5
```

4. **Create Heroku App:**
   ```bash
   heroku create my-flask-app
   ```

5. **Add Database (if needed):**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

6. **Deploy:**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```

**Buildpack Auto-Detection:**
- Heroku detects Python via `requirements.txt`
- Installs dependencies
- Uses Procfile to start app

**Updates/Redeployment:**
```bash
git push heroku main  # Auto-deploys on push
```

**Configuration Files:**
- `Procfile` (REQUIRED)
- `requirements.txt` (REQUIRED)
- `runtime.txt` (optional)
- `app.json` (for Review Apps)

**Pros:**
- "Git push to deploy" (pioneered this model)
- Auto-deploy on push
- Mature buildpack system
- GitHub integration (auto-deploy on PR merge)

**Cons:**
- Requires Procfile knowledge
- Vendor-specific configuration

**Time to First Deploy:** 5-10 minutes (after setup)

---

### 3. Render - Git Push with Infrastructure-as-Code

**Deployment Model:** Git auto-deploy with optional render.yaml

**Method 1: Dashboard Configuration**

1. **Connect GitHub Repo:**
   - Render dashboard → "New +" → "Web Service"
   - Connect repository

2. **Configure:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Plan:** Free/Starter

3. **Deploy:**
   - Click "Create Web Service"
   - Auto-deploys

**Method 2: Infrastructure-as-Code (render.yaml)**

**render.yaml:**
```yaml
services:
  - type: web
    name: flask-app
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --bind 0.0.0.0:$PORT
    plan: starter
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: flask-db
          property: connectionString

databases:
  - name: flask-db
    databaseName: mydb
    plan: starter
```

Commit render.yaml to repo → Render auto-provisions resources

**Method 3: Docker**

**Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
```

**render.yaml (Docker):**
```yaml
services:
  - type: web
    name: flask-app
    env: docker
    dockerfilePath: ./Dockerfile
```

**Updates/Redeployment:**
- Every `git push` triggers auto-deploy
- No manual steps

**Configuration Files:**
- `requirements.txt` (REQUIRED)
- `render.yaml` (optional but recommended)
- `.python-version` or `runtime.txt` (optional)
- `Dockerfile` (if using Docker)

**Pros:**
- Infrastructure-as-code (version-controlled)
- Docker-native (optional)
- No Procfile needed (configure in YAML or dashboard)
- PR preview environments

**Cons:**
- render.yaml syntax to learn
- Requires binding to port 10000

**Time to First Deploy:** 5-10 minutes

---

### 4. Railway - Auto-Detect with Beautiful UI

**Deployment Model:** Git push with Railpack auto-detection

**Step-by-Step:**

1. **Connect GitHub:**
   - Railway dashboard → "+ New Project"
   - "Deploy from GitHub repo"
   - Select repo

2. **Auto-Detection:**
   - Railway detects Python via `requirements.txt`
   - Railpack auto-generates build/start commands

3. **Add Database:**
   - "+ New" → "Database" → "PostgreSQL"
   - Railway auto-creates `DATABASE_URL`

4. **Generate Domain:**
   - Settings → "Generate Domain"

5. **Deploy:**
   - Railway auto-deploys immediately

**Updates/Redeployment:**
- `git push` → automatic rebuild and deploy

**Configuration Files (Optional):**

**Procfile (optional):**
```
web: gunicorn app:app
worker: celery -A app worker
```

**nixpacks.toml (legacy, optional):**
```toml
[start]
cmd = "gunicorn app:app"
```

**railway.json (optional):**
```json
{
  "build": {
    "builder": "NIXPACKS"
  }
}
```

**Minimal Setup:**
- Just `requirements.txt` needed!

**Pros:**
- Beautiful UI (best in class)
- Auto-detection (minimal config)
- Real-time logs
- One-click databases

**Cons:**
- Nixpacks deprecated (transitioning to Railpack)
- Usage-based pricing (unpredictable)

**Time to First Deploy:** 3-5 minutes (fastest!)

---

### 5. Fly.io - CLI with Docker Required

**Deployment Model:** Docker + flyctl CLI

**Step-by-Step:**

1. **Install flyctl:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   flyctl auth login
   ```

2. **Create Dockerfile:**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8080
   CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
   ```

3. **Initialize Fly App:**
   ```bash
   flyctl launch
   ```
   - Prompts for app name
   - Asks which region(s)
   - Generates `fly.toml`

4. **Deploy:**
   ```bash
   flyctl deploy
   ```

**fly.toml (auto-generated):**
```toml
app = "flask-app"
primary_region = "iad"

[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "8080"

[http_service]
  internal_port = 8080
  force_https = true
  min_machines_running = 1

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 512
```

**Multi-Region Deployment:**
```bash
flyctl regions add lhr sin  # Add London, Singapore
flyctl deploy  # Deploys to all regions
```

**Updates/Redeployment:**
```bash
flyctl deploy  # Manual CLI deploy
```

**CI/CD (GitHub Actions):**
```yaml
- uses: superfly/flyctl-actions/setup-flyctl@master
- run: flyctl deploy --remote-only
```

**Configuration Files:**
- `Dockerfile` (REQUIRED)
- `fly.toml` (auto-generated)
- `requirements.txt`

**Pros:**
- Full Docker control
- Multi-region deployment (30+)
- Portable Dockerfile

**Cons:**
- REQUIRES Docker knowledge
- CLI-only (no web UI deploy)
- More complex than buildpack platforms

**Time to First Deploy:** 10-15 minutes (with Docker experience)

---

### 6. DigitalOcean App Platform - Git Push with Buildpacks

**Deployment Model:** Git auto-deploy with buildpack

**Step-by-Step:**

1. **Create App:**
   - DO dashboard → App Platform → "Create App"
   - Connect GitHub repo

2. **Configure Build:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Run Command:** `gunicorn app:app --bind 0.0.0.0:8080`
   - **Plan:** Basic ($5)

3. **Add Database:**
   - Add component → Database → Postgres

4. **Deploy:**
   - Click "Create Resources"

**Infrastructure-as-Code (.do/app.yaml, optional):**
```yaml
name: flask-app
services:
  - name: web
    source_dir: /
    build_command: pip install -r requirements.txt
    run_command: gunicorn app:app --bind 0.0.0.0:8080
    instance_size_slug: basic-xxs
databases:
  - name: db
    engine: PG
    size: basic
```

**Updates/Redeployment:**
- `git push` → auto-deploy

**Configuration Files:**
- `requirements.txt` (REQUIRED)
- `.do/app.yaml` (optional)
- `runtime.txt` (optional)

**Pros:**
- Git auto-deploy
- Integrates with DO ecosystem
- Docker support (optional)

**Cons:**
- Requires manual run command (buildpack doesn't auto-detect fully)
- Less automatic than Render/Railway

**Time to First Deploy:** 5-10 minutes

---

### 7. Vercel - Git Push (Serverless Only)

**Deployment Model:** Git auto-deploy for serverless functions

**NOT for Traditional Flask Apps!**

**Step-by-Step (Serverless API):**

1. **Create Project Structure:**
   ```
   api/
     hello.py
   vercel.json
   requirements.txt
   ```

2. **api/hello.py:**
   ```python
   from flask import Flask
   app = Flask(__name__)

   @app.route('/api/hello')
   def hello():
       return 'Hello'

   def handler(request):
       with app.request_context(request.environ):
           return app.full_dispatch_request()
   ```

3. **vercel.json:**
   ```json
   {
     "functions": {
       "api/*.py": {
         "runtime": "python3.9"
       }
     }
   }
   ```

4. **Deploy:**
   ```bash
   vercel deploy
   # Or connect GitHub for auto-deploy
   ```

**Updates/Redeployment:**
- `git push` → auto-deploy

**Configuration Files:**
- `vercel.json`
- `requirements.txt`

**Limitation:** ONLY serverless functions, NOT full Flask apps

**Time to Deploy:** 2-5 minutes (but incompatible with Flask)

---

### 8. Google Cloud Run - CLI with Docker Required

**Deployment Model:** Docker + gcloud CLI

**Step-by-Step:**

1. **Create Dockerfile:**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD exec gunicorn app:app --bind :$PORT --workers 1 --threads 8
   ```

2. **Authenticate:**
   ```bash
   gcloud auth login
   gcloud config set project my-project
   ```

3. **Build & Deploy:**
   ```bash
   gcloud run deploy flask-app \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

**CI/CD (Cloud Build - cloudbuild.yaml):**
```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/flask-app', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/flask-app']
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args: ['run', 'deploy', 'flask-app', '--image', 'gcr.io/$PROJECT_ID/flask-app']
```

**Updates/Redeployment:**
```bash
gcloud run deploy flask-app --source .
```

**Configuration Files:**
- `Dockerfile` (REQUIRED)
- `cloudbuild.yaml` (for CI/CD)
- `requirements.txt`

**Pros:**
- True serverless (scale to zero)
- Enterprise features (Cloud Logging, Monitoring)
- Auto-scaling (0→1000 instances)

**Cons:**
- Requires Docker + GCP knowledge
- Complex setup
- Cold starts

**Time to First Deploy:** 10-15 minutes (with GCP experience)

---

## Deployment Complexity Ranking

**Simplest to Most Complex:**

1. **Railway** (auto-detect, beautiful UI, 3-5 min)
2. **PythonAnywhere** (web UI, manual but simple, 5-10 min)
3. **Render** (dashboard or YAML, 5-10 min)
4. **Heroku** (Procfile + git push, 5-10 min)
5. **DigitalOcean** (buildpack + manual command, 5-10 min)
6. **Fly.io** (Docker + CLI, 10-15 min)
7. **Google Cloud Run** (Docker + GCP, 10-15 min)
8. **Vercel** (incompatible with Flask)

---

## Recommended by Use Case

### For Beginners
**Best:** PythonAnywhere (web UI), Railway (auto-detect)
**Avoid:** Fly.io, Cloud Run (Docker required)

### For Auto-Deploy Workflow
**Best:** Heroku (mature), Render (modern), Railway (DX)
**Avoid:** PythonAnywhere (manual reload)

### For Infrastructure-as-Code
**Best:** Render (render.yaml), DigitalOcean (.do/app.yaml)
**Good:** Fly.io (fly.toml)

### For Docker Users
**Best:** Render (optional), Fly.io (multi-region), Cloud Run (serverless)
**NOT:** PythonAnywhere (no Docker), Vercel (no Docker)

### For Multi-Region Deployment
**Best:** Fly.io (30+ regions with Anycast)
**NOT:** PythonAnywhere (1 region only)

---

## Key Deployment Differences

| Aspect | PythonAnywhere | Heroku/Render/Railway | Fly.io/Cloud Run |
|--------|---------------|---------------------|------------------|
| **Method** | Web UI config | Git push buildpack | Docker CLI |
| **Auto-Deploy** | NO | YES | Via CI/CD |
| **Config Files** | WSGI (web UI) | Procfile/YAML | Dockerfile |
| **Complexity** | SIMPLE | MEDIUM | COMPLEX |
| **Portability** | Vendor lock-in | Some lock-in | Fully portable |
| **Time** | 5-10 min | 5-10 min | 10-15 min |

---

## Conclusion

**Simplest:** PythonAnywhere (web UI), Railway (auto-detect + beautiful UI)
**Best Auto-Deploy:** Heroku, Render, Railway (git push)
**Most Flexible:** Fly.io, Cloud Run (Docker)
**NOT for Flask:** Vercel (serverless functions only)

**For QRCards:**
- **Current:** PythonAnywhere (simple, but manual reload)
- **Modern Upgrade:** Render or Railway (auto-deploy, modern DX)
- **NOT Needed:** Fly.io (Docker overkill), Vercel (incompatible)
