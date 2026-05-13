# ThinkPad Build Observatory - Codex Fix

This directory is the repaired Codex version of the raw ThinkPad/Qwen project.

The raw local-model output is preserved under `state/`. This copy exists because
the final Qwen artifact had a placeholder `app.js`, incorrect seed data, and a
Markdown-fenced validator script. Codex repaired those issues only after all 24
Qwen turns were complete.

## What This Shows

- A ThinkPad e530 ran local `qwen2.5-coder:3b` for 24 supervised turns.
- 16 turns completed and 8 timed out.
- Direct-file and micro-prompt controllers worked best.
- Large context, JSON envelopes, and code-generation turns were fragile.
- The repaired site keeps the failure history visible instead of hiding it.

## Run Locally

From this directory:

```powershell
python -m http.server 4173
```

Open:

```text
http://127.0.0.1:4173
```

Validate:

```powershell
node scripts\validate-static-site.js
```

## Boundary

Do not treat this directory as raw Qwen output. It is the Codex-owned repair
copy requested after the 24-turn experiment ended.
