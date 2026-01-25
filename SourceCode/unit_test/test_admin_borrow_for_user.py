# tests/test_admin_borrow_for_user.py
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
            },
            {
                "account_id": 2,
                "username": "blocked_user",
                "email": "b@mail.com",
                "fullname": "Blocked User",
                "role": "Member",
                "is_blocked": True
            }
        ],
        "books": [
            {
                "isbn": "978-1",
                "title": "Python",
                "author": "Guido",
                "publisher": "A",
                "year": 2024,
                "quantity": 2,
                "location": "A1",
                "category": "IT"
            }
        ],
        "loans": []
    }
    c._save = lambda: None
    return c


# ---------- TC-AB-01: Admin mượn hộ user thành công ----------
def test_admin_borrow_for_user_success(controller):
    # Act
    ok, msg = controller.admin_borrow_for_user("user1", "978-1")

    # Assert
    assert ok is True
    assert "Admin đã mượn hộ" in msg
    assert len(controller.data["loans"]) == 1
    assert controller.data["books"][0]["quantity"] == 1
    assert controller.data["loans"][0]["status"] == "Active"


# ---------- TC-AB-02: User không tồn tại ----------
def test_admin_borrow_for_user_not_found(controller):
    # Act
    ok, msg = controller.admin_borrow_for_user("ghost", "978-1")

    # Assert
    assert ok is False
    assert msg == "User không tồn tại."
    assert len(controller.data["loans"]) == 0


# ---------- TC-AB-03: User bị chặn ----------
def test_admin_borrow_for_user_blocked_user(controller):
    # Act
    ok, msg = controller.admin_borrow_for_user("blocked_user", "978-1")

    # Assert
    assert ok is False
    assert msg == "User bị CHẶN."
    assert len(controller.data["loans"]) == 0
    assert controller.data["books"][0]["quantity"] == 2


# ---------- TC-AB-04: Sách hết hàng ----------
def test_admin_borrow_for_user_out_of_stock(controller):
    # Arrange
    controller.data["books"][0]["quantity"] = 0

    # Act
    ok, msg = controller.admin_borrow_for_user("user1", "978-1")

    # Assert
    assert ok is False
    assert msg == "Hết hàng."
    assert len(controller.data["loans"]) == 0


# ---------- TC-AB-05: Không gây side-effect ngoài mong đợi ----------
def test_admin_borrow_for_user_no_unexpected_side_effect(controller):
    # Arrange
    original_users = len(controller.data["users"])

    # Act
    controller.admin_borrow_for_user("user1", "978-1")

    # Assert
    assert len(controller.data["users"]) == original_users
