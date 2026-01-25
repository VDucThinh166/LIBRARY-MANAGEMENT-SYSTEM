# tests/test_auth.py
from controllers import LibraryController
from models import User

def test_logout_when_logged_in():
    ctl = LibraryController()

    # giả lập trạng thái login
    ctl.current_user = User(
        1, "testuser", "test@mail.com", "Test User", "Member"
    )
    ctl.cart = {"978-1": 2}

    ctl.logout()

    assert ctl.current_user is None
    assert ctl.cart == {}

def test_logout_with_empty_cart():
    ctl = LibraryController()
    ctl.current_user = User(
        2, "user2", "u2@mail.com", "User Two", "Member"
    )
    ctl.cart = {}

    ctl.logout()

    assert ctl.current_user is None
    assert ctl.cart == {}

def test_logout_without_login():
    ctl = LibraryController()
    ctl.current_user = None
    ctl.cart = {"978-1": 1}

    ctl.logout()

    assert ctl.current_user is None
    assert ctl.cart == {}
