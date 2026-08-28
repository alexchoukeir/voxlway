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

        [embedding] = response.embeddings
        return embedding.values
    except Exception as e:
        raise RuntimeError(f"Error generating embedding for text '{text}': {e}") from e

async def async_generate_embedding(text: str) -> list[float]:
    """
    Generates an embedding.

    Args:
        text (str): The text to generate an embedding for.
    
    Returns:
        list[float]: The generated embedding.
    """
    try:
        response = await client.aio.models.embed_content(
            model="gemini-embedding-2",
            contents=text,
            config=types.EmbedContentConfig(
                output_dimensionality=1536
            )
        )

        [embedding] = response.embeddings
        return embedding.values
    except Exception as e:
        raise RuntimeError(f"Error generating embedding for text '{text}': {e}") from e
