# 📚 Library Management System

A simple Python CLI app to manage books, members, borrowing, and fines.

---

## Setup

Create a virtual environment and install pytest:

```bash
# 1. Go into the project folder
cd files

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run any command
python main.py list-books
```

---

## All Commands

### Books
```bash
python main.py add-book "1984" "Orwell" 2
python main.py list-books
python main.py list-books available        # only books with copies left
python main.py search-books orwell
python main.py remove-book 1
```

### Members
```bash
python main.py add-member "Alice" alice@mail.com
python main.py list-members
python main.py remove-member 1
```

### Borrowing
```bash
python main.py borrow-book 1 1
python main.py return-book 1              # use the record ID shown after borrowing
python main.py list-loans
python main.py list-overdue
python main.py member-loans 1
```

### Fines
```bash
python main.py pay-fine 1 50
```

---

## Run Tests
```bash
pytest
```

---

## Project Files

| File | What it does |
|---|---|
| `main.py` | All CLI commands |
| `library.py` | All business logic |
| `models.py` | Book, Member, BorrowRecord classes |
| `storage.py` | Save/load JSON files |
| `tests.py` | Pytest test suite |
| `data/` | Where your data is saved |
