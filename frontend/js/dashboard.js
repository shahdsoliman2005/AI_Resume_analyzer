requireAuthOrRedirect();

let currentResumeId = null;

function logout() {
  clearToken();
  window.location.href = "login.html";
}

document.getElementById("uploadForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const fileInput = document.getElementById("resumeFile");
  const loading = document.getElementById("loading");
  const errorMsg = document.getElementById("errorMsg");
  const results = document.getElementById("results");
  const matchesSection = document.getElementById("matchesSection");

  errorMsg.textContent = "";
  results.style.display = "none";
  matchesSection.style.display = "none";
  loading.style.display = "flex";

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  try {
    const data = await apiRequest("/resumes/analyze", "POST", formData, true);
    const analysis = data.analysis;
    currentResumeId = data.resume_id;

    document.getElementById("summary").textContent = analysis.summary;
    document.getElementById("education").textContent = analysis.education;
    document.getElementById("experience").textContent = analysis.experience_years;

    renderSkillMarks("technicalSkills", analysis.technical_skills, "tech");
    renderSkillMarks("softSkills", analysis.soft_skills, "soft");

    results.style.display = "block";
  } catch (err) {
    errorMsg.textContent = err.message;
  } finally {
    loading.style.display = "none";
  }
});

function renderSkillMarks(containerId, skills, kind) {
  const container = document.getElementById(containerId);
  container.innerHTML = "";
  if (!skills || !skills.length) {
    container.innerHTML = '<span class="empty-note">None listed.</span>';
    return;
  }
  skills.forEach((skill) => {
    const span = document.createElement("span");
    span.className = `mark ${kind}`;
    span.textContent = skill;
    container.appendChild(span);
  });
}

document.getElementById("findJobsBtn").addEventListener("click", async () => {
  const matchesSection = document.getElementById("matchesSection");
  const matchesList = document.getElementById("matchesList");
  const errorMsg = document.getElementById("errorMsg");

  matchesList.innerHTML = '<div class="empty-note">Finding your best matches…</div>';
  matchesSection.style.display = "block";

  try {
    const matches = await apiRequest(`/resumes/${currentResumeId}/matches`, "GET");
    matchesList.innerHTML = "";

    if (!matches.length) {
      matchesList.innerHTML = '<div class="empty-note">No jobs available yet. Add one from the Jobs page.</div>';
      return;
    }

    matches.forEach((m) => {
      const div = document.createElement("div");
      div.className = "match-card";
      div.innerHTML = `
        <div class="match-head">
          <strong>${m.job_title}</strong>
          <span class="match-score">${m.match_score}% match</span>
        </div>
        <p>${m.explanation}</p>
        <p class="missing"><strong>Missing skills:</strong> ${m.missing_skills.join(", ") || "None — nice fit 🎉"}</p>
      `;
      matchesList.appendChild(div);
    });
  } catch (err) {
    errorMsg.textContent = err.message;
  }
});
