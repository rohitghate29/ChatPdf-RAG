import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
  raise ValueError("GEMINI API KEY is not set")

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_embedding(text: str) -> list[float]:
  response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=text,
  )

  return response.embeddings[0].values

def generate_embeddings(texts: list[str]) -> list[list[float]]:
  response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=texts,
  )

  return [
    embedding.values
    for embedding in response.embeddings
  ]