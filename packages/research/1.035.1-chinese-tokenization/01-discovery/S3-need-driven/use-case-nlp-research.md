# Use Case: Academic NLP Research

## Who Needs This

**Persona**: PhD student or NLP researcher

**Context**: Conducting research on Chinese NER, sentiment analysis, or machine translation. Publishing in ACL, EMNLP, or similar venues. Results must be reproducible and comparable to baselines.

**Scale**: Research datasets (10K-1M examples), not production scale

## Why They Need Tokenization

### Core Requirements
1. **Maximum accuracy**: Segmentation errors propagate to downstream tasks
2. **Reproducibility**: Must use standard benchmarks and tools
3. **Comparability**: Results must match published baselines
4. **Documentation**: Need citations for methodology

### Academic Impact
- Poor tokenization → 10-15% accuracy drop on NER
- Non-standard tokenizer → Paper rejected (can't compare to baselines)
- Example: SIGHAN Bakeoff uses specific segmenters for fair comparison

## Key Constraints

| Constraint | Requirement | Why |
|------------|-------------|-----|
| Accuracy | >95% F1 | Downstream task quality |
| Speed | Less critical | Batch processing OK |
| Reproducibility | Must use published tools | Paper acceptance |
| Citations | Need academic papers | Methodology section |
| Standard benchmarks | PKU, MSR, CTB corpora | Comparison to baselines |

## Recommended Solution

### Primary: PKUSEG (Domain Model)

```python
import pkuseg

# For news/formal text research
seg = pkuseg.pkuseg(model_name='news')

# For social media research
seg = pkuseg.pkuseg(model_name='web')

# For medical NLP research
seg = pkuseg.pkuseg(model_name='medicine')
```

**Why PKUSEG**:
- ✅ **Highest accuracy**: F1 ~96% on benchmarks
- ✅ **Academic credibility**: Peking University, published papers
- ✅ **Domain models**: Match research context
- ✅ **Citable**: Has EMNLP paper you can cite

### Citation
```
@inproceedings{luo2019pkuseg,
  title={PKUSeg: A Toolkit for Multi-Domain Chinese Word Segmentation},
  author={Luo, Ruixuan and Xu, Jingjing and Zhang, Yi and others},
  booktitle={EMNLP},
  year={2019}
}
```

## Alternatives

### If Using Transformer Models
**Use: bert-base-chinese (character-level)**
```python
from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
# Character-level, matches BERT papers exactly
```
- Standard in transformer research
- Reproducible results
- Well-documented in papers

### If Researching Tokenization Itself
**Compare: Jieba vs PKUSEG vs LAC vs BERT**
- Ablation study showing impact of tokenization choice
- Cite all tools properly
- Report F1 scores on standard benchmarks

## Validation Checklist

- [ ] Test on standard benchmarks (PKU, MSR, CTB)
- [ ] Report F1 scores for reproducibility
- [ ] Choose domain model matching your data
- [ ] Cite tokenizer in paper methodology
- [ ] Compare to published baselines using same tokenizer
- [ ] Document all hyperparameters

## Summary

**For academic research, use PKUSEG or bert-base-chinese** because:
- Maximum accuracy needed for publication
- Well-documented and citable
- Standard tools enable fair comparison
- Domain models match research contexts
