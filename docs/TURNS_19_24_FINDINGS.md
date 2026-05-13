# Turns 19-24 Findings

## Summary

The final six turns completed the 24-turn ThinkPad/Qwen experiment. The first
final-loop controller repeated the timeout pattern seen earlier, so it was
stopped after two equivalent failures and replaced with a micro-controller for
turns 22-24.

Outcome for turns 19-24:

- 6 turns attempted.
- 4 turns completed.
- 2 turns timed out.
- No raw runtime files were repaired by Codex.
- The final raw project now includes Qwen-authored validation, handoff, and
  retrospective documentation.

## Turn Results

| Turn | Controller | Elapsed | Target | Result |
| ---: | --- | ---: | --- | --- |
| 19 | `turns-19-24-markdown-only` | 0.00s | `docs/turn-19-ui-copy-tightening.md` | Timeout |
| 20 | `turns-19-24-markdown-only` | 208.55s | `docs/validation-report.md` | Completed |
| 21 | `turns-19-24-markdown-only` | 0.00s | `docs/turn-21-raw-consistency-pass.md` | Timeout |
| 22 | `turns-22-24-micro-markdown` | 70.07s | `docs/turn-22-validator-run-summary.md` | Completed |
| 23 | `turns-22-24-micro-markdown` | 76.01s | `docs/handoff-to-codex.md` | Completed |
| 24 | `turns-22-24-micro-markdown` | 65.51s | `docs/qwen-retrospective.md` | Completed |

## Validation Evidence

Independent local checks after copying the final raw output:

```text
PASS node --check app.js
PASS python -m json.tool data/runs.json
PASS python -m json.tool data/hardware.json
PASS public redaction scan for state\turns-19-24
FAIL node --check scripts/validate-static-site.js
```

The validator failure is the same raw Qwen issue from turn 17: the generated
JavaScript file is Markdown-fenced and is therefore not executable JavaScript.
Codex did not strip those fences because the raw artifact must stay intact until
the final repair phase.

## Controller Lessons

### The first final-loop controller was still too heavy

The `turns-19-24-markdown-only` controller included a file list plus a validation
snapshot. That was enough context to help turn 20, but turns 19 and 21 timed out.
After the second timeout, the surface was stopped according to the retry rule.

### The micro-controller recovered the run

The `turns-22-24-micro-markdown` controller used almost no context, a smaller
output cap, and very explicit summaries. It completed all three remaining turns
quickly:

- turn 22 in 70.07 seconds;
- turn 23 in 76.01 seconds;
- turn 24 in 65.51 seconds.

For this ThinkPad/Qwen route, micro-prompts are the most reliable way to finish
documentation-heavy work.

## Full 24-Turn Outcome

Across all 24 Qwen turns:

- 16 turns completed.
- 8 turns failed by timeout.
- The core static artifact exists and basic app/data syntax checks pass.
- The generated validator script is broken raw output.
- The raw project contains enough provenance for a credible final Codex repair
  and report phase.

## Next Phase

The 24-turn Qwen boundary is now complete. The next phase may be Codex-owned:

1. Preserve and upload the raw Qwen artifact.
2. Create `codex-fix/` with repaired executable files if needed.
3. Write the final report and memory/skill update notes for future ThinkPad
   workflows.

