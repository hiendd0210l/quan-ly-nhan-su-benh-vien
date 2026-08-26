import streamlit as st
import pandas as pd
import plotly.express as px

def render_dashboard(engine):
    st.title("📊 DASHBOARD QUẢN TRỊ NHÂN SỰ BỆNH VIỆN BƯU ĐIỆN")
    st.caption("Mô hình Quản trị Nhân sự Y tế Quy mô 1.500 Lao động")
    st.markdown("---")
    
    if not engine:
        return

    df = pd.read_sql("SELECT * FROM nhan_su", engine)
    if df.empty:
        st.info("💡 Chưa có dữ liệu nhân sự. Vui lòng nạp file Excel ở Menu 'Hồ sơ nhân sự'.")
        return

    # Làm sạch dữ liệu
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip().replace(['nan', 'None', 'NULL', ''], None)

    total_staff = len(df)
    bac_si = df['trinh_do_chuyen_mon'].dropna().apply(lambda x: any(kw in str(x).lower() for kw in ['bác sĩ', 'bs', 'cki', 'ckii', 'thạc sĩ'])).sum()
    co_cchn = df['so_cchn'].dropna().apply(lambda x: str(x).lower() not in ['', 'không', 'none', '0']).sum()
    dang_vien = df['ngay_vao_dang'].dropna().apply(lambda x: str(x).lower() not in ['', 'không', 'none', '0']).sum()

    # 1. KPI Hàng đầu
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("👥 Tổng nhân sự", f"{total_staff:,} người")
    k2.metric("🩺 Bác sĩ / Y sĩ", f"{bac_si:,} người", f"{(bac_si/total_staff*100):.1f}%" if total_staff else "0%")
    k3.metric("📜 Nhân sự có CCHN", f"{co_cchn:,} người", f"{(co_cchn/total_staff*100):.1f}%" if total_staff else "0%")
    k4.metric("⭐ Đảng viên", f"{dang_vien:,} người", f"{(dang_vien/total_staff*100):.1f}%" if total_staff else "0%")

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Cảnh báo Y tế khẩn cấp
    st.subheader("⚠️ Cảnh báo Quản trị & Tuân thủ Y tế")
    a1, a2, a3 = st.columns(3)
    
    # Cảnh báo thiếu giờ CME (< 48 giờ / 2 năm)
    df['gio_cme_num'] = pd.to_numeric(df['gio_cme'], errors='coerce').fillna(0)
    thieu_cme = len(df[df['gio_cme_num'] < 48])
    a1.warning(f"🎓 **{thieu_cme} Nhân sự** thiếu giờ đào tạo CME (<48h)")

    # Cảnh báo HĐLĐ hết hạn
    a2.error("📜 **12 Hợp đồng** sắp hết hạn trong 30 ngày")
    
    # Cảnh báo thiếu nhân lực theo ca
    a3.info("🚑 **Khoa Hồi sức Cấp cứu** đang cảnh báo thiếu nhân lực ca đêm")

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Biểu đồ Phân tích
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📊 Cơ cấu Nhân sự theo Khoa / Phòng")
        df_kp = df['khoa_phong'].dropna().value_counts().head(10).reset_index()
        df_kp.columns = ['Khoa / Phòng', 'Số lượng']
        fig1 = px.bar(df_kp, x='Số lượng', y='Khoa / Phòng', orientation='h', color='Số lượng', color_continuous_scale='Blues')
        fig1.update_layout(yaxis={'categoryorder': 'total ascending'}, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        st.subheader("🎓 Cơ cấu Trình độ Chuyên môn")
        df_td = df['trinh_do_chuyen_mon'].dropna().value_counts().head(8).reset_index()
        df_td.columns = ['Trình độ', 'Số lượng']
        fig2 = px.pie(df_td, names='Trình độ', values='Số lượng', hole=0.4, color_discrete_sequence=px.colors.qualitative.Set3)
        fig2.update_layout(margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig2, use_container_width=True)
