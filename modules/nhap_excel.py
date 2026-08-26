import streamlit as st
import pandas as pd
import io
from sqlalchemy import text

EXCEL_COLUMN_MAP = {
    "Ma_NV": "ma_nv", "Ho_Ten": "ho_ten", "Ten_Goi_Khac": "ten_goi_khac", 
    "Ngay_Sinh": "ngay_sinh", "Gioi_Tinh": "gioi_tinh", "Noi_Sinh": "noi_sinh", 
    "Que_Quan": "que_quan", "Dan_Toc": "dan_toc", "Ton_Giao": "ton_giao", 
    "Noi_O_Hien_Nay": "noi_o_hien_nay", "Dien_Thoai": "dien_thoai", "So_CCCD": "so_cccd", 
    "Khoa_Phong": "khoa_phong", "Chuc_Vu": "chuc_vu", "Ngach_Vien_Chuc": "ngach_vien_chuc", 
    "Bac_Luong": "bac_luong", "He_So_Luong": "he_so_luong", "Ngay_Nang_Luong": "ngay_nang_luong", 
    "Trinh_Do_Giao_Duc": "trinh_do_giao_duc", "Trinh_Do_Chuyen_Mon": "trinh_do_chuyen_mon", 
    "Ly_Luan_Chinh_Tri": "ly_luan_chinh_tri", "Ngoai_Ngu": "ngoai_ngu", "Tin_Hoc": "tin_hoc", 
    "So_CCHN": "so_cchn", "Gio_CME": "gio_cme", "Ngay_Vao_Dang": "ngay_vao_dang", 
    "Ngay_Nhap_Ngu": "ngay_nhap_ngu", "Danh_Hieu_Phong_Tang": "danh_hieu_phong_tang", 
    "Khen_Thuong_Ky_Luat": "khen_thuong_ky_luat", "Suc_Khoe_Thuong_Binh": "suc_khoe_thuong_binh", 
    "Loai_HD": "loai_hd", "Ngay_Het_Han_HD": "ngay_het_han_hd", "Trang_Thai": "trang_thai"
}

def render_nhap_excel(engine):
    st.title("➕ THÊM MỚI & NHẬP DỮ LIỆU TỪ EXCEL")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["📥 Nhập file Excel (Mau_Ly_Lich_2C_BNV.xlsx)", "✏️ Thêm mới từng Nhân viên"])
    
    with tab1:
        st.subheader("1. Tải file Excel mẫu chuẩn 2C-BNV (33 trường thông tin)")
        output = io.BytesIO()
        sample_df = pd.DataFrame(columns=list(EXCEL_COLUMN_MAP.keys()))
        sample_df.loc[0] = [
            "N0001", "Nguyễn Văn A", "", "01/01/1985", "Nam", "Hà Nội", "Hà Nội", "Kinh", "Không",
            "Hà Nội", "0912345678", "001085123456", "Khoa Lâm sàng", "Bác sĩ", "Viên chức A1",
            "1/9", "2.34", "01/01/2025", "12/12", "Thạc sĩ, Bác sĩ CKI", "Sơ cấp", "Tiếng Anh B1",
            "Cơ bản", "001234/BYT-CCHN", "48", "01/01/2015", "", "", "", "Tốt",
            "Không thời hạn", "", "Chính thức"
        ]
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            sample_df.to_excel(writer, index=False, sheet_name='Mau_2C_BNV')
        
        st.download_button(
            label="📥 Tải File Excel Mẫu chuẩn (Mau_Ly_Lich_2C_BNV.xlsx)",
            data=output.getvalue(),
            file_name="Mau_Ly_Lich_2C_BNV.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("2. Cập nhật dữ liệu từ file Excel vào cơ sở dữ liệu")
        
        uploaded_file = st.file_uploader("Chọn file Excel (ví dụ: Mau_Ly_Lich_2C_BNV.xlsx):", type=['xlsx', 'xls'])
        
        if uploaded_file is not None:
            try:
                import_df = pd.read_excel(uploaded_file)
                st.write("📋 **Xem trước dữ liệu từ file Excel:**")
                st.dataframe(import_df.head(), use_container_width=True)
                
                if st.button("🚀 Cập nhật toàn bộ vào Cơ sở dữ liệu"):
                    with st.spinner("⏳ Đang ghi siêu tốc toàn bộ dữ liệu vào PostgreSQL, vui lòng chờ trong vài giây..."):
                        # Ánh xạ tên cột chuẩn CSDL
                        import_df_db = import_df.rename(columns=EXCEL_COLUMN_MAP)
                        
                        # Làm sạch dữ liệu nan/null
                        for col in import_df_db.columns:
                            import_df_db[col] = import_df_db[col].fillna("").astype(str)
                            import_df_db[col] = import_df_db[col].replace(['nan', 'None', 'NaT', '<NA>'], '')

                        if engine:
                            with engine.begin() as conn:
                                # Làm sạch dữ liệu trùng lặp nếu có
                                conn.execute(text("TRUNCATE TABLE nhan_su;"))
                                # Ghi hàng loạt tốc độ cao
                                import_df_db.to_sql(
                                    name='nhan_su', 
                                    con=conn, 
                                    if_exists='append', 
                                    index=False,
                                    method='multi',
                                    chunksize=500
                                )
                            st.success(f"🎉 Đã nạp thành công toàn bộ {len(import_df_db)} hồ sơ vào Cơ sở dữ liệu!")
            except Exception as e:
                st.error(f"❌ Lỗi xử lý file Excel: {e}")

    with tab2:
        with st.form("form_them_thu_cong"):
            c1, c2, c3 = st.columns(3)
            with c1:
                ma_nv = st.text_input("Mã NV (*)", placeholder="N0001")
                ho_ten = st.text_input("Họ tên (*)")
                ten_goi_khac = st.text_input("Tên gọi khác")
                ngay_sinh = st.text_input("Ngày sinh (DD/MM/YYYY)")
                gioi_tinh = st.selectbox("Giới tính", ["Nam", "Nữ"])
                noi_sinh = st.text_input("Nơi sinh")
                que_quan = st.text_input("Quê quán")
                dan_toc = st.text_input("Dân tộc", value="Kinh (Việt)")
                ton_giao = st.text_input("Tôn giáo", value="Không")
                noi_o_hien_nay = st.text_input("Nơi ở hiện nay")
                dien_thoai = st.text_input("Điện thoại")
            with c2:
                so_cccd = st.text_input("Số CCCD")
                khoa_phong = st.text_input("Khoa / Phòng")
                chuc_vu = st.text_input("Chức vụ")
                ngach_vien_chuc = st.text_input("Ngạch viên chức")
                bac_luong = st.text_input("Bậc lương")
                he_so_luong = st.text_input("Hệ số lương")
                ngay_nang_luong = st.text_input("Ngày nâng lương")
                trinh_do_giao_duc = st.text_input("Trình độ giáo dục", value="12 / 12")
                trinh_do_chuyen_mon = st.text_input("Trình độ chuyên môn")
                ly_luan_chinh_tri = st.text_input("Lý luận chính trị")
            with c3:
                ngoai_ngu = st.text_input("Ngoại ngữ")
                tin_hoc = st.text_input("Tin học")
                so_cchn = st.text_input("Số CCHN")
                gio_cme = st.text_input("Giờ CME")
                ngay_vao_dang = st.text_input("Ngày vào Đảng")
                ngay_nhap_ngu = st.text_input("Ngày nhập ngũ")
                danh_hieu_phong_tang = st.text_input("Danh hiệu phong tặng")
                khen_thuong_ky_luat = st.text_input("Khen thưởng kỷ luật")
                suc_khoe_thuong_binh = st.text_input("Sức khỏe / Thương binh")
                loai_hd = st.text_input("Loại HĐ", value="Không có thời hạn xác định")
                ngay_het_han_hd = st.text_input("Ngày hết hạn HĐ")
                trang_thai = st.selectbox("Trạng thái", ["Chính thức", "Thử việc", "Tạm nghỉ", "Đã nghỉ việc"])
                
            btn_submit = st.form_submit_button("💾 Thêm mới Nhân viên")
            if btn_submit and engine:
                if not ma_nv or not ho_ten:
                    st.warning("⚠️ Vui lòng nhập Mã NV và Họ tên!")
                else:
                    try:
                        with engine.begin() as conn:
                            conn.execute(text("""
                                INSERT INTO nhan_su (
                                    ma_nv, ho_ten, ten_goi_khac, ngay_sinh, gioi_tinh, noi_sinh, que_quan,
                                    dan_toc, ton_giao, noi_o_hien_nay, dien_thoai, so_cccd, khoa_phong,
                                    chuc_vu, ngach_vien_chuc, bac_luong, he_so_luong, ngay_nang_luong,
                                    trinh_do_giao_duc, trinh_do_chuyen_mon, ly_luan_chinh_tri, ngoai_ngu,
                                    tin_hoc, so_cchn, gio_cme, ngay_vao_dang, ngay_nhap_ngu,
                                    danh_hieu_phong_tang, khen_thuong_ky_luat, suc_khoe_thuong_binh,
                                    loai_hd, ngay_het_han_hd, trang_thai
                                ) VALUES (
                                    :ma_nv, :ho_ten, :ten_goi_khac, :ngay_sinh, :gioi_tinh, :noi_sinh, :que_quan,
                                    :dan_toc, :ton_giao, :noi_o_hien_nay, :dien_thoai, :so_cccd, :khoa_phong,
                                    :chuc_vu, :ngach_vien_chuc, :bac_luong, :he_so_luong, :ngay_nang_luong,
                                    :trinh_do_giao_duc, :trinh_do_chuyen_mon, :ly_luan_chinh_tri, :ngoai_ngu,
                                    :tin_hoc, :so_cchn, :gio_cme, :ngay_vao_dang, :ngay_nhap_ngu,
                                    :danh_hieu_phong_tang, :khen_thuong_ky_luat, :suc_khoe_thuong_binh,
                                    :loai_hd, :ngay_het_han_hd, :trang_thai
                                )
                            """), {
                                "ma_nv": ma_nv, "ho_ten": ho_ten, "ten_goi_khac": ten_goi_khac,
                                "ngay_sinh": ngay_sinh, "gioi_tinh": gioi_tinh, "noi_sinh": noi_sinh,
                                "que_quan": que_quan, "dan_toc": dan_toc, "ton_giao": ton_giao,
                                "noi_o_hien_nay": noi_o_hien_nay, "dien_thoai": dien_thoai, "so_cccd": so_cccd,
                                "khoa_phong": khoa_phong, "chuc_vu": chuc_vu, "ngach_vien_chuc": ngach_vien_chuc,
                                "bac_luong": bac_luong, "he_so_luong": he_so_luong, "ngay_nang_luong": ngay_nang_luong,
                                "trinh_do_giao_duc": trinh_do_giao_duc, "trinh_do_chuyen_mon": trinh_do_chuyen_mon,
                                "ly_luan_chinh_tri": ly_luan_chinh_tri, "ngoai_ngu": ngoai_ngu, "tin_hoc": tin_hoc,
                                "so_cchn": so_cchn, "gio_cme": gio_cme, "ngay_vao_dang": ngay_vao_dang,
                                "ngay_nhap_ngu": ngay_nhap_ngu, "danh_hieu_phong_tang": danh_hieu_phong_tang,
                                "khen_thuong_ky_luat": khen_thuong_ky_luat, "suc_khoe_thuong_binh": suc_khoe_thuong_binh,
                                "loai_hd": loai_hd, "ngay_het_han_hd": ngay_het_han_hd, "trang_thai": trang_thai
                            })
                        st.success(f"✅ Đã thêm thành công {ho_ten} ({ma_nv})!")
                    except Exception as e:
                        st.error(f"❌ Mã nhân viên '{ma_nv}' có thể đã tồn tại!")
