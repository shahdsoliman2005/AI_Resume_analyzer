function showTab(tab) {
  const isLogin = tab === "login";
  document.getElementById("loginForm").style.display = isLogin ? "flex" : "none";
  document.getElementById("registerForm").style.display = isLogin ? "none" : "flex";
  document.getElementById("loginTabBtn").classList.toggle("active", isLogin);
  document.getElementById("registerTabBtn").classList.toggle("active", !isLogin);
}


if (getToken()) {
  window.location.href = "dashboard.html";
}

document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const errorBox = document.getElementById("loginError");
  errorBox.textContent = "";

  const email = document.getElementById("loginEmail").value;
  const password = document.getElementById("loginPassword").value;


  const formBody = new URLSearchParams();
  formBody.append("username", email);
  formBody.append("password", password);

  try {
    const response = await fetch(`${BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formBody,
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.detail || "Sign in failed.");
    }

    const data = await response.json();
    setToken(data.access_token);
    window.location.href = "dashboard.html";
  } catch (err) {
    errorBox.textContent = err.message;
  }
});

document.getElementById("registerForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const errorBox = document.getElementById("registerError");
  errorBox.textContent = "";

  try {
    await apiRequest("/auth/register", "POST", {
      full_name: document.getElementById("registerName").value,
      email: document.getElementById("registerEmail").value,
      password: document.getElementById("registerPassword").value,
    });

    alert("Account created! You can sign in now.");
    showTab("login");
  } catch (err) {
    errorBox.textContent = err.message;
  }
});
