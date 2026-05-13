# Prompts for Turns 13-18

The next six prompts intentionally avoid multi-file rewrites. Each run has one
target file and a tiny context packet.

## Turn 13

Target: `docs/turn-13-responsive-polish.md`

Write a short responsive-design review of the current static site. Include
specific CSS risks, mobile layout risks, and two small changes that a later
repair pass could make. Do not claim to have edited CSS unless this file is the
only output.

## Turn 14

Target: `docs/turn-14-accessibility-pass.md`

Write a short accessibility review. Include headings/landmarks, keyboard
navigation, color contrast, reduced motion, and screen-reader risks.

## Turn 15

Target: `docs/turn-15-empty-error-states.md`

Write a short review of empty and error states for the static site. Include what
should happen if JSON fetch fails, if no runs exist, or if validation entries
are missing.

## Turn 16

Target: `docs/turn-16-no-external-cleanup.md`

Write a short no-external-dependency audit. Confirm the desired boundary:
browser-native only, no CDN, no external images, no API calls, no package
install during Qwen runs.

## Turn 17

Target: `scripts/validate-static-site.js`

Write a compact Node script that checks required files exist, JSON files parse,
`app.js` has no syntax errors through `node --check`, and source files do not
contain `http://`, `https://`, or `cdn.`.

## Turn 18

Target: `docs/turn-18-validator-repair-notes.md`

Write notes from the available validation evidence. Separate what Qwen can still
attempt in turns 19-24 from what Codex should save for the final `codex-fix/`
phase.

