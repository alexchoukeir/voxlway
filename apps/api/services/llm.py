import json
from google import genai
from google.genai import types
from config import config_settings
from pydantic import BaseModel

client = genai.Client(api_key=config_settings.llm_key)

SYSTEM_PROMPT = config_settings.system_prompt

class GameData(BaseModel):
    category: str
    tags: list[str]

def generate(title: str) -> dict:
    """
    Generates game metadata.

    Args:
        title (str): The title of the game to generate metadata for.

    Returns:
        dict: The generated metadata.
    """
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=GameData
            ),
            contents=f'Game title: "{title}"'
        )
        return json.loads(response.text)
    except Exception as e:
        raise RuntimeError(f"Error generating metadata for title '{title}': {e}") from e
