from llm_client import generate_json


def match_resume_to_job(resume_text: str, job_title: str, job_description: str) -> dict:
    """
    Job Matching Agent (FR-4):
    Compares the resume against a specific job description and returns a
    match score + explanation + missing skills.
    Tries Gemini first, falls back to Groq automatically if Gemini is busy.
    """
    prompt = f"""
    Compare this resume with the job description and return JSON in exactly
    this shape:
    {{
      "match_score": 0,
      "matching_skills": ["..."],
      "missing_skills": ["..."],
      "explanation": "a short explanation of the score"
    }}

    Note: match_score is a number from 0 to 100.
    Respond in English regardless of the language of the resume text below.

    Resume:
    ---
    {resume_text}
    ---

    Job title: {job_title}
    Job description:
    ---
    {job_description}
    ---
    """
    return generate_json(prompt)
