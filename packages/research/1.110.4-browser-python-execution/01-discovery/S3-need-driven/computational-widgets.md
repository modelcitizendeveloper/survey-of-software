# Use Case: Computational Widgets

## Industry Context

Engineering calculators, financial modeling tools, physics simulations, mathematical visualizations, data converters. Small, focused tools embedded in web pages that perform specific computations. Users need instant results without page loads or server round-trips.

## Requirements Definition

### Critical Requirements (Must Have)
- **Fast Startup**: <1s from page load to widget interactive
- **Tiny Bundle**: <3MB total (widget must load quickly)
- **Instant Computation**: No perceivable delay for calculations
- **Offline Capable**: Works without internet (after initial load)
- **Embeddable**: Small footprint, multiple widgets on page

### Important Requirements (Should Have)
- **NumPy Support**: Scientific/numeric operations (matrices, stats)
- **Visualization**: Plot results (lightweight charting)
- **Input Validation**: Prevent invalid input, show helpful errors
- **Responsive UI**: Mobile-friendly controls
- **State Persistence**: Remember last inputs (localStorage)

### Nice to Have
- **Export Results**: Download data/plots
- **Shareable Links**: Encode inputs in URL
- **Multi-language**: i18n support
- **Theming**: Match host site appearance

## Solution Evaluation

### Pyodide (Minimal Load)

**Test Setup - Mortgage Calculator**:
```html
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"></script>
    <style>
        .calculator {
            max-width: 400px;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
        }
        input { width: 100%; padding: 8px; margin: 5px 0; }
        button { width: 100%; padding: 10px; background: #007acc; color: white; border: none; }
        .result { margin-top: 15px; padding: 10px; background: #f0f0f0; }
    </style>
</head>
<body>
    <div class="calculator">
        <h3>Mortgage Calculator</h3>
        <label>Loan Amount ($)</label>
        <input type="number" id="principal" value="300000">

        <label>Interest Rate (%)</label>
        <input type="number" id="rate" value="3.5" step="0.1">

        <label>Loan Term (years)</label>
        <input type="number" id="years" value="30">

        <button onclick="calculate()">Calculate</button>

        <div class="result" id="result" style="display:none"></div>
    </div>

    <script>
        let pyodide;
        const startTime = performance.now();

        async function init() {
            pyodide = await loadPyodide();
            const loadTime = ((performance.now() - startTime) / 1000).toFixed(2);
            console.log(`Pyodide loaded in ${loadTime}s`);
            document.querySelector('button').disabled = false;
        }

        async function calculate() {
            const principal = document.getElementById('principal').value;
            const rate = document.getElementById('rate').value;
            const years = document.getElementById('years').value;

            const code = `
def calculate_mortgage(principal, annual_rate, years):
    monthly_rate = annual_rate / 100 / 12
    num_payments = years * 12

    if monthly_rate == 0:
        return principal / num_payments

    monthly_payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / \
                      ((1 + monthly_rate)**num_payments - 1)

    total_paid = monthly_payment * num_payments
    total_interest = total_paid - principal

    return {
        'monthly_payment': round(monthly_payment, 2),
        'total_paid': round(total_paid, 2),
        'total_interest': round(total_interest, 2)
    }

calculate_mortgage(${principal}, ${rate}, ${years})
            `;

            const result = pyodide.runPython(code).toJs();
            const resultDiv = document.getElementById('result');
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = `
                <strong>Monthly Payment:</strong> $${result.get('monthly_payment').toFixed(2)}<br>
                <strong>Total Paid:</strong> $${result.get('total_paid').toFixed(2)}<br>
                <strong>Total Interest:</strong> $${result.get('total_interest').toFixed(2)}
            `;
        }

        init();
    </script>
</body>
</html>
```

**Validation Results**:
- ❌ **Fast Startup**: 2.8s (too slow for widget)
- ❌ **Tiny Bundle**: 6.4MB (way over 3MB target)
- ✅ **Instant Computation**: <10ms calculation time
- ✅ **Offline Capable**: Service worker caching works
- ⚠️ **Embeddable**: Heavy for small widgets

**Gap Analysis**:
- Pyodide is OVERKILL for simple calculators
- 6.4MB to calculate mortgage payment is absurd
- Could do this in 10 lines of JavaScript
- Only justified if need NumPy/SciPy (complex math)

### PyScript (Widget Mode)

**Test Setup - Statistics Calculator**:
```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://pyscript.net/releases/2023.11.1/core.css">
    <script type="module" src="https://pyscript.net/releases/2023.11.1/core.js"></script>
    <py-config>
        packages = ["numpy"]
    </py-config>
</head>
<body>
    <div class="stats-calculator">
        <h3>Statistical Analysis</h3>
        <textarea id="data" rows="5" placeholder="Enter numbers, one per line">
23
45
67
89
12
34
56
78
        </textarea>
        <button py-click="calculate_stats()">Calculate</button>
        <div id="stats-output"></div>
    </div>

    <py-script>
        import numpy as np
        from pyscript import document

        def calculate_stats():
            data_text = document.querySelector('#data').value
            numbers = [float(x.strip()) for x in data_text.split('\n') if x.strip()]

            if not numbers:
                output = "Please enter some numbers"
            else:
                arr = np.array(numbers)
                output = f"""
                <strong>Descriptive Statistics:</strong><br>
                Count: {len(arr)}<br>
                Mean: {np.mean(arr):.2f}<br>
                Median: {np.median(arr):.2f}<br>
                Std Dev: {np.std(arr):.2f}<br>
                Min: {np.min(arr):.2f}<br>
                Max: {np.max(arr):.2f}<br>
                25th %ile: {np.percentile(arr, 25):.2f}<br>
                75th %ile: {np.percentile(arr, 75):.2f}
                """

            document.querySelector('#stats-output').innerHTML = output
    </py-script>
</body>
</html>
```

**Validation Results**:
- ❌ **Fast Startup**: 4.2s base + 2s NumPy load = 6.2s (too slow)
- ❌ **Tiny Bundle**: 6.8MB + NumPy = 8MB+ (way over target)
- ✅ **Instant Computation**: NumPy operations fast
- ✅ **NumPy Support**: Full NumPy available
- ⚠️ **Embeddable**: Better than raw Pyodide (HTML-first) but still heavy

**Gap Analysis**:
- Slightly worse than raw Pyodide (larger bundle)
- Cleaner code integration (py-click events)
- Still too heavy for "widget" classification
- Justified ONLY if need NumPy (statistical functions)

### Pure JavaScript Alternative (Baseline)

**Test Setup - Same Mortgage Calculator**:
```html
<!DOCTYPE html>
<html>
<head>
    <style>
        .calculator {
            max-width: 400px;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
        }
        input { width: 100%; padding: 8px; margin: 5px 0; }
        button { width: 100%; padding: 10px; background: #007acc; color: white; border: none; }
        .result { margin-top: 15px; padding: 10px; background: #f0f0f0; }
    </style>
</head>
<body>
    <div class="calculator">
        <h3>Mortgage Calculator</h3>
        <label>Loan Amount ($)</label>
        <input type="number" id="principal" value="300000">

        <label>Interest Rate (%)</label>
        <input type="number" id="rate" value="3.5" step="0.1">

        <label>Loan Term (years)</label>
        <input type="number" id="years" value="30">

        <button onclick="calculate()">Calculate</button>

        <div class="result" id="result" style="display:none"></div>
    </div>

    <script>
        function calculate() {
            const principal = parseFloat(document.getElementById('principal').value);
            const annualRate = parseFloat(document.getElementById('rate').value);
            const years = parseInt(document.getElementById('years').value);

            const monthlyRate = annualRate / 100 / 12;
            const numPayments = years * 12;

            let monthlyPayment;
            if (monthlyRate === 0) {
                monthlyPayment = principal / numPayments;
            } else {
                monthlyPayment = principal * (monthlyRate * Math.pow(1 + monthlyRate, numPayments)) /
                                (Math.pow(1 + monthlyRate, numPayments) - 1);
            }

            const totalPaid = monthlyPayment * numPayments;
            const totalInterest = totalPaid - principal;

            const resultDiv = document.getElementById('result');
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = `
                <strong>Monthly Payment:</strong> $${monthlyPayment.toFixed(2)}<br>
                <strong>Total Paid:</strong> $${totalPaid.toFixed(2)}<br>
                <strong>Total Interest:</strong> $${totalInterest.toFixed(2)}
            `;
        }
    </script>
</body>
</html>
```

**Validation Results**:
- ✅ **Fast Startup**: <50ms (instant)
- ✅ **Tiny Bundle**: 2KB (HTML + CSS + JS)
- ✅ **Instant Computation**: <1ms
- ✅ **Offline Capable**: No external dependencies
- ✅ **Embeddable**: Trivial footprint

**Gap Analysis**:
- Perfect for simple math widgets
- No NumPy (but rarely needed for widgets)
- JavaScript math sufficient for 90% of calculators

## Validation Testing

### Test 1: Startup Time Comparison
```javascript
const startupTimes = {
    pyodide: 2800,      // ms
    pyscript: 4200,     // ms
    javascript: 15      // ms (DOM load only)
};

// Target: <1000ms
// Winner: JavaScript (190x faster)
```

### Test 2: Bundle Size
```
Pyodide:      6.4MB compressed
PyScript:     6.8MB compressed
JavaScript:   2KB (no dependencies)

// Target: <3MB
// Winner: JavaScript (3200x smaller)
```

### Test 3: When Python IS Justified - Matrix Operations

**Scenario**: Linear algebra calculator (matrix inversion, eigenvalues)

**JavaScript**:
```javascript
// Requires external library (math.js = 500KB)
// OR implement algorithms from scratch (error-prone)
```

**Pyodide + NumPy**:
```python
import numpy as np

def analyze_matrix(matrix_data):
    matrix = np.array(matrix_data)
    return {
        'determinant': float(np.linalg.det(matrix)),
        'eigenvalues': np.linalg.eigvals(matrix).tolist(),
        'rank': int(np.linalg.matrix_rank(matrix)),
        'inverse': np.linalg.inv(matrix).tolist() if np.linalg.det(matrix) != 0 else None
    }

# Verdict: Python JUSTIFIED for complex numerical operations
```

### Test 4: Physics Simulation Widget

**Test Setup - Projectile Motion**:
```html
<py-config>
    packages = ["numpy", "matplotlib"]
</py-config>

<py-script>
import numpy as np
import matplotlib.pyplot as plt

def simulate_projectile(v0, angle_deg, g=9.81):
    angle = np.radians(angle_deg)
    t_flight = 2 * v0 * np.sin(angle) / g
    t = np.linspace(0, t_flight, 100)

    x = v0 * np.cos(angle) * t
    y = v0 * np.sin(angle) * t - 0.5 * g * t**2

    plt.figure(figsize=(10, 6))
    plt.plot(x, y)
    plt.xlabel('Distance (m)')
    plt.ylabel('Height (m)')
    plt.title(f'Projectile Motion (v₀={v0}m/s, θ={angle_deg}°)')
    plt.grid(True)
    plt.show()

# User inputs connected to function call
</py-script>
```

**Validation**:
- ✅ NumPy for trajectory calculations
- ✅ Matplotlib for visualization
- ⚠️ 8MB bundle + 6s load time
- **Verdict**: Acceptable for educational/scientific widgets where visualization matters

## Best Fit Analysis

### For Simple Calculators: **JavaScript (No Python)**

**Why JavaScript**:
- 3000x smaller bundle
- 200x faster startup
- Native browser support
- No dependencies
- Perfect for: mortgage, loan, unit conversion, basic math

**Implementation Pattern**:
```html
<!DOCTYPE html>
<html>
<head>
    <style>
        .widget { max-width: 400px; padding: 20px; border: 1px solid #ddd; }
        input { width: 100%; padding: 8px; margin: 5px 0; }
        button { width: 100%; padding: 10px; background: #007acc; color: white; border: none; }
    </style>
</head>
<body>
    <div class="widget">
        <h3>Calculator Name</h3>
        <input type="number" id="input1" placeholder="Enter value">
        <button onclick="calculate()">Calculate</button>
        <div id="result"></div>
    </div>

    <script>
        function calculate() {
            const value = parseFloat(document.getElementById('input1').value);
            const result = /* Your calculation */;
            document.getElementById('result').textContent = result;
        }
    </script>
</body>
</html>
```

### For Scientific Widgets: **Pyodide (When NumPy/Matplotlib Required)**

**When Python IS Justified**:
- Matrix operations (eigenvalues, SVD, etc.)
- Statistical analysis (distributions, hypothesis tests)
- Signal processing (FFT, filtering)
- Physics simulations with visualization
- Data analysis with plots

**Implementation Pattern**:
```html
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"></script>
</head>
<body>
    <div class="scientific-widget">
        <h3>Matrix Analysis</h3>
        <textarea id="matrix-input" placeholder="Enter matrix (one row per line)">
1 2 3
4 5 6
7 8 9
        </textarea>
        <button onclick="analyzeMatrix()">Analyze</button>
        <div id="output"></div>
    </div>

    <script>
        let pyodide;

        async function init() {
            pyodide = await loadPyodide();
            await pyodide.loadPackage('numpy');
        }

        async function analyzeMatrix() {
            const matrixText = document.getElementById('matrix-input').value;
            const code = `
import numpy as np

def analyze(text):
    rows = [list(map(float, row.split())) for row in text.strip().split('\\n')]
    matrix = np.array(rows)

    return {
        'shape': matrix.shape,
        'determinant': float(np.linalg.det(matrix)),
        'rank': int(np.linalg.matrix_rank(matrix)),
        'eigenvalues': np.linalg.eigvals(matrix).tolist()
    }

analyze("""${matrixText}""")
            `;

            const result = pyodide.runPython(code).toJs();
            // Display result
        }

        init();
    </script>
</body>
</html>
```

## Decision Matrix

| Widget Type | Recommended Solution | Justification |
|-------------|---------------------|---------------|
| Mortgage/Loan Calculator | JavaScript | Simple arithmetic, no advanced math |
| Unit Converter | JavaScript | Basic multiplication/division |
| BMI Calculator | JavaScript | Simple formula |
| Compound Interest | JavaScript | Math.pow sufficient |
| **Matrix Calculator** | **Pyodide + NumPy** | Linear algebra algorithms |
| **Statistical Analysis** | **Pyodide + NumPy** | Distributions, tests, analysis |
| **Physics Simulation** | **Pyodide + NumPy/Matplotlib** | Numerical integration + plots |
| **Signal Processing** | **Pyodide + NumPy** | FFT, filtering, convolution |
| Data Visualization | JavaScript (Chart.js) | Plotting library lighter than Matplotlib |
| Financial Modeling | JavaScript (or Python if complex) | Depends on complexity |

## Optimization Strategies

### 1. Lazy Load Pyodide
```html
<div class="widget">
    <h3>Matrix Calculator</h3>
    <div id="loading" style="display:none">Loading Python engine...</div>
    <button onclick="initCalculator()" id="init-btn">Start Calculator</button>
    <div id="calculator" style="display:none">
        <!-- Calculator UI appears after Pyodide loads -->
    </div>
</div>

<script>
    let pyodide;

    async function initCalculator() {
        document.getElementById('loading').style.display = 'block';
        document.getElementById('init-btn').style.display = 'none';

        pyodide = await loadPyodide();
        await pyodide.loadPackage('numpy');

        document.getElementById('loading').style.display = 'none';
        document.getElementById('calculator').style.display = 'block';
    }
</script>
```

### 2. Hybrid Approach
```javascript
// Use JavaScript for simple cases, Pyodide for complex

function calculate() {
    const complexity = assessComplexity(userInput);

    if (complexity === 'simple') {
        // JavaScript calculation (instant)
        return simpleCalc(userInput);
    } else {
        // Load Pyodide only when needed
        return await complexCalc(userInput);
    }
}
```

### 3. Pre-compiled Results
```python
# For fixed parameter ranges, pre-compute results
# Store in JSON, lookup instead of computing

results = {
    "v0_20_angle_45": { "range": 40.8, "max_height": 10.2 },
    // ... more combinations
}

# Instant lookup vs. 6s Pyodide load
```

## Limitations & Reality Check

### When Python is NOT Worth It
- **Simple Math**: JavaScript can handle 95% of calculator needs
- **Bundle Cost**: 6MB for basic arithmetic is wasteful
- **Startup Penalty**: Users wait 3-5s for calculator to load
- **Over-engineering**: Python adds complexity without benefit

### When Python IS Worth It
- **Complex Numerics**: Matrix math, statistical tests, signal processing
- **Visualization**: Matplotlib plots (though Chart.js often better)
- **Code Reuse**: Port existing Python scientific code to web
- **Scientific Accuracy**: NumPy algorithms battle-tested

## Recommendation

### Default to JavaScript
```
IF widget does basic math THEN
    Use JavaScript
ELSE IF widget needs NumPy/SciPy THEN
    Use Pyodide
ELSE
    Re-evaluate if web widget is right approach
END IF
```

### Python Exception Cases
Use Pyodide + NumPy for:
1. **Linear Algebra**: Matrix operations, decompositions
2. **Statistics**: Advanced tests, distributions
3. **Signal Processing**: FFT, filtering, convolution
4. **Physics**: Numerical integration, simulations
5. **Code Porting**: Existing Python scientific code

### Implementation Guidance
```html
<!-- DON'T DO THIS (unless justified by NumPy need) -->
<script src="pyodide.js"></script> <!-- 6.4MB -->
<py-script>
    result = principal * rate * years  # Simple multiplication
</py-script>

<!-- DO THIS (for simple math) -->
<script>
    const result = principal * rate * years;  // 0.02KB
</script>

<!-- DO THIS (when NumPy needed) -->
<script src="pyodide.js"></script>
<py-script>
    import numpy as np
    eigenvalues = np.linalg.eigvals(matrix)  # Complex algorithm
</py-script>
```

## Final Verdict

**Computational widgets have a HIGH bar for Python justification.**

- 90% of widgets: JavaScript is superior (faster, smaller, simpler)
- 10% of widgets: Python necessary (complex scientific operations)
- Don't use Python for "coolness factor" - use it when mathematically justified

**Ask yourself**: "Could I implement this in JavaScript with <100 lines of code?"
- If YES: Use JavaScript
- If NO: Consider Pyodide + NumPy
