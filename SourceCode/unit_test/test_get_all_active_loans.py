import pytest
from controllers import LibraryController


# ---------- FIXTURE ----------
@pytest.fixture
def controller(monkeypatch):
    """
    Controller với data giả để test get_all_active_loans
    """
    fake_data = {
        "users": [],
        "books": [],
        "loans": []
    }

    monkeypatch.setattr("controllers.load_data", lambda: fake_data)
    monkeypatch.setattr("controllers.save_data", lambda data: None)

    return LibraryController()


# ---------- TEST CASES ----------

def test_get_all_active_loans_exist(controller):
    """
    TC03: Có loan Active
    """
    controller.data["loans"] = [
        {
            "username": "user1",
            "isbn": "978-1",
            "issue_date": "2025-01-01",
            "due_date": "2025-01-15",
            "status": "Active"
        },
        {
            "username": "user2",
            "isbn": "978-2",
            "issue_date": "2025-01-02",
            "due_date": "2025-01-16",
            "status": "Returned"
        },
        {
            "username": "user3",
            "isbn": "978-3",
            "issue_date": "2025-01-03",
            "due_date": "2025-01-17",
            "status": "Overdue"
        }
    ]

    result = controller.get_all_active_loans()

    assert len(result) == 2
    statuses = [l["status"] for l in result]
    assert "Active" in statuses
    assert "Overdue" in statuses


def test_get_all_active_loans_empty(controller):
    """
    TC04: Không có loan Active
    """
    controller.data["loans"] = [
        {
            "username": "user1",
            "isbn": "978-1",
            "issue_date": "2025-01-01",
            "due_date": "2025-01-15",
            "status": "Returned"
        }
    ]

    result = controller.get_all_active_loans()

    assert result == []
