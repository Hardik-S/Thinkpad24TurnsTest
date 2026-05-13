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
    (19, "UI copy tightening", "docs/turn-19-ui-copy-tightening.md", "Write concise UI copy and information-architecture notes. Include first-screen copy, clearer labels, and what not to overclaim."),
    (20, "Raw validation report", "docs/validation-report.md", "Write the final raw-Qwen validation report. Include passing checks: app.js syntax, JSON parsing, redaction scan. Include known failure: scripts/validate-static-site.js is invalid because it was Markdown-fenced."),
    (21, "Raw consistency pass", "docs/turn-21-raw-consistency-pass.md", "Review raw project consistency. Mention mismatches between planned 24 turns and actual completed/failed turns, extra seed files, and no Codex repair yet."),
    (22, "Validator run summary", "docs/turn-22-validator-run-summary.md", "Summarize validator/static-check evidence. Separate independent Codex checks from Qwen-generated validator output. State the Qwen validator script is broken raw output."),
    (23, "Final handoff to Codex", "docs/handoff-to-codex.md", "Write final handoff to Codex. Include files to preserve, files to inspect, known broken areas, suggested codex-fix priorities, and preservation of raw Qwen output."),
    (24, "Qwen retrospective", "docs/qwen-retrospective.md", "Write a retrospective from Qwen's perspective. Include prompt shapes that worked, failures, future ThinkPad workflow rules, and what Codex should learn."),
]


def file_list():
    files = []
    for path in sorted(PROJECT.rglob("*")):
        if path.is_file():
            files.append(path.relative_to(PROJECT).as_posix())
    return "\n".join(files[:120])


def short_progress():
    path = ROOT / "progress.json"
    if not path.exists():
        return "No progress file found."
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = []
    for item in data.get("turns", []):
        rows.append(f"{item.get('turn')}: {item.get('status')} {item.get('elapsed_seconds')}s {','.join(item.get('changed_files', []))}")
    return "\n".join(rows[-18:])


def validation_summary():
    lines = []
    for rel in ["README.md", "index.html", "styles.css", "app.js", "data/runs.json", "data/hardware.json", "scripts/validate-static-site.js"]:
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
            out = subprocess.run(["node", "--check", str(app)], text=True, capture_output=True, timeout=20)
            lines.append(("PASS" if out.returncode == 0 else "FAIL") + " node --check app.js")
        except Exception as exc:
            lines.append(f"WARN app.js syntax check unavailable: {exc}")
    validator = PROJECT / "scripts" / "validate-static-site.js"
    if validator.exists():
        try:
            out = subprocess.run(["node", "--check", str(validator)], text=True, capture_output=True, timeout=20)
            lines.append(("PASS" if out.returncode == 0 else "FAIL") + " node --check scripts/validate-static-site.js")
            if out.stderr.strip():
                lines.append(out.stderr.strip()[:400])
        except Exception as exc:
            lines.append(f"WARN validator syntax check unavailable: {exc}")
    return "\n".join(lines)


def build_prompt(turn, title, target, instruction):
    return f"""You are Qwen running locally on a ThinkPad e530.
This is turn {turn} of 24 in the ThinkPad Build Observatory experiment.

Target file: {target}
Instruction: {instruction}

Known files:
{file_list()}

Recent turn progress:
{short_progress()}

Validation summary:
{validation_summary()}

Rules:
- Return only the complete Markdown content for {target}.
- No markdown code fences unless you are describing a command in prose.
- Keep output under 700 words.
- Do not claim Codex repaired raw project files.
- Do not include secrets, private keys, IP addresses, or credentials.
- Be honest about failures and uncertainty.
"""


def call_model(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1, "top_p": 0.8, "num_predict": 560, "num_ctx": 3072},
    }
    req = urllib.request.Request(API_URL, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
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
    return {"started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "model": MODEL, "turns": []}


def main():
    progress = load_progress()
    seen = {item["turn"] for item in progress.get("turns", [])}
    for turn, title, target, instruction in TURNS:
        if turn in seen:
            continue
        run_dir = RUNS / f"turn-{turn:02d}"
        run_dir.mkdir(parents=True, exist_ok=True)
        prompt = build_prompt(turn, title, target, instruction)
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
        (run_dir / "changed-files.txt").write_text("\n".join(changed) + ("\n" if changed else ""), encoding="utf-8")
        (run_dir / "elapsed.txt").write_text(f"{elapsed:.2f}s\n", encoding="utf-8")
        (run_dir / "validation.txt").write_text(validation_summary() + "\n", encoding="utf-8")
        progress.setdefault("turns", []).append({
            "turn": turn,
            "title": title,
            "status": status,
            "elapsed_seconds": round(elapsed, 2),
            "changed_files": changed,
            "error": bool(error_text),
            "controller": "turns-19-24-direct-markdown",
        })
        progress["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        (ROOT / "progress.json").write_text(json.dumps(progress, indent=2), encoding="utf-8")
        print(f"TURN {turn:02d} {status} elapsed={elapsed:.2f}s files={','.join(changed) if changed else '-'}", flush=True)
    print("TURNS_19_24_DONE", flush=True)


if __name__ == "__main__":
    main()
