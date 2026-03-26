import os
import numpy as np
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# 🔁 Toggle this
USE_REAL_EMBEDDING = False   # 👉 set True only if you have quota

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def get_embedding(text: str):
    """
    Returns embedding vector for given text.

    Modes:
    - Real Gemini embedding (if USE_REAL_EMBEDDING=True)
    - Mock embedding (default, no API usage)
    """

    # 🟢 MOCK MODE (recommended for demo)
    if not USE_REAL_EMBEDDING:
        np.random.seed(len(text))   # deterministic
        return np.random.rand(384).tolist()

    # 🔵 REAL GEMINI MODE
    try:
        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=text,
        )
        return response.embeddings[0].values

    except Exception as e:
        print("Embedding error:", e)
        print("Falling back to mock embedding...")

        np.random.seed(len(text))
        return np.random.rand(384).tolist()