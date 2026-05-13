# Loop 1 Findings: Turns 1-12

## Summary

Loop 1 proved that the ThinkPad can generate useful project artifacts with
`qwen2.5-coder:3b`, but it also proved that the controller shape matters more
than the high-level task label.

The raw outcome was mixed:

- 12 turns attempted.
- 6 turns completed.
- 6 turns timed out at the 300-second wall-clock cap.
- The copied raw artifact still has a syntactically valid `app.js` and valid
  JSON data files.
- Codex did not repair the generated project.

## Completed Turns

| Turn | Controller | Elapsed | Files |
| ---: | --- | ---: | --- |
| 1 | broad JSON | 112.62s | `README.md`, `docs/qwen-build-log.md`, `docs/file-manifest.md` |
| 2 | broad JSON | 250.29s | `data/runs.json`, `data/hardware.json`, schema docs, seed files |
| 4 | broad JSON | 216.90s | `styles.css` |
| 6 | narrow JSON | 271.25s | `index.html`, `styles.css`, `app.js` |
| 7 | narrow JSON | 182.52s | `app.js` |
| 9 | narrow JSON | 252.09s | `data/hardware.json`, `data/runs.json` |

## Failed Turns

| Turn | Controller | Failure type | Interpretation |
| ---: | --- | --- | --- |
| 3 | broad JSON | Timeout | Asking for HTML with full context and JSON wrapping was too heavy. |
| 5 | broad JSON | Timeout | Asking for app-shell code with full context repeated the same failure surface. |
| 8 | narrow JSON | Timeout | Updating structured data with a JSON envelope remained too expensive. |
| 10 | narrow JSON | Timeout | Editing multiple existing files from copied context still exceeded the cap. |
| 11 | ultra single-file | Timeout | Including full progress context made even Markdown generation too slow. |
| 12 | ultra single-file | Timeout | Same context-heavy Markdown surface failed again. |

## Controller Lessons

### Broad JSON controller

This controller included a project tree, several file excerpts, and required a
JSON file map response. It worked for the earliest simple files but timed out
once HTML and JavaScript tasks appeared.

Do not reuse it for slow local-model turns unless the prompt is extremely small.

### Narrow JSON controller

This controller reduced context and output length. It recovered the project
after turn 3 failed by producing the core browser files in turn 6. It still
timed out on JSON/data and multi-file copy tasks.

Use it only when the target is one small file and the response can stay short.

### Ultra single-file controller

This controller removed JSON wrapping but still included too much progress
context. It failed on both documentation turns.

The failure points to context size, not only response format.

## Practical Prompt Rules For Turns 13-24

Use these rules until the final Codex repair phase:

1. One target file per turn.
2. No JSON envelope unless the target file itself is JSON.
3. No full progress JSON in the prompt.
4. No full copied source files unless the turn explicitly edits that file.
5. Prefer new documentation or validator artifacts over large rewrites.
6. Ask for under 500-700 tokens of output.
7. Save raw response separately even if the written artifact is invalid.
8. Treat timeouts as data, not as something to hide.

## Current Raw Artifact Status

Fresh local checks after copying loop 1:

```text
PASS node --check state\first-loop\thinkpad-build-observatory\app.js
PASS json data/runs.json
PASS json data/hardware.json
PASS public redaction scan for state\first-loop
```

This does not mean the site is visually complete. It means the raw artifact is
syntax-checkable enough to continue the experiment.

## Next-Six Strategy

Turns 13-18 should not try to comprehensively polish the existing app. That is
too large for the observed ThinkPad/Qwen envelope. Instead:

- make Qwen write focused docs that describe responsive, accessibility, error,
  and no-external-dependency findings;
- make Qwen attempt a compact validator script;
- make Qwen record validator-repair notes from whatever checks are available;
- preserve the raw output and evidence for each turn.

This keeps the project portfolio-visible while generating workflow knowledge
that can improve the final Codex repair phase and future ThinkPad workflows.

