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

SYSTEM = """You are Qwen running locally on a ThinkPad e530. Build only the requested part of a static portfolio project called ThinkPad Build Observatory. Use no package manager, no framework, no external assets, no CDN, and no network calls. Keep changes small. Prefer plain HTML, CSS, JavaScript, JSON, and Markdown. Preserve existing files unless the current instruction explicitly says to edit them. Return JSON only, with this exact shape: {"files":[{"path":"relative/path","content":"full file content"}],"notes":"short risk summary"}. Do not wrap the JSON in markdown fences."""

TURNS = [
    (1, "Project brief and manifest", "Create the project brief, directory structure, and file manifest for thinkpad-build-observatory. Write README.md, docs/qwen-build-log.md, and docs/file-manifest.md. Do not create app code yet."),
    (2, "Data schema", "Define the run evidence data schema. Create docs/data-schema.md describing data/runs.json and data/hardware.json. Create small valid seed JSON files with enough fields for later rendering."),
    (3, "HTML skeleton", "Create index.html with semantic regions for hero, run timeline, artifact gallery, validation status, hardware profile, and footer. Link styles.css and app.js, but keep JavaScript behavior minimal for now."),
    (4, "Base styles", "Create styles.css with a restrained portfolio visual identity for a technical artifact: readable, responsive, not marketing-heavy, and not a single-color palette. Support mobile and desktop without horizontal scrolling."),
    (5, "Render shell", "Create app.js with a boot function that loads data/runs.json and data/hardware.json, handles fetch errors, and renders simple placeholder content into existing HTML regions."),
    (6, "Run timeline", "Extend app.js to render a run timeline from data/runs.json. Include turn number, title, status, elapsed time, changed files, and a short note."),
    (7, "Artifact gallery", "Extend app.js and seed data to render an artifact gallery. Each artifact should show file path, purpose, producing turn, and whether it is raw Qwen output or later Codex repair."),
    (8, "Validation panel", "Extend app.js and seed data to render a validation/status panel. Include pass, warn, fail, and not-run states. Make the UI honest about missing validation."),
    (9, "Hardware profile", "Add a model and hardware profile panel using data/hardware.json. Include ThinkPad model, CPU-only constraint, local model name, run budget, and the reason direct Ollama HTTP is used."),
    (10, "Build story copy", "Tighten visible build-story copy in index.html and README. The site should clearly say it was built on a 2012 ThinkPad by a local 3B coding model over 24 supervised turns."),
    (11, "Seed first-loop data", "Expand data/runs.json and data/hardware.json with realistic first-loop placeholder records for turns 1-12. Mark future turns honestly as planned or not-run."),
    (12, "Checkpoint handoff", "Draft the run-12 checkpoint handoff in docs/handoff-to-codex.md. Update docs/qwen-build-log.md with a first-loop summary and list risks for turns 13-24. Do not claim final completion."),
]


def project_tree():
    lines = []
    for path in sorted(PROJECT.rglob("*")):
        if path.is_file():
            rel = path.relative_to(PROJECT).as_posix()
            lines.append(f"- {rel} ({path.stat().st_size} bytes)")
    return "\n".join(lines) or "No files yet."


def read_relevant():
    names = [
        "README.md",
        "index.html",
        "styles.css",
        "app.js",
        "data/runs.json",
        "data/hardware.json",
        "docs/qwen-build-log.md",
        "docs/file-manifest.md",
        "docs/data-schema.md",
        "docs/handoff-to-codex.md",
    ]
    chunks = []
    total = 0
    for name in names:
        path = PROJECT / name
        if not path.exists() or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if len(text) > 4500:
            text = text[:4500] + "\n[truncated]"
        block = f"\n--- {name} ---\n{text}\n"
        if total + len(block) > 18000:
            break
        chunks.append(block)
        total += len(block)
    return "".join(chunks) or "No existing relevant file content."


def call_model(turn, title, instruction):
    prompt = f"""{SYSTEM}

Turn {turn:02d}: {title}
Instruction: {instruction}

Current project tree:
{project_tree()}

Current relevant file contents:
{read_relevant()}

Return JSON only. Include full content for every file you create or modify. Keep each file concise enough to fit this response."""
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2, "top_p": 0.9, "num_predict": 1000, "num_ctx": 8192},
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
    return target


def validate():
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
            if out.stdout.strip():
                lines.append(out.stdout.strip())
            if out.stderr.strip():
                lines.append(out.stderr.strip())
        except Exception as exc:
            lines.append(f"WARN node check unavailable: {exc}")
    external_hits = []
    for path in PROJECT.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".html", ".css", ".js", ".json", ".md"}:
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "http://" in text or "https://" in text or "cdn." in text:
                external_hits.append(path.relative_to(PROJECT).as_posix())
    lines.append(("PASS" if not external_hits else "WARN") + " no external URL scan" + ("" if not external_hits else ": " + ", ".join(external_hits)))
    return "\n".join(lines) + "\n"


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    PROJECT.mkdir(parents=True, exist_ok=True)
    RUNS.mkdir(parents=True, exist_ok=True)
    progress = {"started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "model": MODEL, "turns": []}
    (ROOT / "progress.json").write_text(json.dumps(progress, indent=2), encoding="utf-8")

    for turn, title, instruction in TURNS:
        run_dir = RUNS / f"turn-{turn:02d}"
        run_dir.mkdir(parents=True, exist_ok=True)
        changed = []
        status = "started"
        err = None
        elapsed = 0.0
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
        validation = validate()
        (run_dir / "validation.txt").write_text(validation, encoding="utf-8")
        progress["turns"].append({
            "turn": turn,
            "title": title,
            "status": status,
            "elapsed_seconds": round(elapsed, 2),
            "changed_files": changed,
            "error": bool(err),
        })
        progress["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        (ROOT / "progress.json").write_text(json.dumps(progress, indent=2), encoding="utf-8")
        print(f"TURN {turn:02d} {status} elapsed={elapsed:.2f}s files={','.join(changed) if changed else '-'}", flush=True)

    print("LOOP1_DONE", flush=True)


if __name__ == "__main__":
    main()
