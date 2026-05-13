from pathlib import Path
import json
import subprocess
import time
import traceback
import urllib.request

ROOT = Path.home() / "thinkpad24turns-test"
PROJECT = ROOT / "thinkpad-build-observatory"
RUNS = ROOT / "runs"
MODEL = "qwen2.5-coder:3b"
API_URL = "http://127.0.0.1:11434/api/generate"

TURNS = [
    (
        19,
        "UI copy tightening notes",
        "docs/turn-19-ui-copy-tightening.md",
        "Write concise UI-copy tightening notes for the current static site. Identify unclear visible copy, propose exact replacement wording, and keep all suggestions for later Qwen or final Codex repair rather than editing runtime files.",
    ),
    (
        20,
        "Validation report draft",
        "docs/validation-report.md",
        "Draft a validation report for the raw ThinkPad Build Observatory. Include required-file checks, JSON checks, app syntax state, the fenced-validator issue, and the no-Codex-repair boundary.",
    ),
    (
        21,
        "Raw consistency pass",
        "docs/turn-21-raw-consistency-pass.md",
        "Write a raw consistency review. Compare README, build log, data files, and visible app claims. List contradictions or missing evidence without repairing any source files.",
    ),
    (
        22,
        "Validator run summary",
        "docs/turn-22-validator-run-summary.md",
        "Write a validator run summary from the current validation snapshot. Separate checks that pass, checks that fail because of raw Qwen output, and checks to rerun during final Codex repair.",
    ),
    (
        23,
        "Final handoff to Codex",
        "docs/handoff-to-codex.md",
        "Draft the final handoff to Codex for after turn 24. Include what exists, what failed, what must be preserved as raw Qwen output, and what Codex may repair only inside codex-fix/.",
    ),
    (
        24,
        "Qwen retrospective",
        "docs/qwen-retrospective.md",
        "Write a short retrospective from the local Qwen worker perspective. Cover what worked, where the five-minute cap hurt quality, and what future worker controllers should do differently.",
    ),
]


def file_list():
    files = []
    for path in sorted(PROJECT.rglob("*")):
        if path.is_file():
            files.append(path.relative_to(PROJECT).as_posix())
    return "\n".join(files[:100])


def short_validation():
    lines = []
    required = [
        "README.md",
        "index.html",
        "styles.css",
        "app.js",
        "data/runs.json",
        "data/hardware.json",
    ]
    for rel in required:
        lines.append(("PASS" if (PROJECT / rel).exists() else "MISSING") + f" {rel}")
    for rel in ["data/runs.json", "data/hardware.json"]:
        path = PROJECT / rel
        if path.exists():
            try:
                json.loads(path.read_text(encoding="utf-8"))
                lines.append(f"PASS json {rel}")
            except Exception as exc:
                lines.append(f"FAIL json {rel}: {exc}")
    app = PROJECT / "app.js"
    if app.exists():
        try:
            out = subprocess.run(
                ["node", "--check", str(app)],
                text=True,
                capture_output=True,
                timeout=20,
            )
            lines.append(("PASS" if out.returncode == 0 else "FAIL") + " node --check app.js")
            if out.stderr.strip():
                lines.append(out.stderr.strip()[:500])
        except Exception as exc:
            lines.append(f"WARN node check unavailable: {exc}")
    validator = PROJECT / "scripts" / "validate-static-site.js"
    if validator.exists():
        try:
            out = subprocess.run(
                ["node", "--check", str(validator)],
                text=True,
                capture_output=True,
                timeout=20,
            )
            lines.append(
                ("PASS" if out.returncode == 0 else "FAIL")
                + " node --check scripts/validate-static-site.js"
            )
            if out.stderr.strip():
                lines.append(out.stderr.strip()[:500])
        except Exception as exc:
            lines.append(f"WARN validator check unavailable: {exc}")
    return "\n".join(lines)


def prompt_for(turn, title, target, instruction):
    return f"""You are Qwen running locally on a ThinkPad e530.
This is turn {turn} of 24 in the ThinkPad Build Observatory experiment.
Target file: {target}

Instruction: {instruction}

Known files:
{file_list()}

Current validation summary:
{short_validation()}

Rules:
- Return only the complete Markdown content for {target}. No markdown fences.
- Keep output under 750 words.
- Do not claim Codex repaired anything.
- Do not edit or request edits to runtime files in this turn; this controller writes only the target Markdown file.
- Preserve the raw Qwen artifact boundary until all 24 turns are complete.
- Do not include secrets, private keys, IP addresses, or credentials.
- Do not use external dependencies.
"""


def call_model(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1, "top_p": 0.8, "num_predict": 560, "num_ctx": 3072},
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    start = time.time()
    with urllib.request.urlopen(req, timeout=300) as resp:
        raw = resp.read()
    elapsed = time.time() - start
    data = json.loads(raw.decode("utf-8"))
    return data.get("response", "").strip() + "\n", elapsed


def load_progress():
    path = ROOT / "progress.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "model": MODEL,
        "turns": [],
    }


def main():
    progress = load_progress()
    seen = {item["turn"] for item in progress.get("turns", [])}
    for turn, title, target, instruction in TURNS:
        if turn in seen:
            continue
        run_dir = RUNS / f"turn-{turn:02d}"
        run_dir.mkdir(parents=True, exist_ok=True)
        prompt = prompt_for(turn, title, target, instruction)
        (run_dir / "prompt.md").write_text(prompt, encoding="utf-8")
        changed = []
        elapsed = 0.0
        error_text = None
        try:
            response, elapsed = call_model(prompt)
            (run_dir / "response.txt").write_text(response, encoding="utf-8")
            output = PROJECT / target
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(response, encoding="utf-8", newline="\n")
            changed.append(target)
            status = "completed"
        except Exception:
            status = "failed"
            error_text = traceback.format_exc()
            (run_dir / "error.txt").write_text(error_text, encoding="utf-8")
        (run_dir / "changed-files.txt").write_text(
            "\n".join(changed) + ("\n" if changed else ""),
            encoding="utf-8",
        )
        (run_dir / "elapsed.txt").write_text(f"{elapsed:.2f}s\n", encoding="utf-8")
        (run_dir / "validation.txt").write_text(short_validation() + "\n", encoding="utf-8")
        progress.setdefault("turns", []).append(
            {
                "turn": turn,
                "title": title,
                "status": status,
                "elapsed_seconds": round(elapsed, 2),
                "changed_files": changed,
                "error": bool(error_text),
                "controller": "turns-19-24-markdown-only",
            }
        )
        progress["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        (ROOT / "progress.json").write_text(json.dumps(progress, indent=2), encoding="utf-8")
        print(
            f"TURN {turn:02d} {status} elapsed={elapsed:.2f}s files={','.join(changed) if changed else '-'}",
            flush=True,
        )
    print("TURNS_19_24_DONE", flush=True)


if __name__ == "__main__":
    main()
