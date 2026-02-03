# Web Application Scenarios

## Scenario 1: Search Autocomplete

### Problem
Provide real-time search suggestions as user types, matching across product names, descriptions, and tags.

### Constraints
- Sub-100ms latency requirement
- Fuzzy matching (typo tolerance)
- Unicode support (international products)
- Client-side execution (reduce server load)

### Solution
**fuse.js (JavaScript) for client-side**
```javascript
const fuse = new Fuse(products, {
  keys: ['name', 'description', 'tags'],
  threshold: 0.3,  // 0 = exact, 1 = match anything
  distance: 100    // Max distance for match
});

const results = fuse.search(query).slice(0, 10);
```

**Rationale**:
- Lightweight (~12KB gzipped)
- Fast enough for client-side
- Good fuzzy matching via Bitap
- Works with Unicode

**Alternatives**:
- **Server-side with Elasticsearch**: For large datasets (millions)
- **Whoosh (Python)**: For server-side with moderate data
- **Tantivy (Rust)**: High-performance server-side search

### Pitfalls
- ❌ Fuzzing entire dataset on each keystroke (use debouncing)
- ❌ Not lowercasing/normalizing before indexing
- ❌ Threshold too loose (irrelevant results) or tight (missing near-matches)

## Scenario 2: Input Validation (Email, Phone, etc.)

### Problem
Validate user input fields (email, phone, URL, credit card) before submission.

### Constraints
- Client and server-side validation
- Clear error messages
- Security (no injection)

### Solution
**Regex with sanitization**
```python
import re
from email_validator import validate_email, EmailNotValidError

# Email (use library, don't regex)
try:
    valid = validate_email(email)
    email = valid.email  # Normalized
except EmailNotValidError as e:
    return str(e)

# Phone (international-aware)
import phonenumbers
try:
    number = phonenumbers.parse(phone, region)
    if not phonenumbers.is_valid_number(number):
        return "Invalid phone number"
except phonenumbers.NumberParseException:
    return "Invalid phone format"

# URL
from urllib.parse import urlparse
result = urlparse(url)
if not all([result.scheme, result.netloc]):
    return "Invalid URL"
```

**Rationale**:
- Use specialized libraries instead of regex
- Proper handling of edge cases
- Security-conscious validation

**Alternatives**:
- **Simple regex**: For known-simple formats only
- **HTML5 input types**: Client-side basic validation

### Pitfalls
- ❌ Rolling your own email regex (RFC 5322 is complex)
- ❌ Client-side validation only (users can bypass)
- ❌ Not normalizing before storage (case, whitespace)

## Scenario 3: XSS Prevention in Templates

### Problem
Display user-generated content safely in HTML templates.

### Constraints
- Must escape < > & " ' properly
- Preserve formatting (line breaks, links)
- Good performance (millions of renders)

### Solution
**Auto-escaping template engine**

Python (Jinja2):
```python
from jinja2 import Template
template = Template('<div>{{ user_content }}</div>')  # Auto-escapes
output = template.render(user_content=untrusted)
```

JavaScript (React):
```jsx
<div>{userContent}</div>  {/* Auto-escaped */}
```

Rust (Askama):
```rust
#[derive(Template)]
#[template(path = "user.html")]
struct UserTemplate<'a> {
    content: &'a str  // Auto-escaped
}
```

**Rationale**:
- Auto-escaping is default (opt-out for trusted HTML)
- Context-aware (HTML, JS, CSS, URL)
- Battle-tested implementations

**Alternatives**:
- **Manual escaping**: Only if no template engine available
- **Content Security Policy**: Additional defense layer
- **Markdown with sanitization**: For rich formatting needs

### Pitfalls
- ❌ Disabling auto-escape globally
- ❌ Trusting user HTML (even if "sanitized")
- ❌ Forgetting JavaScript context (different escaping rules)

## Scenario 4: URL Slug Generation

### Problem
Convert article titles to URL-safe slugs: "Hello, World!" → "hello-world"

### Constraints
- ASCII-only for URLs
- No special characters
- Unicode input (article titles in any language)
- Unique slugs (handle collisions)

### Solution
**Unicode normalization + transliteration**

Python:
```python
from slugify import slugify

slug = slugify("Café München 2024", max_length=50)
# Output: "cafe-munchen-2024"

# With uniqueness
def unique_slug(title, existing_slugs):
    base = slugify(title, max_length=45)
    if base not in existing_slugs:
        return base

    # Add counter suffix
    for i in range(1, 1000):
        slug = f"{base}-{i}"
        if slug not in existing_slugs:
            return slug
```

JavaScript:
```javascript
import slugify from 'slugify';

const slug = slugify(title, {
  lower: true,
  strict: true,  // Remove special chars
  locale: 'en'
});
```

**Rationale**:
- Handles Unicode transliteration (ü → u, 中文 → zhong-wen)
- Configurable (max length, separator)
- Consistent across requests

**Alternatives**:
- **Custom base64 encoding**: For non-readable URLs (short IDs)
- **Database-generated IDs**: If SEO not important

### Pitfalls
- ❌ Not handling empty slug (all characters stripped)
- ❌ Very long slugs (truncate with limit)
- ❌ Slug collisions (must check uniqueness)

## Scenario 5: Log Parsing and Search

### Problem
Search application logs for specific patterns, extract structured data.

### Constraints
- Large files (gigabytes)
- Must stream (cannot load entire file)
- Multi-line log entries
- Regex patterns from users

### Solution
**Streaming regex with bounded execution**

Python:
```python
import re
from timeout_decorator import timeout

@timeout(5)  # 5-second timeout
def search_logs(log_file, pattern):
    regex = re.compile(pattern)
    matches = []

    for line in log_file:  # Streaming
        if len(matches) >= 1000:
            break  # Limit results

        match = regex.search(line)
        if match:
            matches.append({
                'line': line,
                'groups': match.groups()
            })

    return matches
```

Rust (ripgrep-style):
```rust
use grep::regex::RegexMatcher;
use grep::searcher::Searcher;

let matcher = RegexMatcher::new(pattern)?;
let mut searcher = Searcher::new();

searcher.search_path(&matcher, path, |lnum, line| {
    // Process match
    Ok(true)
})?;
```

**Rationale**:
- Streaming avoids memory issues
- Timeouts prevent ReDoS
- Result limits prevent overwhelming responses

**Alternatives**:
- **grep/ripgrep**: For command-line use
- **Elasticsearch**: For indexed search at scale
- **CloudWatch Insights**: For cloud logs

### Pitfalls
- ❌ No timeout (ReDoS vulnerability)
- ❌ Loading entire file into memory
- ❌ Unbounded result sets

## Scenario 6: API Rate Limiting by Key

### Problem
Track API usage by key, implement rate limiting.

### Constraints
- Fast lookup (thousands of requests/second)
- Memory-efficient (millions of keys)
- Distributed (multiple servers)

### Solution
**String interning + Redis counter**

Python:
```python
import redis
import sys

# Intern API keys (shared memory)
KEY_POOL = {}

def intern_key(key):
    if key not in KEY_POOL:
        KEY_POOL[key] = sys.intern(key)
    return KEY_POOL[key]

def check_rate_limit(redis_client, api_key):
    key = intern_key(api_key)  # O(1) equality checks

    # Redis sliding window
    now = time.time()
    window = 60  # 1 minute

    pipe = redis_client.pipeline()
    pipe.zadd(f"rate:{key}", {now: now})
    pipe.zremrangebyscore(f"rate:{key}", 0, now - window)
    pipe.zcard(f"rate:{key}")
    pipe.expire(f"rate:{key}", window)

    result = pipe.execute()
    request_count = result[2]

    return request_count <= RATE_LIMIT
```

**Rationale**:
- String interning reduces memory (same key, same object)
- Redis for distributed tracking
- Sliding window more accurate than fixed window

**Alternatives**:
- **In-memory only**: For single server
- **Token bucket**: For burst tolerance
- **API gateway**: Managed rate limiting

### Pitfalls
- ❌ Unbounded intern pool (memory leak)
- ❌ Fixed time windows (allow burst at boundary)
- ❌ No monitoring (can't detect abuse patterns)
