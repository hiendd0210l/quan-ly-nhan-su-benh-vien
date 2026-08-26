import streamlit as st
import pandas as pd
from sqlalchemy import text

def render_luong(engine):
    st.title("💰 QUẢN LÝ LƯƠNG CƠ BẢN & NGẠCH BẬC")
    st.caption("Quản lý Ngạch viên chức, Bậc lương, Hệ số lương và Ngày nâng lương tiếp theo")
    st.markdown("---")

    if not engine:
        st.error("⚠️ Chưa kết nối CSDL PostgreSQL.")
        return

    try:
        query = """
            SELECT ma_nv, ho_ten, khoa_phong, ngach_vien_chuc, bac_luong, he_so_luong, ngay_nang_luong 
            FROM nhan_su 
            ORDER BY ma_nv ASC
        """
        df_luong = pd.read_sql(query, engine)
        
        # Làm sạch hiển thị
        df_luong = df_luong.fillna('')
        df_luong['ngay_nang_luong'] = pd.to_datetime(df_luong['ngay_nang_luong'], errors='coerce').dt.strftime('%d/%m/%Y').fillna('')

        st.markdown(f"**Danh sách Quản lý Lương & Ngạch bậc:** `{len(df_luong)}` nhân sự")
        st.dataframe(df_luong, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Lỗi tải dữ liệu Lương: {e}")
