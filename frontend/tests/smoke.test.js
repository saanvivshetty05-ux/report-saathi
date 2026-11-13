const test = require("node:test");
const assert = require("node:assert");
const fs = require("node:fs");
const path = require("node:path");

test("Frontend Smoke Test: index.html has required verification markup", () => {
  const htmlPath = path.join(__dirname, "../public/index.html");
  assert.ok(fs.existsSync(htmlPath), "index.html must exist");

  const html = fs.readFileSync(htmlPath, "utf-8");
  
  // Verify required DOM element IDs for health and database value display
  assert.ok(html.includes('id="status-badge"'), "Must contain #status-badge");
  assert.ok(html.includes('id="db-value"'), "Must contain #db-value to display database value");
  assert.ok(html.includes('id="health-check-btn"'), "Must contain #health-check-btn");
  assert.ok(html.includes("Statutory Disclaimer"), "Must contain mandatory statutory disclaimer");
});

test("Frontend Smoke Test: style.css satisfies touch target & contrast standards", () => {
  const cssPath = path.join(__dirname, "../public/style.css");
  assert.ok(fs.existsSync(cssPath), "style.css must exist");

  const css = fs.readFileSync(cssPath, "utf-8");
  
  // Verify 56dp minimum touch target height per docs/04-design.md
  assert.ok(css.includes("56px"), "CSS must enforce 56px touch target height");
  assert.ok(css.includes("--color-primary-navy: #0F294A;"), "Must use WCAG AAA Deep Navy palette");
});

test("Frontend Smoke Test: app.js contains API health fetch binding", () => {
  const jsPath = path.join(__dirname, "../public/app.js");
  assert.ok(fs.existsSync(jsPath), "app.js must exist");

  const js = fs.readFileSync(jsPath, "utf-8");
  
  assert.ok(js.includes("/api/health"), "Must call /api/health endpoint");
  assert.ok(js.includes("data.database_value"), "Must read and bind database_value from response");
});
