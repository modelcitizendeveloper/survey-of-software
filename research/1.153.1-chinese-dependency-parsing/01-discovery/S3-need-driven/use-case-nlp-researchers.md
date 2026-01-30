# Use Case: NLP Researchers Building Chinese Language Models

## Who Needs This

**User Persona**: Computational linguistics PhD students and postdocs researching Chinese syntax, semantics, or cross-lingual NLP.

**Organization Context**:
- Academic research labs (universities)
- Independent researchers
- Industrial research teams (Google AI, Meta AI, etc.)

**Technical Background**:
- Strong Python and PyTorch/TensorFlow skills
- Understanding of dependency grammar and Universal Dependencies
- Experience with NLP benchmarking and evaluation

**Scale**: Individual researchers or small teams (2-5 people)

## Why They Need Dependency Parsing

### Primary Goals

**Benchmarking**: Evaluate new models against established baselines
- Need reproducible results on standard test sets (UD Chinese-GSD, CTB)
- Require exact comparison to published papers

**Feature Extraction**: Use dependency structures as features
- Train downstream models (relation extraction, semantic parsing)
- Analyze linguistic phenomena (word order, argument structure)

**Model Development**: Build improved dependency parsers
- Test new neural architectures (graph neural networks, transformers)
- Experiment with cross-lingual transfer learning

### Success Criteria

- Reproducible benchmarks (same test sets as literature)
- Comparison to state-of-the-art (can cite published UAS/LAS scores)
- Training pipeline flexibility (can modify architectures, loss functions)
- Standard output format (CoNLL-U for tool compatibility)

## Requirements and Constraints

### Technical Requirements

**Must-have**:
- UD-native output (standard format for reproducibility)
- Pretrained baseline models (comparison point)
- Custom training support (for novel architectures)
- Clear evaluation protocol (CoNLL 2018 script compatible)

**Nice-to-have**:
- Multiple pretrained models (compare different approaches)
- Cross-lingual models (zero-shot evaluation)
- Model interpretability tools (error analysis)

### Resource Constraints

**Compute**:
- GPU access (university clusters, Google Colab, cloud credits)
- Limited budget (prefer open-source, avoid commercial APIs)

**Time**:
- Rapid iteration (quick experiments, fast training)
- Reproducibility (can reproduce results months later)

**Skills**:
- Expert level (can read papers, modify code)
- Prefer well-documented training procedures

## Library Recommendation

### Primary Choice: **Stanza**

**Why Stanza**:

1. **UD-native design**: Trained and evaluated on UD treebanks
   - Benchmarks directly comparable to ACL/EMNLP/COLING papers
   - Same evaluation protocol as CoNLL shared tasks

2. **Stanford credibility**: Academic provenance matters for citations
   - Papers using Stanza widely accepted in NLP community
   - Regular updates aligned with UD releases (v2.12, v2.13, etc.)

3. **Reproducibility**: Clear versioning and model provenance
   - `stanza.download('zh', version='1.5.1')` locks to specific models
   - Training scripts and hyperparameters documented

4. **Training documentation**: Comprehensive guides for custom models
   - Step-by-step training tutorials
   - Clear data format requirements (CoNLL-U)
   - Hyperparameter recommendations

5. **Baseline comparisons**: Extensive benchmarks published
   - Performance page shows scores on UD test sets
   - Can directly compare custom model to Stanza baseline

**Implementation Considerations**:

- Use Stanza's published scores as baseline (cite Qi et al. 2020)
- Train custom models following official training guide
- Evaluate with CoNLL 2018 script for standard metrics (UAS/LAS)
- Publish results with Stanza version, UD treebank version for reproducibility

### Alternative: **HanLP** (for specific research questions)

**When to choose HanLP instead**:

**Semantic dependency research**:
- Investigating Chinese semantic role labeling
- Comparing syntactic vs semantic structures
- Analyzing topic-comment phenomena

**Multilingual transfer learning**:
- Cross-lingual parser transfer (Chinese ↔ other languages)
- HanLP 2.1 supports 130+ languages (wider than Stanza's 80)

**Multi-task learning research**:
- Studying joint training of segmentation + POS + parsing
- Investigating task synergies in Chinese NLP

**Trade-off**: HanLP benchmarks less standardized (uses Stanford Dependencies 3.3.0, custom CTB splits) → harder to compare to literature.

### Why Not LTP

**Reasons to avoid**:
- Smaller research community (fewer citations in international conferences)
- Non-standard benchmarks (harder to compare to ACL/EMNLP papers)
- Chinese-only (limits cross-lingual research opportunities)
- MTL-only design (cannot isolate parsing from other tasks easily)

**Exception**: If researching HIT-specific annotation standards or knowledge distillation for MTL.

### Why Not CoreNLP

**Reasons to avoid**:
- Pre-neural architecture (not competitive with SOTA)
- Maintenance mode (Stanford recommends Stanza for new research)
- Java (Python dominates NLP research workflows)
- Outdated baselines (2015-era scores, not relevant for 2025 research)

## Risk Factors and Mitigations

### Risk: UD vs CTB Benchmark Mismatch

**Problem**: Many Chinese NLP papers use CTB (Penn Chinese Treebank), but Stanza uses UD.
- Scores may not be directly comparable
- Reviewer asks "why not compare to [CTB-based paper]?"

**Mitigation**:
- Acknowledge different benchmarks in paper
- Report both UD and CTB scores (train Stanza on CTB if needed)
- Cite trend toward UD in recent literature (it's becoming standard)

### Risk: Training Data Size

**Problem**: UD Chinese-GSD (~4K sentences) smaller than CTB (~50K)
- Lower ceiling on model accuracy
- Some linguistic phenomena underrepresented

**Mitigation**:
- Use data augmentation (back-translation, paraphrasing)
- Report results on multiple test sets (UD-GSD + UD-CFL + classical)
- Consider fine-tuning on domain-specific data if available

### Risk: Reproducibility Challenges

**Problem**: Even with version locking, subtle differences can occur
- PyTorch version changes (minor numerical differences)
- Hardware differences (CPU vs GPU, floating-point precision)
- Randomness in training (seed issues)

**Mitigation**:
- Document full environment (PyTorch version, Python version, hardware)
- Fix random seeds (`torch.manual_seed`, `numpy.random.seed`)
- Report mean ± std dev over multiple runs (e.g., 5 runs with different seeds)
- Share trained models on Hugging Face or GitHub (exact reproducibility)

## Expected Outcomes

**Timeline**: 2-6 months for typical research project
- Week 1-2: Baseline evaluation (run Stanza on standard test sets)
- Week 3-8: Custom model development (architecture experiments)
- Week 9-16: Training, evaluation, error analysis
- Week 17-24: Paper writing, reproducibility verification

**Deliverables**:
- Reproducible benchmarks (UD test sets, standard evaluation)
- Trained models (shareable checkpoints)
- Error analysis (what linguistic phenomena are hard)
- Publication-ready results (ACL/EMNLP/COLING submission)

## Summary

**For NLP researchers, Stanza is the clear choice** due to UD-native design, academic credibility, and reproducibility. HanLP is a strong alternative for semantic dependency or multilingual research. LTP and CoreNLP don't fit the typical academic research workflow as well.

**Key success factors**:
- Use standard benchmarks (UD test sets, CoNLL evaluation)
- Document versions precisely (Stanza, UD, PyTorch)
- Compare to published baselines (cite Stanza paper)
- Share trained models (GitHub, Hugging Face)
