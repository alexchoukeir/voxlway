from datetime import datetime, timezone
from services.data import fetch_game_data
from services.sqs import send_batch_messages
from database import SessionLocal
from models import Game, SyncLog

def run() -> None:
    """
    Performs the initial sync of game data.
    """
    db = SessionLocal()
    sync_log = SyncLog(triggered_by="initial_sync")
    db.add(sync_log)
    db.commit()
    db.refresh(sync_log)

    try:
        # Fetch game data
        print("Fetching game data...")
        games = fetch_game_data()
        print(f"Fetched {len(games['games'])} games.")
        
        # Insert new games into the database
        print("Inserting new games into the database...")
        queue = []
        for game in games['games']:
            db.add(Game(external_id=game["external_id"], title=game["title"], player_count=game["player_count"], image=game["image"], url=game["url"]))
            queue.append({"external_id": game["external_id"], "title": game["title"]})
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
