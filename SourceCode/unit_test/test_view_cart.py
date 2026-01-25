# tests/test_view_cart.py
import pytest
from controllers import LibraryController
from models import Book


# ---------- FIXTURE: controller cô lập ----------
@pytest.fixture
def controller():
    c = LibraryController()
    c.data = {
        "users": [],
        "books": [
            {
                "isbn": "978-1",
                "title": "Introduction to Python",
                "author": "Guido",
                "publisher": "O'Reilly",
                "year": 2024,
                "quantity": 3,
                "location": "A1",
                "category": "IT"
            },
            {
                "isbn": "978-2",
                "title": "Clean Code",
                "author": "Robert Martin",
                "publisher": "Prentice Hall",
                "year": 2008,
                "quantity": 5,
                "location": "B1",
                "category": "IT"
            }
        ],
        "loans": []
    }
    c.cart = {}
    c._save = lambda: None
    return c


# ---------- TC-VC-01: Giỏ trống ----------
def test_view_cart_empty(controller):
    # Act
    items = controller.view_cart()

    # Assert
    assert items == []


# ---------- TC-VC-02: Giỏ có 1 sách ----------
def test_view_cart_single_item(controller):
    # Arrange
    controller.cart = {"978-1": 2}

    # Act
    items = controller.view_cart()

    # Assert
    assert len(items) == 1
    book, qty = items[0]
    assert isinstance(book, Book)
    assert book.isbn == "978-1"
    assert qty == 2


# ---------- TC-VC-03: Giỏ có nhiều sách ----------
def test_view_cart_multiple_items(controller):
    # Arrange
    controller.cart = {
        "978-1": 1,
        "978-2": 3
    }

    # Act
    items = controller.view_cart()

    # Assert
    assert len(items) == 2
    isbns = {b.isbn for b, _ in items}
    assert isbns == {"978-1", "978-2"}


# ---------- TC-VC-04: ISBN trong giỏ nhưng không còn trong kho ----------
def test_view_cart_ignore_missing_book(controller):
    # Arrange
    controller.cart = {"999-9": 1}

    # Act
    items = controller.view_cart()

    # Assert
    assert items == []


# ---------- TC-VC-05: Không gây side-effect ----------
def test_view_cart_no_side_effect(controller):
    # Arrange
    controller.cart = {"978-1": 1}

    # Act
    _ = controller.view_cart()

    # Assert
    assert controller.cart == {"978-1": 1}
    assert len(controller.data["books"]) == 2
