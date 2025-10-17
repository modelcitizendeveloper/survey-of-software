# S2 COMPREHENSIVE DISCOVERY - Approach & Methodology

**Experiment:** 3.050 Platform-as-a-Service (PaaS)
**Stage:** S2 - Comprehensive Discovery
**Date:** 2025-10-09
**Time Estimate:** 12-15 minutes

## Objective

Conduct an exhaustive deep-dive analysis of 6-8 PaaS providers to understand the complete landscape of Python/Flask hosting options, with particular focus on how they compare to PythonAnywhere (QRCards' current host).

## Research Questions

1. **Pricing Models:** How do free tiers, paid tiers, and usage-based pricing compare across providers?
2. **Deployment Experience:** What deployment methods are available (Git, Docker, buildpacks, CLI)?
3. **Python/Flask Support:** How native is Python support? Are there Flask-specific features or limitations?
4. **Features & Scale:** What platform features exist for production apps (SSL, databases, monitoring, CI/CD)?
5. **PythonAnywhere's Position:** Is PythonAnywhere's Python-native approach truly simpler, or do Docker/containerized alternatives offer better value?

## Providers Selected

### Core Analysis (8 Providers)

1. **PythonAnywhere** - Current QRCards host, Python-native platform
2. **Heroku** - Classic PaaS, industry standard (no longer has free tier)
3. **Render** - Modern Heroku alternative with free tier
4. **Railway** - Developer experience focused, usage-based pricing
5. **Fly.io** - Edge/global deployment, VM-based architecture
6. **DigitalOcean App Platform** - Traditional cloud provider's PaaS offering
7. **Vercel** - Serverless/frontend-focused but supports Python functions
8. **Google Cloud Run** - Serverless containers from major cloud provider

### Why These Providers?

- **PythonAnywhere:** Baseline for comparison - Python-specific, simple WSGI setup
- **Heroku:** Industry reference point (though expensive post-free-tier removal)
- **Render & Railway:** Modern alternatives gaining popularity in 2024-2025
- **Fly.io:** Unique edge deployment model, different architecture
- **DigitalOcean:** Traditional hosting company's PaaS, bridge between VPS and PaaS
- **Vercel:** Represents serverless/function model, contrast to traditional PaaS
- **Google Cloud Run:** Enterprise-grade serverless containers, major cloud provider

## Research Methodology

### 1. Web Search Strategy

For each provider, searched for:
- Official pricing pages and documentation (2025 current)
- Python/Flask deployment guides and tutorials
- Community discussions and comparison articles
- Recent changes to pricing or free tiers

### 2. Data Collection Categories

For each provider, gathered:

**A. Pricing Structure**
- Free tier details (if exists): CPU, memory, bandwidth, feature limits
- Paid tier pricing: entry-level monthly costs, included resources
- Scaling costs: incremental CPU, memory, bandwidth pricing
- Billing model: fixed monthly vs. usage-based vs. hybrid

**B. Deployment Methods**
- Git-based deployment (GitHub/GitLab integration)
- Docker/container support
- Buildpack systems (Heroku-style, Nixpacks, etc.)
- CLI tools availability
- Configuration files needed (Procfile, Dockerfile, render.yaml, etc.)

**C. Platform Features**
- Auto-scaling capabilities
- Custom domains and SSL certificate handling
- Database add-ons (PostgreSQL, MySQL, Redis)
- Environment management (staging/production)
- Monitoring, logging, and metrics
- CI/CD integration
- Region/edge deployment options

**D. Python/Flask Specifics**
- Native Python runtime support
- Flask framework documentation/examples
- WSGI server options (Gunicorn, uWSGI, etc.)
- Python version support (3.8, 3.9, 3.10, 3.11, 3.12)
- Package manager support (pip, pipenv, poetry)

### 3. Analysis Approach

**Comparative Lens:** Every provider evaluated against PythonAnywhere's baseline of:
- Simple WSGI configuration
- Python-native environment
- Beginner-friendly interface
- Minimal DevOps complexity

**Key Trade-offs Identified:**
- Simplicity vs. flexibility
- Python-native vs. Docker-based
- Fixed pricing vs. usage-based
- Managed services vs. infrastructure control

## Output Structure

### Individual Provider Files
Each `provider-[name].md` contains:
1. Overview & positioning
2. Pricing breakdown (free tier, paid tiers, usage costs)
3. Deployment methods (step-by-step for Flask)
4. Features (with availability by tier)
5. Python/Flask support details
6. Pros/cons relative to alternatives

### Comparison Matrices
1. **pricing-matrix.md** - Side-by-side pricing comparison
2. **feature-matrix.md** - Feature availability across tiers
3. **python-flask-support.md** - Python/Flask specific comparison
4. **deployment-methods.md** - How deployment works for each

## Key Findings Preview

### Pricing Trends (2025)
- **Free tier elimination:** Heroku removed free tier in 2022, Fly.io followed
- **Usage-based pricing:** Railway, Fly.io, Google Cloud Run charge per-second usage
- **Hybrid models:** Render, DigitalOcean have fixed tiers + usage overages
- **Python-native advantage:** PythonAnywhere's $5/month Hacker plan competitive for simple apps

### Deployment Complexity Spectrum
1. **Simplest:** PythonAnywhere (web UI, WSGI config)
2. **Buildpack-based:** Heroku, Render, Railway (Procfile + requirements.txt)
3. **Container-based:** Fly.io, Google Cloud Run (Dockerfile required)
4. **Serverless:** Vercel (function-based, requires /api routes)

### Python/Flask Support
- **Native:** PythonAnywhere (Python-specific platform)
- **First-class:** Heroku, Render, Railway, DigitalOcean (buildpack support)
- **Container-based:** Fly.io, Google Cloud Run (full control, more setup)
- **Limited:** Vercel (serverless functions only, not traditional Flask apps)

## Limitations of This Analysis

1. **Pricing volatility:** Cloud pricing changes frequently; data current as of Oct 2025
2. **Free tier uncertainty:** Free tiers can be removed (see Heroku, Fly.io)
3. **Regional variance:** Some providers have region-specific pricing not captured
4. **Usage patterns:** Real costs depend heavily on traffic, CPU, memory patterns
5. **Enterprise features:** Many providers offer custom enterprise pricing not analyzed

## Next Steps (S3 - Targeted Testing)

Based on S2 findings, S3 should:
1. Deploy identical Flask test app to 3-4 top candidates
2. Measure actual deployment time and complexity
3. Test real-world scenarios (database, environment vars, custom domains)
4. Validate pricing with actual usage metrics
5. Document developer experience friction points

## Conclusion

This S2 comprehensive discovery provides complete landscape visibility for PaaS options. The analysis reveals PythonAnywhere's unique position as the only Python-native platform, but also highlights modern alternatives with Docker/container flexibility that may offer better long-term scaling and DevOps integration.

The question isn't "which is objectively best" but rather "which fits QRCards' current needs and future trajectory?"
