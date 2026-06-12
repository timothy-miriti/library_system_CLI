"""
Library Management System - CLI Entry Point

This module provides the command-line interface for the library management system.
It uses argparse to handle all user commands and dispatches them to the Library class.

Usage:
    python main.py <command> [options]

Example:
    python main.py list-books
    python main.py add-book "1984" "George Orwell" 2
    python main.py borrow-book 1 3

Commands are organized into categories:
  - Book operations: add-book, list-books, search-books, remove-book
  - Member operations: add-member, list-members, remove-member
  - Borrowing operations: borrow-book, return-book, list-loans, list-overdue, member-loans
  - Fine operations: pay-fine

See 'python main.py --help' for complete documentation.
"""

import argparse
import sys
from library import Library


# ── Shared library instance ───────────────────────────────────────────────────

lib = Library()


# ── Output formatting helpers ─────────────────────────────────────────────────

def ok(msg):
    """Print a success message with [OK] prefix."""
    print(f"[OK]  {msg}")


def err(msg):
    """Print an error message with [ERR] prefix and exit."""
    print(f"[ERR] {msg}")
    sys.exit(1)


def info(msg):
    """Print an informational message with [i] prefix."""
    print(f"[i]   {msg}")


def print_table(headers, rows):
    """Print rows in a simple aligned table."""
    if not rows:
        info("Nothing to show.")
        return

    widths = [
        max(len(str(header)), *(len(str(row[index])) for row in rows))
        for index, header in enumerate(headers)
    ]
    border = "+" + "+".join("-" * (width + 2) for width in widths) + "+"
    header_row = "| " + " | ".join(
        str(header).ljust(widths[index]) for index, header in enumerate(headers)
    ) + " |"

    print(border)
    print(header_row)
    print(border)
    for row in rows:
        print("| " + " | ".join(
            str(value).ljust(widths[index]) for index, value in enumerate(row)
        ) + " |")
    print(border)


def format_date(value):
    """Make ISO timestamps easier to read in CLI tables."""
    return value.replace("T", " ") if value else "-"


def print_books(books):
    """Print books as a table."""
    rows = [
        (
            book.id,
            book.title,
            book.author,
            f"{book.available}/{book.total_copies}",
            "Available" if book.available > 0 else "Not Available",
        )
        for book in books
    ]
    print_table(("ID", "Title", "Author", "Copies", "Status"), rows)


def print_members(members):
    """Print members as a table."""
    rows = [
        (
            member.id,
            member.name,
            member.email,
            len(member.active_loans),
            f"KES {member.fines:.2f}",
        )
        for member in members
    ]
    print_table(("ID", "Name", "Email", "Loans", "Fines"), rows)


def print_loans(loans):
    """Print borrow records as a table."""
    rows = [
        (
            loan.id,
            loan.book_title,
            loan.member_name,
            format_date(loan.due_on),
            "Returned" if loan.returned_on else ("Overdue" if loan.is_overdue else "Active"),
            f"KES {loan.fine:.2f}",
        )
        for loan in loans
    ]
    print_table(("ID", "Book", "Member", "Due", "Status", "Fine"), rows)


# ── Command functions ─────────────────────────────────────────────────────────

def cmd_add_book(a):
    """Add a new book to the library."""
    try:
        book = lib.add_book(a.title, a.author, a.copies)
        ok(f"Book added! {book}")
    except ValueError as e:
        err(str(e))


def cmd_list_books(a):
    """List all books or only available ones."""
    books = [b for b in lib.books if b.available > 0] if a.available else lib.books
    print(f"\n--- Books ({len(books)}) ---")
    print_books(books)


def cmd_search_books(a):
    """Search books by title or author."""
    results = lib.search_books(a.query)
    print(f"\n--- Search: '{a.query}' ({len(results)} found) ---")
    print_books(results)


def cmd_remove_book(a):
    """Remove a book from the library."""
    try:
        book = lib.remove_book(a.id)
        ok(f"Removed: {book.title}")
    except ValueError as e:
        err(str(e))


def cmd_add_member(a):
    """Register a new member."""
    try:
        member = lib.add_member(a.name, a.email)
        ok(f"Member added! {member}")
    except ValueError as e:
        err(str(e))


def cmd_list_members(a):
    """List all registered members."""
    print(f"\n--- Members ({len(lib.members)}) ---")
    print_members(lib.members)


def cmd_remove_member(a):
    """Remove a member from the system."""
    try:
        member = lib.remove_member(a.id)
        ok(f"Removed: {member.name}")
    except ValueError as e:
        err(str(e))


def cmd_borrow(a):
    """Borrow a book for a member."""
    try:
        record = lib.borrow_book(a.member_id, a.book_id)
        ok(f"Borrowed! {record}")
    except ValueError as e:
        err(str(e))


def cmd_return(a):
    """Return a borrowed book."""
    try:
        record, fine = lib.return_book(a.record_id)
        if fine > 0:
            print(f"[!]   Returned with a late fine of KES {fine:.2f} added to account.")
        else:
            ok(f"Returned on time! Record #{record.id} closed.")
    except ValueError as e:
        err(str(e))


def cmd_pay_fine(a):
    """Pay fines for a member."""
    try:
        remaining = lib.pay_fine(a.member_id, a.amount)
        ok(f"Payment received. Remaining balance: KES {remaining:.2f}")
    except ValueError as e:
        err(str(e))


def cmd_list_loans(a):
    """List all currently active loans."""
    loans = lib.active_loans()
    print(f"\n--- Active Loans ({len(loans)}) ---")
    print_loans(loans)


def cmd_list_overdue(a):
    """List all overdue loans."""
    overdue = lib.overdue_loans()
    print(f"\n--- Overdue Loans ({len(overdue)}) ---")
    print_loans(overdue)


def cmd_member_loans(a):
    """List all loans for a specific member."""
    try:
        loans = lib.member_loans(a.member_id)
        member = lib.find_member(a.member_id)
        print(f"\n--- Loans for {member.name} ({len(loans)}) ---")
        print_loans(loans)
        info(f"Outstanding fines: KES {member.fines:.2f}")
    except ValueError as e:
        err(str(e))


# ── Build CLI ─────────────────────────────────────────────────────────────────

def build_parser():
    parser = argparse.ArgumentParser(
        prog="library",
        description="📚 Library Management System"
    )
    sub = parser.add_subparsers(dest="command")
    sub.required = True

    # add-book
    p = sub.add_parser("add-book", help="Add a new book")
    p.add_argument("title")
    p.add_argument("author")
    p.add_argument("copies", type=int, nargs="?", default=1)
    p.set_defaults(func=cmd_add_book)

    # list-books
    p = sub.add_parser("list-books", help="List all books")
    p.add_argument("available", nargs="?", choices=["available"], help="Show only available books")
    p.set_defaults(func=cmd_list_books)

    # search-books
    p = sub.add_parser("search-books", help="Search books by title or author")
    p.add_argument("query")
    p.set_defaults(func=cmd_search_books)

    # remove-book
    p = sub.add_parser("remove-book", help="Remove a book by ID")
    p.add_argument("id", type=int)
    p.set_defaults(func=cmd_remove_book)

    # add-member
    p = sub.add_parser("add-member", help="Register a new member")
    p.add_argument("name")
    p.add_argument("email")
    p.set_defaults(func=cmd_add_member)

    # list-members
    p = sub.add_parser("list-members", help="List all members")
    p.set_defaults(func=cmd_list_members)

    # remove-member
    p = sub.add_parser("remove-member", help="Remove a member by ID")
    p.add_argument("id", type=int)
    p.set_defaults(func=cmd_remove_member)

    # borrow-book
    p = sub.add_parser("borrow-book", help="Borrow a book")
    p.add_argument("member_id", type=int)
    p.add_argument("book_id", type=int)
    p.set_defaults(func=cmd_borrow)

    # return-book
    p = sub.add_parser("return-book", help="Return a borrowed book")
    p.add_argument("record_id", type=int)
    p.set_defaults(func=cmd_return)

    # pay-fine
    p = sub.add_parser("pay-fine", help="Pay a member's outstanding fines")
    p.add_argument("member_id", type=int)
    p.add_argument("amount", type=float)
    p.set_defaults(func=cmd_pay_fine)

    # list-loans
    p = sub.add_parser("list-loans", help="List all active loans")
    p.set_defaults(func=cmd_list_loans)

    # list-overdue
    p = sub.add_parser("list-overdue", help="List all overdue loans")
    p.set_defaults(func=cmd_list_overdue)

    # member-loans
    p = sub.add_parser("member-loans", help="Show all loans for a member")
    p.add_argument("member_id", type=int)
    p.set_defaults(func=cmd_member_loans)

    return parser


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    args = build_parser().parse_args()
    args.func(args)
