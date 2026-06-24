import time
import signal

from sqs import receive_messages
from services.llm import generate
from services.embeddings import generate_embeddings
from database import SessionLocal

running = True

def signal_handler(sig, frame):
    global running
    print("Received signal.")
    running = False

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    print("Worker started. Waiting for tasks...")
    while running:
        time.sleep(1)
    print("Worker stopped.")
