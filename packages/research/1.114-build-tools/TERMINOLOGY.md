# Build Tools Terminology Guide

**Purpose**: Explain unfamiliar technical terms for business/non-technical stakeholders
**Audience**: CTOs, PMs, business leaders evaluating build tools
**Created**: 2025-12-01

---

## Core Concepts

### Bundler
**What it is**: A program that combines many JavaScript files into one (or a few) files.

**Why it matters**: Browsers download files one at a time. 1,000 small files = slow website. 1 bundled file = fast website.

**Analogy**: Packing 1,000 loose items into a suitcase instead of carrying each item separately.

**Example**: Your code has 500 JavaScript files. Bundler combines them into `bundle.js` (1 file).

---

### Module
**What it is**: A single JavaScript file that exports code for other files to use.

**Why it matters**: Modules let you organize code into reusable pieces instead of one giant file.

**Example**:
```javascript
// calculator.js (a module)
export function add(a, b) { return a + b; }

// app.js (uses the module)
import { add } from './calculator.js';
```

**Before modules**: All code in one 10,000-line file (unmaintainable).
**With modules**: 100 files × 100 lines each (organized, reusable).

---

### ES Modules (ESM)
**What it is**: Modern JavaScript module system using `import`/`export`.

**Why it matters**: Industry standard (2015+), works in browsers natively, enables tree shaking.

**Alternative**: CommonJS (`require()`/`module.exports`) - older Node.js style, doesn't work in browsers.

**Why "ES"**: ECMAScript (official JavaScript standard name).

---

### Transpilation
**What it is**: Converting code from one language to another (e.g., TypeScript → JavaScript).

**Why it matters**: Browsers only understand JavaScript. Developers want to write TypeScript, JSX, modern JS.

**Examples**:
- TypeScript → JavaScript (`type string` annotations removed)
- JSX → JavaScript (`<button>Click</button>` → `React.createElement('button', ...)`)
- ES2024 → ES2015 (modern syntax → older syntax for old browsers)

**Not compilation**: Compilation = high-level → machine code. Transpilation = language → language (same level).

---

## Performance Concepts

### Hot Module Replacement (HMR)
**What it is**: Update code in the browser WITHOUT full page reload.

**Why it matters**: Saves developer time. Change component → see instantly (form state preserved).

**Example workflow**:
- **Without HMR**: Edit button.js → Save → Refresh browser → Re-enter form → See change (10 seconds)
- **With HMR**: Edit button.js → Save → See change instantly (0.1 seconds)

**Speed comparison**:
- Vite HMR: <10ms (instant)
- Webpack HMR: 500ms - 5 seconds (noticeable lag)

**Business impact**: 100× faster iteration = ship features faster.

---

### Cold Start
**What it is**: Time from "run build command" to "first bundle ready" (first time, no cache).

**Why it matters**: Measures developer wait time after code checkout or cache clear.

**Benchmarks** (1,000 files):
- esbuild: 0.5 seconds
- Vite: 1.2 seconds
- Parcel: 8 seconds
- Webpack: 45 seconds

**When it matters**: Daily (morning code checkout), CI/CD pipelines (clean builds).

---

### Tree Shaking
**What it is**: Removing unused code from final bundle.

**Why it matters**: Smaller bundle = faster website loading = better user experience.

**Example**:
```javascript
// You import ONE function from a library with 100 functions
import { add } from 'math-library';  // Only need 'add'

// Tree shaking removes the other 99 unused functions from bundle
// Result: 10 KB bundle instead of 500 KB
```

**Savings**: 50-70% bundle size reduction typical.

**Best at it**: Rollup (best), Vite (uses Rollup), Webpack (good with config).

---

### Code Splitting
**What it is**: Breaking bundle into smaller chunks loaded on-demand.

**Why it matters**: Users only download code they need, not everything upfront.

**Example**:
- **Without splitting**: User loads 5 MB bundle (includes admin panel they never use)
- **With splitting**: User loads 500 KB (main app), admin panel loads only when accessed

**Types**:
- **Route-based**: `/calculator` route loads `calculator.js` chunk
- **Component-based**: Modal loads `modal.js` only when opened
- **Vendor**: Separate `react.js` from `your-app.js` (cache React separately)

**Business impact**: 10× faster initial page load.

---

### Minification
**What it is**: Removing whitespace, shortening variable names, removing comments.

**Why it matters**: Smaller file size = faster download = faster website.

**Example**:
```javascript
// Before minification (readable, 150 characters)
function calculateTotal(price, tax) {
  const total = price + (price * tax);
  return total;
}

// After minification (unreadable, 50 characters)
function c(a,b){return a+a*b}
```

**Savings**: 40-60% file size reduction.

**All bundlers do this**: Automatic in production mode.

---

### Bundle Size
**What it is**: Total kilobytes (KB) of JavaScript/CSS downloaded by browser.

**Why it matters**: Bigger bundle = slower website (especially mobile).

**Targets**:
- **Good**: <200 KB total
- **Acceptable**: 200-500 KB
- **Slow**: >500 KB (users notice lag)

**Optimization tactics**:
- Tree shaking (remove unused code)
- Code splitting (load on-demand)
- Minification (compress code)
- Compression (gzip/brotli)

**Typical reduction**: 2 MB unoptimized → 300 KB optimized.

---

## Development Concepts

### Dev Server
**What it is**: Local web server for development (http://localhost:3000).

**Why it matters**: Lets you view website on your computer before deploying.

**Features**:
- **Hot reload**: Auto-refresh on code changes
- **HMR**: Update without refresh (faster)
- **Proxy**: Forward API calls to backend (Flask, Django)

**Example**: Edit calculator.js → Dev server auto-updates → See change instantly.

---

### Build Time
**What it is**: How long the bundler takes to create production files.

**Why it matters**: Faster builds = faster CI/CD = faster deployments.

**Benchmarks** (production build, 1,000 files):
- esbuild: 2 seconds (fastest, but larger bundles)
- Vite: 15 seconds (balanced)
- Webpack: 60 seconds (slowest, but most optimized)

**When it matters**: Every deployment, every CI/CD run.

---

### Source Maps
**What it is**: Files that map minified code back to original code.

**Why it matters**: Debug production errors (see original code, not minified mess).

**Example**:
- **Error without source map**: "Error in bundle.js line 1 character 45632" (useless)
- **Error with source map**: "Error in calculator.js line 42" (useful)

**All bundlers generate these**: Enabled by default in development.

---

## Architecture Concepts

### Single Page Application (SPA)
**What it is**: Website that loads once, then updates content dynamically (no page refreshes).

**Examples**: Gmail, Facebook, Twitter

**Bundler need**: One main bundle, code splitting for routes.

**Pattern**: `index.html` + `app.js` (all content rendered by JavaScript)

---

### Multi-Page Application (MPA)
**What it is**: Traditional website with multiple HTML pages (page refreshes on navigation).

**Examples**: Blogs, marketing sites, documentation

**Bundler need**: Multiple entry points (one per page), shared chunk extraction.

**Pattern**: `home.html` + `home.js`, `about.html` + `about.js`, `shared.js`

---

### Backend Template Integration
**What it is**: Using bundler with server-side frameworks (Flask, Django, Rails).

**Why it matters**: Combine server-rendered HTML with bundled JavaScript/CSS.

**Pattern**:
1. Bundler outputs to Flask static folder
2. Flask template includes: `<script src="/static/bundle.js">`
3. JavaScript enhances server-rendered HTML (forms, widgets)

**QRCards uses this**: Flask templates + bundled calculator widgets.

---

## Ecosystem Concepts

### Plugin
**What it is**: Add-on that extends bundler functionality.

**Why it matters**: Plugins add features (CSS processing, image optimization, manifest generation).

**Examples**:
- `vite-plugin-flask`: Generate manifest.json for Flask
- `webpack-bundle-analyzer`: Visualize bundle size
- `rollup-plugin-typescript`: Add TypeScript support

**Ecosystem size**:
- Webpack: 5,000+ plugins (most mature)
- Vite: 500+ plugins (growing fast)
- Rollup: 300+ plugins

---

### Framework
**What it is**: Library for building UIs (React, Vue, Svelte).

**Why it matters**: Bundler must support framework syntax (JSX, .vue files, .svelte files).

**Framework defaults**:
- React: Vite (via `create-vite`) or Webpack (legacy)
- Vue: Vite (official)
- Svelte: Vite (via SvelteKit)
- Angular: Webpack (official)

**Bundler choice often follows framework recommendation.**

---

### Ecosystem Maturity
**What it is**: How long tool has existed, community size, plugin availability.

**Why it matters**: Mature tools have more solutions to problems (Stack Overflow answers, plugins).

**Maturity ranking**:
- Webpack: 12 years, very mature (most Stack Overflow answers)
- Rollup: 9 years, mature (library-focused)
- Vite: 4 years, maturing rapidly (fastest growing)
- Turbopack: 2 years, immature (alpha, Next.js only)

**Trade-off**: Mature = more resources, newer = better DX.

---

## Configuration Concepts

### Zero-Config
**What it is**: Tool works without configuration file (sensible defaults).

**Why it matters**: Faster setup, less maintenance.

**Examples**:
- Parcel: True zero-config (just point at HTML)
- Vite: Near zero-config (30 lines for complex setups)
- Webpack: Not zero-config (100+ lines typical)

**Trade-off**: Zero-config = less control. Full config = more power.

---

### Config File
**What it is**: JavaScript file defining bundler behavior (entry points, output, plugins).

**Why it matters**: Customizes bundler for your architecture.

**Examples**:
- Vite: `vite.config.js` (~30 lines for multidomain)
- Webpack: `webpack.config.js` (~150 lines for multidomain)

**Complexity drivers**:
- Multidomain: +50 lines (entry points)
- Backend integration: +30 lines (output paths, manifest)
- Custom loaders: +20 lines each

---

### Entry Point
**What it is**: Starting file for bundler (usually `main.js` or `index.js`).

**Why it matters**: Bundler starts here, follows imports, bundles everything reachable.

**Example**:
```javascript
// vite.config.js
input: {
  'app': './src/app.js',        // Entry 1
  'admin': './src/admin.js'     // Entry 2
}
// Result: app.js bundle + admin.js bundle
```

**Multidomain**: One entry per domain (QRCards has 5 entries).

---

## Output Concepts

### Output Directory
**What it is**: Folder where bundler writes final files.

**Why it matters**: Must match backend static folder (Flask, Django).

**Examples**:
- Vite: `dist/` (default)
- QRCards: `packages/flasklayer/flasklayer/static/dist/` (Flask static folder)

**Configuration**:
```javascript
build: {
  outDir: '../backend/static/dist'
}
```

---

### Manifest File
**What it is**: JSON file mapping original filenames to hashed filenames.

**Why it matters**: Production bundles have hashes (`app.abc123.js`). Manifest tells backend which file to load.

**Example**:
```json
{
  "app.js": "app.abc123.js",
  "admin.js": "admin.def456.js"
}
```

**Backend usage**:
```python
# Flask reads manifest, includes correct hashed filename
manifest = json.load(open('manifest.json'))
script_url = manifest['app.js']  # Returns 'app.abc123.js'
```

---

### Hashed Filenames
**What it is**: Filenames with content hash (`app.abc123.js` instead of `app.js`).

**Why it matters**: Cache busting. Browser caches `app.abc123.js`. New code = new hash (`app.def456.js`) = browser downloads new version.

**Without hashing**: Browser caches `app.js` → Deploys break (old code cached).
**With hashing**: Each deploy = new hash = browser downloads fresh code.

**All bundlers do this**: Automatic in production mode.

---

## Performance Metrics

### Time to Interactive (TTI)
**What it is**: How long until user can interact with page.

**Why it matters**: Users abandon slow sites (>3 seconds = 50% bounce rate).

**Improved by**:
- Smaller bundles (tree shaking, minification)
- Code splitting (load less upfront)
- Fast bundler (less build time in CI/CD)

**Typical improvement**: 5 seconds → 1.5 seconds (optimize bundle).

---

### First Contentful Paint (FCP)
**What it is**: When first pixel renders on screen.

**Why it matters**: Users perceive fast = good. Slow FCP = users leave.

**Improved by**:
- Smaller bundles
- Defer non-critical JavaScript
- Inline critical CSS

**Not bundler-specific**: Bundler enables optimization (code splitting), but FCP depends on loading strategy too.

---

## Technology Terms

### WebAssembly (WASM)
**What it is**: Binary format for running code in browser (faster than JavaScript).

**Why it matters**: Bundlers written in Rust/Go (esbuild, Turbopack) compile to WASM = 10-100× faster.

**Examples**:
- esbuild: Written in Go, 70× faster than JavaScript bundlers
- Turbopack: Written in Rust, 700× faster claim (unverified)

**Future**: More bundlers will use WASM (speed advantage too big).

---

### Native ESM
**What it is**: Browsers loading ES modules directly (no bundling in dev).

**Why it matters**: Vite's secret - dev server doesn't bundle, serves modules directly = instant HMR.

**Example**:
- **Webpack dev**: Bundle 1,000 files on startup (30 seconds)
- **Vite dev**: Serve files on-demand (0 seconds startup)

**Production still bundles**: Native ESM only for development speed.

---

### TypeScript
**What it is**: JavaScript with type annotations (`string`, `number`, etc.).

**Why it matters**: Catches errors before runtime, better autocomplete.

**Bundler support**:
- Vite: Built-in (zero config)
- Webpack: Requires `ts-loader` plugin
- esbuild: Built-in (but doesn't type-check)

**Not required**: You can use plain JavaScript with any bundler.

---

### JSX
**What it is**: HTML-like syntax in JavaScript (React uses this).

**Example**:
```jsx
const button = <button onClick={handleClick}>Click me</button>;
```

**Why it matters**: React code won't run without JSX → JavaScript transpilation.

**Bundler support**:
- All bundlers support JSX (Vite, Webpack, Rollup, Parcel)
- Automatic detection (sees `.jsx` file extension)

---

## Glossary Quick Reference

| Term | One-Sentence Definition |
|------|------------------------|
| **Bundler** | Combines many JavaScript files into one file |
| **Module** | Single JavaScript file that exports code |
| **ESM** | Modern `import`/`export` syntax |
| **Transpilation** | Converting TypeScript/JSX to JavaScript |
| **HMR** | Update code without page refresh |
| **Cold Start** | Time from command to first bundle |
| **Tree Shaking** | Removing unused code from bundle |
| **Code Splitting** | Breaking bundle into on-demand chunks |
| **Minification** | Removing whitespace, shortening variables |
| **Bundle Size** | Total KB of JavaScript downloaded |
| **Dev Server** | Local server for development |
| **Source Maps** | Map minified code to original code |
| **SPA** | Single page, no refreshes (Gmail-style) |
| **MPA** | Multiple pages, refreshes (blog-style) |
| **Plugin** | Add-on extending bundler features |
| **Zero-Config** | Works without configuration file |
| **Entry Point** | Starting file for bundler |
| **Manifest** | Maps filenames to hashed filenames |
| **WASM** | Binary format (Rust/Go bundlers use this) |
| **Native ESM** | Browser loading modules directly |

---

**Last Updated**: 2025-12-01
**Audience**: Business stakeholders, CTOs, non-technical decision makers
**Purpose**: Demystify build tool terminology for informed decisions
