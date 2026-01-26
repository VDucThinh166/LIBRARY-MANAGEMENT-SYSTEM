import pytest
from controllers import LibraryController


# ---------- FIXTURE ----------
@pytest.fixture
def controller(monkeypatch):
    """
    Controller với data giả để test search_books
    """
    fake_data = {
        "users": [],
        "books": [
            {
                "isbn": "978-1",
                "title": "Python Programming",
                "author": "Guido",
                "publisher": "Pub1",
                "year": 2020,
                "quantity": 5,
                "location": "A1",
                "category": "IT"
            },
            {
                "isbn": "978-2",
                "title": "Clean Code",
                "author": "Robert Martin",
                "publisher": "Pub2",
                "year": 2008,
                "quantity": 3,
                "location": "B1",
                "category": "IT"
            },
            {
                "isbn": "978-3",
                "title": "Advanced Python",
                "author": "Someone Else",
                "publisher": "Pub3",
                "year": 2024,
                "quantity": 2,
                "location": "C1",
                "category": "IT"
            }
        ],
        "loans": []
    }

    monkeypatch.setattr("controllers.load_data", lambda: fake_data)
    return LibraryController()


# ---------- TEST CASES ----------

def test_search_by_title(controller):
    """
    TC01: Keyword trùng title → trả về danh sách
    """
    result = controller.search_books(keyword="python")

    assert len(result) == 2
    titles = [b.title for b in result]
    assert "Python Programming" in titles
    assert "Advanced Python" in titles


def test_search_by_author(controller):
    """
    TC02: Keyword trùng author → trả về danh sách
    """
    result = controller.search_books(keyword="robert")

    assert len(result) == 1
    assert result[0].author == "Robert Martin"


def test_search_no_result(controller):
    """
    TC03: Không có kết quả → danh sách rỗng
    """
    result = controller.search_books(keyword="java")

    assert result == []


def test_search_sort_by_title(controller):
    """
    TC04: Sort theo title
    """
    result = controller.search_books(keyword="python", sort_by="title")

    titles = [b.title for b in result]
    assert titles == sorted(titles)


def test_search_sort_by_year(controller):
    """
    TC05: Sort theo year (giảm dần)
    """
    result = controller.search_books(keyword="python", sort_by="year")

    years = [b.year for b in result]
    assert years == sorted(years, reverse=True)
