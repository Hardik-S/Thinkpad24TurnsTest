# Final Loop Runbook: Turns 19-24

## Goal

Run the last six ThinkPad/Qwen turns without violating the experiment boundary:
Qwen may continue producing raw project evidence, but Codex must not repair the
generated artifact until all 24 turns are complete.

Turns 13-18 showed that the reliable pattern is one direct target file per turn,
small prompts, no JSON wrapper, and a short validation snapshot. The final loop
uses that same shape and avoids executable output because turn 17 proved that
code-generation turns can still return Markdown-wrapped JavaScript.

## Command

Run this on the ThinkPad from the copied coordination repo:

```powershell
python scripts\thinkpad_turns_19_24_controller.py
```

The controller expects the same local worker layout as the previous loops:

```text
~/thinkpad24turns-test/
  progress.json
  runs/
  thinkpad-build-observatory/
```

## Turn Targets

| Turn | Target file | Purpose |
| ---: | --- | --- |
| 19 | `docs/turn-19-ui-copy-tightening.md` | Raw notes on unclear visible copy and later replacement wording. |
| 20 | `docs/validation-report.md` | Raw validation report for required files, JSON, app syntax, and the known validator issue. |
| 21 | `docs/turn-21-raw-consistency-pass.md` | Raw consistency review across app copy, README, data files, and build log. |
| 22 | `docs/turn-22-validator-run-summary.md` | Raw summary of what validation currently proves and what final Codex should rerun. |
| 23 | `docs/handoff-to-codex.md` | Final handoff that preserves raw output and scopes later `codex-fix/` work. |
| 24 | `docs/qwen-retrospective.md` | Local-worker retrospective for future ThinkPad controller design. |

## Evidence Rules

Each turn records:

```text
runs/turn-XX/
  prompt.md
  response.txt
  changed-files.txt
  elapsed.txt
  validation.txt
```

The controller also appends each turn to `progress.json` with the controller id
`turns-19-24-markdown-only`.

## Boundary

Do not strip fences, rewrite JavaScript, patch CSS, or edit the raw app during
this loop. If the finished raw site is broken after turn 24, Codex should create
`codex-fix/` and document every repair separately from the preserved Qwen output.
