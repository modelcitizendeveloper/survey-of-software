# S3: Need-Driven Discovery - Approach

## Methodology

Bottom-up exploration starting from specific user needs and use cases. Rather than surveying algorithms and libraries abstractly, we identify concrete problems and determine the best solutions.

## Problem-Driven Organization

### By Application Domain
- Web applications
- Command-line tools
- Compilers and interpreters
- Data processing pipelines
- Search systems
- Security applications

### By Performance Requirements
- Real-time constraints
- Batch processing scale
- Memory-constrained environments
- Network-bound operations

### By Input Characteristics
- Trusted vs untrusted input
- Size (small strings vs large documents)
- Frequency (one-time vs repeated operations)
- Character set (ASCII vs full Unicode)

## Scenario-Based Analysis

For each scenario, we identify:
1. **The problem**: What needs to be accomplished
2. **Constraints**: Performance, security, compatibility requirements
3. **Solution space**: Viable approaches
4. **Recommended choice**: Best-fit solution with rationale
5. **Alternatives**: When to choose differently
6. **Pitfalls**: Common mistakes

## Coverage

Focus on:
- Real-world problems developers actually encounter
- Practical trade-offs and decision-making
- Integration patterns and API design
- Error handling and edge cases
- Migration paths (replacing existing solutions)

## Goal

Provide actionable guidance: "When you have problem X with constraints Y, use solution Z because..."
