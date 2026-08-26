import streamlit as st
import pandas as pd
import datetime
from sqlalchemy import create_engine, text

# ==============================================================================
# 1. KHỞI TẠO VÀ CẤU HÌNH CƠ SỞ DỮ LIỆU (POSTGRESQL - NEON.TECH)
# ==============================================================================

@st.cache_resource
def get_db_engine():
    try:
        if "postgres" in st.secrets and "url" in st.secrets["postgres"]:
            db_url = st.secrets["postgres"]["url"]
            if db_url.startswith("postgres://"):
                db_url = db_url.replace("postgres://", "postgresql://", 1)
            return create_engine(db_url)
        else:
            st.error("⚠️ Chưa cấu hình chuỗi kết nối trong mục Secrets trên Streamlit Cloud!")
            return None
    except Exception as e:
        st.error(f"⚠️ Lỗi kết nối CSDL: {e}")
        return None

engine = get_db_engine()

def init_db():
    """Khởi tạo các bảng dữ liệu nếu chưa tồn tại"""
    if engine:
        try:
            with engine.begin() as conn:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS nhan_su (
                        ma_nv VARCHAR(50) PRIMARY KEY,
                        ho_ten VARCHAR(100) NOT NULL,
                        phong_ban VARCHAR(100),
                        khoi VARCHAR(100),
                        chuc_vu VARCHAR(100),
                        trinh_do VARCHAR(100),
                        chuyen_mon VARCHAR(100),
                        loai_hop_dong VARCHAR(100),
                        ngay_het_han_hd DATE,
                        bac_luong VARCHAR(50),
                        ngay_nang_luong DATE,
                        tiet_cme INTEGER DEFAULT 0,
                        so_cchn VARCHAR(100),
                        ngay_het_han_cchn DATE,
                        ngay_sinh DATE,
                        is_dang_vien INTEGER DEFAULT 0,
                        trang_thai VARCHAR(50) DEFAULT 'Đang làm việc'
                    );
                """))
        except Exception as e:
            st.error(f"Lỗi khởi tạo bảng: {e}")

init_db()

# ==============================================================================
# 2. CẤU HÌNH TRANG WEB & GIAO DIỆN
# ==============================================================================

st.set_page_config(
    page_title="HRMS - Bệnh viện Bưu điện",
    page_icon="🏥",
    layout="wide"
)

st.sidebar.title("🏥 BỆNH VIỆN BƯU ĐIỆN")
st.sidebar.subheader("Quản lý Nhân sự")

menu = st.sidebar.radio("Chức năng", [
    "📊 Dashboard Tổng quan",
    "👥 Danh sách Nhân viên",
    "➕ Thêm mới Nhân viên"
])

# ==============================================================================
# 3. XỬ LÝ CÁC TRANG CHỨC NĂNG
# ==============================================================================

if menu == "📊 Dashboard Tổng quan":
    st.title("📊 DASHBOARD QUẢN LÝ NHÂN SỰ")
    st.markdown("---")
    
    if engine:
        try:
            df = pd.read_sql("SELECT * FROM nhan_su", engine)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Tổng số nhân sự", len(df))
            col2.metric("Đang làm việc", len(df[df['trang_thai'] == 'Đang làm việc']) if not df.empty else 0)
            col3.metric("Đảng viên", len(df[df['is_dang_vien'] == 1]) if not df.empty else 0)
            
            st.markdown("---")
            if not df.empty:
                st.subheader("📋 Danh sách tóm tắt")
                st.dataframe(df[['ma_nv', 'ho_ten', 'phong_ban', 'chuc_vu', 'trang_thai']], use_container_width=True)
            else:
                st.info("💡 Chưa có dữ liệu nhân sự trong cơ sở dữ liệu. Vui lòng chuyển sang mục 'Thêm mới Nhân viên'.")
        except Exception as e:
            st.error(f"Lỗi truy vấn dữ liệu: {e}")

elif menu == "👥 Danh sách Nhân viên":
    st.title("👥 QUẢN LÝ HỒ SƠ NHÂN VIÊN")
    if engine:
        try:
            df = pd.read_sql("SELECT * FROM nhan_su ORDER BY ma_nv ASC", engine)
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Lỗi đọc dữ liệu: {e}")

elif menu == "➕ Thêm mới Nhân viên":
    st.title("➕ THÊM HỒ SƠ NHÂN VIÊN MỚI")
    
    with st.form("form_them_nv"):
        col1, col2 = st.columns(2)
        with col1:
            ma_nv = st.text_input("Mã nhân viên (*)", placeholder="NV001")
            ho_ten = st.text_input("Họ và tên (*)", placeholder="Nguyễn Văn A")
            phong_ban = st.text_input("Phòng / Khoa / Trung tâm")
            chuc_vu = st.text_input("Chức vụ")
        with col2:
            trinh_do = st.selectbox("Trình độ", ["Tiến sĩ / Bác sĩ CKII", "Thạc sĩ / Bác sĩ CKI", "Bác sĩ Đa khoa", "Cử nhân / Khác"])
            trang_thai = st.selectbox("Trạng thái", ["Đang làm việc", "Tạm nghỉ", "Đã nghỉ việc"])
            is_dang_vien = st.checkbox("Là Đảng viên")
            
        submit = st.form_submit_button("💾 Lưu hồ sơ")
        
        if submit:
            if not ma_nv or not ho_ten:
                st.warning("⚠️ Vui lòng điền mã NV và Họ tên!")
            elif engine:
                try:
                    with engine.begin() as conn:
                        conn.execute(text("""
                            INSERT INTO nhan_su (ma_nv, ho_ten, phong_ban, chuc_vu, trinh_do, is_dang_vien, trang_thai)
                            VALUES (:ma_nv, :ho_ten, :phong_ban, :chuc_vu, :trinh_do, :is_dang_vien, :trang_thai)
                        """), {
                            "ma_nv": ma_nv, "ho_ten": ho_ten, "phong_ban": phong_ban,
                            "chuc_vu": chuc_vu, "trinh_do": trinh_do,
                            "is_dang_vien": 1 if is_dang_vien else 0,
                            "trang_thai": trang_thai
                        })
                    st.success(f"✅ Đã thêm nhân sự {ho_ten} ({ma_nv}) thành công!")
                except Exception as e:
                    st.error(f"❌ Mã nhân viên '{ma_nv}' có thể đã tồn tại!")
