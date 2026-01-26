import pytest
from controllers import LibraryController


# ---------- FIXTURE ----------
@pytest.fixture
def controller(monkeypatch):
    """
    Controller với data giả để test toggle_user_block
    """
    fake_data = {
        "users": [
            {
                "account_id": 1,
                "username": "user1",
                "password": LibraryController().hash_password("123456"),
                "email": "u1@mail.com",
                "fullname": "User One",
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

def test_block_user(controller):
    """
    TC01: Block user → is_blocked = True
    """
    ok, msg = controller.toggle_user_block("user1")

    assert ok is True
    assert "BLOCKED" in msg
    assert controller.data["users"][0]["is_blocked"] is True


def test_unblock_user(controller):
    """
    TC02: Unblock user → is_blocked = False
    """
    # Chuẩn bị: block trước
    controller.data["users"][0]["is_blocked"] = True

    ok, msg = controller.toggle_user_block("user1")

    assert ok is True
    assert "ACTIVE" in msg
    assert controller.data["users"][0]["is_blocked"] is False


def test_toggle_user_not_exist(controller):
    """
    TC03: User không tồn tại → thất bại
    """
    ok, msg = controller.toggle_user_block("no_user")

    assert ok is False
    assert msg == "Không tìm thấy User."
