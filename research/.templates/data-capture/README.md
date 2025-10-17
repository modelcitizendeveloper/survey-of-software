# Structured Data Capture Templates

**Purpose**: Templates for capturing structured data during MPSE research

**Version**: MPSE v3.0 Enhancement
**Date**: October 17, 2025

---

## Overview

These templates enable **parallel** capture of structured JSON data alongside narrative markdown during research. This provides:

✅ **Data lineage** - Track every fact to its source (URL, timestamp, LLM attribution)
✅ **Vendor gaming detection** - Identify pricing changes, suspicious patterns
✅ **Explainability** - Answer "where did this fact come from?"
✅ **Queryability** - Enable database queries across all research
✅ **No conversion debt** - Don't accumulate items needing later conversion

---

## When to Use

### ALWAYS use for:
- ✅ **Tier 3** (Managed Services) - Highest vendor gaming risk
- ✅ **Research with quantified metrics** (costs, hours, percentages)
- ✅ **Comparison-heavy research** (Provider A vs Provider B)

### Optional for:
- ⚠️ **Tier 2** (Open Standards) - Standards comparison benefits from structure
- ⚠️ **Tier 1** (Libraries) - Lower vendor gaming risk, simpler structure

### Skip for:
- ❌ **Purely narrative research** (no structured facts)
- ❌ **Exploratory investigations** (structure not yet known)

---

## Template Inventory

### Tier 3 (Managed Services)

| Template | Purpose | When to Fill | Typical Time |
|----------|---------|--------------|--------------|
| **provider_template.json** | Provider details, pricing, lock-in | S1-S2, per provider | 10-15 min |
| **section0_standards_assessment_template.json** | Does Tier 2 standard exist? | Section 0 | 10-15 min |
| **cost_comparison_template.json** | 3-year TCO (Path 1/2/3) | S2-S3 | 15-20 min |
| **migration_scenario_template.json** | Migration effort, gotchas | S2-S3, per scenario | 10-15 min |
| **vendor_risk_template.json** | Acquisition risk, pricing trajectory | S4 Strategic | 15-20 min |

**Total incremental effort**: +1.5-3 hours per full MPSE research (10-20% overhead)

### Tier 2 (Open Standards)

*Coming soon - standards comparison, backend compatibility matrices*

### Tier 1 (Libraries)

*Coming soon - library feature matrices, performance benchmarks*

---

## Workflow

### Option A: Sequential (Current Process)
1. Do research → Write markdown
2. **Later**: Convert markdown → JSON (45-60 min per item)

**Pros**: Familiar workflow
**Cons**: Conversion debt accumulates, data lineage lost

### Option B: Parallel (Recommended) ⭐
1. Do research → **Fill JSON templates + write markdown simultaneously**
2. **No conversion** needed later

**Pros**: Data lineage captured at source, no debt, higher quality
**Cons**: +10-20% time overhead after learning curve

### Learning Curve:
- **First 2-3 items**: +30-40% overhead (learning templates)
- **Next 5-10 items**: +20-25% overhead (getting efficient)
- **After 10+ items**: +10-15% overhead (becomes natural)

---

## Usage Instructions

### Step 1: Create data/ Directory

```bash
research/X.XXX-research-name/
├── data/
│   ├── section0/          # Section 0 standards assessment
│   ├── providers/         # One JSON per provider
│   ├── comparisons/       # Cost comparisons, feature matrices
│   └── migrations/        # Migration scenarios
```

### Step 2: Copy Templates

**As you discover each provider** (S1 Rapid, S2 Comprehensive):
```bash
cp research/.templates/data-capture/tier3/provider_template.json \
   research/X.XXX-research-name/data/providers/provider_name.json
```

**During Section 0**:
```bash
cp research/.templates/data-capture/tier3/section0_standards_assessment_template.json \
   research/X.XXX-research-name/data/section0/standards_assessment.json
```

**During S2-S3 (cost analysis)**:
```bash
cp research/.templates/data-capture/tier3/cost_comparison_template.json \
   research/X.XXX-research-name/data/comparisons/cost_comparison.json
```

**During S2-S3 (migration scenarios)**:
```bash
cp research/.templates/data-capture/tier3/migration_scenario_template.json \
   research/X.XXX-research-name/data/migrations/provider_a_to_provider_b.json
```

**During S4 Strategic**:
```bash
cp research/.templates/data-capture/tier3/vendor_risk_template.json \
   research/X.XXX-research-name/data/providers/provider_name_risk.json
```

### Step 3: Fill Templates During Research

**Key principle**: Fill JSON **as you discover facts**, not after research complete

**Examples**:
- When you see "$25/month" on a pricing page → Add to `pricing.paid_tiers`
- When you read "8-20 hours migration" in docs → Add to migration scenario
- When LLM generates provider comparison → Record `llm_attribution`

### Step 4: Data Lineage (CRITICAL)

**Always capture**:
- ✅ **Source URL** + timestamp when accessed
- ✅ **LLM attribution** (model, response ID) if LLM-generated
- ✅ **Credibility** (first_party, second_party, third_party)
- ✅ **Method** (manual_research, llm_extraction, web_scraping)

**Example**:
```json
"data_lineage": {
  "source_urls": [
    {
      "url": "https://neon.tech/pricing",
      "accessed_at": "2025-10-17T10:30:00Z",
      "purpose": "Pricing information",
      "status_code": 200
    }
  ],
  "llm_attribution": {
    "model": "claude-sonnet-3.5",
    "response_id": "msg_abc123",
    "timestamp": "2025-10-17T10:30:00Z"
  },
  "credibility": "first_party"
}
```

---

## Quality Checklist

Before finalizing research, verify:

- [ ] Can I query: "Which providers cost <$50/month?" → Check cost_comparison.json
- [ ] Can I query: "Which migrations take <20 hours?" → Check migration scenarios
- [ ] Can I trace: "Where did this $25/month figure come from?" → Check data_lineage.source_urls
- [ ] Can I detect: "Did Supabase pricing change since last check?" → Check pricing.accessed_at
- [ ] Are all URLs accessible? → Check status_code fields
- [ ] Are all LLM responses attributed? → Check llm_attribution fields
- [ ] Are ranges used for uncertainty? → Check hours_min/max, cost_min/max

---

## Integration with MPSE Phases

### S1 Rapid Discovery
**JSON to capture**:
- `providers/provider_name.json` for each discovered provider (10 min each)
- Basic pricing, features, URLs

**Incremental effort**: +15-30 minutes total

### S2 Comprehensive Discovery
**JSON to capture**:
- Complete provider details (fill remaining fields)
- `comparisons/cost_comparison.json` (20 min)
- `migrations/*.json` for key migration paths (15 min each)

**Incremental effort**: +45-90 minutes total

### S3 Need-Driven Discovery
**JSON to capture**:
- Use case → provider mappings (can be added to provider files)
- Scenario-specific cost breakdowns

**Incremental effort**: +20-40 minutes total

### S4 Strategic Discovery
**JSON to capture**:
- `providers/*_risk.json` vendor risk assessments (20 min each)
- Pricing trajectory, acquisition probability

**Incremental effort**: +40-80 minutes total

**Total**: +2-4 hours over complete MPSE research (10-20% overhead)

---

## Example: Real Usage

See `research/3.040-database-services/data/` for complete example:
- ✅ 3 providers captured (Supabase, Neon, Railway)
- ✅ Section 0 standards assessment
- ✅ Cost comparison (Path 1/2/3)
- ✅ 2 migration scenarios
- ✅ Full data lineage

**Time invested**: 45-60 minutes
**Coverage**: ~30% of complete research (representative sample)

---

## Migration from Existing Research

**Don't convert everything at once** - Use phased approach:

**Phase 1**: High-priority Tier 3 items (5 items, ~4 hours)
- Items with highest vendor gaming risk
- Items with quantified metrics

**Phase 2**: Remaining Tier 3 + high-value Tier 1/2 (15-20 hours)
- Use LLM-assisted extraction
- Validate with manual review

**Phase 3**: Bulk conversion with tooling (TBD)
- Automated extraction from markdown
- SQLite database generation

---

## Future Enhancements

**Coming soon**:
1. **Tier 2 templates** - Standards comparison, backend compatibility
2. **Tier 1 templates** - Library benchmarks, feature matrices
3. **LLM prompts** - Auto-generate JSON from research
4. **Validation scripts** - Schema checking, URL validation
5. **Query examples** - Common vendor gaming detection queries

---

## Questions?

See:
- `research/3.040-database-services/data/CONVERSION_ASSESSMENT.md` - Full LoE analysis
- `applications/research-lineage-system/` - Business case and technical requirements
- `frameworks/MPSE_V2.md` - MPSE methodology documentation

**Bottom line**: Structured data capture adds 10-20% overhead but provides:
- Data lineage (explainability)
- Vendor gaming detection
- Queryability across all research
- No conversion debt

**ROI**: $187K-231K over 3 years vs $12K-18K investment = 10-19x return
