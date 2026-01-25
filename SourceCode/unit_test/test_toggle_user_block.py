# tests/test_toggle_user_block.py
from controllers import LibraryController

def make_controller():
    c = LibraryController()
    c.data = {
        "users": [
            {
                "account_id": 1,
                "username": "user1",
                "password": "x",
                "email": "u1@mail.com",
                "fullname": "User One",
                "role": "Member",
                "is_blocked": False
            }
        ],
        "books": [],
        "loans": []
    }
    c._save = lambda: None  # mock save
    return c

def test_toggle_block_from_active_to_blocked():
    c = make_controller()
    ok, msg = c.toggle_user_block("user1")

    assert ok is True
    assert c.data["users"][0]["is_blocked"] is True
    assert "BLOCKED" in msg

def test_toggle_block_from_blocked_to_active():
    c = make_controller()
    c.data["users"][0]["is_blocked"] = True

    ok, msg = c.toggle_user_block("user1")

    assert ok is True
    assert c.data["users"][0]["is_blocked"] is False
    assert "ACTIVE" in msg

def test_toggle_block_user_not_found():
    c = make_controller()
    ok, msg = c.toggle_user_block("ghost")

    assert ok is False
    assert msg == "Không tìm thấy User."
