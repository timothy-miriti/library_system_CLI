# 📚 Library Management System

A modern Python CLI application for managing a library's books, members, and lending operations. Built with clean architecture, persistent JSON storage, and automated fine calculation.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Features

- **📖 Book Management**: Add, list, search, and remove books with copy tracking
- **👥 Member Management**: Register, list, and manage library members
- **📋 Borrowing System**: Check out and return books with automatic due date tracking
- **⏰ Loan Tracking**: View active and overdue loans in real-time
- **💰 Fine Management**: Automatic fine calculation and payment tracking
- **💾 Data Persistence**: All data stored in JSON files for long-term preservation
- **📅 Timestamp Tracking**: Records all dates/times for registration, borrowing, and returns

## 🏗️ Architecture

The project follows a modular design:

```
📂 Library Management System
├── 📄 main.py          # CLI entry point with argparse commands
├── 📄 library.py       # Core business logic and library operations
├── 📄 models.py        # Data models (Book, Member, BorrowRecord)
├── 📄 storage.py       # File I/O and JSON persistence
├── 📂 data/            # JSON data storage directory
│   ├── books.json
│   ├── members.json
│   └── records.json
└── 📄 tests.py         # Unit tests
```

### Module Descriptions

- **main.py**: Command-line interface using `argparse`. Handles all user input and calls library methods.
- **library.py**: Core application logic. Manages books, members, loans, and fines.
- **models.py**: Data classes with auto-incrementing IDs and serialization support.
- **storage.py**: JSON file handling with error recovery.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd demo9/files
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Usage

### Basic Format

```bash
python main.py <command> [arguments]
```

### All Available Commands

View help:
```bash
python main.py --help
```

### 📚 Book Commands

| Command | Usage | Description |
|---------|-------|-------------|
| add-book | `python main.py add-book "Title" "Author" [copies]` | Add a new book (default 1 copy) |
| list-books | `python main.py list-books [available]` | List all books or only available ones |
| search-books | `python main.py search-books "query"` | Search books by title or author |
| remove-book | `python main.py remove-book <id>` | Remove a book by ID |

**Examples:**
```bash
python main.py add-book "1984" "George Orwell" 3
python main.py list-books
python main.py list-books available
python main.py search-books orwell
python main.py remove-book 1
```

### 👥 Member Commands

| Command | Usage | Description |
|---------|-------|-------------|
| add-member | `python main.py add-member "Name" "email@example.com"` | Register a new member |
| list-members | `python main.py list-members` | List all members |
| remove-member | `python main.py remove-member <id>` | Remove a member by ID |

**Examples:**
```bash
python main.py add-member "Alice Johnson" alice@example.com
python main.py list-members
python main.py remove-member 1
```

### 📋 Borrowing Commands

| Command | Usage | Description |
|---------|-------|-------------|
| borrow-book | `python main.py borrow-book <member_id> <book_id>` | Borrow a book (14-day loan) |
| return-book | `python main.py return-book <record_id>` | Return a borrowed book |
| list-loans | `python main.py list-loans` | Show all active loans |
| list-overdue | `python main.py list-overdue` | Show overdue loans |
| member-loans | `python main.py member-loans <member_id>` | Show loans for specific member |

**Examples:**
```bash
python main.py borrow-book 1 2
python main.py list-loans
python main.py list-overdue
python main.py member-loans 1
python main.py return-book 5
```

### 💰 Fine Commands

| Command | Usage | Description |
|---------|-------|-------------|
| pay-fine | `python main.py pay-fine <member_id> <amount>` | Pay outstanding fines |

**Examples:**
```bash
python main.py pay-fine 1 50
```

**Fine Details:**
- Overdue fine: **KES 5.00 per day**
- Standard loan period: **14 days**
- Fines accumulate daily after due date
- Fines must be paid before borrowing new books

## 🧪 Testing

Run the test suite with pytest:

```bash
pytest
pytest -v      # Verbose output
pytest -s      # Show print statements
```

## 💾 Data Storage

All data is persisted in JSON files located in the `data/` directory:

| File | Contents |
|------|----------|
| `data/books.json` | All books with copy counts |
| `data/members.json` | Member profiles, active loans, and fines |
| `data/records.json` | Complete borrow/return history |

Files are automatically created when you first use the app.

## 📋 Technical Details

### Fine Calculation
- **Daily Rate**: KES 5.00
- **Calculation**: `days_overdue × 5.00`
- **Applied**: Automatically when checking loans or returning late books

### Data Model
- **Book**: ID, title, author, total copies, available copies
- **Member**: ID, name, email, join date, fine balance, active loans
- **BorrowRecord**: ID, member info, book info, borrow date, due date, return date

### ID Management
- Auto-incrementing IDs for books, members, and records
- IDs persist across sessions via JSON storage
- IDs cannot be reused (prevents conflicts)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

Created as a demonstration of clean Python architecture, CLI design, and data persistence patterns.
