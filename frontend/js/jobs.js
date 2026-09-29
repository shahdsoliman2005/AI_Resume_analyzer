requireAuthOrRedirect();

function logout() {
  clearToken();
  window.location.href = "login.html";
}

async function loadJobs(query = "") {
  const tbody = document.getElementById("jobsTableBody");
  tbody.innerHTML = "<tr><td colspan='4'>Loading…</td></tr>";

  try {
    const endpoint = query ? `/jobs/?q=${encodeURIComponent(query)}` : "/jobs/";
    const jobs = await apiRequest(endpoint, "GET");

    tbody.innerHTML = "";
    if (!jobs.length) {
      tbody.innerHTML = "<tr><td colspan='4'>No jobs yet — add one below.</td></tr>";
      return;
    }

    jobs.forEach((job) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${job.title}</td>
        <td class="company">${job.company || "–"}</td>
        <td class="location">${job.location || "–"}</td>
        <td><button class="secondary" onclick="deleteJob(${job.id})">Delete</button></td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan='4'>Error: ${err.message}</td></tr>`;
  }
}

async function deleteJob(jobId) {
  if (!confirm("Remove this job posting?")) return;
  try {
    await apiRequest(`/jobs/${jobId}`, "DELETE");
    loadJobs();
  } catch (err) {
    alert(err.message);
  }
}

document.getElementById("searchForm").addEventListener("submit", (e) => {
  e.preventDefault();
  loadJobs(document.getElementById("searchQuery").value);
});

document.getElementById("addJobForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const errorBox = document.getElementById("jobFormError");
  errorBox.textContent = "";

  const skills = document
    .getElementById("jobSkills")
    .value.split(",")
    .map((s) => s.trim())
    .filter(Boolean);

  try {
    await apiRequest("/jobs/", "POST", {
      title: document.getElementById("jobTitle").value,
      company: document.getElementById("jobCompany").value,
      location: document.getElementById("jobLocation").value,
      description: document.getElementById("jobDescription").value,
      required_skills: skills,
    });

    document.getElementById("addJobForm").reset();
    loadJobs();
  } catch (err) {
    errorBox.textContent = err.message;
  }
});

loadJobs();
