# Pyodide - WebAssembly Python Runtime

## Popularity Metrics

- **GitHub Stars**: 13,900 (December 2025)
- **Repository**: pyodide/pyodide
- **Forks**: 982
- **Official Backing**: Independent community-driven project (originally Mozilla)
- **Latest Release**: 0.29.0 (October 2025)
- **NPM Package**: Available, actively maintained

## Quick Validation (5-Minute Test)

**Time to "Hello World"**: ~2 minutes

```html
<!DOCTYPE html>
<html>
  <head>
    <script src="https://cdn.jsdelivr.net/pyodide/v0.29.0/full/pyodide.js"></script>
  </head>
  <body>
    <script>
      async function main() {
        let pyodide = await loadPyodide();
        console.log(pyodide.runPython("print('Hello World')"));
      }
      main();
    </script>
  </body>
</html>
```

**Result**: ✅ Works immediately, no configuration required

## Ecosystem Size

### Package Compatibility
- **Scientific Stack**: ✅ NumPy, Pandas, SciPy, Matplotlib, scikit-learn
- **Pure Python Packages**: Install from PyPI via micropip
- **Pre-built Packages**: 200+ WASM-compiled packages included
- **C Extensions**: Supported through WebAssembly compilation

### Bundle Size Reality
- Core CPython + stdlib: ~7MB
- With NumPy/Pandas: ~17.5MB total
- Full distribution: 200+MB (optional packages)
- Loads in ~2 seconds on broadband

### Community Channels
- GitHub Discussions: Active, hundreds of threads
- Gitter chat: Daily activity
- Stack Overflow: 500+ questions tagged "pyodide"

## Production Adoption Patterns

### Use Cases in the Wild
1. **Educational Platforms**: Python tutorials and interactive learning
2. **Data Science Dashboards**: Client-side analytics without server costs
3. **Scientific Computing**: Browser-based data visualization tools
4. **Development Tools**: In-browser Python REPLs and code playgrounds
5. **Embedded Notebooks**: JupyterLite and other notebook environments

### Notable Deployments
- JupyterLite (serving 500k+ French students)
- Multiple online Python learning platforms
- Data science visualization tools
- Browser-based computational notebooks

## S1 Assessment

### Strengths
- ✅ Highest scientific computing compatibility (full NumPy/Pandas/SciPy)
- ✅ True CPython implementation (maximum Python compatibility)
- ✅ Strong community support and active development
- ✅ Production-proven at scale (JupyterLite case study)

### Limitations
- ⚠️ Large bundle size (7-20MB depending on packages)
- ⚠️ 2-3 second startup time
- ⚠️ Not all Python packages available (C extensions need compilation)

### "Just Works" Score: 9/10
Works immediately with CDN link. Scientific packages load seamlessly. Only deduction for initial download size.

## Validation Verdict

**PASS** - Pyodide is the gold standard for browser Python execution when you need full scientific computing capabilities. The large community, production adoption, and comprehensive package support make it the safe choice for most data science and educational web applications.
