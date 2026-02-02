# Use Case: Content Moderation at Scale

## Who Needs This

**Persona**: Security Engineering Team at Social/UGC Platform
- **Company**: User-generated content platform (forums, comments, reviews)
- **Team Size**: 3-person security team
- **Scale**: 1M posts/day, 10K banned phrases
- **Challenge**: Detect prohibited content in real-time without false positives

## Why This Matters

**Business Problem:**
- Legal liability: Must block illegal content (hate speech, scams, threats)
- Brand safety: Advertisers require clean platform
- User experience: Toxic content drives away users
- Regulatory compliance: GDPR, COPPA, local laws

**Pain Point:**
Current keyword filter (simple regex) has issues:
- **Too slow**: Regex with 10K patterns times out (> 5 seconds per post)
- **Catastrophic backtracking**: Some user posts cause regex DoS
- **High false positive rate**: "Scunthorpe problem" (legitimate words blocked)
- **Easy to bypass**: Users replace letters ("b@d w0rd")

**Goal:**
Detect 10K+ banned phrases in < 100ms per post with predictable performance (no DoS risk).

## Requirements

### Must-Have Features

✅ **Multi-pattern matching** - Check 10,000+ phrases simultaneously
✅ **Low latency** - < 100ms per post (user-facing, can't delay posting)
✅ **Predictable performance** - No catastrophic backtracking (security risk)
✅ **Case-insensitive** - "BadWord" = "badword"
✅ **Unicode support** - Moderation works across languages

### Nice-to-Have Features

⚪ **Fuzzy matching** - Catch "b@d" for "bad" (character substitution)
⚪ **Context-aware** - "kill it" (OK in gaming) vs "kill you" (threat)
⚪ **Confidence scores** - Borderline cases go to human review

### Constraints

📊 **Scale:** 1M posts/day = ~12 posts/second average, 50/sec peak
⏱️ **Latency:** < 100ms p95 (synchronous check before post publish)
💰 **Budget:** Moderate - infrastructure costs acceptable, but cost-conscious
🛠️ **Team:** 3 security engineers, not NLP specialists
🔒 **Security:** Cannot allow user input to cause DoS (critical)

### Success Criteria

- Detect 95% of banned phrases (minimize misses)
- < 2% false positive rate (don't block legitimate content)
- < 100ms p95 latency
- Zero DoS vulnerabilities (handle malicious input safely)

---

## Library Evaluation

### pyahocorasick - Fit Analysis

**Must-Haves:**
- ✅✅ **Multi-pattern**: Designed for this (10K patterns = O(n), not O(n×k))
- ✅✅ **Low latency**: O(n + z) linear time = < 10ms for typical post
- ✅✅ **Predictable**: Worst-case = best-case (no backtracking DoS)
- ✅ **Case-insensitive**: Configurable via automaton settings
- ✅ **Unicode**: Full support

**Nice-to-Haves:**
- ⚠️ **Fuzzy matching**: Limited (not primary strength)
- ❌ **Context-aware**: No built-in context analysis
- ⚪ **Confidence scores**: Exact match only (binary yes/no)

**Constraints:**
- 📊 **Scale**: 50 posts/sec × 10ms = 500ms total → easily handled by single server
- ⏱️ **Latency**: 10ms typical << 100ms SLA ✅✅
- 💰 **Budget**: Minimal infrastructure (CPU-only, low memory)
- 🛠️ **Team**: Learning curve moderate (automaton pattern)
- 🔒 **Security**: **Perfect fit** - O(n) guaranteed, no DoS risk ✅✅

**Fit Score:** 95/100

---

### google-re2 - Fit Analysis

**Must-Haves:**
- ⚠️ **Multi-pattern**: Can combine patterns with `|` but not optimized
- ✅ **Low latency**: O(n) linear time
- ✅✅ **Predictable**: DFA guarantees (DoS-safe)
- ✅ **Case-insensitive**: Regex flag support
- ✅ **Unicode**: Supported

**Constraints:**
- 📊 **Scale**: Linear time, but slower than pyahocorasick for multi-pattern
- ⏱️ **Latency**: DFA compilation overhead for 10K patterns (slower)
- 🔒 **Security**: DoS-safe ✅

**Fit Score:** 70/100

**Why Not Primary:**
- Not optimized for multi-pattern (pyahocorasick designed for this)
- Slower DFA compilation with 10K patterns
- RE2 better for untrusted *regex patterns*, not keyword lists

---

### RapidFuzz - Fit Analysis

**Must-Haves:**
- ❌ **Multi-pattern**: Would need to check each pattern individually (O(n × k) = too slow)
- ❌ **Low latency**: 10K patterns × 1ms = 10 seconds per post ❌

**Fit Score:** 20/100

**Why Not:**
Fuzzy matching library, not multi-pattern exact search. Wrong tool for this job.

---

## Comparison Matrix

| Requirement | pyahocorasick | google-re2 | RapidFuzz |
|-------------|---------------|------------|-----------|
| **Multi-pattern (10K)** | ✅✅ O(n) | ⚠️ O(n) but slower | ❌ O(n×k) |
| **Latency (<100ms)** | ✅✅ ~10ms | ⚠️ ~50ms | ❌ 10s+ |
| **DoS-safe** | ✅✅ | ✅✅ | ✅ (not relevant) |
| **Fuzzy matching** | ⚠️ Limited | ❌ | ✅ |
| **Memory** | Low | DFA size varies | N/A |

---

## Recommendation

### Primary: **pyahocorasick**

**Fit: 95/100**

**Rationale:**

1. **Designed for multi-pattern exact matching**: This is *exactly* pyahocorasick's use case
   - O(n + z) regardless of pattern count
   - 10 patterns: ~10ms
   - 10,000 patterns: Still ~10ms (same!)

2. **DoS-resistant**: Linear time guaranteed (no backtracking)
   - Malicious input cannot cause slowdown
   - Critical for security-sensitive moderation

3. **Proven at scale**: Used in antivirus, IDS/IPS, content filtering

4. **Low latency**: ~10ms typical << 100ms SLA (10× headroom)

**Implementation Approach:**

```python
import ahocorasick

# Build automaton once (at startup)
banned_automaton = ahocorasick.Automaton()
for phrase in banned_phrases:  # 10,000 phrases
    banned_automaton.add_word(phrase.lower(), phrase)
banned_automaton.make_automaton()

# Check content (< 10ms for typical post)
def check_content(post_text):
    matches = []
    for end_index, phrase in banned_automaton.iter(post_text.lower()):
        matches.append(phrase)

    if matches:
        return {"blocked": True, "reasons": matches}
    return {"blocked": False}
```

**Performance:**
- Build time: ~1 second for 10K patterns (one-time at startup)
- Match time: ~10ms for 1000-character post
- Memory: ~1-5 MB for automaton (minimal)

---

### Handling Fuzzy Matching (Character Substitution)

**Problem:** Users bypass filters with "b@d w0rd"

**Solution: Two-tier approach**
1. **Tier 1: Exact match** (pyahocorasick) - catches 90% of violations
2. **Tier 2: Normalization + fuzzy** (for borderline cases flagged by ML model)

```python
# Normalize common substitutions
def normalize(text):
    replacements = {"@": "a", "0": "o", "1": "i", "3": "e", "$": "s"}
    for char, repl in replacements.items():
        text = text.replace(char, repl)
    return text

# Check both original and normalized
matches_original = check_with_ahocorasick(post_text)
matches_normalized = check_with_ahocorasick(normalize(post_text))
```

**Trade-off:**
- Increases false positives slightly (e.g., "g00d" → "good" → flagged if "good" blocked)
- Mitigate with ML confidence scoring (human review for borderline cases)

---

### Alternative: **google-re2** (if regex patterns needed)

**When to consider:**
- Banned "patterns" not just "phrases" (e.g., "credit card number regex")
- Need regex features (anchors, character classes)

**Trade-off:**
- Slower DFA compilation with many patterns
- More complex than keyword matching

---

## Key Insights

**S3 reveals pyahocorasick's perfect fit**: Content moderation with 1,000+ keywords is the canonical use case for Aho-Corasick algorithm. Performance *doesn't degrade* as pattern count grows.

**Security matters**: DoS risk from catastrophic backtracking is real. RE2 or pyahocorasick provide guaranteed O(n) time. Standard regex (re/regex) are unsafe for untrusted input with complex patterns.

**Exact matching often sufficient**: Most content moderation starts with exact keyword matching. Add fuzzy matching only if bypass attempts become common (iterative improvement).

---

## Validation Data

**Industry benchmarks:**
- pyahocorasick: 1-20ms for 10K patterns (typical content length)
- Regex (10K patterns with `|`): 100ms - 5 seconds (catastrophic cases)
- RE2 (10K patterns): 30-100ms (slower than pyahocorasick but faster than regex)

**Production usage:**
- Wikipedia uses Aho-Corasick for spam detection
- Antivirus software uses it for signature matching
- Web proxies use it for URL filtering
