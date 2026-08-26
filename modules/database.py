import streamlit as st
from sqlalchemy import create_engine, text

@st.cache_resource
def get_db_engine():
    try:
        if "postgres" in st.secrets and "url" in st.secrets["postgres"]:
            db_url = st.secrets["postgres"]["url"]
            if db_url.startswith("postgres://"):
                db_url = db_url.replace("postgres://", "postgresql://", 1)
            return create_engine(db_url, pool_size=10, max_overflow=20, pool_pre_ping=True)
        else:
            st.error("⚠️ Chưa cấu hình Postgres URL trong Secrets!")
            return None
    except Exception as e:
        st.error(f"⚠️ Lỗi kết nối CSDL: {e}")
        return None

def init_db(engine):
    if not engine:
        return
    with engine.begin() as conn:
        # 1. Bảng Hồ sơ nhân sự chuẩn BNV (33 cột)
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS nhan_su (
                ma_nv VARCHAR(50) PRIMARY KEY,
                ho_ten VARCHAR(100) NOT NULL,
                ten_goi_khac VARCHAR(100),
                ngay_sinh VARCHAR(50),
                gioi_tinh VARCHAR(20),
                noi_sinh VARCHAR(255),
                que_quan VARCHAR(255),
                dan_toc VARCHAR(50) DEFAULT 'Kinh',
                ton_giao VARCHAR(50) DEFAULT 'Không',
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
                gio_cme VARCHAR(50) DEFAULT '0',
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
        
        # 2. Bảng Người dùng & Phân quyền 9 cấp
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS sys_users (
                username VARCHAR(50) PRIMARY KEY,
                password_hash VARCHAR(255) NOT NULL,
                ma_nv VARCHAR(50) REFERENCES nhan_su(ma_nv) ON DELETE SET NULL,
                full_name VARCHAR(100),
                role VARCHAR(50) NOT NULL,
                khoa_phong VARCHAR(150),
                is_active BOOLEAN DEFAULT TRUE
            );
        """))

        # 3. Bảng Quản lý Ca trực & Chấm công Y tế
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS ca_truc (
                id SERIAL PRIMARY KEY,
                ma_nv VARCHAR(50) REFERENCES nhan_su(ma_nv),
                ngay_truc DATE NOT NULL,
                loai_ca VARCHAR(50) NOT NULL, -- Hành chính, Trực 24h, Trực cấp cứu, Ca đêm
                khoa_phong VARCHAR(150),
                ghi_chu TEXT
            );
        """))

        # 4. Bảng Đào tạo CME & Chứng chỉ y khoa
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dao_tao_cme (
                id SERIAL PRIMARY KEY,
                ma_nv VARCHAR(50) REFERENCES nhan_su(ma_nv),
                ten_khoa_dao_tao VARCHAR(255) NOT NULL,
                so_gio_cme INT DEFAULT 0,
                ngay_cap DATE,
                noi_cap VARCHAR(255),
                loai_chung_chi VARCHAR(100)
            );
        """))

        # 5. Bảng Đơn xin Nghỉ phép (Duyệt 4 cấp)
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS don_nghi_pheap (
                id SERIAL PRIMARY KEY,
                ma_nv VARCHAR(50) REFERENCES nhan_su(ma_nv),
                loai_pheap VARCHAR(100) NOT NULL,
                tu_ngay DATE NOT NULL,
                den_ngay DATE NOT NULL,
                ly_do TEXT,
                trang_thai VARCHAR(50) DEFAULT 'Chờ Trưởng khoa duyệt'
            );
        """))
