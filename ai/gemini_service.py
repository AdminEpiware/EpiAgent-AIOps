import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class GeminiQuotaError(Exception):
    pass


class GeminiUnavailableError(Exception):
    pass


def _is_quota_error(error):
    text = str(error).lower()
    return (
        "quota" in text
        or "429" in text
        or "resource_exhausted" in text
        or "rate limit" in text
    )


class GeminiService:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise GeminiUnavailableError("GEMINI_API_KEY is missing")

        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def generate_incident_analysis(self, incident_data):
        prompt = f"""
You are a senior AIOps engineer.

Analyze the following Splunk-derived operational context:

{incident_data}

Provide a concise operational response with:

1. Severity
2. Root Cause
3. Business Impact
4. Recommended Action
5. Confidence Percentage

Keep the response concise, practical, and incident-focused.
"""

        try:
            response = self.model.generate_content(prompt)
            return response.text

        except Exception as exc:
            if _is_quota_error(exc):
                raise GeminiQuotaError("Gemini API quota limit reached") from exc

            raise GeminiUnavailableError(
                f"Gemini service unavailable: {exc}"
            ) from exc