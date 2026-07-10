import json
import boto3
from datetime import datetime, timezone

from config import config_settings
from services.api_fetcher import fetch_game_data
from services.sqs import send_batch_messages
from database import SessionLocal
from models import Game, SyncLog

def run() -> None:
    """
    Performs the initial sync of game data from the external API to the database.
    """
    db = SessionLocal()
    sync_log = SyncLog(triggered_by="initial_sync")
    db.add(sync_log)
    db.commit()
    db.refresh(sync_log)

    try:
        # Fetch game data from the external API
        print("Fetching game data from external API...")
        games = fetch_game_data()
        print(f"Fetched {len(games['games'])} games.")

        # Backup existing game data to S3
        try:
            print("Backing up game data to S3...")
            s3 = boto3.client("s3", region_name=config_settings.aws_region)

            s3.put_object(Bucket=config_settings.s3_bucket, Key=f"backup/games_{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.json", Body=json.dumps(games).encode("utf-8"))
            print("Backup completed.")
        except Exception as e:
            print(f"Error backing up game data to S3: {e}")
        
        # Insert new games into the database
        print("Inserting new games into the database...")
        queue = []
        for game in games['games']:
            game_details = games['games'][game]
            db.add(Game(external_id=game, title=game_details[0], image=game_details[2]))
            queue.append({"external_id": game, "title": game_details[0]})
        db.commit()
        print(f"Inserted {len(queue)} games into the database.")

        # Send messages
        print("Sending messages to SQS for processing...")
        send_batch_messages(queue)
        print(f"Queued {len(queue)} games for processing.")

        sync_log.completed_at = datetime.now(timezone.utc)
        sync_log.new_games = len(queue)
        sync_log.queue_total = len(queue)
        sync_log.status = "queued"
        db.commit()
        print("Queued games for processing.")
    
    except Exception as e:
        try:
            db.rollback()
            sync_log.status = "failed"
            sync_log.completed_at = datetime.now(timezone.utc)
            db.add(sync_log)
            db.commit()
        except Exception as log_e:
            print(f"Error logging sync failure: {log_e}")
        
        raise RuntimeError(f"Initial sync failed: {e}") from e
    
    finally:
        db.close()

if __name__ == "__main__":
    run()
