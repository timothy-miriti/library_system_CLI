"""
storage.py
Handles saving and loading all data to/from JSON files.
"""

import json
import os

BASE_DIR     = os.path.dirname(__file__)
BOOKS_FILE   = os.path.join(BASE_DIR, "books.json")
MEMBERS_FILE = os.path.join(BASE_DIR, "members.json")
RECORDS_FILE = os.path.join(BASE_DIR, "records.json")


def save(filepath, items):
    """Save a list of objects to a JSON file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump([item.to_dict() for item in items], f, indent=2)


def load(filepath):
    """Load raw data from a JSON file. Returns empty list if file missing."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath) as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: Could not read {filepath}. Starting fresh.")
        return []
