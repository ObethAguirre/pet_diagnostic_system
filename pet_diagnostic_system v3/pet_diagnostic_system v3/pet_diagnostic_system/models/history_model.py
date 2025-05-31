import json
from pathlib import Path

class HistoryModel:
    def __init__(self, filepath=Path('data/history.json')):
        self.filepath = filepath
        self.records = self.load_records()

    def load_records(self):
        if self.filepath.exists():
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_records(self):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.records, f, indent=4)

    def add_record(self, record):
        self.records.append(record)
        self.save_records()

    def get_records(self):
        return self.records
