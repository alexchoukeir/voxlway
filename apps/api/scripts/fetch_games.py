import boto3
import json
import time
import httpx
import uuid

from datetime import datetime, timezone
from config import config_settings

def get_queries() -> dict:
    """
    Fetches the list of queries from the S3 bucket.

    Returns:
        dict: A dictionary containing the queries.
    """
    s3 = boto3.client('s3', region_name=config_settings.aws_region)
    response = s3.get_object(Bucket=config_settings.s3_bucket, Key='queries.json')
    queries = json.loads(response['Body'].read())
    return queries

def fetch_game_data(client: httpx.Client, query: str, page_token: str = None) -> dict:
    """
    Fetches game data from the external API.
    
    Args:
        client (httpx.Client): The HTTP client to use for the request.
        query (str): The query.
        page_token (str): The page token for pagination.

    Returns:
        dict: A dictionary containing the game data.
    """
    api = config_settings.api.format(query, str(uuid.uuid4()), page_token if page_token else "")

    response = client.get(api)
    response.raise_for_status()
    return response.json()

def fetch_game_image(client: httpx.Client, ids: list[str]) -> dict:
    """
    Fetches game images from the external API.
    
    Args:
        client (httpx.Client): The HTTP client to use for the request.
        ids (list[str]): A list of game external IDs.
    
    Returns:
        dict: A dictionary containing the game images.
    """
    ids_str = ",".join(ids)
    api_image = config_settings.api_image.format(ids_str)

    response = client.get(api_image)
    response.raise_for_status()
    games = response.json()

    images = {game['id']: game['image'] for game in games['data']}
    return images
