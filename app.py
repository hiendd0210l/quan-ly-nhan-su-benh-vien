import streamlit as st
import os
from sqlalchemy import create_engine

# -------------------------------------------------------------
# 1. CẤU HÌNH TRANG STREAMLIT
# -------------------------------------------------------------
st.set_page_config(
    page_title="Hệ thống Quản trị Nhân sự Y tế - BV Bưu điện",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# 2. KHỞI TẠO KẾT NỐI CƠ SỞ DỮ LIỆU POSTGRESQL (NEON)
# -------------------------------------------------------------
@st.cache_resource
def init_connection():
    try:
        # Lấy URL kết nối từ st.secrets hoặc biến môi trường
        db_url = st.secrets.get("postgres", {}).get("url") or os.environ.get("DATABASE_URL")
        if not db_url:
            st.error("⚠️ Chưa cấu hình chuỗi kết nối DATABASE_URL trong secrets!")
            return None
        
        # Sửa prefix postgres:// thành postgresql:// nếu dùng SQLAlchemy mới
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
            
        engine = create_engine(db_url, pool_pre_ping=True)
        return engine
    except Exception as e:
        st.error(f"❌ Lỗi kết nối CSDL PostgreSQL: {e}")
        return None

engine = init_connection()

# -------------------------------------------------------------
# 3. THÔNG TIN BỆNH VIỆN TRÊN SIDEBAR
# -------------------------------------------------------------
st.sidebar.markdown(
    """
    <div style="text-align: center; padding-bottom: 10px;">
        <h2 style="color: #008080; margin-bottom: 0;">🏥 BV BƯU ĐIỆN</h2>
        <p style="font-size: 13px; color: #555;">Hệ thống Quản trị Nhân sự Y tế</p>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------------------
# 4. DANH SÁCH MENU BÊN SIDEBAR (13 MỤC ĐỘC LẬP)
# -------------------------------------------------------------
menu_options = [
    "📊 Dashboard Tổng quan",
    "📇 Hồ sơ Nhân sự (Thêm/Sửa/Xóa & Excel)",
    "📜 Quản lý CCHN & Đào tạo CME",
    "📝 Quản lý Hợp đồng Lao động",
    "💰 Quản lý Lương cơ bản",
    "🎯 Đánh giá KPI & Thi đua Khen thưởng",
    "🏢 Quản lý Đảng viên & Tổ chức",
    "🩺 Sức khỏe Nhân viên & BHXH",
    "⏰ Tối ưu Nhân lực & Ca trực Y tế",
    "🌱 Lộ trình Phát triển & Quy hoạch",
    "📊 Báo cáo Nhân sự & Y tế",
    "🤖 Trợ lý AI Nhân sự",
    "⚙️ Cấu hình Hệ thống"
]

st.sidebar.markdown("---")
st.sidebar.subheader("📌 MENU QUẢN LÝ")

# Đã sửa lỗi TypeError bằng cách khai báo tham số chuẩn Streamlit
menu_choice = st.sidebar.radio(
    label="Chọn chức năng quản lý:",
    options=menu_options,
    index=0
)

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 Bệnh viện Bưu điện - Hệ thống Quản trị HR")

# -------------------------------------------------------------
# 5. ĐIỀU HƯỚNG VÀ RENDER MODULE TƯƠNG ỨNG
# -------------------------------------------------------------
if menu_choice == "📊 Dashboard Tổng quan":
    try:
        import modules.dashboard as db
        db.render_dashboard(engine)
    except Exception as e:
        st.info("📊 Module Dashboard Tổng quan đang được hoàn thiện...")

elif menu_choice == "📇 Hồ sơ Nhân sự (Thêm/Sửa/Xóa & Excel)":
    try:
        import modules.ho_so as hs
        hs.render_ho_so(engine)
    except Exception as e:
        st.error(f"❌ Lỗi tải module Hồ sơ Nhân sự: {e}")

elif menu_choice == "📜 Quản lý CCHN & Đào tạo CME":
    try:
        import modules.cchn_cme as cme
        cme.render_cme(engine)
    except Exception as e:
        st.info("📜 Module Quản lý CCHN & Đào tạo CME đang hoàn thiện...")

elif menu_choice == "📝 Quản lý Hợp đồng Lao động":
    try:
        import modules.hop_dong as hd
        hd.render_hop_dong(engine)
    except Exception as e:
        st.info("📝 Module Quản lý Hợp đồng Lao động đang hoàn thiện...")

elif menu_choice == "💰 Quản lý Lương cơ bản":
    try:
        import modules.luong as luong
        luong.render_luong(engine)
    except Exception as e:
        st.info("💰 Module Quản lý Lương cơ bản đang hoàn thiện...")

elif menu_choice == "🎯 Đánh giá KPI & Thi đua Khen thưởng":
    try:
        import modules.kpi as kpi
        kpi.render_kpi(engine)
    except Exception as e:
        st.info("🎯 Module Đánh giá KPI đang hoàn thiện...")

elif menu_choice == "🏢 Quản lý Đảng viên & Tổ chức":
    try:
        import modules.dang_vien as dv
        dv.render_dang_vien(engine)
    except Exception as e:
        st.info("🏢 Module Quản lý Đảng viên & Tổ chức đang hoàn thiện...")

elif menu_choice == "🩺 Sức khỏe Nhân viên & BHXH":
    try:
        import modules.suc_khoe as sk
        sk.render_suc_khoe(engine)
    except Exception as e:
        st.info("🩺 Module Sức khỏe Nhân viên & BHXH đang hoàn thiện...")

elif menu_choice == "⏰ Tối ưu Nhân lực & Ca trực Y tế":
    try:
        import modules.ca_truc as ct
        ct.render_ca_truc(engine)
    except Exception as e:
        st.info("⏰ Module Ca trực Y tế đang hoàn thiện...")

elif menu_choice == "🌱 Lộ trình Phát triển & Quy hoạch":
    try:
        import modules.lo_trinh as lt
        lt.render_lo_trinh(engine)
    except Exception as e:
        st.info("🌱 Module Lộ trình Phát triển đang hoàn thiện...")

elif menu_choice == "📊 Báo cáo Nhân sự & Y tế":
    try:
        import modules.bao_cao as bc
        bc.render_bao_cao(engine)
    except Exception as e:
        st.info("📊 Module Báo cáo Nhân sự đang hoàn thiện...")

elif menu_choice == "🤖 Trợ lý AI Nhân sự":
    try:
        import modules.ai_assistant as ai
        ai.render_ai_assistant(engine)
    except Exception as e:
        st.info("🤖 Module Trợ lý AI Nhân sự đang hoàn thiện...")

elif menu_choice == "⚙️ Cấu hình Hệ thống":
    try:
        import modules.cau_hinh as ch
        ch.render_cau_hinh(engine)
    except Exception as e:
        st.info("⚙️ Module Cấu hình Hệ thống đang hoàn thiện...")
