const DEFAULT_API = "http://127.0.0.1:8000";

// Determine API base dynamically
const API_BASE = (() => {
  try {
    if (location.protocol.startsWith("http")) {
      return `${location.protocol}//${location.hostname}:8000`;
    }
  } catch (e) {
    // fallback
  }
  return DEFAULT_API;
})();

// Helper to get element by ID
const $ = (id) => document.getElementById(id);

// Render loading skeleton
function renderLoading() {
  return `
    <div class="card">
      <div style="width:112px;height:112px;border-radius:12px;background:linear-gradient(90deg, rgba(255,255,255,0.02), rgba(255,255,255,0.04));"></div>
      <div class="meta">
        <div class="skeleton" style="width:40%"></div>
        <div style="height:8px"></div>
        <div class="skeleton" style="width:80%;height:14px;margin-top:8px"></div>
        <div class="stats" style="margin-top:10px">
          <div class="stat skeleton" style="width:80px;height:34px"></div>
          <div class="stat skeleton" style="width:80px;height:34px"></div>
          <div class="stat skeleton" style="width:80px;height:34px"></div>
        </div>
      </div>
    </div>
  `;
}

// Render error message
function renderError(msg) {
  return `<div class="empty"><p class="error">${msg}</p></div>`;
}

// Render GitHub profile
function renderProfile(data) {
  return `
    <div class="card">
      <img src="${data.avatar_url}" alt="${data.login}" class="avatar" />
      <div class="meta">
        <h2>${data.name || data.login}</h2>
        <p>${data.bio || "No bio available"}</p>
        <div class="stats">
          <div class="stat">👥 Followers: ${data.followers}</div>
          <div class="stat">⭐Repos: ${data.public_repos}</div>
          <div class="stat">📍Location: ${data.location || "Unknown"}</div>
        </div>
        <a class="button" href="${data.html_url}" target="_blank" rel="noopener">View on GitHub</a>
      </div>
    </div>
  `;
}

// Fetch profile from backend and render
async function fetchAndRender(username) {
  const profileDiv = $("profile");
  profileDiv.innerHTML = renderLoading();

  try {
    // Correct API path to match FastAPI backend
    const res = await fetch(`${API_BASE}/api/github/${encodeURIComponent(username)}`);

    if (res.status === 404) {
      profileDiv.innerHTML = renderError(`User "${username}" not found`);
      return;
    }

    if (!res.ok) {
      const text = await res.text();
      throw new Error(text || `Request failed: ${res.status}`);
    }

    const data = await res.json();
    profileDiv.innerHTML = renderProfile(data);

  } catch (err) {
    profileDiv.innerHTML = renderError(err.message || "Unexpected error");
  }
}

// Handle search input
function onSearch() {
  const username = $("username").value.trim();
  if (!username) {
    $("profile").innerHTML = `<div class="empty"><p>Please enter a GitHub username.</p></div>`;
    return;
  }
  fetchAndRender(username);
}

// Setup event listeners
document.addEventListener("DOMContentLoaded", () => {
  $("searchBtn").addEventListener("click", onSearch);
  $("username").addEventListener("keydown", (e) => {
    if (e.key === "Enter") onSearch();
  });
});
