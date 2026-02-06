# S3: Need-Driven Discovery Approach

## Methodology
Start with specific use cases and requirements, then find exact-fit solutions. Validation-focused: "Does this solve my actual problem?"

## Time Budget
20 minutes

## Discovery Process
1. **Define concrete use cases** with specific CJK requirements
2. **List must-have vs nice-to-have** features
3. **Test candidate solutions** against requirements
4. **Identify gaps** where no solution fully satisfies
5. **Recommend best fit** per use case

## Selection Criteria
- **Requirement satisfaction** - All must-haves met?
- **Implementation complexity** - Days vs weeks vs months?
- **Constraints respected** - License, dependencies, platform?
- **Use-case fit** - Solves the specific problem, not just "good in general"

## Use Cases Explored

### 1. API Service (Chinese Q&A)
**Profile:** High volume, cost-sensitive, Chinese-primary
**Key requirement:** Low token count to reduce API costs

### 2. Multilingual Code Documentation
**Profile:** English + Chinese comments in code
**Key requirement:** Balanced tokenization, good code handling

### 3. Training Custom Chinese LLM
**Profile:** Domain-specific vocabulary (medical/legal)
**Key requirement:** Full training control, optimize for domain

### 4. Real-Time Translation Service
**Profile:** Low latency, streaming, Chinese ↔ English
**Key requirement:** Fast inference, good quality both languages

### 5. Mobile App (Offline)
**Profile:** Limited resources, Japanese text input
**Key requirement:** Small model size, fast on mobile CPU

## Evaluation Framework

For each use case, score candidates on:
- ✅ Fully satisfies requirement
- ⚠️ Partially satisfies (workaround needed)
- ❌ Does not satisfy
- N/A Not applicable to this use case

## Key Questions Per Use Case
- What's the performance budget?
- What's the cost budget?
- What's the implementation timeline?
- What are the constraints (platform, dependencies)?
- What languages are involved?
- What's the text domain/style?
