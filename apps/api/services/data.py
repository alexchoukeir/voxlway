import boto3
import json

from config import config_settings

def fetch_game_data() -> list[dict]:
    """
    Fetches game data.

    Returns:
        list[dict]: A list of dictionaries containing the game data.
    """
    s3 = boto3.client("s3")
    response = s3.get_object(Bucket=config_settings.data_s3_bucket, Key="game-data/latest.json")
    games = json.loads(response["Body"].read())
    return games
