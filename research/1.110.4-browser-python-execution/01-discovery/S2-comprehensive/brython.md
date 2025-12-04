# Brython - Browser Python via JavaScript Transpilation

## Overview

Brython (Browser Python) is a Python 3 implementation that transpiles Python code to JavaScript at runtime, enabling Python execution in web browsers without WebAssembly. Unlike Pyodide, it converts Python syntax to JavaScript, making it lightweight and fast to load.

**Website:** https://brython.info/
**Repository:** https://github.com/brython-dev/brython
**License:** BSD 3-Clause

## Architecture

### Execution Model
- **Core Technology:** Python-to-JavaScript transpiler
- **Python Version:** 3.x (matches major/minor since 3.8.0)
- **Runtime:** Pure JavaScript implementation
- **Compilation:** On-the-fly transpilation in browser

### Technical Implementation
- Parser converts Python AST to JavaScript AST
- JavaScript code executes directly in browser engine
- No WebAssembly required
- Standard library implemented in JavaScript
- DOM access via native JavaScript bridge

### Integration Points
- Simple script tag inclusion
- Python code in `<script type="text/python">` tags
- Direct DOM manipulation from Python
- Seamless JavaScript library integration

## Performance Analysis

### Startup Time
- **Initial Load:** <1 second (lightweight runtime)
- **Subsequent Loads:** Near-instant with caching
- **Bundle Size:** ~300-500 KB (compressed)
- **No Compilation Overhead:** Transpiles on-the-fly

### Execution Speed
- **Generally Fast:** Faster than Pyodide for many operations
- **Transpilation Cost:** Small overhead for initial parsing
- **JavaScript Speed:** Runs at JavaScript execution speed
- **Compromise:** Fast execution, larger generated code
- **No JIT Optimization:** Always slower than native Python

### Memory Usage
- **Base Footprint:** 5-10 MB
- **Low Overhead:** No WebAssembly memory allocation
- **JavaScript GC:** Standard browser garbage collection
- **Generated Code:** ~10x larger than original Python

### Bundle Size Advantage
- Smallest initial download among full Python implementations
- Fast loading crucial for user experience
- Mobile-friendly footprint
- Quick page interactivity

## Package Ecosystem

### Standard Library
- **Partial Implementation:** math, random, time, re, urllib (partial), unittest
- **Browser-Specific:** DOM, browser storage, events
- **No C Extensions:** Cannot run NumPy, Pandas, SciPy
- **Pure Python Only:** Limited to Python-only libraries

### Package Limitations
- **No Scientific Stack:** No NumPy, Pandas, Matplotlib, scikit-learn
- **No Package Manager:** No pip or micropip equivalent
- **Manual Integration:** Must bundle libraries manually
- **Limited Ecosystem:** No framework support

### Available Libraries
- Python standard library (subset)
- Custom Brython modules (browser, javascript, aio)
- Pure Python packages (with manual integration)
- JavaScript libraries via FFI

### Third-Party Library Integration
```python
# Access JavaScript libraries directly
from browser import window
window.jQuery("#myDiv").hide()

# Use any loaded JavaScript library
from javascript import JSObject
chart = JSObject(window.Chart)
```

## Security Model

### Sandboxing Mechanisms
- **Browser Sandbox:** JavaScript execution sandbox
- **No WebAssembly Isolation:** Relies on JavaScript security
- **Same-Origin Policy:** Standard browser restrictions
- **DOM Access Control:** Browser security model

### Code Execution Safety
- Less isolated than WebAssembly solutions
- Suitable for trusted code execution
- Educational environments (controlled contexts)
- Not recommended for untrusted user code

### Resource Limits
- JavaScript memory limits (typically 1-2 GB)
- Browser CPU throttling
- Network subject to CORS
- localStorage/IndexedDB quotas

### Security Considerations
- **No __del__ Method:** No finalizers (GC limitation)
- **JavaScript Interop Risks:** Potential for script injection
- **Limited Isolation:** Not as secure as Wasm sandboxing
- **Best for Trusted Code:** Internal tools, known users

## Integration Patterns

### Basic Usage
```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/brython@3.12.0/brython.min.js"></script>
</head>
<body onload="brython()">
  <script type="text/python">
    from browser import document, alert

    def greet(event):
        alert("Hello from Brython!")

    document["myButton"].bind("click", greet)
  </script>

  <button id="myButton">Click Me</button>
</body>
</html>
```

### DOM Manipulation
```python
from browser import document, html

# Create elements
div = html.DIV("Hello World", id="myDiv")
document <= div  # Append to document

# Query elements
element = document["myDiv"]
element.style.color = "blue"
```

### Event Handling
```python
from browser import document

def handle_click(event):
    print(f"Clicked at {event.x}, {event.y}")

document["myButton"].bind("click", handle_click)
```

### JavaScript Interoperability
```python
# Import JavaScript objects
from javascript import JSObject, this
from browser import window

# Call JavaScript functions
window.alert("Message")

# Access JavaScript libraries
jquery = window.jQuery
jquery("#element").fadeOut()
```

## Browser Compatibility

### Desktop Browsers
- **Chrome/Edge:** Full support (all modern versions)
- **Firefox:** Full support (all modern versions)
- **Safari:** Full support (v10+)
- **Opera:** Full support (all modern versions)
- **IE11:** Supported with polyfills (deprecated)

### Mobile Browsers
- **iOS Safari:** Full support, excellent performance
- **Android Chrome:** Full support, excellent performance
- **Mobile-Optimized:** Small bundle size ideal for mobile

### No Special Requirements
- No WebAssembly needed
- Works on older browsers (with polyfills)
- Pure JavaScript compatibility

## Use Cases

### Optimal For
- Lightweight web applications
- Interactive UI components
- Educational tools (controlled environments)
- Rapid prototyping
- DOM-heavy applications
- Mobile web apps (fast loading)
- Python developers working with web UI

### Not Ideal For
- Scientific computing (no NumPy/Pandas)
- Data analysis applications
- Machine learning in browser
- Untrusted code execution
- Large-scale applications
- Production systems requiring frameworks

## Advantages

1. **Fast Loading** - Smallest bundle size (<500 KB)
2. **Quick Startup** - <1 second initialization
3. **No WebAssembly** - Works on all browsers
4. **JavaScript Speed** - Fast execution after transpilation
5. **Easy Integration** - Simple script tag setup
6. **Direct DOM Access** - Native browser API integration
7. **Mobile Friendly** - Excellent mobile performance
8. **No Build Step** - Edit and reload development workflow
9. **JavaScript Library Access** - Use jQuery, D3, etc.

## Limitations

1. **No Scientific Stack** - Cannot run NumPy, Pandas, Matplotlib
2. **No Package Manager** - No pip or easy package installation
3. **Limited Standard Library** - Subset of Python stdlib
4. **Code Size Inflation** - Generated JS ~10x larger
5. **No Framework Ecosystem** - No Flask, Django, FastAPI equivalents
6. **Small Community** - Limited resources and examples
7. **No Finalizers** - No __del__ method support
8. **Weaker Isolation** - Less secure than WebAssembly
9. **Async Limitations** - Must use Brython's async module
10. **File System Restrictions** - Browser limitations apply

## Technical Maturity

- **Stability:** Mature and stable (10+ years)
- **Community:** Small but dedicated community
- **Documentation:** Comprehensive official docs
- **Maintenance:** Regular updates, active maintainer
- **Adoption:** Used in education, prototyping, interactive tools

## Brython vs Pyodide

### Advantages Over Pyodide
- 10-20x smaller bundle size
- 3-5x faster startup time
- Better mobile performance
- No WebAssembly requirement
- Simpler deployment

### Disadvantages vs Pyodide
- No scientific libraries (NumPy, Pandas)
- Smaller package ecosystem
- Less isolated (security)
- No C extension support
- Smaller community

## Development Experience

### Fast Iteration
- Edit Python code in HTML
- Reload browser to see changes
- No compilation or build step
- Inline error messages

### Debugging
- Browser DevTools work normally
- Source maps for Python code
- Console output via print()
- JavaScript error stack traces

### Async Support
```python
# Must use Brython's async module
from browser import aio

async def fetch_data():
    response = await aio.get("https://api.example.com/data")
    return response.json()

aio.run(fetch_data())
```

## Deployment Strategies

### CDN Delivery
```html
<script src="https://cdn.jsdelivr.net/npm/brython@3.12.0/brython.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/brython@3.12.0/brython_stdlib.js"></script>
```

### Self-Hosted
- Download brython.js (~300 KB)
- Optionally include brython_stdlib.js (additional features)
- Bundle in project assets
- No external dependencies

### Performance Optimization
- Minimize standard library inclusion
- Lazy load modules
- Cache aggressively
- Minify generated code

## Framework Limitations

### No Python Web Frameworks
- Cannot run Flask, Django, FastAPI
- Must build UI with DOM manipulation
- No template engines (Jinja2 not available)
- Pure Python logic only

### Workarounds
- Use JavaScript frameworks (React, Vue) + Brython for logic
- Server-side rendering with client-side Brython interactivity
- Hybrid JavaScript/Brython applications

## Real-World Applications

### Educational Platforms
- Interactive Python tutorials
- Code playgrounds
- Programming courses
- Computer science education

### Interactive Demos
- Algorithm visualizations
- API explorers
- Interactive documentation
- Code examples

### Web Utilities
- Calculators and converters
- Form validators
- UI widgets
- Browser extensions

## Future Roadmap

- Python 3.12+ compatibility
- Performance optimizations
- Better async/await support
- Expanded standard library coverage
- Improved debugging tools
- Source map generation
