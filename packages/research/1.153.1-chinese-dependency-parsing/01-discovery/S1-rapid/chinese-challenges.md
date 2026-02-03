# Why Chinese Dependency Parsing is Unique

Chinese lacks explicit word boundaries, making segmentation both necessary and inherently ambiguous. This creates a unique challenge: word segmentation is the precondition of dependency parsing, which makes dependency parsing suffer from error propagation and unable to directly make use of character-level pre-trained language models (such as BERT).

Word segmentation has significant impact on dependency parsing performance in Chinese, as variations in segmentation schemes lead to differences in the number and structure of tokens, which affect both the syntactic representations learned by the parser and the evaluation metrics used to assess parsing quality.

## Sources
- [Character-Level Dependency Model for Joint Word Segmentation](https://www.academia.edu/136870493/Character_Level_Dependency_Model_for_Joint_Word_Segmentation_POS_Tagging_and_Dependency_Parsing_in_Chinese)
- [Parsing Through Boundaries in Chinese Word Segmentation](https://arxiv.org/html/2503.23091)
- [A Graph-based Model for Joint Chinese Word Segmentation and Dependency Parsing](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00301/43541/A-Graph-based-Model-for-Joint-Chinese-Word)
