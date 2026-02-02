# Tesseract OCR - CJK Support

## Overview
Tesseract is an open-source OCR engine originally developed by HP, now maintained by Google. First released in 1985, it has evolved through multiple versions with version 4+ adding LSTM-based neural network support.

## CJK Model Availability

**Chinese Models:**
- `chi_sim` - Simplified Chinese
- `chi_tra` - Traditional Chinese
- `chi_sim_vert` - Vertical simplified Chinese
- `chi_tra_vert` - Vertical traditional Chinese

**Japanese Models:**
- `jpn` - Japanese (mixed kanji, hiragana, katakana)
- `jpn_vert` - Vertical Japanese

**Korean Models:**
- `kor` - Korean
- `kor_vert` - Vertical Korean

## Technical Approach

**Pre-v4 (Legacy):**
Traditional pattern recognition with feature extraction

**v4+ (Current):**
LSTM (Long Short-Term Memory) neural networks
- Better handling of connected scripts
- Improved accuracy on complex layouts
- Requires more computational resources

## Character Density Handling

CJK scripts present unique challenges:
- **High information density** - Each character contains more visual information than Latin letters
- **Similar characters** - Many characters differ by subtle stroke variations (e.g., 土/士, 未/末)
- **Vertical text support** - Traditional CJK text flows top-to-bottom, right-to-left

Tesseract handles this through:
- Separate vertical text models (`*_vert`)
- Character segmentation before recognition
- Language-specific dictionaries for context correction

## Installation Complexity

**Pros:**
- Available in most package managers (apt, brew, chocolatey)
- Python wrapper (pytesseract) is simple to use
- Pre-trained models downloadable separately

**Cons:**
- Need to download language models separately
- Configuration for optimal CJK results requires tuning
- Different versions have different model formats

**Basic Setup:**
```bash
# Install engine
apt-get install tesseract-ocr

# Install Chinese models
apt-get install tesseract-ocr-chi-sim tesseract-ocr-chi-tra

# Python wrapper
pip install pytesseract
```

## Reported Accuracy

**Strengths:**
- Mature project with 15+ years of CJK model development
- Good performance on high-quality scans with clean backgrounds
- Handles printed text well

**Limitations:**
- Struggles with handwritten CJK text
- Less accurate on low-resolution images
- Vertical text recognition less robust than horizontal
- Context correction can introduce errors on proper nouns

**Benchmark Context:**
Academic papers report 85-95% character-level accuracy on simplified Chinese printed text, dropping to 60-75% on handwritten or stylized fonts.

## Quick Assessment

**Best for:**
- Printed documents with clean backgrounds
- Projects already using Tesseract for Latin scripts (multi-language consistency)
- On-premise deployments without API dependencies

**Not ideal for:**
- Handwritten text recognition
- Low-quality mobile phone captures
- Real-time processing (slower than modern deep learning approaches)

## License
Apache 2.0 (permissive, commercial-friendly)
