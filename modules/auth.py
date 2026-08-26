import streamlit as st
from sqlalchemy import text
import bcrypt

ROLES = {
    "ADMIN": "Quản trị hệ thống (CNTT)",
    "HR": "Phòng Tổ chức cán bộ / HR",
    "BGD": "Ban Giám đốc",
    "TRUONG_KHOA": "Trưởng khoa / Trưởng phòng",
    "DIEU_DUONG_TRUONG": "Điều dưỡng trưởng",
    "KE_TOAN": "Phòng Tài chính - Kế toán",
    "DAO_TAO": "Phòng Đào tạo / CME",
    "QLCL": "Phòng Quản lý chất lượng",
    "ESS": "Nhân viên (Cổng ESS)"
}

def login_form(engine):
    st.sidebar.title("🔐 ĐĂNG NHẬP HỆ THỐNG")
    username = st.sidebar.text_input("Tên đăng nhập")
    password = st.sidebar.text_input("Mật khẩu", type="password")
    
    if st.sidebar.button("Đăng nhập"):
        if not username or not password:
            st.sidebar.error("Vui lòng nhập đầy đủ thông tin!")
            return False
            
        # Tài khoản Administrator mặc định khởi tạo ban đầu
        if username == "admin" and password == "admin123":
            st.session_state["logged_in"] = True
            st.session_state["user_id"] = "admin"
            st.session_state["user_name"] = "Quản trị viên Hệ thống"
            st.session_state["role"] = "ADMIN"
            st.session_state["khoa_phong"] = "Tất cả"
            st.sidebar.success("Đăng nhập thành công!")
            st.rerun()

        with engine.connect() as conn:
            result = conn.execute(text("SELECT username, password_hash, full_name, role, khoa_phong, ma_nv FROM sys_users WHERE username = :u AND is_active = TRUE"), {"u": username}).fetchone()
            if result and bcrypt.checkpw(password.encode('utf-8'), result[1].encode('utf-8')):
                st.session_state["logged_in"] = True
                st.session_state["user_id"] = result[0]
                st.session_state["user_name"] = result[2]
                st.session_state["role"] = result[3]
                st.session_state["khoa_phong"] = result[4]
                st.session_state["ma_nv"] = result[5]
                st.rerun()
            else:
                st.sidebar.error("Tài khoản hoặc mật khẩu không chính xác!")
    return False

def check_permission(required_roles):
    current_role = st.session_state.get("role", "ESS")
    if current_role == "ADMIN" or current_role in required_roles:
        return True
    return False
