# ThinkPad Build Observatory 24-Turn Plan

## Goal

Build a static, portfolio-visible site whose subject is the experiment itself:
an old ThinkPad using a local 3B coding model to generate a working software
artifact over 24 supervised turns.

The project should make the provenance visible. A reviewer should be able to
open the final page and understand what the ThinkPad built, which runs
succeeded, which runs failed, how validation worked, and where Codex stepped in
after the 24-turn boundary.

## Why This Is Feasible

The ThinkPad route is already verified for direct Ollama HTTP calls to
`qwen2.5-coder:3b`, but prior benchmarks showed that multi-file structured
output can be brittle. This project avoids that failure mode by keeping each
turn narrow and file-focused.

The site uses only browser-native files:

```text
thinkpad-build-observatory/
  index.html
  styles.css
  app.js
  data/
    runs.json
    hardware.json
  docs/
    qwen-build-log.md
    validation-report.md
    handoff-to-codex.md
    qwen-retrospective.md
  scripts/
    validate-static-site.js
  README.md
```

No package manager, bundler, framework, database, API key, or deploy-specific
configuration is allowed during the Qwen phase.

## Non-Negotiable Boundaries

- Qwen creates or edits the portfolio artifact during turns 1-24.
- Codex may create coordination docs and run orchestration only.
- Codex must not repair generated project files before turn 24 is complete.
- Every Qwen turn has a maximum wall-clock budget of 5 minutes.
- Each turn writes a short evidence note under `runs/`.
- The raw Qwen output must be preserved even if broken.
- If the original is broken after turn 24, Codex repair goes into `codex-fix/`.
- Public output must not include credentials, private SSH keys, raw local
  credential paths, or private network secrets.

## Operating Cadence

Run two staged loops:

1. Runs 1-12: create the core site, data model, first visual pass, and README.
2. Runs 13-24: polish, validation, no-dependency cleanup, handoff, and Qwen
   retrospective.

At the run-12 checkpoint, Codex may inspect generated files and evidence, but
must not repair the project. Codex may only decide whether the second loop
needs narrower prompts.

## Success Criteria

Raw Qwen success means:

- `index.html`, `styles.css`, `app.js`, `data/runs.json`, `data/hardware.json`,
  docs, and validator files exist.
- The site opens locally without external dependencies.
- The validator script runs with Node and reports clear pass/fail evidence.
- The README explains the experiment and the provenance.
- The build log documents all 24 turns.

Codex end-stage success means:

- The raw Qwen artifact is uploaded to a `Hardik-S` GitHub repo.
- If the raw artifact is broken, `codex-fix/` contains a repaired version and a
  report explaining what was repaired.
- Workflow findings are captured in a report plus memory/skill update notes.

## Repo Publication Policy

This project is public by default because it is a portfolio artifact and should
not contain secrets. If a generated file accidentally includes private data,
Codex must remove or quarantine that content before publishing and report the
reason.

