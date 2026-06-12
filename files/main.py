"""
main.py
CLI entry point — all commands defined here using argparse.
Run:  python main.py <command> [options]
"""

import argparse
import sys
from library import Library


# ── Shared library instance ───────────────────────────────────────────────────

lib = Library()


# ── Helpers ───────────────────────────────────────────────────────────────────

def ok(msg):    print(f"[OK]  {msg}")
def err(msg):   print(f"[ERR] {msg}"); sys.exit(1)
def info(msg):  print(f"[i]   {msg}")

def print_list(items):
    if not items:
        info("Nothing to show.")
    for item in items:
        print(" ", item)


# ── Command functions ─────────────────────────────────────────────────────────

def cmd_add_book(a):
    try:
        book = lib.add_book(a.title, a.author, a.copies)
        ok(f"Book added! {book}")
    except ValueError as e:
        err(str(e))

def cmd_list_books(a):
    books = [b for b in lib.books if b.available > 0] if a.available else lib.books
    print(f"\n--- Books ({len(books)}) ---")
    print_list(books)

def cmd_search_books(a):
    results = lib.search_books(a.query)
    print(f"\n--- Search: '{a.query}' ({len(results)} found) ---")
    print_list(results)

def cmd_remove_book(a):
    try:
        book = lib.remove_book(a.id)
        ok(f"Removed: {book.title}")
    except ValueError as e:
        err(str(e))

def cmd_add_member(a):
    try:
        member = lib.add_member(a.name, a.email)
        ok(f"Member added! {member}")
    except ValueError as e:
        err(str(e))

def cmd_list_members(a):
    print(f"\n--- Members ({len(lib.members)}) ---")
    print_list(lib.members)

def cmd_remove_member(a):
    try:
        member = lib.remove_member(a.id)
        ok(f"Removed: {member.name}")
    except ValueError as e:
        err(str(e))

def cmd_borrow(a):
    try:
        record = lib.borrow_book(a.member_id, a.book_id)
        ok(f"Borrowed! {record}")
    except ValueError as e:
        err(str(e))

def cmd_return(a):
    try:
        record, fine = lib.return_book(a.record_id)
        if fine > 0:
            print(f"[!]   Returned with a late fine of KES {fine:.2f} added to account.")
        else:
            ok(f"Returned on time! Record #{record.id} closed.")
    except ValueError as e:
        err(str(e))

def cmd_pay_fine(a):
    try:
        remaining = lib.pay_fine(a.member_id, a.amount)
        ok(f"Payment received. Remaining balance: KES {remaining:.2f}")
    except ValueError as e:
        err(str(e))

def cmd_list_loans(a):
    loans = lib.active_loans()
    print(f"\n--- Active Loans ({len(loans)}) ---")
    print_list(loans)

def cmd_list_overdue(a):
    overdue = lib.overdue_loans()
    print(f"\n--- Overdue Loans ({len(overdue)}) ---")
    print_list(overdue)

def cmd_member_loans(a):
    try:
        loans = lib.member_loans(a.member_id)
        member = lib.find_member(a.member_id)
        print(f"\n--- Loans for {member.name} ({len(loans)}) ---")
        print_list(loans)
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
