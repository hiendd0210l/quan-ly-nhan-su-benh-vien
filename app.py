import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
from sqlalchemy import create_engine, text

# ==============================================================================
# 1. CẤU HÌNH TRANG WEB & KẾT NỐI CSDL
# ==============================================================================
st.set_page_config(
    page_title="HRMS - Bệnh viện Bưu điện",
    page_icon="🏥",
    layout="wide"
)

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

engine = get_db_engine()

# Khởi tạo bảng dữ liệu PostgreSQL chuẩn Mẫu 2C-BNV/2008
def init_db():
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

init_db()

# Các trường dữ liệu Mẫu 2C-BNV/2008
MAU_2C_COLUMNS = [
    "Mã NV", "Họ và tên", "Giới tính", "Ngày sinh", "Quê quán", 
    "Dân tộc", "Tôn giáo", "Số CCCD", "Ngày cấp CCCD", "Phòng/Khoa/Trung tâm", 
    "Chức vụ", "Nhóm lao động", "Trình độ chuyên môn", "Trình độ lý luận", 
    "Trình độ ngoại ngữ", "Ngày vào Đảng", "Ngày tuyển dụng", "Trạng thái"
]

DB_COLUMN_MAP = {
    "Mã NV": "ma_nv", "Họ và tên": "ho_ten", "Giới tính": "gioi_tinh", "Ngày sinh": "ngay_sinh",
    "Quê quán": "que_quan", "Dân tộc": "dan_toc", "Tôn giáo": "ton_giao", "Số CCCD": "cccd",
    "Ngày cấp CCCD": "ngay_cap_cccd", "Phòng/Khoa/Trung tâm": "phong_ban", "Chức vụ": "chuc_vu",
    "Nhóm lao động": "nhom_lao_dong", "Trình độ chuyên môn": "trinh_do_chuyen_mon",
    "Trình độ lý luận": "trinh_do_ly_luan", "Trình độ ngoại ngữ": "trinh_do_ngoai_ngu",
    "Ngày vào Đảng": "ngay_vao_dang", "Ngày tuyển dụng": "ngay_tuyen_dung", "Trạng thái": "trang_thai"
}

# ==============================================================================
# 2. THANH DIỀU HƯỚNG MENU (SIDEBAR)
# ==============================================================================
st.sidebar.markdown("<h2 style='text-align: center; color: #0056b3;'>🏥 BỆNH VIỆN BƯU ĐIỆN</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; font-weight: bold;'>HỆ THỐNG QUẢN TRỊ NHÂN SỰ (HRMS)</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

menu = st.sidebar.radio("DANH MỤC CHỨC NĂNG", [
    "📊 Dashboard Tổng quan",
    "👥 Hồ sơ Nhân sự & Chỉnh sửa",
    "➕ Thêm mới & Nhập Excel (Mẫu 2C)",
    "📜 Quản lý CCHN & CME",
    "📝 Quản lý Hợp đồng & Lương",
    "🏛️ Đảng & Đoàn thể",
    "📈 Báo cáo Thống kê"
])

# ==============================================================================
# 3. XỬ LÝ CHỨC NĂNG TỪNG MENU
# ==============================================================================

# ------------------------------------------------------------------------------
# MENU 1: DASHBOARD TỔNG QUAN
# ------------------------------------------------------------------------------
if menu == "📊 Dashboard Tổng quan":
    st.title("📊 DASHBOARD QUẢN TRỊ NHÂN SỰ BỆNH VIỆN BƯU ĐIỆN")
    st.caption("Cập nhật theo tiêu chuẩn quản trị nhóm lao động V3")
    st.markdown("---")
    
    if engine:
        df = pd.read_sql("SELECT * FROM nhan_su", engine)
        
        # 1. Các Thẻ KPI
        col1, col2, col3, col4 = st.columns(4)
        
        total_staff = len(df)
        col1.metric("👥 Tổng nhân sự", f"{total_staff:,} người", "↗ +12 trong tháng")
        
        truc_tiep = len(df[df['nhom_lao_dong'] == '1. Lao động Trực tiếp sản xuất']) if not df.empty else 0
        col2.metric("🩺 Trực tiếp sản xuất", f"{truc_tiep} người", f"{(truc_tiep/total_staff*100):.1f}%" if total_staff else "0%")
        
        chuyen_mon = len(df[df['nhom_lao_dong'] == '2. Lao động Chuyên môn nghiệp vụ']) if not df.empty else 0
        col3.metric("📑 Chuyên môn nghiệp vụ", f"{chuyen_mon} người", f"{(chuyen_mon/total_staff*100):.1f}%" if total_staff else "0%")
        
        dang_vien = len(df[df['ngay_vao_dang'].notnull() & (df['ngay_vao_dang'] != '')]) if not df.empty else 0
        col4.metric("⭐ Đảng viên", f"{dang_vien} người", f"{(dang_vien/total_staff*100):.1f}%" if total_staff else "0%")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 2. Biểu đồ thống kê
        if not df.empty:
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("Chart 1: Cơ cấu Nhân sự theo Nhóm lao động")
                fig1 = px.pie(df, names='nhom_lao_dong', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
                fig1.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig1, use_container_width=True)
                
            with c2:
                st.subheader("Chart 2: Trình độ Chuyên môn Y tế")
                fig2 = px.bar(df['trinh_do_chuyen_mon'].value_counts().reset_index(), 
                              x='trinh_do_chuyen_mon', y='count', color='trinh_do_chuyen_mon',
                              labels={'trinh_do_chuyen_mon': 'Trình độ', 'count': 'Số lượng'})
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("💡 Hệ thống chưa có dữ liệu. Vui lòng chọn Menu 'Thêm mới & Nhập Excel' để tải dữ liệu lên.")

# ------------------------------------------------------------------------------
# MENU 2: HỒ SƠ NHÂN SỰ & CHỈNH SỬA / XÓA DỮ LIỆU
# ------------------------------------------------------------------------------
elif menu == "👥 Hồ sơ Nhân sự & Chỉnh sửa":
    st.title("👥 QUẢN LÝ & CHỈNH SỬA HỒ SƠ NHÂN SỰ")
    st.markdown("---")
    
    if engine:
        df = pd.read_sql("SELECT * FROM nhan_su ORDER BY ma_nv ASC", engine)
        
        if not df.empty:
            st.subheader("✏️ Chỉnh sửa dữ liệu trực tiếp trên bảng")
            st.caption("Bạn có thể double-click vào ô để sửa dữ liệu, tích chọn ở ô đầu dòng để xóa. Nhớ nhấn 'Lưu thay đổi' sau khi hoàn tất!")
            
            # Map tên cột CSDL sang tên hiển thị
            reverse_map = {v: k for k, v in DB_COLUMN_MAP.items()}
            df_display = df.rename(columns=reverse_map)
            
            # Cho phép sửa dữ liệu trên bảng
            edited_df = st.data_editor(
                df_display, 
                num_rows="dynamic", 
                use_container_width=True,
                key="editor_nhansu"
            )
            
            c1, c2 = st.columns([1, 4])
            with c1:
                if st.button("💾 Lưu mọi thay đổi"):
                    try:
                        # Chuẩn hóa lại tên cột trước khi ghi đè vào DB
                        save_df = edited_df.rename(columns=DB_COLUMN_MAP)
                        with engine.begin() as conn:
                            conn.execute(text("DELETE FROM nhan_su;"))
                            save_df.to_sql('nhan_su', conn, if_exists='append', index=False)
                        st.success("✅ Đã lưu toàn bộ thay đổi vào Cơ sở dữ liệu thành công!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Lỗi khi lưu dữ liệu: {e}")
        else:
            st.warning("Chưa có dữ liệu nhân sự để hiển thị!")

# ------------------------------------------------------------------------------
# MENU 3: THÊM MỚI & NHẬP EXCEL (MẪU 2C-BNV/2008)
# ------------------------------------------------------------------------------
elif menu == "➕ Thêm mới & Nhập Excel (Mẫu 2C)":
    st.title("➕ THÊM MỚI & NHẬP DỮ LIỆU TỪ EXCEL")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["📥 Nhập file Excel (Mẫu 2C-BNV/2008)", "✏️ Thêm mới từng Nhân viên"])
    
    # TAB 1: NHẬP EXCEL MẪU 2C
    with tab1:
        st.subheader("1. Tải file Excel mẫu 2C-BNV/2008")
        
        # Tạo file Excel mẫu trong bộ nhớ
        output = io.BytesIO()
        sample_df = pd.DataFrame(columns=MAU_2C_COLUMNS)
        sample_df.loc[0] = [
            "NV001", "Nguyễn Văn A", "Nam", "15/08/1985", "Hà Nội", "Kinh", "Không",
            "001085123456", "01/01/2021", "Khoa Lâm sàng", "Bác sĩ Chuyên khoa I",
            "1. Lao động Trực tiếp sản xuất", "Thạc sĩ / Bác sĩ CKI", "Trung cấp",
            "Tiếng Anh B1", "03/02/2015", "01/06/2010", "Đang làm việc"
        ]
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            sample_df.to_excel(writer, index=False, sheet_name='Mau_2C_BNV')
        
        st.download_button(
            label="📥 Tải File Excel Mẫu chuẩn (Mẫu 2C-BNV/2008)",
            data=output.getvalue(),
            file_name="Mau_2C_BNV_2008_BVBD.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("2. Cập nhật dữ liệu từ file Excel vào ứng dụng")
        
        uploaded_file = st.file_uploader("Chọn file Excel đã nhập dữ liệu:", type=['xlsx', 'xls'])
        
        if uploaded_file is not None:
            try:
                import_df = pd.read_excel(uploaded_file)
                st.write("📋 **Xem trước dữ liệu từ file Excel:**")
                st.dataframe(import_df.head(), use_container_width=True)
                
                if st.button("🚀 Cập nhật toàn bộ vào Cơ sở dữ liệu"):
                    # Đổi tên cột từ tiếng Việt sang tên cột trong CSDL
                    import_df_db = import_df.rename(columns=DB_COLUMN_MAP)
                    
                    if engine:
                        with engine.begin() as conn:
                            # Đẩy dữ liệu vào DB (chèn mới hoặc ghi đè nếu trùng Mã NV)
                            for _, row in import_df_db.iterrows():
                                conn.execute(text("""
                                    INSERT INTO nhan_su (
                                        ma_nv, ho_ten, gioi_tinh, ngay_sinh, que_quan, dan_toc, ton_giao,
                                        cccd, ngay_cap_cccd, phong_ban, chuc_vu, nhom_lao_dong,
                                        trinh_do_chuyen_mon, trinh_do_ly_luan, trinh_do_ngoai_ngu,
                                        ngay_vao_dang, ngay_tuyen_dung, trang_thai
                                    ) VALUES (
                                        :ma_nv, :ho_ten, :gioi_tinh, :ngay_sinh, :que_quan, :dan_toc, :ton_giao,
                                        :cccd, :ngay_cap_cccd, :phong_ban, :chuc_vu, :nhom_lao_dong,
                                        :trinh_do_chuyen_mon, :trinh_do_ly_luan, :trinh_do_ngoai_ngu,
                                        :ngay_vao_dang, :ngay_tuyen_dung, :trang_thai
                                    ) ON CONFLICT (ma_nv) DO UPDATE SET
                                        ho_ten = EXCLUDED.ho_ten,
                                        phong_ban = EXCLUDED.phong_ban,
                                        chuc_vu = EXCLUDED.chuc_vu,
                                        nhom_lao_dong = EXCLUDED.nhom_lao_dong,
                                        trinh_do_chuyen_mon = EXCLUDED.trinh_do_chuyen_mon,
                                        trang_thai = EXCLUDED.trang_thai;
                                """), row.to_dict())
                        st.success(f"✅ Đã tải lên và cập nhật thành công {len(import_df)} hồ sơ nhân sự!")
            except Exception as e:
                st.error(f"❌ Lỗi xử lý file Excel: {e}")

    # TAB 2: THÊM MỚI TỪNG NHÂN VIÊN
    with tab2:
        with st.form("form_them_thu_cong"):
            c1, c2, c3 = st.columns(3)
            with c1:
                ma_nv = st.text_input("Mã Nhân viên (*)", placeholder="NV002")
                ho_ten = st.text_input("Họ và tên (*)")
                gioi_tinh = st.selectbox("Giới tính", ["Nam", "Nữ"])
                ngay_sinh = st.text_input("Ngày sinh", placeholder="DD/MM/YYYY")
                que_quan = st.text_input("Quê quán")
                dan_toc = st.text_input("Dân tộc", value="Kinh")
            with c2:
                phong_ban = st.text_input("Phòng / Khoa / Trung tâm")
                chuc_vu = st.text_input("Chức vụ")
                nhom_lao_dong = st.selectbox("Nhóm lao động (Chuẩn V3)", [
                    "1. Lao động Trực tiếp sản xuất",
                    "2. Lao động Chuyên môn nghiệp vụ",
                    "3. Lao động Thừa hành phục vụ",
                    "4. Lao động Lãnh đạo"
                ])
                trinh_do_cm = st.selectbox("Trình độ chuyên môn", [
                    "Tiến sĩ / Bác sĩ CKII", "Thạc sĩ / Bác sĩ CKI",
                    "Bác sĩ Đa khoa / Chuyên khoa", "Cử nhân Điều dưỡng / Dược sĩ / KTV",
                    "Cao đẳng / Trung cấp / Khác"
                ])
                trinh_do_ll = st.text_input("Trình độ lý luận chính trị")
            with c3:
                cccd = st.text_input("Số CCCD")
                ngay_cap_cccd = st.text_input("Ngày cấp CCCD")
                ngay_tuyen_dung = st.text_input("Ngày tuyển dụng")
                ngay_vao_dang = st.text_input("Ngày vào Đảng (nếu có)")
                trang_thai = st.selectbox("Trạng thái", ["Đang làm việc", "Nghỉ phép", "Đã nghỉ việc"])
                
            btn_submit = st.form_submit_button("💾 Thêm mới Nhân viên")
            if btn_submit:
                if not ma_nv or not ho_ten:
                    st.warning("⚠️ Vui lòng nhập Mã NV và Họ tên!")
                elif engine:
                    try:
                        with engine.begin() as conn:
                            conn.execute(text("""
                                INSERT INTO nhan_su (ma_nv, ho_ten, gioi_tinh, ngay_sinh, que_quan, dan_toc, cccd, ngay_cap_cccd, phong_ban, chuc_vu, nhom_lao_dong, trinh_do_chuyen_mon, trinh_do_ly_luan, ngay_tuyen_dung, ngay_vao_dang, trang_thai)
                                VALUES (:ma_nv, :ho_ten, :gioi_tinh, :ngay_sinh, :que_quan, :dan_toc, :cccd, :ngay_cap_cccd, :phong_ban, :chuc_vu, :nhom_ld, :trinh_do_cm, :trinh_do_ll, :ngay_td, :ngay_vd, :trang_thai)
                            """), {
                                "ma_nv": ma_nv, "ho_ten": ho_ten, "gioi_tinh": gioi_tinh, "ngay_sinh": ngay_sinh,
                                "que_quan": que_quan, "dan_toc": dan_toc, "cccd": cccd, "ngay_cap_cccd": ngay_cap_cccd,
                                "phong_ban": phong_ban, "chuc_vu": chuc_vu, "nhom_ld": nhom_lao_dong,
                                "trinh_do_cm": trinh_do_cm, "trinh_do_ll": trinh_do_ll, "ngay_td": ngay_tuyen_dung,
                                "ngay_vd": ngay_vao_dang, "trang_thai": trang_thai
                            })
                        st.success(f"✅ Đã thêm mới nhân viên {ho_ten} ({ma_nv})!")
                    except Exception as e:
                        st.error(f"❌ Lỗi: Mã nhân viên '{ma_nv}' có thể đã tồn tại trong CSDL!")

# ------------------------------------------------------------------------------
# MENU 4 TỚI 7: CÁC MODULE MỞ RỘNG PHÁT TRUYỂN SAU
# ------------------------------------------------------------------------------
elif menu == "📜 Quản lý CCHN & CME":
    st.title("📜 QUẢN LÝ CHỨNG CHỈ HÀNH NGHỀ Y TẾ & ĐÀO TẠO CME")
    st.info("📌 Phân hệ đang được cấu hình sẵn kết nối. Bạn có thể mở rộng bảng lưu trữ Chứng chỉ hành nghề y tế (CCHN) và số tiết CME đào tạo liên tục tại đây.")

elif menu == "📝 Quản lý Hợp đồng & Lương":
    st.title("📝 QUẢN LÝ HỢP ĐỒNG LAO ĐỘNG & BẬC LƯƠNG")
    st.info("📌 Phân hệ theo dõi thời hạn hợp đồng lao động 2 năm, hợp đồng chuyên gia hưu trí và thời hạn nâng bậc lương Q3/Q4.")

elif menu == "🏛️ Đảng & Đoàn thể":
    st.title("🏛️ QUẢN LÝ TỔ CHỨC ĐẢNG & ĐOÀN THỂ")
    st.info("📌 Phân hệ quản lý hồ sơ Đảng viên, sinh hoạt Đảng và danh sách khen thưởng/kỷ luật.")

elif menu == "📈 Báo cáo Thống kê":
    st.title("📈 BÁO CÁO & XUẤT DỮ LIỆU TỔNG HỢP")
    if engine:
        df = pd.read_sql("SELECT * FROM nhan_su", engine)
        if not df.empty:
            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 Tải Báo cáo Toàn bộ Nhân sự Bệnh viện (File CSV/Excel)",
                data=csv,
                file_name="Bao_cao_nhan_su_BVBD.csv",
                mime="text/csv"
            )
        else:
            st.warning("Chưa có dữ liệu để kết xuất báo cáo!")
