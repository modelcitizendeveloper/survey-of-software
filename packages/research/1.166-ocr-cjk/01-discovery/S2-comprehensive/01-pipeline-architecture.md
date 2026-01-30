# OCR Pipeline Architecture

## General Pipeline

Modern CJK OCR systems follow a multi-stage pipeline:

### 1. Preprocessing
[Common preprocessing techniques](https://medium.com/@TechforHumans/image-pre-processing-techniques-for-ocr-d231586c1230):
- **Binarization**: [Adaptive binarization uses neighboring pixels for conversion](https://www.mdpi.com/2079-9292/12/11/2449)
- **Contrast Enhancement**: [CLAHE for local contrast improvement](https://www.mdpi.com/2079-9292/12/11/2449)
- **Noise Reduction**: [Smoothing background to reduce ISO noise, using autoencoders](https://medium.com/@TechforHumans/image-pre-processing-techniques-for-ocr-d231586c1230)

### 2. Text Detection
Locating text regions within images

### 3. Segmentation
[Techniques can be summarized as top-down, bottom-up, and hybrid approaches](https://intuitionlabs.ai/pdfs/technical-analysis-of-modern-non-llm-ocr-engines.pdf). [Logographic systems like CJK scripts present unique challenges for segmentation](https://milvus.io/ai-quick-reference/how-does-deepseekocr-enable-multilingual-and-mixedscript-document-processing).

### 4. Recognition
Converting detected text regions to character sequences

### 5. Post-processing
Language models and context for error correction

## Evolution: Traditional vs Deep Learning

### Traditional Approaches
- Template matching
- Feature-based classification
- Rule-based segmentation

### Modern Deep Learning (2026)
- End-to-end neural networks
- Attention mechanisms for complex character sets
- Unified multilingual models
- Visual pattern recognition over alphabet-specific tokens
