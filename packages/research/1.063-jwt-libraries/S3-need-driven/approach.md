# S3: Need-Driven Discovery Methodology

## Core Philosophy

Requirements first, then find exact fits. Define precise needs before exploring solutions.
Avoid solution-driven thinking where we pick popular tools and justify their features.

## Discovery Process

### Phase 1: Use Case Definition (Reality-Based)
- Start with concrete scenarios from actual systems
- Define what users/systems are trying to accomplish
- Identify constraints (performance, security, deployment)
- Document failure modes and edge cases
- NO reference to existing libraries yet

### Phase 2: Requirement Extraction (Precision)
- Convert use cases into measurable requirements
- Separate MUST-HAVE from NICE-TO-HAVE
- Define acceptance criteria for each requirement
- Specify validation tests to verify fit
- Quantify performance/security thresholds

### Phase 3: Solution Mapping (Fit Analysis)
- Survey available libraries (PyJWT, python-jose, authlib, jwcrypto)
- Test each library against specific requirements
- Document gaps where libraries don't meet needs
- Avoid "close enough" - measure exact fit
- Identify bloat (features we don't need that add complexity)

### Phase 4: Gap Assessment (Honesty)
- Where do libraries over-deliver? (unnecessary complexity)
- Where do libraries under-deliver? (missing critical features)
- Can gaps be filled with minimal additional code?
- What are the costs of feature-rich libraries we don't fully use?

### Phase 5: Minimum Sufficient Solution
- Pick library that satisfies requirements with minimal bloat
- Prefer simple, focused tools over Swiss Army knives
- Validate choice through actual implementation tests
- Document tradeoffs explicitly

## Key Principles

1. **Requirements Before Research**: Define what you need before looking at what exists
2. **Perfect Fit Over Features**: A library with 10 features you need beats one with 100 features (5 needed, 95 bloat)
3. **Validation Testing**: Don't trust documentation - test libraries against actual requirements
4. **Gap Transparency**: Acknowledge when no library perfectly fits
5. **Avoid Over-Engineering**: Resist feature creep from seeing what libraries offer
6. **Use-Case Driven**: Each use case may need different libraries - no universal solution

## Anti-Patterns to Avoid

- Starting with "What does PyJWT offer?" instead of "What do we need?"
- Justifying library choice by listing all its features
- Picking the most popular/feature-rich library by default
- Adding requirements because a library makes them easy
- Ignoring complexity costs of unused features

## Success Criteria

A successful analysis will:
- Define requirements independently of solutions
- Map requirements to libraries with test validation
- Identify specific gaps and bloat for each option
- Recommend minimum sufficient solution for each use case
- Acknowledge when multiple libraries are needed for different scenarios

## JWT-Specific Methodology Application

### Use Case First
- REST API authentication (stateless tokens)
- OAuth 2.0 / OIDC integration (standard claims)
- Microservice authentication (service-to-service)
- SPA authentication (refresh token patterns)

### Requirements Per Use Case
- Algorithm requirements (HS256 vs RS256 vs ES256)
- Validation needs (signature, expiration, custom claims)
- Performance constraints (tokens/second)
- Security requirements (vulnerability history, audit trail)
- Integration points (existing crypto libraries)

### Testing Methodology
- Create minimal test implementations for each use case
- Measure lines of code needed with each library
- Test against malformed/expired/invalid tokens
- Validate RFC 7519 compliance with test vectors
- Check for CVE history and security practices

### Decision Framework
- Does library satisfy all MUST-HAVE requirements? (yes/no)
- How many NICE-TO-HAVE requirements satisfied? (count)
- How much bloat? (unused features that add dependencies/complexity)
- What are integration costs? (learning curve, boilerplate)
- What are maintenance risks? (activity, breaking changes)

This methodology ensures we select libraries that solve our actual problems,
not libraries that impress us with features we don't need.
