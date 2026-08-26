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
                # Xóa bảng cũ nếu cấu trúc chưa đúng
                conn.execute(text("DROP TABLE IF EXISTS nhan_su;"))
                
                # Tạo lại bảng đầy đủ 33 cột chuẩn Mẫu 2C
                conn.execute(text("""
                    CREATE TABLE nhan_su (
                        ma_nv VARCHAR(50) PRIMARY KEY,
                        ho_ten VARCHAR(100) NOT NULL,
                        ten_goi_khac VARCHAR(100),
                        ngay_sinh VARCHAR(50),
                        gioi_tinh VARCHAR(20),
                        noi_sinh VARCHAR(255),
                        que_quan VARCHAR(255),
                        dan_toc VARCHAR(50),
                        ton_giao VARCHAR(50),
                        noi_o_hien_nay VARCHAR(255),
                        dien_thoai VARCHAR(50),
                        so_cccd VARCHAR(50),
                        khoa_phong VARCHAR(150),
                        chuc_vu VARCHAR(150),
                        ngach_vien_chuc VARCHAR(100),
                        bac_luong VARCHAR(50),
                        he_so_luong VARCHAR(50),
                        ngay_nang_luong VARCHAR(50),
                        trinh_do_giao_duc VARCHAR(100),
                        trinh_do_chuyen_mon VARCHAR(150),
                        ly_luan_chinh_tri VARCHAR(100),
                        ngoai_ngu VARCHAR(100),
                        tin_hoc VARCHAR(100),
                        so_cchn VARCHAR(100),
                        gio_cme VARCHAR(50),
                        ngay_vao_dang VARCHAR(50),
                        ngay_nhap_ngu VARCHAR(50),
                        danh_hieu_phong_tang VARCHAR(200),
                        khen_thuong_ky_luat VARCHAR(200),
                        suc_khoe_thuong_binh VARCHAR(200),
                        loai_hd VARCHAR(150),
                        ngay_het_han_hd VARCHAR(50),
                        trang_thai VARCHAR(50) DEFAULT 'Chính thức'
                    );
                """))
        except Exception as e:
            st.error(f"Lỗi khởi tạo bảng: {e}")
