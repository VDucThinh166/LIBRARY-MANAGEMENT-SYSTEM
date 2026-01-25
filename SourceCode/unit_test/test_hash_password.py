# UNIT TEST
# Chức năng: kiểm tra hàm hash_password

import sys
import os

# Thêm thư mục gốc của project vào sys.path
# để file test có thể import được controllers.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from controllers import LibraryController

# Test case 1:
# Hai mật khẩu khác nhau phải cho ra hai giá trị hash khác nhau
def test_hash_password_different_input_different_output():
    ctrl = LibraryController()
    h1 = ctrl.hash_password("123456")
    h2 = ctrl.hash_password("654321")
    assert h1 != h2

# Test case 2:
# Mật khẩu sau khi hash không được trùng với mật khẩu gốc
def test_hash_password_not_plain_text():
    ctrl = LibraryController()
    pw = "123456"
    hashed = ctrl.hash_password(pw)
    assert hashed != pw
