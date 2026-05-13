# Final Six Runbook: Turns 19-24

## Goal

Complete the 24-turn ThinkPad/Qwen experiment without allowing Codex to repair
the generated project during the Qwen phase.

The final six turns should complete the raw provenance layer:

- UI copy recommendations;
- validation report;
- raw consistency review;
- validator run summary;
- handoff to Codex;
- Qwen retrospective.

## Why These Targets

Turns 13-18 showed that direct-file documentation prompts completed reliably
under the five-minute cap. The one code-generation turn completed but produced
Markdown-fenced JavaScript, so the final six should avoid new executable code.

The raw project already has browser files and data files. The most valuable
remaining Qwen work is to document what exists, what is broken, and what Codex
should repair after the 24-turn boundary.

## Turn Targets

| Turn | Target | Purpose |
| ---: | --- | --- |
| 19 | `docs/turn-19-ui-copy-tightening.md` | Qwen's copy and information-architecture notes. |
| 20 | `docs/validation-report.md` | Qwen-authored final validation report. |
| 21 | `docs/turn-21-raw-consistency-pass.md` | Qwen review of raw project consistency and contradictions. |
| 22 | `docs/turn-22-validator-run-summary.md` | Qwen summary of validator evidence, including the broken validator script. |
| 23 | `docs/handoff-to-codex.md` | Qwen handoff for the final Codex phase. |
| 24 | `docs/qwen-retrospective.md` | Qwen self-retrospective and future workflow rules. |

## Controller Rules

- One target file per turn.
- No JSON envelope.
- No executable-code targets.
- No large source dumps.
- Output under 700 words.
- Record the prompt, response, elapsed time, changed files, and validation.
- If a turn times out, record it and continue.

## Codex Boundary

Codex may start the controller, copy evidence, run independent checks, document
findings, commit, and push. Codex may not repair raw generated project files in
this phase.

