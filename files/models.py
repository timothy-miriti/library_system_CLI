"""
models.py
Simple classes for Book, Member, and BorrowRecord.
"""

from datetime import date, timedelta

FINE_PER_DAY = 5.0   # KES per overdue day
LOAN_DAYS    = 14    # how many days before a book is overdue


class Book:
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
    id_counter = 1

    def __init__(self, name, email):
        self.id           = Member.id_counter
        self.name         = name
        self.email        = email
        self.joined       = date.today().isoformat()
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
    id_counter = 1

    def __init__(self, member_id, member_name, book_id, book_title):
        self.id          = BorrowRecord.id_counter
        self.member_id   = member_id
        self.member_name = member_name
        self.book_id     = book_id
        self.book_title  = book_title
        self.borrowed_on = date.today().isoformat()
        self.due_on      = (date.today() + timedelta(days=LOAN_DAYS)).isoformat()
        self.returned_on = None
        BorrowRecord.id_counter += 1

    @property
    def is_overdue(self):
        return not self.returned_on and date.today() > date.fromisoformat(self.due_on)

    @property
    def fine(self):
        if not self.is_overdue:
            return 0.0
        days = (date.today() - date.fromisoformat(self.due_on)).days
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
