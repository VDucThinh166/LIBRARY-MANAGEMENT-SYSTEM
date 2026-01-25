import pytest
from controllers import LibraryController


# ---------- FIXTURE: controller cô lập ----------
@pytest.fixture
def controller():
    c = LibraryController()

    # Override data để KHÔNG đụng library_data.json thật
    c.data = {
        "users": [
            {
                "account_id": 1,
                "username": "user1",
                "email": "user1@mail.com",
                "password": c.hash_password("oldpass"),
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

    # Reset otp_storage cho sạch
    c.otp_storage = {}

    return c


# ---------- TC-RP-01: Reset password thành công ----------
def test_reset_pass_success(controller):
    # Arrange
    controller.otp_storage["user1@mail.com"] = "123456"

    # Act
    ok, msg = controller.reset_pass(
        email="user1@mail.com",
        otp="123456",
        newp="newpass"
    )

    # Assert
    assert ok is True
    assert msg == "Done."
    assert controller.data["users"][0]["password"] == controller.hash_password("newpass")


# ---------- TC-RP-02: Sai OTP ----------
def test_reset_pass_wrong_otp(controller):
    # Arrange
    controller.otp_storage["user1@mail.com"] = "123456"
    old_hash = controller.data["users"][0]["password"]

    # Act
    ok, msg = controller.reset_pass(
        email="user1@mail.com",
        otp="000000",
        newp="newpass"
    )

    # Assert
    assert ok is False
    assert msg == "Sai OTP."
    assert controller.data["users"][0]["password"] == old_hash


# ---------- TC-RP-03: Email chưa có OTP ----------
def test_reset_pass_no_otp(controller):
    # Act
    ok, msg = controller.reset_pass(
        email="user1@mail.com",
        otp="123456",
        newp="newpass"
    )

    # Assert
    assert ok is False
    assert msg == "Sai OTP."


# ---------- TC-RP-04: Password phải được hash ----------
def test_reset_pass_password_is_hashed(controller):
    # Arrange
    controller.otp_storage["user1@mail.com"] = "999999"

    # Act
    controller.reset_pass(
        email="user1@mail.com",
        otp="999999",
        newp="plainpassword"
    )

    # Assert
    stored_pw = controller.data["users"][0]["password"]
    assert stored_pw != "plainpassword"
    assert stored_pw == controller.hash_password("plainpassword")
