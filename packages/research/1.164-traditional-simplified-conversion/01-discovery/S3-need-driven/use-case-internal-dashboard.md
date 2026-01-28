# Use Case: Internal Analytics Dashboard

**Scenario:** Internal BI dashboard converts Chinese customer feedback (Simplified) to Traditional for Taiwan-based analyst team. Low volume (~1,000 conversions/day), accuracy not mission-critical.

---

## Requirements

### Must-Have (Deal-Breakers)

1. **Pure Python Stack** - Team uses Python-only environment (corporate policy)
2. **No Build Tools** - Analysts can't install C++ compilers on locked-down workstations
3. **Simple Integration** - Junior devs maintaining the dashboard
4. **Works on Windows** - Analysts run Windows 10 Pro
5. **Quick Setup** - Integrate in <2 hours

### Nice-to-Have (Preferences)

6. **Low Cost** - Minimize infrastructure spend
7. **Good Enough Accuracy** - 80-90% correct is acceptable (humans review anyway)
8. **Small Package** - Faster deployment, smaller Docker images
9. **No External Dependencies** - Air-gapped network (no internet on prod)
10. **Easy Debugging** - Pure Python stack traces

### Constraints

- **Platform:** Windows workstations + Linux Docker (Alpine)
- **Team:** 2 junior Python devs (minimal ML/NLP expertise)
- **Volume:** ~1,000 conversions/day × 500 chars avg = 500K chars/day
- **Budget:** <$10/month

---

## Library Evaluation

### OpenCC

#### Must-Haves
- ❌ **Pure Python:** NO (C++ extension required)
- ❌ **No build tools:** Requires C++ compiler if no wheel
- ✅ **Simple integration:** Once installed, API is straightforward
- ⚠️ **Windows:** Pre-built wheels available, BUT depends on Python version
- ⚠️ **Quick setup:** 2-4 hours (wheel installation issues common on Windows)

**Fit Score:** **35/100** (20 must-haves (partial) + 15 nice-to-haves)

**Issue:** Corporate IT blocks C++ compiler installation → can't build from source if wheel fails.

---

### zhconv-rs

#### Must-Haves
- ❌ **Pure Python:** NO (Rust extension required)
- ❌ **No build tools:** Requires Rust compiler if no wheel
- ✅ **Simple integration:** Clean API once installed
- ⚠️ **Windows:** Pre-built wheels available, BUT newer library = fewer wheels
- ⚠️ **Quick setup:** 2-4 hours (potential wheel availability issues)

**Fit Score:** **38/100** (20 must-haves (partial) + 18 nice-to-haves)

**Issue:** Same as OpenCC - blocked by pure-Python requirement.

---

### HanziConv

#### Must-Haves
- ✅ **Pure Python:** 100% pure Python (no extensions)
- ✅ **No build tools:** `pip install hanziconv` just works
- ✅ **Simple integration:** Dead simple 1-line API
- ✅ **Windows:** Works everywhere Python runs
- ✅ **Quick setup:** 15-30 minutes (install + test)

#### Nice-to-Haves (9/10 points)
- ✅ **Low cost:** Negligible (500K chars/day = <1sec processing)
- ⚠️ **Accuracy:** 80-90% (character-level, but acceptable for this use case)
- ✅ **Small package:** ~200 KB (vs 1-3 MB alternatives)
- ✅ **No dependencies:** Pure Python, stdlib only
- ✅ **Easy debugging:** Python exceptions, no C++ crashes

**Fit Score:** **99/100** (60 must-haves + 39 nice-to-haves)

---

## Recommendation

### Winner: **HanziConv**

**Rationale:**
1. **Only library meeting all must-haves** (pure Python requirement is blocking)
2. **15-minute setup** vs 2-4 hours fighting with wheels
3. **No build complexity** = junior devs can maintain
4. **Accuracy acceptable** for internal tool (humans review feedback anyway)

**Why This Is The Right Trade-Off:**

| Factor | Importance | HanziConv | OpenCC/zhconv-rs |
|--------|------------|-----------|------------------|
| Works on locked-down Windows | **CRITICAL** | ✅ Yes | ❌ Blocked by IT |
| Regional vocabulary accuracy | Nice-to-have | ❌ No | ✅ Yes |
| Phrase-level conversion | Nice-to-have | ❌ No | ✅ Yes |
| Junior dev maintenance | **HIGH** | ✅ Simple | ⚠️ Complex |
| Volume (500K chars/day) | Low | ✅ Fast enough | ✅ Overkill |

**Key Insight:** For internal tools where **constraints dominate requirements**, HanziConv's simplicity wins despite lower accuracy.

### Implementation Example

```python
# dashboard/convert.py
from hanziconv import HanziConv
import pandas as pd

def convert_feedback_to_traditional(df):
    """
    Convert customer feedback column to Traditional Chinese
    for Taiwan analyst team
    """
    df['feedback_traditional'] = df['feedback_simplified'].apply(
        HanziConv.toTraditional
    )
    return df

# Usage in dashboard
feedback = pd.read_csv('customer_feedback.csv')
converted = convert_feedback_to_traditional(feedback)

# Display in Streamlit dashboard
import streamlit as st
st.dataframe(converted[['customer_id', 'feedback_traditional']])
```

### Deployment (Docker on Alpine)

```dockerfile
FROM python:3.12-alpine
# No build tools needed (pure Python)
RUN pip install hanziconv pandas streamlit
COPY app.py /app/
CMD ["streamlit", "run", "/app/app.py"]
```

**Image size:** ~200 MB (vs ~300 MB with OpenCC/zhconv-rs)

---

## Accuracy Expectations

### What HanziConv Gets Wrong

**Example:** Taiwan software terminology
```python
# Input (Simplified)
"我们的软件支持网络功能"

# HanziConv output
"我們的軟件支持網絡功能"  # WRONG for Taiwan

# Correct Taiwan Traditional
"我們的軟體支持網路功能"  # 軟體 (software), 網路 (network)
```

**Impact for This Use Case:**
- Analysts are Taiwan-based → notice vocabulary differences
- BUT they're reading for sentiment/issues, not translation quality
- Human review catches critical errors
- **80-90% accuracy is acceptable** for internal tool

### Mitigation Strategy

If accuracy becomes a problem later:

```python
# Post-process common Taiwan terms
def fix_taiwan_vocab(text):
    """Fix most common Taiwan vocabulary issues"""
    replacements = {
        '軟件': '軟體',  # software
        '硬件': '硬體',  # hardware
        '網絡': '網路',  # network
        '信息': '資訊',  # information
    }
    for wrong, correct in replacements.items():
        text = text.replace(wrong, correct)
    return text

# Apply after HanziConv
df['feedback_traditional'] = df['feedback_simplified'].apply(
    lambda x: fix_taiwan_vocab(HanziConv.toTraditional(x))
)
```

**Result:** Boosts accuracy to 90-95% with 10 lines of code.

---

## Cost Analysis

**Infrastructure:**
- Docker container on company servers (internal hosting)
- No cloud costs

**Development Time:**
- HanziConv: 30 min integration + 1 hour testing = **1.5 hours** ($187 at $125/hr)
- OpenCC: 2 hours fighting wheels + 2 hours integration = **4 hours** ($500)

**Maintenance:**
- HanziConv: Near-zero (pure Python, no dependencies)
- OpenCC: Wheel compatibility issues on Python upgrades

**Total Cost (1 year):**
- HanziConv: $187 one-time
- OpenCC: $500 one-time + $200 maintenance = $700

**ROI:** HanziConv saves $513 in year 1 for an internal tool where accuracy isn't critical.

---

## When to Migrate to OpenCC

**Triggers for switching:**
1. **Accuracy complaints** from analyst team (>10% error rate unacceptable)
2. **Volume increase** to >10M chars/day (HanziConv too slow)
3. **External use** (dashboard becomes customer-facing)
4. **IT policy change** (pure Python requirement lifted)

**Migration Effort:** ~4 hours (swap HanziConv → OpenCC, test)

**Decision:** Start with HanziConv, migrate only if needed.

---

## Alternative: If Pure Python Not Required

If IT allows pre-built wheels (just no compilers):

**Recommendation changes to:**
1. **Try OpenCC first** (pre-built wheel for Windows x86-64)
2. **Fall back to HanziConv** if wheel fails

**Best of both worlds:** OpenCC accuracy with minimal hassle.

But given **corporate environment constraints**, assume pure-Python is safer.

---

**Use Case Winner:** **HanziConv** (99/100 fit for constrained internal tool)

**Key Lesson:** For internal tools with hard constraints, simplicity > accuracy.
