You are Qwen on a ThinkPad e530. Continue a static site called ThinkPad Build Observatory. Use only plain HTML, CSS, JS, JSON, and Markdown. Return JSON only: {"files":[{"path":"relative/path","content":"full file content"}],"notes":"short note"}. Keep output short. No markdown fences. No external links, CDNs, package managers, or network calls.

Turn 09: Hardware profile pass
Instruction: Update data/hardware.json with concise ThinkPad e530 hardware, qwen2.5-coder:3b model, CPU-only constraint, 24-turn budget, and direct Ollama HTTP route.

Context:
Existing files: README.md, app.js, data/hardware-seed.json, data/hardware.json, data/runs-seed.json, data/runs.json, docs/data-schema.md, docs/file-manifest.md, docs/qwen-build-log.md, index.html, styles.css

data/runs.json first 1400 chars:
[
  {
    "id": 1,
    "date": "2023-10-01",
    "description": "Initial setup and basic files created."
  }
]

data/hardware.json first 1400 chars:
[
  {
    "id": 1,
    "name": "ThinkPad e530",
    "specs": [
      {"feature": "Processor", "value": "Intel Core i7-8565U"},
      {"feature": "RAM", "value": "16GB DDR4"},
      {"feature": "Storage", "value": "512GB SSD"}
    ]
  }
]

index.html first 1400 chars:
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ThinkPad Build Observatory</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header id="hero">
    <h1>ThinkPad Build Observatory</h1>
  </header>

  <section id="timeline">
    <h2>Timeline</h2>
    <!-- Timeline content will be dynamically loaded here using JavaScript -->
  </section>

  <section id="artifacts">
    <h2>Artifacts</h2>
    <!-- Artifacts content will be dynamically loaded here using JavaScript -->
  </section>

  <section id="validation">
    <h2>Validation</h2>
    <!-- Validation content will be dynamically loaded here using JavaScript -->
  </section>

  <section id="hardware">
    <h2>Hardware Specifications</h2>
    <!-- Hardware specifications content will be dynamically loaded here using JavaScript -->
  </section>

  <footer id="footer">
    <p>&copy; 2023 ThinkPad Build Observatory</p>
  </footer>

  <script src="app.js"></script>
</body>
</html>

app.js first 1400 chars:
// Placeholder for JavaScript to load data and populate sections dynamically

README.md first 1400 chars:
# ThinkPad Build Observatory

This project is a static portfolio showcasing the build process of a ThinkPad e530.

## Directory Structure
- `docs/`
  - `qwen-build-log.md`
  - `file-manifest.md`
- `index.html`


Return JSON only. Keep the total response short enough to finish within five minutes.