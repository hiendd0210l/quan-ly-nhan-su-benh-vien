import streamlit as st
import pandas as pd
import numpy as np
import io
from sqlalchemy import text, DATE, String

# Danh sách 33 cột chuẩn theo Mẫu Lý Lịch 2C BNV
COLUMNS_2C = [
    "Ma_NV", "Ho_Ten", "Ten_Goi_Khac", "Ngay_Sinh", "Gioi_Tinh", "Noi_Sinh", "Que_Quan", 
    "Dan_Toc", "Ton_Giao", "Noi_O_Hien_Nay", "Dien_Thoai", "So_CCCD", "Khoa_Phong", 
    "Chuc_Vu", "Ngach_Vien_Chuc", "Bac_Luong", "He_So_Luong", "Ngay_Nang_Luong", 
    "Trinh_Do_Giao_Duc", "Trinh_Do_Chuyen_Mon", "Ly_Luan_Chinh_Tri", "Ngoai_Ngu", 
    "Tin_Hoc", "So_CCHN", "Gio_CME", "Ngay_Vao_Dang", "Ngay_Nhap_Ngu", 
    "Danh_Hieu_Phong_Tang", "Khen_Thuong_Ky_Luat", "Suc_Khoe_Thuong_Binh", 
    "Loai_HD", "Ngay_Het_Han_HD", "Trang_Thai"
]

# Các cột chứa dữ liệu ngày tháng
DATE_COLUMNS = ["ngay_sinh", "ngay_nang_luong", "ngay_vao_dang", "ngay_nhap_ngu", "ngay_het_han_hd"]

def clean_and_format_dataframe(df):
    """Hàm làm sạch dữ liệu:
    1. Chuẩn hóa tên cột
    2. Chuyển ô rỗng / NaN / None thành None (NULL)
    3. Định dạng các cột ngày tháng sang kiểu datetime (Y-m-d)
    """
    df_clean = df.copy()
    df_clean.columns = [c.strip().lower() for c in df_clean.columns]
    
    # 1. Thay thế tất cả các biến thể NaN/None/Rỗng bằng None (NULL)
    df_clean = df_clean.replace({np.nan: None, 'NaN': None, 'nan': None, 'None': None, 'null': None, '': None})
    
    # Làm sạch khoảng trắng trên từng ô kiểu chuỗi
    for col in df_clean.columns:
        if df_clean[col].dtype == 'object':
            df_clean[col] = df_clean[col].apply(lambda x: x.strip() if isinstance(x, str) and x.strip() not in ['', 'NaN', 'nan', 'None', 'null'] else None)

    # 2. Định dạng các cột ngày tháng
    for d_col in DATE_COLUMNS:
        if d_col in df_clean.columns:
            # Chuyển đổi sang datetime, ép lỗi về NaT (None)
            df_clean[d_col] = pd.to_datetime(df_clean[d_col], errors='coerce', dayfirst=True)
            # Chuyển NaT thành None để ghi đúng vào PostgreSQL DATE
            df_clean[d_col] = df_clean[d_col].apply(lambda x: x.date() if pd.notnull(x) else None)
            
    return df_clean

def format_date_str(val):
    """Chuyển đổi hiển thị Date ra định dạng DD/MM/YYYY trên giao diện"""
    if pd.isna(val) or val is None or str(val).strip() in ['', 'None', 'NaT', 'nan']:
        return ""
    try:
        dt = pd.to_datetime(val)
        return dt.strftime('%d/%m/%Y')
    except:
        return str(val)

def create_sample_excel():
    """Tạo file Excel mẫu chứa dòng dữ liệu ví dụ chuẩn 33 cột"""
    sample_data = [{
        "Ma_NV": "N0001", "Ho_Ten": "Nguyễn Văn A", "Ten_Goi_Khac": "", "Ngay_Sinh": "01/01/1985",
        "Gioi_Tinh": "Nam", "Noi_Sinh": "Hà Nội", "Que_Quan": "Hà Nội", "Dan_Toc": "Kinh (Việt)",
        "Ton_Giao": "Không", "Noi_O_Hien_Nay": "Số 1 Trần Hưng Đạo, Hà Nội", "Dien_Thoai": "0912345678",
        "So_CCCD": "001085000001", "Khoa_Phong": "Khoa Hồi sức Cấp cứu", "Chuc_Vu": "Trưởng khoa",
        "Ngach_Vien_Chuc": "Viên chức A2", "Bac_Luong": "3/8", "He_So_Luong": "5.08",
        "Ngay_Nang_Luong": "01/01/2024", "Trinh_Do_Giao_Duc": "12 / 12", "Trinh_Do_Chuyen_Mon": "Bác sĩ CKII",
        "Ly_Luan_Chinh_Tri": "Cao cấp", "Ngoai_Ngu": "Tiếng Anh C1", "Tin_Hoc": "Đạt",
        "So_CCHN": "001234/BYT-CCHN", "Gio_CME": "48", "Ngay_Vao_Dang": "19/05/2010",
        "Ngay_Nhap_Ngu": "", "Danh_Hieu_Phong_Tang": "Thầy thuốc Ưu tú", "Khen_Thuong_Ky_Luat": "Bằng khen BYT",
        "Suc_Khoe_Thuong_Binh": "Tốt", "Loai_HD": "Không thời hạn", "Ngay_Het_Han_HD": "", "Trang_Thai": "Chính thức"
    }]
    df_sample = pd.DataFrame(sample_data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_sample.to_excel(writer, sheet_name='Mau_2C_BNV', index=False)
    return output.getvalue()

def render_ho_so(engine):
    st.title("📂 QUẢN LÝ HỒ SƠ NHÂN SỰ (MẪU 2C-BNV)")
    st.caption("Chuẩn hóa thông tin hồ sơ nhân sự theo quy định Bộ Nội vụ & Bệnh viện Bưu điện")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["📋 Danh sách & Thêm/Sửa/Xóa Nhân sự", "📥 Import / Export File Excel", "📄 Xuất Mẫu File Excel 2C"])

    # -------------------------------------------------------------
    # TAB 1: DANH SÁCH & QUẢN LÝ THÊM / SỬA / XÓA NHÂN SỰ
    # -------------------------------------------------------------
    with tab1:
        if not engine:
            st.error("⚠️ Chưa kết nối được CSDL PostgreSQL.")
            return

        try:
            df_db = pd.read_sql("SELECT * FROM nhan_su ORDER BY ma_nv ASC", engine)
        except Exception as e:
            st.error(f"❌ Lỗi tải dữ liệu: {e}")
            df_db = pd.DataFrame(columns=[c.lower() for c in COLUMNS_2C])

        # Chuyển các trường ngày sang định dạng DD/MM/YYYY để hiển thị đẹp
        df_display = df_db.copy()
        for d_col in DATE_COLUMNS:
            if d_col in df_display.columns:
                df_display[d_col] = df_display[d_col].apply(format_date_str)

        # Xử lý bỏ các chữ NaN/None rỗng trên bảng hiển thị
        df_display = df_display.fillna('')

        # Tìm kiếm & Lọc
        col_search1, col_search2 = st.columns([3, 1])
        with col_search1:
            search_term = st.text_input("🔍 Tìm kiếm theo Mã NV, Họ tên, CCCD, Số CCHN...")

        if search_term and not df_display.empty:
            df_display = df_display[
                df_display['ma_nv'].astype(str).str.contains(search_term, case=False, na=False) |
                df_display['ho_ten'].astype(str).str.contains(search_term, case=False, na=False) |
                df_display['so_cccd'].astype(str).str.contains(search_term, case=False, na=False)
            ]

        st.markdown(f"**Tổng số nhân sự hiện có:** `{len(df_display)}` người")
        st.dataframe(df_display, use_container_width=True, height=300)

        # FORM THÊM / SỬA CÁ NHÂN TỪNG NHÂN SỰ
        st.subheader("📝 Cập nhật thông tin chi tiết Nhân sự")
        
        selected_ma_nv = st.selectbox(
            "Chọn Mã Nhân viên để SỬA/XÓA (Hoặc chọn Thêm mới):", 
            ["-- Thêm Mới Nhân Viên --"] + list(df_db['ma_nv'].dropna().unique()) if not df_db.empty else ["-- Thêm Mới Nhân Viên --"]
        )

        curr_data = {}
        if selected_ma_nv != "-- Thêm Mới Nhân Viên --":
            row = df_db[df_db['ma_nv'] == selected_ma_nv].iloc[0]
            curr_data = row.to_dict()

        with st.form("form_nhan_su", clear_on_submit=False):
            c1, c2, c3 = st.columns(3)
            with c1:
                ma_nv = st.text_input("Mã NV (*)", value=str(curr_data.get('ma_nv', '') or ''))
                ho_ten = st.text_input("Họ và Tên (*)", value=str(curr_data.get('ho_ten', '') or ''))
                ngay_sinh = st.text_input("Ngày sinh (DD/MM/YYYY)", value=format_date_str(curr_data.get('ngay_sinh')))
                gioi_tinh = st.selectbox("Giới tính", ["Nam", "Nữ"], index=0 if curr_data.get('gioi_tinh') != "Nữ" else 1)
                so_cccd = st.text_input("Số CCCD", value=str(curr_data.get('so_cccd', '') or ''))
                dien_thoai = st.text_input("Điện thoại", value=str(curr_data.get('dien_thoai', '') or ''))
                
            with c2:
                khoa_phong = st.text_input("Khoa / Phòng", value=str(curr_data.get('khoa_phong', '') or ''))
                chuc_vu = st.text_input("Chức vụ", value=str(curr_data.get('chuc_vu', '') or ''))
                trinh_do_cm = st.text_input("Trình độ Chuyên môn", value=str(curr_data.get('trinh_do_chuyen_mon', '') or ''))
                so_cchn = st.text_input("Số CCHN", value=str(curr_data.get('so_cchn', '') or ''))
                gio_cme = st.text_input("Giờ CME tích lũy", value=str(curr_data.get('gio_cme', '') or ''))
                ngay_vao_dang = st.text_input("Ngày vào Đảng (DD/MM/YYYY)", value=format_date_str(curr_data.get('ngay_vao_dang')))

            with c3:
                he_so_luong = st.text_input("Hệ số lương", value=str(curr_data.get('he_so_luong', '') or ''))
                bac_luong = st.text_input("Bậc lương", value=str(curr_data.get('bac_luong', '') or ''))
                loai_hd = st.text_input("Loại hợp đồng", value=str(curr_data.get('loai_hd', '') or ''))
                trang_thai = st.selectbox("Trạng thái", ["Chính thức", "Thử việc", "Nghỉ hưu", "Đã nghỉ việc"], index=0)
                noi_o = st.text_input("Nơi ở hiện nay", value=str(curr_data.get('noi_o_hien_nay', '') or ''))
                que_quan = st.text_input("Quê quán", value=str(curr_data.get('que_quan', '') or ''))

            b_save, b_del = st.columns([1, 1])
            with b_save:
                btn_submit = st.form_submit_button("💾 LƯU DỮ LIỆU NHÂN SỰ", type="primary", use_container_width=True)
            with b_del:
                btn_delete = st.form_submit_button("🗑️ XÓA NHÂN SỰ NÀY", use_container_width=True)

            if btn_submit:
                if not ma_nv or not ho_ten:
                    st.error("⚠️ Vui lòng nhập Mã NV và Họ Tên!")
                else:
                    try:
                        # Ép kiểu Date hợp lệ trước khi lưu
                        d_ns = pd.to_datetime(ngay_sinh, dayfirst=True, errors='coerce')
                        d_ns_val = d_ns.date() if pd.notnull(d_ns) else None

                        d_vd = pd.to_datetime(ngay_vao_dang, dayfirst=True, errors='coerce')
                        d_vd_val = d_vd.date() if pd.notnull(d_vd) else None

                        with engine.begin() as conn:
                            query = text("""
                                INSERT INTO nhan_su (
                                    ma_nv, ho_ten, ngay_sinh, gioi_tinh, so_cccd, dien_thoai,
                                    khoa_phong, chuc_vu, trinh_do_chuyen_mon, so_cchn, gio_cme,
                                    ngay_vao_dang, he_so_luong, bac_luong, loai_hd, trang_thai,
                                    noi_o_hien_nay, que_quan
                                ) VALUES (
                                    :ma_nv, :ho_ten, :ngay_sinh, :gioi_tinh, :so_cccd, :dien_thoai,
                                    :khoa_phong, :chuc_vu, :trinh_do_cm, :so_cchn, :gio_cme,
                                    :ngay_vao_dang, :he_so_luong, :bac_luong, :loai_hd, :trang_thai,
                                    :noi_o, :que_quan
                                )
                                ON CONFLICT (ma_nv) DO UPDATE SET
                                    ho_ten = EXCLUDED.ho_ten,
                                    ngay_sinh = EXCLUDED.ngay_sinh,
                                    gioi_tinh = EXCLUDED.gioi_tinh,
                                    so_cccd = EXCLUDED.so_cccd,
                                    dien_thoai = EXCLUDED.dien_thoai,
                                    khoa_phong = EXCLUDED.khoa_phong,
                                    chuc_vu = EXCLUDED.chuc_vu,
                                    trinh_do_chuyen_mon = EXCLUDED.trinh_do_chuyen_mon,
                                    so_cchn = EXCLUDED.so_cchn,
                                    gio_cme = EXCLUDED.gio_cme,
                                    ngay_vao_dang = EXCLUDED.ngay_vao_dang,
                                    he_so_luong = EXCLUDED.he_so_luong,
                                    bac_luong = EXCLUDED.bac_luong,
                                    loai_hd = EXCLUDED.loai_hd,
                                    trang_thai = EXCLUDED.trang_thai,
                                    noi_o_hien_nay = EXCLUDED.noi_o_hien_nay,
                                    que_quan = EXCLUDED.que_quan;
                            """)
                            conn.execute(query, {
                                "ma_nv": ma_nv, "ho_ten": ho_ten, "ngay_sinh": d_ns_val,
                                "gioi_tinh": gioi_tinh, "so_cccd": so_cccd or None, "dien_thoai": dien_thoai or None,
                                "khoa_phong": khoa_phong or None, "chuc_vu": chuc_vu or None, "trinh_do_cm": trinh_do_cm or None,
                                "so_cchn": so_cchn or None, "gio_cme": gio_cme or None, "ngay_vao_dang": d_vd_val,
                                "he_so_luong": he_so_luong or None, "bac_luong": bac_luong or None, "loai_hd": loai_hd or None,
                                "trang_thai": trang_thai, "noi_o": noi_o or None, "que_quan": que_quan or None
                            })
                        st.success(f"✅ Đã lưu thành công nhân sự [{ma_nv}] {ho_ten} vào CSDL!")
                        st.rerun()
                    except Exception as ex:
                        st.error(f"❌ Lỗi lưu dữ liệu: {ex}")

            if btn_delete and selected_ma_nv != "-- Thêm Mới Nhân Viên --":
                try:
                    with engine.begin() as conn:
                        conn.execute(text("DELETE FROM nhan_su WHERE ma_nv = :m"), {"m": selected_ma_nv})
                    st.success(f"✅ Đã xóa nhân sự [{selected_ma_nv}] khỏi CSDL!")
                    st.rerun()
                except Exception as ex:
                    st.error(f"❌ Lỗi xóa nhân sự: {ex}")

    # -------------------------------------------------------------
    # TAB 2: UPLOAD FILE EXCEL CẬP NHẬT VĨNH VIỄN VÀO CSDL
    # -------------------------------------------------------------
    with tab2:
        st.subheader("📤 Upload dữ liệu Excel Mẫu 2C vào Cơ sở dữ liệu PostgreSQL")
        st.info("💡 Hệ thống tự động làm sạch ô dữ liệu NaN/Rỗng và định dạng các trường Ngày tháng sang chuẩn Date (DD/MM/YYYY).")

        uploaded_file = st.file_uploader("Chọn file Excel (.xlsx, .xls)", type=["xlsx", "xls"])
        
        if uploaded_file is not None:
            try:
                # Đọc Excel
                df_raw = pd.read_excel(uploaded_file, sheet_name=0)
                st.write("🔍 **Xem trước dữ liệu sau khi làm sạch & định dạng DATE:**")
                
                # Làm sạch NaN và ép kiểu DATE
                df_clean = clean_and_format_dataframe(df_raw)
                st.dataframe(df_clean.head(10), use_container_width=True)

                if st.button("🚀 XÁC NHẬN LƯU VĨNH VIỄN VÀO CSDL", type="primary"):
                    # Thiết lập kiểu dữ liệu CSDL cho các cột ngày tháng
                    dtype_dict = {d_col: DATE() for d_col in DATE_COLUMNS if d_col in df_clean.columns}
                    
                    with engine.begin() as conn:
                        df_clean.to_sql('nhan_su', con=conn, if_exists='replace', index=False, dtype=dtype_dict)
                    
                    st.success(f"🎉 Đã làm sạch và lưu thành công {len(df_clean)} nhân sự vĩnh viễn vào CSDL!")
                    st.balloons()
            except Exception as e:
                st.error(f"❌ Lỗi xử lý file Excel: {e}")

    # -------------------------------------------------------------
    # TAB 3: TẠO VÀ TẢI FILE EXCEL MẪU CHUẨN 2C-BNV
    # -------------------------------------------------------------
    with tab3:
        st.subheader("📄 Tạo & Tải File Excel Mẫu Lý Lịch 2C-BNV")
        st.write("File mẫu này chứa đầy đủ 33 trường thông tin chuẩn theo Mẫu 2C/BNV của Bộ Nội vụ.")

        excel_sample_bytes = create_sample_excel()

        st.download_button(
            label="📥 TẢI FILE EXCEL MẪU (Mau_Ly_Lich_2C_BNV.xlsx)",
            data=excel_sample_bytes,
            file_name="Mau_Ly_Lich_2C_BNV.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary"
        )
