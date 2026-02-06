# Skulpt - JavaScript-Based Python 2.x Implementation

## Overview

Skulpt is a JavaScript implementation of Python 2.x designed for educational purposes and browser-based Python execution. Created in 2009, it focuses on providing a Python environment for learning and interactive coding without requiring server infrastructure.

**Website:** https://skulpt.org/
**Repository:** https://github.com/skulpt/skulpt
**License:** MIT License

## Architecture

### Execution Model
- **Core Technology:** Python interpreter written in JavaScript
- **Python Version:** 2.x (Python 3 support in progress)
- **Runtime:** Pure JavaScript implementation
- **Execution:** Interprets Python bytecode in JavaScript

### Technical Implementation
- Python parser generates bytecode
- JavaScript-based bytecode interpreter
- No compilation to native JavaScript
- Virtual machine executes instructions
- DOM integration for browser APIs

### Integration Points
- JavaScript API for embedding
- Script tag inclusion
- Configurable input/output handling
- Module system for extensions

## Performance Analysis

### Startup Time
- **Initial Load:** <1 second
- **Subsequent Loads:** Near-instant with caching
- **Bundle Size:** ~400-600 KB
- **Fast Initialization:** Lightweight runtime

### Execution Speed
- **Slower than Native Python:** Interpreted bytecode overhead
- **80/20 Rule:** Covers 80-90% of common use cases
- **Educational Performance:** Adequate for learning scenarios
- **Not Optimized for Speed:** Focus on compatibility

### Memory Usage
- **Base Footprint:** 5-15 MB
- **JavaScript GC:** Standard browser memory management
- **Modest Requirements:** Suitable for resource-constrained environments

### Bundle Size
- Small download footprint
- Mobile-friendly
- Quick page load times

## Package Ecosystem

### Standard Library Support
**Implemented Modules:**
- math - Mathematical functions
- random - Random number generation (partial)
- turtle - Graphics library for education
- time - Time access (partial)
- urllib - URL handling (partial)
- unittest - Testing framework
- image - Image manipulation
- DOM - Browser DOM access (partial)
- re - Regular expressions (partial)

### Library Limitations
- **No Scientific Stack:** No NumPy, Pandas, SciPy, Matplotlib
- **Partial Implementations:** Many stdlib modules incomplete
- **No Package Manager:** No pip or easy installation
- **Educational Focus:** Prioritizes teaching over completeness

### Advanced Module Requests
- Community has requested matplotlib, tkinter, numpy
- These contain C code, making porting extremely challenging
- Unlikely to be implemented due to complexity

### Python 3 Migration
- Python 2 end-of-life drives Python 3 work
- Ongoing effort to support Python 3.x
- Breaking changes require significant refactoring

## Security Model

### Sandboxing Mechanisms
- **Browser Sandbox:** JavaScript execution environment
- **No File System Access:** Browser restrictions apply
- **Network Limitations:** CORS and same-origin policies
- **Storage:** localStorage/IndexedDB only

### Code Execution Safety
- Suitable for educational environments (student code)
- Browser sandbox provides basic isolation
- Less secure than WebAssembly solutions
- Designed for trusted or semi-trusted code

### Resource Limits
- JavaScript memory constraints
- Browser CPU throttling
- No native resource controls
- Depends on browser enforcement

### Security Considerations
- Educational focus assumes controlled environment
- Not designed for untrusted production code
- Basic isolation via browser sandbox
- Suitable for classroom/tutorial settings

## Integration Patterns

### Basic Embedding
```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://skulpt.org/js/skulpt.min.js"></script>
  <script src="https://skulpt.org/js/skulpt-stdlib.js"></script>
</head>
<body>
  <script type="text/javascript">
    function outf(text) {
      document.getElementById("output").innerHTML += text;
    }

    function builtinRead(x) {
      if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
        throw "File not found: '" + x + "'";
      return Sk.builtinFiles["files"][x];
    }

    function runit() {
      var prog = document.getElementById("pythonCode").value;
      Sk.configure({output:outf, read:builtinRead});
      Sk.misceval.asyncToPromise(() => {
        return Sk.importMainWithBody("<stdin>", false, prog, true);
      });
    }
  </script>

  <textarea id="pythonCode" rows="10" cols="50">
print "Hello from Skulpt!"
  </textarea>
  <button onclick="runit()">Run</button>
  <pre id="output"></pre>
</body>
</html>
```

### Output Handling
```javascript
function outputHandler(text) {
  console.log(text);
  // Or append to DOM element
  document.getElementById("output").textContent += text;
}

Sk.configure({output: outputHandler});
```

### Input Handling
```javascript
function inputHandler(prompt) {
  return window.prompt(prompt);
}

Sk.configure({inputfun: inputHandler});
```

## Browser Compatibility

### Desktop Browsers
- **Chrome/Edge:** Full support (all modern versions)
- **Firefox:** Full support (all modern versions)
- **Safari:** Full support (v10+)
- **Opera:** Full support (all modern versions)
- **IE:** Supported with polyfills (deprecated)

### Mobile Browsers
- **iOS Safari:** Works well, lightweight
- **Android Chrome:** Full support
- **Mobile-Optimized:** Small bundle suitable for mobile

### No Special Requirements
- Pure JavaScript, no WebAssembly
- Works on older browsers
- Broad compatibility

## Use Cases

### Optimal For
- Educational platforms (Python learning)
- Interactive Python textbooks
- Code playgrounds for beginners
- Turtle graphics tutorials
- Computer science education (intro courses)
- Simple Python demonstrations

### Not Ideal For
- Production applications
- Scientific computing
- Data analysis
- Modern Python 3.x features
- Performance-critical code
- Large-scale applications

## Advantages

1. **Educational Focus** - Designed for teaching Python
2. **Turtle Graphics** - Built-in turtle module for visual learning
3. **Small Bundle** - Fast loading (~400-600 KB)
4. **Quick Startup** - <1 second initialization
5. **Pure JavaScript** - No WebAssembly required
6. **Broad Compatibility** - Works on older browsers
7. **Interactive Textbooks** - Proven in educational settings
8. **Simple Integration** - Straightforward JavaScript API
9. **Mobile Friendly** - Lightweight for mobile devices

## Limitations

1. **Python 2.x** - Outdated language version (Python 3 in progress)
2. **Incomplete Standard Library** - Many modules partial or missing
3. **No Scientific Stack** - Cannot run NumPy, Pandas, Matplotlib
4. **No Package Manager** - No pip or package installation
5. **Small Community** - Limited resources and updates
6. **Performance** - Slower than other implementations
7. **Feature Incomplete** - 80/20 rule applies (basic features work)
8. **No Advanced Features** - Modern Python features unavailable
9. **Limited Builtins** - Some not implemented or partial

## Technical Maturity

- **Stability:** Mature but feature-limited
- **Community:** Small, primarily educational focus
- **Documentation:** Basic documentation available
- **Maintenance:** Sporadic updates, slow development
- **Adoption:** Used in education (Interactive Python, BlockPy)

## Educational Applications

### Interactive Python Textbooks
- "How to Think Like a Computer Scientist"
- "Problem Solving with Algorithms and Data Structures"
- Various computer science curricula

### BlockPy Project
- Visual programming + text-based Python
- Used in university CS courses
- Integrated with Skulpt for execution

### Code Learning Platforms
- Simple Python REPL environments
- Tutorial exercises with instant feedback
- Introductory programming courses

## Skulpt vs Modern Alternatives

### Advantages Over Pyodide
- 10-15x smaller bundle
- Faster startup
- Simpler for basic education
- No WebAssembly complexity

### Disadvantages vs Pyodide
- Python 2.x (outdated)
- No scientific libraries
- Incomplete features
- Slower performance
- Smaller ecosystem

### Advantages Over Brython
- Established educational track record
- Turtle graphics included
- Simpler API for educators

### Disadvantages vs Brython
- Python 2.x vs Python 3.x
- Fewer features
- Less active development

## Development Status

### Python 3 Migration
- Active effort to support Python 3.x
- Significant work required
- Community contributions welcomed
- No definite timeline

### Feature Completeness
- Core language features mostly work
- Advanced features often missing
- Focus on 80/20 coverage
- Prioritizes education over completeness

### Community Involvement
- Open to contributions
- Small core team
- Educational users provide feedback
- Slow but steady progress

## Deployment Strategies

### CDN Hosting
```html
<script src="https://skulpt.org/js/skulpt.min.js"></script>
<script src="https://skulpt.org/js/skulpt-stdlib.js"></script>
```

### Self-Hosting
- Download skulpt.min.js and skulpt-stdlib.js
- Bundle in project assets
- No build process required
- Simple static file serving

### Educational Platforms
- Embed in learning management systems (LMS)
- Integrate with autograders
- Provide instant feedback
- Enable interactive exercises

## Configuration Options

### Output Configuration
```javascript
Sk.configure({
  output: outputFunction,      // Handle print statements
  read: builtinReadFunction,   // File reading
  inputfun: inputFunction,     // Handle input()
  __future__: Sk.python3       // Python 3 mode (experimental)
});
```

### Execution Options
```javascript
Sk.misceval.asyncToPromise(() => {
  return Sk.importMainWithBody("<stdin>", false, code, true);
}).then(
  () => console.log("Success"),
  (err) => console.error(err.toString())
);
```

## Turtle Graphics

### Educational Visualization
```python
import turtle

t = turtle.Turtle()
for i in range(4):
    t.forward(100)
    t.right(90)
```

### Visual Learning
- Teaches programming concepts visually
- Immediate feedback for students
- Engages learners with graphics
- Standard Python turtle API

## Comparison Summary

### Best Use Case
Skulpt excels for introductory Python education where:
- Python 2.x compatibility is acceptable (or Python 3 experimental mode)
- Turtle graphics is desired
- Scientific libraries are not needed
- Students are learning basic programming concepts
- Quick browser-based execution is required

### When to Choose Alternatives
- **Pyodide:** Need Python 3.x, scientific libraries, or modern features
- **Brython:** Want Python 3.x and faster development
- **PyScript:** Need modern framework with multiple backend options

## Future Roadmap

- Complete Python 3.x support
- Expand standard library coverage
- Improve performance
- Better debugging tools
- More complete builtin implementations
- Community-driven enhancements
