# spaCy Terminology Components

## Quick Summary

spaCy itself doesn't have built-in "terminology extraction" but provides the NLP pipeline infrastructure. Term extraction happens via:
1. Custom pipeline components
2. Ecosystem extensions (spaCy Universe)
3. Integration with other libraries (pyate, textacy)

## Installation

```bash
pip install spacy
python -m spacy download en_core_web_sm  # or other language models
```

## Relevant Components

### Built-in Features:
- **POS tagging**: Identify nouns, noun phrases
- **Dependency parsing**: Understand phrase structure
- **Named Entity Recognition**: Extract entities
- **Noun phrase chunking**: Extract multi-word terms
- **Matchers**: Pattern-based extraction (Matcher, PhraseMatcher)

### Ecosystem Extensions (spaCy Universe):
- **pyate**: Multiple term extraction algorithms (covered separately)
- **sense2vec**: Combines noun phrases with POS/entity labels
- **textacy**: Higher-level NLP tasks including term extraction

## How to Use for Term Extraction

### Approach 1: Manual noun phrase extraction
```python
import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("Your text here")
terms = [chunk.text for chunk in doc.noun_chunks]
```

### Approach 2: Add pyate to pipeline
```python
import spacy
from pyate import combo_basic
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("combo_basic")
doc = nlp("Your text here")
terms = doc._.terms
```

### Approach 3: Custom component
Create custom pipeline component with domain-specific rules.

## Use Cases

- **Framework for term extraction**: Use built-in features + custom logic
- **Integration point**: Combine with specialized libraries (pyate, textacy)
- **Multilingual support**: 70+ language models available

## Resources

- **Website**: [spacy.io](https://spacy.io/)
- **spaCy Universe**: [spacy.io/universe](https://spacy.io/universe) (ecosystem directory)
- **Linguistic Features**: [spacy.io/usage/linguistic-features](https://spacy.io/usage/linguistic-features)

## Initial Assessment

**Pros**:
- Industry-standard NLP library
- Excellent multilingual support (70+ languages)
- Fast, production-ready
- Extensible architecture
- Large ecosystem

**Cons**:
- Not a term extraction library per se (requires extensions)
- Heavier dependency (language models are large)
- Requires understanding of NLP pipeline architecture

**Recommended for**: Projects needing **robust NLP infrastructure** with term extraction as one component. Use spaCy + pyate/textacy for best results, not spaCy alone.
