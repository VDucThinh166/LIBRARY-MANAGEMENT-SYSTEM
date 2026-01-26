import pytest
from controllers import LibraryController


# ---------- FIXTURE ----------
@pytest.fixture
def controller(monkeypatch):
    """
    Controller với data giả để test remove_from_cart
    """
    fake_data = {
        "users": [],
        "books": [
            {
                "isbn": "978-1",
                "title": "Python Programming",
                "author": "Guido",
                "publisher": "O'Reilly",
                "year": 2024,
                "quantity": 5,
                "location": "Shelf A1",
                "category": "IT"
            }
        ],
        "loans": []
    }

    monkeypatch.setattr("controllers.load_data", lambda: fake_data)
    return LibraryController()


# ---------- TEST CASES ----------

def test_remove_from_cart_success(controller):
    """
    TC04: Xóa sách có trong giỏ
    """
    # Chuẩn bị: thêm sách vào giỏ
    controller.add_to_cart("978-1", qty=2)

    ok, msg = controller.remove_from_cart("978-1")

    assert ok is True
    assert msg == "Đã xóa khỏi giỏ."
    assert "978-1" not in controller.cart
    assert controller.cart == {}


def test_remove_from_cart_not_exist(controller):
    """
    TC05: Xóa ISBN không có trong giỏ → thất bại
    """
    ok, msg = controller.remove_from_cart("978-1")

    assert ok is False
    assert msg == "Không có trong giỏ."
    assert controller.cart == {}
