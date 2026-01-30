# S2: How Does CJK OCR Work?

## General Pipeline Architecture

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

## Tesseract LSTM Architecture

### Overview
[Tesseract Version 4 employs Long Short-Term Memory (LSTM), a form of Recurrent Neural Network (RNN)](https://nanonets.com/blog/ocr-with-tesseract/). [This neural network-based recognition engine delivers significantly higher accuracy than previous versions](https://github.com/tesseract-ocr/tesseract/wiki/4.0-with-lstm).

### How It Works
[The input image is processed in boxes (rectangles) line by line, feeding into the LSTM model](https://www.researchgate.net/figure/Fig6Internal-Architecture-of-OCR-Tesseract-8-Version-4-has-a-dataset-knowledge-of_fig3_341779791). [Tesseract 4 focuses on line recognition](https://learnopencv.com/deep-learning-based-text-recognition-ocr-using-tesseract-and-opencv/).

### Architecture Components
[To recognize a single character, CNNs are typically used. For arbitrary-length text (sequences of characters), RNNs are used, with LSTM being a popular form](https://nanonets.com/blog/ocr-with-tesseract/).

[The network specification string describes the architecture](https://groups.google.com/g/tesseract-ocr/c/ZuXSyBDvPhk/m/vcZWc8FjAAAJ). Example: `[1,36,0,1Ct3,3,16Mp3,3Lfys64Lfx96Lrx96Lfx512O1c1]` includes:
- **Ct3,3,16**: 3x3 convolution with 16 filters
- **Mp3,3**: Max pooling layers
- **Lfys64, Lfx96, Lrx96, Lfx512**: LSTM layers in different dimensions

### CJK-Specific Configurations
[For CJK languages, page segmentation mode (--psm) settings are important](https://tesseract-ocr.github.io/tessdoc/tess5/TrainingTesseract-5.html). [The .traineddata files include script-specific configurations, including vertical text detection in jpn_vert.traineddata](https://deepwiki.com/tesseract-ocr/tessdata/6-developer-guide).

### Training Data
[For Latin languages, models trained on ~400,000 textlines spanning ~4,500 fonts](https://github.com/tesseract-ocr/tesseract/wiki/4.0-with-lstm). [For other scripts, fewer fonts available but similar number of textlines](https://github.com/tesseract-ocr/tesseract/wiki/4.0-with-lstm).

## PaddleOCR PP-OCRv5 Architecture

### Pipeline Overview
[PP-OCRv5 employs a four-stage pipeline: image preprocessing, text detection, text line orientation classification, and text recognition](https://arxiv.org/html/2507.05595v1). [System offers both server and mobile variants](https://arxiv.org/html/2507.05595v1).

### Core Stages

**1. Image Preprocessing**
[Handles image rotation and distortion to standardize input](https://paddlepaddle.github.io/PaddleX/3.3/en/pipeline_usage/tutorials/ocr_pipelines/OCR.html)

**2. Text Detection**
[Based on improved DB (Differentiable Binarization) architecture](https://huggingface.co/PaddlePaddle/PP-OCRv5_server_det). [Models output probability maps post-processed into polygon bounding boxes](https://huggingface.co/PaddlePaddle/PP-OCRv5_server_det).

**3. Text Line Orientation Classification**
[Classifies orientation of detected text for correct alignment](https://paddlepaddle.github.io/PaddleX/3.3/en/pipeline_usage/tutorials/ocr_pipelines/OCR.html)

**4. Text Recognition**
[Uses encoder-decoder architecture with CTC (Connectionist Temporal Classification) loss](https://huggingface.co/blog/baidu/ppocrv5). [Supports variable-length text input and outputs character sequences with confidence scores](https://huggingface.co/blog/baidu/ppocrv5).

### Key Innovation
[PP-OCRv5 achieves unified recognition of Simplified Chinese, Traditional Chinese, Chinese Pinyin, English, and Japanese in a single model](https://deepwiki.com/PaddlePaddle/PaddleOCR/2.1-pp-ocrv5-universal-text-recognition). [Previous versions required separate models for different languages](https://huggingface.co/blog/baidu/ppocrv5).

[Single model supports five text types with 13% accuracy improvement](https://www.alphaxiv.org/overview/2507.05595). [Maintains efficiency for both cloud and edge deployment](https://huggingface.co/blog/baidu/ppocrv5).

## EasyOCR Architecture

### Dual-Architecture Approach
[Languages with complex characters like Chinese/Japanese use attention-based architectures rather than CTC due to large character sets](https://github.com/JaidedAI/EasyOCR/blob/master/custom_model.md). [Script-specific models: CRNN for Latin, Transformer for CJK](https://medium.com/@mohamed5elyousfi/-277e9c685578).

### Core Components
[Recognition model is CRNN with three main components](https://medium.com/@adityamahajan.work/easyocr-a-comprehensive-guide-5ff1cb850168):

**1. Feature Extraction**
[Deep learning models like ResNet and VGG extract features from input images](https://eng-mhasan.medium.com/ocr-with-deep-learning-in-python-e443970d09e4). [Current configuration: 'None-VGG-BiLSTM-CTC'](https://github.com/JaidedAI/EasyOCR/blob/master/custom_model.md).

**2. Sequence Labeling**
[LSTM networks interpret extracted features' sequential context](https://products.documentprocessing.com/parser/python/easyocr/)

**3. Decoding**
[CTC algorithm decodes and transcribes labeled sequences into recognized text](https://products.documentprocessing.com/parser/python/easyocr/)

### Text Detection
[CRAFT-based text localization enhanced with ResNet backbone](https://medium.com/@mohamed5elyousfi/-277e9c685578)

### Training Pipeline
[Based on modified version of deep-text-recognition-benchmark framework](https://www.bentoml.com/blog/deploying-an-ocr-model-with-easyocr-and-bentoml)

## CJK-Specific Technical Challenges

### Character Set Size
The fundamental architectural difference between Latin and CJK OCR: [CJK scripts with thousands of characters require different model architectures](https://github.com/JaidedAI/EasyOCR/blob/master/custom_model.md).

### Multilingual Mixed Documents
[DeepSeek-OCR (2026) focuses on recognizing patterns in visual structure rather than alphabet-specific tokens, allowing seamless handling of multilingual and mixed-script content on a single page](https://milvus.io/ai-quick-reference/how-does-deepseekocr-enable-multilingual-and-mixedscript-document-processing).

[PaddleOCR has dedicated Chinese+English models reflecting Baidu's focus](https://intuitionlabs.ai/pdfs/technical-analysis-of-modern-non-llm-ocr-engines.pdf). [Engineered for both high accuracy and deployment efficiency, excelling in industrial use cases](https://intuitionlabs.ai/pdfs/technical-analysis-of-modern-non-llm-ocr-engines.pdf).

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
