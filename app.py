import streamlit as st
import os
from sqlalchemy import create_engine

# Thiết lập cấu hình trang Streamlit
st.set_page_config(
    page_title="Quản trị Nhân sự Bệnh viện Bưu điện",
    page_icon="🏥",
    layout="wide"
)

# Import các modules chức năng
from modules.dashboard import render_dashboard
from modules.ho_so import render_ho_so

# Kết nối Cơ sở dữ liệu PostgreSQL
@st.cache_resource
def get_db_engine():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url and "postgres" in st.secrets:
        db_url = st.secrets["postgres"]["url"]
    
    if db_url:
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        return create_engine(db_url)
    return None

engine = get_db_engine()

# --- THANH MENU BÊN TRÁI (SIDEBAR) ---
st.sidebar.image("https://img.icons8.com/color/96/hospital-2.png", width=80)
st.sidebar.title("BV BƯU ĐIỆN")
st.sidebar.caption("Hệ thống Quản trị Nhân sự Y tế")

# Định nghĩa các mục Menu
menu_choice = st.sidebar.radio(
    "📌 MENU QUẢN LÝ",
    [
        "📊 Dashboard Tổng quan",
        "📂 Hồ sơ Nhân sự (Thêm/Sửa/Xóa & Import Excel)",
        "⚙️ Cấu hình Hệ thống"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Hướng dẫn:** Vào mục **📂 Hồ sơ Nhân sự** để dùng chức năng Tải Excel mẫu, Upload CSDL, Thêm/Sửa/Xóa nhân sự.")

# --- ĐIỀU HƯỚNG HIỂN THỊ CHỨC NĂNG ---
if menu_choice == "📊 Dashboard Tổng quan":
    render_dashboard(engine)

elif menu_choice == "📂 Hồ sơ Nhân sự (Thêm/Sửa/Xóa & Import Excel)":
    render_ho_so(engine)

elif menu_choice == "⚙️ Cấu hình Hệ thống":
    st.title("⚙️ CẤU HÌNH HỆ THỐNG")
    st.write("Trạng thái kết nối CSDL PostgreSQL:")
    if engine:
        st.success("✅ Đã kết nối thành công với Cơ sở dữ liệu PostgreSQL!")
    else:
        st.error("❌ Chưa kết nối CSDL PostgreSQL. Vui lòng cấu hình Secrets trên Streamlit Cloud.")
