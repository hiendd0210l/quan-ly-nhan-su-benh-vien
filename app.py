import streamlit as st
import os
from sqlalchemy import create_engine

# 1. Cấu hình trang Streamlit
st.set_page_config(
    page_title="Quản trị Nhân sự Bệnh viện Bưu điện",
    page_icon="🏥",
    layout="wide"
)

# 2. Import các module
from modules.dashboard import render_dashboard
from modules.ho_so import render_ho_so

# 3. Kết nối CSDL PostgreSQL
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
st.sidebar.image("https://img.icons8.com/color/96/hospital-2.png", width=70)
st.sidebar.title("BV BƯU ĐIỆN")
st.sidebar.caption("Hệ thống Quản trị Nhân sự Y tế")

# Danh sách đầy đủ các chức năng quản trị
menu_choice = st.sidebar.radio(
    "📌 MENU QUẢN LÝ",
   # Thay đổi danh sách menu trong app.py
menu_options = [
    "📊 Dashboard Tổng quan",
    "📇 Hồ sơ Nhân sự (Thêm/Sửa/Xóa & Excel)",
    "📜 Quản lý CCHN & Đào tạo CME",
    "📝 Quản lý Hợp đồng Lao động",     # Tách riêng
    "💰 Quản lý Lương cơ bản",         # Tách riêng
    "🎯 Đánh giá KPI & Thi đua Khen thưởng",
    "🏢 Quản lý Đảng viên & Tổ chức",
    "🩺 Sức khỏe Nhân viên & BHXH",
    "⏰ Tối ưu Nhân lực & Ca trực Y tế",
    "🌱 Lộ trình Phát triển & Quy hoạch",
    "📊 Báo cáo Nhân sự & Y tế",
    "🤖 Trợ lý AI Nhân sự",
    "⚙️ Cấu hình Hệ thống"
]
)

st.sidebar.markdown("---")

# --- ĐIỀU HƯỚNG HIỂN THỊ CHỨC NĂNG ---
if menu_choice == "📊 Dashboard Tổng quan":
    render_dashboard(engine)

elif menu_choice == "📂 Hồ sơ Nhân sự (Thêm/Sửa/Xóa & Excel)":
    render_ho_so(engine)

elif menu_choice == "📜 Quản lý CCHN & Đào tạo CME":
    st.title("📜 QUẢN LÝ CỨNG CHỈ HÀNH NGHỀ (CCHN) & ĐÀO TẠO CME")
    st.info("Chức năng theo dõi thời hạn CCHN và tổng hợp giờ đào tạo liên tục (CME) tối thiểu 48h/2 năm.")

elif menu_choice == "📑 Hợp đồng Lao động & Lương":
    st.title("📑 QUẢN LÝ HỢP ĐỒNG LAO ĐỘNG & BẬC LƯƠNG")
    st.info("Chức năng quản lý loại hợp đồng, cảnh báo hết hạn hợp đồng và quá trình nâng lương viên chức.")

elif menu_choice == "⭐ Đánh giá KPI & Thi đua Khen thưởng":
    st.title("⭐ ĐÁNH GIÁ KPI & THI ĐƯA KHEN THƯỞNG")
    st.info("Chức năng chấm điểm KPI hàng tháng/quyý, xét duyệt danh hiệu Chiến sĩ thi đua, Bằng khen.")

elif menu_choice == "🏛️ Quản lý Đảng viên & Tổ chức":
    st.title("🏛️ QUẢN LÝ ĐẢNG VIÊN & TỔ CHỨC ĐẢNG")
    st.info("Chức năng theo dõi hồ sơ Đảng viên, ngày vào Đảng, sinh hoạt Đảng và phân loại chất lượng.")

elif menu_choice == "🩺 Sức khỏe Nhân viên & BHXH":
    st.title("🩺 QUẢN LÝ SỨC KHỎE NHÂN VIÊN & BHXH")
    st.info("Chức năng theo dõi khám sức khỏe định kỳ, phân loại sức khỏe, chế độ độc hại và BHXH.")

elif menu_choice == "🚑 Tối ưu Nhân lực & Ca trực Y tế":
    st.title("🚑 TỐI ƯU NHÂN LỰC & XẾP LỊCH TRỰC Y TẾ")
    st.info("Chức năng hỗ trợ phân ca, phân lịch trực cấp cứu và điều phối nhân sự giữa các khoa/phòng.")

elif menu_choice == "🎯 Lộ trình Phát triển & Quy hoạch":
    st.title("🎯 LỘ TRÌNH PHÁT TRIỂN & QUY HOẠCH CÁN BỘ")
    st.info("Chức năng quy hoạch cán bộ quản lý, lộ trình thăng tiến bác sĩ/y sĩ chuyên khoa.")

elif menu_choice == "📈 Báo cáo Nhân sự & Y tế":
    st.title("📈 BÁO CÁO THỐNG KÊ NHÂN SỰ & Y TẾ")
    st.info("Chức năng xuất báo cáo định kỳ gửi Bộ Y tế, Tập đoàn VNPT và các cơ quan quản lý.")

elif menu_choice == "🤖 Trợ lý AI Nhân sự":
    st.title("🤖 TRỢ LÝ AI HỎI ĐÁP NHÂN SỰ")
    st.info("Hỏi đáp thông minh về Luật lao động, Quy định nội bộ Bệnh viện và Tìm kiếm hồ sơ nhân sự.")

elif menu_choice == "⚙️ Cấu hình Hệ thống":
    st.title("⚙️ CẤU HÌNH HỆ THỐNG")
    st.write("Trạng thái kết nối CSDL PostgreSQL:")
    if engine:
        st.success("✅ Đã kết nối thành công với Cơ sở dữ liệu PostgreSQL!")
    else:
        st.error("❌ Chưa kết nối CSDL PostgreSQL. Vui lòng cấu hình Secrets trên Streamlit Cloud.")
