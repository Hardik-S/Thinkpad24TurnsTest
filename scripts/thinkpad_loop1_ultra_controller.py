from pathlib import Path
import subprocess
import time
import traceback
import urllib.request
import json

ROOT = Path.home() / "thinkpad24turns-test"
PROJECT = ROOT / "thinkpad-build-observatory"
RUNS = ROOT / "runs"
MODEL = "qwen2.5-coder:3b"
API_URL = "http://127.0.0.1:11434/api/generate"

TURNS = [
    (11, "First-loop evidence doc", "docs/validation-report.md", "Write a concise Markdown validation report for the first 12-turn checkpoint. Mention that turns 3, 5, 8, and 10 timed out. State that Codex has not repaired generated project files. Include current known files and risks for turns 13-24."),
    (12, "Checkpoint handoff", "docs/handoff-to-codex.md", "Write a concise Markdown handoff to Codex for the run-12 checkpoint. Include what exists, what failed, what must not be repaired until turn 24, and recommended prompt changes for turns 13-24."),
]


def context():
    files = []
    for path in sorted(PROJECT.rglob("*")):
        if path.is_file():
            files.append(path.relative_to(PROJECT).as_posix())
    progress = ROOT / "progress.json"
    progress_text = progress.read_text(encoding="utf-8") if progress.exists() else "{}"
    return "Files:\n" + "\n".join(files) + "\n\nProgress:\n" + progress_text[:4500]


def call_model(turn, title, target, instruction):
    prompt = f"""You are Qwen running locally on a ThinkPad e530.
Write only the complete Markdown content for {target}. Do not use JSON. Do not use code fences. Keep it under 900 words.

Turn {turn:02d}: {title}
Instruction: {instruction}

Context:
{context()}
"""
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.15, "top_p": 0.85, "num_predict": 450, "num_ctx": 4096},
    }
    req = urllib.request.Request(API_URL, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    start = time.time()
    with urllib.request.urlopen(req, timeout=300) as resp:
        raw = resp.read()
    elapsed = time.time() - start
    data = json.loads(raw.decode("utf-8"))
    return prompt, data.get("response", "").strip() + "\n", elapsed


def validate():
    lines = []
    for rel in ["README.md", "index.html", "styles.css", "app.js", "data/runs.json", "data/hardware.json"]:
        lines.append(("PASS" if (PROJECT / rel).exists() else "MISSING") + f" {rel}")
    for rel in ["data/runs.json", "data/hardware.json"]:
        path = PROJECT / rel
        if path.exists():
            try:
                json.loads(path.read_text(encoding="utf-8"))
                lines.append(f"PASS json {rel}")
            except Exception as exc:
                lines.append(f"FAIL json {rel}: {exc}")
    if (PROJECT / "app.js").exists():
        out = subprocess.run(["node", "--check", str(PROJECT / "app.js")], text=True, capture_output=True, timeout=20)
        lines.append(("PASS" if out.returncode == 0 else "FAIL") + " node --check app.js")
        if out.stderr.strip():
            lines.append(out.stderr.strip())
    return "\n".join(lines) + "\n"


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
        changed = []
        elapsed = 0.0
        err = None
        try:
            prompt, content, elapsed = call_model(turn, title, target, instruction)
            (run_dir / "prompt.md").write_text(prompt, encoding="utf-8")
            (run_dir / "response.txt").write_text(content, encoding="utf-8")
            output = PROJECT / target
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(content, encoding="utf-8", newline="\n")
            changed.append(target)
            status = "completed"
        except Exception:
            status = "failed"
            err = traceback.format_exc()
            (run_dir / "error.txt").write_text(err, encoding="utf-8")
        (run_dir / "changed-files.txt").write_text("\n".join(changed) + ("\n" if changed else ""), encoding="utf-8")
        (run_dir / "elapsed.txt").write_text(f"{elapsed:.2f}s\n", encoding="utf-8")
        (run_dir / "validation.txt").write_text(validate(), encoding="utf-8")
        progress.setdefault("turns", []).append({
            "turn": turn,
            "title": title,
            "status": status,
            "elapsed_seconds": round(elapsed, 2),
            "changed_files": changed,
            "error": bool(err),
            "controller": "ultra-single-file",
        })
        progress["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        (ROOT / "progress.json").write_text(json.dumps(progress, indent=2), encoding="utf-8")
        print(f"TURN {turn:02d} {status} elapsed={elapsed:.2f}s files={','.join(changed) if changed else '-'}", flush=True)
    print("ULTRA_LOOP1_DONE", flush=True)


if __name__ == "__main__":
    main()
