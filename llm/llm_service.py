import os
from dotenv import load_dotenv
from google import genai

# Load .env file
load_dotenv()

class LLMService:
    def __init__(self):
        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            print("⚠️ No API key found — LLM disabled")
            self.available = False
            return

        from google import genai
        self.client = genai.Client(api_key=api_key)
        self.available = True

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        text = response.text.strip()
        text = text.replace("```json", "").replace("```", "")
        return text