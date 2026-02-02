# PaddleOCR - CJK Support

## Overview
PaddleOCR is a lightweight OCR toolkit developed by Baidu, released in 2020. Built on the PaddlePaddle deep learning framework, it's specifically designed with strong Chinese language support as a primary goal.

## CJK Model Availability

**Chinese Models (Primary Focus):**
- Simplified Chinese (default, highly optimized)
- Traditional Chinese
- Multi-language models including Chinese + English

**Other CJK:**
- Japanese
- Korean

**Language Detection:**
Automatic language detection for mixed Chinese/English text

## Technical Approach

**Modern Deep Learning Pipeline:**

1. **Text Detection** - DB (Differentiable Binarization) algorithm
   - Locates text regions in images
   - Handles arbitrary orientations and curved text

2. **Text Recognition** - CRNN (Convolutional Recurrent Neural Network)
   - Converts detected regions to text
   - Uses CTC (Connectionist Temporal Classification) for sequence modeling

3. **Text Direction Classification**
   - Automatically detects text orientation (0°, 90°, 180°, 270°)
   - Handles vertical and horizontal text

**Model Variants:**
- **Mobile models** - Lightweight (~10MB), optimized for edge devices
- **Server models** - Higher accuracy, larger size (~100MB+)
- **Slim models** - Quantized versions for resource-constrained environments

## Character Density Handling

PaddleOCR was designed with CJK challenges in mind:

**Similar Characters:**
- Large training dataset with intentional focus on confusable pairs
- Character-level attention mechanisms
- Context modeling to disambiguate (e.g., 土/士 by surrounding characters)

**Vertical Text:**
- Native support without separate models
- Automatic rotation detection
- Preserves reading order (top-to-bottom, right-to-left)

**Font Variation:**
- Trained on diverse font styles (serif, sans-serif, handwritten styles)
- Handles both simplified and traditional simultaneously in multi-language mode

## Installation Complexity

**Pros:**
- Pure Python package via pip
- Models download automatically on first use
- Good documentation (Chinese + English)
- Includes visualization tools

**Cons:**
- Requires PaddlePaddle framework (additional dependency vs pure TensorFlow/PyTorch)
- Larger initial download due to model size
- GPU acceleration requires CUDA setup (like most deep learning tools)

**Basic Setup:**
```bash
# CPU version
pip install paddlepaddle paddleocr

# GPU version (requires CUDA)
pip install paddlepaddle-gpu paddleocr

# First run downloads models automatically
from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='ch')  # 'ch' = Chinese
```

## Reported Accuracy

**Strengths:**
- Excellent on Chinese text (both simplified and traditional)
- Handles handwritten Chinese better than Tesseract
- Robust on low-quality images (mobile phone captures)
- Good performance on scene text (signs, billboards)

**Benchmark Results:**
- 96%+ character accuracy on printed simplified Chinese (clean scans)
- 90-95% on mobile phone captures
- 85-90% on stylized fonts and handwritten text
- Consistently outperforms Tesseract on Chinese benchmarks

**Performance:**
- Faster inference than Tesseract on GPU
- Mobile models run at 50-100ms per image on modern CPUs

## Quick Assessment

**Best for:**
- Chinese text as primary focus
- Mixed quality input (scans, photos, screenshots)
- Production systems requiring high accuracy
- Mobile/edge deployment (mobile models)
- Document layout analysis (includes table detection)

**Not ideal for:**
- Projects already standardized on TensorFlow/PyTorch (different framework)
- Extremely resource-constrained environments (models still 10MB+ minimum)
- Latin-script primary use cases (optimized for CJK)

## Unique Features

**Beyond basic OCR:**
- Table structure recognition
- Layout analysis
- PDF processing
- Angle correction
- Dewarping for curved text

**Active Development:**
- Regular model updates
- Strong Chinese community support
- Baidu commercial backing

## License
Apache 2.0 (permissive, commercial-friendly)

## Ecosystem
- PaddleOCR-json (cross-platform API wrapper)
- PaddleX (low-code training platform)
- Pre-trained models for 80+ languages
