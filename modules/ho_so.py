import streamlit as st
import pandas as pd
from sqlalchemy import text

DB_COLUMN_MAP = {
    "Mã NV": "ma_nv", "Họ và tên": "ho_ten", "Giới tính": "gioi_tinh", "Ngày sinh": "ngay_sinh",
    "Quê quán": "que_quan", "Dân tộc": "dan_toc", "Tôn giáo": "ton_giao", "Số CCCD": "cccd",
    "Ngày cấp CCCD": "ngay_cap_cccd", "Phòng/Khoa/Trung tâm": "phong_ban", "Chức vụ": "chuc_vu",
    "Nhóm lao động": "nhom_lao_dong", "Trình độ chuyên môn": "trinh_do_chuyen_mon",
    "Trình độ lý luận": "trinh_do_ly_luan", "Trình độ ngoại ngữ": "trinh_do_ngoai_ngu",
    "Ngày vào Đảng": "ngay_vao_dang", "Ngày tuyển dụng": "ngay_tuyen_dung", "Trạng thái": "trang_thai"
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
