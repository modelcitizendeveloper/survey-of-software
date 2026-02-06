# Quick Start: Testing CLTK for Latin

## Step 1: Set Up Test Environment

```bash
cd ~/spawn-solutions/research/1.140-classical-language-libraries/02-implementations

# Create virtual environment with uv
uv venv

# Activate it
source .venv/bin/activate

# Install CLTK
uv pip install cltk
```

## Step 2: Run Quick Test

```bash
# Run the test script
python test_cltk.py
```

Expected output: Declensions for all 5 declension types (puella, dominus, templum, rex, manus, res)

## Step 3: Manual Interactive Test

```bash
python
```

```python
from cltk.morphology.latin import CollatinusDecliner

decliner = CollatinusDecliner()

# Test 1st declension
print("Testing: puella (girl)")
forms = decliner.decline("puella", declension=1)
for case, form in forms.items():
    print(f"{case:30s} {form}")
```

## Step 4: Document Results

Edit `01-discovery/S1_RAPID_DISCOVERY.md` and fill in:
- Installation time
- Output from tests
- Observations (forms correct? API intuitive?)
- Star rating

## Step 5: Test Other Libraries

### pyLatinam
```bash
uv pip install pyLatinam

python -c "import pyLatinam; help(pyLatinam)"
# Document API and test
```

### PyWORDS
```bash
# Check if on PyPI
uv pip install PyWORDS

# If not, clone from GitHub
cd /tmp
git clone https://github.com/sjgallagher2/PyWORDS
cd PyWORDS
uv pip install -e .
```

## Step 6: Compare and Choose

Update `01-discovery/S1_RAPID_DISCOVERY.md` with comparison matrix and initial recommendation.

---

**Estimated time**: 1-2 hours
**Next**: S2 Comprehensive Discovery (deep dive into winner)
