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
        u_clean = username.strip().lower()
        p_clean = password.strip()

        # Tài khoản Admin mặc định
        if u_clean == "admin" and p_clean == "admin123":
            st.session_state["logged_in"] = True
            st.session_state["user_id"] = "admin"
            st.session_state["user_name"] = "Quản trị viên Hệ thống"
            st.session_state["role"] = "ADMIN"
            st.session_state["khoa_phong"] = "Tất cả"
            st.success("Đăng nhập thành công!")
            st.rerun()

        # Kiểm tra CSDL
        if engine:
            try:
                with engine.connect() as conn:
                    result = conn.execute(
                        text("SELECT username, password_hash, full_name, role, khoa_phong FROM sys_users WHERE LOWER(username) = :u AND is_active = TRUE"), 
                        {"u": u_clean}
                    ).fetchone()
                    
                    if result and bcrypt.checkpw(p_clean.encode('utf-8'), result[1].encode('utf-8')):
                        st.session_state["logged_in"] = True
                        st.session_state["user_id"] = result[0]
                        st.session_state["user_name"] = result[2]
                        st.session_state["role"] = result[3]
                        st.session_state["khoa_phong"] = result[4]
                        st.rerun()
                    else:
                        st.sidebar.error("❌ Tài khoản hoặc mật khẩu không đúng!")
            except Exception as e:
                st.sidebar.error(f"Lỗi kết nối CSDL: {e}")

def check_permission(required_roles):
    current_role = st.session_state.get("role", "ESS")
    if current_role == "ADMIN" or current_role in required_roles:
        return True
    return False
