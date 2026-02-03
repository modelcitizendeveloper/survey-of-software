# S3: Need-Driven Discovery Approach

## Core Philosophy

**"Requirements first, then find exact fits"**

The need-driven methodology inverts the traditional technology evaluation process. Instead of surveying available libraries and comparing features, we start with concrete business problems and derive precise technical requirements. Only after requirements are crystallized do we search for solutions that match perfectly.

## Why Need-Driven for Cryptography?

Cryptographic library selection is particularly suited to need-driven discovery because:

1. **Security through minimalism**: Extra features = expanded attack surface
2. **Compliance precision**: FIPS/SOC2/GDPR have specific algorithmic requirements
3. **Performance constraints**: Real applications have concrete throughput/latency needs
4. **Integration reality**: Libraries must fit existing authentication/storage systems
5. **Maintenance burden**: Unused capabilities still require security updates

Over-engineering in cryptography is dangerous. A "comprehensive" library with 50 algorithms when you need 3 creates unnecessary risk.

## Discovery Process

### Phase 1: Use Case Extraction (Real Problems)
- Start with concrete application scenarios
- Document existing systems and constraints
- Identify security threats specific to each use case
- Define success criteria (performance, compliance, usability)

**Example**: Instead of "need encryption", specify:
- "Encrypt 10,000 PII database fields, avg 50 bytes each"
- "Decrypt fields in <5ms for web request response"
- "Support key rotation without full re-encryption"
- "GDPR Article 32 technical safeguards compliance"

### Phase 2: Requirement Specification (Precise Needs)
For each use case, define:
- **Cryptographic primitives required** (AES-256-GCM, not just "encryption")
- **Performance requirements** (quantified: ops/sec, latency percentiles)
- **Compliance mandates** (specific standards: FIPS 140-2 Level 1)
- **Integration constraints** (Python version, existing auth systems)
- **Security properties** (authenticated encryption, forward secrecy)

### Phase 3: Solution Mapping (Find Exact Fits)
- Search for libraries providing ONLY required primitives
- Validate each requirement through testing
- Measure actual performance against requirements
- Check compliance certifications (FIPS validation numbers)
- Assess maintenance status and security response history

### Phase 4: Gap Analysis (What's Missing?)
- Identify requirements no library satisfies
- Determine if gaps are acceptable (workarounds)
- Flag over-provisioned features (bloat)
- Document tradeoffs explicitly

### Phase 5: Minimum Sufficient Solution
- Select library meeting all MUST-HAVE requirements
- Prefer minimal feature set over comprehensive
- Validate through proof-of-concept implementations
- Verify compliance through actual testing

## Key Principles

### 1. Specificity Over Generality
Bad: "Need encryption for data at rest"
Good: "Encrypt 500GB PostgreSQL database with column-level AES-256-GCM, supporting 10K decryptions/sec"

### 2. Validation Over Specification
Don't trust documentation. Write test code:
- Measure actual encryption throughput
- Test key rotation procedures
- Verify FIPS mode actually works
- Check API usability with real code

### 3. Constraints Are Assets
"Must work with Django 4.2" or "Cannot require C compiler" are positive constraints that narrow the solution space effectively.

### 4. No Premature Generalization
Don't select a library "in case we need quantum-resistant crypto someday." Solve today's problems. Re-evaluate when new needs emerge.

### 5. Fit Scoring
Quantify requirement-solution matching:
- Each MUST-HAVE requirement: +10 points if met, -1000 if not
- Each NICE-TO-HAVE: +1 point if met
- Each unnecessary feature: -1 point (bloat penalty)
- Security incident history: -5 per CVE in last 2 years
- Maintenance frequency: +2 if updated in last 3 months

## Deliverables

1. **Use Case Documents**: Concrete scenarios with specific requirements
2. **Requirement Matrix**: Which libraries satisfy which use cases
3. **Validation Tests**: Proof-of-concept code proving fit
4. **Gap Report**: What's missing or over-provisioned
5. **Minimum Sufficient Recommendation**: Best-fit solution with justification

## Anti-Patterns to Avoid

- **Feature comparison tables**: Leads to feature creep
- **"Best practices" shopping lists**: Generic advice without context
- **Vendor benchmarks**: Use your own performance tests
- **Future-proofing**: Over-engineer for hypothetical needs
- **Consensus-driven**: "Everyone uses X" ignores your specific needs

## Success Criteria

A successful need-driven analysis produces:
- Clear traceability: requirement → test → library choice
- Minimal solution: No unused major features
- Validated claims: Performance/compliance verified through testing
- Risk transparency: Known gaps explicitly documented
