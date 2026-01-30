# S1: What is OCR for CJK Text?

## Overview

OCR for CJK (Chinese, Japanese, Korean) text refers to specialized optical character recognition systems designed to handle the unique challenges of East Asian writing systems. The three major open-source tools in this space are Tesseract, PaddleOCR, and EasyOCR.

## Why CJK OCR is Different

CJK text recognition presents fundamentally different challenges compared to Latin alphabet OCR:

### Character Set Complexity
- **Scale**: Unicode defines [101,996 characters in the CJK Unified Ideographs set](https://en.wikipedia.org/wiki/CJK_Unified_Ideographs)
- **Classes**: [Large number of character classes creates high probability of confusions between similar character shapes](https://link.springer.com/rwe/10.1007/978-0-85729-859-1_14)
- **Monospacing**: [CJK characters are typically monospaced/fixed-pitch](https://tesseract-ocr.github.io/docs/MOCRadaptingtesseract2.pdf)

### Language-Specific Differences
- **Word boundaries**: [Chinese and Japanese don't use spaces between words, unlike Korean](https://github.com/TheJoeFin/Text-Grab/issues/191)
- **Mixed scripts**: Japanese uses Hiragana, Katakana, and Kanji in the same text
- **Vertical text**: Japanese often written vertically (top to bottom, right to left)

### Handwriting Challenges
- **Shape variations**: [Primary difficulty comes from writers' habits, styles, and times](https://pnclink.org/annual/annual2000/2000pdf/4-7-3.pdf)
- **Cursive strings**: Classical CJK text requires preprocessing from color filtering to segmentation
- **Seals and stamps**: Traditional documents include seals that must be distinguished from text

## The Three Major Tools

### Tesseract OCR

**What it is**: [Open-source OCR engine originally developed by HP, now maintained by Google](https://en.wikipedia.org/wiki/Tesseract_(software))

**CJK Capabilities**:
- [Version 3+ supports ideographic (Chinese & Japanese) and 116+ languages total](https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html)
- [Trained data files for chi_sim, chi_tra, jpn, jpn_vert, kor](https://pyimagesearch.com/2020/08/03/tesseract-ocr-for-non-english-languages/)
- [Three model variants: tessdata_best (accuracy), tessdata (balanced), tessdata_fast](https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html)

**Architecture**: [LSTM-based OCR engine with language-specific configurations for fixed-pitch character segmentation](https://tesseract-ocr.github.io/docs/MOCRadaptingtesseract2.pdf)

### PaddleOCR

**What it is**: [OCR toolkit from Baidu built on PaddlePaddle framework](https://github.com/PaddlePaddle/PaddleOCR)

**CJK Capabilities**:
- [PP-OCRv5 unified model supports Simplified Chinese, Traditional Chinese, Chinese Pinyin, English, and Japanese](https://www.tenorshare.com/ocr/paddleocr.html)
- [PaddleOCR-VL supports 109 languages including Chinese, Japanese, Korean](https://huggingface.co/PaddlePaddle/PaddleOCR-VL)
- [13% accuracy improvement over previous versions for multilingual mixed documents](https://www.tenorshare.com/ocr/paddleocr.html)

**Architecture**: [PaddleOCR 3.0 built around model training toolkit and inference library](https://arxiv.org/html/2507.05595v1); [PaddleOCR-VL uses NaViT-style dynamic resolution visual encoder with ERNIE-4.5-0.3B language model](https://huggingface.co/PaddlePaddle/PaddleOCR-VL)

**Performance**: [OCR block edit rates ≤0.035, actively maintained through 2025-2026](https://huggingface.co/PaddlePaddle/PaddleOCR-VL)

### EasyOCR

**What it is**: [Ready-to-use OCR library supporting 80+ languages](https://github.com/JaidedAI/EasyOCR)

**CJK Capabilities**:
- [Supports ch_sim, ch_tra, ja, ko with Gen2 models for improved accuracy](https://www.jaided.ai/easyocr/)
- [Character sets: Simplified Chinese (6,000+ chars), Traditional Chinese (8,000+ chars), Japanese (Hiragana, Katakana, Kanji)](https://deepwiki.com/JaidedAI/EasyOCR/7.3-supported-languages)
- [Language compatibility: English compatible with all languages, shared character languages compatible with each other](https://www.jaided.ai/easyocr/tutorial/)

**Limitations**: [Open issue for enhanced CJK-specific punctuation support (「」，。、)](https://github.com/JaidedAI/EasyOCR/issues/1175)

## When You Need CJK-Specific OCR

**Use CJK OCR when**:
- Processing documents in Chinese, Japanese, or Korean
- Handling mixed-script documents (e.g., Japanese with Kanji + Hiragana)
- Working with vertical text layouts (Japanese publications)
- Dealing with historical or classical CJK texts
- Processing forms with thousands of possible character classes

**General OCR is insufficient because**:
- Latin-focused OCR trained on 26-letter alphabets can't handle 100,000+ ideographs
- Word segmentation algorithms assume space-delimited words
- Character similarity detection needs CJK-specific training
- [Pattern training not supported for CJK in some commercial systems](https://support.abbyy.com/hc/en-us/articles/360003422379-Using-pattern-training-for-Chinese-Japanese-and-Korean-CJK-languages-in-FineReader-Engine)

## Key Insight

The fundamental challenge is scale and ambiguity: [CJK languages have large symbol sets and lack clear word boundaries, posing serious tests for classification engines designed for well-delimited words from small alphabets](https://tesseract-ocr.github.io/docs/MOCRadaptingtesseract2.pdf).
