# Discovery vs Implementation: Clear Boundaries

**Purpose**: Prevent mixing implementation/validation work into discovery research
**Created**: November 7, 2025
**Context**: Hardware Store for Software philosophy - keep research generic

---

## The Three Layers

### 1. Discovery (01-discovery/) - RESEARCH ONLY

**What it IS**:
- Reading documentation, GitHub repos, case studies
- Analyzing existing benchmarks from maintainers/community
- Comparing features across libraries (from docs/marketing)
- Strategic analysis (maintenance, adoption, vendor viability)
- **NO code execution** - pure research

**S1 Rapid**: Quick ecosystem scan
- GitHub stars, last commit, maintenance status
- Documentation quality check
- Quick capability assessment from docs
- **NOT**: Running hello world examples

**S2 Comprehensive**: Deep research
- Multi-source discovery (PyPI, GitHub, academic papers)
- Documentation deep-dives (API reference, tutorials)
- Existing benchmarks (from official sources, blog posts)
- Production case studies (who uses it, what they say)
- **NOT**: Running our own benchmarks

**S3 Need-Driven**: Generic use case patterns
- Pattern: "Insert code at specific location with formatting"
- Pattern: "Parse files with syntax errors gracefully"
- Pattern: "Preserve comments and docstrings"
- **NOT**: "For schema evolution orchestrator layer updaters"

**S4 Strategic**: Long-term viability
- Maintenance trajectory, Python version support roadmap
- Vendor/community health, market consolidation
- Technology evolution (e.g., Rust parsers replacing Python)
- **NOT**: Application-specific ROI calculations

### 2. Implementation (02-implementations/) - VALIDATION WORK

**What it IS**:
- Installing libraries and running code
- Writing proof-of-concepts
- Running benchmarks on your machine
- Testing edge cases hands-on
- Performance measurements
- Learning curve assessment (actual timer)

**Examples**:
- `validation-plan.md` - Hands-on testing plan
- `benchmarks/` - Performance tests you run
- `proof-of-concept/` - Working code examples
- `edge-cases/` - Test cases you discovered

**When to create**:
- After S1-S4 discovery is complete
- When you need to validate claims from research
- For application-specific validation
- To measure actual performance in your environment

### 3. Applications (applications/{app}/) - APPLICATION-SPECIFIC

**What it IS**:
- Strategic analysis for specific product needs
- Application-specific ROI calculations
- Integration plans for your architecture
- Migration roadmaps from current systems
- Technology selection decisions for your app

**Examples**:
- `applications/schema-evolution-automation/` - Why we chose LibCST
- `applications/qrcards/` - QR code library selection for QRCards app
- Application-specific implementation details

---

## Clear Boundaries

### ❌ NEVER in Discovery (S1-S4):

1. **Implementation Plans**
   - "Install library X and test..."
   - "Run benchmarks on files of size..."
   - "Write proof-of-concept that..."

2. **Application-Specific Content**
   - "For our schema evolution framework..."
   - "Based on our 7-layer architecture..."
   - "Given our use case requirements..."

3. **Hands-On Validation**
   - "Time how long it takes to..."
   - "Test with our models.py file..."
   - "Measure performance on our machine..."

4. **Code Execution**
   - Running examples
   - Installing packages
   - Writing test scripts

### ✅ ALWAYS in Discovery (S1-S4):

1. **Generic Research**
   - "According to official documentation..."
   - "GitHub shows last commit was..."
   - "Maintainers claim X performance..."
   - "Production users report Y..."

2. **Generic Use Case Patterns**
   - "Pattern: Find last method in class definition"
   - "Pattern: Preserve formatting during modification"
   - NOT: "For ORM layer updaters in our orchestrator"

3. **Technology Landscape**
   - "CST vs AST architecture trade-offs"
   - "Industry adoption trends"
   - "Maintenance health indicators"

4. **Evidence Citation**
   - "Per LibCST docs section 4.2..."
   - "Instagram blog post describes..."
   - "PyPI shows 3.1M weekly downloads..."

---

## Red Flags in Discovery Documents

If you see these phrases in S1-S4, move them to 02-implementations/ or applications/:

- ❌ "Install and test..."
- ❌ "Run benchmarks on..."
- ❌ "For our use case..."
- ❌ "Based on our requirements..."
- ❌ "Time how long it takes..."
- ❌ "Write proof-of-concept..."
- ❌ "Test with our files..."
- ❌ "Integrate with our architecture..."

---

## Validation Checklist for Discovery Documents

Before marking S1-S4 complete, check:

- [ ] No hands-on testing plans (move to 02-implementations/)
- [ ] No application-specific references (move to applications/)
- [ ] No code execution described (move to 02-implementations/)
- [ ] All use cases are generic patterns, not specific to one app
- [ ] All claims cite sources (docs, GitHub, blog posts, etc.)
- [ ] Content is reusable reference material for any developer

---

## Quick Decision Tree

**Writing content for experiment X.YYY, where does it go?**

```
Is it hands-on testing/benchmarking?
├─ YES → 02-implementations/
└─ NO ↓

Is it specific to Application Z?
├─ YES → applications/{app}/
└─ NO ↓

Is it research/analysis of the technology landscape?
├─ YES → 01-discovery/S1-S4/
└─ ??? → Clarify what you're writing
```

---

## Example: Python AST Libraries (1.104.1)

**01-discovery/** - Generic library research:
- LibCST capabilities from documentation
- Comparison of CST vs AST architectures
- Generic use case patterns (find class, insert code, preserve formatting)
- Strategic analysis (Meta backing, maintenance, Python version support)

**02-implementations/** - Validation work:
- `validation-plan.md` - Hands-on testing plan
- `benchmarks/` - Performance tests on sample files
- `proof-of-concept/` - Working LibCST examples
- `edge-cases/` - Testing multi-line strings, decorators, etc.

**applications/schema-evolution-automation/** - Application-specific:
- Why we chose LibCST for schema evolution framework
- Integration with 7-layer orchestrator architecture
- ROI calculation for our specific use case
- Migration plan from manual code editing

---

## Framework Update Proposal

**Proposed Addition to MPSE v3.0** (frameworks/MPSE_V2.md):

Add after "Enhanced Independence Protocols" section:

```markdown
## 🔒 Discovery vs Implementation Boundaries

**Critical Separation**: Keep research generic, implementation application-specific

### Discovery (01-discovery/) - Research Phase
- **What**: Reading, analyzing, comparing (no code execution)
- **Output**: Generic reference material reusable by any developer
- **Validation**: No app-specific content, no hands-on testing plans

### Implementation (02-implementations/) - Validation Phase
- **What**: Installing, testing, benchmarking (hands-on work)
- **Output**: Proof-of-concepts, performance data, validation results
- **When**: After S1-S4 complete, before application integration

### Applications (applications/{app}/) - Strategic Decision Phase
- **What**: App-specific ROI, integration plans, technology selection
- **Output**: Why we chose X for app Y, migration roadmaps
- **When**: After validation proves library viable for specific use case

**See**: research/.templates/DISCOVERY_VS_IMPLEMENTATION.md for detailed guidance
```

---

**This guidance document should prevent future mixing of discovery/implementation/application content.**
