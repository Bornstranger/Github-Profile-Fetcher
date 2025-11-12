const API_BASE = "http://127.0.0.1:8000"; // backend FastAPI base URL

document.getElementById("searchBtn").addEventListener("click", async () => {
  const username = document.getElementById("username").value.trim();
  const profileDiv = document.getElementById("profile");

  if (!username) {
    profileDiv.innerHTML = "<p>Please enter a GitHub username.</p>";
    return;
  }

  profileDiv.innerHTML = "<p>Loading...</p>";

  try {
    const res = await fetch(`${API_BASE}/user/${username}`);
    if (!res.ok) throw new Error("User not found");

    const data = await res.json();

    profileDiv.innerHTML = `
      <div class="card">
        <img src="${data.avatar_url}" alt="${data.login}" class="avatar" />
        <h2>${data.name || data.login}</h2>
        <p>${data.bio || "No bio available"}</p>
        <ul>
          <li>👥 Followers: ${data.followers}</li>
          <li>⭐ Public Repos: ${data.public_repos}</li>
          <li>📍 Location: ${data.location || "Unknown"}</li>
        </ul>
        <a href="${data.html_url}" target="_blank" class="button">View on GitHub</a>
      </div>
    `;
  } catch (err) {
    profileDiv.innerHTML = `<p class="error">${err.message}</p>`;
  }
});
