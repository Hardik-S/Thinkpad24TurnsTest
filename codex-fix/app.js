const runDataUrl = "data/runs.json";
const hardwareDataUrl = "data/hardware.json";

const statusClass = (status) => (status === "completed" ? "pass" : "fail");

async function loadJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Unable to load ${url}: ${response.status}`);
  }
  return response.json();
}

function renderSummary(runs) {
  const total = runs.length;
  const completed = runs.filter((run) => run.status === "completed").length;
  const failed = total - completed;
  const qwenSeconds = runs.reduce((sum, run) => sum + Number(run.elapsed_seconds || 0), 0);
  const cards = [
    ["Turns attempted", total],
    ["Completed", completed],
    ["Timed out", failed],
    ["Qwen runtime", `${Math.round(qwenSeconds / 60)} min`],
  ];
  document.querySelector("#summary").innerHTML = cards.map(([label, value]) => `
    <article class="summary-card">
      <span class="metric">${value}</span>
      <span class="label">${label}</span>
    </article>
  `).join("");
}

function renderTimeline(runs) {
  document.querySelector("#timeline").innerHTML = runs.map((run) => `
    <article class="turn-card ${statusClass(run.status)}">
      <span class="status ${statusClass(run.status)}">${run.status}</span>
      <h3>Turn ${run.turn}: ${run.title}</h3>
      <p class="meta">${run.controller || "initial controller"} | ${run.elapsed_seconds}s</p>
      ${run.changed_files.length ? `
        <ul class="file-list">
          ${run.changed_files.map((file) => `<li>${file}</li>`).join("")}
        </ul>
      ` : `<p class="meta">No files written. Failure preserved as raw evidence.</p>`}
    </article>
  `).join("");
}

function renderValidation() {
  const validations = [
    ["Core app syntax", "pass", "Codex verified node --check app.js passes in the final raw snapshot."],
    ["Run data", "pass", "data/runs.json and data/hardware.json parse as JSON in codex-fix."],
    ["Qwen validator", "fail", "Raw Qwen wrapped scripts/validate-static-site.js in Markdown fences."],
    ["Repair boundary", "warn", "Raw output remains in state/. This directory is the repaired Codex copy."],
  ];
  document.querySelector("#validation").innerHTML = validations.map(([title, state, text]) => `
    <article class="validation-card">
      <span class="status ${state}">${state}</span>
      <h3>${title}</h3>
      <p>${text}</p>
    </article>
  `).join("");
}

function renderArtifacts() {
  const artifacts = [
    ["state/turns-19-24/", "Raw final ThinkPad output and all per-turn evidence."],
    ["codex-fix/", "Repaired static site copy created after the 24-turn Qwen boundary."],
    ["docs/TURNS_19_24_FINDINGS.md", "Final slice findings and controller lessons."],
    ["docs/FINAL_PHASE_REPORT.md", "Codex-owned repair, report, memory, and skill handoff."],
  ];
  document.querySelector("#artifacts").innerHTML = artifacts.map(([path, purpose]) => `
    <article class="artifact-card">
      <h3>${path}</h3>
      <p>${purpose}</p>
    </article>
  `).join("");
}

function renderHardware(profile) {
  document.querySelector("#hardware").innerHTML = `
    <article>
      <h3>${profile.machine}</h3>
      <p>${profile.role}</p>
    </article>
    <article>
      <h3>${profile.model}</h3>
      <p>${profile.route}</p>
    </article>
    ${profile.specs.map((item) => `
      <article>
        <h3>${item.label}</h3>
        <p>${item.value}</p>
      </article>
    `).join("")}
  `;
}

function renderError(error) {
  document.querySelector("#timeline").innerHTML = `
    <article class="turn-card fail">
      <span class="status fail">error</span>
      <h3>Unable to render Observatory data</h3>
      <p>${error.message}</p>
    </article>
  `;
}

async function boot() {
  try {
    const [runs, hardware] = await Promise.all([
      loadJson(runDataUrl),
      loadJson(hardwareDataUrl),
    ]);
    renderSummary(runs);
    renderTimeline(runs);
    renderValidation();
    renderArtifacts();
    renderHardware(hardware);
  } catch (error) {
    renderError(error);
  }
}

document.addEventListener("DOMContentLoaded", boot);
