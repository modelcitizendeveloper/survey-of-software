# Vercel - Provider Analysis

**Platform Type:** Serverless/Frontend-Focused Platform
**Website:** https://vercel.com/
**Founded:** 2015 (as Zeit, rebranded Vercel 2020)
**Positioning:** "Deploy the best web experiences"

## Overview & Positioning

Vercel is a **frontend-focused serverless platform** optimized for **Next.js, React, Vue, and static sites**. While it supports Python serverless functions, it is **NOT designed for traditional Flask applications**.

**Key Focus:**
- **Frontend frameworks** (Next.js - Vercel's own framework)
- **Serverless functions** (not long-running servers)
- **Edge computing** (Vercel Edge Functions)
- **Global CDN** (instant worldwide distribution)

**Market Position:** Targets frontend developers building modern web apps with serverless backends.

**Python/Flask Limitation:** Vercel supports **Python serverless functions only** - NOT traditional Flask apps with routing, templates, etc.

---

## 1. Pricing Structure

### Hobby Plan (Free)

**Monthly Cost:** $0

**Includes:**
- **100 GB bandwidth**
- **Serverless function invocations:** 100,000/month
- **Edge function invocations:** 1,000,000/month
- **Build execution time:** Limited
- **Custom domains:** Unlimited with SSL
- **Deployments:** Unlimited

**Limitations:**
- **1 team member** (personal projects only)
- Function execution limits (10-second timeout)

---

### Pro Plan

**Monthly Cost:** $20/month per team member

**Includes:**
- **1 TB bandwidth** (~10x Hobby)
- **1,000,000 serverless function invocations**
- **10,000,000 edge function invocations**
- **400 hours build execution**
- **Team collaboration**
- **Analytics**

**Overages:**
- **$40 per 100 GB bandwidth** (expensive!)
- **$2 per million function invocations**

---

### Enterprise Plan

**Monthly Cost:** $20-25K/year minimum

**For:** Large companies with compliance, scale, SLAs.

---

## 2. Deployment Methods

### Primary Method: Git Auto-Deploy

**GitHub/GitLab Integration:**
1. Connect repository
2. Vercel auto-detects framework (Next.js, Vite, etc.)
3. Auto-deploys on push

**For Python Serverless Functions:**

**Project Structure:**
```
vercel-flask-functions/
├── api/
│   ├── hello.py
│   └── user.py
├── vercel.json
└── requirements.txt
```

**IMPORTANT:** Python functions must be in `/api` directory.

**api/hello.py:**
```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/api/hello')
def hello():
    return 'Hello from Vercel!'

# Expose WSGI app
def handler(request):
    with app.request_context(request.environ):
        return app.full_dispatch_request()
```

**vercel.json:**
```json
{
  "functions": {
    "api/*.py": {
      "runtime": "python3.9"
    }
  }
}
```

**Deployment:**
```bash
npm install -g vercel
vercel login
vercel
```

---

## 3. Python/Flask Support

### MAJOR LIMITATION: Serverless Functions Only

Vercel **CANNOT run traditional Flask apps**:
- **NO long-running Flask server**
- **NO app.run()**
- **NO routing outside /api routes**
- **NO templates rendered server-side** (use frontend framework for UI)

**What WORKS:**
- Flask-based **API endpoints** in `/api` folder
- Each file is a separate function
- **10-second execution limit** (Hobby) / 60 seconds (Pro)
- Stateless functions only

**What DOESN'T WORK:**
- Traditional Flask app with `@app.route('/')`
- Flask templates (Jinja2)
- Session management (unless using external store)
- WebSockets, long-polling

### Python Versions
- Python 3.9, 3.10, 3.11

### Use Case
**Vercel is for:**
- **Frontend app (Next.js/React) + Python API** (in /api)
- **NOT for** full Flask applications

---

## 4. Pros & Cons

### Advantages
1. **Generous Free Tier** (100 GB bandwidth, 100K function calls)
2. **Global Edge Network** (instant worldwide deployment)
3. **Perfect for Next.js** (Vercel's framework)
4. **Serverless** (pay only for executions)

### Disadvantages
1. **NOT for Traditional Flask Apps** (serverless functions only)
2. **Expensive Overages** ($40 per 100 GB bandwidth)
3. **10-Second Timeout** (free tier)
4. **Stateless Only** (no persistent connections)

---

## 5. Best Use Cases

### Ideal For:
- **Next.js/React apps** with Python API
- **Jamstack sites** with serverless functions
- **Frontend-heavy apps** needing edge deployment

### NOT Ideal For:
- **Traditional Flask applications** (this is QRCards' case!)
- **Long-running processes**
- **Stateful applications**
- **Apps needing templates/server-side rendering** (unless using Next.js)

---

## 6. Summary Verdict

**Vercel is the WRONG choice for Flask apps** like QRCards.

While it supports Python, it's designed for **serverless API functions**, not traditional web frameworks.

**For QRCards:** **NOT RECOMMENDED** - QRCards needs full Flask app, not serverless functions.

**Vercel's 2025 Position:** Best-in-class for Next.js/frontend, but incompatible with traditional Flask architecture.
