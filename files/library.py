"""
Library Management System - Core Business Logic

This module contains the Library class which manages all library operations:
- Book management (add, remove, search)
- Member management (add, remove)
- Borrowing operations (borrow, return, track loans)
- Fine management (calculate, pay fines)
- Data persistence (load/save from JSON)

The Library class serves as the main service layer that handles all business
rules and constraints (e.g., preventing borrowing with unpaid fines, blocking
removal of books with active loans, etc.).

Architecture:
- Uses Model classes (Book, Member, BorrowRecord) for data representation
- Uses Storage module for JSON file operations
- Manages ID counters to ensure unique IDs across sessions
"""

import datetime

from models import Book, Member, BorrowRecord
from storage import save, load, BOOKS_FILE, MEMBERS_FILE, RECORDS_FILE


class Library:

    def __init__(self):
        """
        Initialize the Library by loading all data from JSON files.
        
        Sets up:
        - books: List of all books in the library
        - members: List of all registered members
        - records: List of all borrow records (history)
        - ID counters for each model to ensure unique IDs
        """
        self.books = [Book.from_dict(item) for item in load(BOOKS_FILE)]
        self.members = [Member.from_dict(item) for item in load(MEMBERS_FILE)]
        self.records = [BorrowRecord.from_dict(item) for item in load(RECORDS_FILE)]

        Book.id_counter = max((b.id for b in self.books), default=0) + 1
        Member.id_counter = max((m.id for m in self.members), default=0) + 1
        BorrowRecord.id_counter = max((r.id for r in self.records), default=0) + 1

    def save(self):
        save(BOOKS_FILE,   self.books)
        save(MEMBERS_FILE, self.members)
        save(RECORDS_FILE, self.records)

    # ── Books ────────────────────────────────────────────────────────────────

    def add_book(self, title, author, copies=1):
        if copies < 1:
            raise ValueError("A book must have at least one copy.")
        book = Book(title, author, copies)
        self.books.append(book)
        self.save()
        return book

    def find_book(self, book_id):
        for b in self.books:
            if b.id == book_id:
                return b
        raise ValueError(f"No book with ID {book_id}.")

    def search_books(self, query):
        q = query.lower()
        return [b for b in self.books
                if q in b.title.lower() or q in b.author.lower()]

    def remove_book(self, book_id):
        book = self.find_book(book_id)
        # Make sure no one has it borrowed
        active = [r for r in self.records if r.book_id == book_id and not r.returned_on]
        if active:
            raise ValueError(f"Cannot remove '{book.title}' — it has {len(active)} active loan(s).")
        self.books.remove(book)
        self.save()
        return book

    # ── Members ──────────────────────────────────────────────────────────────

    def add_member(self, name, email):
        member = Member(name, email)
        self.members.append(member)
        self.save()
        return member

    def find_member(self, member_id):
        for m in self.members:
            if m.id == member_id:
                return m
        raise ValueError(f"No member with ID {member_id}.")

    def remove_member(self, member_id):
        member = self.find_member(member_id)
        if member.active_loans:
            raise ValueError(f"Cannot remove '{member.name}' — they still have active loans.")
        self.members.remove(member)
        self.save()
        return member

    # ── Borrowing ────────────────────────────────────────────────────────────

    def borrow_book(self, member_id, book_id):
        member = self.find_member(member_id)
        book   = self.find_book(book_id)

        if book.available == 0:
            raise ValueError(f"'{book.title}' has no available copies right now.")
        if member.fines > 0:
            raise ValueError(f"{member.name} has unpaid fines of KES {member.fines:.2f}. Please pay first.")

        book.available -= 1
        record = BorrowRecord(member.id, member.name, book.id, book.title)
        member.active_loans.append(record.id)
        self.records.append(record)
        self.save()
        return record

    def return_book(self, record_id):
        record = next((r for r in self.records if r.id == record_id), None)
        if not record:
            raise ValueError(f"No borrow record with ID {record_id}.")
        if record.returned_on:
            raise ValueError(f"Record #{record_id} is already returned.")

        fine = record.fine
        record.returned_on = datetime.datetime.now().isoformat(timespec="seconds")

        # Update book and member
        book   = self.find_book(record.book_id)
        member = self.find_member(record.member_id)
        book.available += 1
        member.active_loans = [lid for lid in member.active_loans if lid != record_id]
        if fine > 0:
            member.fines = round(member.fines + fine, 2)

        self.save()
        return record, fine

    def pay_fine(self, member_id, amount):
        member = self.find_member(member_id)
        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")
        if member.fines == 0:
            raise ValueError(f"{member.name} has no fines to pay.")
        member.fines = max(0.0, round(member.fines - amount, 2))
        self.save()
        return member.fines

    # ── Reports ──────────────────────────────────────────────────────────────

    def overdue_loans(self):
        return [r for r in self.records if r.is_overdue]

    def active_loans(self):
        return [r for r in self.records if not r.returned_on]

    def member_loans(self, member_id):
        self.find_member(member_id)
        return [r for r in self.records if r.member_id == member_id]
