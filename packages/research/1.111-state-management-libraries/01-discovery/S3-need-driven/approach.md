# S3 Need-Driven Discovery - Approach

**Phase**: S3 - Need-Driven Analysis
**Bead**: research-k9d (1.111 State Management Libraries)
**Date**: 2026-01-16

## Objectives

S3 flips the perspective from library-first (S2) to need-first. Each document analyzes a specific use case and determines which state management libraries fit best.

## Use Cases Covered

1. **Simple React SPA** - Todo app, basic CRUD, minimal state
2. **Complex Forms** - Multi-step wizards, validation, conditional fields
3. **Real-Time Collaboration** - Multiplayer editing, live cursors, WebSocket sync
4. **E-Commerce** - Shopping cart, checkout flow, inventory sync
5. **Analytics Dashboard** - Live metrics, charts, high-frequency updates
6. **Vue Project** - Vue-specific patterns and recommendations
7. **Cross-Cutting** - Multi-framework monorepos, micro-frontends

## Methodology

For each use case, we analyze:

### Requirements Analysis
- State complexity (simple, medium, complex)
- Update frequency (low, medium, high)
- Derived state needs (minimal, moderate, heavy)
- Performance constraints (bundle, runtime, memory)
- Team constraints (size, experience, timeline)

### Library Fit Scoring

**Scoring Matrix** (1-5 stars):
- ⭐ Poor fit (significant limitations)
- ⭐⭐ Workable (major compromises)
- ⭐⭐⭐ Good fit (minor trade-offs)
- ⭐⭐⭐⭐ Great fit (excellent match)
- ⭐⭐⭐⭐⭐ Perfect fit (ideal solution)

**Evaluation Criteria**:
1. API fit for use case patterns
2. Performance characteristics
3. Bundle size appropriateness
4. DevEx for specific needs
5. Ecosystem support (plugins, examples)

### Code Examples

Each use case includes:
- Requirements breakdown
- Implementation with top 2-3 libraries
- Performance comparison
- Trade-off analysis
- Final recommendation

## Deliverables

1. **approach.md** - This document
2. **use-case-react-spa.md** - Simple SPAs (10-15KB)
3. **use-case-complex-forms.md** - Multi-step forms, validation (10-15KB)
4. **use-case-real-time-collab.md** - Collaborative editing (10-15KB)
5. **use-case-e-commerce.md** - Shopping cart, checkout (10-15KB)
6. **use-case-dashboard.md** - Analytics dashboards (10-15KB)
7. **use-case-vue-project.md** - Vue-specific patterns (10-15KB)
8. **recommendation.md** - Cross-use-case synthesis (10KB)

## Use Case Selection Rationale

These use cases represent ~80% of real-world state management scenarios:

- **Simple SPA**: Entry point, learning, prototypes
- **Complex Forms**: Common enterprise need, validation-heavy
- **Real-Time**: Growing category (collaborative tools)
- **E-Commerce**: High-value business apps
- **Dashboard**: Data-intensive, performance-critical
- **Vue**: Second-largest framework after React
- **Multi-Framework**: Emerging architecture pattern

## Analysis Framework

### For Each Use Case

**1. Requirements Breakdown**
- State structure (flat, nested, normalized)
- Update patterns (mutations, batches, streams)
- Read patterns (selective, full-tree, computed)
- Performance needs (bundle, speed, memory)

**2. Library Evaluation**
Test each library against requirements:
- Redux Toolkit (enterprise standard)
- Zustand (popular choice)
- Jotai (atomic alternative)
- MobX (OOP/reactive)
- Pinia (Vue official)
- Valtio (proxy-based)
- Nanostores (minimal)
- Preact Signals (performance)
- TanStack Store (framework-agnostic)

**3. Implementation Comparison**
Side-by-side code for top candidates:
- Initial setup
- Core operations (CRUD)
- Advanced patterns (derived, async)
- Testing approach

**4. Decision Matrix**
Quantitative + qualitative assessment:
- Performance metrics
- Code volume (LoC)
- Complexity rating
- Maintainability score

**5. Recommendation**
Clear guidance:
- Primary recommendation
- Alternative (with trade-offs)
- Anti-recommendations (why not to use X)

## Quality Standards

Each use-case document must include:
- ✅ Real-world scenario description
- ✅ Concrete requirements list
- ✅ Code examples (2-3 libraries minimum)
- ✅ Performance analysis
- ✅ Clear recommendation with rationale
- ✅ Anti-patterns section (what NOT to do)
- ✅ 10-15KB content (substantial)

## Sources

- Real-world application architectures
- Community patterns (Reddit r/reactjs, Vue Discord)
- Official library documentation examples
- Production codebases (GitHub)
- Performance benchmarks from S2

## Connection to Other Phases

**S1 (Rapid)**: Quick overview → S3 uses for context
**S2 (Comprehensive)**: Library deep-dives → S3 references for details
**S4 (Strategic)**: Long-term viability → S3 uses for risk assessment

S3 is the "decision-making phase" - where teams choose based on actual needs rather than library features.
