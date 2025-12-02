# Webpack 5 - Flask Integration Profile

## Overview

**Webpack 5** is the industry-standard module bundler with massive ecosystem and extensive plugin support. Battle-tested for Flask integration with established patterns.

## Flask Integration Pattern

### Configuration (`webpack.config.js`)

```javascript
const path = require('path')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const { WebpackManifestPlugin } = require('webpack-manifest-plugin')

module.exports = {
  mode: process.env.NODE_ENV || 'development',

  // Multiple entry points for multi-domain
  entry: {
    'calculators-prod': './src/domains/calculators/prod/main.js',
    'calculators-dev': './src/domains/calculators/dev/main.js',
    'language-prod': './src/domains/language/prod/main.js',
    'recipes-prod': './src/domains/recipes/prod/main.js'
  },

  output: {
    path: path.resolve(__dirname, '../flasklayer/static'),
    filename: 'js/[name].[contenthash:8].js',
    chunkFilename: 'js/[name].[contenthash:8].js',
    clean: false, // Don't delete other static files
    publicPath: '/static/' // Flask static URL prefix
  },

  optimization: {
    splitChunks: {
      cacheGroups: {
        // Extract shared vendor libraries
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendor',
          chunks: 'all'
        },
        // Extract shared app code
        common: {
          minChunks: 2,
          name: 'common',
          chunks: 'all',
          reuseExistingChunk: true
        }
      }
    }
  },

  module: {
    rules: [
      // JavaScript/TypeScript
      {
        test: /\.(js|ts)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-typescript']
          }
        }
      },
      // CSS
      {
        test: /\.css$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'postcss-loader'
        ]
      },
      // Sass/SCSS
      {
        test: /\.s[ac]ss$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'postcss-loader',
          'sass-loader'
        ]
      },
      // Images/Fonts
      {
        test: /\.(png|svg|jpg|jpeg|gif|woff|woff2|eot|ttf|otf)$/,
        type: 'asset/resource',
        generator: {
          filename: 'assets/[name].[hash:8][ext]'
        }
      }
    ]
  },

  plugins: [
    // Extract CSS to separate files
    new MiniCssExtractPlugin({
      filename: 'css/[name].[contenthash:8].css'
    }),
    // Generate manifest.json for Flask
    new WebpackManifestPlugin({
      fileName: 'manifest.json',
      publicPath: '/static/',
      generate: (seed, files) => {
        return files.reduce((manifest, file) => {
          // Remove hash from key for easier template lookup
          const name = file.name.replace(/\.[a-f0-9]{8}\./, '.')
          manifest[name] = file.path
          return manifest
        }, seed)
      }
    })
  ],

  // Development server (optional - for HMR)
  devServer: {
    port: 8080,
    hot: true,
    headers: {
      'Access-Control-Allow-Origin': '*'
    },
    static: {
      directory: path.resolve(__dirname, '../flasklayer/static')
    }
  },

  resolve: {
    extensions: ['.js', '.ts', '.json'],
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  }
}
```

### Flask Helper for Manifest

```python
# flasklayer/utils/webpack.py
import json
import os
from flask import current_app, url_for
from functools import lru_cache

@lru_cache(maxsize=1)
def load_webpack_manifest():
    """Load webpack manifest.json (cached)"""
    manifest_path = os.path.join(
        current_app.static_folder,
        'manifest.json'
    )

    if not os.path.exists(manifest_path):
        current_app.logger.warning("Webpack manifest.json not found")
        return {}

    with open(manifest_path, 'r') as f:
        return json.load(f)

def webpack_asset(asset_name):
    """
    Get asset path from webpack manifest

    Usage:
        webpack_asset('js/calculators-prod.js')
        # Returns: 'js/calculators-prod.a1b2c3d4.js'
    """
    manifest = load_webpack_manifest()
    return manifest.get(asset_name, asset_name)

def init_webpack_helpers(app):
    """Register webpack template helpers"""

    @app.template_filter('webpack_asset')
    def webpack_asset_filter(asset_name):
        """
        Jinja2 filter for webpack assets

        Usage in template:
            {{ 'js/calculators-prod.js' | webpack_asset }}
        """
        return webpack_asset(asset_name)

    @app.context_processor
    def webpack_helpers():
        """Add webpack helper to all templates"""
        return {
            'webpack_asset': webpack_asset
        }
```

### Jinja2 Template Integration

**Simple Pattern (Recommended):**
```jinja2
{% block styles %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/calculators-prod.css' | webpack_asset) }}">
{% endblock %}

{% block scripts %}
{{ super() }}
<script src="{{ url_for('static', filename='js/vendor.js' | webpack_asset) }}"></script>
<script src="{{ url_for('static', filename='js/calculators-prod.js' | webpack_asset) }}"></script>
{% endblock %}
```

**Development with HMR (Optional):**
```jinja2
{% if config.ENV == 'development' and config.WEBPACK_DEV_SERVER %}
  {# Development: Use webpack-dev-server #}
  <script src="http://localhost:8080/js/vendor.js"></script>
  <script src="http://localhost:8080/js/calculators-prod.js"></script>
{% else %}
  {# Production: Use bundled assets #}
  <script src="{{ url_for('static', filename=webpack_asset('js/vendor.js')) }}"></script>
  <script src="{{ url_for('static', filename=webpack_asset('js/calculators-prod.js')) }}"></script>
{% endif %}
```

## Development Workflow

### Setup
```bash
# Install webpack and dependencies
npm install -D webpack webpack-cli webpack-dev-server
npm install -D mini-css-extract-plugin webpack-manifest-plugin
npm install -D babel-loader @babel/core @babel/preset-env
npm install -D css-loader postcss-loader sass-loader
```

### package.json Scripts
```json
{
  "scripts": {
    "dev": "webpack --mode development --watch",
    "dev:server": "webpack serve --mode development",
    "build": "webpack --mode production",
    "build:stats": "webpack --mode production --json > webpack-stats.json"
  }
}
```

### Running Development

**Option 1: Watch Mode (Simpler)**
```bash
# Terminal 1: Webpack watch
npm run dev

# Terminal 2: Flask dev server
./local dev dev

# Changes trigger rebuild, refresh browser manually
```

**Option 2: Dev Server with HMR (Advanced)**
```bash
# Terminal 1: Webpack dev server
npm run dev:server

# Terminal 2: Flask dev server
./local dev dev

# Changes trigger HMR, browser updates automatically
```

## Multi-Domain Configuration

### Entry Points Strategy

```javascript
// webpack.config.js
module.exports = {
  entry: {
    // Domain-specific bundles
    'calculators-prod': './src/domains/calculators/prod/main.js',
    'calculators-dev': './src/domains/calculators/dev/main.js',
    'language-prod': './src/domains/language/prod/main.js',
    'recipes-prod': './src/domains/recipes/prod/main.js',

    // Shared utilities (optional manual entry)
    'shared-utils': './src/shared/index.js'
  },

  optimization: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        // Vendor code (node_modules)
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendor',
          priority: 10
        },
        // Shared app code between domains
        common: {
          minChunks: 2,
          name: 'common',
          priority: 5,
          reuseExistingChunk: true
        }
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
│   ├── vendor.a1b2c3d4.js        # All node_modules
│   ├── common.e5f6g7h8.js        # Shared domain code
│   ├── calculators-prod.i9j0k1l2.js
│   ├── calculators-dev.m3n4o5p6.js
│   ├── language-prod.q7r8s9t0.js
│   └── recipes-prod.u1v2w3x4.js
└── css/
    ├── calculators-prod.a1b2c3d4.css
    └── language-prod.e5f6g7h8.css
```

### Template Loading Pattern
```jinja2
{# Load vendor + common chunks first #}
<script src="{{ url_for('static', filename=webpack_asset('js/vendor.js')) }}"></script>
<script src="{{ url_for('static', filename=webpack_asset('js/common.js')) }}"></script>

{# Then domain-specific bundle #}
<script src="{{ url_for('static', filename=webpack_asset('js/calculators-prod.js')) }}"></script>
```

## Production Build

### Build Command
```bash
npm run build
```

### Optimization Features

1. **Tree Shaking**: Removes unused exports
2. **Code Splitting**: Automatic vendor/common chunks
3. **Minification**: TerserPlugin for JS (built-in)
4. **CSS Optimization**: CssMinimizerPlugin
5. **Asset Hashing**: Content hash for cache busting
6. **Source Maps**: Optional for debugging
7. **Bundle Analysis**: webpack-bundle-analyzer plugin

### Advanced Production Config
```javascript
const TerserPlugin = require('terser-webpack-plugin')
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin')
const CompressionPlugin = require('compression-webpack-plugin')

module.exports = {
  mode: 'production',

  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          compress: {
            drop_console: true // Remove console.log in production
          }
        }
      }),
      new CssMinimizerPlugin()
    ]
  },

  plugins: [
    // Gzip compression
    new CompressionPlugin({
      filename: '[path][base].gz',
      algorithm: 'gzip',
      test: /\.(js|css|html|svg)$/,
      threshold: 10240,
      minRatio: 0.8
    })
  ]
}
```

## Pros & Cons for Flask

### Pros
1. **Mature Flask Integration**: Many examples, established patterns
2. **Massive Ecosystem**: Plugin for everything (Babel, TypeScript, Sass, etc.)
3. **Granular Control**: Fine-tune every aspect of bundling
4. **Code Splitting**: Best-in-class chunk optimization
5. **Asset Management**: Handles fonts, images, all asset types
6. **Community Support**: Largest community, extensive Stack Overflow answers
7. **Production Battle-Tested**: Used by major applications worldwide
8. **Single Build Output**: Can skip dev server, just use watch mode
9. **Flask-Webpack Extension**: Third-party Flask extension available

### Cons
1. **Complex Configuration**: Verbose config, steep learning curve
2. **Slow Build Times**: Slower than Vite/esbuild (improving in v5)
3. **Large node_modules**: Heavy dependency tree
4. **Configuration Boilerplate**: Need many plugins for common tasks
5. **Webpack-Specific Knowledge**: Concepts like loaders, plugins require learning

## Flask Integration Complexity

**Score: MEDIUM-LOW**

**Why:**
- Well-documented Flask integration patterns
- Flask-Webpack extension available (optional)
- Can skip dev server complexity (use watch mode)
- Manifest plugin works seamlessly with Flask
- Established community practices

## Use Case Fit for QRCards

### Excellent Fit If:
- Need maximum control over build process
- Complex asset requirements (images, fonts, Sass)
- Large team familiar with Webpack
- Want extensive plugin ecosystem
- Need advanced optimization (lazy loading, prefetching)
- Prefer stability over bleeding-edge features

### Poor Fit If:
- Want fast build times (consider Vite/esbuild)
- Prefer minimal configuration (consider Parcel)
- Small project, simple bundling needs
- Team unfamiliar with Webpack concepts

## Migration Path

### Phase 1: Basic Setup
```bash
npm init -y
npm install -D webpack webpack-cli mini-css-extract-plugin
```

### Phase 2: Minimal Config
```javascript
// webpack.config.js - start simple
module.exports = {
  entry: './src/main.js',
  output: {
    path: path.resolve(__dirname, '../flasklayer/static/js'),
    filename: 'bundle.js'
  }
}
```

### Phase 3: Add Manifest + Flask Helper
```bash
npm install -D webpack-manifest-plugin
```

```python
# Add to Flask app init
from flasklayer.utils.webpack import init_webpack_helpers
init_webpack_helpers(app)
```

### Phase 4: Expand to Multi-Domain
Add more entry points as needed.

## Example: Calculator Widget

### Webpack Entry Structure
```
src/
├── domains/
│   └── calculators/
│       └── prod/
│           ├── main.js           # Entry point
│           ├── compound.js
│           ├── loan.js
│           └── styles.scss
└── shared/
    ├── api.js
    └── utils.js
```

### main.js (Entry Point)
```javascript
// Import styles
import './styles.scss'

// Import domain logic
import { initCompound } from './compound.js'
import { initLoan } from './loan.js'

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  initCompound()
  initLoan()
})
```

### Webpack Output
```
static/
├── manifest.json
├── js/
│   ├── vendor.a1b2c3.js          # node_modules
│   └── calculators-prod.d4e5f6.js
└── css/
    └── calculators-prod.g7h8i9.css
```

### Template Reference
```jinja2
{% extends "qr/base_qr.html" %}

{% block styles %}
{{ super() }}
<link rel="stylesheet" href="{{ url_for('static', filename=webpack_asset('css/calculators-prod.css')) }}">
{% endblock %}

{% block scripts %}
{{ super() }}
<script src="{{ url_for('static', filename=webpack_asset('js/vendor.js')) }}"></script>
<script src="{{ url_for('static', filename=webpack_asset('js/calculators-prod.js')) }}"></script>
{% endblock %}

{% block content %}
<!-- Calculator HTML here -->
{% endblock %}
```

## Flask-Webpack Extension

**Optional third-party integration:**

```bash
pip install flask-webpack
```

```python
# flasklayer/app.py
from flask_webpack import Webpack

webpack = Webpack()

def create_app():
    app = Flask(__name__)
    webpack.init_app(app)
    return app
```

```jinja2
{# Automatic asset resolution #}
{{ webpack['calculators-prod.js'] }}
{{ webpack['calculators-prod.css'] }}
```

## Recommendation

**RECOMMENDED for QRCards if:**
- Team has Webpack experience
- Need maximum control and flexibility
- Complex asset types (Sass, images, fonts)
- Large codebase, many domains
- Want proven, stable tooling

**Consider Alternatives if:**
- Build speed is priority (Vite, esbuild)
- Want simpler config (Parcel, esbuild)
- Small project, simple needs

## Additional Resources

- Webpack Docs: https://webpack.js.org
- Flask-Webpack: https://github.com/nickjj/flask-webpack
- Webpack Academy: https://webpack.academy
- Bundle Analysis: https://github.com/webpack-contrib/webpack-bundle-analyzer
