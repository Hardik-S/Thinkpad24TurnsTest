const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const root = path.resolve(__dirname, "..");
const requiredFiles = [
  "README.md",
  "index.html",
  "styles.css",
  "app.js",
  "data/runs.json",
  "data/hardware.json",
];

const sourceExtensions = new Set([".html", ".css", ".js", ".json", ".md"]);
const failures = [];

function check(condition, message) {
  if (condition) {
    console.log(`PASS ${message}`);
  } else {
    console.error(`FAIL ${message}`);
    failures.push(message);
  }
}

function walk(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const target = path.join(dir, entry.name);
    return entry.isDirectory() ? walk(target) : [target];
  });
}

for (const file of requiredFiles) {
  check(fs.existsSync(path.join(root, file)), `${file} exists`);
}

for (const file of ["data/runs.json", "data/hardware.json"]) {
  try {
    JSON.parse(fs.readFileSync(path.join(root, file), "utf8"));
    check(true, `${file} parses`);
  } catch (error) {
    check(false, `${file} parses: ${error.message}`);
  }
}

const appCheck = spawnSync(process.execPath, ["--check", path.join(root, "app.js")], {
  encoding: "utf8",
});
check(appCheck.status === 0, "app.js passes node --check");
if (appCheck.stderr) {
  process.stderr.write(appCheck.stderr);
}

for (const file of walk(root)) {
  if (!sourceExtensions.has(path.extname(file))) {
    continue;
  }
  const relative = path.relative(root, file);
  const text = fs.readFileSync(file, "utf8");
  check(!/(https?:\/\/(?!127\.0\.0\.1|localhost)|cdn\.)/i.test(text), `${relative} has no external URL/CDN reference`);
}

if (failures.length) {
  console.error(`\n${failures.length} validation failure(s).`);
  process.exit(1);
}

console.log("\nStatic site validation passed.");
