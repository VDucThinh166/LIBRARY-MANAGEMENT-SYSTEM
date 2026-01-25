# test_forgot_pass.py
# Unit tests for forgot_pass() – LibraryController
# Tool: pytest

import pytest
from controllers import LibraryController


@pytest.fixture
def controller():
    """
    Fixture tạo LibraryController với dữ liệu test độc lập.
    Không dùng file JSON thật để đảm bảo unit test isolation.
    """
    c = LibraryController()

    # Override data để tránh phụ thuộc library_data.json
    c.data = {
        "users": [
            {
                "account_id": 1,
                "username": "admin",
                "password": c.hash_password("123456"),
                "email": "admin@library.com",
                "fullname": "Administrator",
                "role": "Librarian",
                "phone": "0909000111",
                "address": "Library HQ",
                "dob": "01/01/1990",
                "gender": "Other",
                "is_blocked": False
            }
        ],
        "books": [],
        "loans": []
    }

    # Reset OTP storage cho mỗi test
    c.otp_storage = {}
    return c


# ---------- TEST CASES ----------

def test_forgot_pass_email_exists(controller):
    """
    TC-FP-01
    Email tồn tại → sinh OTP hợp lệ và lưu vào otp_storage
    """
    ok, otp = controller.forgot_pass("admin@library.com")

    assert ok is True
    assert isinstance(otp, str)
    assert len(otp) == 6
    assert otp.isdigit()
    assert controller.otp_storage["admin@library.com"] == otp


def test_forgot_pass_email_not_exists(controller):
    """
    TC-FP-02
    Email không tồn tại → fail, không tạo OTP
    """
    ok, msg = controller.forgot_pass("notfound@mail.com")

    assert ok is False
    assert msg == "Email không có."
    assert "notfound@mail.com" not in controller.otp_storage


def test_forgot_pass_override_otp(controller):
    """
    TC-FP-03
    Gọi forgot_pass nhiều lần → OTP mới ghi đè OTP cũ
    """
    ok1, otp1 = controller.forgot_pass("admin@library.com")
    ok2, otp2 = controller.forgot_pass("admin@library.com")

    assert ok1 is True
    assert ok2 is True
    assert otp1 != otp2
    assert controller.otp_storage["admin@library.com"] == otp2


def test_forgot_pass_otp_value_range(controller):
    """
    TC-FP-04
    OTP phải nằm trong khoảng 100000–999999
    """
    ok, otp = controller.forgot_pass("admin@library.com")

    assert ok is True
    assert 100000 <= int(otp) <= 999999
