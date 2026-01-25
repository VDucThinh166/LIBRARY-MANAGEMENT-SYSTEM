# tests/test_search_books.py
from controllers import LibraryController

def make_controller():
    c = LibraryController()
    c.data = {
        "users": [],
        "loans": [],
        "books": [
            {
                "isbn": "1",
                "title": "Python Basics",
                "author": "Guido",
                "publisher": "A",
                "year": 2020,
                "quantity": 5,
                "location": "A1",
                "category": "IT"
            },
            {
                "isbn": "2",
                "title": "Clean Code",
                "author": "Robert Martin",
                "publisher": "B",
                "year": 2008,
                "quantity": 3,
                "location": "B1",
                "category": "IT"
            }
        ]
    }
    c._save = lambda: None  # mock save
    return c

def test_search_by_title():
    c = make_controller()
    res = c.search_books("python")

    assert len(res) == 1
    assert res[0].title == "Python Basics"

def test_search_by_author():
    c = make_controller()
    res = c.search_books("martin")

    assert len(res) == 1
    assert res[0].author == "Robert Martin"


def test_search_no_result():
    c = make_controller()
    res = c.search_books("java")

    assert res == []


def test_search_empty_keyword():
    c = make_controller()
    res = c.search_books("")

    assert len(res) == 2


def test_search_sort_by_title():
    c = make_controller()
    res = c.search_books("", sort_by="title")

    titles = [b.title for b in res]
    assert titles == sorted(titles)


def test_search_sort_by_year_desc():
    c = make_controller()
    res = c.search_books("", sort_by="year")

    years = [b.year for b in res]
    assert years == sorted(years, reverse=True)


def test_search_case_insensitive():
    c = make_controller()
    res = c.search_books("PYTHON")

    assert len(res) == 1
    assert res[0].title == "Python Basics"


def test_search_invalid_sort_value():
    c = make_controller()
    res = c.search_books("", sort_by="invalid")

    assert len(res) == 2
