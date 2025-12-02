# Research Methodology: Build Tools for Flask

## MPSE S1 - Rapid Discovery Approach

### Research Context
QRCards uses Flask Blueprint REST APIs with Jinja2 templates. The architecture includes:
- Flask serving Jinja2 templates at `/qr/domains/{domain}/{env}/`
- JavaScript embedded in templates for interactive widgets (calculators, language tools, recipe scalers)
- Static assets currently inline (CSS in `<style>` blocks, JS in `<script>` blocks)
- Multidomain architecture requiring independent bundles per domain

### Research Questions Priority
1. **Flask Integration** - How does bundler output integrate with Flask's static file serving?
2. **Dev Experience** - Can we get HMR while Flask dev server is running?
3. **Template References** - How do we reference bundled assets in Jinja2 templates?
4. **Multi-Domain** - Can we bundle multiple domains with shared dependencies?
5. **Production** - Bundle size, tree shaking, code splitting effectiveness

### Evaluation Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Flask Integration Complexity | HIGH | How easy to integrate with Flask's static assets pattern |
| Dev Server Compatibility | HIGH | Works alongside Flask dev server (no port conflicts) |
| Build Speed | MEDIUM | Fast rebuilds for development workflow |
| Template Integration | HIGH | Simple asset references in Jinja2 templates |
| Multi-Domain Support | MEDIUM | Handle multiple entry points with shared code |
| Production Optimization | MEDIUM | Tree shaking, code splitting, minification |
| TypeScript Support | LOW | Built-in or easy to add |
| CSS Processing | LOW | PostCSS, Sass, etc. |
| Learning Curve | MEDIUM | Team adoption speed |
| Community Support | LOW | Flask-specific examples and plugins |

### Flask Static Assets Pattern

**Current Structure:**
```
templates/qr/domains/{domain}/{env}/activity_display.html
  └─ Contains inline <style> and <script>
```

**Target Structure:**
```
static/
├── css/
│   └── {domain}-{env}.css
└── js/
    └── {domain}-{env}.js

templates/qr/domains/{domain}/{env}/activity_display.html
  └─ References bundled assets via url_for()
```

**Jinja2 Asset Reference Pattern:**
```jinja2
{% block styles %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/calculators-prod.css') }}">
{% endblock %}

{% block scripts %}
<script src="{{ url_for('static', filename='js/calculators-prod.js') }}"></script>
{% endblock %}
```

### Research Methodology

**For Each Platform (Vite, Webpack, esbuild, etc.):**

1. **Flask Integration Assessment**
   - How does bundler output to Flask's `static/` directory?
   - Can we configure output paths to match Flask conventions?
   - Does it support Flask's development workflow?

2. **Development Experience**
   - Can bundler run alongside Flask dev server?
   - Hot Module Replacement (HMR) support?
   - Watch mode performance for template changes?

3. **Template Integration**
   - How to reference bundled assets in Jinja2?
   - Manifest/entrypoints file for dynamic asset paths?
   - Cache-busting strategy (hash in filename)?

4. **Multi-Domain Architecture**
   - Multiple entry points configuration
   - Shared dependency extraction (vendors bundle)
   - Per-domain bundle strategy

5. **Production Build**
   - Bundle size optimization
   - Tree shaking effectiveness
   - Code splitting strategies
   - Minification quality

### Flask-Specific Challenges

1. **Static File Serving**
   - Flask expects assets in `static/` directory
   - `url_for('static', filename='...')` pattern for cache busting
   - No CDN integration (self-hosted assets)

2. **Template-Based Architecture**
   - JavaScript not in separate `.js` files initially
   - Need to extract inline scripts to modules
   - Maintain Jinja2 template structure

3. **Development Workflow**
   - Flask dev server runs on port 5000
   - Bundler dev server should not conflict
   - Avoid proxy setup if possible (add complexity)

4. **Multidomain Complexity**
   - Each domain has independent templates
   - Shared utility functions across domains
   - Need separate bundles to avoid loading unused code

### Decision Framework

**Phase 1: Rapid Assessment (This Research)**
- Profile each platform's Flask compatibility
- Identify blockers or major integration issues
- Estimate setup complexity

**Phase 2: Recommendation**
- Select top 2 candidates based on Flask integration
- Provide clear decision criteria
- Include migration path from inline scripts

**Phase 3: Implementation (Post-Research)**
- Prototype selected bundler with one domain
- Test HMR workflow with Flask dev server
- Validate production bundle size/performance

### Success Metrics

**Must Have:**
- Bundler outputs to Flask `static/` directory
- Simple Jinja2 template integration
- Works with Flask dev server (no conflicts)
- Production builds with cache busting

**Nice to Have:**
- HMR without proxy setup
- Automatic manifest generation for Jinja2
- Multi-domain configuration examples
- Flask community adoption

**Avoid:**
- Bundlers requiring custom Flask middleware
- Complex proxy setup for development
- Frameworks tied to specific backend (Next.js, SvelteKit)
- Tools requiring major Flask architecture changes

### Research Output

Each platform profile will include:

1. **Flask Integration Pattern** - Code example
2. **Development Workflow** - How to run with Flask
3. **Template Integration** - Jinja2 asset reference example
4. **Multi-Domain Config** - Entry points setup
5. **Pros/Cons** - Flask-specific advantages/disadvantages
6. **Complexity Score** - LOW/MEDIUM/HIGH for Flask integration
7. **Recommendation** - Use case fit for QRCards

### Timeline

- **Rapid Discovery**: 45-60 minutes (platform profiles)
- **Recommendation**: 15 minutes (decision framework)
- **Total**: ~1 hour research session

### References

- Flask Static Files: https://flask.palletsprojects.com/en/latest/tutorial/static/
- Jinja2 Templates: https://jinja.palletsprojects.com/
- QRCards Architecture: `/home/ivanadamin/qrcards/project/python-api/ARCHITECTURE.md`
