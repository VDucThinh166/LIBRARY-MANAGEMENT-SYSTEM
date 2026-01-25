# tests/test_remove_from_cart.py
import pytest
from controllers import LibraryController


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


# ---------- TC-RC-01: Xóa sách thành công ----------
def test_remove_from_cart_success(controller):
    # Arrange
    controller.cart = {"978-1": 2}

    # Act
    ok, msg = controller.remove_from_cart("978-1")

    # Assert
    assert ok is True
    assert msg == "Đã xóa khỏi giỏ."
    assert controller.cart == {}


# ---------- TC-RC-02: Xóa khi giỏ có nhiều sách ----------
def test_remove_from_cart_multiple_items(controller):
    # Arrange
    controller.cart = {
        "978-1": 1,
        "978-2": 3
    }

    # Act
    ok, msg = controller.remove_from_cart("978-2")

    # Assert
    assert ok is True
    assert "978-2" not in controller.cart
    assert "978-1" in controller.cart
    assert controller.cart["978-1"] == 1


# ---------- TC-RC-03: ISBN không có trong giỏ ----------
def test_remove_from_cart_not_in_cart(controller):
    # Arrange
    controller.cart = {"978-1": 1}

    # Act
    ok, msg = controller.remove_from_cart("978-2")

    # Assert
    assert ok is False
    assert msg == "Không có trong giỏ."
    assert controller.cart == {"978-1": 1}


# ---------- TC-RC-04: Xóa khi giỏ trống ----------
def test_remove_from_cart_empty(controller):
    # Act
    ok, msg = controller.remove_from_cart("978-1")

    # Assert
    assert ok is False
    assert msg == "Không có trong giỏ."
    assert controller.cart == {}


# ---------- TC-RC-05: Không gây side-effect ----------
def test_remove_from_cart_no_side_effect(controller):
    # Arrange
    controller.cart = {"978-1": 1}

    # Act
    controller.remove_from_cart("978-1")

    # Assert
    assert len(controller.data["books"]) == 2
    assert controller.data["books"][0]["quantity"] == 3
