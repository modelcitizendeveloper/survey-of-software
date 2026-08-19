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
  /* call(pyodideOrModule, fn, ...args): fn may be a global (legacy) or a module attribute */
  const call = (py, fn, ...args) => {
    const f = (py && py.globals) ? py.globals.get(fn) : py[fn];
    return JSON.parse(f(...args));
  };
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

  /* ── the Python half ──────────────────────────────────────────────────
     Pages do not embed Python. They fetch /workshop/_lib/workshop.py (timing, shared
     samples) and their own core.py, write both into Pyodide's filesystem and import
     them — the same files the marimo notebook and the native bench import. One copy.
       const core = await W.loadModules(py, { workshop: "/workshop/_lib/workshop.py", core: "core.py" });
       W.call(core, "measure", ...)  // calls a function on the module, parses its JSON */
  async function loadModules(py, mods){
    let last = null;
    for (const [name, url] of Object.entries(mods)) {
      const src = await (await fetch(url, { cache: "no-cache" })).text();
      py.FS.writeFile(`/home/pyodide/${name}.py`, src);
      last = py.pyimport(name);
    }
    return last;
  }

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

  /* ── newsletter capture ───────────────────────────────────────────────
     The same Field Notes form as the survey pages (native POST to Buttondown,
     tags method / research-site / placement-workshop, metadata__source = the
     page path), injected automatically above .foot. One copy for the whole
     workshop. Opt out per page with <body data-no-newsletter>; or place a
     <div id="newsletter"></div> to choose the spot. */
  function newsletter(){
    if (document.body.dataset.noNewsletter !== undefined) return;
    if (document.querySelector('.newsletter-cta, form[action*="embed-subscribe"]')) return;
    // styles ride with the injector (not workshop.css) so pages that predate the
    // lib (sortie, qrkadelic) need only this script; the tokens are the shared palette
    if (!document.getElementById("newsletter-cta-css")) {
      const st = document.createElement("style"); st.id = "newsletter-cta-css";
      st.textContent = `
.newsletter-cta{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:18px 20px;margin:44px 0 0}
.newsletter-cta__pitch{margin:0 0 12px;color:var(--text)}
.newsletter-cta__pitch strong{color:var(--bright)}
.newsletter-cta__form{display:flex;gap:8px;flex-wrap:wrap}
.newsletter-cta__input{font:inherit;flex:1 1 220px;padding:9px 12px;border-radius:6px;background:var(--field);color:var(--bright);border:1px solid var(--line)}
.newsletter-cta__form button{font:inherit;cursor:pointer;background:var(--accent);color:var(--on-accent);border:1px solid var(--accent);border-radius:6px;padding:8px 16px;font-weight:700}
.newsletter-cta__fineprint{font-size:.82rem;color:var(--faint);margin:10px 0 0}`;
      document.head.appendChild(st);
    }
    const user = "model-citizen-developer";
    const el = document.createElement("aside");
    el.className = "newsletter-cta";
    el.innerHTML =
      `<p class="newsletter-cta__pitch"><strong>Field Notes — what happens after the measurement.</strong> ` +
      `The surveys behind these pages stay neutral by design. The Reports built from them argue a case, ` +
      `and a new one is at the center of each edition.</p>` +
      `<form class="newsletter-cta__form" action="https://buttondown.com/api/emails/embed-subscribe/${user}" method="post" ` +
      `target="popupwindow" onsubmit="window.open('https://buttondown.com/${user}','popupwindow')">` +
      `<input class="newsletter-cta__input" type="email" name="email" placeholder="you@example.com" aria-label="Email address" autocomplete="email" required>` +
      `<input type="hidden" name="tag" value="method">` +
      `<input type="hidden" name="tag" value="research-site">` +
      `<input type="hidden" name="tag" value="placement-workshop">` +
      `<input type="hidden" name="metadata__source" value="${location.pathname}">` +
      `<input type="hidden" name="embed" value="1">` +
      `<button type="submit">Subscribe</button></form>` +
      `<p class="newsletter-cta__fineprint">No tracking pixels. Unsubscribe in one click.</p>`;
    const slot = document.getElementById("newsletter"), foot = document.querySelector(".foot");
    if (slot) slot.appendChild(el);
    else if (foot) foot.parentNode.insertBefore(el, foot);
    else document.body.appendChild(el);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", newsletter);
  else newsletter();

  window.Workshop = { $, mode, boot, loadModules, call, yieldUI, guarded, fmtRate, fmtMs, kb, bars, copyText, copyImages, newsletter };
})();
