# S3 Need-Driven Discovery - Approach

**Phase**: S3 Need-Driven (In Progress)
**Goal**: Identify WHO needs full-text search libraries and WHY
**Date**: February 2026

---

## S3 Methodology

S3 answers the fundamental questions:
- **WHO** encounters the need for full-text search in their workflow?
- **WHY** do they need it? (What problem are they solving?)
- **WHEN** does DIY search make sense vs managed services?

This is NOT about implementation (that's S2 and S4). This is about understanding the decision-makers and their contexts.

---

## Identified User Personas

Based on S1 findings and the full-text search landscape, we identified 5 distinct user groups:

1. **Product Developers (User-Facing Search)** - Building apps where search is a core feature
2. **Technical Writers & Doc Site Builders** - Need search for static documentation
3. **Academic Researchers** - Conducting reproducible information retrieval research
4. **Prototype & Proof-of-Concept Builders** - Quick validation without infrastructure overhead
5. **Scale-Aware Architects** - Making build-vs-buy decisions based on data scale

Each persona has distinct:
- **Context**: Where they work, what they build
- **Requirements**: Performance, scale, installation constraints
- **Decision criteria**: What makes a library suitable for their needs
- **Path to managed services**: When DIY stops making sense

---

## What S3 is NOT

❌ S3 does NOT contain:
- Implementation guides ("how to install")
- Code examples or tutorials
- CI/CD workflows
- Infrastructure architecture

✅ S3 DOES contain:
- User contexts and motivations
- Decision criteria from user perspective
- Requirements validation
- When DIY search makes sense vs managed services

---

## Use Case Files

Each use case file follows this structure:

```markdown
## Who Needs This
[Persona description, context, role]

## Why They Need Full-Text Search
[Problem being solved, business/technical motivation]

## Their Requirements
[Performance, scale, features, constraints]

## Library Selection Criteria
[How they evaluate options from S1]

## When to Consider Managed Services
[Scale/complexity triggers for Path 3]
```

---

## S3 Artifacts

- ✅ `approach.md` - This document
- 🔄 `use-case-product-developers.md` - User-facing search builders
- 🔄 `use-case-documentation-sites.md` - Static site search
- 🔄 `use-case-academic-researchers.md` - IR research use case
- 🔄 `use-case-prototype-builders.md` - Quick proof-of-concept
- 🔄 `use-case-scale-aware-architects.md` - Build vs buy decisions
- 🔄 `recommendation.md` - Persona-to-library mapping

---

**S3 Status**: 🔄 In Progress
**Estimated Completion**: Same session
**Next Action**: Create use case files for each persona
