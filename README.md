# ThinkPad 24 Turns Test

This folder coordinates a public portfolio experiment: a 2012 ThinkPad `e530`
running local `qwen2.5-coder:3b` gets 24 supervised, short-capped turns to build
a static site called **ThinkPad Build Observatory**.

Codex owns only coordination, review, publishing, and final repair. The project
artifact itself must be generated on the ThinkPad by Qwen during the 24 turns.

## Experiment Contract

- Worker machine: ThinkPad `e530`
- Model: `qwen2.5-coder:3b` through direct Ollama HTTP
- Turn budget: 24 total runs
- Time cap: 5 minutes per run
- First checkpoint: after run 12
- Final checkpoint: after run 24
- Project type: static HTML, CSS, JavaScript, JSON, Markdown
- Package installs: none during Qwen runs
- External runtime dependencies: none
- Codex repair: forbidden until all 24 Qwen runs complete

## Final Codex Duties

After the 24 ThinkPad Qwen runs finish, Codex may do exactly three end-stage
tasks:

1. Upload the raw Qwen work to GitHub.
2. If the raw project is broken, create `codex-fix/` and put the repaired
   working version there while preserving the raw Qwen output.
3. Write a report and add memory/skill update notes that improve future
   ThinkPad worker workflows.

## Files

- `docs/PLAN.md` - full 24-turn operating plan.
- `docs/TURN_SCHEDULE.md` - exact prompt intent for every Qwen run.
- `docs/FIRST_LOOP_RUNBOOK.md` - commands and evidence rules for runs 1-12.
- `prompts/turns-01-12.md` - first-loop prompts to send to Qwen.
- `state/` - run evidence copied back from the ThinkPad.

