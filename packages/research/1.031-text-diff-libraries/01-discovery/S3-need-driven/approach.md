# S3 Need-Driven Discovery - Approach

## Goal

Map requirements to library choices through real-world use cases. Answer "WHO needs diff libraries and WHY?"

**NOT implementation guides** - this identifies needs and validates library fit.

## Discovery Strategy

### Requirement-First
- Start with user personas and their problems
- Identify specific constraints (scale, ecosystem, team skills)
- Map to library capabilities discovered in S1/S2
- Validate technical fit against S2 feature matrix

### Scenario-Based Selection
- Each use case = specific context + requirements
- Multiple valid solutions per use case (trade-offs explicit)
- Anti-patterns identified (wrong tool for the job)
- Success criteria for validation

## Use Case Structure

Each use-case-*.md file follows WHO + WHY format:

```
## Who Needs This
- Persona description
- Context (team, project, constraints)
- Scale/volume expectations

## Why They Need It
- Problem statement
- Specific requirements (must-haves)
- Nice-to-haves
- Constraints (time, budget, skills)

## Library Fit Analysis
- Recommended libraries (with trade-offs)
- Anti-patterns (what NOT to use)
- Decision factors

## Validation Criteria
- How to test if choice is correct
- Red flags indicating wrong choice
```

## Use Cases Covered

1. **Software testing engineers** - Comparing test outputs
2. **Code review automation builders** - Git integration for CI/CD
3. **Data engineers** - Comparing structured data (JSON, XML, objects)
4. **Developer tool creators** - Semantic code analysis
5. **Text processing application developers** - Fuzzy matching, deduplication

## Success Criteria

S3 complete when we have:
- ✅ 3-5 use-case-*.md files
- ✅ Each starts with "## Who Needs This" or "## User Persona"
- ✅ Clear requirement → library mapping
- ✅ Trade-offs and anti-patterns identified
- ✅ Validation criteria provided

**NOT success**: Implementation tutorials, code walkthroughs, CI/CD setup guides
