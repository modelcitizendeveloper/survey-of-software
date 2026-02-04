# PyScript - Python Framework for the Browser

## Overview

PyScript is an open-source framework developed by Anaconda that enables Python execution in web browsers through HTML. It provides a high-level abstraction over Pyodide and MicroPython, making browser-based Python more accessible to developers.

**Website:** https://pyscript.net/
**Repository:** https://github.com/pyscript/pyscript
**Documentation:** https://docs.pyscript.net/
**License:** Apache License 2.0

## Architecture

### Execution Model
- **Dual Backend Support:** Pyodide (CPython) or MicroPython
- **Python Version:** 3.11.x (Pyodide) or 3.4 (MicroPython)
- **HTML Integration:** Python code embedded in HTML via custom tags
- **Framework Layer:** Abstracts runtime complexity

### Technical Implementation
- Custom HTML elements (`<py-script>`, `<py-repl>`)
- Automatic runtime initialization
- Bidirectional Python-JavaScript FFI
- Web Workers for background execution
- Plugin architecture for extensibility

### Runtime Options

**Pyodide Backend:**
- Full CPython compatibility
- Complete scientific stack
- Larger bundle size (~6-8 MB)
- 2-5 second startup time

**MicroPython Backend:**
- Lightweight implementation
- Fast startup (<1 second)
- Smaller bundle (~200-400 KB)
- Limited package ecosystem
- Optimized for mobile devices

## Performance Analysis

### Startup Time

**Pyodide Mode:**
- **Initial Load:** 3-6 seconds (runtime + framework)
- **Subsequent Loads:** 1-2 seconds (cached)
- **Bundle Size:** 8-12 MB total

**MicroPython Mode:**
- **Initial Load:** <1 second
- **Subsequent Loads:** Near-instant
- **Bundle Size:** ~500 KB-1 MB

### Execution Speed

**Pyodide Backend:**
- Same performance as native Pyodide (1x-16x slower than native Python)
- Scientific computations leverage NumPy (near-native speed)
- Framework overhead minimal (<5%)

**MicroPython Backend:**
- Faster startup but slower execution for compute-intensive tasks
- No NumPy/Pandas support
- Suitable for UI interactions and simple logic

### Memory Usage
- **Pyodide:** 30-50 MB base + packages
- **MicroPython:** 5-15 MB base
- **Framework Overhead:** 2-5 MB
- Browser memory limits apply

### Bundle Size Trade-offs
- Pyodide: Full features, large download
- MicroPython: Fast loading, limited capabilities
- Choice depends on use case requirements

## Package Ecosystem

### Pyodide Backend Packages

**Scientific Stack:**
- NumPy - Array computing
- Pandas - Data analysis
- Matplotlib - Plotting
- SciPy - Scientific algorithms
- scikit-learn - Machine learning

**Package Installation:**
```html
<py-config>
  packages = ["numpy", "pandas", "matplotlib"]
</py-config>
```

**Available Packages:**
- All Pyodide-compatible packages (100+)
- Pure Python wheels from PyPI
- micropip for runtime installation

### MicroPython Backend Packages

**Limited Ecosystem:**
- No NumPy, Pandas, or Matplotlib
- Standard library subset
- Pure Python packages only (limited)
- Focus on lightweight operations

**Use Cases:**
- UI interactions
- Simple calculations
- Mobile-optimized apps
- Fast-loading demos

## Security Model

### Sandboxing Mechanisms
- **WebAssembly Isolation:** Pyodide backend security
- **Browser Sandbox:** All code runs client-side
- **No Server Access:** Fully browser-contained
- **Storage Isolation:** Per-origin limits

### Code Execution Safety
- User code executes in isolated environment
- No access to host system
- Suitable for untrusted code (educational platforms)
- WebAssembly fault isolation

### Resource Limits
- Browser memory constraints
- CPU throttling by browser
- Network subject to CORS
- Storage quotas (localStorage, IndexedDB)

### Security Considerations
- Safe for public websites
- User data remains in browser
- Privacy-preserving execution
- Crypto-mining risk (computational code)

## Integration Patterns

### HTML Embedding
```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://pyscript.net/releases/2024.3.2/core.css">
  <script type="module" src="https://pyscript.net/releases/2024.3.2/core.js"></script>
</head>
<body>
  <py-script>
    print("Hello from PyScript!")
    import numpy as np
    data = np.array([1, 2, 3, 4, 5])
    print(f"Mean: {data.mean()}")
  </py-script>
</body>
</html>
```

### Interactive REPL
```html
<py-repl>
  # Users can type Python code here
</py-repl>
```

### JavaScript Interoperability
```python
# Access JavaScript from Python
from pyscript import document, window
document.querySelector("#myDiv").innerText = "Updated from Python"

# Call JavaScript functions
window.alert("Hello from Python")
```

```javascript
// Access Python from JavaScript
const result = await pyscript.interpreter.run("2 + 2");
```

### Web Workers
```html
<py-script worker>
  # Runs in background thread
  import time
  for i in range(100):
    time.sleep(0.1)
    # Heavy computation
</py-script>
```

## Browser Compatibility

### Desktop Browsers
- **Chrome/Edge:** Full support (v90+)
- **Firefox:** Full support (v89+)
- **Safari:** Full support (v15+)
- **Opera:** Full support (v76+)

### Mobile Browsers

**Pyodide Mode:**
- iOS Safari: Functional but slow (JIT limitations)
- Android Chrome: Works, performance varies

**MicroPython Mode:**
- iOS Safari: Good performance
- Android Chrome: Excellent performance
- Optimized for mobile constraints

### WebAssembly Requirements
- Pyodide requires Wasm 1.0
- MicroPython requires basic JavaScript support
- Modern browser recommended

## Use Cases

### Optimal For (Pyodide)
- Data science web applications
- Interactive data visualizations
- Educational Python platforms
- Scientific computing dashboards
- Code documentation with runnable examples

### Optimal For (MicroPython)
- Mobile web applications
- Fast-loading demos and tutorials
- UI-focused web apps
- Progressive Web Apps
- Interactive forms and calculators

### Not Ideal For
- Production backend systems
- Real-time performance-critical apps
- Very large dataset processing
- Legacy Python 2.x applications

## Advantages

1. **Easy Integration** - HTML-first approach, minimal JavaScript
2. **Dual Runtime** - Choose Pyodide (features) or MicroPython (speed)
3. **Bidirectional FFI** - Seamless Python-JavaScript interaction
4. **Web Workers** - Background execution support
5. **Active Development** - Regular updates from Anaconda
6. **Educational Focus** - Designed for learning and teaching
7. **Mobile Support** - MicroPython optimized for mobile
8. **Plugin System** - Extensible architecture

## Limitations

1. **Pyodide Load Time** - 3-6 seconds with full runtime
2. **Bundle Size** - Large download for Pyodide mode
3. **Limited MicroPython Ecosystem** - No scientific packages
4. **Performance Overhead** - Framework layer adds slight cost
5. **Beta Status** - Still evolving (as of 2024)
6. **Documentation Gaps** - Some advanced features under-documented
7. **Browser Memory** - Subject to browser constraints

## PyScript vs Direct Pyodide

### Advantages Over Pyodide
- Simpler HTML-based API
- Less JavaScript boilerplate
- Built-in REPL component
- Plugin architecture
- MicroPython option for mobile

### When to Use Pyodide Directly
- Need fine-grained control
- Custom loading strategies
- Minimal framework overhead
- Advanced WebAssembly optimizations

## Technical Maturity

- **Stability:** Beta/Production-ready (v2024.3+ in 2024)
- **Community:** Growing community, Anaconda support
- **Documentation:** Improving, some gaps remain
- **Maintenance:** Active development by Anaconda team
- **Adoption:** Used in education, prototyping, interactive docs

## Framework Features

### Configuration System
```html
<py-config>
  packages = ["numpy", "pandas"]
  [[runtimes]]
  src = "https://cdn.jsdelivr.net/pyodide/v0.24.0/full/pyodide.js"
  name = "pyodide-0.24.0"
  lang = "python"
</py-config>
```

### Plugin Architecture
- Custom element extensions
- Runtime plugins
- Theme customization
- Event hooks

### Developer Experience
- Error handling and display
- Console output formatting
- Interactive debugging
- Development mode features

## Deployment Strategies

### Static Hosting
- Deploy as static HTML pages
- CDN for PyScript framework
- GitHub Pages, Netlify, Vercel
- No server infrastructure needed

### Content Delivery
- Use PyScript CDN for framework
- Self-host for air-gapped environments
- Version pinning for stability
- Subresource Integrity (SRI) support

### Performance Optimization
- Choose MicroPython for fast loading
- Lazy-load packages
- Cache aggressively
- Service Worker for offline

## Future Roadmap

- Improved startup performance
- Better MicroPython package ecosystem
- Enhanced developer tools
- More built-in components
- Better mobile optimization
- Collaboration features
- TypeScript support for Python
