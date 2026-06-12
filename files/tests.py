"""
Pytest tests for the library management system.
Run: pytest
"""

import os

import pytest

import library
import storage
from library import Library
from models import Book, BorrowRecord, Member


@pytest.fixture(autouse=True)
def isolated_storage(tmp_path):
    """Use temporary JSON files so tests do not touch real library data."""
    books_file = os.path.join(tmp_path, "books.json")
    members_file = os.path.join(tmp_path, "members.json")
    records_file = os.path.join(tmp_path, "records.json")

    storage.BOOKS_FILE = library.BOOKS_FILE = books_file
    storage.MEMBERS_FILE = library.MEMBERS_FILE = members_file
    storage.RECORDS_FILE = library.RECORDS_FILE = records_file
    Book.id_counter = Member.id_counter = BorrowRecord.id_counter = 1

    for path in [books_file, members_file, records_file]:
        with open(path, "w") as fp:
            fp.write("[]")


def test_book_creates_with_correct_copies():
    book = Book("1984", "Orwell", 3)
    assert book.available == 3


def test_book_available_decreases_on_borrow():
    book = Book("Dune", "Herbert", 1)
    book.available -= 1
    assert book.available == 0


def test_book_save_and_reload_works():
    book = Book("Test", "A", 2)
    book.available -= 1
    reloaded = Book.from_dict(book.to_dict())
    assert reloaded.title == "Test"
    assert reloaded.available == 1


def test_member_creates_with_zero_fines():
    member = Member("Alice", "alice@x.com")
    assert member.fines == 0.0


def test_member_fines_persist_after_reload():
    member = Member("Bob", "bob@x.com")
    member.fines = 50.0
    reloaded = Member.from_dict(member.to_dict())
    assert reloaded.fines == 50.0


def test_record_new_record_is_active_not_overdue():
    record = BorrowRecord(1, "Alice", 1, "1984")
    assert not record.returned_on
    assert not record.is_overdue
    assert record.fine == 0.0


def test_record_overdue_fine_is_calculated():
    record = BorrowRecord(1, "Alice", 1, "1984")
    record.due_on = "2020-01-01"
    assert record.is_overdue
    assert record.fine > 0


def test_library_borrow_then_return_works():
    lib = Library()
    lib.add_book("Novel", "Writer", 2)
    lib.add_member("Carol", "carol@x.com")

    record = lib.borrow_book(1, 1)
    assert lib.find_book(1).available == 1

    _, fine = lib.return_book(record.id)
    assert lib.find_book(1).available == 2
    assert fine == 0.0


def test_library_cannot_borrow_unavailable_book():
    lib = Library()
    lib.add_book("Scarce", "A", copies=1)
    lib.add_member("Dave", "d@x.com")
    lib.add_member("Eve", "e@x.com")
    lib.borrow_book(1, 1)

    with pytest.raises(ValueError):
        lib.borrow_book(2, 1)


def test_library_search_returns_correct_result():
    lib = Library()
    lib.add_book("Python", "G")
    lib.add_book("Java", "H")

    results = lib.search_books("python")
    assert len(results) == 1
    assert results[0].title == "Python"


def test_library_data_persists_across_sessions():
    lib = Library()
    lib.add_book("Persist", "A")
    lib.add_member("Frank", "f@x.com")

    reloaded = Library()
    assert len(reloaded.books) == 1
    assert len(reloaded.members) == 1


def test_library_pay_fine_reduces_balance():
    lib = Library()
    lib.add_member("Grace", "g@x.com")
    lib.find_member(1).fines = 80.0
    lib.save()

    remaining = lib.pay_fine(1, 50.0)
    assert remaining == 30.0
