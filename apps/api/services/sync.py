from datetime import datetime, timezone
from api_fetcher import fetch_game_data
from sqs import send_batch_messages
from database import SessionLocal
from sqlalchemy import select
from models import Game, SyncLog

def run(triggered_by: str) -> None:
    """
    Performs the sync of game data from the external API to the database.

    Args:
        triggered_by (str): The source that triggered the sync.
    """
    db = SessionLocal()
    sync_log = SyncLog(triggered_by=triggered_by)
    db.add(sync_log)
    db.commit()
    db.refresh(sync_log)

    try:
        # Fetch game data from the external API
        print("Fetching game data from external API...")
        games = fetch_game_data()
        print(f"Fetched {len(games['games'])} games.")

        # Get games from the database
        print("Fetching games from the database...")
        db_external_ids = {game.external_id: game for game in db.scalars(select(Game))}

        # New and updated games counters
        new = 0
        updated = 0
        
        queue = []
        for game in games['games']:
            game_details = games['games'][game]
            title = game_details[0]

            # If the game is not in the database, add it. If it is, see if the title has changed, update and add to queue
            if game not in db_external_ids:
                db.add(Game(external_id=game, title=title, image=game_details[2]))
                queue.append({"external_id": game, "title": game_details[0]})
                new += 1
            else:
                game_in_db = db_external_ids[game]
                game_in_db.last_synced_at = datetime.now(timezone.utc)

                # If the title is different, update the title and mark for reprocessing
                if game_in_db.title != title:
                    game_in_db.title = title
                    game_in_db.image = game_details[2]
                    game_in_db.processed = False
                    game_in_db.reprocess_needed = True
                    queue.append({"external_id": game, "title": title})
                    updated += 1
        db.commit()
        print(f"Inserted {new} new games and updated {updated} existing games in the database.")

        # Send messages
        if queue:
            print("Sending messages to SQS for processing...")
            send_batch_messages(queue)
        
        sync_log.completed_at = datetime.now(timezone.utc)
        sync_log.new_games = new
        sync_log.updated_games = updated
        sync_log.queue_total = len(queue)
        sync_log.status = "queued" if queue else "completed"
        db.commit()
        print("Queued games for processing.") if queue else print("Sync completed.")

        return {
            "new_games": new,
            "updated_games": updated,
            "queue_total": len(queue),
            "status": sync_log.status
        }
    except Exception as e:
        try:
            db.rollback()
            sync_log.status = "failed"
            sync_log.completed_at = datetime.now(timezone.utc)
            db.add(sync_log)
            db.commit()
        except Exception as log_e:
            print(f"Error logging sync failure: {log_e}")
        
        raise RuntimeError(f"Sync failed: {e}") from e

    finally:
        db.close()
