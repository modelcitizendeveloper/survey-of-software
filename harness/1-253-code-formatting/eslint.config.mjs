// Matched rule set for the 1.250 lint benchmark.
//
// This file is the reason the ESLint numbers mean anything. A linter's wall time is a
// function of how many rules it runs, so timing ESLint on its recommended set against
// oxlint on its defaults would measure the two CONFIGURATIONS, not the two tools.
//
// The set below is the intersection all three JS linters implement natively: correctness
// rules over plain JavaScript, no type-aware rules (those need the TypeScript compiler and
// belong to 1.251), no stylistic rules (those are a formatter's job — see 1.253).
export default [
  {
    files: ["**/*.js"],
    languageOptions: { ecmaVersion: 2022, sourceType: "commonjs" },
    linterOptions: { reportUnusedDisableDirectives: false },
    rules: {
      "no-unused-vars": "error",
      "no-undef": "off",          // needs env globals the corpus does not declare
      "no-dupe-keys": "error",
      "no-dupe-args": "error",
      "no-duplicate-case": "error",
      "no-unreachable": "error",
      "no-constant-condition": "error",
      "no-empty": "error",
      "no-extra-boolean-cast": "error",
      "no-self-assign": "error",
      "no-sparse-arrays": "error",
      "use-isnan": "error",
      "valid-typeof": "error",
      "no-fallthrough": "error",
      "no-redeclare": "error",
      "no-cond-assign": "error",
      "no-debugger": "error",
      "no-control-regex": "error",
    },
  },
];
