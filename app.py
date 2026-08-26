import streamlit as st

# Nạp các module chức năng từ thư mục modules
from modules.database import get_db_engine, init_db
from modules.dashboard import render_dashboard
from modules.ho_so import render_ho_so
from modules.nhap_excel import render_nhap_excel

# 1. Cấu hình trang
st.set_page_config(
    page_title="HRMS - Bệnh viện Bưu điện",
    page_icon="🏥",
    layout="wide"
)

# 2. Khởi tạo CSDL
engine = get_db_engine()
init_db(engine)

# 3. Thanh điều hướng
st.sidebar.markdown("<h2 style='text-align: center; color: #0056b3;'>🏥 BỆNH VIỆN BƯU ĐIỆN</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; font-weight: bold;'>HỆ THỐNG QUẢN TRỊ NHÂN SỰ (HRMS)</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

menu = st.sidebar.radio("DANH MỤC CHỨC NĂNG", [
    "📊 Dashboard Tổng quan",
    "👥 Hồ sơ Nhân sự & Chỉnh sửa",
    "➕ Thêm mới & Nhập Excel (Mẫu 2C)",
    "📜 Quản lý CCHN & CME",
    "📝 Quản lý Hợp đồng & Lương",
    "🏛️ Đảng & Đoàn thể"
])

# 4. Điều hướng ứng dụng chạy từng Module tương ứng
if menu == "📊 Dashboard Tổng quan":
    render_dashboard(engine)

elif menu == "👥 Hồ sơ Nhân sự & Chỉnh sửa":
    render_ho_so(engine)

elif menu == "➕ Thêm mới & Nhập Excel (Mẫu 2C)":
    render_nhap_excel(engine)

elif menu == "📜 Quản lý CCHN & CME":
    st.title("📜 QUẢN LÝ CCHN & CME")
    st.info("📌 Phân hệ này đã có vị trí sẵn. Lần tới nâng cấp, bạn chỉ cần tạo file `modules/cchn_cme.py` mà không ảnh hưởng tới `app.py`!")

elif menu == "📝 Quản lý Hợp đồng & Lương":
    st.title("📝 QUẢN LÝ HỢP ĐỒNG & LƯƠNG")
    st.info("📌 Phân hệ này đã có vị trí sẵn.")

elif menu == "🏛️ Đảng & Đoàn thể":
    st.title("🏛️ QUẢN LÝ ĐẢNG & ĐOÀN THỂ")
    st.info("📌 Phân hệ này đã có vị trí sẵn.")
