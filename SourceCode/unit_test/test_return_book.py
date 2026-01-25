# tests/test_return_book.py
import pytest
from controllers import LibraryController
from datetime import datetime, timedelta


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
                "username": "admin",
                "email": "admin@mail.com",
                "fullname": "Admin",
                "role": "Librarian",
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
                "quantity": 1,
                "location": "A1",
                "category": "IT"
            }
        ],
        "loans": []
    }
    c._save = lambda: None
    return c


# ---------- TC-RB-01: Member trả sách đúng hạn ----------
def test_return_book_on_time(controller):
    # Arrange
    controller.current_user = type("U", (), {"username": "user1", "role": "Member"})()
    controller.data["loans"].append({
        "username": "user1",
        "isbn": "978-1",
        "issue_date": str(datetime.now().date()),
        "due_date": str((datetime.now() + timedelta(days=3)).date()),
        "status": "Active"
    })

    # Act
    ok, msg = controller.return_book("978-1")

    # Assert
    assert ok is True
    assert "Đã trả sách" in msg
    assert controller.data["loans"][0]["status"] == "Returned"
    assert controller.data["books"][0]["quantity"] == 2


# ---------- TC-RB-02: Member trả sách trễ (cảnh báo) ----------
def test_return_book_late_warning(controller):
    # Arrange
    controller.current_user = type("U", (), {"username": "user1", "role": "Member"})()
    controller.data["loans"].append({
        "username": "user1",
        "isbn": "978-1",
        "issue_date": str((datetime.now() - timedelta(days=10)).date()),
        "due_date": str((datetime.now() - timedelta(days=5)).date()),
        "status": "Active"
    })

    # Act
    ok, msg = controller.return_book("978-1")

    # Assert
    assert ok is True
    assert "CẢNH BÁO" in msg
    assert controller.data["loans"][0]["status"] == "Returned"


# ---------- TC-RB-03: Member trả sách trễ nặng (phạt) ----------
def test_return_book_late_fine(controller):
    # Arrange
    controller.current_user = type("U", (), {"username": "user1", "role": "Member"})()
    controller.data["loans"].append({
        "username": "user1",
        "isbn": "978-1",
        "issue_date": str((datetime.now() - timedelta(days=20)).date()),
        "due_date": str((datetime.now() - timedelta(days=10)).date()),
        "status": "Overdue"
    })

    # Act
    ok, msg = controller.return_book("978-1")

    # Assert
    assert ok is True
    assert "PHẠT" in msg
    assert controller.data["loans"][0]["status"] == "Returned"


# ---------- TC-RB-04: Admin trả hộ cho user ----------
def test_return_book_admin_for_user(controller):
    # Arrange
    controller.current_user = type("U", (), {"username": "admin", "role": "Librarian"})()
    controller.data["loans"].append({
        "username": "user1",
        "isbn": "978-1",
        "issue_date": str(datetime.now().date()),
        "due_date": str((datetime.now() - timedelta(days=1)).date()),
        "status": "Active"
    })

    # Act
    ok, msg = controller.return_book("978-1")

    # Assert
    assert ok is True
    assert "Đã trả sách" in msg
    assert controller.data["loans"][0]["status"] == "Returned"


# ---------- TC-RB-05: Không tìm thấy phiếu mượn ----------
def test_return_book_not_found(controller):
    # Arrange
    controller.current_user = type("U", (), {"username": "user1", "role": "Member"})()

    # Act
    ok, msg = controller.return_book("978-1")

    # Assert
    assert ok is False
    assert msg == "Không tìm thấy phiếu mượn."
