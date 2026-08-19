/* workshop.js — shared runtime for Survey of Software floor models.
   Extracted 2026-08-19 from compresso (which copied it from qrkadelic, which
   copied it from sortie). What every page needs and none should rewrite:
     - the Plain/Engineering register toggle (persisted per page)
     - the Pyodide loader, pinned, with a status line
     - JSON-returning calls into Python, and a yield so the UI can paint
     - clamp-safe timing (the Python snippet pages embed in their own code)
     - bars, number formatting, copy-to-clipboard, copy-image buttons
   A page is still a page: it owns its panels, its Python, its argument.
   Usage:  <script src="/workshop/_lib/workshop.js"></script>
           const W = Workshop;  W.mode("pagekey");  const py = await W.boot({...}); */
(function(){
  const $ = id => document.getElementById(id);

  /* ── register toggle ──────────────────────────────────────────────────
     Expects #m-plain, #m-eng, #mode-hint. Same in both registers; Engineering
     ADDS instrumentation — the surprising result must land in both. */
  function mode(key, hints){
    const bPlain = $("m-plain"), bEng = $("m-eng"), hint = $("mode-hint");
    hints = hints || {
      plain: "Plain language. Switch to Engineering for versions, byte counts and the measurements behind each claim.",
      eng:   "Engineering. Versions, byte counts and the measurement behind each claim. Switch to Plain for the same demos in ordinary words."
    };
    function setMode(eng){
      document.body.classList.toggle("engineering", eng);
      bPlain.setAttribute("aria-pressed", String(!eng));
      bEng.setAttribute("aria-pressed", String(eng));
      hint.textContent = eng ? hints.eng : hints.plain;
      try { localStorage.setItem(key + "-mode", eng ? "eng" : "plain"); } catch(e){}
    }
    bPlain.onclick = () => setMode(false);
    bEng.onclick   = () => setMode(true);
    try { setMode(localStorage.getItem(key + "-mode") === "eng"); } catch(e){ setMode(false); }
    return setMode;
  }

  /* ── Pyodide ──────────────────────────────────────────────────────────
     Pin the version per page; check the CURRENT pyodide-lock.json when building
     a new one — 314.x is Python 3.14 and ships far more compiled packages than
     the 0.27 line the first models were checked against. */
  async function boot({ version, packages = [], status, statusText = {} }){
    const say = t => { if (status) status.textContent = t; };
    say(statusText.download || "Downloading CPython (WebAssembly)… first time only, then cached.");
    const base = `https://cdn.jsdelivr.net/pyodide/v${version}/full/`;
    if (!window.loadPyodide) {
      await new Promise((res, rej) => {
        const s = document.createElement("script");
        s.src = base + "pyodide.js"; s.onload = res;
        s.onerror = () => rej(new Error("could not load Pyodide")); document.head.appendChild(s);
      });
    }
    const py = await loadPyodide({ indexURL: base });
    if (packages.length) { say(statusText.packages || ("Loading " + packages.join(", ") + "…")); await py.loadPackage(packages); }
    return py;
  }
  const call = (py, fn, ...args) => JSON.parse(py.globals.get(fn)(...args));
  const yieldUI = () => new Promise(r => setTimeout(r, 0));

  /* Serialise re-entrant async panel updates: a slider firing mid-measurement
     queues exactly one re-run with the latest value, never a pile-up. */
  const busy = {};
  async function guarded(key, fn){
    if (busy[key]) { busy[key] = "again"; return; }
    busy[key] = true;
    do { if (busy[key] === "again") busy[key] = true; await yieldUI(); await fn(); } while (busy[key] === "again");
    busy[key] = false;
  }

  /* ── timing, the Python half ──────────────────────────────────────────
     Browsers clamp the clock (100 µs in Chromium without cross-origin isolation).
     A call that finishes in microseconds reads as zero; best-of in batches large
     enough to register. Pages paste this into their own Python source. */
  const PY_TIMING = String.raw`
import time as _time
def _best(fn, arg, budget_s, min_reps=3):
    """Best-of timing under a wall-clock budget. Browser clocks clamp (100 us in Chromium
    without cross-origin isolation), so calls are timed in batches calibrated to take at
    least 5 ms - fifty clamp ticks - before a reading is trusted. Slow calls get one rep."""
    t0 = _time.perf_counter(); fn(arg); first = _time.perf_counter() - t0
    if first > budget_s: return first, 1
    k = 1
    while True:
        t0 = _time.perf_counter()
        for _ in range(k): fn(arg)
        dt = _time.perf_counter() - t0
        if dt >= 0.005 or k >= 200_000: break
        k *= 4
    b = dt / k; reps = 1; total = dt
    while reps < min_reps or total < budget_s:
        t0 = _time.perf_counter()
        for _ in range(k): fn(arg)
        dt = _time.perf_counter() - t0
        if dt > 0: b = min(b, dt / k)
        reps += 1; total += dt
        if reps >= 40: break
    return max(b, 1e-9), reps
`;

  /* ── formatting and bars ──────────────────────────────────────────── */
  const fmtRate = (n, unit = "B/s") => n >= 1e3 ? (n/1e3).toFixed(1).replace(/\.0$/,"") + " G" + unit : n.toFixed(n < 10 ? 1 : 0) + " M" + unit;
  const fmtMs   = ms => ms >= 1000 ? (ms/1000).toFixed(2) + " s" : ms >= 10 ? ms.toFixed(0) + " ms" : ms >= 1 ? ms.toFixed(1) + " ms" : (ms*1000).toFixed(0) + " µs";
  const kb      = n => n >= 1048576 ? (n/1048576).toFixed(2) + " MB" : n >= 1024 ? (n/1024).toFixed(0) + " KB" : n + " B";
  /* rows: [{label, value, max, display, color, log}] → bars with values outside the fill */
  function bars(el, rows){
    el.innerHTML = rows.map(r => {
      const frac = r.log ? Math.log10(1 + r.value) / Math.log10(1 + r.max) : r.value / r.max;
      const w = Math.max(1, Math.min(70, frac * 70)).toFixed(1);
      return `<div class="bar"><span class="lbl">${r.label}</span><span class="fill" style="width:${w}%${r.color ? ";background:" + r.color : ""}"></span><span class="val">${r.display}</span></div>`;
    }).join("");
  }

  /* ── clipboard ────────────────────────────────────────────────────── */
  function copyText(button, statusEl, getText, okMsg = "Copied — paste it into any AI."){
    button.onclick = async () => {
      try { await navigator.clipboard.writeText(getText()); statusEl.textContent = okMsg; }
      catch(e){ statusEl.textContent = "Select the text below and copy it."; }
    };
  }
  /* <button class="copyimg" data-src="canvasOrImgId"> + <span id="{id}msg"> */
  function copyImages(filename = "workshop.png"){
    document.addEventListener("click", async (e) => {
      const b = e.target.closest("button.copyimg"); if (!b) return;
      const el = $(b.dataset.src), msg = $(b.dataset.src + "msg");
      try {
        const blob = el.tagName === "CANVAS" ? await new Promise(r => el.toBlob(r, "image/png")) : await (await fetch(el.src)).blob();
        await navigator.clipboard.write([new ClipboardItem({ "image/png": blob })]);
        if (msg) msg.textContent = "Copied — paste it anywhere.";
      } catch (err) {
        const a = document.createElement("a");
        a.href = el.tagName === "CANVAS" ? el.toDataURL("image/png") : el.src; a.download = filename; a.click();
        if (msg) msg.textContent = "Downloaded instead — this browser blocks image copy.";
      }
      if (msg) setTimeout(() => { msg.textContent = ""; }, 4000);
    });
  }

  window.Workshop = { $, mode, boot, call, yieldUI, guarded, PY_TIMING, fmtRate, fmtMs, kb, bars, copyText, copyImages };
})();
