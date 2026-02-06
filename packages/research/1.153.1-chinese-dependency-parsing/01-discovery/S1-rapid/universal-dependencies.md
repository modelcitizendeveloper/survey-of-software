# Universal Dependencies (UD)

## What It Is
A framework for morphosyntactic annotation providing consistent grammatical annotation across 100+ languages. Not a library itself, but the standard format and treebank collection that other parsers use.

## Chinese Support
Multiple Chinese treebanks available:
- **UD_Chinese-GSD**: General-purpose corpus
- **UD_Chinese-CFL**: Chinese as Foreign Language learner texts
- **UD_Chinese-PUD**: Parallel corpus (1000 sentences)
- **Classical Chinese**: Historical texts support

## Technical Overview

**Format**: CoNLL-U (10-field tabular format)
- ID, FORM, LEMMA, UPOS, XPOS, FEATS, HEAD, DEPREL, DEPS, MISC
- Represents dependency trees with HEAD and DEPREL fields
- Standardized across all UD-compliant parsers

**Role in Ecosystem**: UD is the training data and output format. Most modern parsers (Stanza, HanLP, LTP) train on UD treebanks and output UD-compliant structures.

## Ecosystem Position

**Strengths**:
- Cross-linguistic consistency enables multilingual applications
- Multiple treebanks for different Chinese varieties and domains
- Foundation for academic research and benchmarking

**Limitations**:
- Not a parser—you need tools like Stanza or HanLP to generate UD parses
- Different parsers trained on same UD data yield different accuracy
- Treebank size limits domain coverage

## Quick Assessment

**Use UD when**:
- Building multilingual systems requiring consistent annotations
- Need standardized output format for downstream tasks
- Academic research requiring reproducible benchmarks

**Choose another approach when**:
- Need Chinese-specific annotation schemes (e.g., semantic dependencies)
- Domain-specific requirements not covered by available treebanks
- Prefer proprietary formats from existing systems

## Key Resources
- Official site: https://universaldependencies.org/
- Chinese treebanks: https://github.com/UniversalDependencies/UD_Chinese-GSD
- Format specification: https://universaldependencies.org/format.html
