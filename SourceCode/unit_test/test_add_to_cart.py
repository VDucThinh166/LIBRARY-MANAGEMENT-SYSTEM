# tests/test_add_to_cart.py
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
                "quantity": 3,   # tồn kho
                "location": "A1",
                "category": "IT"
            }
        ],
        "loans": []
    }
    c.cart = {}        # giỏ rỗng
    c._save = lambda: None
    return c


# ---------- TC-AC-01: Thêm sách thành công ----------
def test_add_to_cart_success(controller):
    # Act
    ok, msg = controller.add_to_cart("978-1", 1)

    # Assert
    assert ok is True
    assert controller.cart["978-1"] == 1
    assert "Đã thêm" in msg


# ---------- TC-AC-02: Thêm nhiều lần cùng ISBN ----------
def test_add_to_cart_accumulate_quantity(controller):
    # Arrange
    controller.add_to_cart("978-1", 1)

    # Act
    controller.add_to_cart("978-1", 2)

    # Assert
    assert controller.cart["978-1"] == 3


# ---------- TC-AC-03: Thêm vượt quá số lượng kho ----------
def test_add_to_cart_exceed_stock(controller):
    # Act
    ok, msg = controller.add_to_cart("978-1", 5)

    # Assert
    assert ok is False
    assert "Kho không đủ hàng" in msg
    assert controller.cart == {}


# ---------- TC-AC-04: ISBN không tồn tại ----------
def test_add_to_cart_book_not_found(controller):
    # Act
    ok, msg = controller.add_to_cart("999-9", 1)

    # Assert
    assert ok is False
    assert msg == "Sách không tồn tại."
    assert controller.cart == {}


# ---------- TC-AC-05: Không gây side-effect lên kho ----------
def test_add_to_cart_no_stock_side_effect(controller):
    # Act
    controller.add_to_cart("978-1", 2)

    # Assert
    assert controller.data["books"][0]["quantity"] == 3
