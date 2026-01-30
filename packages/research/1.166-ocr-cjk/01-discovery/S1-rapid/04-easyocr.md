# EasyOCR: CJK Capabilities

## What It Is

[Ready-to-use OCR library supporting 80+ languages](https://github.com/JaidedAI/EasyOCR)

## CJK Capabilities

- [Supports ch_sim, ch_tra, ja, ko with Gen2 models for improved accuracy](https://www.jaided.ai/easyocr/)
- [Character sets: Simplified Chinese (6,000+ chars), Traditional Chinese (8,000+ chars), Japanese (Hiragana, Katakana, Kanji)](https://deepwiki.com/JaidedAI/EasyOCR/7.3-supported-languages)
- [Language compatibility: English compatible with all languages, shared character languages compatible with each other](https://www.jaided.ai/easyocr/tutorial/)

## Architecture

Built on PyTorch with dual architecture approach (CRNN for Latin, Transformer for CJK)

## Strengths

- Easiest to set up and use
- Good out-of-box performance
- Active development
- Well-suited for prototyping

## Limitations

- [Open issue for enhanced CJK-specific punctuation support (「」，。、)](https://github.com/JaidedAI/EasyOCR/issues/1175)
- Accuracy lower than PaddleOCR on complex CJK documents
- Less optimization for CJK compared to PaddleOCR
