# Turns 13-18 Findings

## Summary

Turns 13-18 were materially better than turns 1-12 because the controller used
one target file per turn, small prompts, no JSON envelope, and minimal context.

Outcome:

- 6 turns attempted.
- 6 turns completed.
- 0 timeouts.
- 5 documentation artifacts were usable as raw Qwen output.
- 1 code artifact was generated but failed syntax validation because Qwen wrapped
  JavaScript in Markdown fences.

## Turn Results

| Turn | Elapsed | Target | Result |
| ---: | ---: | --- | --- |
| 13 | 159.01s | `docs/turn-13-responsive-polish.md` | Completed |
| 14 | 200.30s | `docs/turn-14-accessibility-pass.md` | Completed |
| 15 | 129.99s | `docs/turn-15-empty-error-states.md` | Completed |
| 16 | 133.46s | `docs/turn-16-no-external-cleanup.md` | Completed |
| 17 | 196.60s | `scripts/validate-static-site.js` | Completed but invalid JavaScript |
| 18 | 194.27s | `docs/turn-18-validator-repair-notes.md` | Completed |

## Validation Evidence

Independent checks after copying the raw ThinkPad output:

```text
PASS node --check app.js
PASS python -m json.tool data/runs.json
PASS python -m json.tool data/hardware.json
PASS public redaction scan for state\turns-13-18
FAIL node --check scripts/validate-static-site.js
```

The generated validator failure is not a logic bug. The file begins with a
Markdown JavaScript fence and ends with a closing Markdown fence.

That means Qwen violated the no-fence instruction and produced Markdown-wrapped
JavaScript. Codex did not strip the fences or repair the file because the raw
artifact must remain untouched until the final Codex phase.

## Important Workflow Lessons

### Direct-file prompts are the current winning pattern

Compared with the loop-1 controllers, the direct-file controller produced six
straight completions. The key differences were:

- no JSON response wrapper;
- one target file only;
- minimal file list context;
- short validation summary instead of full progress JSON;
- tight output budget.

This should be the default for turns 19-24.

### Documentation is a valid portfolio artifact here

The docs generated in turns 13-16 and 18 are not filler. They make the project
observable: a reviewer can see the local model reason about responsive design,
accessibility, empty states, external dependencies, and repair boundaries.

For this experiment, provenance and auditability are part of the product.

### Code generation still needs a fence guard

Even with explicit "no markdown fences" instructions, Qwen returned fenced code
for turn 17. Future code-generation turns should either:

- target Markdown that contains code as a documented artifact, or
- include a dedicated later Qwen turn that rewrites the exact same file without
  fences, or
- use a controller that records raw output and separately writes a sanitized
  derived artifact only after the final 24-turn boundary.

Before turn 24, do not silently sanitize code output.

## Recommendation For Turns 19-24

Use the direct-file controller again, but bias toward:

- `docs/turn-19-ui-copy-tightening.md`
- `docs/turn-20-validation-report.md`
- `docs/turn-21-raw-consistency-pass.md`
- `docs/turn-22-validator-run-summary.md`
- `docs/handoff-to-codex.md`
- `docs/qwen-retrospective.md`

If a code turn is attempted, make it a self-contained Markdown artifact first.
The final Codex phase can then create `codex-fix/` and repair executable files
without losing the raw Qwen trail.
