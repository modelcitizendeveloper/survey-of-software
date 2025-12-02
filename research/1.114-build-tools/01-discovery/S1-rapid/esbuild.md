# esbuild - Flask Integration Profile

## Overview

**esbuild** is an extremely fast JavaScript bundler written in Go. Known for build speeds 10-100x faster than Webpack/Parcel. Minimal configuration, focused on speed and simplicity.

## Flask Integration Pattern

### Configuration (`esbuild.config.js`)

```javascript
const esbuild = require('esbuild')
const path = require('path')
const fs = require('fs')

// Plugin to generate manifest.json for Flask
const manifestPlugin = {
  name: 'manifest',
  setup(build) {
    build.onEnd(result => {
      const manifest = {}

      // Parse output files to create manifest
      for (const file of result.metafile.outputs) {
        const relativePath = path.relative(
          build.initialOptions.outdir,
          file
        )
        // Extract entry name from path
        const entryName = path.basename(relativePath)
        manifest[entryName] = relativePath
      }

      // Write manifest.json
      fs.writeFileSync(
        path.join(build.initialOptions.outdir, 'manifest.json'),
        JSON.stringify(manifest, null, 2)
      )
    })
  }
}

// Build configuration
esbuild.build({
  // Entry points for multi-domain
  entryPoints: {
    'js/calculators-prod': './src/domains/calculators/prod/main.js',
    'js/calculators-dev': './src/domains/calculators/dev/main.js',
    'js/language-prod': './src/domains/language/prod/main.js',
    'js/recipes-prod': './src/domains/recipes/prod/main.js'
  },

  // Output to Flask static directory
  outdir: '../flasklayer/static',

  // Bundle settings
  bundle: true,
  minify: process.env.NODE_ENV === 'production',
  sourcemap: process.env.NODE_ENV === 'development',

  // Code splitting for shared dependencies
  splitting: true,
  format: 'esm', // Required for splitting

  // Asset handling
  loader: {
    '.png': 'file',
    '.jpg': 'file',
    '.svg': 'file',
    '.woff': 'file',
    '.woff2': 'file'
  },

  // Asset output path
  assetNames: 'assets/[name]-[hash]',

  // Content hashing for cache busting
  entryNames: '[dir]/[name]-[hash]',
  chunkNames: 'chunks/[name]-[hash]',

  // Generate metafile for manifest
  metafile: true,

  // Public path for assets
  publicPath: '/static/',

  // Add manifest plugin
  plugins: [manifestPlugin]
}).catch(() => process.exit(1))
```

### Simpler Configuration (No Hashing)

```javascript
// esbuild.simple.js - Quick start
const esbuild = require('esbuild')

esbuild.build({
  entryPoints: ['./src/main.js'],
  outfile: '../flasklayer/static/js/bundle.js',
  bundle: true,
  minify: true
}).catch(() => process.exit(1))
```

### Watch Mode for Development

```javascript
// esbuild.watch.js
const esbuild = require('esbuild')

const ctx = await esbuild.context({
  entryPoints: {
    'js/calculators-prod': './src/domains/calculators/prod/main.js'
  },
  outdir: '../flasklayer/static',
  bundle: true,
  sourcemap: true,
  splitting: true,
  format: 'esm'
})

// Watch for changes
await ctx.watch()
console.log('esbuild watching for changes...')
```

### Flask Helper for Assets

```python
# flasklayer/utils/esbuild.py
import json
import os
from flask import current_app, url_for
from functools import lru_cache

@lru_cache(maxsize=1)
def load_esbuild_manifest():
    """Load esbuild manifest.json"""
    manifest_path = os.path.join(
        current_app.static_folder,
        'manifest.json'
    )

    if not os.path.exists(manifest_path):
        # No manifest in development, use direct paths
        return {}

    with open(manifest_path, 'r') as f:
        return json.load(f)

def esbuild_asset(asset_name):
    """
    Get asset path from esbuild manifest

    Usage:
        esbuild_asset('js/calculators-prod.js')
        # Returns: 'js/calculators-prod-ABC123.js'
    """
    manifest = load_esbuild_manifest()

    # If no manifest, assume development mode
    if not manifest:
        return asset_name

    return manifest.get(asset_name, asset_name)

def init_esbuild_helpers(app):
    """Register esbuild template helpers"""

    @app.template_filter('esbuild_asset')
    def esbuild_asset_filter(asset_name):
        return esbuild_asset(asset_name)

    @app.context_processor
    def esbuild_helpers():
        return {'esbuild_asset': esbuild_asset}
```

### Jinja2 Template Integration

**Simple Pattern (No Hashing):**
```jinja2
{% block scripts %}
{{ super() }}
<script type="module" src="{{ url_for('static', filename='js/calculators-prod.js') }}"></script>
{% endblock %}
```

**With Manifest (Production Hashing):**
```jinja2
{% block scripts %}
{{ super() }}
<script type="module" src="{{ url_for('static', filename='js/calculators-prod.js' | esbuild_asset) }}"></script>
{% endblock %}
```

**CSS Handling:**
esbuild doesn't extract CSS by default. Options:
1. Import CSS in JS (injected via `<style>` tags)
2. Use plugin for CSS extraction
3. Process CSS separately

```javascript
// Option 1: CSS in JS (default)
import './styles.css' // Injected as <style> tag

// Option 2: CSS extraction plugin
const cssPlugin = require('esbuild-css-modules-plugin')
// Add to plugins array
```

## Development Workflow

### Setup
```bash
# Install esbuild (single dependency!)
npm install -D esbuild
```

### package.json Scripts
```json
{
  "scripts": {
    "dev": "node esbuild.watch.js",
    "build": "NODE_ENV=production node esbuild.config.js",
    "build:analyze": "node esbuild.config.js --analyze"
  }
}
```

### Running Development

**Terminal 1: esbuild watch**
```bash
npm run dev
# esbuild rebuilds on file changes (extremely fast)
```

**Terminal 2: Flask dev server**
```bash
./local dev dev
# Refresh browser to see changes
```

**No Dev Server Required:**
- esbuild doesn't have built-in dev server
- Watch mode rebuilds instantly (< 100ms typical)
- Refresh browser manually (or use Flask auto-reload)
- Simpler setup than Vite/Webpack dev servers

## Multi-Domain Configuration

### Entry Points
```javascript
esbuild.build({
  entryPoints: {
    'js/calculators-prod': './src/domains/calculators/prod/main.js',
    'js/calculators-dev': './src/domains/calculators/dev/main.js',
    'js/language-prod': './src/domains/language/prod/main.js',
    'js/recipes-prod': './src/domains/recipes/prod/main.js'
  },
  outdir: '../flasklayer/static',
  bundle: true,
  splitting: true, // Automatic shared chunk extraction
  format: 'esm'
})
```

### Code Splitting Output
```
static/
├── js/
│   ├── calculators-prod-ABC123.js
│   ├── language-prod-DEF456.js
│   └── recipes-prod-GHI789.js
└── chunks/
    └── shared-JKL012.js  # Automatically extracted shared code
```

### Shared Dependencies
esbuild automatically extracts shared code when `splitting: true`:

```javascript
// src/domains/calculators/prod/main.js
import { apiClient } from '../../../shared/api.js'

// src/domains/language/prod/main.js
import { apiClient } from '../../../shared/api.js'

// esbuild creates: chunks/shared-HASH.js containing apiClient
```

**Template loads chunks automatically:**
```jinja2
{# Browser automatically loads shared chunks via ES modules #}
<script type="module" src="{{ url_for('static', filename='js/calculators-prod.js') }}"></script>
```

## Production Build

### Build Command
```bash
NODE_ENV=production npm run build
```

### Optimization Features

1. **Minification**: Built-in, extremely fast
2. **Tree Shaking**: Removes unused code
3. **Code Splitting**: Automatic with `splitting: true`
4. **Source Maps**: Optional for debugging
5. **Bundle Analysis**: Via metafile

**No Built-In:**
- CSS extraction (needs plugin)
- Image optimization (needs plugin)
- Advanced transforms (Babel features)

### Bundle Analysis
```javascript
// esbuild.config.js
const result = await esbuild.build({
  // ... config
  metafile: true
})

// Write metafile for analysis
fs.writeFileSync('meta.json', JSON.stringify(result.metafile))

// Analyze with esbuild-visualizer or online tool
```

## Pros & Cons for Flask

### Pros
1. **Extreme Speed**: 10-100x faster than Webpack
2. **Simple Configuration**: Minimal boilerplate
3. **Single Dependency**: Just `esbuild` in package.json
4. **No Dev Server Complexity**: Watch mode is sufficient
5. **TypeScript Built-In**: Native TS support, no loader needed
6. **Instant Rebuilds**: < 100ms typical for medium projects
7. **Low Learning Curve**: Straightforward API, few concepts
8. **Code Splitting**: Automatic shared chunk extraction
9. **Tree Shaking**: Excellent dead code elimination
10. **Small node_modules**: Minimal dependencies

### Cons
1. **Limited Plugin Ecosystem**: Fewer plugins than Webpack
2. **CSS Extraction**: Needs plugin or workaround
3. **No HMR**: Watch mode only, no hot module replacement
4. **Less Mature**: Newer tool, fewer Flask examples
5. **No Advanced Transforms**: Limited Babel-like features
6. **Asset Handling**: Basic compared to Webpack loaders
7. **Smaller Community**: Less Stack Overflow content

## Flask Integration Complexity

**Score: LOW**

**Why:**
- No dev server simplifies setup (just watch mode)
- Minimal configuration required
- Direct output to Flask static directory
- Optional manifest for cache busting
- No complex plugin chains

## Use Case Fit for QRCards

### Excellent Fit If:
- Build speed is top priority
- Want minimal configuration
- Simple bundling needs (JS/TS, basic CSS)
- Team values simplicity over flexibility
- No need for complex asset pipeline
- Prefer single dev server (Flask only)

### Poor Fit If:
- Need extensive CSS preprocessing (Sass, PostCSS)
- Want HMR (hot module replacement)
- Require advanced Babel transforms
- Need large plugin ecosystem
- Complex asset handling (images, fonts, etc.)

## Migration Path

### Phase 1: Install esbuild
```bash
npm install -D esbuild
```

### Phase 2: Create Build Script
```javascript
// build.js
require('esbuild').build({
  entryPoints: ['./src/main.js'],
  outfile: '../flasklayer/static/js/bundle.js',
  bundle: true,
  minify: true
}).catch(() => process.exit(1))
```

### Phase 3: Add to package.json
```json
{
  "scripts": {
    "build": "node build.js"
  }
}
```

### Phase 4: Update Template
```jinja2
<script type="module" src="{{ url_for('static', filename='js/bundle.js') }}"></script>
```

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

### esbuild Config
```javascript
// esbuild.config.js
const esbuild = require('esbuild')

esbuild.build({
  entryPoints: {
    'js/calculators-prod': './src/domains/calculators/prod/main.js'
  },
  outdir: '../flasklayer/static',
  bundle: true,
  minify: process.env.NODE_ENV === 'production',
  splitting: true,
  format: 'esm',
  sourcemap: true
})
```

### main.js
```javascript
// Import styles (injected as <style> tag)
import './styles.css'

// Import logic
import { initCompound } from './compound.js'
import { initLoan } from './loan.js'

// Initialize
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
└── chunks/
    └── shared.js  # If shared code detected
```

### Template
```jinja2
{% block scripts %}
{{ super() }}
<script type="module" src="{{ url_for('static', filename='js/calculators-prod.js') }}"></script>
{% endblock %}
```

## CSS Handling Options

### Option 1: CSS-in-JS (Default)
```javascript
// Imported CSS injected as <style> tags
import './styles.css'
// Fast, but FOUC (Flash of Unstyled Content) possible
```

### Option 2: External CSS Plugin
```javascript
const { sassPlugin } = require('esbuild-sass-plugin')

esbuild.build({
  // ... config
  plugins: [sassPlugin()]
})
```

### Option 3: Separate CSS Build
```bash
# Process CSS separately with PostCSS or Sass
npm run build:css  # Separate command
npm run build:js   # esbuild
```

## TypeScript Support

**Native TypeScript support (no config needed):**

```javascript
// esbuild.config.js
esbuild.build({
  entryPoints: ['./src/main.ts'],  // .ts file
  outfile: '../flasklayer/static/js/bundle.js',
  bundle: true
  // TypeScript compiled automatically!
})
```

**No tsconfig.json required** (though recommended for IDE support)

## Performance Comparison

**Benchmark (medium project, ~1000 modules):**

| Bundler | Initial Build | Rebuild (Watch) |
|---------|--------------|-----------------|
| esbuild | 0.3s | 0.05s |
| Vite | 1.2s | 0.1s (HMR) |
| Webpack 5 | 5.8s | 1.2s |
| Parcel 2 | 4.2s | 0.8s |

**Why so fast?**
- Written in Go (compiled, not JS)
- Parallelized build process
- Efficient AST parsing
- Minimal overhead

## Recommendation

**STRONGLY RECOMMENDED for QRCards if:**
- Build speed is critical
- Prefer simplicity over features
- TypeScript support desired
- No complex asset pipeline needed
- Want minimal configuration
- Team values fast iteration

**Consider Alternatives if:**
- Need advanced CSS preprocessing (Webpack)
- Want HMR (Vite)
- Require extensive plugin ecosystem (Webpack)
- Need zero-config (Parcel)

## Additional Resources

- esbuild Docs: https://esbuild.github.io
- esbuild Plugins: https://github.com/esbuild/community-plugins
- Performance: https://esbuild.github.io/faq/#benchmark-details
- TypeScript: https://esbuild.github.io/content-types/#typescript
