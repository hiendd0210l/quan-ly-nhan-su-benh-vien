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

# 2. KHỞI TẠO SESSION STATE
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_info" not in st.session_state:
    st.session_state.user_info = None

# 3. KẾT NỐI CSDL POSTGRESQL
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
        return None

engine = init_connection()

# LOGO BỆNH VIỆN BƯU ĐIỆN
LOGO_BASE64 = "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'><circle cx='100' cy='100' r='96' fill='%23006cb7'/><circle cx='100' cy='100' r='66' fill='%23ffffff'/><path id='arc' d='M 28,100 A 72,72 0 1,1 172,100' fill='none'/><text fill='%23ffffff' font-size='14.5' font-weight='bold' font-family='Arial, sans-serif'><textPath href='%23arc' startOffset='50%' text-anchor='middle'>BỆNH VIỆN BƯU ĐIỆN</textPath></text><path d='M 25 93 L 27.5 99 L 34 99 L 28.5 103 L 30.5 109 L 25 105 L 19.5 109 L 21.5 103 L 16 99 L 22.5 99 Z' fill='%23ffffff'/><path d='M 175 93 L 177.5 99 L 184 99 L 178.5 103 L 180.5 109 L 175 105 L 169.5 109 L 171.5 103 L 166 99 L 172.5 99 Z' fill='%23ffffff'/><text x='100' y='180' fill='%23ffffff' font-size='22' font-weight='900' font-family='Arial, sans-serif' text-anchor='middle' letter-spacing='4'>VNPT</text><rect x='87' y='72' width='26' height='56' rx='3' fill='%23e30613'/><rect x='72' y='87' width='56' height='26' rx='3' fill='%23e30613'/><path d='M 40,105 C 55,148 100,164 100,164 C 100,164 78,142 60,128 C 48,118 42,108 40,105 Z' fill='%236bbd45'/><path d='M 160,105 C 145,148 100,164 100,164 C 100,164 122,142 140,128 C 152,118 158,108 160,105 Z' fill='%236bbd45'/><path d='M 60,128 C 75,145 100,164 100,164 C 100,164 85,138 72,128 Z' fill='%236bbd45'/><path d='M 140,128 C 125,145 100,164 100,164 C 100,164 115,138 128,128 Z' fill='%236bbd45'/></svg>"

# 4. MÀN HÌNH ĐĂNG NHẬP CHUẨN GIAO DIỆN CŨ
def login_screen():
    st.markdown("""
        <style>
            .main .block-container {
                padding-top: 3rem;
                padding-bottom: 2rem;
            }
            .logo-container {
                text-align: center;
                margin-bottom: 15px;
            }
            .hospital-logo-img {
                width: 130px;
                height: 130px;
                object-fit: contain;
                margin-bottom: 10px;
                filter: drop-shadow(0px 4px 8px rgba(0, 0, 0, 0.12));
            }
            .login-title {
                text-align: center;
                color: #0056b3;
                font-size: 24px;
                font-weight: 800;
                margin-bottom: 4px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            .login-subtitle {
                text-align: center;
                color: #64748b;
                font-size: 14px;
                margin-bottom: 20px;
                font-weight: 500;
            }

            [data-testid="stForm"] {
                background: linear-gradient(145deg, #ffffff, #f8fafc);
                padding: 30px 25px;
                border-radius: 16px;
                box-shadow: 0 10px 25px rgba(13, 71, 161, 0.08);
                border: 1px solid #e2e8f0;
            }
            [data-testid="stForm"] label {
                color: #1e293b !important;
                font-weight: 600 !important;
                font-size: 14px !important;
            }
            [data-testid="stForm"] input {
                background-color: #ffffff !important;
                border: 1.5px solid #cbd5e1 !important;
                border-radius: 8px !important;
                color: #0f172a !important;
                padding: 10px 14px !important;
            }

            div[data-testid="stFormSubmitButton"] > button {
                background: linear-gradient(135deg, #0284c7, #0369a1) !important;
                color: white !important;
                font-weight: 700 !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 10px 0px !important;
                transition: all 0.2s ease !important;
            }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown(f"""
            <div class="logo-container">
                <img class="hospital-logo-img" src="{LOGO_BASE64}" alt="Logo Bệnh viện Bưu điện">
                <div class="login-title">BỆNH VIỆN BƯU ĐIỆN</div>
                <div class="login-subtitle">Hệ thống Quản trị Nhân sự & Điều hành</div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Tên đăng nhập / Username:", value="admin", placeholder="Nhập tên đăng nhập...")
            password = st.text_input("Mật khẩu / Password:", type="password", value="admin123", placeholder="Nhập mật khẩu...")
            st.markdown("<br>", unsafe_allow_html=True)

            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                submit_button = st.form_submit_button("🔑 Đăng nhập", use_container_width=True)
            with btn_col2:
                exit_in_form = st.form_submit_button("❌ Thoát", use_container_width=True)

            if submit_button:
                if username == "admin" and password == "admin123":
                    st.session_state.logged_in = True
                    st.session_state.user_info = {
                        "name": "admin",
                        "fullname": "Đoàn Danh Hiển",
                        "role": "Quản trị viên Hệ thống — Bệnh viện Bưu điện",
                        # Trỏ trực tiếp tới file ảnh upload trên Repo GitHub
                        "avatar_path": "doan_danh_hien.jpg" if os.path.exists("doan_danh_hien.jpg") else "assets/doan_danh_hien.jpg"
                    }
                    st.success("Đăng nhập thành công!")
                    st.rerun()
                else:
                    st.error("❌ Tên đăng nhập hoặc mật khẩu không chính xác!")

            if exit_in_form:
                st.info("Cảm ơn bạn đã sử dụng hệ thống!")
                st.stop()

if not st.session_state.logged_in:
    login_screen()
    st.stop()

# 5. GIAO DIỆN CHÍNH
st.markdown("""
    <style>
        [data-testid="stSidebar"] { background-color: #2b303b !important; }
        [data-testid="stSidebar"] * { color: #d1d5db !important; }
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown(
    f"""
    <div style="text-align: center; padding-bottom: 10px;">
        <h3 style="color: #4da6ff; margin-bottom: 2px;">DANH MỤC CHỨC NĂNG</h3>
        <p style="font-size: 13px; color: #a0aec0;">👤 Xin chào: <b>{st.session_state.user_info['fullname']}</b></p>
    </div>
    """,
    unsafe_allow_html=True
)

if st.sidebar.button("🚪 Đăng xuất", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.user_info = None
    st.rerun()

menu_options = [
    "Trang chủ / Dashboard", "Thông báo & Văn bản", "Hồ sơ Cán bộ CNV", 
    "Phân loại Trình độ", "Hợp đồng Lao động", "Hồ sơ Đảng viên", 
    "Giấy phép hành nghề (GPHN)", "Theo dõi Đào tạo CME", "Nâng bậc lương & Ngạch", 
    "Bố trí & Điều chuyển", "Quản lý BHXH", "Quản lý chấm công", 
    "Báo cáo - Thống kê", "Thống kê Biến động NS", "Cấu hình Hệ thống"
]

st.sidebar.markdown("---")
menu_choice = st.sidebar.radio("Điều hướng chức năng:", options=menu_options, index=0)

if menu_choice == "Trang chủ / Dashboard":
    import modules.dashboard as db
    db.render_dashboard(engine, user_info=st.session_state.user_info)
elif menu_choice == "Cấu hình Hệ thống":
    import modules.cau_hinh as ch
    ch.render_cau_hinh(engine)
else:
    st.title(f"📌 {menu_choice}")
    st.info("Chức năng đang trong quá trình kết nối dữ liệu chi tiết...")
