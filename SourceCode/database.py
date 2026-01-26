# Mục đích: Thay thế SQL, dùng để đọc/ghi dữ liệu xuống file JSON
import json       # Thư viện JSON để đọc/ghi dữ liệu có cấu trúc (dạng key-value)
import os         # Thư viện OS để tương tác với hệ điều hành (kiểm tra file có tồn tại hay không)
import hashlib    # Thư viện Hashlib để mã hóa mật khẩu (bảo mật), không lưu password dạng text thông thường

class LibraryDB:
    # Hàm khởi tạo (Constructor) chạy khi Class được gọi
    def __init__(self, filename='library_data.json'):
        self.filename = filename  # Lưu tên file cơ sở dữ liệu (mặc định là library_data.json)

    # Hàm LOAD_DATA: Đọc dữ liệu từ ổ cứng lên RAM
    def load_data(self):
        # Kiểm tra xem file json đã tồn tại trên máy chưa
        if not os.path.exists(self.filename):
            # Nếu file chưa tồn tại (lần chạy đầu tiên), trả về cấu trúc dữ liệu mặc định
            return {
                "users": [  # Danh sách người dùng, khởi tạo sẵn 1 Admin mặc định
                    {
                        "id": 1, 
                        "username": "admin", 
                        # Mã hóa mật khẩu '123456' thành chuỗi hash SHA-256 để bảo mật
                        "password": hashlib.sha256("123456".encode()).hexdigest(), 
                        "role": "Librarian", # Vai trò là Thủ thư
                        "is_blocked": False  # Trạng thái tài khoản: Không bị khóa
                    }
                ],
                "books": [],
                "loans": [] 
            }
        
        # Nếu file đã tồn tại, tiến hành đọc file
        try:
            # Mở file ở chế độ 'r' (read - chỉ đọc)
            with open(self.filename, 'r') as f:
                return json.load(f) # Dùng json.load để chuyển đổi text trong file thành Dictionary Python
        except json.JSONDecodeError:
            # Phòng trường hợp file có tồn tại nhưng bên trong bị lỗi (rỗng hoặc sai cú pháp)
            # Trả về cấu trúc rỗng để chương trình không bị crash (dừng đột ngột)
            return {"users": [], "books": [], "loans": []}

    # Hàm SAVE_DATA: Ghi dữ liệu từ RAM xuống ổ cứng
    def save_data(self, data):
        # Mở file ở chế độ 'w' (write - ghi đè). Lưu ý: Dữ liệu cũ sẽ bị xóa và thay bằng mới
        with open(self.filename, 'w') as f:
            # Dùng json.dump để ghi Dictionary 'data' vào file 'f'
            # indent=4: Tự động thụt đầu dòng 4 khoảng trắng giúp file JSON đẹp, dễ đọc bằng mắt thường
            json.dump(data, f, indent=4)