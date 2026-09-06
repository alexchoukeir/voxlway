import time
import signal
import json
from datetime import datetime, timezone

from services.sqs import receive_messages, delete_messages
from services.llm import generate
from services.embeddings import generate_embedding
from database import SessionLocal
from sqlalchemy import select
from models import Game

running = True

def signal_handler(sig, frame):
    global running
    print("Received signal.")
    running = False

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

def process_message(message: dict) -> None:
    """
    Processes a single message from the SQS queue.
    """
    message_body = json.loads(message['Body'])

    title = message_body['title']
    external_id = message_body['external_id']

    db = SessionLocal()

    try:
        game = db.execute(select(Game).where(Game.external_id == external_id)).scalar_one_or_none()

        if not game:
            print(f"Game with external_id {external_id} not found in the database.")
            return

        # Generate
        result = generate(title)
        embedding_text = f"{title} {result['category']} {' '.join(result['tags'])}"
        embedding = generate_embedding(embedding_text)
        
        # Store in db
        game.category = result['category']
        game.tags = result['tags']
        game.embedding = embedding
        game.processed = True
        game.processed_at = datetime.now(timezone.utc)
        db.commit()
        print(f"Processed game with external_id {external_id} and title '{title}'.")
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        db.close()

def run() -> None:
    """
    Runs the worker process that listens for messages from the SQS queue.
    """
    print("Worker started. Waiting...")
    
    while running:
        # Receive messages
        messages = receive_messages(maximum=1)

        if not messages:
            continue

        # Process each message. After a message is processed, delete from the queue.
        for message in messages:
            if not running:
                break
            try:
                process_message(message)
                delete_messages(message['ReceiptHandle'])
            except Exception as e:
                print(f"Error processing message: {e}")
                time.sleep(5)
        
        if messages:
            print("Sync completed.")
    
    print("Worker stopped.")

if __name__ == "__main__":
    run()
