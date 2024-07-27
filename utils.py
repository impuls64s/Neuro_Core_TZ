import json
import logging
import time
import uuid


content_type_to_extension = {
    'image/jpeg': 'jpg',
    'image/png': 'png',
    'image/gif': 'gif'
}


def setup_logging():
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )


def load_credentials(json_file: str) -> dict:
    try:
        with open(json_file, 'r') as file:
            return json.load(file)
    except Exception:
        logging.exception('Loading error credentials.json')


class Counter:
    def __init__(self, start: int = 1):
        self.value = start

    def increment(self):
        self.value += 1

    def __str__(self):
        return str(self.value)


def generate_unique_name() -> str:
    timestamp = int(time.time() * 1000)
    unique_id = uuid.uuid4()
    return f'{timestamp}_{unique_id}'
