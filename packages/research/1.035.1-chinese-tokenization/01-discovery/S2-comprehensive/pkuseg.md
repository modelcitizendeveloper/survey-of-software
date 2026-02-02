# PKUSEG: Technical Deep-Dive

## Architecture: BiLSTM-CRF

### Model Components

**BiLSTM Layer**:
```
Input: Character sequence [我, 爱, 北, 京]
       ↓
Embedding: [emb_我, emb_爱, emb_北, emb_京]
       ↓
BiLSTM: Forward + Backward LSTM
       ↓
Hidden states: [h_1, h_2, h_3, h_4]
```

**CRF Layer**:
```
Hidden states → Transition probabilities
BMES tags: B(begin) M(middle) E(end) S(single)

Valid transitions:
B → M, B → E
M → M, M → E
E → B, E → S
S → B, S → S
```

**Output**:
```
我: S (single-char word)
爱: S
北: B (begin word)
京: E (end word)
→ Segmentation: 我 / 爱 / 北京
```

## Training Process

### Data Requirements
- **Format**: Pre-segmented corpus with space-separated words
- **Size**: 10M+ characters for good quality
- **Domain-specific**: Separate models for news, web, medicine, tourism

### Training Steps
1. **Character embedding**: Learn 128-dim character vectors
2. **BiLSTM training**: 2-layer LSTM, 256 hidden units
3. **CRF transition learning**: Optimize transition matrix
4. **Validation**: F1 score on held-out set

### Hyperparameters
```python
embedding_dim = 128
lstm_hidden = 256
lstm_layers = 2
dropout = 0.5
learning_rate = 0.001
batch_size = 32
epochs = 10-20
```

## Domain Models

### Pre-trained Models

| Model | Training Corpus | Size | Best For |
|-------|----------------|------|----------|
| news | People's Daily | 1.5M sentences | News articles |
| web | Weibo, forums | 2M sentences | Social media |
| medicine | Medical texts | 500K sentences | Healthcare |
| tourism | Travel reviews | 300K sentences | Travel content |
| mixed | Multi-domain | 3M sentences | General purpose |

### Model Selection Impact

**Example: Medical term "高血压" (hypertension)**
```
General model: 高 / 血 / 压 (wrong - split into chars)
Medical model: 高血压 (correct - recognized as medical term)
```

Domain models learn terminology through training data, not dictionaries.

## Feature Engineering

### Input Features
1. **Character embeddings**: 128-dim learned vectors
2. **Character type**: Digit, letter, Chinese, punctuation
3. **Character n-grams**: Bigrams, trigrams (optional)

### Context Window
- BiLSTM sees entire sentence (both directions)
- Effective context: ~50 characters in each direction
- Longer context than Jieba (which uses local bigrams)

## Performance Characteristics

### Speed Analysis
```
Processing pipeline:
1. Character encoding: 10% time
2. BiLSTM forward pass: 70% time
3. CRF decoding: 15% time
4. Post-processing: 5% time

Bottleneck: BiLSTM forward pass (neural computation)
```

### Memory Profile
| Component | Memory |
|-----------|--------|
| Model weights | ~200 MB |
| Embeddings | ~50 MB |
| LSTM states | ~50 MB (per sentence) |
| Total | ~300 MB |

### GPU Acceleration
- **CPU**: ~130 KB/s
- **GPU**: ~800 KB/s (6x speedup)
- Batch processing improves GPU utilization

## Accuracy Breakdown

### By Text Type
| Corpus | F1 Score |
|--------|----------|
| PKU (news) | 96.5% |
| MSR (mixed) | 96.2% |
| CTB (formal) | 95.8% |
| Weibo (informal) | 93.1% |

### Error Analysis

**Common errors**:
1. **Rare proper names**: "史蒂夫·乔布斯" may be split incorrectly
2. **New compounds**: "人工智能" if not in training data
3. **Ambiguous boundaries**: Context-dependent cases

**Compared to Jieba**:
- 11% fewer errors overall
- 25% fewer errors on domain-specific terms (with domain model)
- Better on OOV words (neural embeddings vs HMM)

## Advanced Configuration

### Custom Training
```python
import pkuseg

# Train custom model
pkuseg.train(
    train_file='train.txt',
    test_file='test.txt',
    save_dir='my_model/',
    train_iter=10,
    init_model='mixed'  # Start from pre-trained
)

# Use custom model
seg = pkuseg.pkuseg(model_name='my_model/')
```

### Inference Options
```python
seg = pkuseg.pkuseg(
    model_name='medicine',
    user_dict='custom_terms.txt',  # Add domain dictionary
    postag=True                     # Enable POS tagging
)
```

## Integration with Deep Learning

### With PyTorch
```python
import pkuseg
import torch

seg = pkuseg.pkuseg()

# Segment before feeding to model
text = "我爱北京天安门"
words = seg.cut(text)
tokens = [word_to_id[w] for w in words]
input_tensor = torch.tensor([tokens])
```

### With BERT
```python
from transformers import BertTokenizer
import pkuseg

# Pre-segment with PKUSEG
seg = pkuseg.pkuseg()
words = " ".join(seg.cut(text))

# Then use BERT tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
tokens = tokenizer.tokenize(words)
```

## Technical Limitations

1. **Fixed model**: Cannot adapt at inference time
2. **No uncertainty**: Single output (no probability distribution)
3. **Sequence length**: Performance degrades on very long texts (>500 chars)
4. **Domain shift**: Accuracy drops on out-of-domain text without retraining

## Comparison with LAC

| Aspect | PKUSEG | LAC |
|--------|--------|-----|
| Architecture | BiLSTM-CRF | BiGRU-CRF |
| Speed | 130 KB/s | 800 QPS |
| Domain models | 5 pre-trained | 1 general |
| Joint tasks | Seg + POS (optional) | Seg + POS + NER |
| Training | Academic corpus | Baidu production data |
| Accuracy | F1 ~96% | F1 ~91% |

PKUSEG optimizes for accuracy, LAC for speed.

## When Architecture Matters

Choose BiLSTM-CRF (PKUSEG) when:
- Domain-specific accuracy is critical
- You have GPU for faster inference
- Training custom models is acceptable
- Context matters (BiLSTM sees full sentence)

Avoid when:
- Real-time processing required (use Jieba or LAC)
- Simple general-purpose segmentation sufficient
- No GPU available and speed matters
