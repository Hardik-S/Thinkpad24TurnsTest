# 24-Turn Schedule

Each Qwen turn should be one short-capped direct Ollama HTTP generation on the
ThinkPad. The controller may save the prompt, model response, generated files,
and validation output, but should not ask Codex to repair anything until all 24
turns finish.

## Loop 1: Runs 1-12

1. Create the project brief, directory structure, and file manifest.
2. Define the data schema for run evidence.
3. Create `index.html` skeleton with semantic regions.
4. Create `styles.css` base layout and visual identity.
5. Create `app.js` boot/render shell.
6. Add run timeline rendering.
7. Add artifact gallery rendering.
8. Add validation/status panel rendering.
9. Add model and hardware profile panel.
10. Draft visible build-story copy.
11. Create seed `data/runs.json` and `data/hardware.json`.
12. Draft `README.md` and first checkpoint handoff.

## Loop 2: Runs 13-24

13. Responsive polish pass.
14. Accessibility pass.
15. Empty and error state pass.
16. No-external-dependency cleanup.
17. Create `scripts/validate-static-site.js`.
18. Repair only issues reported by the validator, still using Qwen.
19. Tighten visible UI copy.
20. Draft `docs/validation-report.md`.
21. Final raw project consistency pass.
22. Run validator and record summary.
23. Draft `docs/handoff-to-codex.md`.
24. Draft `docs/qwen-retrospective.md`.

