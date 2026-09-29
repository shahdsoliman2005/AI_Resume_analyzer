from llm_client import generate_json


def analyze_resume(resume_text: str) -> dict:

    prompt = f"""
    Analyze this resume text professionally and return JSON in exactly this
    shape (no extra text before or after it):
    {{
      "summary": "a professional 3-line summary",
      "technical_skills": ["skill1", "skill2"],
      "soft_skills": ["skill1", "skill2"],
      "education": "highest qualification",
      "experience_years": 0
    }}

    Respond in English regardless of the language of the resume text below.

    Resume text:
    ---
    {resume_text}
    ---
    """
    return generate_json(prompt)
