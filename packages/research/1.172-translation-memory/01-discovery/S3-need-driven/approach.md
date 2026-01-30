# S3 NEED-DRIVEN DISCOVERY: Approach

**Experiment**: 1.172 Translation Memory
**Pass**: S3 - Need-Driven Discovery
**Date**: 2026-01-29
**Target Duration**: 45-60 minutes

## Objective

Analyze Translation Memory systems from a **use case perspective**, identifying the optimal tool for specific real-world scenarios based on WHO needs it, WHY they need it, technical requirements, and library fitness.

## Research Method

For each use case, evaluate:

### Use Case Characteristics
- **WHO**: Personas and industries (software teams, LSPs, freelancers)
- **WHY**: Business impact (cost savings, quality, speed)
- **Context**: Organizational setting and workflow
- **Volume**: Words per year, language pairs, update frequency
- **Technical requirements**: Integration needs, latency, accuracy

### Tool Selection Criteria
- **Recommended tool**: Best fit based on requirements
- **Rationale**: Why this tool vs. alternatives
- **Implementation guidance**: Concrete code examples and workflows
- **Alternative options**: Backup choices with trade-offs
- **Success metrics**: Measurable targets for ROI

## Use Cases in Scope

### 1. Software Localization
**WHO**: SaaS companies, mobile app developers
**WHY**: Reuse UI translations across versions, reduce incremental translation costs
**Volume**: 10K-100K segments, 5-20 languages, quarterly releases
**Tool focus**: OmegaT (Git integration) or Memsource (CI/CD automation)

### 2. Translation Agencies
**WHO**: LSPs managing 10-100+ translators
**WHY**: Team scalability, client data isolation, consistent quality
**Volume**: 1M-10M words/year, 50+ projects simultaneously
**Tool focus**: MemoQ Server or SDL Trados GroupShare

### 3. Technical Documentation
**WHO**: Documentation teams for SaaS, APIs, hardware
**WHY**: Efficiently update translations when docs change monthly
**Volume**: 100K-500K words, 8-15 languages, monthly updates
**Tool focus**: OmegaT (docs-as-code) or Memsource (API-driven)

### 4. Enterprise Multilingual Content
**WHO**: Global corporations (marketing, training, compliance)
**WHY**: Brand consistency, corporate terminology enforcement
**Volume**: 5M+ words/year, 20-50 languages
**Tool focus**: SDL GroupShare (enterprise) or Memsource (cloud collaboration)

### 5. Freelance Translators
**WHO**: Independent translators specializing in legal, medical, technical
**WHY**: Build personal TM knowledge base, competitive pricing advantage
**Volume**: 500K-2M words/year, domain-specific
**Tool focus**: OmegaT (free, portable) or SDL Trados (agency compatibility)

## Deliverables

1. **approach.md** (this document)
2. **use-case-software-localization.md**
3. **use-case-translation-agencies.md**
4. **use-case-technical-documentation.md**
5. **use-case-enterprise-content.md**
6. **use-case-freelance-translators.md**
7. **recommendation.md**

## Success Criteria

- Identify optimal TM tool for each use case with clear rationale
- Provide actionable implementation guidance with code examples
- Include realistic ROI calculations and success metrics
- Address common pitfalls and edge cases
- Create decision matrix for tool selection

## Research Sources

- S1 and S2 findings (TM tool capabilities)
- Localization industry case studies (TAUS, GALA, Localization World)
- User reports from ProZ.com, translator forums
- Real-world deployment patterns from LSPs
- Published benchmarks on TM leverage rates
