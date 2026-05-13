# Next Six Runbook: Turns 13-18

## Goal

Run six more ThinkPad/Qwen turns while applying the loop-1 findings:

- one target file per turn;
- tiny prompts;
- no large context dumps;
- no Codex repair;
- evidence copied back immediately after the checkpoint.

## Turn Targets

| Turn | Target file | Purpose |
| ---: | --- | --- |
| 13 | `docs/turn-13-responsive-polish.md` | Qwen responsive-design observations and recommended small CSS changes. |
| 14 | `docs/turn-14-accessibility-pass.md` | Qwen accessibility observations, gaps, and possible fixes. |
| 15 | `docs/turn-15-empty-error-states.md` | Qwen notes on empty/error states already present or missing. |
| 16 | `docs/turn-16-no-external-cleanup.md` | Qwen no-external-dependency audit and cleanup notes. |
| 17 | `scripts/validate-static-site.js` | Qwen attempt at a compact Node validator. |
| 18 | `docs/turn-18-validator-repair-notes.md` | Qwen notes from validator/static checks and proposed raw repair priorities. |

## Why Mostly Docs

Loop 1 showed that large source rewrites are too slow for the current five-minute
cap. Documentation artifacts are not filler here; they are the product's
provenance layer. The final portfolio story depends on being able to show what
the local model could and could not do.

## Controller Behavior

The controller writes direct model responses to the target file. It does not ask
for JSON and it does not repair invalid output. It records:

```text
runs/turn-XX/
  prompt.md
  response.txt
  changed-files.txt
  elapsed.txt
  validation.txt
```

If a turn times out, the controller records the timeout and continues unless two
equivalent failures show that the surface is exhausted.

