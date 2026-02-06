# Use Case: Traditional Chinese Academic Corpus

**Tool**: CKIP
**Accuracy**: 97.33% F1 on ASBC (Traditional Chinese)
**Domain**: Taiwan/HK academic texts, historical documents

## Key Strengths
- Highest accuracy for Traditional Chinese
- Academia Sinica backing (Taiwan institution)
- Multi-task: WS + POS + NER

## Implementation
```python
from ckiptagger import WS, POS, NER

ws = WS("./data", device=0)  # GPU 0
pos = POS("./data", device=0)
ner = NER("./data", device=0)

sentences = ["蔡英文是台灣總統。"]
word_s = ws(sentences)
pos_s = pos(word_s)
ner_s = ner(word_s, pos_s)

# Words: [['蔡英文', '是', '台灣', '總統', '。']]
# POS: [['Nb', 'SHI', 'Nc', 'Na', 'PERIODCATEGORY']]
# NER: [[(0, 3, 'PERSON', '蔡英文')]]
```

## Use Cases
- Taiwan government documents
- Hong Kong archives
- Classical Chinese literature
- Academic linguistic research

**Requirements**: GPU recommended (CPU too slow for large corpora)

**Cross-reference**: [S2 ckip.md](../S2-comprehensive/ckip.md)
