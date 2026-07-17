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
    api = config_settings.api_games.format(query, str(uuid.uuid4()), page_token if page_token else "")

    response = client.get(api)
    response.raise_for_status()
    return response.json()

def fetch_game_images(client: httpx.Client, ids: list[int]) -> dict:
    """
    Fetches game images from the external API.
    
    Args:
        client (httpx.Client): The HTTP client to use for the request.
        ids (list[int]): A list of game external IDs.
    
    Returns:
        dict: A dictionary containing the game images.
    """
    ids_str = ",".join(map(str, ids))
    api = (config_settings.api).split(',')
    api_image = config_settings.api_image.format(ids_str)

    response = client.get(api_image)
    response.raise_for_status()
    games = response.json()

    images = {game[api[8]]: game[api[9]] for game in games['data']}
    return images

def collect_game_data(queries: list[str], games_count: int) -> list[dict]:
    """
    Collects game data from the external API for the given queries.

    Args:
        queries (list[str]): A list of queries.
    
    Returns:
        list[dict]: A list of dictionaries containing the game data.
    """
    pages_per_query = 2
    games = []
    seen_external_ids = set()
    api = (config_settings.api).split(',')

    with httpx.Client(timeout=30.0) as client:

        # Loop through each query and fetch game data
        for query in queries:

            # If enough games have been collected, break out of the loop
            if len(games) >= games_count:
                break
            
            page_token = None

            # Loop through pages for the current query
            for i in range(pages_per_query):
                if len(games) >= games_count:
                    break

                # Fetch game data for the current query and page
                try:
                    fetched_games = fetch_game_data(client, query, page_token)
                    time.sleep(1.5)  # Sleep to avoid rate limiting
                except Exception as e:
                    print(f"Error fetching game data for query '{query}': {e}")
                    time.sleep(1.5)
                    break
                
                for game in fetched_games.get(api[0], []):
                    game_inner = game.get(api[1], [])
                    game_data = game_inner[0]
                    external_id = game_data[api[2]]

                    if external_id not in seen_external_ids:
                        seen_external_ids.add(external_id)
                        games.append({
                            "external_id": external_id,
                            "title": game_data[api[3]],
                            "player_count": game_data[api[4]],
                            "image": "",
                            "url": api[5] + game_data[api[6]]
                        })

                # Get the next page token for pagination
                page_token = fetched_games.get(api[7])

                # If there is no next page token, break out of the loop
                if not page_token:
                    break
    
    return games

def collect_game_images(games: list[dict]) -> list[dict]:
    """
    Collects game images from the external API for the given games.

    Args:
        games (list[dict]): A list of dictionaries containing the game data.
    
    Returns:
        list[dict]: A list of dictionaries containing the game data with images.
    """
    external_ids = {game["external_id"]: game for game in games}
    ids = list(external_ids.keys())
    
    with httpx.Client(timeout=30.0) as client:

        # Loop through the external IDs in batches to fetch game images
        for i in range(0, len(ids), 50):
            batch_ids = ids[i:i + 50]
            try:
                images = fetch_game_images(client, batch_ids)
                time.sleep(1.5)  # Sleep to avoid rate limiting
            except Exception as e:
                print(f"Error fetching game images for batch {batch_ids}: {e}")
                time.sleep(1.5)
                continue
            
            for external_id, image in images.items():
                external_ids[external_id]["image"] = image
    
    return games

def run() -> None:
    """
    Main function to run the game data collection and upload to S3.
    """
    config = get_queries()
    queries = config["queries"]
    games_count = config["games_count"]
    games = collect_game_data(queries, games_count=games_count)
    games = collect_game_images(games)

    s3 = boto3.client("s3", region_name=config_settings.aws_region)

    try:
        s3.put_object(Bucket=config_settings.s3_bucket, Key="game-data/latest.json", Body=json.dumps({"games": games}).encode("utf-8"))
        s3.put_object(Bucket=config_settings.s3_bucket, Key=f"game-data/games-{datetime.now(timezone.utc).strftime("%Y-%m-%d_%H:%M:%S")}.json", Body=json.dumps({"games": games}).encode("utf-8"))
        print(f"Successfully uploaded {len(games)} games to S3.")
    except Exception as e:
        raise RuntimeError(f"Error uploading games to S3: {e}") from e

if __name__ == "__main__":
    run()
