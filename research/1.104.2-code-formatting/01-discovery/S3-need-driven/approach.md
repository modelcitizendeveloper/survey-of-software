# S3 Need-Driven Discovery: Code Formatting Tools

## Methodology Overview

S3 Need-Driven Discovery matches specific workflow requirements to optimal code formatting solutions through requirement validation and perfect solution alignment.

## Discovery Process

### 1. Requirement Identification
- Define specific workflow constraints
- Identify language requirements
- Determine team size and collaboration patterns
- Assess CI/CD integration needs
- Evaluate performance requirements

### 2. Solution Validation
- Test tools against real-world scenarios
- Measure performance metrics
- Validate configuration complexity
- Assess adoption friction
- Verify ecosystem compatibility

### 3. Perfect Matching
- Align tool capabilities with requirements
- Identify configuration approaches
- Document integration patterns
- Map migration paths
- Define success criteria

## Use Case Categories

### Python Library Development
Requirements: Pure Python formatting, package compatibility, minimal configuration

### Full-Stack TypeScript Application
Requirements: Unified formatting, framework support, developer experience

### Python + JavaScript Monorepo
Requirements: Multi-language support, consistent styling, toolchain coordination

### Legacy Codebase Migration
Requirements: Incremental adoption, backwards compatibility, minimal disruption

### CI/CD Pipeline Optimization
Requirements: Speed, caching, parallelization, minimal resource usage

## Evaluation Criteria

### Performance
- Format speed (lines/second)
- Parse overhead
- Cache effectiveness
- Parallel execution support

### Configuration
- Zero-config defaults
- Customization depth
- Migration complexity
- Team alignment

### Integration
- Pre-commit hook support
- CI/CD platform compatibility
- Editor/IDE integration
- Git workflow integration

### Ecosystem
- Community size
- Plugin availability
- Framework support
- Long-term maintenance

## Success Metrics

### Adoption Success
- Time to first format < 5 minutes
- Team agreement on configuration < 1 day
- Zero formatting debates after adoption

### Performance Success
- CI formatting check < 30 seconds for medium codebases
- Local format-on-save < 200ms
- Pre-commit hook < 2 seconds

### Maintenance Success
- Configuration changes < 2 per year
- Tool updates cause zero breaking changes
- Onboarding new developers < 15 minutes

## Anti-Patterns

### Over-Configuration
Custom rules that conflict with tool philosophy create maintenance burden

### Multi-Tool Overlap
Running multiple formatters on same files causes conflicts

### Inconsistent Enforcement
Optional formatting creates style debates and PR friction

### Performance Ignorance
Slow formatters block developers and waste CI resources

## Decision Framework

1. Identify primary language(s)
2. Determine configuration philosophy (opinionated vs flexible)
3. Evaluate performance requirements
4. Assess team size and collaboration patterns
5. Select tool with best requirement alignment
6. Validate through pilot implementation
7. Document and enforce standards

## Date Compiled
December 4, 2025
