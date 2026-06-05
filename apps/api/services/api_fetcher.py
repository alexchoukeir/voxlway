import httpx
from config import config_settings

async def fetch_game_data() -> list[dict]:
    """
    Fetches game data from the external API.

    Returns:
        list[dict]: A list of game data.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(config_settings.api)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise RuntimeError(f"Error fetching game data: {e}") from e
