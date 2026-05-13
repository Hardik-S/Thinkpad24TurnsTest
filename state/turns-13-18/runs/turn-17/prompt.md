You are Qwen running locally on a ThinkPad e530.
This is turn 17 of 24 in the ThinkPad Build Observatory experiment.
Target file: scripts/validate-static-site.js

Instruction: Write only a compact Node CommonJS script. It should check required files, parse data/runs.json and data/hardware.json, run node --check app.js, and scan .html/.css/.js/.json/.md files for http://, https://, or cdn. Keep it under 120 lines.

Known files:
README.md
app.js
data/hardware-seed.json
data/hardware.json
data/runs-seed.json
data/runs.json
docs/data-schema.md
docs/file-manifest.md
docs/qwen-build-log.md
docs/turn-13-responsive-polish.md
docs/turn-14-accessibility-pass.md
docs/turn-15-empty-error-states.md
docs/turn-16-no-external-cleanup.md
index.html
styles.css

Current validation summary:
PASS README.md
PASS index.html
PASS styles.css
PASS app.js
PASS data/runs.json
PASS data/hardware.json
PASS json data/runs.json
PASS json data/hardware.json
PASS node --check app.js

Rules:
- Return only the complete JavaScript source for scripts/validate-static-site.js. No markdown fences, no explanation.
- Keep output under 700 words or under 120 JavaScript lines.
- Do not claim Codex repaired anything.
- Do not include secrets, private keys, IP addresses, or credentials.
- Do not use external dependencies.
