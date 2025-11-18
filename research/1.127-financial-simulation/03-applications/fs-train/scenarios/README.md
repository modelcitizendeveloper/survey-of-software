# Training Scenarios for fs-train

## Overview

Synthetic financial scenarios designed to teach financial analysis fluency through progressive difficulty.

## Scenario Structure

Each scenario is a YAML file containing:
- Company context (industry, stage, funding)
- 3 months of financial data
- Key insights (ground truth for scoring)
- Prompts and suggested views
- Expected score ranges by skill level

## Scenarios

### Beginner (Learn Core Concepts)

**001: Simple Growth**
- **Concept**: Healthy revenue growth with stable margins
- **Key Learning**: Revenue trends, gross margin, profitability
- **Difficulty**: ⭐ Beginner
- **Duration**: 2-3 minutes

**002: Margin Compression**
- **Concept**: Flat revenue but rising COGS = margin squeeze
- **Key Learning**: COGS impact on margins, unit economics
- **Difficulty**: ⭐ Beginner
- **Duration**: 3-4 minutes

### Intermediate (Understand Trade-offs)

**003: Growth with Hiring**
- **Concept**: Invest in growth (hire first, revenue follows)
- **Key Learning**: Profitability trade-offs, strategic investment
- **Difficulty**: ⭐⭐ Intermediate
- **Duration**: 4-5 minutes

**004: Cash Flow Crisis**
- **Concept**: Profitable on paper but running out of cash
- **Key Learning**: Cash vs accrual accounting, AR timing, working capital
- **Difficulty**: ⭐⭐ Intermediate
- **Duration**: 5-6 minutes

### Advanced (Nuanced Analysis)

**005: Seasonal Patterns**
- **Concept**: Don't confuse seasonality with permanent decline
- **Key Learning**: Industry patterns, YoY comparisons, context matters
- **Difficulty**: ⭐⭐⭐ Advanced
- **Duration**: 6-8 minutes

## Recommended Learning Path

### Week 1: Fundamentals
1. **001: Simple Growth** - Learn to spot trends
2. **002: Margin Compression** - Understand efficiency

### Week 2: Complexity
3. **003: Growth with Hiring** - Investment trade-offs
4. **004: Cash Flow Crisis** - Cash vs profit

### Week 3: Nuance
5. **005: Seasonal Patterns** - Context and patterns

## Scoring Guide

**Beginner Level**:
- 30-50 points: Catch 2-3 major insights
- Surface exploration (default view + 1-2 others)
- Time: 2-3 minutes

**Intermediate Level**:
- 50-75 points: Catch 4-5 insights with some connections
- Multiple view exploration
- Time: 3-5 minutes

**Advanced Level**:
- 75-100 points: Catch 6+ insights, strategic thinking
- Deep exploration with custom comparisons
- Time: 5-8 minutes

## Key Concepts Taught

### Financial Metrics
- Revenue growth (MoM, YoY)
- Gross margin
- Operating margin
- Cash burn rate
- Runway

### Operational Patterns
- Hiring impacts
- Marketing efficiency (CAC)
- Unit economics
- Operating leverage

### Strategic Thinking
- Growth vs profitability trade-offs
- Investment timing
- Sustainability analysis
- Industry context

### Cash Management
- Cash vs profit
- Working capital
- AR/AP timing
- Runway calculation

## Future Scenarios (Planned)

**006: Product Mix Shift** (Advanced)
- Changing revenue composition
- Margin implications

**007: Multiple Issues** (Advanced)
- Several problems at once
- Prioritization needed

**008: Geographic Expansion** (Advanced)
- New market investment
- Upfront costs vs future revenue

**009: Pricing Change** (Intermediate)
- Price increase impact
- Volume vs margin trade-off

**010: Competitive Pressure** (Advanced)
- Market share loss
- Strategic response needed

## Usage

```bash
# Run specific scenario
fs-train scenarios/001_simple_growth.yaml

# Run all beginner scenarios
fs-train scenarios/ --difficulty beginner

# Practice mode (no scoring, just exploration)
fs-train scenarios/003_growth_hiring.yaml --practice
```

## Contributing New Scenarios

To add a new scenario:

1. Copy template from existing scenario
2. Create realistic 3-month financial data
3. Define 5-7 key insights with point values
4. Add prompts for different skill levels
5. Test with users at target difficulty level
6. Update this README

## Data Sources

All scenarios use **synthetic data** designed to teach specific concepts.

Real company data may be added in future versions with:
- Public company 10-K/10-Q data
- Anonymized startup metrics
- Industry benchmark comparisons
