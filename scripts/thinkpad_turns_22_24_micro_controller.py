from pathlib import Path
import json
import time
import traceback
import urllib.request

ROOT = Path.home() / "thinkpad24turns-test"
PROJECT = ROOT / "thinkpad-build-observatory"
RUNS = ROOT / "runs"
MODEL = "qwen2.5-coder:3b"
API_URL = "http://127.0.0.1:11434/api/generate"

TURNS = [
    (22, "Validator run summary", "docs/turn-22-validator-run-summary.md", "Summarize current validation evidence in under 350 words. Include: app.js passes syntax, JSON parses, Qwen validator script is broken raw output, Codex has not repaired files."),
    (23, "Final handoff to Codex", "docs/handoff-to-codex.md", "Write a handoff in under 350 words. Include: preserve raw output, inspect app/data/docs, create codex-fix later if needed, do not hide failed Qwen turns."),
    (24, "Qwen retrospective", "docs/qwen-retrospective.md", "Write a retrospective in under 350 words. Include: direct-file prompts worked best, large context timed out, code may include fences, future controllers should stay tiny."),
]


def prompt_for(turn, title, target, instruction):
    return f"""ThinkPad Qwen turn {turn}/24.
Target: {target}
Task: {instruction}
Return only Markdown for the target file. No code fences. No secrets. Be concise."""


def call_model(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1, "top_p": 0.8, "num_predict": 260, "num_ctx": 2048},
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
        (run_dir / "validation.txt").write_text("micro-controller: validation deferred to Codex copyback\n", encoding="utf-8")
        progress.setdefault("turns", []).append({
            "turn": turn,
            "title": title,
            "status": status,
            "elapsed_seconds": round(elapsed, 2),
            "changed_files": changed,
            "error": bool(error_text),
            "controller": "turns-22-24-micro-markdown",
        })
        progress["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        (ROOT / "progress.json").write_text(json.dumps(progress, indent=2), encoding="utf-8")
        print(f"TURN {turn:02d} {status} elapsed={elapsed:.2f}s files={','.join(changed) if changed else '-'}", flush=True)
    print("TURNS_22_24_MICRO_DONE", flush=True)


if __name__ == "__main__":
    main()
