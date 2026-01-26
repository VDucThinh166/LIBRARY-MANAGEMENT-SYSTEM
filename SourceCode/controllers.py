# Mục đích: Xử lý toàn bộ logic nghiệp vụ (Business Logic)
import hashlib
import random
from datetime import datetime, timedelta
from database import load_data, save_data
from models import User, Book

class LibraryController:
    def __init__(self):
        self.current_user = None
        self.data = load_data()
        self.otp_storage = {}
        self.cart = {}  # Dictionary {isbn: so_luong}

    def _save(self):
        save_data(self.data)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # --- 1. AUTH & REGISTER ---
    def login(self, username, password):
        hashed_pw = self.hash_password(password)
        for u in self.data["users"]:
            if u["username"] == username and u["password"] == hashed_pw:
                if u.get("is_blocked", False):
                    print("❌ TÀI KHOẢN BỊ CHẶN (BLOCKED). Liên hệ Admin.")
                    return False
                
                # Load User với đầy đủ tham số (Fix lỗi 8 arguments)
                self.current_user = User(
                    u["account_id"], u["username"], u["email"], u["fullname"], 
                    u["role"], u.get("phone",""), u.get("address",""), 
                    u.get("dob",""), u.get("gender",""), u.get("is_blocked", False)
                )
                self.cart = {} # Reset giỏ khi login mới
                return True
        return False

    def logout(self):
        self.current_user = None
        self.cart = {}

    def register(self, username, password, email, fullname, phone, address, dob, gender):
        for u in self.data["users"]:
            if u["username"] == username: return False, "Username đã tồn tại!"
        
        new_user = {
            "account_id": len(self.data["users"]) + 1,
            "username": username,
            "password": self.hash_password(password),
            "email": email,
            "fullname": fullname,
            "role": "Member",
            "phone": phone, "address": address, "dob": dob, "gender": gender,
            "is_blocked": False
        }
        self.data["users"].append(new_user)
        self._save()
        return True, "Đăng ký thành công!"

    # --- 2. SEARCH & CART (NÂNG CAO) ---
    def search_books(self, keyword="", sort_by="title"):
        keyword = keyword.lower()
        results = []
        for b in self.data["books"]:
            if keyword in b["title"].lower() or keyword in b["author"].lower():
                results.append(Book(b["isbn"], b["title"], b["author"], b["publisher"], 
                                    b["year"], b["quantity"], b["location"], b.get("category", "General")))
        
        if sort_by == "title": results.sort(key=lambda x: x.title)
        elif sort_by == "year": results.sort(key=lambda x: x.year, reverse=True)
        return results

    def get_book_by_isbn(self, isbn):
        """Lấy object sách theo ISBN"""
        b = next((b for b in self.data["books"] if b["isbn"] == isbn), None)
        if b:
            return Book(b["isbn"], b["title"], b["author"], b["publisher"], 
                        b["year"], b["quantity"], b["location"], b.get("category", "General"))
        return None

    def get_book_availability(self, isbn):
        """Tính tổng số và số khả dụng"""
        book = next((b for b in self.data["books"] if b["isbn"] == isbn), None)
        if not book: return 0, 0
        available = book["quantity"]
        # Đếm sách đang cho mượn
        borrowed = sum(1 for l in self.data["loans"] if l["isbn"] == isbn and l["status"] in ["Active", "Overdue"])
        total = available + borrowed
        return total, available

    def add_to_cart(self, isbn, qty=1):
        """Thêm vào giỏ với số lượng"""
        book = next((b for b in self.data["books"] if b["isbn"] == isbn), None)
        if not book: return False, "Sách không tồn tại."
        
        current_in_cart = self.cart.get(isbn, 0)
        if book["quantity"] < (current_in_cart + qty):
            return False, f"Kho không đủ hàng (Còn {book['quantity']} cuốn)."
        
        self.cart[isbn] = current_in_cart + qty
        return True, f"Đã thêm {qty} cuốn '{book['title']}' vào giỏ."

    def view_cart(self):
        """Trả về danh sách (Sách, Số lượng)"""
        items = []
        for isbn, q in self.cart.items():
            b = self.get_book_by_isbn(isbn)
            if b: items.append((b, q))
        return items

    def remove_from_cart(self, isbn):
        if isbn in self.cart:
            del self.cart[isbn]
            return True, "Đã xóa khỏi giỏ."
        return False, "Không có trong giỏ."

    def checkout_cart(self):
        """Mượn tất cả trong giỏ"""
        if not self.cart: return False, "Giỏ trống."
        msgs = []
        for isbn, qty in list(self.cart.items()):
            for _ in range(qty): # Mượn n lần
                ok, msg = self.borrow_book(isbn)
                msgs.append(msg)
                if not ok: break
            if ok: del self.cart[isbn]
        return True, "\n".join(msgs)

    # --- 3. MƯỢN TRẢ & ADMIN ---
    def borrow_book(self, isbn):
        # Check nợ xấu
        for l in self.data["loans"]:
            if l["username"] == self.current_user.username and l["status"] == "Overdue":
                return False, "BỊ CHẶN: Bạn có sách quá hạn chưa trả!"

        target = next((b for b in self.data["books"] if b["isbn"] == isbn), None)
        if not target or target["quantity"] < 1: return False, "Hết hàng."

        loan = {
            "username": self.current_user.username, "isbn": isbn,
            "issue_date": str(datetime.now().date()),
            "due_date": str((datetime.now() + timedelta(days=14)).date()),
            "status": "Active"
        }
        target["quantity"] -= 1
        self.data["loans"].append(loan)
        self._save()
        return True, f"Mượn thành công. Hạn trả: {loan['due_date']}"

    def return_book(self, isbn, username=None):
        target = None
        # TRƯỜNG HỢP 1: ADMIN TRẢ SÁCH GIÙM
        if self.current_user.role == "Librarian":
            if not username: 
                return False, "⚠️ Lỗi: Admin phải nhập Username của người trả sách."
            # Tìm phiếu mượn khớp cả ISBN lẫn USERNAME
            target = next((l for l in self.data["loans"] 
                           if l["isbn"] == isbn 
                           and l["username"] == username  # <--- Điều kiện quan trọng
                           and l["status"] in ["Active", "Overdue"]), None)
        # TRƯỜNG HỢP 2: MEMBER TỰ TRẢ SÁCH
        else:
            target = next((l for l in self.data["loans"] 
                           if l["username"] == self.current_user.username 
                           and l["isbn"] == isbn 
                           and l["status"] in ["Active", "Overdue"]), None)
        
        if not target: return False, "❌ Không tìm thấy phiếu mượn hợp lệ."

        # --- Tính toán phạt ---
        due = datetime.strptime(target["due_date"], "%Y-%m-%d").date()
        today = datetime.now().date()
        late = (today - due).days
        
        msg = f"Đã trả sách '{target['isbn']}' của user '{target['username']}'."
        
        if late > 7: msg += f" 🔴 TRỄ {late} NGÀY! PHẠT: {late*5000} VNĐ."
        elif late > 3: msg += f" 🟡 CẢNH BÁO: Trễ {late} ngày."

        bk = next((b for b in self.data["books"] if b["isbn"]==isbn), None)
        if bk: bk["quantity"] += 1
        
        target["status"] = "Returned"
        target["return_date"] = str(today)
        self._save()
        return True, msg

    def admin_borrow_for_user(self, username, isbn):
        """Admin mượn hộ"""
        u = next((x for x in self.data["users"] if x["username"]==username), None)
        if not u: return False, "User không tồn tại."
        if u.get("is_blocked"): return False, "User bị CHẶN."
        
        bk = next((b for b in self.data["books"] if b["isbn"]==isbn), None)
        if not bk or bk["quantity"] < 1: return False, "Hết hàng."

        loan = {
            "username": username, "isbn": isbn,
            "issue_date": str(datetime.now().date()),
            "due_date": str((datetime.now()+timedelta(days=14)).date()),
            "status": "Active"
        }
        bk["quantity"] -= 1
        self.data["loans"].append(loan)
        self._save()
        return True, f"Admin đã mượn hộ cho {username}."

    def toggle_user_block(self, username):
        for u in self.data["users"]:
            if u["username"] == username:
                u["is_blocked"] = not u.get("is_blocked", False)
                st = "BLOCKED" if u["is_blocked"] else "ACTIVE"
                self._save()
                return True, f"User {username} -> {st}"
        return False, "Không tìm thấy User."

    # --- 4. UTILS ---
    def get_all_users(self): return [u for u in self.data["users"] if u["role"]=="Member"]
    def get_all_active_loans(self):
        res = []
        for l in self.data["loans"]:
            if l["status"] in ["Active", "Overdue"]:
                res.append(l)
        return res
    def get_history(self): return [l for l in self.data["loans"] if l["username"]==self.current_user.username][::-1]
    def update_profile(self, ph, ad):
        for u in self.data["users"]:
            if u["username"]==self.current_user.username:
                u["phone"]=ph; u["address"]=ad; self.current_user.phone=ph; self.current_user.address=ad
                self._save(); return True, "Đã cập nhật."
        return False, "Lỗi."
    def forgot_pass(self, email):
        if any(u["email"]==email for u in self.data["users"]):
            otp = str(random.randint(100000,999999))
            self.otp_storage[email]=otp; return True, otp
        return False, "Email không có."
    def reset_pass(self, email, otp, newp):
        if self.otp_storage.get(email)==otp:
            for u in self.data["users"]:
                if u["email"]==email: u["password"]=self.hash_password(newp); self._save(); return True, "Done."
        return False, "Sai OTP."
    def admin_add_book(self, b): self.data["books"].append(b.__dict__); self._save(); return True, "Added."