import pytest
from controllers import LibraryController

@pytest.fixture
def controller():
    c = LibraryController()
    # Cô lập dữ liệu
    c.data = {
        "users": [
            {
                "account_id": 1,
                "username": "admin",
                "password": "hashed",
                "email": "admin@lib.com",
                "fullname": "Admin",
                "role": "Librarian",
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
    c._save = lambda: None  # chặn ghi file
    return c


def test_register_success(controller):
    ok, msg = controller.register(
        "user1", "123456", "u1@mail.com",
        "User One", "0123", "HN", "2000-01-01", "M"
    )
    assert ok is True
    assert msg == "Đăng ký thành công!"
    assert len(controller.data["users"]) == 2


def test_register_duplicate_username(controller):
    ok, msg = controller.register(
        "admin", "123456", "x@mail.com",
        "X", "", "", "", ""
    )
    assert ok is False
    assert msg == "Username đã tồn tại!"
    assert len(controller.data["users"]) == 1


def test_register_password_hashed(controller):
    password = "mypassword"
    controller.register(
        "user2", password, "u2@mail.com",
        "User Two", "", "", "", ""
    )
    saved_pw = controller.data["users"][-1]["password"]
    assert saved_pw != password


def test_register_account_id_increment(controller):
    controller.register(
        "user3", "123", "u3@mail.com",
        "User Three", "", "", "", ""
    )
    assert controller.data["users"][-1]["account_id"] == 2
