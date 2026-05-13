# First Loop Runbook: Turns 1-12

## Target

Run the first 12 Qwen turns on the ThinkPad and copy evidence back into this
coordination repo without repairing the generated artifact with Codex.

## ThinkPad Target

```text
Host: hardik@100.89.101.40
SSH key from Windows: openclaw-setup-guide/.codex-local/thinkpad_ed25519
Model: qwen2.5-coder:3b
Ollama API: http://127.0.0.1:11434/api/generate
Remote work root: ~/thinkpad24turns-test
Remote project root: ~/thinkpad24turns-test/thinkpad-build-observatory
```

## Evidence Requirements

Each run should leave:

```text
runs/turn-XX/
  prompt.md
  response.txt
  changed-files.txt
  elapsed.txt
  validation.txt
```

The project should also keep a human-readable cumulative log:

```text
thinkpad-build-observatory/docs/qwen-build-log.md
```

## Codex Boundary

During the first loop, Codex may:

- start SSH commands,
- send prompts to the ThinkPad,
- copy generated evidence back,
- inspect files,
- report status.

During the first loop, Codex must not:

- rewrite generated project files,
- fix broken HTML/CSS/JS,
- add missing application features,
- normalize Qwen prose,
- hide Qwen mistakes.

## First Checkpoint

After run 12, copy the remote project and `runs/` evidence into:

```text
state/first-loop/
```

Then report:

- completed turn count,
- files created,
- validator or syntax results if available,
- obvious blockers,
- recommended prompt adjustments for turns 13-24.

