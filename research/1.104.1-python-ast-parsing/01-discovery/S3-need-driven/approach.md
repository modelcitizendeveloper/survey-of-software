# S3: Need-Driven Discovery Approach

## Methodology Philosophy

**S3 Need-Driven Discovery** starts with the problem, not the solution. We begin by defining precise use case requirements, then evaluate which libraries best satisfy those needs. Our focus is practical fit: which library makes the developer's job easiest for their specific pattern?

## Core Principles

### 1. Requirements First
Define what success looks like before examining tools:
- **Functional requirements**: What must the library do?
- **Quality requirements**: How well must it perform?
- **Constraint requirements**: What limitations exist?

### 2. Evidence-Based Validation
Claims are verified through documentation:
- **Documentation review**: Does the library document this capability?
- **Example validation**: Do official examples demonstrate this pattern?
- **Community evidence**: Do tutorials/guides show real-world usage?

### 3. Fit Scoring Framework
Not all solutions are equal:
- **Perfect Fit (5/5)**: Library explicitly designed for this pattern
- **Good Fit (4/5)**: Library handles this naturally with documented approach
- **Adequate Fit (3/5)**: Library can do this but requires extra work
- **Poor Fit (2/5)**: Library struggles; workarounds needed
- **No Fit (1/5)**: Library fundamentally cannot satisfy requirement

### 4. Gap Analysis
Honest assessment of limitations:
- **Feature gaps**: What the library cannot do
- **Quality gaps**: What it does poorly
- **Edge case gaps**: Where it breaks down

## Discovery Process

### Step 1: Pattern Definition
Define generic, parameterized use case patterns:
- **Pattern name**: Clear, searchable identifier
- **Parameters**: Variables that change per instance
- **Invariants**: What stays constant across instances

### Step 2: Requirement Specification
For each pattern, define:
- **Must-have requirements**: Non-negotiable capabilities
- **Should-have requirements**: Important but not critical
- **Nice-to-have requirements**: Convenience features

### Step 3: Library Capability Mapping
For each library, answer:
- Can it satisfy must-have requirements? (yes/no)
- How well does it satisfy should-have requirements? (score)
- Does it provide nice-to-have features? (bonus points)

### Step 4: Comparative Fit Analysis
Compare libraries on requirement satisfaction:
- Which satisfies most must-haves?
- Which has fewest gaps?
- Which requires least workaround effort?

### Step 5: Recommendation
Select best fit based on:
- Requirement coverage
- Implementation effort
- Gap severity
- Real-world practicality

## Validation Framework

### Documentation Evidence
Every claim must be backed by:
- Link to official documentation
- Quote from relevant section
- Example code if available

### Fit Justification
Every fit score must explain:
- Why this score and not higher/lower?
- What specific capability supports this?
- What gap prevents higher score?

### Gap Documentation
Every identified gap must specify:
- What requirement is unmet?
- How severe is the gap?
- Is there a workaround? (effort required)

## Use Case Selection Criteria

We analyze patterns that represent:
- **Common operations**: Tasks many developers encounter
- **Critical operations**: Tasks that must work reliably
- **Complex operations**: Tasks that differentiate libraries
- **Generic patterns**: Not tied to specific applications

## Success Metrics

A successful S3 analysis delivers:
- Clear requirement-to-library mapping
- Justified fit scores with evidence
- Honest gap assessment
- Practical guidance for pattern-based selection
- Confidence ratings on recommendations
