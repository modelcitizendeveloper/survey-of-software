# PyScript - HTML-First Python Framework

## Popularity Metrics

- **GitHub Stars**: 18,600 (December 2025)
- **Repository**: pyscript/pyscript
- **Forks**: 1,500
- **Official Backing**: ✅ Anaconda Inc (core contributors employed by Anaconda)
- **Launch Impact**: 15,000+ stars at launch, 2,500% growth in search interest
- **Latest Releases**: Multiple 2025 releases (2025.2.4, 2025.8.1)
- **Active Development**: Regular releases throughout 2025

## Quick Validation (5-Minute Test)

**Time to "Hello World"**: ~4 minutes

```html
<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="https://pyscript.net/releases/2025.8.1/core.css">
    <script type="module" src="https://pyscript.net/releases/2025.8.1/core.js"></script>
  </head>
  <body>
    <py-script>
      print("Hello World")
      display("Hello from PyScript!")
    </py-script>
  </body>
</html>
```

**Result**: ✅ Works with custom HTML tags

## Ecosystem Size

### Technical Foundation
- **Runtime Engine**: Built on Pyodide (WebAssembly Python)
- **Framework Type**: HTML-first, declarative Python in HTML
- **Package Support**: Inherits Pyodide ecosystem
- **Philosophy**: Make Python feel native to web development

### Bundle Size & Performance
- **Initial Download**: 18.5MB for Hello World (9MB wasm, 5MB data, 1.9MB JS, 1.15MB pyscript)
- **Compressed**: 8.7MB compressed, 22.7MB uncompressed
- **Startup Time**: ~3 seconds average
- **Load Performance**: Pyodide averages 2s, PyScript adds ~1s overhead

### Community Channels
- Official Anaconda Forum for PyScript
- Active Discord community
- Tutorial repositories (anaconda/pyscript-tutorial)
- Stack Overflow questions growing

## Production Adoption Patterns

### Launch Platform
- **PyScript.com**: Anaconda launched dedicated platform
- "Democratizes Python for All" positioning
- Web-native Python development focus

### Use Cases in the Wild
1. **Educational Content**: Interactive Python tutorials in HTML
2. **Data Science Demos**: Embedded analytics in marketing sites
3. **Corporate Intranets**: Internal tools with Python logic
4. **Prototyping**: Rapid Python-in-web prototypes
5. **Python-First Teams**: Web apps for Python developers

### Target Audience
- Python developers who want to build web apps
- Data scientists creating web-based visualizations
- Educators embedding interactive Python examples
- Teams preferring Python over JavaScript

## S1 Assessment

### Strengths
- ✅ Highest GitHub stars (18.6k) - most popular by this metric
- ✅ Strong corporate backing (Anaconda)
- ✅ HTML-first approach familiar to web developers
- ✅ Built on proven Pyodide runtime
- ✅ Active development with frequent releases

### Limitations
- ⚠️ Largest bundle size (18.5MB uncompressed for Hello World)
- ⚠️ Slower startup (3 seconds vs 2 for Pyodide)
- ⚠️ Performance concerns for public web apps (7.71s for loops vs 0.11s Brython)
- ⚠️ Opinionated framework (HTML-first may not fit all use cases)
- ⚠️ Framework overhead on top of Pyodide

### "Just Works" Score: 7/10
Works immediately with CDN link and custom HTML tags. Deductions for large bundle size, slower performance, and framework overhead making it unsuitable for performance-sensitive public web applications.

## Validation Verdict

**CONDITIONAL PASS** - PyScript has the highest GitHub stars and strong Anaconda backing, but the S1 quick validation reveals significant performance concerns. The 18.5MB bundle and 3-second startup make it problematic for public web apps. However, it excels in specific scenarios:

✅ **Good for**: Corporate intranets, educational platforms, internal tools, Python-first teams
❌ **Poor for**: Public web apps with performance expectations, mobile users, bandwidth-constrained environments

The high star count validates developer interest, but practical testing suggests this is more a "Python for web developers" tool than a general-purpose browser Python solution.
