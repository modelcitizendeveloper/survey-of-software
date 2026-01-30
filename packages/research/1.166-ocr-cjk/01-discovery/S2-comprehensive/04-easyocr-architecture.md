# EasyOCR Architecture

## Dual-Architecture Approach

[Languages with complex characters like Chinese/Japanese use attention-based architectures rather than CTC due to large character sets](https://github.com/JaidedAI/EasyOCR/blob/master/custom_model.md). [Script-specific models: CRNN for Latin, Transformer for CJK](https://medium.com/@mohamed5elyousfi/-277e9c685578).

## Core Components

[Recognition model is CRNN with three main components](https://medium.com/@adityamahajan.work/easyocr-a-comprehensive-guide-5ff1cb850168):

### 1. Feature Extraction
[Deep learning models like ResNet and VGG extract features from input images](https://eng-mhasan.medium.com/ocr-with-deep-learning-in-python-e443970d09e4). [Current configuration: 'None-VGG-BiLSTM-CTC'](https://github.com/JaidedAI/EasyOCR/blob/master/custom_model.md).

### 2. Sequence Labeling
[LSTM networks interpret extracted features' sequential context](https://products.documentprocessing.com/parser/python/easyocr/)

### 3. Decoding
[CTC algorithm decodes and transcribes labeled sequences into recognized text](https://products.documentprocessing.com/parser/python/easyocr/)

## Text Detection

[CRAFT-based text localization enhanced with ResNet backbone](https://medium.com/@mohamed5elyousfi/-277e9c685578)

## Training Pipeline

[Based on modified version of deep-text-recognition-benchmark framework](https://www.bentoml.com/blog/deploying-an-ocr-model-with-easyocr-and-bentoml)

## CJK-Specific Considerations

The fundamental architectural difference: [CJK scripts with thousands of characters require different model architectures than Latin scripts](https://github.com/JaidedAI/EasyOCR/blob/master/custom_model.md). This is why EasyOCR uses Transformer models for CJK rather than the CRNN approach used for Latin scripts.
