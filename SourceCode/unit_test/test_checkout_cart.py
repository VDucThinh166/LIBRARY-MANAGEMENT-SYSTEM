import pytest
from controllers import LibraryController


# ---------- FIXTURE ----------
@pytest.fixture
def controller(monkeypatch):
    """
    Controller với data giả để test checkout_cart
    """
    fake_data = {
        "users": [
            {
                "account_id": 1,
                "username": "user1",
                "password": LibraryController().hash_password("123456"),
                "email": "user1@mail.com",
                "fullname": "User One",
                "role": "Member",
                "phone": "",
                "address": "",
                "dob": "",
                "gender": "",
                "is_blocked": False
            }
        ],
        "books": [
            {
                "isbn": "978-1",
                "title": "Python Programming",
                "author": "Guido",
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
    monkeypatch.setattr("controllers.save_data", lambda data: None)

    ctrl = LibraryController()
    # Giả lập user đã login
    ctrl.current_user = type(
        "UserObj",
        (),
        {"username": "user1", "role": "Member"}
    )()

    return ctrl


# ---------- TEST CASES ----------

def test_checkout_cart_empty(controller):
    """
    TC06: Checkout giỏ trống → thất bại
    """
    ok, msg = controller.checkout_cart()

    assert ok is False
    assert msg == "Giỏ trống."
    assert controller.data["loans"] == []


def test_checkout_cart_valid(controller):
    """
    TC07: Checkout giỏ hợp lệ → tạo loan
    """
    # Thêm sách vào giỏ
    controller.add_to_cart("978-1", qty=2)

    ok, msg = controller.checkout_cart()

    assert ok is True
    # Tạo đúng số loan
    assert len(controller.data["loans"]) == 2
    # Giỏ đã bị clear
    assert controller.cart == {}
    # Quantity giảm đúng
    assert controller.data["books"][0]["quantity"] == 3
