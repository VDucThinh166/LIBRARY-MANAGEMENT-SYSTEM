import pytest
from controllers import LibraryController


# ---------- FIXTURE ----------
@pytest.fixture
def controller(tmp_path, monkeypatch):
    """
    Tạo controller với data giả, KHÔNG dùng file library_data.json thật
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
        "books": [],
        "loans": []
    }

    # Mock load_data() trong controllers
    monkeypatch.setattr("controllers.load_data", lambda: fake_data)

    return LibraryController()


# ---------- TEST CASES ----------

def test_login_success(controller):
    """
    TC01: Đúng username + password → login thành công
    """
    result = controller.login("user1", "123456")

    assert result is True
    assert controller.current_user is not None
    assert controller.current_user.username == "user1"


def test_login_wrong_password(controller):
    """
    TC02: Sai password → login thất bại
    """
    result = controller.login("user1", "wrongpass")

    assert result is False
    assert controller.current_user is None


def test_login_blocked_user(controller):
    """
    TC03: User bị block → login thất bại
    """
    result = controller.login("blocked_user", "123456")

    assert result is False
    assert controller.current_user is None


def test_login_user_not_exist(controller):
    """
    TC04: Username không tồn tại → login thất bại
    """
    result = controller.login("no_such_user", "123456")

    assert result is False
    assert controller.current_user is None
