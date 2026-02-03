# S3: Need-Driven Discovery Approach

## Methodology Overview

S3 Need-Driven Discovery follows a "requirements first, then find exact fits" philosophy. This approach starts by decomposing generic use case patterns into precise technical requirements, then systematically matches Python libraries against those requirements.

## Core Philosophy: Hardware Store for Software

Like finding the right tool in a hardware store, we:
1. Define the job to be done (generic use case pattern)
2. Specify requirements (what capabilities are needed)
3. Evaluate candidate tools (which libraries fit)
4. Validate fit (does it solve the pattern elegantly?)

This is NOT about finding libraries and then inventing use cases. It's about understanding common patterns developers face and identifying which tools solve them best.

## Use Case Pattern Decomposition

### Step 1: Pattern Identification
We identified 6 fundamental Monte Carlo patterns that span multiple domains:

1. **Sensitivity Analysis Pattern**: Which inputs matter most?
2. **Confidence Interval Pattern**: What are statistical bounds on predictions?
3. **Risk Quantification Pattern**: What's the probability of meeting goals?
4. **Uncertainty Propagation Pattern**: How does input uncertainty affect outputs?
5. **Model Calibration Pattern**: How to fit uncertain model parameters to data?
6. **Distribution Characterization Pattern**: What does the output distribution look like?

### Step 2: Requirement Extraction
For each pattern, we extract:
- **Functional requirements**: What computation must be performed?
- **Performance requirements**: How fast/scalable must it be?
- **Usability requirements**: How easy should implementation be?
- **Integration requirements**: What data structures/frameworks must it work with?

### Step 3: Parameterization
Each pattern is parameterized by:
- **D**: Number of input parameters/dimensions
- **N**: Number of Monte Carlo samples/replications
- **model_complexity**: Computational cost of single evaluation
- **output_dimensionality**: Scalar vs. vector vs. multivariate outputs

This parameterization allows developers to map their specific problem onto the generic pattern.

## Library Matching Methodology

### Candidate Library Identification
We evaluate libraries across three tiers:

**Tier 1: Foundation Libraries**
- NumPy/SciPy: Core statistical distributions and array operations
- Requirements: Always needed, provides base functionality

**Tier 2: Specialized Monte Carlo Libraries**
- SALib: Sensitivity analysis focused
- UncertaintyQuantification/Chaospy: Uncertainty propagation
- PyMC/emcee: Bayesian parameter estimation

**Tier 3: Domain-Specific Extensions**
- DES libraries (SimPy): Discrete event simulation
- Financial libraries (QuantLib): Options pricing
- Engineering libraries (OpenTURNS): Structural reliability

### Requirement Matching Process

For each use case pattern:

1. **List explicit requirements**:
   - "Must support arbitrary parameter distributions"
   - "Must calculate Sobol indices for D > 100"
   - "Must handle correlated inputs"
   - "Must integrate with existing model code"

2. **Evaluate each library**:
   - ✓ Full support (native functionality)
   - ○ Partial support (requires workaround)
   - ✗ No support (fundamental gap)

3. **Score overall fit**:
   - Perfect fit: All requirements met natively
   - Good fit: Core requirements met, minor gaps acceptable
   - Poor fit: Significant requirements unmet

### Gap Identification

We explicitly identify:
- **Capability gaps**: Requirements no library satisfies well
- **Efficiency gaps**: Requirements satisfied but inefficiently
- **Usability gaps**: Requirements satisfied but with poor developer experience

## Validation Approach

### Template Validation
Each use case pattern includes a generic code template validated for:

1. **Correctness**: Does it produce statistically valid results?
2. **Generality**: Can developers easily adapt it to their domain?
3. **Clarity**: Are placeholder parameters obvious to replace?
4. **Completeness**: Does it include all steps (setup, execution, analysis)?

### Multi-Domain Examples
For each pattern, we provide 3-5 examples across different domains showing:
- How to map domain problem onto generic pattern
- What parameters to use (D, N, distributions)
- What libraries fit best for that domain's characteristics

### Performance Characterization
We characterize when each library is appropriate based on:
- **Problem scale**: D < 10 (small), 10 ≤ D ≤ 100 (medium), D > 100 (large)
- **Evaluation cost**: Fast (< 1ms), Medium (1ms-1s), Slow (> 1s)
- **Developer experience**: Beginner, Intermediate, Advanced

## Methodology Independence

This analysis is performed in complete isolation from other discovery methods (S1, S2, S4). We:
- Do NOT reference other methodologies' findings
- Do NOT attempt to coordinate or reconcile approaches
- Focus solely on requirement-driven library matching
- Make recommendations based purely on fit analysis

The goal is authentic S3 methodology application, not a hybrid approach.

## Output Structure

### approach.md (this file)
Documents the S3 methodology and how it was applied.

### use-case-pattern-X.md files
One file per generic pattern containing:
- Pattern definition and parameterization
- Requirement breakdown
- Library fit analysis
- Generic code template
- Multi-domain examples

### recommendation.md
Synthesis across all patterns:
- Best-fit recommendations per pattern
- Decision trees based on parameters (D, N, complexity)
- Gap analysis across all patterns
- Integration patterns when combining use cases

## Key Differentiators of S3 Approach

1. **Requirements-first**: We start with what developers need, not what libraries exist
2. **Pattern-based**: We organize by problem pattern, not by library feature
3. **Parameterized**: Generic patterns allow mapping from any specific problem
4. **Multi-domain**: Examples across 5+ domains prove generality
5. **Gap-aware**: We explicitly identify what's NOT well supported

This approach serves developers searching for "How do I solve X?" rather than "What can library Y do?"
