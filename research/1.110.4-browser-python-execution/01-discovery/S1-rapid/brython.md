# Brython - Browser Python Transpiler

## Popularity Metrics

- **GitHub Stars**: 6,458 (December 2025)
- **Repository**: brython-dev/brython
- **PyPI Downloads**: 1,133 weekly downloads
- **Maintenance Status**: ✅ Healthy (releases within last 3 months)
- **Popularity Classification**: "Recognized" (Snyk analysis)
- **Project Type**: Pure Python-to-JavaScript transpiler

## Quick Validation (5-Minute Test)

**Time to "Hello World"**: ~2 minutes

```html
<!DOCTYPE html>
<html>
  <head>
    <script src="https://cdn.jsdelivr.net/npm/brython@3/brython.min.js"></script>
  </head>
  <body onload="brython()">
    <script type="text/python">
      from browser import document, alert
      document <= "Hello World from Brython!"
    </script>
  </body>
</html>
```

**Result**: ✅ Works immediately, very lightweight

## Ecosystem Size

### Technical Foundation
- **Approach**: Python 3 implementation that transpiles to JavaScript
- **Runtime**: No WebAssembly, pure JavaScript execution
- **Bundle Size**: ~1-2MB (significantly smaller than WebAssembly solutions)
- **Startup Time**: Near-instant (no WASM loading)

### Package Compatibility
- ❌ No NumPy/Pandas/SciPy (can't run C extensions)
- ✅ Pure Python standard library
- ✅ Browser DOM manipulation via `browser` module
- ⚠️ Limited third-party package support
- ❌ Cannot run packages with native dependencies

### Performance Characteristics
- **Loop Performance**: 0.11 seconds (vs 7.71s for PyScript)
- **Startup**: Near-instant (no WASM initialization)
- **Execution**: JavaScript speed (faster than interpreted WASM for simple operations)

### Community Channels
- GitHub Issues: Active maintenance
- Google Groups discussion list
- Stack Overflow: Modest but present
- Documentation site: brython.info

## Production Adoption Patterns

### Use Cases in the Wild
1. **Interactive Web Forms**: Client-side validation in Python syntax
2. **Educational Sites**: Teaching Python without scientific computing
3. **DOM Manipulation**: Python syntax for web interactivity
4. **Lightweight Scripting**: Simple web page behaviors
5. **Python Syntax Preference**: Teams avoiding JavaScript

### Adoption Constraints
- Not suitable for data science web applications
- Cannot replace scientific computing workflows
- Best for simple scripting and DOM manipulation
- Appeals to developers who prefer Python syntax

## S1 Assessment

### Strengths
- ✅ Very lightweight (1-2MB vs 7-20MB for WebAssembly)
- ✅ Near-instant startup (no WASM initialization)
- ✅ Fast execution for simple operations (0.11s vs 7.71s loops)
- ✅ Active maintenance (releases within 3 months)
- ✅ Good for DOM manipulation use cases

### Limitations
- ❌ No scientific computing packages (NumPy/Pandas/SciPy)
- ❌ Limited third-party package ecosystem
- ❌ Cannot run code with C extensions
- ⚠️ Lower GitHub stars (6.4k vs 18.6k PyScript, 13.9k Pyodide)
- ⚠️ Smaller community than WebAssembly solutions

### "Just Works" Score: 7/10
Works immediately and very fast for simple use cases. Major deductions for missing scientific computing stack and limited package ecosystem. Only suitable for basic Python scripting.

## Validation Verdict

**CONDITIONAL PASS** - Brython passes S1 validation for lightweight Python scripting in browsers, but fails for data science and scientific computing applications.

✅ **Good for**: Simple web scripting, DOM manipulation, educational sites (basic Python), lightweight interactivity
❌ **Poor for**: Data science, scientific computing, any application requiring NumPy/Pandas, complex third-party packages

The low bundle size and fast performance are compelling for simple use cases, but the lack of scientific computing support disqualifies it for the majority of serious browser Python applications. This is a niche solution that excels in its specific domain but has clear limitations.
