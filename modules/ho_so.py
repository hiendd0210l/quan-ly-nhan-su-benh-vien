import streamlit as st
import pandas as pd
from sqlalchemy import text

DB_COLUMN_MAP = {
    "Mã NV": "ma_nv", "Họ tên": "ho_ten", "Tên gọi khác": "ten_goi_khac", 
    "Ngày sinh": "ngay_sinh", "Giới tính": "gioi_tinh", "Nơi sinh": "noi_sinh", 
    "Quê quán": "que_quan", "Dân tộc": "dan_toc", "Tôn giáo": "ton_giao", 
    "Nơi ở hiện nay": "noi_o_hien_nay", "Điện thoại": "dien_thoai", "Số CCCD": "so_cccd", 
    "Khoa/Phòng": "khoa_phong", "Chức vụ": "chuc_vu", "Ngạch viên chức": "ngach_vien_chuc", 
    "Bậc lương": "bac_luong", "Hệ số lương": "he_so_luong", "Ngày nâng lương": "ngay_nang_luong", 
    "Trình độ giáo dục": "trinh_do_giao_duc", "Trình độ chuyên môn": "trinh_do_chuyen_mon", 
    "Lý luận chính trị": "ly_luan_chinh_tri", "Ngoại ngữ": "ngoai_ngu", "Tin học": "tin_hoc", 
    "Số CCHN": "so_cchn", "Giờ CME": "gio_cme", "Ngày vào Đảng": "ngay_vao_dang", 
    "Ngày nhập ngũ": "ngay_nhap_ngu", "Danh hiệu phong tặng": "danh_hieu_phong_tang", 
    "Khen thưởng kỷ luật": "khen_thuong_ky_luat", "Sức khỏe thương binh": "suc_khoe_thuong_binh", 
    "Loại HĐ": "loai_hd", "Ngày hết hạn HĐ": "ngay_het_han_hd", "Trạng thái": "trang_thai"
}

def render_ho_so(engine):
    st.title("👥 QUẢN LÝ & CHỈNH SỬA HỒ SƠ NHÂN SỰ")
    st.markdown("---")
    
    if engine:
        df = pd.read_sql("SELECT * FROM nhan_su ORDER BY ma_nv ASC", engine)
        
        if not df.empty:
            reverse_map = {v: k for k, v in DB_COLUMN_MAP.items()}
            df_display = df.rename(columns=reverse_map)
            
            edited_df = st.data_editor(
                df_display, 
                num_rows="dynamic", 
                use_container_width=True,
                key="editor_nhansu"
            )
            
            if st.button("💾 Lưu mọi thay đổi"):
                try:
                    save_df = edited_df.rename(columns=DB_COLUMN_MAP)
                    with engine.begin() as conn:
                        conn.execute(text("DELETE FROM nhan_su;"))
                        save_df.to_sql('nhan_su', conn, if_exists='append', index=False)
                    st.success("✅ Đã lưu toàn bộ thay đổi thành công!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Lỗi khi lưu dữ liệu: {e}")
        else:
            st.warning("Chưa có dữ liệu nhân sự để hiển thị!")
