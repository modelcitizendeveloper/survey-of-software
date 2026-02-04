# S1: Rapid Discovery - Approach

**Methodology**: Rapid Library Search (speed-focused)
**Time Box**: 60-90 minutes maximum
**Goal**: Identify clear winner for personal language learning use case (80/20 answer)

## Core Philosophy

Get the fastest useful answer. Prioritize:
- What's most popular/widely used?
- What has active maintenance?
- What's easiest to implement?
- Is there obvious consensus?

## Discovery Process

### 1. Algorithm Landscape Scan (15 min)
- Identify major algorithms: SM-2, FSRS, SM-18, Leitner
- Understand basic differences
- Historical adoption patterns

### 2. Python Implementation Search (20 min)
- PyPI search: "spaced repetition", "sm2", "fsrs"
- GitHub search: Popular repositories
- Check: Last commit, stars, downloads, maintainers

### 3. Rapid Validation (20 min)
- Does it install cleanly? (`pip install`)
- Is documentation clear?
- Can I run basic example in <5 minutes?

### 4. Popularity Signals (10 min)
- PyPI download counts (pypistats.org)
- GitHub stars/forks
- Anki community consensus (r/Anki)
- Stack Overflow mentions

### 5. Quick Recommendation (10 min)
- Default choice for 90% of learners
- When to consider alternatives
- Confidence level + reasoning

## Evaluation Criteria

**Primary**: Popularity + ease of implementation
**Secondary**: Active maintenance + documentation quality
**Tertiary**: Performance (if obviously problematic)

## Output Files

- `approach.md` (this file)
- `sm2.md` - SM-2 algorithm implementations
- `fsrs.md` - FSRS algorithm implementations
- `sm18.md` - SM-18 algorithm implementations (if Python impl exists)
- `leitner.md` - Leitner system implementations (if Python impl exists)
- `recommendation.md` - Final rapid choice

## Success Criteria

- Found viable Python implementations (3+ options)
- Clear popularity leader identified
- Can answer: "What should I use for my language learning app?"
- Total time: <90 minutes
