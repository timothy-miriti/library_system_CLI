# Library Management System

A Python command-line app for managing a small library. It stores books, members, borrow records, return dates, and fines in JSON files so the data stays available after the program closes.

## What The App Does

- Add, list, search, and remove books
- Add, list, and remove members
- Borrow and return books
- Track active and overdue loans
- Calculate overdue fines automatically
- Pay member fines
- Save data in JSON files that you can open and inspect

The app uses Python's `datetime` module to record real date and time values for member registration, borrowing, due dates, and returns.

## Setup

Create a virtual environment and install the project dependencies:

```bash
cd files
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run The App

Use this format:

```bash
python main.py <command> <values>
```

Example:

```bash
python main.py list-books
```

## Book Commands

```bash
python main.py add-book "2002" "me" 2
python main.py list-books
python main.py list-books available
python main.py search-books orwell
python main.py remove-book 1
```

`add-book` values are:

```bash
title author copies
```

The `copies` value is optional. If you leave it out, the app uses `1`.

## Member Commands

```bash
python main.py add-member "Timoh" tim@mail.com
python main.py list-members
python main.py remove-member 1
```

`add-member` values are:

```bash
name email
```

## Borrowing Commands

```bash
python main.py borrow-book 1 1
python main.py return-book 1
python main.py list-loans
python main.py list-overdue
python main.py member-loans 1
```

`borrow-book` values are:

```bash
member_id book_id
```

When a book is borrowed, the app records the current date and time, then sets the due date 14 days later.

## Fine Commands

```bash
python main.py pay-fine 1 50
```

`pay-fine` values are:

```bash
member_id amount
```

Late fines are calculated at `KES 5.00` per overdue day.

## Data Storage

The app saves data in:

| File | Stores |
|---|---|
| `books.json` | Book records and copy counts |
| `members.json` | Member records, active loans, and fines |
| `records.json` | Borrow history, due dates, and return dates |

These are the active files used by the app. When you add a book, add a member, borrow, return, or pay a fine, these JSON files are updated.

## Project Files

| File | What it does |
|---|---|
| `main.py` | Defines the command-line interface |
| `library.py` | Handles library actions and business rules |
| `models.py` | Defines Book, Member, and BorrowRecord classes |
| `storage.py` | Loads and saves JSON data |
| `tests.py` | Pytest test suite |
| `requirements.txt` | Python dependencies |
| `pytest.ini` | Pytest configuration |

## Run Tests

After activating the virtual environment:

```bash
pytest
```

Expected result:

```text
13 passed
```
