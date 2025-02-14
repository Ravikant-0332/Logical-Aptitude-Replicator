import os
import sys
import logging
from datetime import datetime

BASE_LOG_DIR = "logs"

current_date = datetime.now().strftime("%Y-%m-%d")
current_time = datetime.now().strftime("%H-%M-%S")

daily_log_dir = os.path.join(BASE_LOG_DIR, current_date)
os.makedirs(daily_log_dir, exist_ok=True)

log_file_path = os.path.join(daily_log_dir, f"{current_time}.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler(sys.stdout)
    ]
)

# Redirect print statements to logging.info
class LoggerWriter:
    def __init__(self, level):
        self.level = level
        self.buffer = ""

    def write(self, message):
        if message.strip():
            self.level(message.strip())

    def flush(self):
        pass

