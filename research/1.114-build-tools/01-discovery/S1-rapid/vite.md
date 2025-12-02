# Vite - Flask Integration Profile

## Overview

**Vite** is a modern build tool that leverages native ES modules in development and Rollup for production builds. Created by Evan You (Vue.js creator), known for exceptional development speed.

## Flask Integration Pattern

### Configuration (`vite.config.js`)

```javascript
import { defineConfig } from 'vite'

export default defineConfig({
  // Build configuration for Flask static directory
  build: {
    outDir: '../flasklayer/static',
    emptyOutDir: false, // Don't delete other static files
    manifest: true, // Generate manifest.json for Jinja2
    rollupOptions: {
      input: {
        'calculators-prod': './src/domains/calculators/prod/main.js',
        'calculators-dev': './src/domains/calculators/dev/main.js',
        'language-prod': './src/domains/language/prod/main.js',
        'recipes-prod': './src/domains/recipes/prod/main.js'
      },
      output: {
        entryFileNames: 'js/[name].[hash].js',
        chunkFileNames: 'js/[name].[hash].js',
        assetFileNames: (assetInfo) => {
          if (assetInfo.name.endsWith('.css')) {
            return 'css/[name].[hash][extname]'
          }
          return 'assets/[name].[hash][extname]'
        }
      }
    }
  },
  // Development server (runs alongside Flask)
  server: {
    port: 5173,
    strictPort: false,
    origin: 'http://localhost:5173'
  }
})
```

### Jinja2 Template Integration

**Option 1: Manifest-based (Production)**
```jinja2
{# Load manifest.json to get hashed filenames #}
{% set manifest = load_manifest('manifest.json') %}

{% block styles %}
<link rel="stylesheet" href="{{ url_for('static', filename=manifest['calculators-prod.css']) }}">
{% endblock %}

{% block scripts %}
<script type="module" src="{{ url_for('static', filename=manifest['calculators-prod.js']) }}"></script>
{% endblock %}
```

**Option 2: Vite Dev Server (Development)**
```jinja2
{% if config.ENV == 'development' %}
  {# Vite dev server with HMR #}
  <script type="module" src="http://localhost:5173/@vite/client"></script>
  <script type="module" src="http://localhost:5173/src/domains/calculators/prod/main.js"></script>
{% else %}
  {# Production bundle #}
  <link rel="stylesheet" href="{{ url_for('static', filename='css/calculators-prod.css') }}">
  <script type="module" src="{{ url_for('static', filename='js/calculators-prod.js') }}"></script>
{% endif %}
```

### Flask Helper (manifest.json loader)

```python
# flasklayer/utils/vite.py
import json
import os
from flask import current_app

def load_manifest():
    """Load Vite manifest.json for production asset paths"""
    manifest_path = os.path.join(
        current_app.static_folder,
        'manifest.json'
    )

    if not os.path.exists(manifest_path):
        return {}

    with open(manifest_path, 'r') as f:
        return json.load(f)

def vite_asset(entry_name):
    """Get asset path from Vite manifest"""
    if current_app.config.get('ENV') == 'development':
        # Return dev server URL
        return f"http://localhost:5173/src/{entry_name}"

    # Load production manifest
    manifest = load_manifest()
    entry = manifest.get(entry_name, {})
    return entry.get('file', entry_name)

# Register as Jinja2 filter
@current_app.template_filter('vite_asset')
def vite_asset_filter(entry_name):
    return vite_asset(entry_name)
```

**Simplified Jinja2 Template:**
```jinja2
{% block scripts %}
<script type="module" src="{{ 'src/domains/calculators/prod/main.js' | vite_asset }}"></script>
{% endblock %}
```

## Development Workflow

### Setup
```bash
# Install Vite
npm install -D vite

# Create directory structure
mkdir -p src/domains/calculators/prod
```

### Running Development Servers

**Terminal 1: Flask Dev Server**
```bash
cd qrcards
./local dev dev  # Runs on port 5000
```

**Terminal 2: Vite Dev Server**
```bash
cd frontend  # Or wherever vite.config.js is
npm run dev  # Runs on port 5173
```

**How It Works:**
1. Flask serves templates from port 5000
2. Vite dev server runs on port 5173 with HMR
3. Templates reference Vite dev server in development mode
4. Changes to JS/CSS trigger HMR (no Flask restart needed)
5. Changes to Jinja2 templates require Flask reload (as normal)

### Hot Module Replacement (HMR)

**Pros:**
- Instant updates for JavaScript/CSS changes
- State preservation during updates
- Fast feedback loop

**Cons:**
- Requires conditional logic in templates (dev vs prod)
- Two servers running during development
- CORS headers may be needed

## Multi-Domain Configuration

### Directory Structure
```
frontend/
├── src/
│   └── domains/
│       ├── calculators/
│       │   ├── prod/
│       │   │   └── main.js
│       │   └── dev/
│       │       └── main.js
│       ├── language/
│       │   └── prod/
│       │       └── main.js
│       └── recipes/
│           └── prod/
│               └── main.js
├── vite.config.js
└── package.json
```

### Shared Dependencies

Vite automatically handles shared dependencies:
```javascript
// src/domains/calculators/prod/main.js
import { formatCurrency } from '../../../shared/utils.js'
import './styles.css'

// Vite will create shared chunk if used by multiple domains
```

**Build Output:**
```
static/
├── js/
│   ├── calculators-prod.abc123.js
│   ├── language-prod.def456.js
│   ├── shared-utils.789xyz.js  # Automatically extracted
│   └── vendor.123abc.js        # Third-party libraries
└── css/
    ├── calculators-prod.abc123.css
    └── language-prod.def456.css
```

## Production Build

### Build Command
```bash
npm run build
```

### Output
```
static/
├── manifest.json          # Asset mapping
├── js/
│   ├── calculators-prod.a1b2c3.js
│   └── shared.d4e5f6.js
└── css/
    └── calculators-prod.a1b2c3.css
```

### Optimization Features
- **Tree Shaking**: Removes unused code
- **Code Splitting**: Automatic shared chunks
- **Minification**: Terser for JS, LightningCSS for CSS
- **Asset Hashing**: Cache busting via filename hashes
- **Source Maps**: Optional for debugging

## Pros & Cons for Flask

### Pros
1. **Fastest Dev Experience**: HMR is instant, no bundler overhead
2. **Simple Configuration**: Minimal config for basic setup
3. **Modern Defaults**: ES modules, CSS preprocessing built-in
4. **Great TypeScript Support**: Built-in, no extra config
5. **Active Community**: Growing ecosystem, good documentation
6. **Plugin System**: Easy to extend (PostCSS, Sass, etc.)
7. **Smart Code Splitting**: Automatic shared chunk extraction

### Cons
1. **Two Servers Required**: Flask + Vite in development
2. **Template Complexity**: Conditional logic for dev vs prod
3. **Flask Not Native**: Designed for SPA frameworks (Vue, React)
4. **Manifest Parsing**: Need Python helper for production
5. **ES Modules Only**: Older browser support requires plugin
6. **CORS Setup**: May need headers for dev server access

## Flask Integration Complexity

**Score: MEDIUM**

**Why:**
- Simple build config, but requires dev/prod template logic
- Need Python helper to parse manifest.json
- Two dev servers add complexity but enable HMR
- Not designed for Flask, but adapts well

## Use Case Fit for QRCards

### Good Fit If:
- Team values fast development experience (HMR)
- Willing to run two dev servers
- Building modern, interactive widgets
- Using TypeScript or want future TS adoption
- Need excellent CSS preprocessing

### Poor Fit If:
- Want single dev server (Flask only)
- Avoiding template conditional logic
- Team unfamiliar with modern JS tooling
- Serving older browsers (IE11)

## Migration Path

### Phase 1: Extract Inline Scripts
```javascript
// Before (in template)
<script>
document.getElementById('form').addEventListener('submit', async (e) => {
  // ... calculator logic
});
</script>

// After (src/domains/calculators/prod/main.js)
import { initCalculator } from './calculator.js'
initCalculator()
```

### Phase 2: Add Vite Config
```javascript
// vite.config.js - minimal starting config
export default {
  build: {
    outDir: '../flasklayer/static',
    rollupOptions: {
      input: './src/main.js'
    }
  }
}
```

### Phase 3: Update Template
```jinja2
{% block scripts %}
{{ super() }}
{% if config.ENV == 'development' %}
  <script type="module" src="http://localhost:5173/src/main.js"></script>
{% else %}
  <script type="module" src="{{ url_for('static', filename='js/main.js') }}"></script>
{% endif %}
{% endblock %}
```

## Example: Calculator Widget

### Source Structure
```
src/
├── domains/
│   └── calculators/
│       └── prod/
│           ├── main.js
│           ├── compound-interest.js
│           ├── loan-payment.js
│           └── styles.css
└── shared/
    ├── api-client.js
    └── formatters.js
```

### main.js
```javascript
import './styles.css'
import { initCompoundInterest } from './compound-interest.js'
import { initLoanPayment } from './loan-payment.js'

// Initialize all calculators on page load
document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('compound-interest-form')) {
    initCompoundInterest()
  }
  if (document.getElementById('loan-payment-form')) {
    initLoanPayment()
  }
})
```

### compound-interest.js
```javascript
import { apiClient } from '../../shared/api-client.js'
import { formatCurrency } from '../../shared/formatters.js'

export function initCompoundInterest() {
  const form = document.getElementById('compound-interest-form')

  form.addEventListener('submit', async (e) => {
    e.preventDefault()

    const data = {
      principal: parseFloat(form.principal.value),
      rate: parseFloat(form.rate.value),
      time: parseFloat(form.time.value)
    }

    const result = await apiClient.post('/api/v1/calculators/compound-interest', data)

    document.getElementById('final-amount').textContent =
      formatCurrency(result.data.final_amount)
  })
}
```

## Recommendation

**RECOMMENDED for QRCards if:**
- Team prioritizes development speed
- Comfortable managing two dev servers
- Building complex, interactive widgets
- Want best-in-class HMR experience

**Consider Alternatives if:**
- Prefer simpler, single-server setup
- Want zero config (consider Parcel)
- Need backend-agnostic build (consider esbuild)

## Additional Resources

- Vite Docs: https://vitejs.dev
- Flask + Vite Examples: https://github.com/topics/flask-vite
- Backend Integration Guide: https://vitejs.dev/guide/backend-integration.html
