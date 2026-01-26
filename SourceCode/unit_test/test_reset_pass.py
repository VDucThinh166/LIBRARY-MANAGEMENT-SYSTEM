import pytest
from controllers import LibraryController


# ---------- FIXTURE ----------
@pytest.fixture
def controller(monkeypatch):
    """
    Controller với data giả + OTP giả, không ghi file thật
    """
    fake_data = {
        "users": [
            {
                "account_id": 1,
                "username": "user1",
                "password": LibraryController().hash_password("oldpass"),
                "email": "user1@mail.com",
                "fullname": "User One",
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

    # Mock load_data
    monkeypatch.setattr("controllers.load_data", lambda: fake_data)
    # Mock save_data để không ghi file
    monkeypatch.setattr("controllers.save_data", lambda data: None)

    ctrl = LibraryController()

    # Giả lập OTP đã được sinh trước đó (từ forgot_pass)
    ctrl.otp_storage["user1@mail.com"] = "123456"

    return ctrl


# ---------- TEST CASES ----------

def test_reset_pass_correct_otp(controller):
    """
    TC09: OTP đúng → đổi mật khẩu thành công
    """
    ok, msg = controller.reset_pass(
        email="user1@mail.com",
        otp="123456",
        newp="newpass"
    )

    assert ok is True
    assert msg == "Done."

    # Mật khẩu đã được hash và cập nhật
    new_hash = controller.hash_password("newpass")
    assert controller.data["users"][0]["password"] == new_hash


def test_reset_pass_wrong_otp(controller):
    """
    TC10: OTP sai → thất bại
    """
    ok, msg = controller.reset_pass(
        email="user1@mail.com",
        otp="000000",
        newp="newpass"
    )

    assert ok is False
    assert msg == "Sai OTP."

    # Mật khẩu KHÔNG bị thay đổi
    old_hash = controller.hash_password("oldpass")
    assert controller.data["users"][0]["password"] == old_hash
