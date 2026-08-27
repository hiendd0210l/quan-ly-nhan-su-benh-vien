import streamlit as st
import os
from sqlalchemy import create_engine

# 1. CẤU HÌNH TRANG STREAMLIT
st.set_page_config(
    page_title="Hệ thống Quản lý Nhân sự Bệnh viện Bưu điện",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. KHỞI TẠO SESSION STATE ĐĂNG NHẬP
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_info" not in st.session_state:
    st.session_state.user_info = None

# 3. KẾT NỐI CSDL POSTGRESQL (NEON)
@st.cache_resource
def init_connection():
    try:
        db_url = st.secrets.get("postgres", {}).get("url") or os.environ.get("DATABASE_URL")
        if not db_url:
            return None
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        return create_engine(db_url, pool_pre_ping=True)
    except Exception as e:
        st.error(f"❌ Lỗi kết nối CSDL PostgreSQL: {e}")
        return None

engine = init_connection()

# 4. HÀM XỬ LÝ ĐĂNG NHẬP
def login_screen():
    st.markdown("""
        <style>
            .login-box {
                max-width: 420px;
                margin: 50px auto;
                padding: 30px;
                background-color: #ffffff;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                border: 1px solid #e0e0e0;
            }
            .login-title {
                text-align: center;
                color: #0d47a1;
                font-weight: 700;
                margin-bottom: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h2 class='login-title'>🏥 BỆNH VIỆN BƯU ĐIỆN</h2>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #555;'>Đăng nhập Hệ thống Quản trị Nhân sự</h4><br>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Tên đăng nhập / Username:", value="admin")
            password = st.text_input("Mật khẩu / Password:", type="password", value="admin123")
            submit_button = st.form_submit_button("Đăng nhập", use_container_width=True)

            if submit_button:
                # Kiểm tra thông tin đăng nhập mặc định
                if username == "admin" and password == "admin123":
                    st.session_state.logged_in = True
                    st.session_state.user_info = {
                        "name": "admin",
                        "role": "Quản trị viên Hệ thống — Bệnh viện Bưu điện",
                        "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=200&auto=format&fit=crop" # Ảnh đại diện cá nhân mới
                    }
                    st.success("Đăng nhập thành công!")
                    st.rerun()
                else:
                    st.error("❌ Tên đăng nhập hoặc mật khẩu không chính xác!")

# NẾU CHƯA ĐĂNG NHẬP -> HIỂN THỊ MÀN HÌNH ĐĂNG NHẬP
if not st.session_state.logged_in:
    login_screen()
    st.stop()

# ---------------------------------------------------------
# GIAO DIỆN CHÍNH KHI ĐÃ ĐĂNG NHẬP THÀNH CÔNG
# ---------------------------------------------------------

# TÙY CHỈNH THEME SIDEBAR TỐI MÀU
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #2b303b !important;
        }
        [data-testid="stSidebar"] * {
            color: #d1d5db !important;
        }
        [data-testid="stSidebar"] .stRadio label:hover {
            color: #ffffff !important;
        }
    </style>
""", unsafe_allow_html=True)

# GIAO DIỆN BÊN SIDEBAR
st.sidebar.markdown(
    f"""
    <div style="text-align: center; padding-bottom: 10px;">
        <h3 style="color: #4da6ff; margin-bottom: 2px;">DANH MỤC CHỨC NĂNG</h3>
        <p style="font-size: 13px; color: #a0aec0;">👤 Xin chào: <b>{st.session_state.user_info['name']}</b></p>
    </div>
    """,
    unsafe_allow_html=True
)

# Thêm nút Đăng xuất ở Sidebar
if st.sidebar.button("🚪 Đăng xuất", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.user_info = None
    st.rerun()

menu_options = [
    # CHUNG & ĐIỀU HÀNH
    "Trang chủ / Dashboard",
    "Thông báo & Văn bản",
    
    # QUẢN LÝ HỒ SƠ NHÂN SỰ
    "Hồ sơ Cán bộ CNV",
    "Phân loại Trình độ",
    "Hợp đồng Lao động",
    "Hồ sơ Đảng viên",
    
    # NGHIỆP VỤ CHUYÊN SÂU
    "Giấy phép hành nghề (GPHN)",
    "Theo dõi Đào tạo CME",
    "Nâng bậc lương & Ngạch",
    "Bố trí & Điều chuyển",
    "Quản lý BHXH",
    "Quản lý chấm công",
    
    # BÁO CÁO & THỐNG KÊ
    "Báo cáo - Thống kê",
    "Thống kê Biến động NS",
    "Cấu hình Hệ thống"
]

st.sidebar.markdown("---")
menu_choice = st.sidebar.radio(
    label="Điều hướng chức năng:",
    options=menu_options,
    index=0
)

# ĐIỀU HƯỚNG MODULE
if menu_choice == "Trang chủ / Dashboard":
    import modules.dashboard as db
    # Truyền thông tin người dùng đã đăng nhập vào Dashboard
    db.render_dashboard(engine, user_info=st.session_state.user_info)

elif menu_choice == "Hồ sơ Cán bộ CNV":
    import modules.ho_so as hs
    hs.render_ho_so(engine)

elif menu_choice == "Hợp đồng Lao động":
    import modules.hop_dong as hd
    hd.render_hop_dong(engine)

elif menu_choice == "Nâng bậc lương & Ngạch":
    import modules.luong as luong
    luong.render_luong(engine)

elif menu_choice == "Quản lý BHXH":
    try:
        import modules.bhxh as bh
        bh.render_bhxh(engine)
    except Exception as e:
        st.title("🩺 Quản lý Bảo hiểm xã hội (BHXH)")
        st.info("Chức năng đang kết nối CSDL và hoàn thiện giao diện...")

elif menu_choice == "Quản lý chấm công":
    try:
        import modules.cham_cong as cc
        cc.render_cham_cong(engine)
    except Exception as e:
        st.title("⏰ Quản lý Chấm công & Tăng ca")
        st.info("Chức năng đang kết nối CSDL và hoàn thiện giao diện...")

elif menu_choice == "Báo cáo - Thống kê":
    try:
        import modules.bao_cao as bc
        bc.render_bao_cao(engine)
    except Exception as e:
        st.title("📊 Báo cáo - Thống kê")
        st.info("Chức năng đang kết nối dữ liệu báo cáo chi tiết...")

else:
    st.title(f"📌 {menu_choice}")
    st.info("Chức năng đang trong quá trình kết nối dữ liệu chi tiết...")
