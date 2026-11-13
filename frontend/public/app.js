/**
 * ReportSaathi Walking Skeleton Frontend Controller
 * Connects to GET /api/health and binds database status
 */

const API_BASE = window.API_BASE_URL || "";

async function checkHealth() {
  const statusBadge = document.getElementById("status-badge");
  const dbValueEl = document.getElementById("db-value");
  const timestampEl = document.getElementById("timestamp-value");
  const versionEl = document.getElementById("version-value");
  const checkBtn = document.getElementById("health-check-btn");

  if (!statusBadge || !dbValueEl) return;

  statusBadge.className = "status-badge status-connecting";
  statusBadge.textContent = "Connecting to Backend & Database...";
  checkBtn.disabled = true;

  try {
    const response = await fetch(`${API_BASE}/api/health`, {
      method: "GET",
      headers: {
        "Accept": "application/json"
      }
    });

    if (!response.ok) {
      throw new Error(`Server returned HTTP ${response.status}`);
    }

    const data = await response.json();

    statusBadge.className = "status-badge status-healthy";
    statusBadge.textContent = `Status: ${data.status.toUpperCase()} (DB: ${data.database_status})`;
    
    // Bind value read from database
    dbValueEl.textContent = data.database_value || "No value returned";
    
    if (timestampEl) {
      timestampEl.textContent = new Date(data.timestamp).toLocaleString();
    }
    if (versionEl) {
      versionEl.textContent = `v${data.version}`;
    }
  } catch (error) {
    statusBadge.className = "status-badge status-error";
    statusBadge.textContent = "Connection Error";
    dbValueEl.textContent = `Failed to read database: ${error.message}`;
  } finally {
    checkBtn.disabled = false;
  }
}

// Auto-run on page load
document.addEventListener("DOMContentLoaded", () => {
  const checkBtn = document.getElementById("health-check-btn");
  if (checkBtn) {
    checkBtn.addEventListener("click", checkHealth);
  }
  checkHealth();
});
