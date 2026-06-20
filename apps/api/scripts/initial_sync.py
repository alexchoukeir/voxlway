import json
import boto3
from datetime import datetime
import hashlib

from config import config_settings
from services.api_fetcher import fetch_game_data
from services.sqs import send_batch_messages
from database import SessionLocal
from models import Game, SyncLog

def run() -> None:
    """
    Runs the initial sync process.
    """
    # Fetch game data from the external API
    print("Fetching game data from external API...")
    games = fetch_game_data()
    print(f"Fetched {len(games['games'])} games.")

    # Backup existing game data to S3
    print("Backing up game data to S3...")
    s3 = boto3.client('s3', region_name=config_settings.aws_region)

    try:
        s3.put_object(Bucket=config_settings.s3_bucket, Key=f"backup/games_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.json", Body=json.dumps(games).encode("utf-8"))
        print("Backup completed.")
    except Exception as e:
        print(f"Error occurred while backing up game data: {e}")

    db = SessionLocal()

    # Add games to the database and queue
    try:
        queue = []
        for game in games['games']:
            game_details = games['games'][game]
            db.add(Game(external_id=game, title=game_details[0], title_hash=hashlib.md5(game_details[0].encode()).hexdigest(), image=game_details[2]))
            queue.append({"external_id": game, "title": game_details[0]})
        db.commit()
    except Exception as e:
        print(f"Database error occurred: {e}")
        db.rollback()
    finally:
        db.close()
    
    # Send messages
    send_batch_messages(queue)

    print(f"Queued {len(queue)} games for processing.")

    print("Initial sync completed.")

if __name__ == "__main__":
    run()
