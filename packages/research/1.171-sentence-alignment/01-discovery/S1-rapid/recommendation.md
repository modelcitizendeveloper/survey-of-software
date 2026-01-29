# S1 Recommendation: Quick Decision Guide

## TL;DR Comparison

| Tool | Best For | Speed | Accuracy | Setup Complexity |
|------|----------|-------|----------|------------------|
| **Hunalign** | Large-scale MT pipelines | ⚡⚡⚡ Very Fast | 85-95% | Low |
| **Bleualign** | High-accuracy, divergent texts | ⚡ Slow | 90-98% | Medium (needs MT) |
| **vecalign** | Multilingual, low-resource | ⚡⚡ Moderate | 93-99% | Medium-High |

## Decision Tree

### Choose **Hunalign** if:
✅ You need maximum speed for large corpora
✅ You have clean, well-formed parallel texts
✅ You have or can create bilingual dictionaries
✅ You're building an MT data preprocessing pipeline
✅ You need a proven, stable tool with minimal dependencies

**Skip Hunalign if:** You're dealing with paraphrases or highly divergent translations

### Choose **Bleualign** if:
✅ Accuracy is more important than speed
✅ Your texts have significant reordering or paraphrasing
✅ You already have MT infrastructure (API or local)
✅ You're working with research-quality alignments
✅ Your parallel texts have length mismatches

**Skip Bleualign if:** You don't have access to MT or need to process millions of sentences quickly

### Choose **vecalign** if:
✅ You're working with low-resource or rare language pairs
✅ You need state-of-the-art accuracy
✅ You have GPU resources available
✅ You're handling multiple language pairs (multilingual project)
✅ Your text is noisy (web-crawled, OCR, informal)
✅ You want language-agnostic solution

**Skip vecalign if:** You're on CPU-only with simple European language pairs

## Common Use Cases

### MT Training Data Preparation (Large Scale)
**Recommendation**: **Hunalign**
*Rationale*: Speed and reliability matter most; quality filtering happens downstream

### Building High-Quality Parallel Corpus
**Recommendation**: **vecalign** (GPU) or **Bleualign** (with MT)
*Rationale*: Accuracy is paramount; can afford slower processing

### Multilingual Content Management
**Recommendation**: **vecalign**
*Rationale*: Single tool for all language pairs; no per-language resources needed

### Academic/Research Alignments
**Recommendation**: **Bleualign** or **vecalign**
*Rationale*: Published benchmarks, reproducible, highest accuracy

### Production Pipeline (Fast Turnaround)
**Recommendation**: **Hunalign**
*Rationale*: Minimal dependencies, predictable performance, battle-tested

## Next Steps

- **S2 (Comprehensive)**: Deep dive into algorithms, parameter tuning, edge cases
- **S3 (Need-Driven)**: Specific workflows for common scenarios
- **S4 (Strategic)**: Combining tools, quality assessment, production deployment
