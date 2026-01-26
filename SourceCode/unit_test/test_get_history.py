import pytest
from controllers import LibraryController
from datetime import datetime, timedelta


# ---------- FIXTURE ----------
@pytest.fixture
def controller(monkeypatch):
    """
    Controller với data giả để test get_history
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
        "books": [],
        "loans": []
    }

    monkeypatch.setattr("controllers.load_data", lambda: fake_data)
    monkeypatch.setattr("controllers.save_data", lambda data: None)

    return LibraryController()


# ---------- TEST CASES ----------

def test_get_history_empty(controller):
    """
    TC01: User chưa từng mượn → danh sách rỗng
    """
    controller.current_user = type(
        "U",
        (),
        {"username": "member1", "role": "Member"}
    )()

    history = controller.get_history()

    assert history == []


def test_get_history_multiple_loans_order(controller):
    """
    TC02: User có nhiều loan → trả đúng thứ tự (mới nhất trước)
    """
    controller.current_user = type(
        "U",
        (),
        {"username": "member1", "role": "Member"}
    )()

    today = datetime.now().date()

    # Thêm loan cũ hơn
    controller.data["loans"].append({
        "username": "member1",
        "isbn": "978-1",
        "issue_date": str(today - timedelta(days=10)),
        "due_date": str(today - timedelta(days=3)),
        "status": "Returned"
    })

    # Thêm loan mới hơn
    controller.data["loans"].append({
        "username": "member1",
        "isbn": "978-2",
        "issue_date": str(today - timedelta(days=2)),
        "due_date": str(today + timedelta(days=12)),
        "status": "Active"
    })

    history = controller.get_history()

    assert len(history) == 2
    # Loan mới nhất phải đứng trước
    assert history[0]["isbn"] == "978-2"
    assert history[1]["isbn"] == "978-1"
