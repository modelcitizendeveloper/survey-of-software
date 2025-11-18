# S1: Rapid Discovery - Classical Language Libraries

**Methodology**: Rapid Discovery (S1)
**Time Budget**: 1-2 hours
**Goal**: Quick hands-on testing to identify obvious winners or showstoppers

## Discovery Approach

### 1. Installation Test (15-30 min)
Test each library for installation ease and dependencies.

### 2. Basic Functionality Test (30-45 min)
Generate sample declensions/conjugations to verify core capabilities.

### 3. First Impressions (15-30 min)
Document API quality, error messages, documentation clarity.

---

## Library 1: CLTK (Classical Language Toolkit)

### Installation

```bash
# Create test environment
cd /tmp
python3 -m venv cltk-test
source cltk-test/bin/activate

# Install CLTK
pip install cltk

# Test import
python -c "from cltk.morphology.latin import CollatinusDecliner; print('CLTK installed successfully')"
```

**Installation time**: ___ minutes
**Issues encountered**:
-
-

**Dependencies installed**:
```bash
pip list | grep cltk
```

### Basic Functionality Test

#### Test 1: First Declension Noun (puella, -ae, f - girl)

```python
from cltk.morphology.latin import CollatinusDecliner

decliner = CollatinusDecliner()

# Generate all forms
print("=" * 50)
print("1st Declension: puella, puellae (f) - girl")
print("=" * 50)

try:
    forms = decliner.decline("puella", declension=1)
    for case, form in forms.items():
        print(f"{case:20s} {form}")
except Exception as e:
    print(f"ERROR: {e}")
```

**Output**:
```
[Paste actual output here]
```

**Observations**:
- Forms correct? Yes/No
- All cases present? (Nom, Gen, Dat, Acc, Abl, Voc × Sg, Pl)
- API intuitive?

#### Test 2: Second Declension Noun (dominus, -i, m - lord)

```python
print("\n" + "=" * 50)
print("2nd Declension: dominus, domini (m) - lord")
print("=" * 50)

try:
    forms = decliner.decline("dominus", declension=2)
    for case, form in forms.items():
        print(f"{case:20s} {form}")
except Exception as e:
    print(f"ERROR: {e}")
```

**Output**:
```
[Paste actual output here]
```

#### Test 3: Third Declension Noun (rex, regis, m - king)

```python
print("\n" + "=" * 50)
print("3rd Declension: rex, regis (m) - king")
print("=" * 50)

try:
    forms = decliner.decline("rex", declension=3)
    for case, form in forms.items():
        print(f"{case:20s} {form}")
except Exception as e:
    print(f"ERROR: {e}")
```

**Output**:
```
[Paste actual output here]
```

#### Test 4: Verb Conjugation (amo, amare - to love)

```python
print("\n" + "=" * 50)
print("1st Conjugation: amo, amare - to love")
print("=" * 50)

# Check if CLTK has verb conjugation
try:
    # Try to find verb conjugation capability
    from cltk.morphology.latin import CollatinusConjugator
    conjugator = CollatinusConjugator()
    forms = conjugator.conjugate("amo")
    print(forms)
except ImportError:
    print("No conjugation module found in CLTK")
except Exception as e:
    print(f"ERROR: {e}")
```

**Output**:
```
[Paste actual output here]
```

### API Exploration

```python
# Check what methods are available
print("\n" + "=" * 50)
print("CLTK API Exploration")
print("=" * 50)

print("\nCollatinusDecliner methods:")
print([m for m in dir(decliner) if not m.startswith('_')])

# Check decline signature
import inspect
print("\ndecline() signature:")
print(inspect.signature(decliner.decline))
```

**Output**:
```
[Paste actual output here]
```

### First Impressions

**Pros**:
-
-
-

**Cons**:
-
-
-

**Showstoppers?**: Yes/No - Reason:

**Quick Rating**: ⭐⭐⭐⭐⭐ (1-5 stars)

---

## Library 2: pyLatinam

### Installation

```bash
# In same virtual environment or new one
pip install pyLatinam

python -c "import pyLatinam; print('pyLatinam installed successfully')"
```

**Installation time**: ___ minutes
**Issues encountered**:
-
-

### Basic Functionality Test

#### Test 1: First Declension

```python
import pyLatinam

# Test API - check documentation for correct usage
print("=" * 50)
print("pyLatinam: 1st Declension - puella")
print("=" * 50)

try:
    # Attempt to use pyLatinam API
    # NOTE: Check actual API from docs/examples
    # This is placeholder - adjust based on actual API

    # Example possibilities:
    # forms = pyLatinam.decline_noun("puella", declension=1)
    # or
    # noun = pyLatinam.Noun("puella", declension=1)
    # forms = noun.decline()

    print("TODO: Find correct API usage")

except Exception as e:
    print(f"ERROR: {e}")
    print(f"Type: {type(e)}")
```

**Output**:
```
[Paste actual output here]
```

**API Documentation**:
```bash
# Check for documentation
python -c "import pyLatinam; help(pyLatinam)"
```

### First Impressions

**Pros**:
-
-

**Cons**:
-
-

**Showstoppers?**: Yes/No - Reason:

**Quick Rating**: ⭐⭐⭐⭐⭐ (1-5 stars)

---

## Library 3: PyWORDS

### Installation

```bash
# Check if available on PyPI
pip search PyWORDS  # May not work if pip search disabled

# Try direct install
pip install PyWORDS

# If not on PyPI, try GitHub
git clone https://github.com/sjgallagher2/PyWORDS
cd PyWORDS
pip install -e .
```

**Installation time**: ___ minutes
**Issues encountered**:
-
-

### Basic Functionality Test

```python
# Test PyWORDS API
try:
    import PyWORDS

    print("=" * 50)
    print("PyWORDS: Latin Dictionary Test")
    print("=" * 50)

    # Test lookup
    # API unknown - explore
    print("TODO: Find correct API usage")

except ImportError as e:
    print(f"PyWORDS not installed: {e}")
except Exception as e:
    print(f"ERROR: {e}")
```

**Output**:
```
[Paste actual output here]
```

### First Impressions

**Pros**:
-
-

**Cons**:
-
-

**Showstoppers?**: Yes/No - Reason:

**Quick Rating**: ⭐⭐⭐⭐⭐ (1-5 stars)

---

## Quick Comparison Matrix

| Feature | CLTK | pyLatinam | PyWORDS |
|---------|------|-----------|---------|
| Installation ease | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Documentation | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| API clarity | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Noun declension | ✅/❌ | ✅/❌ | ✅/❌ |
| Verb conjugation | ✅/❌ | ✅/❌ | ✅/❌ |
| Irregular forms | ✅/❌ | ✅/❌ | ✅/❌ |
| Dictionary lookup | ✅/❌ | ✅/❌ | ✅/❌ |
| Active maintenance | ✅/❌ | ✅/❌ | ✅/❌ |

## Initial Recommendation

**Winner (if clear)**: ________________

**Rationale**:
-
-
-

**Needs more investigation**:
-
-

## Next Steps for S2 (Comprehensive Discovery)

1. Deep dive into winner from S1
2. Test edge cases and irregular forms
3. Performance benchmarking
4. Error handling assessment
5. Full API exploration

---

**S1 Status**: ⬜ Not Started | ⬜ In Progress | ⬜ Complete
**Time Spent**: ___ minutes
**Date**: 2025-11-17
**Researcher**: [Your name]

## Notes

[Any additional observations, links, resources discovered]
