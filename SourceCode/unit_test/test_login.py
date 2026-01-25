
import pytest
from controllers import LibraryController

@pytest.fixture
def controller():
    c = LibraryController()
    c.data = {
        "users": [
            {
                "account_id": 1,
                "username": "user1",
                "password": c.hash_password("123456"),
                "email": "u1@test.com",
                "fullname": "User One",
                "role": "Member",
                "is_blocked": False
            },
            {
                "account_id": 2,
                "username": "blocked",
                "password": c.hash_password("123456"),
                "email": "b@test.com",
                "fullname": "Blocked User",
                "role": "Member",
                "is_blocked": True
            }
        ],
        "books": [],
        "loans": []
    }
    return c

#TC-01
def test_login_success(controller):
    ok = controller.login("user1", "123456")
    assert ok is True
    assert controller.current_user is not None
    assert controller.current_user.username == "user1"

#TC-02
def test_login_wrong_password(controller):
    ok = controller.login("user1", "wrong")
    assert ok is False
    assert controller.current_user is None

#TC-03
def test_login_user_not_exist(controller):
    ok = controller.login("ghost", "123456")
    assert ok is False

#TC-04
def test_login_blocked_user(controller):
    ok = controller.login("blocked", "123456")
    assert ok is False
    assert controller.current_user is None

#TC-05
def test_login_reset_cart(controller):
    controller.cart = {"978-1": 2}
    controller.login("user1", "123456")
    assert controller.cart == {}
