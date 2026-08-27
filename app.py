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

# 4. GIAO DIỆN MÀN HÌNH ĐĂNG NHẬP
def login_screen():
    st.markdown("""
        <style>
            .main .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
            }
            
            /* Định dạng Logo & Tiêu đề */
            .logo-container {
                text-align: center;
                margin-bottom: 20px;
            }
            .hospital-logo-img {
                width: 110px;
                height: 110px;
                object-fit: contain;
                margin-bottom: 12px;
                filter: drop-shadow(0px 4px 8px rgba(0,0,0,0.1));
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

            /* Styling cho Form */
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
            [data-testid="stForm"] input:focus {
                border-color: #0284c7 !important;
                box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.15) !important;
            }

            /* Tùy chỉnh Nút Đăng Nhập & Nút Thoát */
            div[data-testid="stFormSubmitButton"] > button {
                background: linear-gradient(135deg, #0284c7, #0369a1) !important;
                color: white !important;
                font-weight: 700 !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 10px 0px !important;
                transition: all 0.2s ease !important;
            }
            div[data-testid="stFormSubmitButton"] > button:hover {
                background: linear-gradient(135deg, #0369a1, #075985) !important;
                box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3) !important;
            }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        # LOGO VÀ TIÊU ĐỀ
        st.markdown("""
            <div class="logo-container">
                <img class="hospital-logo-img" src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Logo_VNPT.svg/1200px-Logo_VNPT.svg.png" alt="Logo VNPT Bệnh viện Bưu điện">
                <div class="login-title">BỆNH VIỆN BƯU ĐIỆN</div>
                <div class="login-subtitle">Hệ thống Quản trị Nhân sự & Điều hành</div>
            </div>
        """, unsafe_allow_html=True)
        
        # FORM ĐĂNG NHẬP
        with st.form("login_form"):
            username = st.text_input("Tên đăng nhập / Username:", value="", placeholder="Nhập tên đăng nhập...")
            password = st.text_input("Mật khẩu / Password:", type="password", value="", placeholder="Nhập mật khẩu...")
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
                        "role": "Quản trị viên Hệ thống — Bệnh viện Bưu điện",
                        "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=200&auto=format&fit=crop"
                    }
                    st.success("Đăng nhập thành công!")
                    st.rerun()
                elif username == "" or password == "":
                    st.warning("⚠️ Vui lòng nhập đầy đủ Tên đăng nhập và Mật khẩu!")
                else:
                    st.error("❌ Tên đăng nhập hoặc mật khẩu không chính xác!")

            if exit_in_form:
                st.info("Cảm ơn bạn đã sử dụng hệ thống!")
                st.stop()

# KIỂM TRA ĐĂNG NHẬP
if not st.session_state.logged_in:
    login_screen()
    st.stop()

# ---------------------------------------------------------
# GIAO DIỆN CHÍNH KHI ĐÃ ĐĂNG NHẬP THÀNH CÔNG
# ---------------------------------------------------------

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

# SIDEBAR
st.sidebar.markdown(
    f"""
    <div style="text-align: center; padding-bottom: 10px;">
        <h3 style="color: #4da6ff; margin-bottom: 2px;">DANH MỤC CHỨC NĂNG</h3>
        <p style="font-size: 13px; color: #a0aec0;">👤 Xin chào: <b>{st.session_state.user_info['name']}</b></p>
    </div>
    """,
    unsafe_allow_html=True
)

if st.sidebar.button("🚪 Đăng xuất", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.user_info = None
    st.rerun()

menu_options = [
    "Trang chủ / Dashboard",
    "Thông báo & Văn bản",
    "Hồ sơ Cán bộ CNV",
    "Phân loại Trình độ",
    "Hợp đồng Lao động",
    "Hồ sơ Đảng viên",
    "Giấy phép hành nghề (GPHN)",
    "Theo dõi Đào tạo CME",
    "Nâng bậc lương & Ngạch",
    "Bố trí & Điều chuyển",
    "Quản lý BHXH",
    "Quản lý chấm công",
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
