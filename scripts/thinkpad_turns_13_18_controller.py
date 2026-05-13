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
    (13, "Responsive polish notes", "docs/turn-13-responsive-polish.md", "Write a concise responsive-design review of the current static site. Include CSS/mobile risks and two small later repair suggestions. Do not claim to edit CSS."),
    (14, "Accessibility pass notes", "docs/turn-14-accessibility-pass.md", "Write a concise accessibility review. Cover headings, landmarks, keyboard navigation, contrast, reduced motion, and screen-reader risks."),
    (15, "Empty and error state notes", "docs/turn-15-empty-error-states.md", "Write a concise empty/error-state review. Cover JSON fetch failure, no runs, and missing validation entries."),
    (16, "No-external cleanup notes", "docs/turn-16-no-external-cleanup.md", "Write a concise no-external-dependency audit. Confirm browser-native only, no CDN, no external images, no API calls, no package installs."),
    (17, "Static validator script", "scripts/validate-static-site.js", "Write only a compact Node CommonJS script. It should check required files, parse data/runs.json and data/hardware.json, run node --check app.js, and scan .html/.css/.js/.json/.md files for http://, https://, or cdn. Keep it under 120 lines."),
    (18, "Validator repair notes", "docs/turn-18-validator-repair-notes.md", "Write concise validation and repair-priority notes. Separate what Qwen should still attempt in turns 19-24 from what Codex should save for the final codex-fix phase."),
]


def file_list():
    files = []
    for path in sorted(PROJECT.rglob("*")):
        if path.is_file():
            files.append(path.relative_to(PROJECT).as_posix())
    return "\n".join(files[:80])


def short_validation():
    lines = []
    required = ["README.md", "index.html", "styles.css", "app.js", "data/runs.json", "data/hardware.json"]
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
            out = subprocess.run(["node", "--check", str(app)], text=True, capture_output=True, timeout=20)
            lines.append(("PASS" if out.returncode == 0 else "FAIL") + " node --check app.js")
            if out.stderr.strip():
                lines.append(out.stderr.strip()[:500])
        except Exception as exc:
            lines.append(f"WARN node check unavailable: {exc}")
    return "\n".join(lines)


def prompt_for(turn, title, target, instruction):
    if target.endswith(".js"):
        output_rule = f"Return only the complete JavaScript source for {target}. No markdown fences, no explanation."
    else:
        output_rule = f"Return only the complete Markdown content for {target}. No markdown fences."
    return f"""You are Qwen running locally on a ThinkPad e530.
This is turn {turn} of 24 in the ThinkPad Build Observatory experiment.
Target file: {target}

Instruction: {instruction}

Known files:
{file_list()}

Current validation summary:
{short_validation()}

Rules:
- {output_rule}
- Keep output under 700 words or under 120 JavaScript lines.
- Do not claim Codex repaired anything.
- Do not include secrets, private keys, IP addresses, or credentials.
- Do not use external dependencies.
"""


def call_model(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1, "top_p": 0.8, "num_predict": 520, "num_ctx": 3072},
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
        (run_dir / "changed-files.txt").write_text("\n".join(changed) + ("\n" if changed else ""), encoding="utf-8")
        (run_dir / "elapsed.txt").write_text(f"{elapsed:.2f}s\n", encoding="utf-8")
        (run_dir / "validation.txt").write_text(short_validation() + "\n", encoding="utf-8")
        progress.setdefault("turns", []).append({
            "turn": turn,
            "title": title,
            "status": status,
            "elapsed_seconds": round(elapsed, 2),
            "changed_files": changed,
            "error": bool(error_text),
            "controller": "turns-13-18-direct-file",
        })
        progress["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        (ROOT / "progress.json").write_text(json.dumps(progress, indent=2), encoding="utf-8")
        print(f"TURN {turn:02d} {status} elapsed={elapsed:.2f}s files={','.join(changed) if changed else '-'}", flush=True)
    print("TURNS_13_18_DONE", flush=True)


if __name__ == "__main__":
    main()
