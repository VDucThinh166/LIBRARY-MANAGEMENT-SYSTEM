# 📚 Library Management System (LMS) - Group 12

Chào mừng đến với dự án **Hệ thống Quản lý Thư viện** (Console-based) của Nhóm 12. Đây là ứng dụng quản lý quy trình mượn trả sách, quản lý độc giả và kho sách, được xây dựng bằng ngôn ngữ **Python** và lưu trữ dữ liệu dưới dạng **JSON**.

---

## 🚀 Tính năng nổi bật

Hệ thống được phân quyền chặt chẽ giữa **Khách (Guest)**, **Thành viên (Member)** và **Thủ thư (Librarian/Admin)**.

### 1. Dành cho Thủ thư (Librarian/Admin)
* ✅ **Quản lý Kho sách:** Thêm sách mới vào kho.
* ✅ **Quản lý Độc giả:** Xem danh sách, Chặn (Block) hoặc Mở khóa (Unblock) tài khoản thành viên.
* ✅ **Lưu thông (Circulation):**
    * **Check-out:** Mượn sách hộ thành viên tại quầy (bỏ qua giới hạn nợ xấu nếu cần thiết).
    * **Check-in:** Nhận trả sách, hệ thống tự động tính ngày quá hạn và hiển thị số tiền phạt (nếu có).
* ✅ **Giám sát:** Xem danh sách tất cả các phiếu mượn đang kích hoạt (Active Loans).

### 2. Dành cho Thành viên (Member)
* ✅ **Tìm kiếm thông minh:** Tìm sách theo Tên hoặc Năm xuất bản. Xem chi tiết số lượng tồn kho.
* ✅ **Giỏ sách (Book Bag):** Thêm sách vào giỏ với số lượng tùy chọn trước khi mượn chính thức.
* ✅ **Quản lý cá nhân:** Xem lịch sử mượn trả, Cập nhật thông tin (SĐT, Địa chỉ).
* ✅ **Quy tắc mượn:** Tự động bị chặn mượn mới nếu đang giữ sách quá hạn.

### 3. Tính năng chung
* 🔐 **Bảo mật:** Mật khẩu được mã hóa (Hash SHA-256).
* 📧 **Quên mật khẩu:** Giả lập gửi mã OTP để lấy lại mật khẩu.
* 💾 **Dữ liệu bền vững:** Tự động lưu trữ vào file `library_data.json`.

---

## 🛠️ Công nghệ sử dụng
* **Ngôn ngữ:** Python 3.9+
* **Cơ sở dữ liệu:** JSON (File-based storage)
* **Đóng gói:** Docker
* **Công cụ:** VS Code, Git

---

## ⚙️ Cài đặt và Chạy chương trình

### Cách 1: Chạy trực tiếp bằng Python (Local)

1.  **Clone dự án:**
    ```bash
    git clone [https://github.com/VDucThinh166/LIBRARY-MANAGEMENT-SYSTEM.git](https://github.com/VDucThinh166/LIBRARY-MANAGEMENT-SYSTEM.git)
    cd project-name
    ```

2.  **Chạy ứng dụng:**
    ```bash
    python main.py
    ```
    *(Lưu ý: Hệ thống sẽ tự động tạo file `library_data.json` và tài khoản Admin mặc định trong lần chạy đầu tiên).*

### Cách 2: Chạy bằng Docker 

1.  **Build Image:**
    ```bash
    docker build -t group12-lms .
    ```

2.  **Chạy Container (Có lưu dữ liệu):**
    * **Windows (PowerShell):**
        ```powershell
        docker run -it -v ${PWD}:/app group12-lms
        ```
    * **Mac / Linux / Git Bash:**
        ```bash
        docker run -it -v $(pwd):/app group12-lms
        ```