# Stanford CoreNLP

## What It Is
A comprehensive Java-based NLP toolkit from Stanford NLP Group with 8-language support including Chinese. Established in the pre-neural era, now maintained alongside Stanza.

## Chinese Support
Full pipeline for Chinese text:
- Word segmentation
- POS tagging
- Named entity recognition
- Constituency and dependency parsing
- Coreference resolution

**Parsing approach**: Graph-based, non-projective dependency parsing

## Technical Overview

**Language**: Java (requires Java 8+)
**Output format**: Universal Dependencies (since v3.5.2)
**Python access**: Via wrappers (`stanfordcorenlp`, `chinese_corenlp`)

**Dependencies formalism**: Stanford Dependencies developed by Huihsin Tseng and Pi-Chuan Chang, now outputs UD by default.

**Character encoding**: Handles both Traditional and Simplified Chinese (wrappers convert Traditional → Simplified for processing, restore in output)

## Ecosystem Position

**Strengths**:
- Battle-tested reliability from decade+ of use
- Complete NLP pipeline (not just parsing)
- Strong academic foundation and documentation

**Limitations**:
- Java requirement adds deployment complexity for Python projects
- Slower than modern neural parsers
- Stanza supersedes CoreNLP for most new projects (per Stanford FAQ)
- Python wrappers introduce additional dependencies

## Quick Assessment

**Use CoreNLP when**:
- Maintaining legacy systems already using CoreNLP
- Need exact reproducibility of older research
- Java infrastructure already in place
- Require both Traditional and Simplified Chinese handling

**Choose Stanza instead when**:
- Starting new Python projects
- Need faster processing with neural models
- Want native Python integration without Java dependencies
- Building modern ML pipelines

## Key Resources
- Official docs: https://stanfordnlp.github.io/CoreNLP/
- Dependency parsing: https://stanfordnlp.github.io/CoreNLP/depparse.html
- Chinese wrapper: https://github.com/hhhuang/chinese_corenlp
