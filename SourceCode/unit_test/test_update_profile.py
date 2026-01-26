import pytest
from controllers import LibraryController


# ---------- FIXTURE ----------
@pytest.fixture
def controller(monkeypatch):
    """
    Controller với data giả để test update_profile
    """
    fake_data = {
        "users": [
            {
                "account_id": 1,
                "username": "member1",
                "password": LibraryController().hash_password("123456"),
                "email": "m1@mail.com",
                "fullname": "Member One",
                "role": "Member",
                "phone": "0900000000",
                "address": "Old Address",
                "dob": "",
                "gender": "",
                "is_blocked": False
            }
        ],
        "books": [],
        "loans": []
    }

    monkeypatch.setattr("controllers.load_data", lambda: fake_data)
    monkeypatch.setattr("controllers.save_data", lambda data: None)

    return LibraryController()


# ---------- TEST CASES ----------

def test_update_profile_success(controller):
    """
    TC04: Update phone + address thành công
    """
    # Giả lập user đã login
    controller.current_user = type(
        "U",
        (),
        {"username": "member1", "phone": "0900000000", "address": "Old Address"}
    )()

    ok, msg = controller.update_profile("0911111111", "New Address")

    assert ok is True
    assert msg == "Đã cập nhật."

    # Kiểm tra data model
    user = controller.data["users"][0]
    assert user["phone"] == "0911111111"
    assert user["address"] == "New Address"

    # Kiểm tra current_user cũng được cập nhật
    assert controller.current_user.phone == "0911111111"
    assert controller.current_user.address == "New Address"


def test_update_profile_user_not_exist(controller):
    """
    TC05: User không tồn tại → thất bại
    """
    # Giả lập user không có trong data
    controller.current_user = type(
        "U",
        (),
        {"username": "ghost", "phone": "", "address": ""}
    )()

    ok, msg = controller.update_profile("0999999999", "Nowhere")

    assert ok is False
    assert msg == "Lỗi."
