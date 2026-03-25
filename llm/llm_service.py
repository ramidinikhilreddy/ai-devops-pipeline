import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


class LLMService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env")

        self.client = genai.Client(api_key=api_key)

    def generate(self, prompt: str, temperature: float = 0.2) -> str:
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        text = response.text.strip()
        text = text.replace("```json", "").replace("```python", "").replace("```", "")
        return text