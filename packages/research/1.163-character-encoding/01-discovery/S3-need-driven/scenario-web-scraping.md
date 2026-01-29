# Scenario: E-Commerce Web Scraping (Multi-Region)

## Context

**Business**: Price comparison service aggregating products from Taiwan, Mainland China, Hong Kong sites
**Current state**: Scrapers collect HTML, but encoding detection is unreliable
**Goal**: Normalize all content to UTF-8 for search indexing and display
**Volume**: 50,000 pages/day across 200 sites
**Data type**: Product titles, descriptions, prices, reviews

## Requirements Analysis

| Requirement | Priority | Constraint |
|-------------|----------|------------|
| **Accuracy** | HIGH | Display errors reduce user trust |
| **Performance** | CRITICAL | Real-time updates (5-minute freshness) |
| **Robustness** | CRITICAL | Sites lie about encoding, change without notice |
| **Coverage** | HIGH | Must handle all major Chinese sites |
| **Cost** | MEDIUM | Scraping at scale (cloud costs) |

### Pain Points

1. **Meta tags lie**: Site claims UTF-8, actually serves Big5
2. **Mixed encodings**: Header says GBK, JavaScript inserts UTF-8
3. **Mojibake from proxies**: CDN/proxies double-encode
4. **No meta tag**: Some sites don't declare encoding
5. **Dynamic content**: JavaScript-rendered content may use different encoding

## Library Selection

### Detection: **charset-normalizer** (accuracy matters)
- Sites lie, can't trust meta tags
- Need multiple hypotheses (show alternatives)
- Explanation helps debug problematic sites

### Transcoding: **Python codecs**
- Standard library, reliable

### Repair: **ftfy** (conditional)
- Use if detection confidence < 90%
- Common on sites with proxy/CDN issues

### CJK Conversion: **zhconv** (normalization)
- Normalize Traditional/Simplified for search
- Fast (50,000 pages/day)

## Integration Pattern

```python
import requests
from charset_normalizer import from_bytes
import ftfy
import zhconv
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def scrape_product_page(url):
    """
    Scrape product page with robust encoding handling

    Returns:
        dict: {
            'url': str,
            'title': str,
            'price': str,
            'description': str,
            'encoding_detected': str,
            'encoding_confidence': float,
            'repaired': bool,
        }
    """
    try:
        # Step 1: Fetch page
        response = requests.get(url, timeout=10)
        raw_html = response.content

        # Step 2: Detect encoding (ignore Content-Type header)
        result = from_bytes(raw_html)
        best = result.best()

        if best is None:
            logger.warning(f"Could not detect encoding for {url}")
            # Fallback to UTF-8
            html = raw_html.decode('utf-8', errors='replace')
            confidence = 0.0
            repaired = False
        else:
            html = str(best)
            confidence = best.encoding_confidence
            repaired = False

            # Step 3: Repair if low confidence
            if confidence < 0.9:
                logger.info(f"Low confidence ({confidence}) for {url}, attempting repair")
                html = ftfy.fix_text(html)
                repaired = True

        # Step 4: Parse HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Extract data
        title = soup.find('h1', class_='product-title')
        price = soup.find('span', class_='price')
        description = soup.find('div', class_='description')

        # Step 5: Normalize for search (convert all to Simplified)
        title_normalized = zhconv.convert(title.text, 'zh-cn') if title else ''
        desc_normalized = zhconv.convert(description.text, 'zh-cn') if description else ''

        return {
            'url': url,
            'title': title_normalized,
            'price': price.text if price else '',
            'description': desc_normalized,
            'encoding_detected': best.encoding if best else 'utf-8',
            'encoding_confidence': confidence,
            'repaired': repaired,
        }

    except requests.RequestException as e:
        logger.error(f"Request failed for {url}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error scraping {url}: {e}")
        return None
```

## Error Handling Strategy

### 1. Multi-Hypothesis Detection
```python
def smart_detect_with_alternatives(raw_html, meta_charset=None):
    """
    Detect encoding with fallback to meta tag if detection uncertain
    """
    # Try detection first
    result = from_bytes(raw_html)
    best = result.best()

    if best and best.encoding_confidence > 0.85:
        # High confidence, use detection
        return str(best)

    # Low confidence, check meta tag
    if meta_charset:
        try:
            # Try meta charset
            html = raw_html.decode(meta_charset, errors='strict')
            return html
        except UnicodeDecodeError:
            pass  # Meta tag was wrong, fall back to detection

    # Use detection result even if low confidence
    if best:
        html = str(best)
        # Repair since confidence is low
        return ftfy.fix_text(html)

    # Last resort: UTF-8 with replacement
    return raw_html.decode('utf-8', errors='replace')
```

### 2. Handle Mixed Encodings
```python
def extract_with_encoding_repair(soup, selector):
    """
    Extract text, repair mojibake if detected
    """
    element = soup.select_one(selector)
    if not element:
        return ''

    text = element.get_text()

    # Heuristic: if text has replacement chars, try repair
    if '�' in text or '?' in text:
        text = ftfy.fix_text(text)

    return text
```

### 3. Retry with Alternative Encoding
```python
def scrape_with_retry(url, max_attempts=3):
    """
    Retry with different encoding strategies if first attempt fails
    """
    encodings_to_try = [
        None,  # Auto-detect
        'utf-8',
        'big5',
        'gbk',
        'gb18030',
    ]

    for i, encoding in enumerate(encodings_to_try[:max_attempts]):
        try:
            result = scrape_with_encoding(url, encoding)
            if result and result['title']:  # Basic validation
                return result
        except Exception as e:
            logger.warning(f"Attempt {i+1} failed for {url}: {e}")
            continue

    # All attempts failed
    return None
```

## Performance Optimization

### Parallel Scraping
```python
from concurrent.futures import ThreadPoolExecutor
import time

def scrape_batch(urls, max_workers=20):
    """
    Scrape multiple URLs in parallel
    """
    results = []
    failed = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_url = {executor.submit(scrape_product_page, url): url for url in urls}

        # Collect results
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result(timeout=30)
                if result:
                    results.append(result)
                else:
                    failed.append(url)
            except Exception as e:
                logger.error(f"Failed to scrape {url}: {e}")
                failed.append(url)

    return results, failed
```

**Performance estimate**:
- Single page: 200ms (fetch) + 100ms (detect) + 50ms (parse) = 350ms
- 50,000 pages/day = ~34 pages/minute
- With 20 workers: 20 × 34 = 680 pages/minute = 41,000 pages/hour
- **Can process daily volume in <90 minutes**

### Caching Detection Results
```python
import hashlib
from functools import lru_cache

@lru_cache(maxsize=1000)
def detect_encoding_cached(content_hash):
    """
    Cache detection results for identical content
    """
    # (In reality, pass actual bytes, not hash)
    # This is conceptual - shows caching strategy
    pass

def scrape_with_cache(url):
    response = requests.get(url)
    content_hash = hashlib.md5(response.content).hexdigest()

    # Check if we've seen this exact content before
    cached_encoding = get_from_cache(content_hash)
    if cached_encoding:
        html = response.content.decode(cached_encoding)
    else:
        # Detect and cache
        result = from_bytes(response.content)
        encoding = result.best().encoding
        save_to_cache(content_hash, encoding)
        html = str(result.best())

    # ... rest of scraping
```

## Testing Strategy

### Site-Specific Tests
```python
# Build test suite from actual problematic sites
test_sites = [
    {
        'url': 'https://example.tw/product/1',
        'expected_encoding': 'big5',
        'meta_charset': 'utf-8',  # Lies!
        'expected_title': '筆記型電腦',
    },
    {
        'url': 'https://example.cn/product/2',
        'expected_encoding': 'gbk',
        'has_mojibake': True,
        'expected_title_after_repair': '笔记本电脑',
    },
]

def test_site_scraping():
    for test in test_sites:
        result = scrape_product_page(test['url'])
        assert result['encoding_detected'] == test['expected_encoding']
        if test.get('has_mojibake'):
            assert result['repaired']
        assert test['expected_title'] in result['title']
```

### Regression Testing
```python
# Capture HTML snapshots of problematic sites
# Re-test after library updates to ensure no regressions

def test_regression_big5_site():
    # Load saved HTML from file
    with open('test_data/big5_site_snapshot.html', 'rb') as f:
        html = f.read()

    result = from_bytes(html)
    assert result.best().encoding == 'big5'
    assert result.best().encoding_confidence > 0.9
```

## Monitoring & Alerts

```python
# Track encoding distribution
encoding_stats = {
    'utf-8': 0,
    'big5': 0,
    'gbk': 0,
    'unknown': 0,
}

# Track confidence
low_confidence_urls = []  # Log for manual review

# Track repair rate
repair_rate = repaired / total

# Alerts
if repair_rate > 0.2:  # >20% need repair
    alert('High mojibake rate - check sites')

if encoding_stats['unknown'] / total > 0.05:  # >5% unknown
    alert('Detection failure rate high')
```

## Site-Specific Overrides

```python
# Maintain database of known problematic sites
SITE_OVERRIDES = {
    'example.tw': {
        'encoding': 'big5',  # Force Big5, don't detect
        'repair': False,  # Don't repair, clean encoding
    },
    'example.cn': {
        'encoding': 'gbk',
        'repair': True,  # Known mojibake from proxy
    },
}

def scrape_with_overrides(url):
    domain = extract_domain(url)

    if domain in SITE_OVERRIDES:
        override = SITE_OVERRIDES[domain]
        # Use override settings
        html = response.content.decode(override['encoding'])
        if override['repair']:
            html = ftfy.fix_text(html)
    else:
        # Standard detection pipeline
        html = detect_and_decode(response.content)
```

## Trade-offs & Decisions

| Decision | Chosen | Alternative | Rationale |
|----------|--------|-------------|-----------|
| **Detection** | charset-normalizer | cchardet | Accuracy > speed for display quality |
| **Repair** | Conditional ftfy | Always repair | Only repair low-confidence (reduce false positives) |
| **CJK normalize** | zhconv (fast) | OpenCC | Search normalization, speed matters |
| **Error handling** | Log + continue | Fail on error | Can't let one bad site break entire scrape |
| **Parallelism** | 20 workers | More workers | Balance throughput vs server load |

## Success Criteria

- [ ] 95%+ of pages scraped successfully
- [ ] <5% need mojibake repair
- [ ] Detection confidence >85% on average
- [ ] No user complaints about garbled text
- [ ] Process daily volume within 2 hours
- [ ] Cost within budget (<$500/month infrastructure)

## Estimated Effort

- Development: 1 week (scraper + encoding pipeline + tests)
- Testing: 1 week (build test suite from real sites)
- Rollout: Gradual (add sites incrementally)
- Maintenance: Ongoing (new sites, encoding changes)
