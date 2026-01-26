import pytest
from controllers import LibraryController
from datetime import datetime, timedelta


# ---------- FIXTURE ----------
@pytest.fixture
def controller(monkeypatch):
    """
    Controller với data giả để test borrow_book
    """
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
                "quantity": 2,
                "location": "Shelf A1",
                "category": "IT"
            }
        ],
        "loans": []
    }

    monkeypatch.setattr("controllers.load_data", lambda: fake_data)
    monkeypatch.setattr("controllers.save_data", lambda data: None)

    ctrl = LibraryController()

    # Giả lập member đã login
    ctrl.current_user = type(
        "UserObj",
        (),
        {"username": "member1", "role": "Member"}
    )()

    return ctrl


# ---------- TEST CASES ----------

def test_borrow_book_success(controller):
    """
    TC01: Member mượn hợp lệ → tạo loan
    """
    ok, msg = controller.borrow_book("978-1")

    assert ok is True
    assert "Mượn thành công" in msg
    assert len(controller.data["loans"]) == 1
    assert controller.data["loans"][0]["status"] == "Active"


def test_borrow_book_out_of_stock(controller):
    """
    TC02: Sách quantity = 0 → thất bại
    """
    # Set quantity = 0
    controller.data["books"][0]["quantity"] = 0

    ok, msg = controller.borrow_book("978-1")

    assert ok is False
    assert msg == "Hết hàng."
    assert controller.data["loans"] == []


def test_borrow_book_user_has_overdue(controller):
    """
    TC03: User có loan Overdue → bị chặn
    """
    controller.data["loans"].append({
        "username": "member1",
        "isbn": "978-99",
        "issue_date": "2024-01-01",
        "due_date": "2024-01-10",
        "status": "Overdue"
    })

    ok, msg = controller.borrow_book("978-1")

    assert ok is False
    assert "BỊ CHẶN" in msg
    assert len(controller.data["loans"]) == 1  # không tạo loan mới


def test_borrow_book_quantity_decrease(controller):
    """
    TC04: Quantity giảm sau khi mượn
    """
    before_qty = controller.data["books"][0]["quantity"]

    controller.borrow_book("978-1")

    after_qty = controller.data["books"][0]["quantity"]
    assert after_qty == before_qty - 1


def test_borrow_book_due_date_14_days(controller):
    """
    TC05: Due date = issue date + 14 ngày
    """
    controller.borrow_book("978-1")

    loan = controller.data["loans"][0]
    issue_date = datetime.strptime(loan["issue_date"], "%Y-%m-%d").date()
    due_date = datetime.strptime(loan["due_date"], "%Y-%m-%d").date()

    assert due_date == issue_date + timedelta(days=14)
