# CJK-Specific Technical Challenges

## Character Set Size

The fundamental architectural difference between Latin and CJK OCR: [CJK scripts with thousands of characters require different model architectures](https://github.com/JaidedAI/EasyOCR/blob/master/custom_model.md).

**Impact**:
- Attention mechanisms preferred over CTC for CJK
- Larger model sizes required
- More training data needed
- Higher computational requirements

## Multilingual Mixed Documents

[DeepSeek-OCR (2026) focuses on recognizing patterns in visual structure rather than alphabet-specific tokens, allowing seamless handling of multilingual and mixed-script content on a single page](https://milvus.io/ai-quick-reference/how-does-deepseekocr-enable-multilingual-and-mixedscript-document-processing).

[PaddleOCR has dedicated Chinese+English models reflecting Baidu's focus](https://intuitionlabs.ai/pdfs/technical-analysis-of-modern-non-llm-ocr-engines.pdf). [Engineered for both high accuracy and deployment efficiency, excelling in industrial use cases](https://intuitionlabs.ai/pdfs/technical-analysis-of-modern-non-llm-ocr-engines.pdf).

## Vertical Text Processing

Japanese documents often use vertical writing (tategaki):
- Text flows top to bottom
- Columns progress right to left
- Mixed horizontal inserts require special handling
- Furigana (pronunciation guides) positioned differently

**Solutions**:
- Dedicated vertical text models (jpn_vert in Tesseract)
- Orientation detection and classification
- Layout-aware processing pipelines

## Word Boundary Detection

Chinese and Japanese lack explicit word boundaries:
- Character sequences must be parsed for word breaks
- Context-dependent segmentation required
- Different from Korean which uses spaces

**Impact**: OCR alone insufficient - requires additional word segmentation step for downstream NLP tasks.
