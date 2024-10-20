# logger.py

from datetime import datetime


def log(message, file=None):
    """Log a message with a timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if file:
        print(f"[{timestamp}] [{file}]: {message}")
    else:
        print(f"[{timestamp}]: {message}")