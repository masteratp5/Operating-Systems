# config.py

CHUNK_SIZE = 1024  # Size of each chunk (1KB)
CHUNKS_PER_PACKAGE = 5  # Number of chunks sent in each package
PORT = 5001  # Default port
DEBUG = True  # Enable debug logs

def debug(msg):
    if DEBUG:
        print(f"[DEBUG] {msg}")