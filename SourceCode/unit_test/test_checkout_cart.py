# tests/test_checkout_cart.py
import pytest
from controllers import LibraryController


# ---------- FIXTURE: controller cô lập ----------
@pytest.fixture
def controller():
    c = LibraryController()
    c.data = {
        "users": [
            {
                "account_id": 1,
                "username": "user1",
                "email": "u1@mail.com",
                "fullname": "User One",
                "role": "Member",
                "is_blocked": False
            }
        ],
        "books": [
            {
                "isbn": "978-1",
                "title": "Python",
                "author": "Guido",
                "publisher": "A",
                "year": 2024,
                "quantity": 3,
                "location": "A1",
                "category": "IT"
            },
            {
                "isbn": "978-2",
                "title": "Clean Code",
                "author": "Martin",
                "publisher": "B",
                "year": 2008,
                "quantity": 1,
                "location": "B1",
                "category": "IT"
            }
        ],
        "loans": []
    }

    # giả lập user đã login
    class DummyUser:
        username = "user1"
        role = "Member"
    c.current_user = DummyUser()

    c.cart = {}
    c._save = lambda: None
    return c


# ---------- TC-CC-01: Checkout giỏ trống ----------
def test_checkout_cart_empty(controller):
    # Act
    ok, msg = controller.checkout_cart()

    # Assert
    assert ok is False
    assert msg == "Giỏ trống."
    assert controller.cart == {}


# ---------- TC-CC-02: Checkout 1 sách thành công ----------
def test_checkout_cart_single_item(controller):
    # Arrange
    controller.cart = {"978-1": 1}

    # Act
    ok, msg = controller.checkout_cart()

    # Assert
    assert ok is True
    assert "Mượn thành công" in msg
    assert controller.cart == {}
    assert len(controller.data["loans"]) == 1
    assert controller.data["books"][0]["quantity"] == 2


# ---------- TC-CC-03: Checkout nhiều sách, đủ số lượng ----------
def test_checkout_cart_multiple_items(controller):
    # Arrange
    controller.cart = {
        "978-1": 2,
        "978-2": 1
    }

    # Act
    ok, msg = controller.checkout_cart()

    # Assert
    assert ok is True
    assert controller.cart == {}
    assert len(controller.data["loans"]) == 3
    assert controller.data["books"][0]["quantity"] == 1
    assert controller.data["books"][1]["quantity"] == 0


# ---------- TC-CC-04: Một sách trong giỏ bị hết hàng ----------
def test_checkout_cart_partial_failure(controller):
    # Arrange
    controller.cart = {
        "978-1": 1,
        "978-2": 2  # vượt tồn kho
    }

    # Act
    ok, msg = controller.checkout_cart()

    # Assert
    assert ok is True          # hàm vẫn return True theo logic hiện tại
    assert "Hết hàng." in msg  # có thông báo lỗi
    # 978-1 mượn được, 978-2 chỉ mượn 1
    assert len(controller.data["loans"]) == 2
    assert controller.data["books"][0]["quantity"] == 2
    assert controller.data["books"][1]["quantity"] == 0


# ---------- TC-CC-05: Không gây side-effect ngoài mong đợi ----------
def test_checkout_cart_no_unexpected_side_effect(controller):
    # Arrange
    controller.cart = {"978-1": 1}

    # Act
    controller.checkout_cart()

    # Assert
    assert controller.current_user.username == "user1"
