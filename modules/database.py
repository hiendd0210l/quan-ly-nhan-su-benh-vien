import streamlit as st
from sqlalchemy import create_engine, text

@st.cache_resource
def get_db_engine():
    try:
        if "postgres" in st.secrets and "url" in st.secrets["postgres"]:
            db_url = st.secrets["postgres"]["url"]
            if db_url.startswith("postgres://"):
                db_url = db_url.replace("postgres://", "postgresql://", 1)
            return create_engine(db_url)
        else:
            st.error("⚠️ Chưa cấu hình Secrets trên Streamlit Cloud!")
            return None
    except Exception as e:
        st.error(f"⚠️ Lỗi kết nối CSDL: {e}")
        return None

def init_db(engine):
    if engine:
        try:
            with engine.begin() as conn:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS nhan_su (
                        ma_nv VARCHAR(50) PRIMARY KEY,
                        ho_ten VARCHAR(100) NOT NULL,
                        gioi_tinh VARCHAR(10),
                        ngay_sinh VARCHAR(20),
                        que_quan VARCHAR(200),
                        dan_toc VARCHAR(50),
                        ton_giao VARCHAR(50),
                        cccd VARCHAR(20),
                        ngay_cap_cccd VARCHAR(20),
                        phong_ban VARCHAR(100),
                        chuc_vu VARCHAR(100),
                        nhom_lao_dong VARCHAR(100),
                        trinh_do_chuyen_mon VARCHAR(100),
                        trinh_do_ly_luan VARCHAR(100),
                        trinh_do_ngoai_ngu VARCHAR(100),
                        ngay_vao_dang VARCHAR(20),
                        ngay_tuyen_dung VARCHAR(20),
                        trang_thai VARCHAR(50) DEFAULT 'Đang làm việc'
                    );
                """))
        except Exception as e:
            st.error(f"Lỗi khởi tạo bảng: {e}")
