# Rollup - Flask Integration Profile

## Overview

**Rollup** is a module bundler optimized for libraries and tree shaking. Vite uses Rollup for production builds. Known for creating smaller bundles via aggressive dead code elimination. Popular for npm package authoring.

## Flask Integration Pattern

### Configuration (`rollup.config.js`)

```javascript
import resolve from '@rollup/plugin-node-resolve'
import commonjs from '@rollup/plugin-commonjs'
import { babel } from '@rollup/plugin-babel'
import terser from '@rollup/plugin-terser'
import postcss from 'rollup-plugin-postcss'
import { hash } from 'rollup-plugin-hash'

export default {
  // Multi-domain entry points
  input: {
    'calculators-prod': 'src/domains/calculators/prod/main.js',
    'calculators-dev': 'src/domains/calculators/dev/main.js',
    'language-prod': 'src/domains/language/prod/main.js',
    'recipes-prod': 'src/domains/recipes/prod/main.js'
  },

  // Output to Flask static directory
  output: {
    dir: '../flasklayer/static/js',
    format: 'esm', // ES modules for modern browsers
    entryFileNames: '[name].[hash].js',
    chunkFileNames: '[name].[hash].js',
    sourcemap: process.env.NODE_ENV === 'development'
  },

  plugins: [
    // Resolve node_modules
    resolve({
      browser: true
    }),

    // Convert CommonJS to ES modules
    commonjs(),

    // Process CSS
    postcss({
      extract: true,
      extract: '../css/[name].[hash].css',
      minimize: process.env.NODE_ENV === 'production',
      sourceMap: process.env.NODE_ENV === 'development'
    }),

    // Babel for older browser support
    babel({
      babelHelpers: 'bundled',
      exclude: 'node_modules/**',
      presets: ['@babel/preset-env']
    }),

    // Minification (production)
    process.env.NODE_ENV === 'production' && terser(),

    // Generate manifest.json
    hash({
      dest: '../flasklayer/static/manifest.json',
      manifest: true
    })
  ],

  // Code splitting configuration
  manualChunks: {
    // Extract vendor libraries
    vendor: ['module-name-1', 'module-name-2']
  }
}
```

### Simpler Configuration

```javascript
// rollup.config.simple.js
import resolve from '@rollup/plugin-node-resolve'
import commonjs from '@rollup/plugin-commonjs'

export default {
  input: 'src/main.js',
  output: {
    file: '../flasklayer/static/js/bundle.js',
    format: 'iife', // Immediately Invoked Function Expression
    name: 'App'
  },
  plugins: [
    resolve(),
    commonjs()
  ]
}
```

### Flask Helper for Manifest

```python
# flasklayer/utils/rollup.py
import json
import os
from flask import current_app
from functools import lru_cache

@lru_cache(maxsize=1)
def load_rollup_manifest():
    """Load Rollup manifest.json"""
    manifest_path = os.path.join(
        current_app.static_folder,
        'manifest.json'
    )

    if not os.path.exists(manifest_path):
        return {}

    with open(manifest_path, 'r') as f:
        return json.load(f)

def rollup_asset(asset_name):
    """
    Get hashed asset path from Rollup manifest

    Usage:
        rollup_asset('js/calculators-prod.js')
        # Returns: 'js/calculators-prod-a1b2c3.js'
    """
    manifest = load_rollup_manifest()
    return manifest.get(asset_name, asset_name)

def init_rollup_helpers(app):
    """Register Rollup template helpers"""

    @app.template_filter('rollup_asset')
    def rollup_asset_filter(asset_name):
        return rollup_asset(asset_name)

    @app.context_processor
    def rollup_helpers():
        return {'rollup_asset': rollup_asset}
```

### Jinja2 Template Integration

**Simple Pattern (IIFE format, no hashing):**
```jinja2
{% block scripts %}
{{ super() }}
<script src="{{ url_for('static', filename='js/bundle.js') }}"></script>
{% endblock %}
```

**ES Modules with Manifest:**
```jinja2
{% block scripts %}
{{ super() }}
<script type="module" src="{{ url_for('static', filename='js/calculators-prod.js' | rollup_asset) }}"></script>
{% endblock %}
```

## Development Workflow

### Setup
```bash
# Install Rollup and plugins
npm install -D rollup
npm install -D @rollup/plugin-node-resolve
npm install -D @rollup/plugin-commonjs
npm install -D @rollup/plugin-babel
npm install -D @rollup/plugin-terser
npm install -D rollup-plugin-postcss
```

### package.json Scripts
```json
{
  "scripts": {
    "dev": "rollup -c -w",
    "build": "NODE_ENV=production rollup -c",
    "build:analyze": "rollup -c --bundleConfigAsCjs"
  }
}
```

### Running Development

**Watch Mode (No Dev Server):**
```bash
# Terminal 1: Rollup watch
npm run dev

# Terminal 2: Flask dev server
./local dev dev

# Rollup rebuilds on file changes, refresh browser manually
```

**No HMR:** Rollup doesn't have built-in dev server or HMR. Watch mode only.

### Development Experience
- **Fast Rebuilds**: Faster than Webpack, slower than esbuild
- **No Dev Server**: Watch mode rebuilds to Flask static directory
- **Manual Refresh**: Browser refresh required (no HMR)
- **Simple Setup**: Single dev server (Flask only)

## Multi-Domain Configuration

### Manual Chunks Strategy

```javascript
// rollup.config.js
export default {
  input: {
    'calculators-prod': 'src/domains/calculators/prod/main.js',
    'language-prod': 'src/domains/language/prod/main.js',
    'recipes-prod': 'src/domains/recipes/prod/main.js'
  },

  output: {
    dir: '../flasklayer/static/js',
    format: 'esm',
    chunkFileNames: '[name].[hash].js',
    manualChunks: (id) => {
      // Extract node_modules to vendor chunk
      if (id.includes('node_modules')) {
        return 'vendor'
      }
      // Extract shared utils to common chunk
      if (id.includes('src/shared')) {
        return 'common'
      }
    }
  }
}
```

### Output Structure
```
static/
├── manifest.json
├── js/
│   ├── vendor.abc123.js         # node_modules
│   ├── common.def456.js         # shared utilities
│   ├── calculators-prod.ghi789.js
│   ├── language-prod.jkl012.js
│   └── recipes-prod.mno345.js
└── css/
    ├── calculators-prod.abc123.css
    └── language-prod.def456.css
```

### Template Loading
```jinja2
{# ES modules automatically load dependencies #}
<script type="module" src="{{ url_for('static', filename='js/calculators-prod.js' | rollup_asset) }}"></script>

{# Browser fetches vendor.js and common.js automatically #}
```

## Production Build

### Build Command
```bash
NODE_ENV=production npm run build
```

### Optimization Features

1. **Tree Shaking**: Best-in-class dead code elimination
2. **Code Splitting**: Manual chunks + automatic shared dependencies
3. **Minification**: Terser plugin for JS minification
4. **Scope Hoisting**: Flattens module scope for smaller bundles
5. **Asset Hashing**: Cache busting via hash plugin
6. **Source Maps**: Optional for debugging

**Rollup's Strength:** Superior tree shaking produces smallest bundles.

### Advanced Configuration
```javascript
import { visualizer } from 'rollup-plugin-visualizer'
import analyze from 'rollup-plugin-analyzer'

export default {
  // ... config
  plugins: [
    // ... other plugins

    // Bundle analysis
    process.env.ANALYZE && visualizer({
      filename: 'bundle-stats.html',
      open: true
    }),

    // Size analysis
    process.env.ANALYZE && analyze({
      summaryOnly: true
    })
  ]
}
```

## Pros & Cons for Flask

### Pros
1. **Best Tree Shaking**: Smallest production bundles
2. **Simple Config**: More straightforward than Webpack
3. **ES Modules Native**: First-class ES module support
4. **No Dev Server Complexity**: Watch mode sufficient
5. **Flexible Output**: Multiple formats (ESM, IIFE, UMD, CJS)
6. **Library-Friendly**: Great for reusable components
7. **Vite Uses It**: Same production build as Vite
8. **Plugin Ecosystem**: Good selection of official plugins
9. **Scope Hoisting**: Efficient code structure

### Cons
1. **No HMR**: Watch mode only, manual refresh required
2. **Slower Than esbuild**: Not as fast for development builds
3. **Plugin Configuration**: Requires setup for common tasks
4. **Less Beginner-Friendly**: More concepts than Parcel
5. **No Built-In CSS**: Needs plugin for CSS processing
6. **No Dev Server**: No browser sync or live reload
7. **Smaller Community**: Less popular than Webpack, fewer Stack Overflow answers

## Flask Integration Complexity

**Score: LOW-MEDIUM**

**Why:**
- Simple watch mode (no dev server)
- Direct output to Flask static directory
- Plugin setup required for CSS, Babel, etc.
- Manifest generation needs plugin
- No HMR adds simplicity but reduces DX

## Use Case Fit for QRCards

### Good Fit If:
- Want smallest production bundles (tree shaking priority)
- Don't need HMR (manual refresh acceptable)
- Prefer simple, single-server setup (Flask only)
- Building reusable widget libraries
- Value ES module output
- Want Vite-like production quality without dev server

### Poor Fit If:
- Need HMR for development
- Want zero-config setup (consider Parcel)
- Need fastest build times (consider esbuild)
- Require extensive plugin ecosystem (consider Webpack)

## Migration Path

### Phase 1: Install Rollup
```bash
npm install -D rollup @rollup/plugin-node-resolve @rollup/plugin-commonjs
```

### Phase 2: Basic Config
```javascript
// rollup.config.js
export default {
  input: 'src/main.js',
  output: {
    file: '../flasklayer/static/js/bundle.js',
    format: 'iife'
  },
  plugins: [
    require('@rollup/plugin-node-resolve')(),
    require('@rollup/plugin-commonjs')()
  ]
}
```

### Phase 3: Add Watch Mode
```json
{
  "scripts": {
    "dev": "rollup -c -w"
  }
}
```

### Phase 4: Expand to Multi-Domain
Add multiple entry points and code splitting as needed.

## Example: Calculator Widget

### Source Structure
```
src/
├── domains/
│   └── calculators/
│       └── prod/
│           ├── main.js
│           ├── compound.js
│           ├── loan.js
│           └── styles.css
└── shared/
    ├── api.js
    └── formatters.js
```

### Rollup Config
```javascript
import resolve from '@rollup/plugin-node-resolve'
import commonjs from '@rollup/plugin-commonjs'
import postcss from 'rollup-plugin-postcss'

export default {
  input: 'src/domains/calculators/prod/main.js',

  output: {
    file: '../flasklayer/static/js/calculators-prod.js',
    format: 'esm',
    sourcemap: true
  },

  plugins: [
    resolve(),
    commonjs(),
    postcss({
      extract: '../css/calculators-prod.css'
    })
  ]
}
```

### main.js
```javascript
import './styles.css'
import { initCompound } from './compound.js'
import { initLoan } from './loan.js'

document.addEventListener('DOMContentLoaded', () => {
  initCompound()
  initLoan()
})
```

### Build Output
```
static/
├── js/
│   └── calculators-prod.js
└── css/
    └── calculators-prod.css
```

### Template
```jinja2
{% block styles %}
{{ super() }}
<link rel="stylesheet" href="{{ url_for('static', filename='css/calculators-prod.css') }}">
{% endblock %}

{% block scripts %}
{{ super() }}
<script type="module" src="{{ url_for('static', filename='js/calculators-prod.js') }}"></script>
{% endblock %}
```

## Tree Shaking Example

**Why Rollup Excels:**

```javascript
// utils.js
export function add(a, b) { return a + b }
export function subtract(a, b) { return a - b }
export function multiply(a, b) { return a * b }
export function divide(a, b) { return a / b }

// main.js
import { add } from './utils.js'
console.log(add(2, 3))

// Rollup output: Only includes add(), removes unused functions
// Webpack: May include all functions depending on config
// Result: Smaller bundle size
```

## Output Format Comparison

**IIFE (Browser Global):**
```javascript
output: {
  format: 'iife',
  name: 'Calculators'
}
// Creates window.Calculators
```

**ESM (Modern Browsers):**
```javascript
output: {
  format: 'esm'
}
// <script type="module">
```

**UMD (Universal):**
```javascript
output: {
  format: 'umd',
  name: 'Calculators'
}
// Works as script tag, AMD, or CommonJS
```

## Recommendation

**CONSIDER for QRCards if:**
- Production bundle size is top priority
- HMR not required (manual refresh acceptable)
- Want ES module output
- Building widget libraries for reuse
- Prefer simple watch mode over dev server

**Use Vite Instead if:**
- Want HMR for better DX
- Need full dev server features
- Same production quality (Vite uses Rollup)

**Use esbuild Instead if:**
- Build speed more important than bundle size
- Want even simpler configuration

## Additional Resources

- Rollup Docs: https://rollupjs.org
- Plugins: https://github.com/rollup/awesome
- Tree Shaking Guide: https://rollupjs.org/guide/en/#tree-shaking
- Vite (uses Rollup): https://vitejs.dev
