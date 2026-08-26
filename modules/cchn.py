import streamlit as st
import pandas as pd

def render_cchn(engine):
    st.title("📜 QUẢN LÝ CHỨNG CHỈ HÀNH NGHỀ & GIẤY PHÉP CHUYÊN MÔN")
    st.markdown("---")

    if not engine:
        return

    df = pd.read_sql("SELECT ma_nv, ho_ten, khoa_phong, chuc_vu, so_cchn, gio_cme FROM nhan_su", engine)
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.subheader("🔍 Bộ lọc")
        search = st.text_input("Tìm kiếm Họ tên / CCHN")
        filter_status = st.radio("Lọc trạng thái CCHN", ["Tất cả", "Đã có CCHN", "Chưa có CCHN", "Cảnh báo thiếu CME (<48h)"])

    with col2:
        # Xử lý lọc
        if search:
            df = df[df['ho_ten'].str.contains(search, case=False, na=False) | df['so_cchn'].str.contains(search, case=False, na=False)]
        
        df['gio_cme_num'] = pd.to_numeric(df['gio_cme'], errors='coerce').fillna(0)

        if filter_status == "Đã có CCHN":
            df = df[df['so_cchn'].notnull() & (df['so_cchn'] != '') & (df['so_cchn'] != 'nan')]
        elif filter_status == "Chưa có CCHN":
            df = df[df['so_cchn'].isnull() | (df['so_cchn'] == '') | (df['so_cchn'] == 'nan')]
        elif filter_status == "Cảnh báo thiếu CME (<48h)":
            df = df[df['gio_cme_num'] < 48]

        st.subheader(f"Danh sách Hồ sơ CCHN ({len(df)} bản ghi)")
        st.dataframe(
            df[['ma_nv', 'ho_ten', 'khoa_phong', 'chuc_vu', 'so_cchn', 'gio_cme_num']],
            column_config={
                "ma_nv": "Mã NV",
                "ho_ten": "Họ và Tên",
                "khoa_phong": "Khoa / Phòng",
                "chuc_vu": "Chức vụ",
                "so_cchn": "Số CCHN / Giấy phép",
                "gio_cme_num": st.column_config.NumberColumn("Số giờ CME đạt được", format="%d hrs ⏱️")
            },
            use_container_width=True
        )
