"""
Data Persistence Layer - JSON File Management

This module handles all file I/O operations for the library system:
- Loading data from JSON files
- Saving data to JSON files
- Automatic directory creation
- Error handling for corrupted files

File Locations:
- books.json: All books in the library
- members.json: All registered members
- records.json: Complete borrow transaction history

The module automatically creates the 'data/' directory if it doesn't exist
and provides graceful error handling if JSON files are corrupted.
"""

import json
import os

BASE_DIR     = os.path.dirname(__file__)
BOOKS_FILE   = os.path.join(BASE_DIR, "books.json")
MEMBERS_FILE = os.path.join(BASE_DIR, "members.json")
RECORDS_FILE = os.path.join(BASE_DIR, "records.json")


def save(filepath, items):
    """
    Save a list of model objects to a JSON file.
    
    Converts each item to a dictionary and writes to JSON with pretty
    formatting (indented with 2 spaces). Creates necessary directories
    if they don't exist.
    
    Args:
        filepath (str): Path to the JSON file to write
        items (list): List of model objects with to_dict() method
    
    Raises:
        IOError: If file cannot be written
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump([item.to_dict() for item in items], f, indent=2)


def load(filepath):
    """
    Load raw data from a JSON file.
    
    Reads a JSON file and returns the parsed data. If the file doesn't
    exist, returns an empty list. If the file is corrupted, prints a
    warning and returns an empty list.
    
    Args:
        filepath (str): Path to the JSON file to read
    
    Returns:
        list: Parsed JSON data or empty list if file missing/corrupted
    
    Note:
        The returned data is raw dictionaries. Models should use their
        from_dict() class method to reconstruct objects.
    """
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath) as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: Could not read {filepath}. Starting fresh.")
        return []
