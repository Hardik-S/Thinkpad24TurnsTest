You are Qwen running locally on a ThinkPad e530. Build only the requested part of a static portfolio project called ThinkPad Build Observatory. Use no package manager, no framework, no external assets, no CDN, and no network calls. Keep changes small. Prefer plain HTML, CSS, JavaScript, JSON, and Markdown. Preserve existing files unless the current instruction explicitly says to edit them. Return JSON only, with this exact shape: {"files":[{"path":"relative/path","content":"full file content"}],"notes":"short risk summary"}. Do not wrap the JSON in markdown fences.

Turn 02: Data schema
Instruction: Define the run evidence data schema. Create docs/data-schema.md describing data/runs.json and data/hardware.json. Create small valid seed JSON files with enough fields for later rendering.

Current project tree:
- README.md (210 bytes)
- docs/file-manifest.md (97 bytes)
- docs/qwen-build-log.md (270 bytes)

Current relevant file contents:

--- README.md ---
# ThinkPad Build Observatory

This project is a static portfolio showcasing the build process of a ThinkPad e530.

## Directory Structure
- `docs/`
  - `qwen-build-log.md`
  - `file-manifest.md`
- `index.html`


--- docs/qwen-build-log.md ---
# Qwen Build Log

This log will track the build process of the ThinkPad e530.

## Steps Taken
1. **Initial Setup**: Created project structure and basic files.
2. **README.md**: Added brief description and directory structure.
3. **qwen-build-log.md**: Initial log entry.

--- docs/file-manifest.md ---
# File Manifest
- `README.md`
- `docs/qwen-build-log.md`
- `docs/file-manifest.md`
- `index.html`


Return JSON only. Include full content for every file you create or modify. Keep each file concise enough to fit this response.