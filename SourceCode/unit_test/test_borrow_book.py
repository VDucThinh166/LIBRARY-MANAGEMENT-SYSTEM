# tests/test_borrow_book.py
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
                "quantity": 2,
                "location": "A1",
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

    c._save = lambda: None
    return c


# ---------- TC-BB-01: Mượn sách thành công ----------
def test_borrow_book_success(controller):
    # Act
    ok, msg = controller.borrow_book("978-1")

    # Assert
    assert ok is True
    assert "Mượn thành công" in msg
    assert controller.data["books"][0]["quantity"] == 1
    assert len(controller.data["loans"]) == 1
    assert controller.data["loans"][0]["status"] == "Active"


# ---------- TC-BB-02: Hết hàng ----------
def test_borrow_book_out_of_stock(controller):
    # Arrange
    controller.data["books"][0]["quantity"] = 0

    # Act
    ok, msg = controller.borrow_book("978-1")

    # Assert
    assert ok is False
    assert msg == "Hết hàng."
    assert len(controller.data["loans"]) == 0


# ---------- TC-BB-03: User có sách quá hạn ----------
def test_borrow_book_user_overdue(controller):
    # Arrange
    controller.data["loans"].append({
        "username": "user1",
        "isbn": "978-1",
        "status": "Overdue"
    })

    # Act
    ok, msg = controller.borrow_book("978-1")

    # Assert
    assert ok is False
    assert "BỊ CHẶN" in msg
    assert controller.data["books"][0]["quantity"] == 2
    assert len(controller.data["loans"]) == 1


# ---------- TC-BB-04: ISBN không tồn tại ----------
def test_borrow_book_isbn_not_found(controller):
    # Act
    ok, msg = controller.borrow_book("999-9")

    # Assert
    assert ok is False
    assert msg == "Hết hàng."
    assert len(controller.data["loans"]) == 0


# ---------- TC-BB-05: Không gây side-effect ngoài mong đợi ----------
def test_borrow_book_no_unexpected_side_effect(controller):
    # Arrange
    original_user = controller.current_user.username

    # Act
    controller.borrow_book("978-1")

    # Assert
    assert controller.current_user.username == original_user
