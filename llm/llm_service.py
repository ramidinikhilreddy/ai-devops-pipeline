import os
import time
from dotenv import load_dotenv
from google import genai


class LLMService:
    def __init__(self):
        load_dotenv()

        use_real_llm = os.getenv("USE_REAL_LLM", "true").strip().lower()
        self.use_real_llm = use_real_llm == "true"

        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        api_key = os.getenv("GEMINI_API_KEY")

        print(f"USE_REAL_LLM: {self.use_real_llm}")
        print(f"GEMINI_MODEL: {self.model_name}")

        if not self.use_real_llm:
            print("⚠️ Real LLM usage is disabled by USE_REAL_LLM=false")
            self.available = False
            self.client = None
            return

        if not api_key:
            print("⚠️ No API key found — LLM disabled")
            self.available = False
            self.client = None
            return

        self.client = genai.Client(api_key=api_key)
        self.available = True

        self.max_retries = 2
        self.retry_delay_seconds = 4

    def _clean_text(self, text: str) -> str:
        text = text.strip()
        text = text.replace("```python", "")
        text = text.replace("```json", "")
        text = text.replace("```", "")
        return text.strip()

    def _is_quota_error(self, error_text: str) -> bool:
        error_upper = error_text.upper()
        return (
            "429" in error_upper
            or "RESOURCE_EXHAUSTED" in error_upper
            or "QUOTA" in error_upper
            or "RATE LIMIT" in error_upper
        )

    def _is_temporary_server_error(self, error_text: str) -> bool:
        error_upper = error_text.upper()
        return (
            "503" in error_upper
            or "UNAVAILABLE" in error_upper
            or "INTERNAL" in error_upper
            or "TIMEOUT" in error_upper
        )

    def generate(self, prompt: str) -> str:
        if not self.available or self.client is None:
            print("⚠️ Real LLM is disabled or unavailable.")
            return ""

        for attempt in range(1, self.max_retries + 1):
            try:
                print(
                    f"🤖 Trying real Gemini model: {self.model_name} "
                    f"(attempt {attempt}/{self.max_retries})"
                )

                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                )

                text = getattr(response, "text", "") or ""
                text = self._clean_text(text)

                if not text:
                    print("❌ Gemini returned empty output.")
                    return ""

                print("✅ Real LLM response received")
                return text

            except Exception as e:
                error_text = str(e)
                print(f"❌ LLM generation failed: {error_text}")

                if self._is_quota_error(error_text):
                    print("⛔ Quota/rate limit reached. Stopping immediately.")
                    return ""

                is_last_attempt = attempt == self.max_retries
                if self._is_temporary_server_error(error_text) and not is_last_attempt:
                    print(f"⏳ Retrying in {self.retry_delay_seconds} seconds...")
                    time.sleep(self.retry_delay_seconds)
                    continue

                return ""

        return ""