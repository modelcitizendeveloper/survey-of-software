# Use Case: Multi-Page Application (MPA)

**Use Case ID**: UC-MPA-01
**Date**: 2025-12-01
**Methodology**: S3 Need-Driven Discovery

---

## Use Case Definition

**Project Type**: Multi-page application with multiple HTML entry points

**Characteristics**:
- Multiple independent HTML pages (`about.html`, `contact.html`, `calculator.html`)
- Each page has its own JavaScript entry point
- Shared components/utilities across pages
- Traditional navigation (full page loads between pages)
- Some pages may have complex JavaScript, others minimal

**Example Applications**:
- Marketing website with interactive features
- Documentation site with embedded demos
- Corporate website with calculator/tools pages
- Educational platform with multiple standalone modules

**Key Difference from SPA**: Each page is independent, but they share code (components, utilities, styles).

---

## Requirements Specification

### Primary Requirements (Must-Have)

**P1. Multiple Entry Points**
- Success Criteria: Build multiple HTML pages independently
- Justification: Each page is a separate entry point
- Deal-Breaker: Cannot configure multiple pages = tool doesn't fit

**P2. Shared Code Extraction**
- Success Criteria: Common code shared across pages (not duplicated)
- Justification: Avoid shipping same React library 5 times
- Deal-Breaker: Code duplication wastes bandwidth

**P3. Independent Page Bundles**
- Success Criteria: `about.html` only loads its JavaScript, not calculator's
- Justification: Each page should be lightweight
- Deal-Breaker: Monolithic bundle loaded on every page

**P4. Fast Rebuild Per Page**
- Success Criteria: Editing one page rebuilds only that page
- Justification: Development efficiency
- Deal-Breaker: Full rebuild on every change kills productivity

**P5. Production Optimization**
- Success Criteria: Minification, tree shaking, asset hashing
- Justification: Standard production requirements
- Deal-Breaker: Unoptimized bundles unacceptable

### Secondary Requirements (Nice-to-Have)

**S1. Zero Configuration MPA Support**
- Target: Tool automatically detects multiple HTML files
- Value: Less setup friction

**S2. Shared Chunk Optimization**
- Target: Automatically extract common chunks (vendor, shared utilities)
- Value: Optimal cache usage across pages

**S3. Per-Page Code Splitting**
- Target: Each page can lazy-load its own components
- Value: Further performance optimization

**S4. Development Server**
- Target: HMR works across all pages
- Value: Good developer experience

**S5. Asset Management**
- Target: Images/fonts shared across pages handled efficiently
- Value: Avoid asset duplication

---

## Tool Evaluation

### Vite

**Primary Requirements**:
- P1 (Multiple Entries): ✅ **PASS** - Native MPA support via `build.rollupOptions.input`
- P2 (Shared Code): ✅ **PASS** - Automatic chunk splitting
- P3 (Independent Bundles): ✅ **PASS** - Each page gets its own bundle
- P4 (Fast Rebuild): ✅ **PASS** - Only changed page rebuilds
- P5 (Optimization): ✅ **PASS** - Full Rollup optimization

**Secondary Requirements**:
- S1 (Zero Config): ⚠️ Partial - Need to list HTML files in config
- S2 (Shared Chunks): ✅ Automatic via Rollup
- S3 (Per-Page Split): ✅ Dynamic imports work
- S4 (Dev Server): ✅ Excellent HMR
- S5 (Assets): ✅ Shared assets handled well

**Configuration Example**:
```javascript
// vite.config.js (30 lines)
export default {
  build: {
    rollupOptions: {
      input: {
        main: 'index.html',
        about: 'about.html',
        calculator: 'calculator.html'
      }
    }
  }
}
```

**Gap Analysis**: Minimal config needed (~30 lines). Not truly "zero-config" but close.

---

### Webpack 5

**Primary Requirements**:
- P1 (Multiple Entries): ✅ **PASS** - Multiple entry points well-supported
- P2 (Shared Code): ✅ **PASS** - SplitChunksPlugin (mature)
- P3 (Independent Bundles): ✅ **PASS** - Per-page bundles
- P4 (Fast Rebuild): ⚠️ **CONDITIONAL** - Slow (30s-2min) but works
- P5 (Optimization): ✅ **PASS** - Full optimization suite

**Secondary Requirements**:
- S1 (Zero Config): ❌ Heavy config required
- S2 (Shared Chunks): ✅ SplitChunksPlugin (best in class)
- S3 (Per-Page Split): ✅ Dynamic imports
- S4 (Dev Server): ⚠️ HMR slow
- S5 (Assets): ✅ Excellent asset handling

**Configuration Example**:
```javascript
// webpack.config.js (150-200 lines)
module.exports = {
  entry: {
    main: './src/main.js',
    about: './src/about.js',
    calculator: './src/calculator.js'
  },
  output: { /* ... */ },
  optimization: {
    splitChunks: { /* 30 lines of config */ }
  },
  plugins: [
    new HtmlWebpackPlugin({ /* config per page */ }),
    new HtmlWebpackPlugin({ /* config per page */ }),
    new HtmlWebpackPlugin({ /* config per page */ })
  ]
}
```

**Gap Analysis**: Works perfectly but requires extensive configuration (150-200 lines). Rebuild speed is painful.

---

### esbuild

**Primary Requirements**:
- P1 (Multiple Entries): ✅ **PASS** - Multiple entry points supported
- P2 (Shared Code): ⚠️ **LIMITED** - Manual configuration needed
- P3 (Independent Bundles): ✅ **PASS** - Separate bundles per entry
- P4 (Fast Rebuild): ✅ **PASS** - Extremely fast (<1s)
- P5 (Optimization): ⚠️ **LIMITED** - Basic minification, weak tree shaking

**Secondary Requirements**:
- S1 (Zero Config): ❌ Manual setup
- S2 (Shared Chunks): ❌ No automatic chunk splitting
- S3 (Per-Page Split): ⚠️ Limited code splitting
- S4 (Dev Server): ❌ No built-in dev server
- S5 (Assets): ⚠️ Basic

**Configuration Needed**: 50-100 lines + custom dev server

**Gap Analysis**: **PRIMARY REQUIREMENT FAILING** - Shared code extraction is manual and limited. No automatic common chunk optimization. Fast but missing critical MPA features.

---

### Rollup

**Primary Requirements**:
- P1 (Multiple Entries): ✅ **PASS** - Multiple inputs supported
- P2 (Shared Code): ⚠️ **LIMITED** - Manual chunk configuration
- P3 (Independent Bundles): ✅ **PASS** - Per-entry bundles
- P4 (Fast Rebuild): ❌ **FAIL** - No dev server (manual watch mode)
- P5 (Optimization): ✅ **PASS** - Excellent tree shaking

**Secondary Requirements**:
- S1 (Zero Config): ❌ Manual config
- S2 (Shared Chunks): ⚠️ Manual `manualChunks` config
- S3 (Per-Page Split): ✅ Dynamic imports
- S4 (Dev Server): ❌ No built-in server
- S5 (Assets): ⚠️ Via plugins

**Configuration Needed**: 100+ lines + separate dev server solution

**Gap Analysis**: **DISQUALIFIED** - No dev server makes development painful. Need to add rollup-plugin-serve + watch mode + manual reload.

---

### Parcel

**Primary Requirements**:
- P1 (Multiple Entries): ✅ **PASS** - Auto-detects HTML files
- P2 (Shared Code): ✅ **PASS** - Automatic chunk splitting
- P3 (Independent Bundles): ✅ **PASS** - Per-page bundles
- P4 (Fast Rebuild): ✅ **PASS** - Fast incremental builds
- P5 (Optimization): ✅ **PASS** - Full optimization

**Secondary Requirements**:
- S1 (Zero Config): ✅ **BEST** - Truly zero config (just point at HTML files)
- S2 (Shared Chunks): ✅ Automatic
- S3 (Per-Page Split): ✅ Dynamic imports
- S4 (Dev Server): ✅ Good HMR
- S5 (Assets): ✅ Automatic

**Configuration Needed**: 0 lines (truly zero-config)

**Usage**:
```bash
# Just point at HTML files, Parcel figures it out
parcel src/*.html
```

**Gap Analysis**: No gaps. Parcel designed for this exact use case.

---

### Turbopack

**Primary Requirements**:
- P1 (Multiple Entries): ⚠️ **UNCLEAR** - Next.js-specific (pages router)
- P2 (Shared Code): ⚠️ **UNCLEAR** - Next.js handles this
- P3 (Independent Bundles): ⚠️ **UNCLEAR** - Next.js architecture
- P4 (Fast Rebuild): ✅ **PASS** - Very fast
- P5 (Optimization): ⚠️ **UNCLEAR** - Limited documentation

**Gap Analysis**: **DISQUALIFIED** - Not a general-purpose tool. Tied to Next.js.

---

## Requirement Coverage Matrix

| Tool | P1 (Entries) | P2 (Shared) | P3 (Independent) | P4 (Rebuild) | P5 (Optimization) | Primary Score | Config Lines |
|------|--------------|-------------|------------------|--------------|-------------------|---------------|--------------|
| **Vite** | ✅ | ✅ | ✅ | ✅ | ✅ | **5/5** | ~30 |
| **Parcel** | ✅ | ✅ | ✅ | ✅ | ✅ | **5/5** | **0** |
| **Webpack 5** | ✅ | ✅ | ✅ | ⚠️ | ✅ | **4/5** | 150-200 |
| **esbuild** | ✅ | ⚠️ | ✅ | ✅ | ⚠️ | **3/5** | 50-100 |
| **Rollup** | ✅ | ⚠️ | ✅ | ❌ | ✅ | **DISQUALIFIED** | 100+ |
| **Turbopack** | ⚠️ | ⚠️ | ⚠️ | ✅ | ⚠️ | **DISQUALIFIED** | N/A |

---

## Best Fit Recommendation

**Winner: Parcel**

**Justification**:
1. **Perfect primary requirement coverage** (5/5)
2. **Zero configuration** - Just point at HTML files
3. **Automatic shared chunk optimization** - No manual config
4. **Fast development** - Good HMR, fast rebuilds
5. **Production optimized** - Minification, tree shaking automatic

**Strong Alternative: Vite**
- Choose if you need faster HMR (Vite: 10ms vs Parcel: 100ms)
- Minor config required (~30 lines to list HTML files)
- Better tree shaking (Rollup-based)
- Trade-off: Configuration vs speed

**Why Not Webpack?**
- 150-200 lines of configuration is excessive for MPA
- Slow rebuilds (30s-2min) hurt development
- Use only if maintaining existing Webpack setup

**Why Not esbuild?**
- Shared code extraction is manual and limited
- No automatic common chunk optimization
- Missing critical MPA features

---

## Configuration Comparison

### Parcel (Winner)
```bash
# package.json scripts
{
  "dev": "parcel src/*.html",
  "build": "parcel build src/*.html"
}
```
**Total config**: 0 lines

### Vite (Strong Alternative)
```javascript
// vite.config.js
export default {
  build: {
    rollupOptions: {
      input: {
        main: 'index.html',
        about: 'about.html',
        calculator: 'calculator.html'
      }
    }
  }
}
```
**Total config**: ~30 lines

### Webpack 5
```javascript
// webpack.config.js
module.exports = {
  entry: { /* ... */ },
  output: { /* ... */ },
  optimization: {
    splitChunks: { /* 30 lines */ }
  },
  plugins: [
    new HtmlWebpackPlugin({ /* page 1 */ }),
    new HtmlWebpackPlugin({ /* page 2 */ }),
    new HtmlWebpackPlugin({ /* page 3 */ })
  ],
  module: { /* loaders */ }
}
```
**Total config**: 150-200 lines

---

## Confidence Level

**HIGH CONFIDENCE**

**Reasoning**:
- Parcel and Vite both designed for MPA use case
- All primary requirements met by both tools
- Parcel has edge on zero-config
- Vite has edge on performance

**Decision Factor**:
- Choose **Parcel** if minimizing setup is priority
- Choose **Vite** if maximum speed is priority

**Risk Factors**:
- Parcel ecosystem smaller than Vite (if custom plugins needed, Vite better)
- For very large MPAs (>50 pages), test both for performance

**Validation Sources**:
- Parcel MPA documentation (https://parceljs.org/features/targets/)
- Vite multi-page guide (https://vitejs.dev/guide/build.html#multi-page-app)
