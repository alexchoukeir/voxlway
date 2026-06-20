import httpx
from config import config_settings

def fetch_game_data() -> list[dict]:
    """
    Fetches game data from the external API.

    Returns:
        list[dict]: A list of game data.
    """
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(config_settings.api)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise RuntimeError(f"Error fetching game data: {e}") from e
