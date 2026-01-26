import pytest
from controllers import LibraryController
from models import Book


# ---------- FIXTURE ----------
@pytest.fixture
def controller(monkeypatch):
    """
    Controller với data giả để test get_book_by_isbn
    """
    fake_data = {
        "users": [],
        "books": [
            {
                "isbn": "978-1",
                "title": "Python Programming",
                "author": "Guido van Rossum",
                "publisher": "O'Reilly",
                "year": 2024,
                "quantity": 5,
                "location": "Shelf A1",
                "category": "IT"
            }
        ],
        "loans": []
    }

    monkeypatch.setattr("controllers.load_data", lambda: fake_data)
    return LibraryController()


# ---------- TEST CASES ----------

def test_get_book_by_isbn_exists(controller):
    """
    TC06: ISBN tồn tại → trả về Book
    """
    book = controller.get_book_by_isbn("978-1")

    assert book is not None
    assert isinstance(book, Book)
    assert book.isbn == "978-1"
    assert book.title == "Python Programming"
    assert book.author == "Guido van Rossum"


def test_get_book_by_isbn_not_exists(controller):
    """
    TC07: ISBN không tồn tại → None
    """
    book = controller.get_book_by_isbn("999-9")

    assert book is None
