import pytest
from controllers import LibraryController


# ---------- FIXTURE ----------
@pytest.fixture
def controller(monkeypatch):
    """
    Tạo controller với data giả, không dùng file JSON thật
    """
    fake_data = {
        "users": [
            {
                "account_id": 1,
                "username": "user1",
                "password": LibraryController().hash_password("123456"),
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

    # Mock load_data()
    monkeypatch.setattr("controllers.load_data", lambda: fake_data)
    # Mock save_data() (forgot_pass không gọi save nhưng giữ chuẩn)
    monkeypatch.setattr("controllers.save_data", lambda data: None)

    return LibraryController()


# ---------- TEST CASES ----------

def test_forgot_pass_email_exists(controller):
    """
    TC07: Email tồn tại → sinh OTP
    """
    ok, otp = controller.forgot_pass("user1@mail.com")

    assert ok is True
    assert otp is not None
    assert len(otp) == 6
    assert otp.isdigit()
    assert controller.otp_storage["user1@mail.com"] == otp


def test_forgot_pass_email_not_exist(controller):
    """
    TC08: Email không tồn tại → thất bại
    """
    ok, msg = controller.forgot_pass("not_exist@mail.com")

    assert ok is False
    assert msg == "Email không có."
    assert "not_exist@mail.com" not in controller.otp_storage
