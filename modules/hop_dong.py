import streamlit as st
import pandas as pd
from sqlalchemy import text

def render_hop_dong(engine):
    st.title("📝 QUẢN LÝ HỢP ĐỒNG LAO ĐỘNG")
    st.caption("Theo dõi loại hợp đồng, thời hạn hợp đồng và cảnh báo nhân sự sắp hết hạn HĐ")
    st.markdown("---")

    if not engine:
        st.error("⚠️ Chưa kết nối CSDL PostgreSQL.")
        return

    try:
        query = """
            SELECT ma_nv, ho_ten, khoa_phong, loai_hd, ngay_het_han_hd, trang_thai 
            FROM nhan_su 
            ORDER BY ma_nv ASC
        """
        df_hd = pd.read_sql(query, engine)
        
        # Làm sạch hiển thị
        df_hd = df_hd.fillna('')
        df_hd['ngay_het_han_hd'] = pd.to_datetime(df_hd['ngay_het_han_hd'], errors='coerce').dt.strftime('%d/%m/%Y').fillna('')

        st.markdown(f"**Tổng số hợp đồng đang theo dõi:** `{len(df_hd)}` record")
        st.dataframe(df_hd, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Lỗi tải dữ liệu Hợp đồng: {e}")
