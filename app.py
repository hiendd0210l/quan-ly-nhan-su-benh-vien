import streamlit as st
from modules.database import get_db_engine, init_db
from modules.auth import login_form, check_permission
from modules.dashboard import render_dashboard
from modules.cham_cong_truc import render_cham_cong_truc
from modules.cchn import render_cchn
from modules.bao_cao import render_bao_cao
import pandas as pd
from sqlalchemy import text

st.set_page_config(
    page_title="HRMS - Bệnh viện Bưu điện",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1. Khởi tạo CSDL
engine = get_db_engine()
if engine:
    init_db(engine)

# 2. Đăng nhập
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    login_form(engine)
    st.info("👋 Vui lòng đăng nhập từ thanh Sidebar bên trái để sử dụng hệ thống!")
    st.stop()

# 3. Sidebar Menu 18 Chức năng & Cổng ESS/MSS
st.sidebar.title(f"🏥 BV BƯU ĐIỆN")
st.sidebar.caption(f"👤 {st.session_state.get('user_name')} | Vai trò: {st.session_state.get('role')}")

if st.sidebar.button("🚪 Đăng xuất"):
    st.session_state.clear()
    st.rerun()

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "DANH MỤC QUẢN TRỊ (18 MENU)",
    [
        "1. Dashboard Tổng quan",
        "2. Danh mục hệ thống",
        "3. Cơ cấu tổ chức",
        "4. Hồ sơ nhân sự (Mẫu 2C)",
        "5. Tuyển dụng & Thử việc",
        "6. Hợp đồng lao động",
        "7. Điều động - Bổ nhiệm",
        "8. Chấm công - Ca trực",
        "9. Tiền lương & Phụ cấp Y tế",
        "10. Đánh giá KPI Chuyên môn",
        "11. Đào tạo & Giờ CME",
        "12. Chứng chỉ hành nghề (CCHN)",
        "13. Thi đua - Khen thưởng",
        "14. Quản lý Nghỉ phép (ESS/MSS)",
        "15. Sức khỏe & Phơi nhiễm",
        "16. Văn bản - Quyết định",
        "17. Báo cáo thống kê (BYT/BHXH)",
        "18. Quản trị hệ thống & Phân quyền"
    ]
)

# 4. Điều hướng Menu
if menu.startswith("1."):
    render_dashboard(engine)
elif menu.startswith("8."):
    render_cham_cong_truc(engine)
elif menu.startswith("12."):
    render_cchn(engine)
elif menu.startswith("17."):
    render_bao_cao(engine)
elif menu.startswith("4."):
    st.title("📂 QUẢN LÝ HỒ SƠ NHÂN SỰ 360° (MẪU 2C-BNV)")
    if engine:
        df = pd.read_sql("SELECT * FROM nhan_su", engine)
        st.dataframe(df, use_container_width=True)
else:
    st.title(f"⚙️ CHỨC NĂNG: {menu}")
    st.info("Chức năng đang được kết nối dữ liệu thời gian thực cho quy mô 1.500 nhân sự Bệnh viện Bưu điện.")
