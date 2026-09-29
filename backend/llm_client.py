import json
import os
from openai import OpenAI
from gemini_client import client as gemini_client, MODEL_NAME as GEMINI_MODEL

GROQ_MODEL = "openai/gpt-oss-120b"

_groq_client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY", "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"),
    base_url="https://api.groq.com/openai/v1",
)


def generate_json(prompt: str) -> dict:

    try:
        response = gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config={"response_mime_type": "application/json"},
        )
        return json.loads(response.text)
    except Exception as gemini_error:
        print(f"[Gemini failed: {gemini_error}] Falling back to Groq...")
        try:
            response = _groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": prompt + "\n\nImportant: return JSON only, with no extra text or explanation.",
                    }
                ],
                response_format={"type": "json_object"},
            )
            return json.loads(response.choices[0].message.content)
        except Exception as groq_error:
            raise RuntimeError(
                f"Both providers failed: Gemini ({gemini_error}) and Groq ({groq_error})"
            )


def generate_text(prompt: str) -> str:

    try:
        response = gemini_client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        return response.text
    except Exception as gemini_error:
        print(f"[Gemini failed: {gemini_error}] Falling back to Groq...")
        try:
            response = _groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content
        except Exception as groq_error:
            raise RuntimeError(
                f"Both providers failed: Gemini ({gemini_error}) and Groq ({groq_error})"
            )
