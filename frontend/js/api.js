const BASE_URL = window.location.origin.includes("8000")
  ? window.location.origin
  : "http://127.0.0.1:8000";

function getToken() {
  return localStorage.getItem("access_token");
}

function setToken(token) {
  localStorage.setItem("access_token", token);
}

function clearToken() {
  localStorage.removeItem("access_token");
}

function requireAuthOrRedirect() {
  if (!getToken()) {
    window.location.href = "login.html";
  }
}

async function apiRequest(endpoint, method = "GET", body = null, isForm = false) {
  const headers = {};
  const token = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;
  if (!isForm && body) headers["Content-Type"] = "application/json";

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    method,
    headers,
    body: isForm ? body : body ? JSON.stringify(body) : null,
  });

  if (response.status === 401) {
    clearToken();
    window.location.href = "login.html";
    return;
  }

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || "Something went wrong reaching the server.");
  }

  return response.json();
}
