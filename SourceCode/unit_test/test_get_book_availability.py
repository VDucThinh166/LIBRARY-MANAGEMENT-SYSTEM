# tests/test_get_book_availability.py
import pytest
from controllers import LibraryController


# ---------- FIXTURE: controller cô lập ----------
@pytest.fixture
def controller():
    c = LibraryController()
    c.data = {
        "users": [],
        "books": [
            {
                "isbn": "978-1",
                "title": "Introduction to Python",
                "author": "Guido",
                "publisher": "O'Reilly",
                "year": 2024,
                "quantity": 3,   # số sách còn trong kho
                "location": "A1",
                "category": "IT"
            }
        ],
        "loans": []
    }
    return c


# ---------- TC-GA-01: ISBN tồn tại, chưa có sách đang mượn ----------
def test_get_book_availability_no_loans(controller):
    # Act
    total, available = controller.get_book_availability("978-1")

    # Assert
    assert total == 3
    assert available == 3


# ---------- TC-GA-02: ISBN tồn tại, có sách đang mượn ----------
def test_get_book_availability_with_active_loans(controller):
    # Arrange: thêm 2 loan đang mượn
    controller.data["loans"] = [
        {"isbn": "978-1", "status": "Active"},
        {"isbn": "978-1", "status": "Overdue"}
    ]

    # Act
    total, available = controller.get_book_availability("978-1")

    # Assert
    assert total == 5      # 3 available + 2 borrowed
    assert available == 3


# ---------- TC-GA-03: ISBN tồn tại, loan trạng thái khác không tính ----------
def test_get_book_availability_ignore_returned(controller):
    # Arrange: loan đã trả không được tính
    controller.data["loans"] = [
        {"isbn": "978-1", "status": "Returned"},
        {"isbn": "978-1", "status": "Returned"}
    ]

    # Act
    total, available = controller.get_book_availability("978-1")

    # Assert
    assert total == 3
    assert available == 3


# ---------- TC-GA-04: ISBN không tồn tại ----------
def test_get_book_availability_isbn_not_found(controller):
    # Act
    total, available = controller.get_book_availability("999-9")

    # Assert
    assert total == 0
    assert available == 0


# ---------- TC-GA-05: Không gây side-effect lên dữ liệu ----------
def test_get_book_availability_no_side_effect(controller):
    # Act
    _ = controller.get_book_availability("978-1")

    # Assert
    assert controller.data["books"][0]["quantity"] == 3
    assert controller.data["loans"] == []
