from pathlib import Path
import json
import re
import subprocess
import time
import traceback
import urllib.request

ROOT = Path.home() / "thinkpad24turns-test"
PROJECT = ROOT / "thinkpad-build-observatory"
RUNS = ROOT / "runs"
MODEL = "qwen2.5-coder:3b"
API_URL = "http://127.0.0.1:11434/api/generate"

SYSTEM = """You are Qwen on a ThinkPad e530. Continue a static site called ThinkPad Build Observatory. Use only plain HTML, CSS, JS, JSON, and Markdown. Return JSON only: {"files":[{"path":"relative/path","content":"full file content"}],"notes":"short note"}. Keep output short. No markdown fences. No external links, CDNs, package managers, or network calls."""

TURNS = [
    (6, "Recovery HTML skeleton", "Create a compact index.html because the earlier HTML turn timed out. Include linked styles.css and app.js, and sections with ids: hero, timeline, artifacts, validation, hardware, footer."),
    (7, "Compact app shell", "Create a compact app.js. On DOMContentLoaded, fetch data/runs.json and data/hardware.json, then render simple timeline, artifacts, validation, and hardware summaries into the existing section ids. Include error text if fetch fails."),
    (8, "Validation data pass", "Update data/runs.json so it has turns 1-12, including completed, failed, and planned states from the experiment so far. Include artifact and validation arrays that app.js can render."),
    (9, "Hardware profile pass", "Update data/hardware.json with concise ThinkPad e530 hardware, qwen2.5-coder:3b model, CPU-only constraint, 24-turn budget, and direct Ollama HTTP route."),
    (10, "Build story copy pass", "Update README.md and index.html copy so the visible story says this was built on a 2012 ThinkPad by local qwen2.5-coder:3b over 24 supervised turns. Keep both files concise."),
    (11, "First-loop evidence doc", "Create docs/validation-report.md summarizing the first-loop validation state honestly. Mention that turns 3 and 5 timed out and that Codex has not repaired the generated project."),
    (12, "Checkpoint handoff", "Create docs/handoff-to-codex.md and update docs/qwen-build-log.md with a run-12 checkpoint summary, risks for turns 13-24, and the no-Codex-repair boundary."),
]


def current_file_list():
    files = []
    for path in sorted(PROJECT.rglob("*")):
        if path.is_file():
            files.append(path.relative_to(PROJECT).as_posix())
    return ", ".join(files) or "none"


def small_context():
    pieces = [f"Existing files: {current_file_list()}"]
    for rel in ["data/runs.json", "data/hardware.json", "index.html", "app.js", "README.md"]:
        path = PROJECT / rel
        if path.exists():
            text = path.read_text(encoding="utf-8", errors="replace")
            pieces.append(f"\n{rel} first 1400 chars:\n{text[:1400]}")
    return "\n".join(pieces)[:7000]


def call_model(turn, title, instruction):
    prompt = f"""{SYSTEM}

Turn {turn:02d}: {title}
Instruction: {instruction}

Context:
{small_context()}

Return JSON only. Keep the total response short enough to finish within five minutes."""
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.15, "top_p": 0.85, "num_predict": 650, "num_ctx": 4096},
    }
    req = urllib.request.Request(API_URL, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    start = time.time()
    with urllib.request.urlopen(req, timeout=300) as resp:
        raw = resp.read()
    elapsed = time.time() - start
    data = json.loads(raw.decode("utf-8"))
    return prompt, data.get("response", ""), elapsed


def parse_response(text):
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    first = cleaned.find("{")
    last = cleaned.rfind("}")
    if first >= 0 and last > first:
        cleaned = cleaned[first:last + 1]
    return json.loads(cleaned)


def safe_write(rel, content):
    rel_path = Path(rel)
    if rel_path.is_absolute() or ".." in rel_path.parts:
        raise ValueError(f"unsafe path: {rel}")
    target = (PROJECT / rel_path).resolve()
    if PROJECT.resolve() not in target.parents and target != PROJECT.resolve():
        raise ValueError(f"outside project: {rel}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8", newline="\n")


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
    app = PROJECT / "app.js"
    if app.exists():
        out = subprocess.run(["node", "--check", str(app)], text=True, capture_output=True, timeout=20)
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
    completed_turns = {item["turn"] for item in progress.get("turns", [])}
    for turn, title, instruction in TURNS:
        if turn in completed_turns:
            continue
        run_dir = RUNS / f"turn-{turn:02d}"
        run_dir.mkdir(parents=True, exist_ok=True)
        changed = []
        elapsed = 0.0
        err = None
        try:
            prompt, response, elapsed = call_model(turn, title, instruction)
            (run_dir / "prompt.md").write_text(prompt, encoding="utf-8")
            (run_dir / "response.txt").write_text(response, encoding="utf-8")
            parsed = parse_response(response)
            for item in parsed.get("files", []):
                safe_write(item["path"], item.get("content", ""))
                changed.append(item["path"])
            status = "completed" if changed else "no-files"
            (run_dir / "notes.txt").write_text(str(parsed.get("notes", "")), encoding="utf-8")
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
            "controller": "narrow",
        })
        progress["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        (ROOT / "progress.json").write_text(json.dumps(progress, indent=2), encoding="utf-8")
        print(f"TURN {turn:02d} {status} elapsed={elapsed:.2f}s files={','.join(changed) if changed else '-'}", flush=True)
    print("NARROW_LOOP1_DONE", flush=True)


if __name__ == "__main__":
    main()
