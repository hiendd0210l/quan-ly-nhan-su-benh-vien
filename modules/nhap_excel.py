import streamlit as st
import pandas as pd
import io
from sqlalchemy import text

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

def render_nhap_excel(engine):
    st.title("➕ THÊM MỚI & NHẬP DỮ LIỆU TỪ EXCEL")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["📥 Nhập file Excel (Mẫu 2C-BNV/2008)", "✏️ Thêm mới từng Nhân viên"])
    
    with tab1:
        st.subheader("1. Tải file Excel mẫu 2C-BNV/2008")
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
                    import_df_db = import_df.rename(columns=DB_COLUMN_MAP)
                    if engine:
                        with engine.begin() as conn:
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
                        st.success(f"✅ Đã nạp thành công {len(import_df)} hồ sơ!")
            except Exception as e:
                st.error(f"❌ Lỗi xử lý file Excel: {e}")

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
                nhom_lao_dong = st.selectbox("Nhóm lao động", [
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
            if btn_submit and engine:
                if not ma_nv or not ho_ten:
                    st.warning("⚠️ Vui lòng nhập Mã NV và Họ tên!")
                else:
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
                        st.error(f"❌ Mã nhân viên '{ma_nv}' có thể đã tồn tại!")
