# Skulpt - JavaScript Python Implementation

## Popularity Metrics

- **GitHub Stars**: 3,375 (September 2025)
- **Repository**: skulpt/skulpt
- **Forks**: 897
- **Watchers**: 238
- **Maintenance Status**: ✅ Active (updated September 2025)
- **Project Maintainer**: Brad Miller (since 2010/2011)
- **Python Version**: Transitioning from 2.x to 3.7-ish support

## Quick Validation (5-Minute Test)

**Time to "Hello World"**: ~3 minutes

```html
<!DOCTYPE html>
<html>
  <head>
    <script src="https://cdn.jsdelivr.net/npm/skulpt@1/dist/skulpt.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/skulpt@1/dist/skulpt-stdlib.js"></script>
  </head>
  <body>
    <script>
      function outf(text) {
        document.getElementById("output").innerHTML += text;
      }
      function builtinRead(x) {
        if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
          throw "File not found: '" + x + "'";
        return Sk.builtinFiles["files"][x];
      }
      Sk.configure({output:outf, read:builtinRead});
      Sk.importMainWithBody("<stdin>", false, "print('Hello World')");
    </script>
    <pre id="output"></pre>
  </body>
</html>
```

**Result**: ⚠️ Works but requires more setup than alternatives

## Ecosystem Size

### Technical Foundation
- **Approach**: JavaScript implementation of Python interpreter
- **Runtime**: No WebAssembly, pure JavaScript
- **Python Version**: Python 2.x legacy, working on Python 3.7+ support
- **Architecture**: Compiles Python to JavaScript

### Package Compatibility
- ❌ No NumPy/Pandas/SciPy (no C extension support)
- ✅ Limited standard library (skulpt-stdlib)
- ⚠️ Python 2.x compatibility as primary (Python 3 in progress)
- ❌ Very limited third-party package ecosystem

### Development Status
- **Python 3 Migration**: High priority project goal
- **Toolchain Updates**: Moved to Node.js + webpack
- **Active Work**: Python 3.9 pegen parser experiments (April 2023)

### Community Channels
- GitHub Issues and discussions
- Multiple organizational forks (blockpy-edu, trinketapp)
- Educational adoption (BlockPy project)
- Modest Stack Overflow presence

## Production Adoption Patterns

### Use Cases in the Wild
1. **Educational Platforms**: BlockPy uses Skulpt for teaching
2. **Online Python IDEs**: Trinket.io built on Skulpt
3. **Browser-Based Code Editors**: Simple Python execution
4. **Learning Environments**: Beginner Python tutorials
5. **Legacy Projects**: Python 2.x browser execution

### Adoption Context
- Primarily educational/learning platform niche
- Historical choice (pre-Pyodide era)
- Organizations built entire platforms on Skulpt
- Some migration pressure to newer solutions

## S1 Assessment

### Strengths
- ✅ Active maintenance (updates in 2025)
- ✅ Proven in educational context (BlockPy, Trinket)
- ✅ Lightweight compared to WebAssembly solutions
- ✅ Long project history (2010-present)

### Limitations
- ❌ Lowest GitHub stars (3.4k) among all options
- ❌ No scientific computing support (NumPy/Pandas/SciPy)
- ❌ Python 2.x primary, Python 3 still in progress
- ❌ Limited standard library implementation
- ❌ More complex setup than modern alternatives
- ⚠️ Being superseded by WebAssembly solutions

### "Just Works" Score: 5/10
Requires more manual setup than alternatives. Python 3 support incomplete. No scientific computing. Limited package ecosystem. Works for basic Python but with significant friction.

## Validation Verdict

**MARGINAL PASS** - Skulpt passes S1 only for very specific legacy or educational use cases. It has the lowest popularity metrics and most limitations among all solutions evaluated.

✅ **Good for**: Maintaining existing Skulpt-based platforms, extremely basic Python education, Python 2.x legacy code
❌ **Poor for**: New projects, scientific computing, modern Python 3.x features, data science applications

**Recommendation**: Do not choose Skulpt for new projects in 2025. The ecosystem has moved to WebAssembly-based solutions (Pyodide, PyScript, JupyterLite) that offer better Python 3 support, scientific computing packages, and larger communities. Skulpt's main value is for organizations with existing Skulpt infrastructure or very specific Python 2.x requirements.

The project is actively working on Python 3 support, but it's playing catch-up while WebAssembly solutions already deliver full CPython compatibility.
