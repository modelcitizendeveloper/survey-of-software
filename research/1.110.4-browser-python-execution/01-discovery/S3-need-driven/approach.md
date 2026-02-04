# S3: Need-Driven Discovery - Browser Python Execution

## Discovery Philosophy

**Start with requirements, validate through testing.**

Most technology evaluations begin with "what exists" and try to match it to needs. Need-driven discovery inverts this: define precise requirements first, then test each solution against those requirements with actual validation code.

## Core Principles

1. **Requirements First**: Define specific, measurable requirements before evaluating solutions
2. **Validation Testing**: Write actual test code that validates each requirement
3. **Use Case Driven**: Organize by industry use case patterns, not by technology
4. **Evidence Based**: Every claim backed by test results, not marketing materials
5. **Gap Analysis**: Explicitly document what requirements are NOT met

## Industry Use Case Patterns

### Interactive Python Tutorials
- **Critical Requirements**: Fast startup (<3s), small bundle size, beginner-friendly errors
- **Test Focus**: Cold start time, error message quality, basic syntax execution
- **Success Criteria**: Non-technical users can run code without confusion

### Data Science Notebooks
- **Critical Requirements**: NumPy/Pandas/Matplotlib, Jupyter compatibility, data visualization
- **Test Focus**: Package availability, visualization rendering, notebook format support
- **Success Criteria**: Real scientific workflows execute without modification

### Python REPLs (Embeddable)
- **Critical Requirements**: Minimal bundle (<5MB), fast embedding, isolated execution
- **Test Focus**: Bundle size, iframe isolation, multi-instance performance
- **Success Criteria**: Multiple REPLs on one page without interference

### Computational Widgets
- **Critical Requirements**: Fast compute, small footprint, offline capable
- **Test Focus**: Numerical computation speed, caching, progressive loading
- **Success Criteria**: Calculator/simulation loads <1s, works offline

### Security Sandboxing
- **Critical Requirements**: No file system access, resource limits, XSS prevention
- **Test Focus**: Attempt filesystem access, infinite loops, memory limits
- **Success Criteria**: Malicious code safely contained

## Validation Methodology

### 1. Define Requirements (Measurable)
- Startup time: <3s cold, <500ms warm
- Bundle size: <10MB for full stack, <5MB for REPL
- Python version: 3.10+
- Package support: NumPy, Pandas, Matplotlib minimum
- Security: No DOM access from Python, resource limits

### 2. Write Validation Tests
- Real HTML files that load each solution
- Actual Python code that tests each requirement
- Performance measurements (timing, bundle size)
- Security tests (attempt to break sandbox)

### 3. Document Results
- Pass/Fail for each requirement
- Performance numbers (not subjective opinions)
- Screenshots of actual tests running
- Gap analysis: what's missing?

### 4. Best Fit Analysis
- Which solution best satisfies EACH use case?
- Not "which is best overall" but "which is best FOR X?"
- Specific guidance by use case type

## Solutions Under Test

**Pyodide**: CPython compiled to WebAssembly, full standard library, pip support
**JupyterLite**: Full Jupyter environment in browser, built on Pyodide
**PyScript**: Declarative framework on Pyodide, HTML-first syntax

## Testing Tools

- Simple HTML harness files
- Performance.now() for timing measurements
- Network inspector for bundle size
- Browser DevTools for security validation
- Generic test cases (no proprietary code)

## Expected Outcomes

Not "Pyodide is best" but "For interactive tutorials, PyScript's HTML syntax reduces friction. For notebooks, JupyterLite is the obvious choice. For embeddable REPLs, raw Pyodide offers smallest footprint."

## Time Budget: 2-3 hours

Focus on validation quality, not exhaustive coverage. Better to thoroughly test 3 use cases than superficially test 10.
