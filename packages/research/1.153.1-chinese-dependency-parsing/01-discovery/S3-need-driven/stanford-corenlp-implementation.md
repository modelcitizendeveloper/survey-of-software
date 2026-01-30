# Using Stanford CoreNLP

Stanford CoreNLP provides a Java suite of NLP tools. The Chinese parser based on Chinese Treebank is included in the distribution.

## How It Works

The neural dependency parser performs a linear-time scan over sentence words, maintaining:
- A partial parse
- A stack of words currently being processed
- A buffer of words yet to be processed

It applies transitions (LEFT-ARC, RIGHT-ARC, SHIFT) until the buffer is empty and dependency graph is complete.

## Sources
- [CoreNLP GitHub](https://github.com/stanfordnlp/CoreNLP)
- [Stanford Parser](https://nlp.stanford.edu/software/lex-parser.shtml)
- [Parsing Chinese with Stanford NLP](https://michelleful.github.io/code-blog/2015/09/10/parsing-chinese-with-stanford/)
