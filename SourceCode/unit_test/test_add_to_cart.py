import pytest
from controllers import LibraryController


# ---------- FIXTURE ----------
@pytest.fixture
def controller(monkeypatch):
    """
    Controller với data giả để test add_to_cart
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

def test_add_to_cart_valid(controller):
    """
    TC01: Thêm sách hợp lệ
    """
    ok, msg = controller.add_to_cart("978-1", qty=2)

    assert ok is True
    assert "Đã thêm" in msg
    assert controller.cart["978-1"] == 2


def test_add_to_cart_exceed_quantity(controller):
    """
    TC02: Thêm vượt quá quantity → thất bại
    """
    # Thêm trước 4 cuốn
    controller.add_to_cart("978-1", qty=4)

    # Thêm tiếp 2 cuốn (vượt kho = 5)
    ok, msg = controller.add_to_cart("978-1", qty=2)

    assert ok is False
    assert "Kho không đủ hàng" in msg
    assert controller.cart["978-1"] == 4


def test_add_to_cart_isbn_not_exist(controller):
    """
    TC03: ISBN không tồn tại → thất bại
    """
    ok, msg = controller.add_to_cart("999-9", qty=1)

    assert ok is False
    assert msg == "Sách không tồn tại."
    assert controller.cart == {}
