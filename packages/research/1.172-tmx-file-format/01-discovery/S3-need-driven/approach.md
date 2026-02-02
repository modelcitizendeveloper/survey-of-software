# S3 Approach: Need-Driven Selection for TMX Libraries

## Purpose of This Document

This document explains the **scenario-based selection methodology** for TMX translation memory libraries. Unlike S2 (technical comparison) which focuses on WHAT libraries can do, S3 focuses on WHO needs them and WHY.

**Not included**: Technical implementation details, code examples, CI/CD workflows

**Included**: User personas, requirements, constraints, library fitness criteria

## S3 Methodology: Persona-Driven Selection

### 1. Define User Personas

Each persona represents a distinct user archetype with specific:
- **Role**: Professional context (freelancer, developer, researcher, etc.)
- **Goals**: What they're trying to achieve with TMX files
- **Constraints**: Budget, time, technical expertise, infrastructure
- **Pain points**: Current problems that need solving

### 2. Map Requirements to Library Capabilities

For each persona, identify:
- **Must-have requirements**: Non-negotiable technical needs (deal-breakers)
- **Nice-to-have features**: Valuable but not essential
- **Anti-requirements**: Features that complicate without adding value
- **Infrastructure constraints**: Python version, platform, dependencies

### 3. Evaluate Library Fitness

Match persona requirements against S2 technical findings:
- **Primary fit**: Library designed for this use case
- **Acceptable fit**: Library can handle it with workarounds
- **Poor fit**: Library technically capable but impractical
- **Not suitable**: Library cannot meet must-have requirements

### 4. Provide Requirement-Driven Recommendations

Instead of "use library X", provide decision rules:
- "If you need [requirement A] AND [requirement B], use library X"
- "If [constraint C] applies, avoid library Y"
- "If [scenario D], consider library Z despite [trade-off E]"

## TMX Context for Personas

### What is TMX?

Translation Memory eXchange (TMX) is an XML standard for storing translation memories - databases of source-target language pairs that enable translators to reuse previous translations.

**Key concepts**:
- **Translation Unit (TU)**: A source segment and its translations
- **Translation Unit Variant (TUV)**: Language-specific content within a TU
- **Segment**: The actual translatable text
- **Inline markup**: Formatting tags embedded in text (e.g., bold, links, placeholders)
- **TMX Level 1**: Inline markup preserved as unstructured text
- **TMX Level 2**: Inline markup represented as structured nested objects

### Who Uses TMX?

1. **Professional translators**: Freelancers using CAT (Computer-Aided Translation) tools
2. **Localization agencies (LSPs)**: Companies managing translations for clients
3. **Software companies**: Developers integrating translation workflows
4. **NLP researchers**: Scientists extracting parallel corpora for machine translation
5. **CAT tool developers**: Engineers building translation software

### Why Python for TMX?

- **Automation**: Batch processing, quality checks, migrations
- **Integration**: Connecting CAT tools with version control, CMSs, databases
- **Custom workflows**: Workflows not supported by commercial CAT tools
- **Research**: Data extraction, corpus building, statistical analysis

## S3 vs S2: Complementary Perspectives

| Aspect | S2 (Technical) | S3 (Need-Driven) |
|--------|---------------|------------------|
| **Question** | What can each library do? | Who should use each library? |
| **Focus** | Features, performance, API | Personas, requirements, constraints |
| **Content** | Benchmarks, comparisons, trade-offs | Use cases, workflows, decision rules |
| **Structure** | Library-centric (compare X vs Y) | Persona-centric (who needs X?) |
| **Outcome** | Technical capability matrix | Requirement-based selection guide |

**Example**:
- **S2**: "hypomnema supports TMX Level 2 with streaming API, requires Python 3.12+"
- **S3**: "NLP researchers need Level 2 for inline markup extraction → hypomnema fits if Python 3.12+ available, otherwise translate-toolkit with manual parsing"

## Use Case File Structure

Each `use-case-<persona>.md` file follows this format:

### 1. Who Needs This (Required)

Start with persona definition:
- **Role**: Professional identity
- **Context**: Work environment, team size, budget
- **Technical background**: Programming experience, infrastructure access

### 2. Requirements and Constraints

**Must-have requirements**: Deal-breakers
- Format: "Must support X because [business reason]"

**Constraints**: Limitations imposed by environment
- Licensing, Python version, platform, dependencies

**Anti-requirements**: Features that add complexity without value

### 3. Current Workflow and Pain Points

**As-is workflow**: How they currently work with TMX
**Pain points**: Specific problems needing solutions

### 4. Library Fitness Assessment

For each library (translate-toolkit, hypomnema, polib):
- **Fitness rating**: Primary fit / Acceptable / Poor fit / Not suitable
- **Rationale**: Why this rating (reference S2 findings)
- **Trade-offs**: Costs vs benefits for this persona

### 5. Decision Criteria

Provide conditional recommendations:
- "Use X if [condition A]"
- "Avoid Y if [constraint B]"
- "Consider Z when [scenario C]"

### 6. Migration Considerations (if applicable)

For personas with existing workflows:
- What changes if they adopt library X?
- Compatibility with existing tools/data
- Training/learning curve

## Personas Covered in S3

1. **Freelance Translators** (`use-case-freelance-translators.md`)
   - Solo practitioners managing personal translation memories
   - Need: Build reusable TM database across projects

2. **Localization Agencies** (`use-case-localization-agencies.md`)
   - LSPs with large-scale translation workflows
   - Need: Multi-client CAT tool integration, QA automation

3. **NLP Researchers** (`use-case-nlp-researchers.md`)
   - Scientists extracting parallel corpora from TMX datasets
   - Need: Train machine translation models, linguistic analysis

4. **Enterprise Localization Teams** (`use-case-enterprise-localization.md`)
   - Software companies with continuous localization pipelines
   - Need: CI/CD integration, version control, automation

5. **CAT Tool Developers** (`use-case-cat-tool-developers.md`)
   - Engineers building custom translation software
   - Need: Native TMX support in commercial products

## Key Differentiation: Requirements → Libraries

The core value of S3 is mapping personas to libraries via requirements:

```
Persona → Requirements → Constraints → Library Fitness
```

**Example decision flow**:

```
NLP Researcher
├─ Requirement: Extract inline markup structure (Level 2)
├─ Requirement: Process large corpora (1M+ units)
├─ Constraint: Python 3.12+ available
└─ Result: hypomnema (primary fit: streaming + Level 2)

vs.

Freelance Translator
├─ Requirement: Export PO → TMX for CAT tool import
├─ Requirement: Simple one-off scripts
├─ Constraint: Python 3.11 (no upgrade budget)
└─ Result: translate-toolkit (primary fit: po2tmx CLI + stable)
```

## Relationship to Other Phases

- **S1 (Rapid)**: Initial landscape scan → Libraries exist and are viable
- **S2 (Comprehensive)**: Technical evaluation → How each library works
- **S3 (Need-Driven)**: Persona mapping → Who should use which library and why
- **S4 (Strategic)**: Ecosystem analysis → Where TMX fits in broader landscape

S3 bridges technical capabilities (S2) with real-world adoption decisions (who, when, why).

## Anti-Patterns to Avoid

### Don't Include in S3:

1. **Code examples**: Implementation details belong in tutorials, not persona analysis
2. **Installation instructions**: Technical how-to, not requirement analysis
3. **Benchmarks**: Performance numbers in S2, not use cases
4. **API documentation**: Technical reference, not persona needs
5. **CI/CD workflows**: Implementation details, not requirements

### Do Include in S3:

1. **Persona context**: Who they are, what they do, why TMX matters
2. **Business requirements**: Must-haves driven by business needs
3. **Constraints**: Real-world limitations (budget, expertise, infrastructure)
4. **Decision criteria**: Conditional recommendations based on requirements
5. **Trade-offs**: Explicit costs vs benefits for each persona

## Validation Criteria

Each use-case file must:
- [ ] Start with "## Who Needs This" or "## User Persona"
- [ ] Define persona before discussing libraries
- [ ] Focus on WHY (requirements) not HOW (implementation)
- [ ] Reference S2 for technical justifications
- [ ] Provide conditional decision rules, not prescriptive "use X"
- [ ] Avoid code examples and implementation details
- [ ] Address constraints (licensing, Python version, dependencies)

## Summary: S3 Value Proposition

**For readers**: "I see myself in persona X → These are my requirements → Library Y fits because [technical reason from S2]"

**For decision-makers**: Requirement-driven selection based on business context, not just technical features.

This approach ensures library selection aligns with real-world needs, constraints, and workflows.
