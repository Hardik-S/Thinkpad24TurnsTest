# Prompts for Turns 1-12

All prompts share this system instruction:

```text
You are Qwen running locally on a ThinkPad e530. Build only the requested part
of a static portfolio project called ThinkPad Build Observatory. Use no package
manager, no framework, no external assets, no CDN, and no network calls. Keep
changes small. Prefer plain HTML, CSS, JavaScript, JSON, and Markdown. Preserve
existing files unless the current instruction explicitly says to edit them.
After each turn, summarize changed files and any risks.
```

## Turn 01

Create the project brief, directory structure, and file manifest for
`thinkpad-build-observatory`. Write `README.md`, `docs/qwen-build-log.md`, and
`docs/file-manifest.md`. Do not create app code yet.

## Turn 02

Define the run evidence data schema. Create `docs/data-schema.md` describing
`data/runs.json` and `data/hardware.json`. Create small valid seed JSON files
with enough fields for later rendering.

## Turn 03

Create `index.html` with semantic regions for hero, run timeline, artifact
gallery, validation status, hardware profile, and footer. Link `styles.css` and
`app.js`, but keep JavaScript behavior minimal for now.

## Turn 04

Create `styles.css` with a restrained portfolio visual identity for a technical
artifact: readable, responsive, not marketing-heavy, and not a single-color
palette. Support mobile and desktop without horizontal scrolling.

## Turn 05

Create `app.js` with a boot function that loads `data/runs.json` and
`data/hardware.json`, handles fetch errors, and renders simple placeholder
content into existing HTML regions.

## Turn 06

Extend `app.js` to render a run timeline from `data/runs.json`. Include turn
number, title, status, elapsed time, changed files, and a short note.

## Turn 07

Extend `app.js` and seed data to render an artifact gallery. Each artifact
should show file path, purpose, producing turn, and whether it is raw Qwen
output or later Codex repair.

## Turn 08

Extend `app.js` and seed data to render a validation/status panel. Include pass,
warn, fail, and not-run states. Make the UI honest about missing validation.

## Turn 09

Add a model and hardware profile panel using `data/hardware.json`. Include
ThinkPad model, CPU-only constraint, local model name, run budget, and the
reason direct Ollama HTTP is used.

## Turn 10

Tighten visible build-story copy in `index.html` and README. The site should
clearly say it was built on a 2012 ThinkPad by a local 3B coding model over 24
supervised turns.

## Turn 11

Expand `data/runs.json` and `data/hardware.json` with realistic first-loop
placeholder records for turns 1-12. Mark future turns honestly as planned or
not-run.

## Turn 12

Draft the run-12 checkpoint handoff in `docs/handoff-to-codex.md`. Update
`docs/qwen-build-log.md` with a first-loop summary and list risks for turns
13-24. Do not claim final completion.

