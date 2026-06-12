"""
Data Models for Library Management System

This module defines the core data models used throughout the application:
- Book: Represents a book in the library with copy tracking
- Member: Represents a registered library member
- BorrowRecord: Represents a loan transaction (borrowing and returning)

Each model includes:
- Auto-incrementing ID generation
- String representation for display
- Serialization (to_dict) and deserialization (from_dict) for JSON storage
- Additional properties for calculated values (e.g., fine calculations)

Configuration Constants:
- FINE_PER_DAY: Amount charged per overdue day (KES 5.00)
- LOAN_DAYS: Standard loan period in days (14 days)
"""

import datetime

FINE_PER_DAY = 5.0   # KES per overdue day
LOAN_DAYS    = 14    # how many days before a book is overdue


class Book:
    """
    Represents a book in the library.
    
    Attributes:
        id (int): Unique identifier (auto-generated)
        title (str): Book title
        author (str): Author name
        total_copies (int): Total number of physical copies
        available (int): Number of copies currently available to borrow
    """
    # Counts how many books have been created (auto ID)
    id_counter = 1

    def __init__(self, title, author, copies=1):
        self.id            = Book.id_counter
        self.title         = title
        self.author        = author
        self.total_copies  = copies
        self.available     = copies
        Book.id_counter   += 1

    def __str__(self):
        status = "Available" if self.available > 0 else "Not Available"
        return (f"[Book #{self.id}] {self.title} by {self.author} | "
                f"Copies: {self.available}/{self.total_copies} | {status}")

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, d):
        b = cls(d["title"], d["author"], d["total_copies"])
        b.id        = d["id"]
        b.available = d["available"]
        return b


class Member:
    """
    Represents a registered library member.
    
    Attributes:
        id (int): Unique identifier (auto-generated)
        name (str): Member's full name
        email (str): Member's email address
        joined (str): ISO format timestamp when member registered
        fines (float): Outstanding fine balance (KES)
        active_loans (list): List of record IDs for currently borrowed books
    """
    id_counter = 1

    def __init__(self, name, email):
        self.id           = Member.id_counter
        self.name         = name
        self.email        = email
        self.joined       = datetime.datetime.now().isoformat(timespec="seconds")
        self.fines        = 0.0
        self.active_loans = []    # list of record IDs
        Member.id_counter += 1

    def __str__(self):
        return (f"[Member #{self.id}] {self.name} | {self.email} | "
                f"Loans: {len(self.active_loans)} | Fines: KES {self.fines:.2f}")

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, d):
        m              = cls(d["name"], d["email"])
        m.id           = d["id"]
        m.joined       = d["joined"]
        m.fines        = d["fines"]
        m.active_loans = d["active_loans"]
        return m


class BorrowRecord:
    """
    Represents a borrow transaction (loan of a book to a member).
    
    Attributes:
        id (int): Unique identifier (auto-generated)
        member_id (int): ID of the member who borrowed
        member_name (str): Member's name (cached for display)
        book_id (int): ID of the borrowed book
        book_title (str): Book title (cached for display)
        borrowed_on (str): ISO format timestamp when borrowed
        due_on (str): ISO format timestamp when due (14 days from borrow)
        returned_on (str): ISO format timestamp when returned (None if active)
    
    Properties:
        is_overdue: True if loan is past due date and not yet returned
        fine: Calculated fine amount based on days overdue (KES 5.00/day)
    """
    id_counter = 1

    def __init__(self, member_id, member_name, book_id, book_title):
        self.id          = BorrowRecord.id_counter
        self.member_id   = member_id
        self.member_name = member_name
        self.book_id     = book_id
        self.book_title  = book_title
        self.borrowed_on = datetime.datetime.now().isoformat(timespec="seconds")
        self.due_on      = (datetime.datetime.now() + datetime.timedelta(days=LOAN_DAYS)).isoformat(timespec="seconds")
        self.returned_on = None
        BorrowRecord.id_counter += 1

    @property
    def is_overdue(self):
        return not self.returned_on and datetime.datetime.now() > datetime.datetime.fromisoformat(self.due_on)

    @property
    def fine(self):
        if not self.is_overdue:
            return 0.0
        days = (datetime.datetime.now() - datetime.datetime.fromisoformat(self.due_on)).days
        return round(days * FINE_PER_DAY, 2)

    def __str__(self):
        status = "Returned" if self.returned_on else ("OVERDUE" if self.is_overdue else "Active")
        fine   = f" | Fine: KES {self.fine:.2f}" if self.is_overdue else ""
        return (f"[Record #{self.id}] '{self.book_title}' → {self.member_name} | "
                f"Due: {self.due_on} | Status: {status}{fine}")

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, d):
        r              = cls(d["member_id"], d["member_name"], d["book_id"], d["book_title"])
        r.id           = d["id"]
        r.borrowed_on  = d["borrowed_on"]
        r.due_on       = d["due_on"]
        r.returned_on  = d["returned_on"]
        return r
