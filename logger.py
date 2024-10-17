# logger.py

from datetime import datetime


def log(message):
    """Log a message with a timestamp."""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")
