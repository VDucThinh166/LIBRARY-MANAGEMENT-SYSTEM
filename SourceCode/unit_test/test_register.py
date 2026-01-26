import pytest
from controllers import LibraryController


# ---------- FIXTURE ----------
@pytest.fixture
def controller(monkeypatch):
    """
    Tạo controller với data giả, không ghi file thật
    """
    fake_data = {
        "users": [
            {
                "account_id": 1,
                "username": "existing_user",
                "password": LibraryController().hash_password("123456"),
                "email": "exist@mail.com",
                "fullname": "Existing User",
                "role": "Member",
                "phone": "",
                "address": "",
                "dob": "",
                "gender": "",
                "is_blocked": False
            }
        ],
        "books": [],
        "loans": []
    }

    # Mock load_data()
    monkeypatch.setattr("controllers.load_data", lambda: fake_data)
    # Mock save_data() để không ghi file
    monkeypatch.setattr("controllers.save_data", lambda data: None)

    return LibraryController()


# ---------- TEST CASES ----------

def test_register_success(controller):
    """
    TC05: Đăng ký user mới hợp lệ → thành công
    """
    ok, msg = controller.register(
        username="new_user",
        password="abc123",
        email="new@mail.com",
        fullname="New User",
        phone="0909000000",
        address="HCM",
        dob="01/01/2000",
        gender="Male"
    )

    assert ok is True
    assert msg == "Đăng ký thành công!"
    assert len(controller.data["users"]) == 2
    assert controller.data["users"][1]["username"] == "new_user"
    assert controller.data["users"][1]["role"] == "Member"


def test_register_duplicate_username(controller):
    """
    TC06: Username trùng → thất bại
    """
    ok, msg = controller.register(
        username="existing_user",
        password="abc123",
        email="dup@mail.com",
        fullname="Dup User",
        phone="0909000001",
        address="HN",
        dob="02/02/2000",
        gender="Female"
    )

    assert ok is False
    assert msg == "Username đã tồn tại!"
    assert len(controller.data["users"]) == 1
