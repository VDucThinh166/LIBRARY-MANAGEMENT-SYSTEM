import pytest
from controllers import LibraryController


# ---------- FIXTURE ----------
@pytest.fixture
def controller(monkeypatch):
    """
    Controller với data giả để test get_book_availability
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

def test_availability_no_loan(controller):
    """
    TC08: Book tồn tại, chưa ai mượn
    total = quantity, available = quantity
    """
    total, available = controller.get_book_availability("978-1")

    assert total == 5
    assert available == 5


def test_availability_with_active_loan(controller):
    """
    TC09: Book đang có loan Active
    total = quantity + số đang mượn
    available = quantity
    """
    controller.data["loans"].append({
        "username": "user1",
        "isbn": "978-1",
        "issue_date": "2025-01-01",
        "due_date": "2025-01-15",
        "status": "Active"
    })

    total, available = controller.get_book_availability("978-1")

    assert total == 6     # 5 còn kho + 1 đang mượn
    assert available == 5


def test_availability_isbn_not_exist(controller):
    """
    TC10: ISBN không tồn tại → (0, 0)
    """
    total, available = controller.get_book_availability("999-9")

    assert total == 0
    assert available == 0
