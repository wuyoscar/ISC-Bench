// ISC-Bench — JailbreakArena Website
// Auto-fetches data from GitHub repo for real-time updates

const REPO_RAW = "https://raw.githubusercontent.com/wuyoscar/ISC-Bench/main";

// ====== Fallback data (used if fetch fails) ======
const FALLBACK_CASES = {
  "Claude Opus 4.6": { demos: [{ link: "https://claude.ai/share/407d33f5-4655-4479-b3e3-0a6dc6639d34", by: "wuyoscar" }] },
  "Claude Opus 4.5": { demos: [{ link: "https://claude.ai/share/1e3e997c-0315-46f1-9cbd-37157314a7ef", by: "wuyoscar" }] },
  "Claude Sonnet 4.6": { demos: [{ link: "https://claude.ai/share/cc972f9b-a558-4bca-8bc6-0e6d65590793", by: "wuyoscar" }] },
  "Gemini 3 Pro": { demos: [{ link: "https://gemini.google.com/share/320bf34b0334", by: "wuyoscar" }] },
  "GPT-5.2 Chat": { demos: [{ link: "https://chatgpt.com/share/69a3f6e1-24d8-800c-9581-3d1a7180ee55", by: "wuyoscar" }] },
  "o3": { demos: [{ link: "https://chatgpt.com/share/69c3b0a7-3554-839a-95a5-d22d60758dc9", by: "wuyoscar" }] },
  "Grok 4.1": { demos: [{ link: "https://grok.com/share/c2hhcmQtMi1jb3B5_54de710c-9331-4fca-a953-6c35775156fb", by: "wuyoscar" }] },
  "Kimi K2.5 Thinking": { demos: [{ link: "https://www.kimi.com/share/19ca8616-9e32-810d-8000-0000647caebf", by: "wuyoscar" }] },
  "Qwen 3 Max Preview": { demos: [{ link: "https://chat.qwen.ai/s/f1e5d846-018e-4a3d-94ff-418e34559497?fev=0.2.9", by: "wuyoscar" }] },
  "DeepSeek V3.2": { demos: [{ link: "https://chat.deepseek.com/share/pbzirkyhfkvapyc3g0", by: "wuyoscar" }] },
  "GLM-5": { demos: [{ link: "https://chat.z.ai/s/79e38d45-d370-4c03-8fb2-6ff3427046cc", by: "wuyoscar" }] },
  "Qwen 3.5 397B": { demos: [{ link: "https://chat.qwen.ai/s/f4faf33a-a6b3-4503-8c9b-6d57ee39c0c6?fev=0.2.16", by: "HanxunH" }] },
  "Qwen 3 Max 2025-09-23": { demos: [{ link: "https://chat.qwen.ai/s/c4247247-ddfd-43f1-bae6-1f703b29de27?fev=0.2.16", by: "HanxunH" }] },
  "ERNIE 5.0": { demos: [{ link: "https://ernie.baidu.com/share/TlRKBSn5kT", by: "HanxunH" }] },
};

// ====== Dynamic Data Fetch ======
async function fetchJSON(path) {
  try {
    const resp = await fetch(`${REPO_RAW}/${path}?t=${Date.now()}`);
    if (!resp.ok) throw new Error(resp.status);
    return await resp.json();
  } catch (e) {
    console.warn(`Failed to fetch ${path}, using fallback:`, e);
    return null;
  }
}

async function loadData() {
  const [arenaData, iscData] = await Promise.all([
    fetchJSON("assets/arena_cache.json"),
    fetchJSON("assets/isc_cases.json"),
  ]);

  const arena = arenaData || [];
  const cases = iscData || FALLBACK_CASES;

  window._allModels = arena;
  window._allCases = cases;
  window._currentPage = 1;
  window._perPage = 25;
  renderPage(1, arena, cases);
  populateDemos(cases);
  updateStats(arena, cases);
}

// ====== Pagination ======
function renderPage(page, models, cases) {
  const perPage = window._perPage;
  const start = (page - 1) * perPage;
  const end = start + perPage;
  const pageModels = models.slice(start, end);
  window._currentPage = page;
  populateLeaderboard(pageModels, cases);
  renderPagination(models.length, perPage, page);
}

function renderPagination(total, perPage, current) {
  const totalPages = Math.ceil(total / perPage);
  let container = document.getElementById("pagination-nav");
  if (!container) {
    container = document.createElement("nav");
    container.id = "pagination-nav";
    container.className = "pagination is-centered is-small mt-4";
    container.setAttribute("role", "navigation");
    const tableContainer = document.querySelector(".table-container");
    if (tableContainer) tableContainer.parentNode.insertBefore(container, tableContainer.nextSibling);
  }

  let html = '<ul class="pagination-list">';

  // Previous
  if (current > 1) {
    html += `<li><a class="pagination-link" onclick="renderPage(${current-1}, window._allModels, window._allCases)">&laquo;</a></li>`;
  }

  // Page numbers
  for (let i = 1; i <= totalPages; i++) {
    if (i === 1 || i === totalPages || (i >= current - 2 && i <= current + 2)) {
      html += `<li><a class="pagination-link ${i === current ? 'is-current' : ''}" onclick="renderPage(${i}, window._allModels, window._allCases)">${i}</a></li>`;
    } else if (i === current - 3 || i === current + 3) {
      html += '<li><span class="pagination-ellipsis">&hellip;</span></li>';
    }
  }

  // Next
  if (current < totalPages) {
    html += `<li><a class="pagination-link" onclick="renderPage(${current+1}, window._allModels, window._allCases)">&raquo;</a></li>`;
  }

  html += '</ul>';
  container.innerHTML = html;
}

// ====== Leaderboard ======
function populateLeaderboard(models, cases) {
  const tbody = document.getElementById("leaderboard-body");
  if (!tbody) return;
  tbody.innerHTML = "";

  models.forEach(model => {
    const displayName = slugToDisplay(model.name);
    const isc = cases[displayName];
    const tr = document.createElement("tr");

    let statusHTML, demoHTML = "", byHTML = "";
    if (isc) {
      statusHTML = '<span class="badge-jailbroken"><i class="fas fa-unlock"></i> Jailbroken</span>';
      demoHTML = isc.demos.map((d, i) =>
        `<a href="${d.link}" target="_blank" title="View conversation">🔗${isc.demos.length > 1 ? `₊${i+1}` : ""}</a>`
      ).join(" ");
      byHTML = isc.demos.map(d =>
        `<a href="https://github.com/${d.by}" target="_blank">@${d.by}</a>`
      ).join("<br>");
    } else {
      statusHTML = '<span class="badge-safe"><i class="fas fa-hourglass-half"></i> Pending</span>';
    }

    tr.innerHTML = `
      <td class="has-text-centered"><strong>${model.rank}</strong></td>
      <td><span class="model-name">${displayName}</span><span class="model-org">${model.org}</span></td>
      <td class="has-text-centered">${model.score}</td>
      <td class="has-text-centered">${statusHTML}</td>
      <td class="has-text-centered">${demoHTML}</td>
      <td class="has-text-centered">${byHTML}</td>
    `;
    tr.dataset.name = displayName.toLowerCase();
    tr.dataset.status = isc ? "jailbroken" : "safe";
    tbody.appendChild(tr);
  });
}

// ====== Demo Cards (Marquee) ======
function populateDemos(cases) {
  const container = document.getElementById("demo-grid");
  if (!container) return;
  container.innerHTML = "";

  const favicons = {
    "claude": "anthropic.com", "gemini": "google.com", "gpt": "openai.com", "chatgpt": "openai.com",
    "grok": "x.ai", "kimi": "moonshot.ai", "qwen": "alibabacloud.com", "deepseek": "deepseek.com",
    "glm": "z.ai", "ernie": "baidu.com", "o3": "openai.com", "dola": "volcengine.com",
  };

  // Build card HTML
  function makeCard(name, data) {
    const demo = data.demos[0];
    const key = Object.keys(favicons).find(k => name.toLowerCase().includes(k)) || "";
    const domain = favicons[key] || "";
    const icon = domain
      ? `<img src="https://www.google.com/s2/favicons?domain=${domain}&sz=32" width="20" style="vertical-align:middle;border-radius:3px;">`
      : "🤖";
    return `<div class="demo-card">
      <div class="demo-icon">${icon}</div>
      <div class="demo-info"><h4>${name}</h4><p>by @${demo.by}</p></div>
      <a href="${demo.link}" target="_blank" class="demo-link">View →</a>
    </div>`;
  }

  const entries = Object.entries(cases);
  const mid = Math.ceil(entries.length / 2);
  const row1Items = entries.slice(0, mid);
  const row2Items = entries.slice(mid);

  // Create two marquee rows
  [row1Items, row2Items].forEach(items => {
    const row = document.createElement("div");
    row.className = "marquee-row";
    const inner = document.createElement("div");
    inner.className = "marquee-inner";
    // Original + duplicate for seamless loop
    const cardsHTML = items.map(([n, d]) => makeCard(n, d)).join("");
    inner.innerHTML = cardsHTML + cardsHTML;
    row.appendChild(inner);
    container.appendChild(row);
  });
}

// ====== Update Stats ======
function updateStats(arena, cases) {
  const confirmed = Object.keys(cases).length;
  const total = arena.length || 330;

  // Update stat cards if they exist
  document.querySelectorAll(".stat-num").forEach(el => {
    if (el.textContent === "56") return; // keep templates count
    if (el.textContent === "8") return;  // keep domains count
  });

  // Update arena subtitle
  const subtitle = document.querySelector("#arena .subtitle");
  if (subtitle) {
    subtitle.innerHTML = `Real-time tracking of ISC across <strong>${total}</strong> Arena-ranked models.
      Every <span class="has-text-danger">red dot</span> is a confirmed case.
      <strong class="has-text-danger">${confirmed}</strong> jailbroken so far.`;
  }
}

// ====== Search + Filter ======
function setupSearch() {
  const searchInput = document.getElementById("arenaSearch");
  const filterSelect = document.getElementById("arenaFilter");
  if (!searchInput || !filterSelect) return;

  function applyFilter() {
    const query = searchInput.value.toLowerCase();
    const filter = filterSelect.value;
    const allModels = window._allModels || [];
    const cases = window._allCases || {};

    const filtered = allModels.filter(m => {
      const name = slugToDisplay(m.name).toLowerCase();
      const isc = cases[slugToDisplay(m.name)];
      const nameMatch = name.includes(query) || m.org.toLowerCase().includes(query);
      const statusMatch = filter === "all" || (filter === "jailbroken" && isc) || (filter === "safe" && !isc);
      return nameMatch && statusMatch;
    });

    window._filteredModels = filtered;
    window._currentPage = 1;
    populateLeaderboard(filtered.slice(0, window._perPage), cases);
    renderPagination(filtered.length, window._perPage, 1);
  }

  // Override renderPage to use filtered if available
  const origRenderPage = window.renderPage;
  window.renderPage = function(page, models, cases) {
    const src = window._filteredModels || models;
    const perPage = window._perPage;
    const start = (page - 1) * perPage;
    populateLeaderboard(src.slice(start, start + perPage), cases);
    renderPagination(src.length, perPage, page);
    window._currentPage = page;
  };

  searchInput.addEventListener("input", applyFilter);
  filterSelect.addEventListener("change", applyFilter);
}

// ====== Name Conversion ======
const DISPLAY_NAMES = {
  "claude-opus-4-6-thinking": "Claude Opus 4.6 Thinking",
  "claude-opus-4-6": "Claude Opus 4.6",
  "gemini-3.1-pro-preview": "Gemini 3.1 Pro Preview",
  "grok-4.20-beta1": "Grok 4.20 Beta",
  "gemini-3-pro": "Gemini 3 Pro",
  "gpt-5.4-high": "GPT-5.4 High",
  "gpt-5.2-chat-latest-20260210": "GPT-5.2 Chat",
  "grok-4.20-beta-0309-reasoning": "Grok 4.20 Reasoning",
  "gemini-3-flash": "Gemini 3 Flash",
  "claude-opus-4-5-20251101-thinking-32k": "Claude Opus 4.5 Thinking",
  "grok-4.1-thinking": "Grok 4.1 Thinking",
  "claude-opus-4-5-20251101": "Claude Opus 4.5",
  "claude-sonnet-4-6": "Claude Sonnet 4.6",
  "qwen3.5-max-preview": "Qwen 3.5 Max Preview",
  "gpt-5.3-chat-latest": "GPT-5.3 Chat",
  "gemini-3-flash (thinking-minimal)": "Gemini 3 Flash Thinking",
  "gpt-5.4": "GPT-5.4",
  "dola-seed-2.0-preview": "Dola Seed 2.0 Preview",
  "grok-4.1": "Grok 4.1",
  "gpt-5.1-high": "GPT-5.1 High",
  "glm-5": "GLM-5",
  "kimi-k2.5-thinking": "Kimi K2.5 Thinking",
  "claude-sonnet-4-5-20250929": "Claude Sonnet 4.5",
  "claude-sonnet-4-5-20250929-thinking-32k": "Claude Sonnet 4.5 Thinking",
  "ernie-5.0-0110": "ERNIE 5.0",
  "qwen3.5-397b-a17b": "Qwen 3.5 397B",
  "ernie-5.0-preview-1203": "ERNIE 5.0 Preview",
  "claude-opus-4-1-20250805-thinking-16k": "Claude Opus 4.1 Thinking",
  "gemini-2.5-pro": "Gemini 2.5 Pro",
  "claude-opus-4-1-20250805": "Claude Opus 4.1",
  "mimo-v2-pro": "Mimo V2 Pro",
  "gpt-4.5-preview-2025-02-27": "GPT-4.5 Preview",
  "chatgpt-4o-latest-20250326": "ChatGPT 4o Latest",
  "glm-4.7": "GLM-4.7",
  "gpt-5.2-high": "GPT-5.2 High",
  "gpt-5.2": "GPT-5.2",
  "gpt-5.1": "GPT-5.1",
  "gemini-3.1-flash-lite-preview": "Gemini 3.1 Flash Lite",
  "qwen3-max-preview": "Qwen 3 Max Preview",
  "gpt-5-high": "GPT-5 High",
  "kimi-k2.5-instant": "Kimi K2.5 Instant",
  "o3-2025-04-16": "o3",
  "grok-4-1-fast-reasoning": "Grok 4.1 Fast Reasoning",
  "kimi-k2-thinking-turbo": "Kimi K2 Thinking Turbo",
  "amazon-nova-experimental-chat-26-02-10": "Amazon Nova Experimental",
  "gpt-5-chat": "GPT-5 Chat",
  "glm-4.6": "GLM-4.6",
  "deepseek-v3.2-exp-thinking": "DeepSeek V3.2 Thinking",
  "deepseek-v3.2": "DeepSeek V3.2",
  "qwen3-max-2025-09-23": "Qwen 3 Max 2025-09-23",
};

function slugToDisplay(slug) {
  return DISPLAY_NAMES[slug] || slug.replace(/-/g, " ").replace(/\b\w/g, c => c.toUpperCase());
}

// ====== Nav ======
document.addEventListener("DOMContentLoaded", () => {
  // Burger menu toggle
  document.querySelectorAll(".navbar-burger").forEach(el => {
    el.addEventListener("click", () => {
      const target = document.getElementById(el.dataset.target);
      el.classList.toggle("is-active");
      target.classList.toggle("is-active");
    });
  });

  // Scroll animations
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add("visible"); });
  }, { threshold: 0.1 });
  document.querySelectorAll(".fade-in").forEach(el => {
    el.style.opacity = "0";
    el.style.transform = "translateY(20px)";
    el.style.transition = "opacity 0.5s ease, transform 0.5s ease";
    observer.observe(el);
  });

  // Copy BibTeX
  window.copyBibtex = function() {
    const text = document.getElementById("bibtex").textContent;
    navigator.clipboard.writeText(text).then(() => {
      const btn = document.querySelector(".copy-btn span:last-child");
      if (btn) { btn.textContent = "Copied!"; setTimeout(() => { btn.textContent = "Copy"; }, 2000); }
    });
  };

  // Load data + search
  loadData().then(() => setupSearch());
});
