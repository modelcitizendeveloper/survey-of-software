/* Which five? — a chooser, not a measurer.
 *
 * Every number quoted below was measured by the harness at
 * /workshop/formatters/ and is recorded in the surveys it cites. Where a
 * recommendation has no number behind it, it is tagged `reasoned` rather than
 * dressed up as measurement. That distinction is the point of the page.
 */
(function () {
  "use strict";

  var ASKS = [
    { id: "lang", q: "What are you writing?",
      opts: [["py", "Python"], ["js", "TypeScript / JavaScript"], ["both", "Both"]] },
    { id: "size", q: "How much code is there now?",
      opts: [["s", "Under ~1 MB"], ["m", "A few MB"], ["l", "10 MB or more"]] },
    { id: "grow", q: "Where is it going?",
      opts: [["flat", "About the same"], ["grow", "Steadily bigger"], ["mono", "Toward a monolith"]] },
    { id: "arch", q: "Dev machine and CI — same architecture?",
      opts: [["same", "Both x86, or both ARM"], ["split", "ARM laptop, x86 CI"], ["dunno", "Not sure"]] },
    { id: "rules", q: "Do you need rules nobody else would ship?",
      opts: [["no", "No — standard rules are fine"], ["yes", "Yes — we have house rules"]] },
    { id: "hist", q: "Anything that constrains the type checker?",
      opts: [["fresh", "Typed from the start"], ["grad", "Adding types to old code"],
             ["fw", "Django / SQLAlchemy / Pydantic"], ["none", "Not typing it"]] }
  ];

  var state = { lang: "py", size: "m", grow: "grow", arch: "same", rules: "no", hist: "grad" };

  function slot(code, name, pick, runner, why, tag) {
    return '<div class="slot"><header><h3>' + name + '</h3>' +
      '<span class="code">' + code + '</span>' +
      '<span class="tag ' + tag[0] + '">' + tag[1] + '</span></header>' +
      '<div class="body"><div class="pick">' + pick + '</div>' +
      '<div class="runner">runner-up: ' + runner + '</div>' +
      '<p class="why">' + why + '</p></div></div>';
  }

  // ---- the five slots -------------------------------------------------

  function formatter(s) {
    if (s.lang === "js") {
      return slot("1.253", "Formatter", "Prettier", "Biome",
        "Biome is the faster binary and folds the linter in, but Prettier formats " +
        "<strong>Markdown and YAML and Biome does not</strong>. A repo containing either keeps " +
        "Prettier whatever the speed argument says. That is a capability difference, not a " +
        "preference — which is why speed does not decide this slot.",
        ["m", "measured"]);
    }
    var why = "Ruff emits Black-compatible output and also sorts imports, so it replaces two " +
      "tools with one. Measured at <strong>16&ndash;32&times; Black</strong> depending on " +
      "architecture and corpus size.";
    if (s.size === "s") {
      why += " On a codebase your size that ratio is <strong>real and unfeelable</strong> — both " +
        "finish faster than you can notice. Pick Ruff for the consolidation, not the speed.";
    }
    why += " Black remains the reference implementation; choose it if you want that specifically.";
    return slot("1.253", "Formatter", s.lang === "both" ? "Ruff format + Prettier" : "Ruff format",
      s.lang === "both" ? "Black + Biome" : "Black", why, ["m", "measured"]);
  }

  function linter(s) {
    if (s.lang === "js") {
      return slot("1.250", "Linter", "ESLint", s.rules === "yes" ? "(nothing — see why)" : "oxlint in front of it",
        s.rules === "yes"
          ? "There is no runner-up. oxlint and Biome compile their rules into a Rust binary and " +
            "<strong>cannot run a rule you wrote</strong>. With house rules, ESLint is not the " +
            "faster choice or the safer one — it is the only one."
          : "ESLint at 160.1M weekly downloads is roughly five times oxlint and Biome combined. " +
            "Add oxlint as a fast first pass if lint time actually hurts, and keep ESLint for the " +
            "type-aware and framework rules the Rust tools do not have. The cost that speed number " +
            "hides: two tools means two rule configs that must agree.",
        ["r", "reasoned"]);
    }
    var pick = "Ruff check", runner = "Flake8", why;
    if (s.rules === "yes") {
      pick = "Flake8"; runner = "Ruff check";
      why = "<strong>This is the input that changed the answer.</strong> Ruff's rules are compiled " +
        "into a Rust binary and there is no plugin interface — a house rule written as a Flake8 " +
        "plugin has nowhere to go. Ruff is 28&ndash;38&times; faster and it cannot run your rule, " +
        "so it is not the choice. Consider Semgrep alongside: its rules are patterns that look " +
        "like the code, so anyone on the team can write one.";
    } else {
      why = "One binary covering Flake8's rules, its popular plugins, isort and a port of Bandit. " +
        "Measured on an idle machine at <strong>28&times; Flake8 at 1&nbsp;MB and 37.9&times; at 12&nbsp;MB</strong> " +
        "on matched rule sets. Enable the <code>S</code> prefix on day one — it is Bandit's rules " +
        "and it is free if Ruff is installed.";
      if (s.size === "s") {
        why += " At your size both are instant; take Ruff for the consolidation.";
      }
    }
    return slot("1.250", "Linter", s.lang === "both" ? pick + " + ESLint" : pick,
      s.lang === "both" ? runner + " + oxlint" : runner, why, ["m", "measured"]);
  }

  function checker(s) {
    if (s.hist === "none") {
      return slot("1.251", "Type checker", "None, deliberately", "mypy, loosely, later",
        "You said you are not typing it, so this slot is empty and that is a legitimate answer. " +
        "If that changes, start with mypy at its loosest and ratchet — it is the only checker " +
        "with a per-module strictness gradient, which is what makes adoption survivable.",
        ["n", "not applicable"]);
    }
    if (s.lang === "js") {
      return slot("1.251", "Type checker", "TypeScript", "(there is no runner-up)",
        "<strong>This slot is not a choice.</strong> TypeScript has 274.2M weekly downloads " +
        "against Flow's 450K — six hundred to one. Flow is maintained and works; nobody will be " +
        "able to help you with it. The live question is not which tool but which version: " +
        "TypeScript 7 is a rewrite in Go, and the type system did not change but the " +
        "implementation did.", ["r", "reasoned"]);
    }
    var pick, runner, why;
    if (s.hist === "fw") {
      pick = "mypy"; runner = "(nothing — see why)";
      why = "<strong>This input overrides everything else in this slot.</strong> Django, " +
        "SQLAlchemy and Pydantic build types through metaclasses and decorators, so the types " +
        "you need are real at runtime and absent from the source. mypy has plugins for them; " +
        "pyright and ty have no plugin interface at all. A faster checker that cannot see your " +
        "ORM is not an improvement.";
    } else if (s.hist === "fresh") {
      pick = "pyright"; runner = "mypy";
      why = "On code typed from the start, pyright infers into unannotated bodies where mypy " +
        "leaves them alone, so it finds more. It is also what VS Code runs, so editor and CI " +
        "agree by construction. Outside official VS Code, use basedpyright — Pylance is licensed " +
        "to Microsoft's builds and the fork exists to close that gap.";
    } else {
      pick = "mypy"; runner = "pyright";
      why = "Adding types to existing code is what mypy was designed for: it leaves unannotated " +
        "bodies alone and lets individual packages opt into strictness. pyright infers into them " +
        "and will report a great deal of work you have not done yet — correct behaviour, wrong " +
        "moment.";
    }
    why += " <strong>Not ty, yet</strong> — 8.6M weekly downloads at version 0.0.75. A linter's " +
      "new rule is a warning; a checker's changed inference is a failed build.";
    return slot("1.251", "Type checker", s.lang === "both" ? pick + " + TypeScript" : pick,
      s.lang === "both" ? runner + " + (none)" : runner, why, ["r", "reasoned"]);
  }

  function parser(s) {
    return slot("1.252", "Parser / AST", "You are not choosing this", "libcst, if you are writing a tool",
      "<strong>Included to say it is not a decision.</strong> Every tool above parses your code, " +
      "and each brought its own parser — you do not pick one. This slot only becomes a choice if " +
      "you are <em>writing</em> a tool that rewrites code, and then it is a real one: " +
      "<code>ast</code> discards formatting and comments, so a transform round-trips into a diff " +
      "nobody wants. libcst preserves them. That is the whole survey in one sentence.",
      ["n", "not a choice"]);
  }

  function tests(s) {
    if (s.lang === "js") {
      return slot("1.254", "Test runner", "Vitest", "Jest",
        "Vitest if the project already builds with Vite — it shares the config and the transform " +
        "pipeline, which is most of the setup cost. Jest otherwise; it is the older default and " +
        "the larger ecosystem.", ["r", "reasoned"]);
    }
    return slot("1.254", "Test runner", s.lang === "both" ? "pytest + Vitest" : "pytest",
      s.lang === "both" ? "unittest + Jest" : "unittest",
      "pytest for the fixture model and the plugin ecosystem. unittest is the runner-up on one " +
      "axis only: it is in the standard library, so it adds no dependency — which matters for a " +
      "library other people install and almost nowhere else.", ["r", "reasoned"]);
  }

  // ---- cross-cutting notes: the part that teaches ---------------------

  function notes(s) {
    var out = [];
    if (s.size === "s") {
      out.push('<div class="flag good"><strong>At your size, speed is not a differentiator.</strong> ' +
        'On a 1&nbsp;MB codebase the measured gap between the fastest and slowest linter here is ' +
        '<code>0.014s</code> against <code>0.40s</code>. That is a real 28&times; and it is under ' +
        'four tenths of a second — you cannot feel it. Every speed answer above is honest and none of it ' +
        'should decide anything. Choose on the extension question instead.</div>');
    }
    if (s.arch === "split") {
      out.push('<div class="flag"><strong>Your laptop and your CI may not agree about which tool is fast.</strong> ' +
        'The formatter harness measured Ruff\'s lead over Black at 32.3&times; on an ARM laptop and ' +
        '16.1&times; on an x86 droplet — but the ARM machine was doing other work, and the harness ' +
        'timed the tools in separate windows, so that gap is <strong>not yet a finding about ' +
        'architecture</strong>. A clean ARM run is outstanding. What is safe to say: benchmark on ' +
        'the architecture your CI uses, not the one in front of you, because you cannot assume ' +
        'they agree.</div>');
    }
    if ((s.grow === "mono" || s.size === "l") && s.lang !== "js") {
      out.push('<div class="flag"><strong>You are buying a curve, not a ratio.</strong> Twelve times ' +
        'more code did not cost these tools twelve times more time — it cost Biome 3.8&times;, ' +
        'Ruff 4.7&times;, Flake8 6.4&times; and <strong>Pylint 23.5&times;</strong> — a shape that reproduced on two architectures. Pylint is the ' +
        'only one here whose cost grows <em>faster</em> than your codebase does. Run it on a ' +
        'narrowed path or a slower job; do not put it in the inner loop of a codebase headed ' +
        'toward a monolith.</div>');
    }
    if (s.rules === "yes") {
      out.push('<div class="flag"><strong>That one answer changed more than the speed answers did.</strong> ' +
        'Try switching the size and architecture questions and watch the recommendations barely ' +
        'move. Then switch this one back. The extension point — whether your rules can be somebody ' +
        'else\'s rules — decides more of this than any benchmark, and it is the finding all three ' +
        'surveys arrived at independently.</div>');
    }
    return out.join("");
  }

  // ---- wiring ---------------------------------------------------------

  function render() {
    var o = document.getElementById("out");
    o.innerHTML = notes(state) + formatter(state) + linter(state) +
                  checker(state) + parser(state) + tests(state);
  }

  function build() {
    var a = document.getElementById("asks");
    a.innerHTML = ASKS.map(function (k) {
      return '<div class="ask"><h3>' + k.q + '</h3><div class="opts">' +
        k.opts.map(function (p) {
          return '<button class="opt" data-k="' + k.id + '" data-v="' + p[0] + '" ' +
                 'aria-pressed="' + (state[k.id] === p[0]) + '">' + p[1] + '</button>';
        }).join("") + "</div></div>";
    }).join("");
    a.addEventListener("click", function (e) {
      var b = e.target.closest(".opt");
      if (!b) return;
      state[b.dataset.k] = b.dataset.v;
      Array.prototype.forEach.call(a.querySelectorAll('.opt[data-k="' + b.dataset.k + '"]'),
        function (x) { x.setAttribute("aria-pressed", String(x === b)); });
      render();
    });
  }

  build();
  render();
})();
