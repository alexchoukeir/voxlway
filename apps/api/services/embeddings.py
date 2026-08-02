from google import genai
from google.genai import types
from config import config_settings

client = genai.Client(api_key=config_settings.llm_key)

def generate_embedding(text: str) -> list[float]:
    """
    Generates an embedding.

    Args:
        text (str): The text to generate an embedding for.
    
    Returns:
        list[float]: The generated embedding.
    """
    try:
        response = client.models.embed_content(
            model="gemini-embedding-2",
            contents=text,
            config=types.EmbedContentConfig(
                output_dimensionality=1536
            )
        )
        return response.embeddings
    except Exception as e:
        raise RuntimeError(f"Error generating embedding for text '{text}': {e}") from e
