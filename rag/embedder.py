import os

from dotenv import load_dotenv
# from openai import OpenAI
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def get_embedding(text: str):
    """
    Generate an embedding vector for the provided text using Gemini.
    """
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
    )

    return response.embeddings[0].values


# def get_embedding(text: str):
#     """
#     Generate an embedding vector for the provided text.
#     """
#     response = client.embeddings.create(
#         model="text-embedding-3-small",
#         input=text
#     )
#     return response.data[0].embedding