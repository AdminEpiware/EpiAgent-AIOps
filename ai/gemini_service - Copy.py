import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)


class GeminiService:

    def __init__(self):
        self.model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

    def generate_incident_analysis(self, incident_data):

        prompt = f"""
You are a senior AIOps engineer.

Analyze the following operational signals:

Health: {incident_data['health']}
Score: {incident_data['score']}
Errors: {incident_data['errors']}
Sources: {incident_data['sources']}

Provide:

1. Severity
2. Root Cause
3. Business Impact
4. Recommended Action
5. Confidence Percentage

Keep response concise.
"""

        response = self.model.generate_content(prompt)

        return response.text