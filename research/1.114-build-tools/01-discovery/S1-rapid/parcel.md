# Parcel - Flask Integration Profile

## Overview

**Parcel** is a zero-configuration web application bundler. Known for "just works" experience with automatic asset handling, built-in dev server, and fast builds via Rust-based compiler (Parcel 2+). Ideal for quick setup with minimal config.

## Flask Integration Pattern

### Configuration (Optional!)

Parcel works with ZERO configuration. Optional `.parcelrc` for customization:

```json
{
  "extends": "@parcel/config-default",
  "transformers": {
    "*.js": ["@parcel/transformer-babel"]
  }
}
```

**Most common use: NO CONFIG FILE NEEDED**

### package.json Configuration

```json
{
  "name": "qrcards-frontend",
  "scripts": {
    "dev": "parcel watch src/domains/*/prod/main.js --dist-dir ../flasklayer/static --public-url /static/",
    "build": "parcel build src/domains/*/prod/main.js --dist-dir ../flasklayer/static --public-url /static/"
  },
  "devDependencies": {
    "parcel": "^2.11.0"
  }
}
```

### Directory Structure

```
frontend/
├── src/
│   └── domains/
│       ├── calculators/
│       │   └── prod/
│       │       ├── main.js
│       │       └── styles.css
│       ├── language/
│       │   └── prod/
│       │       └── main.js
│       └── recipes/
│           └── prod/
│               └── main.js
└── package.json  # No config file needed!
```

### Automatic Features (No Config)

Parcel automatically handles:
- **JavaScript/TypeScript**: Transpilation via Babel/SWC
- **CSS**: PostCSS, CSS Modules, Sass/SCSS
- **Images**: Optimization and hashing
- **Fonts**: WOFF/WOFF2 handling
- **Code Splitting**: Automatic shared chunk extraction
- **Hot Module Replacement**: Built-in dev server
- **Tree Shaking**: Production optimization
- **Source Maps**: Development debugging

## Flask Integration Options

### Option 1: Build Mode (Simplest)

**Build to Flask static directory:**
```bash
parcel build src/main.js --dist-dir ../flasklayer/static/js --public-url /static/js/
```

**Output:**
```
static/
├── js/
│   ├── main.HASH.js
│   └── main.HASH.css
└── assets/
    └── image.HASH.png
```

**Jinja2 Template (manual asset reference):**
```jinja2
{% block scripts %}
<script src="{{ url_for('static', filename='js/main.js') }}"></script>
{% endblock %}
```

**Limitation:** Hash changes require template update.

### Option 2: Manifest Integration

**Install manifest plugin:**
```bash
npm install -D parcel-reporter-manifest
```

**Configuration (.parcelrc):**
```json
{
  "extends": "@parcel/config-default",
  "reporters": ["...", "parcel-reporter-manifest"]
}
```

**Generates manifest.json:**
```json
{
  "main.js": "main.abc123.js",
  "main.css": "main.def456.css"
}
```

**Flask Helper:**
```python
# flasklayer/utils/parcel.py
import json
import os
from flask import current_app
from functools import lru_cache

@lru_cache(maxsize=1)
def load_parcel_manifest():
    """Load Parcel manifest.json"""
    manifest_path = os.path.join(
        current_app.static_folder,
        'manifest.json'
    )

    if not os.path.exists(manifest_path):
        return {}

    with open(manifest_path, 'r') as f:
        return json.load(f)

def parcel_asset(asset_name):
    """
    Get hashed asset path from Parcel manifest

    Usage:
        parcel_asset('main.js')
        # Returns: 'main.abc123.js'
    """
    manifest = load_parcel_manifest()
    return manifest.get(asset_name, asset_name)

def init_parcel_helpers(app):
    """Register Parcel template helpers"""

    @app.template_filter('parcel_asset')
    def parcel_asset_filter(asset_name):
        return parcel_asset(asset_name)

    @app.context_processor
    def parcel_helpers():
        return {'parcel_asset': parcel_asset}
```

**Jinja2 Template:**
```jinja2
{% block scripts %}
<script src="{{ url_for('static', filename='js/' + ('main.js' | parcel_asset)) }}"></script>
{% endblock %}
```

### Option 3: Dev Server with Proxy (Advanced)

**Parcel dev server (port 1234):**
```bash
parcel src/main.js
```

**Flask template in development:**
```jinja2
{% if config.ENV == 'development' %}
  <script src="http://localhost:1234/main.js"></script>
{% else %}
  <script src="{{ url_for('static', filename='js/main.js') }}"></script>
{% endif %}
```

**HMR enabled:** Changes reflect instantly in browser.

## Development Workflow

### Setup (Minimal)

```bash
# Initialize project
npm init -y

# Install Parcel (single dependency!)
npm install -D parcel

# Done! No configuration needed
```

### package.json Scripts

```json
{
  "scripts": {
    "dev": "parcel watch src/domains/*/prod/main.js --dist-dir ../flasklayer/static --public-url /static/",
    "dev:server": "parcel src/main.js",
    "build": "parcel build src/domains/*/prod/main.js --dist-dir ../flasklayer/static --public-url /static/"
  }
}
```

### Running Development

**Option 1: Watch Mode (Recommended for Flask)**
```bash
# Terminal 1: Parcel watch
npm run dev

# Terminal 2: Flask dev server
./local dev dev

# Parcel rebuilds on changes, refresh browser manually
```

**Option 2: Dev Server with HMR**
```bash
# Terminal 1: Parcel dev server
npm run dev:server

# Terminal 2: Flask dev server
./local dev dev

# Template references http://localhost:1234/main.js
# HMR enabled, instant updates
```

### Build Speed

**Parcel 2 (Rust compiler):**
- Fast initial builds (competitive with Vite)
- Fast rebuilds (faster than Webpack, slower than esbuild)
- Caching improves subsequent builds

## Multi-Domain Configuration

### Glob Pattern Entry Points

```bash
# Build all domain bundles at once
parcel build 'src/domains/*/prod/main.js' --dist-dir ../flasklayer/static
```

**Parcel automatically:**
- Creates separate bundles per entry point
- Extracts shared dependencies
- Optimizes code splitting

### Output Structure
```
static/
├── calculators-prod.abc123.js
├── calculators-prod.def456.css
├── language-prod.ghi789.js
├── recipes-prod.jkl012.js
└── shared.mno345.js  # Automatically extracted
```

### Automatic Code Splitting

**No configuration needed!**

```javascript
// src/domains/calculators/prod/main.js
import { apiClient } from '../../../shared/api.js'

// src/domains/language/prod/main.js
import { apiClient } from '../../../shared/api.js'

// Parcel automatically creates shared.js containing apiClient
```

## Production Build

### Build Command
```bash
npm run build
```

### Optimization Features (Automatic)

1. **Minification**: JS, CSS, HTML, SVG
2. **Tree Shaking**: Dead code elimination
3. **Code Splitting**: Shared dependency extraction
4. **Image Optimization**: Automatic compression
5. **Scope Hoisting**: Smaller bundles
6. **Content Hashing**: Cache busting
7. **Differential Bundling**: Modern + legacy browsers
8. **Source Maps**: Optional for debugging

**All enabled by default, no configuration!**

### Differential Bundling (Unique Feature)

Parcel automatically creates two bundles:

```html
<!-- Modern browsers (ES2018+) -->
<script type="module" src="main.modern.js"></script>

<!-- Legacy browsers (ES5) -->
<script nomodule src="main.legacy.js"></script>
```

**Modern browsers:** Smaller bundle, faster execution
**Legacy browsers:** Larger bundle with polyfills

## Pros & Cons for Flask

### Pros
1. **Zero Configuration**: Works out of the box
2. **Automatic Everything**: CSS, images, fonts handled automatically
3. **Fast Setup**: Install and start building in minutes
4. **Good Performance**: Rust compiler is fast
5. **Built-In HMR**: Dev server with hot module replacement
6. **TypeScript Support**: Automatic, no config needed
7. **Differential Bundling**: Modern + legacy browsers
8. **Scope Hoisting**: Smaller bundles than Webpack
9. **Intuitive**: Minimal learning curve
10. **Caching**: Fast subsequent builds

### Cons
1. **Less Control**: Hard to customize build process
2. **Opinionated**: Some decisions can't be overridden
3. **Smaller Ecosystem**: Fewer plugins than Webpack
4. **Manifest Not Built-In**: Needs third-party plugin
5. **Debug Difficulty**: Black box when things go wrong
6. **Bundle Size**: Not as optimized as Rollup/esbuild
7. **Cache Bugs**: Occasionally needs `.parcel-cache` deletion
8. **Community**: Smaller than Webpack/Vite

## Flask Integration Complexity

**Score: LOW**

**Why:**
- Zero configuration to start
- Direct output to Flask static directory
- Simple watch mode works well with Flask
- Optional dev server for HMR
- Automatic asset handling reduces setup

## Use Case Fit for QRCards

### Excellent Fit If:
- Want fastest setup time (zero config)
- Team unfamiliar with bundlers
- Simple to moderate bundling needs
- Don't want to manage loaders/plugins
- Value "just works" experience
- Need TypeScript without config

### Poor Fit If:
- Need maximum bundle size optimization (use Rollup)
- Need fastest build speeds (use esbuild)
- Require extensive customization (use Webpack)
- Want maximum control over build process

## Migration Path

### Phase 1: Install Parcel
```bash
npm init -y
npm install -D parcel
```

### Phase 2: Create Entry Point
```javascript
// src/main.js
import './styles.css'
console.log('Hello from Parcel!')
```

### Phase 3: Build
```bash
npx parcel build src/main.js --dist-dir ../flasklayer/static/js
```

### Phase 4: Add to Template
```jinja2
<script src="{{ url_for('static', filename='js/main.js') }}"></script>
```

**That's it!** No config files, no plugins, no setup.

## Example: Calculator Widget

### Source Structure
```
src/
└── domains/
    └── calculators/
        └── prod/
            ├── main.js
            ├── compound.js
            ├── loan.js
            └── styles.scss  # SCSS works automatically!
```

### main.js (Entry Point)
```javascript
// Import styles (Parcel handles SCSS automatically)
import './styles.scss'

// Import logic
import { initCompound } from './compound.js'
import { initLoan } from './loan.js'

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  initCompound()
  initLoan()
})
```

### Build Command
```bash
parcel build src/domains/calculators/prod/main.js --dist-dir ../flasklayer/static
```

### Output
```
static/
├── main.abc123.js
├── main.def456.css
└── assets/
    └── icon.ghi789.png  # If imported
```

### Template
```jinja2
{% block styles %}
<link rel="stylesheet" href="{{ url_for('static', filename='main.css') }}">
{% endblock %}

{% block scripts %}
<script src="{{ url_for('static', filename='main.js') }}"></script>
{% endblock %}
```

## Automatic Asset Handling Examples

### Images
```javascript
// Automatically optimized and hashed
import icon from './icon.png'
document.getElementById('logo').src = icon
```

### Fonts
```css
/* Automatically bundled */
@font-face {
  font-family: 'CustomFont';
  src: url('./fonts/custom.woff2');
}
```

### TypeScript
```typescript
// Just works, no tsconfig.json required
const greet = (name: string): void => {
  console.log(`Hello, ${name}!`)
}
```

### CSS Modules
```javascript
// Import as module (automatic detection)
import styles from './button.module.css'
element.className = styles.button
```

## Watch Mode vs Dev Server

### Watch Mode (Recommended for Flask)
```bash
parcel watch src/main.js --dist-dir ../flasklayer/static
```

**Pros:**
- Simple, single server (Flask)
- Outputs to static directory
- No CORS issues
- No template conditionals

**Cons:**
- No HMR (manual refresh)
- Slightly slower feedback loop

### Dev Server Mode
```bash
parcel src/main.js
```

**Pros:**
- HMR enabled
- Instant updates
- Better DX

**Cons:**
- Two servers running
- Template conditionals needed
- Potential CORS configuration

## Caching

**Parcel creates `.parcel-cache/` directory:**

```bash
# If builds seem stuck or incorrect:
rm -rf .parcel-cache
npm run build
```

**Good practice:** Add to `.gitignore`:
```
.parcel-cache/
dist/
```

## TypeScript Integration

**Zero configuration TypeScript:**

```typescript
// src/main.ts - Just rename to .ts!
interface Calculator {
  principal: number
  rate: number
  time: number
}

const calculate = (calc: Calculator): number => {
  // Parcel compiles TypeScript automatically
  return calc.principal * Math.pow(1 + calc.rate / 100, calc.time)
}
```

**No tsconfig.json required** (though can add for IDE support)

## Recommendation

**STRONGLY RECOMMENDED for QRCards if:**
- Team wants fastest setup time
- Zero-config appeals to team philosophy
- Simple to moderate bundling needs
- TypeScript support desired without config overhead
- "Convention over configuration" preferred

**Consider Alternatives if:**
- Need maximum performance (esbuild)
- Need maximum bundle optimization (Rollup/Vite)
- Require extensive customization (Webpack)
- Want HMR as priority (Vite)

## Additional Resources

- Parcel Docs: https://parceljs.org
- Getting Started: https://parceljs.org/getting-started/webapp/
- Recipes: https://parceljs.org/recipes/
- Migration Guide: https://parceljs.org/getting-started/migration/
