# Use Case: E-Commerce Product Label Recognition

## Context

**Scenario:** Online marketplace app (similar to Taobao, Amazon) where users can scan product barcodes or take photos of product packaging to quickly add items to cart, compare prices, or verify authenticity.

**User Persona:**
- Shoppers in physical stores comparing prices online
- Users verifying authentic products vs counterfeits
- Inventory managers cataloging stock

**Workflow:**
1. User opens mobile app, points camera at product
2. App captures photo of product label/packaging
3. OCR extracts product name, brand, specifications
4. App searches database for matching product
5. Display price, reviews, availability

## Requirements Analysis

### Input Characteristics

**Text Type:**
- Primarily printed text on product packaging
- Mix of Chinese (product name, description) and English (brand, model numbers)
- Occasional Japanese/Korean for imported products
- Font sizes vary (6pt warnings to 24pt+ brand names)

**Quality Factors:**
- Mobile phone camera (8-48MP typical)
- Varied lighting (store lighting, shadows, glare)
- Angles: Not always perpendicular to label
- Motion blur: Users may not hold steady
- Background clutter: Shelves, other products

**Volume:**
- Peak: 10,000+ requests/minute during shopping hours
- Daily: 5-10 million requests
- Geographic distribution: Primarily Asia (China, Japan, Korea)

### Accuracy Requirements

**Critical Text (Product Name, Brand):**
- Target: >92% character accuracy
- Acceptable: 88-92% (still finds correct product most of the time)
- Unacceptable: <88% (too many failed searches)

**Secondary Text (Specs, Descriptions):**
- Target: >85%
- Acceptable: Lower accuracy OK (supplementary info)

**Error Tolerance:**
- OK if occasionally misses small text (ingredient lists)
- NOT OK if misreads brand/product name (wrong product)
- Confidence scores critical to flag uncertain reads

### Speed Requirements

**End-to-End Latency:**
- Target: <2 seconds (capture to search results)
- Acceptable: 2-4 seconds
- Unacceptable: >4 seconds (user will retry or abandon)

**OCR Component Allocation:**
- Detection + Recognition: <800ms
- Network + Search: <1200ms
- Total: <2000ms

### Scale and Performance

**Infrastructure:**
- Global deployment (CDN for images, regional compute)
- Auto-scaling based on load (10x difference peak vs off-peak)
- 99.9% uptime requirement (shopping is 24/7)

## Technical Constraints

### Deployment Environment

**Architecture:**
```
Mobile App (Camera) → CDN (Image Upload) → API Gateway
                                              ↓
                                    Load Balancer
                                              ↓
                         OCR Service (Kubernetes, GPU workers)
                                              ↓
                         Product Search (ElasticSearch)
```

**Resource Availability:**
- GPU: Yes (cost justified by volume)
- Target: 50-100ms inference time (GPU)
- Batch processing: Mini-batches (4-8 images) for GPU efficiency

### Privacy and Compliance

**Data Handling:**
- User photos may contain personal info (low risk)
- No HIPAA/financial data concerns
- GDPR compliance: Store only hashed image fingerprints, not raw images
- Retention: Process and discard images after search (don't store)

### Cost Constraints

**Budget:**
- Infrastructure: $10K-30K/month acceptable
- Cost per recognition: Target <$0.001 (sub-cent)
- Break-even: Must be cheaper than commercial APIs at scale

## Solution Design

### Recommended Library: **EasyOCR**

**Rationale:**
1. **Multi-language strength:** Chinese + English + Japanese/Korean simultaneously
   - Product labels often mix languages (Chinese product name + English brand)
   - No need to pre-specify language per region
2. **Scene text performance:** 90-95% accuracy on product photos
   - CRAFT detection handles varied angles, lighting
   - Robust on low-quality mobile captures
3. **Confidence scoring:** Well-calibrated probabilities
   - Can filter low-confidence results (<0.7) and show "unclear, please retake" message
4. **PyTorch ecosystem:** Easy integration with product search ML models
   - Many e-commerce companies already use PyTorch for recommendations
5. **Good enough accuracy:** 92-96% on product labels sufficient
   - PaddleOCR's 2-3% higher accuracy not worth tradeoff for this use case
   - Multi-language handling more valuable

**Why not PaddleOCR:**
- Optimized for Chinese documents, not multi-language scene text
- Product labels often have English brands, Japanese product names
- EasyOCR's simultaneous multi-language recognition is killer feature

**Why not Tesseract:**
- Poor scene text accuracy (50-70% on product photos)
- No multi-language simultaneous recognition
- Much slower (3-6s vs 0.5-1s)

### Architecture

```python
# FastAPI service
from fastapi import FastAPI, File, UploadFile
from easyocr import Reader
import numpy as np
from PIL import Image
import io

app = FastAPI()

# Load model once at startup
reader = Reader(['ch_sim', 'en', 'ja'], gpu=True)

@app.post("/ocr/product")
async def extract_product_text(image: UploadFile):
    # Load image
    image_bytes = await image.read()
    img = Image.open(io.BytesIO(image_bytes))

    # Pre-processing
    img = enhance_contrast(img)
    img = resize_if_needed(img, max_size=1920)

    # OCR
    results = reader.readtext(np.array(img))

    # Post-processing
    filtered_results = [
        {"text": text, "confidence": conf}
        for bbox, text, conf in results
        if conf > 0.7  # Filter low-confidence
    ]

    # Sort by position (top-to-bottom) - product name usually at top
    filtered_results = sort_by_position(filtered_results, [bbox for bbox, _, _ in results])

    return {
        "product_texts": filtered_results,
        "status": "success" if filtered_results else "low_confidence"
    }
```

### Processing Pipeline

**1. Pre-processing (Client-side, Mobile App):**
```python
# Resize large images before upload (reduce bandwidth)
def prepare_image_for_upload(image, max_size=1920):
    if max(image.size) > max_size:
        image.thumbnail((max_size, max_size), Image.LANCZOS)
    return image
```

**2. Server-side Pre-processing:**
```python
def enhance_contrast(img):
    """Improve text clarity for low-light captures"""
    from PIL import ImageEnhance
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(1.5)

def resize_if_needed(img, max_size=1920):
    """EasyOCR has max canvas size"""
    if max(img.size) > max_size:
        img.thumbnail((max_size, max_size), Image.LANCZOS)
    return img
```

**3. OCR Inference:**
```python
# Enable paragraph mode to group related text
results = reader.readtext(
    img,
    paragraph=True,  # Group into paragraphs (product name often one block)
    min_size=10,     # Ignore very small text (ingredient lists)
    text_threshold=0.7,  # Confidence threshold
    low_text=0.4
)
```

**4. Post-processing and Ranking:**
```python
def rank_product_texts(results):
    """Prioritize likely product name/brand"""
    scored_results = []

    for bbox, text, conf in results:
        score = conf  # Start with OCR confidence

        # Boost score for top region (product name usually at top)
        y_pos = bbox[0][1]  # Top-left y coordinate
        if y_pos < image_height * 0.3:
            score *= 1.2

        # Boost score for larger text (brand/product name larger)
        text_height = bbox[2][1] - bbox[0][1]
        if text_height > 50:
            score *= 1.1

        # Boost score if contains brand keywords
        if contains_known_brand(text):
            score *= 1.3

        scored_results.append((text, score))

    # Return top 3-5 candidates
    return sorted(scored_results, key=lambda x: x[1], reverse=True)[:5]
```

### Error Handling Strategy

**1. Low Confidence Detection:**
```python
if all(conf < 0.7 for _, conf in filtered_results):
    return {
        "status": "low_confidence",
        "message": "Photo unclear. Try better lighting or closer angle.",
        "retry_suggestions": [
            "Move closer to product",
            "Ensure good lighting",
            "Hold camera steady"
        ]
    }
```

**2. Fallback to Manual Entry:**
```python
if not filtered_results:
    return {
        "status": "no_text_found",
        "fallback_options": [
            "manual_barcode_entry",
            "text_search",
            "browse_categories"
        ]
    }
```

**3. Hybrid Approach (OCR + Barcode):**
```python
# Try barcode first (faster, more accurate if available)
barcode = detect_barcode(image)
if barcode:
    return lookup_by_barcode(barcode)

# Fall back to OCR for products without barcodes
return extract_text_and_search(image)
```

## Success Metrics

### Key Performance Indicators

**Accuracy Metrics:**
- **Primary:** Product match rate (% of scans that find correct product)
  - Target: >85% (including retries)
  - Measured: Log OCR text + search result, sample 1000/day for human validation
- **Secondary:** Character accuracy
  - Target: >90% character-level
  - Measured: Benchmark dataset updated monthly

**Performance Metrics:**
- **Latency:** P95 <2s, P99 <4s
  - Measured: End-to-end time from image upload to search results
- **Throughput:** 10,000 requests/minute sustained
  - Measured: Load test weekly, monitor production metrics

**User Experience Metrics:**
- **Retry rate:** <30% (users who retake photo)
  - Measured: Track retry button clicks
- **Fallback rate:** <15% (users who give up on scan, use manual entry)
  - Measured: Track manual entry after failed scan

### Failure Modes and Detection

**1. Blurry Images (Motion Blur):**
- Detection: Low average confidence scores across all detected text
- Mitigation: Ask user to retake, show "hold steady" animation
- Metric: % of images with avg_confidence < 0.6

**2. Glare/Reflections:**
- Detection: Large white regions, low text detection count
- Mitigation: Guide user to adjust angle
- Metric: % of images with <3 text regions detected

**3. Wrong Language Model:**
- Detection: Gibberish output (detected text not in any character set)
- Mitigation: EasyOCR's multi-language reduces this, but monitor
- Metric: % of outputs with >50% unrecognized characters

**4. Rare/Artistic Fonts:**
- Detection: Low confidence on large text (usually high-confidence)
- Mitigation: Accept lower accuracy, rely on search fuzzy matching
- Metric: % of large text regions with confidence <0.75

## Cost Analysis

### Infrastructure Costs (Monthly)

**Compute:**
- 20 GPU instances (NVIDIA T4): $200/month each = $4,000
- Load balancers, API gateways: $500
- Image storage (CDN, temporary): $300
- Monitoring, logging: $200
- **Total compute: $5,000/month**

**Bandwidth:**
- 10M requests/day × 30 days × 500KB avg image = 150TB/month
- CDN egress: $0.05/GB = $7,500/month
- **Total bandwidth: $7,500/month**

**Total Infrastructure: ~$12,500/month**

### Cost Per Recognition

**Per-image cost:**
- Infrastructure: $12,500 / (10M × 30) = **$0.00004 per image**
- Extremely low cost at scale

### Development and Maintenance (Annual)

**Initial Development:**
- Backend service: 3 weeks × 1 engineer = $15,000
- Mobile app integration: 2 weeks × 1 engineer = $10,000
- Testing and QA: 1 week × 2 engineers = $10,000
- **Total initial: $35,000**

**Ongoing Maintenance:**
- DevOps: 20% of 1 engineer = $20,000/year
- Model updates: 10% of 1 engineer = $10,000/year
- Bug fixes: $5,000/year
- **Total annual: $35,000/year**

### 3-Year TCO

| Component | Year 1 | Year 2 | Year 3 | Total |
|-----------|--------|--------|--------|-------|
| Infrastructure | $150,000 | $150,000 | $150,000 | $450,000 |
| Development | $35,000 | $0 | $0 | $35,000 |
| Maintenance | $35,000 | $35,000 | $35,000 | $105,000 |
| **Total** | **$220,000** | **$185,000** | **$185,000** | **$590,000** |

**Cost per recognition:** $590,000 / (10M × 30 × 36) = **$0.00005**

### Comparison to Commercial API

**Google Cloud Vision API:**
- $1.50 per 1,000 requests for OCR
- 10M requests/day × 30 days = 300M requests/month
- Cost: 300M × $1.50 / 1000 = **$450,000/month**
- 3-year cost: **$16.2 million**

**Savings with EasyOCR:**
- $16.2M - $590K = **$15.6M saved over 3 years**
- ROI: 2550% return on infrastructure investment

## Conclusion

**Summary:** EasyOCR is the optimal solution for e-commerce product label recognition due to:
1. Excellent multi-language support (Chinese + English + Japanese/Korean simultaneously)
2. Strong scene text performance (90-95% on product photos)
3. Cost-effective at scale (<$0.0001 per image)
4. Fast inference (50-100ms with GPU)
5. Easy integration (PyTorch ecosystem familiar to e-commerce companies)

**Tradeoffs Accepted:**
- Slightly lower Chinese accuracy than PaddleOCR (92% vs 96%)
  - Acceptable: Product search has fuzzy matching, 92% sufficient
- Larger dependency footprint (PyTorch ~1-3GB)
  - Acceptable: Running on cloud servers with ample storage

**Success Criteria:**
- >85% product match rate ✓ (EasyOCR's 92% text accuracy sufficient)
- <2s P95 latency ✓ (50-100ms OCR + 1-2s search)
- Cost <$0.001 per recognition ✓ ($0.00005 achieved)

**Recommendation:** Proceed with EasyOCR-based implementation.
