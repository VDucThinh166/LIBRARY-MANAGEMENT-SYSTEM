import pytest
from controllers import LibraryController


# ---------- FIXTURE ----------
@pytest.fixture
def controller(monkeypatch):
    """
    Controller với data giả để test admin_borrow_for_user
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
            },
            {
                "account_id": 2,
                "username": "blocked_user",
                "password": LibraryController().hash_password("123456"),
                "email": "blocked@mail.com",
                "fullname": "Blocked User",
                "role": "Member",
                "phone": "",
                "address": "",
                "dob": "",
                "gender": "",
                "is_blocked": True
            }
        ],
        "books": [
            {
                "isbn": "978-1",
                "title": "Python Programming",
                "author": "Guido",
                "publisher": "O'Reilly",
                "year": 2024,
                "quantity": 3,
                "location": "Shelf A1",
                "category": "IT"
            }
        ],
        "loans": []
    }

    monkeypatch.setattr("controllers.load_data", lambda: fake_data)
    monkeypatch.setattr("controllers.save_data", lambda data: None)

    ctrl = LibraryController()

    # Giả lập admin đã login
    ctrl.current_user = type(
        "UserObj",
        (),
        {"username": "admin", "role": "Librarian"}
    )()

    return ctrl


# ---------- TEST CASES ----------

def test_admin_borrow_valid(controller):
    """
    TC06: Admin mượn hộ hợp lệ
    """
    ok, msg = controller.admin_borrow_for_user("member1", "978-1")

    assert ok is True
    assert "Admin đã mượn hộ" in msg
    assert len(controller.data["loans"]) == 1
    assert controller.data["loans"][0]["username"] == "member1"
    assert controller.data["books"][0]["quantity"] == 2


def test_admin_borrow_user_not_exist(controller):
    """
    TC07: User không tồn tại → thất bại
    """
    ok, msg = controller.admin_borrow_for_user("no_user", "978-1")

    assert ok is False
    assert msg == "User không tồn tại."
    assert controller.data["loans"] == []


def test_admin_borrow_blocked_user(controller):
    """
    TC08: User bị block → thất bại
    """
    ok, msg = controller.admin_borrow_for_user("blocked_user", "978-1")

    assert ok is False
    assert msg == "User bị CHẶN."
    assert controller.data["loans"] == []
