# Use Case: Backend Template Integration

**Use Case ID**: UC-BACKEND-01
**Date**: 2025-12-01
**Methodology**: S3 Need-Driven Discovery

---

## Use Case Definition

**Project Type**: JavaScript/CSS bundling for server-rendered applications (Flask, Django, Rails, Laravel)

**Characteristics**:
- Backend renders HTML templates (Jinja2, Django templates, ERB, Blade)
- Frontend JavaScript enhances pages (forms, interactivity, widgets)
- Assets must output to backend's static folder
- Templates reference bundled assets via URLs
- Mix of traditional pages and interactive components

**Example Applications**:
- Flask dashboard with interactive charts
- Django admin panel with custom widgets
- Rails e-commerce with enhanced checkout flow
- Laravel CMS with rich text editor

**Key Challenge**: Build tool must integrate with backend's asset serving, not replace it.

---

## Requirements Specification

### Primary Requirements (Must-Have)

**P1. Static Folder Output**
- Success Criteria: Bundle outputs to `backend/static/` or configurable path
- Justification: Backend serves static files from specific folder
- Deal-Breaker: Cannot configure output path = incompatible

**P2. Asset Manifest Generation**
- Success Criteria: Generate manifest.json mapping `app.js` → `app.abc123.js`
- Justification: Backend templates need to reference hashed filenames
- Deal-Breaker: No manifest = cannot reference hashed assets

**P3. No HTML Generation**
- Success Criteria: Build tool only bundles JS/CSS, doesn't generate HTML
- Justification: Backend generates HTML, not build tool
- Deal-Breaker: Tool that generates HTML fights with backend

**P4. Development Mode Integration**
- Success Criteria: Dev server proxies to backend OR backend proxies to dev server
- Justification: Need HMR while backend serves pages
- Deal-Breaker: Cannot develop with backend running = broken workflow

**P5. Production Optimization**
- Success Criteria: Minification, tree shaking, asset hashing
- Justification: Standard production requirements
- Deal-Breaker: Unoptimized bundles unacceptable

### Secondary Requirements (Nice-to-Have)

**S1. Multiple Entry Points**
- Target: Different bundles for different sections (admin.js, public.js)
- Value: Page-specific bundles for performance

**S2. CSS Extraction**
- Target: Separate CSS file (not inlined in JS)
- Value: Backend can load CSS in `<head>`, JS at end of `<body>`

**S3. Source Maps in Development**
- Target: Debug original TypeScript/JSX in browser
- Value: Better debugging experience

**S4. Watch Mode Integration**
- Target: Auto-rebuild when files change
- Value: Fast iteration during development

**S5. Framework Agnostic**
- Target: Works with Flask, Django, Rails, Laravel, Express
- Value: One tool for multiple backend frameworks

---

## Tool Evaluation

### Vite

**Primary Requirements**:
- P1 (Static Output): ✅ **PASS** - `build.outDir` configurable
- P2 (Manifest): ✅ **PASS** - `build.manifest: true` generates manifest.json
- P3 (No HTML): ⚠️ **CONDITIONAL** - Generates HTML by default, but can skip
- P4 (Dev Integration): ⚠️ **COMPLEX** - Middleware available but requires setup
- P5 (Optimization): ✅ **PASS** - Full Rollup optimization

**Secondary Requirements**:
- S1 (Multiple Entries): ✅ Multiple inputs supported
- S2 (CSS Extraction): ✅ Separate CSS files
- S3 (Source Maps): ✅ Built-in
- S4 (Watch Mode): ✅ Dev server watches
- S5 (Framework Agnostic): ✅ Any backend

**Configuration Example**:
```javascript
// vite.config.js
export default {
  build: {
    outDir: '../backend/static/dist',
    manifest: true,
    rollupOptions: {
      input: 'src/main.js'  // No HTML input
    }
  },
  server: {
    origin: 'http://localhost:5173'  // For backend templates
  }
}
```

**Backend Template Usage**:
```jinja2
{# Flask/Jinja2 example #}
{% set manifest = load_manifest('static/dist/manifest.json') %}
<script src="{{ url_for('static', filename=manifest['main.js']) }}"></script>
```

**Gap Analysis**: Requires backend integration work (manifest parsing, middleware for dev mode). Not plug-and-play but doable.

---

### Webpack 5

**Primary Requirements**:
- P1 (Static Output): ✅ **PASS** - `output.path` configurable
- P2 (Manifest): ✅ **PASS** - webpack-manifest-plugin (mature)
- P3 (No HTML): ✅ **PASS** - Skip HtmlWebpackPlugin, just bundle JS/CSS
- P4 (Dev Integration): ✅ **PASS** - webpack-dev-middleware well-established
- P5 (Optimization): ✅ **PASS** - Full optimization suite

**Secondary Requirements**:
- S1 (Multiple Entries): ✅ Excellent support
- S2 (CSS Extraction): ✅ MiniCssExtractPlugin
- S3 (Source Maps): ✅ Built-in
- S4 (Watch Mode): ✅ Watch mode + middleware
- S5 (Framework Agnostic): ✅ Best-in-class backend integration

**Configuration Example**:
```javascript
// webpack.config.js
const ManifestPlugin = require('webpack-manifest-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
  entry: './src/main.js',
  output: {
    path: path.resolve(__dirname, '../backend/static/dist'),
    filename: '[name].[contenthash].js',
    publicPath: '/static/dist/'
  },
  plugins: [
    new ManifestPlugin(),
    new MiniCssExtractPlugin({
      filename: '[name].[contenthash].css'
    })
  ]
};
```

**Middleware Integration** (Flask example):
```python
# Flask development setup
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

if app.debug:
    # Proxy webpack-dev-server assets
    from flask_webpack import Webpack
    webpack = Webpack(app)
```

**Gap Analysis**: Mature ecosystem with established patterns. Excellent documentation for backend integration. Configuration heavy but well-supported.

---

### esbuild

**Primary Requirements**:
- P1 (Static Output): ✅ **PASS** - `outdir` configurable
- P2 (Manifest): ⚠️ **CONDITIONAL** - Metafile generation (not standard manifest.json)
- P3 (No HTML): ✅ **PASS** - JS/CSS only
- P4 (Dev Integration): ❌ **FAIL** - No built-in dev server or middleware
- P5 (Optimization): ⚠️ **LIMITED** - Basic minification

**Secondary Requirements**:
- S1 (Multiple Entries): ✅ Supported
- S2 (CSS Extraction): ✅ Separate CSS
- S3 (Source Maps): ✅ Built-in
- S4 (Watch Mode): ✅ Watch mode available
- S5 (Framework Agnostic): ✅ Any backend

**Configuration Needed**: 50-100 lines + custom manifest generation + custom dev server

**Gap Analysis**: **PRIMARY REQUIREMENT FAILING** - No dev server/middleware. Metafile format not standard (requires custom parsing). Fast but missing critical backend integration features.

---

### Rollup

**Primary Requirements**:
- P1 (Static Output): ✅ **PASS** - `output.dir` configurable
- P2 (Manifest): ⚠️ **CONDITIONAL** - Via plugins (not built-in)
- P3 (No HTML): ✅ **PASS** - JS/CSS only
- P4 (Dev Integration): ❌ **FAIL** - No built-in dev server
- P5 (Optimization): ✅ **PASS** - Excellent tree shaking

**Secondary Requirements**:
- S1 (Multiple Entries): ✅ Multiple inputs
- S2 (CSS Extraction): ✅ Via plugins
- S3 (Source Maps): ✅ Built-in
- S4 (Watch Mode): ✅ Watch mode
- S5 (Framework Agnostic): ✅ Any backend

**Configuration Needed**: 100+ lines + plugins + custom dev solution

**Gap Analysis**: **PRIMARY REQUIREMENT FAILING** - No dev server. Need manual solution for development integration.

---

### Parcel

**Primary Requirements**:
- P1 (Static Output): ✅ **PASS** - `--dist-dir` flag
- P2 (Manifest): ❌ **FAIL** - No manifest.json generation
- P3 (No HTML): ⚠️ **CONDITIONAL** - Wants HTML entry, can work around
- P4 (Dev Integration): ⚠️ **COMPLEX** - Dev server available but no middleware
- P5 (Optimization): ✅ **PASS** - Full optimization

**Secondary Requirements**:
- S1 (Multiple Entries): ✅ Multiple inputs
- S2 (CSS Extraction): ✅ Automatic
- S3 (Source Maps): ✅ Automatic
- S4 (Watch Mode): ✅ Built-in
- S5 (Framework Agnostic): ✅ Any backend

**Gap Analysis**: **PRIMARY REQUIREMENT FAILING** - No manifest generation is deal-breaker. Backend templates cannot reference hashed filenames without manifest.

---

### Turbopack

**Primary Requirements**:
- P1 (Static Output): ⚠️ **UNCLEAR** - Next.js-specific architecture
- P2 (Manifest): ⚠️ **UNCLEAR** - Next.js handles assets
- P3 (No HTML): ❌ **FAIL** - Next.js generates HTML
- P4 (Dev Integration): ❌ **FAIL** - Next.js is the backend
- P5 (Optimization): ⚠️ **UNCLEAR** - Limited documentation

**Gap Analysis**: **DISQUALIFIED** - Not designed for backend integration. Next.js IS the backend.

---

## Requirement Coverage Matrix

| Tool | P1 (Output) | P2 (Manifest) | P3 (No HTML) | P4 (Dev Mode) | P5 (Optimization) | Primary Score |
|------|-------------|---------------|--------------|---------------|-------------------|---------------|
| **Webpack 5** | ✅ | ✅ | ✅ | ✅ | ✅ | **5/5** |
| **Vite** | ✅ | ✅ | ⚠️ | ⚠️ | ✅ | **4/5** |
| **esbuild** | ✅ | ⚠️ | ✅ | ❌ | ⚠️ | **DISQUALIFIED** |
| **Rollup** | ✅ | ⚠️ | ✅ | ❌ | ✅ | **DISQUALIFIED** |
| **Parcel** | ✅ | ❌ | ⚠️ | ⚠️ | ✅ | **DISQUALIFIED** |
| **Turbopack** | ⚠️ | ⚠️ | ❌ | ❌ | ⚠️ | **DISQUALIFIED** |

---

## Best Fit Recommendation

**Winner: Webpack 5**

**Justification**:
1. **Perfect primary requirement coverage** (5/5)
2. **Mature backend integration** - webpack-dev-middleware is industry standard
3. **Established patterns** - Flask-Webpack, Django-Webpack, Rails Webpacker
4. **Excellent manifest plugin** - webpack-manifest-plugin is battle-tested
5. **Framework ecosystem** - Plugins for every backend framework

**Alternative: Vite (with caveats)**
- Choose if Webpack config feels too heavy
- Requires custom middleware integration (less mature than Webpack)
- Manifest generation works but less documented for backend use cases
- Good if team prioritizes modern tooling over established patterns

**Why Not Parcel?**
- **DISQUALIFIED** - No manifest generation is critical missing feature
- Backend templates cannot reference hashed assets without manifest

**Why Not esbuild/Rollup?**
- **DISQUALIFIED** - No dev server/middleware support
- Would need to build custom development integration

---

## Implementation Guidance

### Webpack 5 (Recommended)

**Step 1: Install Dependencies**
```bash
npm install --save-dev webpack webpack-cli webpack-manifest-plugin \
  mini-css-extract-plugin webpack-dev-middleware
```

**Step 2: Configure Webpack**
```javascript
// webpack.config.js
const ManifestPlugin = require('webpack-manifest-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const path = require('path');

module.exports = {
  entry: './frontend/src/main.js',
  output: {
    path: path.resolve(__dirname, 'backend/static/dist'),
    filename: '[name].[contenthash:8].js',
    publicPath: '/static/dist/'
  },
  plugins: [
    new ManifestPlugin({ fileName: 'manifest.json' }),
    new MiniCssExtractPlugin({
      filename: '[name].[contenthash:8].css'
    })
  ]
};
```

**Step 3: Backend Integration (Flask)**
```python
# backend/app.py
import json
from flask import Flask, url_for

def load_manifest():
    with open('static/dist/manifest.json') as f:
        return json.load(f)

@app.context_processor
def inject_assets():
    manifest = load_manifest()
    return {'asset': lambda name: url_for('static', filename=f"dist/{manifest[name]}")}
```

**Step 4: Template Usage**
```jinja2
{# backend/templates/base.html #}
<link rel="stylesheet" href="{{ asset('main.css') }}">
<script src="{{ asset('main.js') }}"></script>
```

**Step 5: Development Mode**
```javascript
// backend/middleware.js (for webpack-dev-middleware)
const webpack = require('webpack');
const webpackDevMiddleware = require('webpack-dev-middleware');
const config = require('./webpack.config.js');

const compiler = webpack(config);
app.use(webpackDevMiddleware(compiler, {
  publicPath: config.output.publicPath
}));
```

---

## Confidence Level

**HIGH CONFIDENCE**

**Reasoning**:
- Webpack 5 has mature, well-documented backend integration patterns
- webpack-manifest-plugin is industry standard
- Established middleware for every major backend framework
- Large ecosystem of examples (Flask-Webpack, Django-Webpack, Rails Webpacker)

**Risk Factors**:
- Webpack configuration complexity (150-200 lines typical)
- Slower dev rebuilds than Vite (but middleware mitigates this)

**When to Choose Vite Instead**:
- Small project where custom middleware integration is acceptable
- Team values modern tooling over established patterns
- Willing to write custom manifest parsing in backend

**Validation Sources**:
- webpack-manifest-plugin documentation
- Flask-Webpack library
- Django-Webpack-Loader library
- Rails Webpacker documentation
