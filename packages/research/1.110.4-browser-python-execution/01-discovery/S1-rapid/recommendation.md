# S1 Recommendation: Browser Python Execution

## Quick Decision Matrix

| Solution | GitHub Stars | Bundle Size | Scientific Computing | "Just Works" Score | Verdict |
|----------|-------------|-------------|---------------------|-------------------|---------|
| **Pyodide** | 13,900 | 7-20MB | ✅ Full Stack | 9/10 | **RECOMMENDED** |
| PyScript | 18,600 | 18.5MB | ✅ Full Stack | 7/10 | Conditional |
| JupyterLite | 4,669 | 7-20MB | ✅ Full Stack | 8/10 | Niche (Notebooks) |
| Brython | 6,458 | 1-2MB | ❌ None | 7/10 | Niche (Scripting) |
| Skulpt | 3,375 | ~2MB | ❌ None | 5/10 | Legacy Only |

## Primary Recommendation: Pyodide

**Confidence Level: HIGH (9/10)**

### S1 Rationale

Pyodide wins the S1 rapid library search based on:

1. **Proven Production Scale**: JupyterLite (built on Pyodide) serves 500,000 students with 200k+ weekly sessions
2. **Ecosystem Validation**: 13,900 GitHub stars + independent community-driven project
3. **Scientific Computing**: Only solution (with derivatives) offering full NumPy/Pandas/SciPy/Matplotlib
4. **"Just Works" Factor**: CDN link + 2 minutes = working Python code
5. **Foundation Layer**: Both PyScript and JupyterLite build on Pyodide (validates technical approach)

### When to Choose Pyodide

✅ **Use Pyodide directly when:**
- Building custom Python execution UI
- Integrating Python REPL into existing applications
- Need maximum control over Python runtime
- Want smallest bundle overhead (7MB core vs 18.5MB PyScript)
- Data science or scientific computing in browser
- Educational platforms with computational content

### Implementation Complexity
**Minimal**: Copy CDN link, write async JavaScript loader, execute Python strings. 15-20 lines of boilerplate code.

## Alternative: JupyterLite (Notebooks)

**Confidence Level: HIGH (8/10) for notebook use cases**

### When to Choose JupyterLite

✅ **Use JupyterLite when:**
- Jupyter notebooks are the desired interface
- Educational platform with notebook workflow
- Documentation sites with interactive examples
- Need full JupyterLab experience in browser
- Static site deployment (GitHub Pages, S3)
- Zero server infrastructure requirement

### Why Not Default?

JupyterLite is opinionated (notebook-only). If you need general Python execution without notebook UI, Pyodide is more flexible. But for notebook workflows, JupyterLite's proven 500k-student scale makes it the obvious choice.

## Alternative: PyScript (HTML-First)

**Confidence Level: MEDIUM (6/10)**

### When to Choose PyScript

✅ **Use PyScript when:**
- Python developers want web apps without learning JavaScript
- Corporate intranet tools (bandwidth not constrained)
- Internal dashboards and demos
- HTML-first development philosophy matches team
- Anaconda ecosystem alignment desired

### Why Not Default?

18.5MB bundle size and 3-second startup make it problematic for public web apps. Performance benchmarks show 70x slower loop execution vs Brython (7.71s vs 0.11s). High GitHub stars (18.6k) reflect developer interest, but practical testing reveals performance constraints.

**Trade-off**: Developer experience (HTML-first Python) vs user experience (slow loading).

## Alternative: Brython (Lightweight Scripting)

**Confidence Level: MEDIUM (6/10) for simple scripting**

### When to Choose Brython

✅ **Use Brython when:**
- Simple DOM manipulation in Python syntax
- No scientific computing needed
- Bundle size critical (<2MB requirement)
- Near-instant startup required
- Basic Python scripting only
- Avoiding JavaScript syntax preference

### Why Not Default?

No NumPy/Pandas/SciPy disqualifies it for majority of serious Python-in-browser use cases. Fast performance (0.11s loops) and small bundle are compelling, but limited to basic scripting niche.

## Not Recommended: Skulpt

**Confidence Level: LOW (3/10)**

Skulpt fails S1 criteria for new projects:
- Lowest popularity (3.4k stars)
- Python 2.x primary, Python 3 incomplete
- No scientific computing
- Being superseded by WebAssembly solutions

Only acceptable for maintaining existing Skulpt-based platforms.

## Generic Use Case Mapping

### Data Science Web Applications
**→ Pyodide** (direct) or **JupyterLite** (notebooks)
- Need: NumPy, Pandas, Matplotlib
- Bundle size acceptable for value provided
- 2-3 second startup acceptable for computational workflows

### Educational Platforms (Computational)
**→ JupyterLite** (if notebooks) or **Pyodide** (custom UI)
- Proven at 500k-student scale
- Full scientific computing support
- Static hosting economics

### Educational Platforms (Basic Python)
**→ Brython** (if no scientific computing) or **Pyodide** (if future-proofing)
- Lightweight for simple syntax teaching
- Instant startup for beginner experience

### Internal Corporate Tools
**→ PyScript** (HTML-first teams) or **Pyodide** (performance-conscious)
- Bandwidth less constrained on corporate networks
- Developer productivity may justify bundle size

### Public Web Apps (Performance-Critical)
**→ Pyodide** (with careful optimization) or **reconsider requirement**
- 7MB minimum bundle is non-negotiable
- 2-second startup requires loading UX
- Consider if Python truly needed vs JavaScript

### Interactive Documentation
**→ JupyterLite** (if notebooks) or **Pyodide** (embedded REPLs)
- Static hosting advantage
- Try-before-install experience
- Examples that actually execute

## Method Limitations

S1 explicitly ignores:

1. **Performance Tuning**: Detailed benchmarking needed for production (→ S2)
2. **Security Implications**: Browser sandbox risks, code injection (→ S3)
3. **Long-Term Maintenance**: Upgrade paths, breaking changes (→ S4)
4. **Edge Cases**: Memory limits, package conflicts, browser compatibility
5. **Architectural Fit**: Integration patterns, state management

## Confidence Assessment

**HIGH confidence in Pyodide recommendation** based on:
- Proven at massive scale (500k users via JupyterLite)
- Foundation for other successful projects (PyScript, JupyterLite)
- Active independent community (not dependent on single vendor)
- Full CPython compatibility via WebAssembly
- Comprehensive scientific computing support

**MEDIUM confidence in alternatives** (each excels in specific niches):
- JupyterLite: HIGH for notebooks specifically
- PyScript: MEDIUM due to performance trade-offs
- Brython: MEDIUM for lightweight scripting only
- Skulpt: LOW - legacy maintenance only

## Final Recommendation

**For 90% of browser Python needs: Start with Pyodide.**

It's the proven foundation layer that balances capability, performance, and community validation. If you later need notebooks (JupyterLite) or HTML-first framework (PyScript), they both build on Pyodide anyway.

The WebAssembly approach (Pyodide) has won the browser Python execution battle. Transpilers (Brython, Skulpt) are niche solutions for specific lightweight constraints.
