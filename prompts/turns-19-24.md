# Prompts for Turns 19-24

All prompts are direct-file prompts. Qwen should return only the full content of
the target Markdown file.

## Turn 19

Target: `docs/turn-19-ui-copy-tightening.md`

Write concise UI copy and information-architecture notes for the current static
site. Include what copy should be visible on the first screen, what labels
should be clearer, and what not to overclaim.

## Turn 20

Target: `docs/validation-report.md`

Write the final raw-Qwen validation report. Include known passing checks:
`app.js` syntax, JSON parsing, redaction scan. Include known failure:
`scripts/validate-static-site.js` is invalid because it was Markdown-fenced.

## Turn 21

Target: `docs/turn-21-raw-consistency-pass.md`

Review the raw project for consistency. Mention mismatches between planned 24
turns and actual completed/failed turns, extra seed files, and the fact that
Codex has not repaired the generated project.

## Turn 22

Target: `docs/turn-22-validator-run-summary.md`

Summarize validator and static-check evidence. Separate independent checks run
by Codex from Qwen-generated validator output. Be explicit that the Qwen
validator script is broken raw output.

## Turn 23

Target: `docs/handoff-to-codex.md`

Write the final handoff to Codex. Include files to preserve, files to inspect,
known broken areas, suggested `codex-fix/` priorities, and the rule that raw
Qwen output must remain available.

## Turn 24

Target: `docs/qwen-retrospective.md`

Write a retrospective from Qwen's perspective. Include what prompt shapes
worked, what failed, how to run future ThinkPad workflows, and what Codex should
learn from this experiment.

