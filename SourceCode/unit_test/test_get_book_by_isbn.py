# tests/test_get_book_by_isbn.py
import pytest
from controllers import LibraryController
from models import Book


# ---------- FIXTURE: controller cô lập ----------
@pytest.fixture
def controller():
    c = LibraryController()
    c.data = {
        "users": [],
        "loans": [],
        "books": [
            {
                "isbn": "978-1",
                "title": "Introduction to Python",
                "author": "Guido van Rossum",
                "publisher": "O'Reilly",
                "year": 2024,
                "quantity": 10,
                "location": "Shelf A1",
                "category": "IT"
            },
            {
                "isbn": "978-2",
                "title": "Clean Code",
                "author": "Robert C. Martin",
                "publisher": "Prentice Hall",
                "year": 2008,
                "quantity": 5,
                "location": "Shelf B2",
                "category": "IT"
            }
        ]
    }
    return c


# ---------- TC-GB-01: Lấy sách theo ISBN tồn tại ----------
def test_get_book_by_isbn_success(controller):
    # Act
    book = controller.get_book_by_isbn("978-1")

    # Assert
    assert book is not None
    assert isinstance(book, Book)
    assert book.isbn == "978-1"
    assert book.title == "Introduction to Python"
    assert book.author == "Guido van Rossum"


# ---------- TC-GB-02: ISBN không tồn tại ----------
def test_get_book_by_isbn_not_found(controller):
    # Act
    book = controller.get_book_by_isbn("999-9")

    # Assert
    assert book is None


# ---------- TC-GB-03: Kiểm tra dữ liệu Book được map đúng ----------
def test_get_book_by_isbn_full_attributes(controller):
    # Act
    book = controller.get_book_by_isbn("978-2")

    # Assert
    assert book.publisher == "Prentice Hall"
    assert book.year == 2008
    assert book.quantity == 5
    assert book.location == "Shelf B2"
    assert book.category == "IT"


# ---------- TC-GB-04: Không làm thay đổi dữ liệu gốc ----------
def test_get_book_by_isbn_no_side_effect(controller):
    # Act
    _ = controller.get_book_by_isbn("978-1")

    # Assert
    assert len(controller.data["books"]) == 2
    assert controller.data["books"][0]["quantity"] == 10
