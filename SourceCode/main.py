import sys
from controllers import LibraryController
from models import Book

system = LibraryController()
def print_line(): print("="*60)

# --- MENUS ---
def guest_menu():
    print_line(); print("LIBRARY MANAGEMENT SYSTEM v1.0"); print_line()
    print("1. Search (Tìm kiếm)"); print("2. Login (Đăng nhập)")
    print("3. Register (Đăng ký)"); print("4. Forgot Password")
    print("5. Exit"); return input("Chọn: ")

def member_menu():
    print_line(); print(f"MEMBER: {system.current_user.fullname}"); print_line()
    print("1. Search & Browse"); print("2. My Book Bag (Giỏ sách)")
    print("3. History (Lịch sử)"); print("4. Profile")
    print("5. Logout"); return input("Chọn: ")

def librarian_menu():
    print_line(); print("ADMIN PANEL"); print_line()
    print("1. Add Book (Thêm sách)"); print("2. Manage Patrons (Chặn user)")
    print("3. Circulation: Check-out (Mượn hộ)"); print("4. Circulation: Check-in (Nhận trả)")
    print("5. Active Loans (Xem ds mượn)"); print("6. Logout")
    return input("Chọn: ")

# --- ACTIONS ---
def act_book_details(isbn):
    b = system.get_book_by_isbn(isbn)
    if not b: print("Sách không tồn tại."); return
    tot, avail = system.get_book_availability(isbn)
    
    print("\n[CHI TIẾT SÁCH]")
    print(f"Tên: {b.title} | Tác giả: {b.author}")
    print(f"Kho: {avail} / {tot} (Khả dụng/Tổng)")
    print("-" * 30)
    print("[1] Thêm vào giỏ  [2] Quay lại")
    
    if input("Chọn: ") == '1':
        if system.current_user and system.current_user.role == "Member":
            try:
                q = int(input(f"Nhập số lượng (Max {avail}): "))
                if q > 0: print(system.add_to_cart(isbn, q)[1])
                else: print("Số lượng phải > 0")
            except: print("Nhập số không hợp lệ.")
        elif not system.current_user: print("Hãy đăng nhập.")
        else: print("Admin không dùng giỏ.")

def act_search():
    while True:
        k = input("\n[SEARCH] Nhập từ khóa (Enter để thoát): ")
        if not k: break
        res = system.search_books(k, "title")
        print(f"\n{'ISBN':<8} | {'Title':<25} | {'Year':<6}")
        print("-" * 45)
        for b in res: print(f"{b.isbn:<8} | {b.title[:23]:<25} | {b.year:<6}")
        
        isbn = input("\nNhập ISBN xem chi tiết (Enter tìm tiếp): ")
        if isbn: act_book_details(isbn)

def act_manage_patrons():
    for u in system.get_all_users():
        st = "BLOCKED" if u.get("is_blocked") else "Active"
        print(f"User: {u['username']} | Name: {u['fullname']} | {st}")
    t = input("Nhập User để Chặn/Mở (Enter bỏ qua): ")
    if t: print(system.toggle_user_block(t)[1])

def main():
    while True:
        if not system.current_user:
            c = guest_menu()
            if c=='1': act_search()
            elif c=='2': 
                if system.login(input("User: "), input("Pass: ")): print("Login OK!")
                else: print("Login Fail.")
            elif c=='3':
                print(system.register(input("User: "), input("Pass: "), input("Email: "), 
                      input("Name: "), input("Phone: "), input("Addr: "), input("DOB: "), input("Gender: "))[1])
            elif c=='4':
                e=input("Email: "); ok,otp=system.forgot_pass(e)
                if ok: print(f"OTP: {otp}"); print(system.reset_pass(e, input("OTP: "), input("New Pass: "))[1])
            elif c=='5': sys.exit()
        
        elif system.current_user.role == "Member":
            c = member_menu()
            if c=='1': act_search()
            elif c=='2':
                its = system.view_cart()
                print("\n[GIỎ SÁCH]"); 
                for b,q in its: print(f"{b.title} (SL: {q})")
                opt = input("[C] Checkout  [R] Xóa  [B] Back: ").upper()
                if opt=='C': print(system.checkout_cart()[1])
                elif opt=='R': print(system.remove_from_cart(input("ISBN xóa: "))[1])
            elif c=='3': 
                for h in system.get_history(): print(h)
                input("Enter...")
            elif c=='4':
                u=system.current_user; print(f"{u.fullname} | {u.phone} | {u.address}")
                if input("Sửa? (y/n): ")=='y': print(system.update_profile(input("Phone: "), input("Addr: "))[1])
            elif c=='5': system.logout()

        elif system.current_user.role == "Librarian":
            c = librarian_menu()
            if c=='1':
                system.admin_add_book(Book(input("ISBN: "), input("Title: "), input("Author: "), "Pub", 2024, input("Qty: "), "Loc", "IT"))
            elif c=='2': act_manage_patrons()
            elif c=='3': print(system.admin_borrow_for_user(input("User: "), input("ISBN: "))[1])
            elif c=='4':
                print("\n[NHẬN TRẢ SÁCH]")
                isbn_input = input("Nhập ISBN sách trả: ")
                user_input = input("Nhập Username người trả: ")
                print(system.return_book(isbn_input, user_input)[1])
            elif c=='5': 
                for l in system.get_all_active_loans(): print(l)
                input("Enter...")
            elif c=='6': system.logout()

if __name__ == "__main__":
    main()