import pytest
from controllers import LibraryController
from datetime import datetime, timedelta


# ---------- FIXTURE ----------
@pytest.fixture
def controller(monkeypatch):
    today = datetime.now().date()

    fake_data = {
        "users": [
            {
                "account_id": 1,
                "username": "member1",
                "password": LibraryController().hash_password("123456"),
                "email": "m1@mail.com",
                "fullname": "Member One",
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
                "quantity": 1,
                "location": "Shelf A1",
                "category": "IT"
            }
        ],
        "loans": [],
    }

    monkeypatch.setattr("controllers.load_data", lambda: fake_data)
    monkeypatch.setattr("controllers.save_data", lambda data: None)

    return LibraryController()


# ---------- TEST CASES ----------

def test_return_on_time(controller):
    """
    TC01: Member trả đúng hạn
    """
    today = datetime.now().date()
    controller.current_user = type("U", (), {"username": "member1", "role": "Member"})()

    controller.data["loans"].append({
        "username": "member1",
        "isbn": "978-1",
        "issue_date": str(today - timedelta(days=5)),
        "due_date": str(today + timedelta(days=5)),
        "status": "Active"
    })

    ok, msg = controller.return_book("978-1")

    assert ok is True
    assert "Đã trả sách" in msg
    assert controller.data["loans"][0]["status"] == "Returned"


def test_return_late_warning(controller):
    """
    TC02: Trễ > 3 ngày → warning
    """
    today = datetime.now().date()
    controller.current_user = type("U", (), {"username": "member1", "role": "Member"})()

    controller.data["loans"].append({
        "username": "member1",
        "isbn": "978-1",
        "issue_date": str(today - timedelta(days=20)),
        "due_date": str(today - timedelta(days=4)),
        "status": "Active"
    })

    ok, msg = controller.return_book("978-1")

    assert ok is True
    assert "CẢNH BÁO" in msg


def test_return_late_fine(controller):
    """
    TC03: Trễ > 7 ngày → fine
    """
    today = datetime.now().date()
    controller.current_user = type("U", (), {"username": "member1", "role": "Member"})()

    controller.data["loans"].append({
        "username": "member1",
        "isbn": "978-1",
        "issue_date": str(today - timedelta(days=30)),
        "due_date": str(today - timedelta(days=10)),
        "status": "Active"
    })

    ok, msg = controller.return_book("978-1")

    assert ok is True
    assert "PHẠT" in msg


def test_admin_return_for_user(controller):
    """
    TC04: Admin trả hộ đúng user + ISBN
    """
    today = datetime.now().date()
    controller.current_user = type("U", (), {"username": "admin", "role": "Librarian"})()

    controller.data["loans"].append({
        "username": "member1",
        "isbn": "978-1",
        "issue_date": str(today - timedelta(days=5)),
        "due_date": str(today - timedelta(days=1)),
        "status": "Active"
    })

    ok, msg = controller.return_book("978-1", username="member1") 
    assert ok is True


def test_return_isbn_not_exist(controller):
    """
    TC05: Trả ISBN không tồn tại → thất bại
    """
    controller.current_user = type("U", (), {"username": "member1", "role": "Member"})()

    ok, msg = controller.return_book("999-9")

    assert ok is False
    assert "Không tìm thấy phiếu mượn" in msg   


def test_return_quantity_increase(controller):
    """
    TC06: Quantity tăng sau khi trả
    """
    today = datetime.now().date()
    controller.current_user = type("U", (), {"username": "member1", "role": "Member"})()

    controller.data["loans"].append({
        "username": "member1",
        "isbn": "978-1",
        "issue_date": str(today - timedelta(days=5)),
        "due_date": str(today - timedelta(days=1)),
        "status": "Active"
    })

    before = controller.data["books"][0]["quantity"]

    controller.return_book("978-1")

    after = controller.data["books"][0]["quantity"]
    assert after == before + 1
