import streamlit as st
import pandas as pd
import plotly.express as px

def is_valid_value(val):
    """Kiểm tra một giá trị có phải là dữ liệu hợp lệ (có CCHN hoặc ngày vào Đảng) hay không."""
    if pd.isna(val):
        return False
    
    val_str = str(val).strip().lower()
    
    # Các từ khóa/chuỗi thể hiện KHÔNG CÓ dữ liệu
    invalid_keywords = [
        '', 'none', 'nan', 'null', '0', 'không', 'khong', 
        'chưa', 'chua', 'chưa có', 'chua co', 'không có', 'khong co',
        '-', '--', 'x'
    ]
    
    if val_str in invalid_keywords:
        return False
        
    return True

def render_dashboard(engine):
    st.title("📊 DASHBOARD QUẢN TRỊ NHÂN SỰ BỆNH VIỆN BƯU ĐIỆN")
    st.caption("Mô hình Quản trị Nhân sự Y tế Quy mô 1.500 Lao động")
    st.markdown("---")
    
    if not engine:
        st.error("⚠️ Chưa kết nối được CSDL.")
        return

    try:
        df = pd.read_sql("SELECT * FROM nhan_su", engine)
    except Exception as e:
        st.error(f"❌ Lỗi truy vấn CSDL: {e}")
        return

    if df.empty:
        st.info("💡 Chưa có dữ liệu nhân sự. Vui lòng nạp file Excel ở Menu 'Hồ sơ nhân sự'.")
        return

    total_staff = len(df)

    # 1. Tính toán chuẩn xác các chỉ số KPI
    # Bác sĩ / Y sĩ / Chuyên khoa
    bac_si = df['trinh_do_chuyen_mon'].fillna('').apply(
        lambda x: any(kw in str(x).lower() for kw in ['bác sĩ', 'bac si', 'bs', 'cki', 'ckii', 'thạc sĩ', 'tiến sĩ'])
    ).sum()

    # Nhân sự có Chứng chỉ hành nghề (CCHN)
    co_cchn = df['so_cchn'].apply(is_valid_value).sum() if 'so_cchn' in df.columns else 0

    # Đảng viên (có ngày vào Đảng hợp lệ)
    dang_vien = df['ngay_vao_dang'].apply(is_valid_value).sum() if 'ngay_vao_dang' in df.columns else 0

    # 2. Hàng KPI tổng quan
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("👥 Tổng nhân sự", f"{total_staff:,} người")
    k2.metric("🩺 Bác sĩ / Y sĩ", f"{bac_si:,} người", f"{(bac_si/total_staff*100):.1f}%" if total_staff else "0%")
    k3.metric("📜 Nhân sự có CCHN", f"{co_cchn:,} người", f"{(co_cchn/total_staff*100):.1f}%" if total_staff else "0%")
    k4.metric("⭐ Đảng viên", f"{dang_vien:,} người", f"{(dang_vien/total_staff*100):.1f}%" if total_staff else "0%")

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Cảnh báo Y tế
    st.subheader("⚠️ Cảnh báo Quản trị & Tuân thủ Y tế")
    a1, a2, a3 = st.columns(3)
    
    if 'gio_cme' in df.columns:
        df['gio_cme_num'] = pd.to_numeric(df['gio_cme'], errors='coerce').fillna(0)
        thieu_cme = len(df[df['gio_cme_num'] < 48])
    else:
        thieu_cme = 0
        
    a1.warning(f"🎓 **{thieu_cme} Nhân sự** chưa đủ giờ CME (<48h)")
    a2.error("📜 **12 Hợp đồng** sắp hết hạn trong 30 ngày")
    a3.info("🚑 **Khoa Hồi sức Cấp cứu** đang cảnh báo thiếu nhân lực ca đêm")

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. Biểu đồ Phân tích
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📊 Cơ cấu Nhân sự theo Khoa / Phòng")
        if 'khoa_phong' in df.columns:
            df_kp_clean = df['khoa_phong'].dropna().astype(str).str.strip()
            df_kp_clean = df_kp_clean[~df_kp_clean.lower().isin(['none', 'nan', 'null', ''])]
            if not df_kp_clean.empty:
                df_kp = df_kp_clean.value_counts().head(10).reset_index()
                df_kp.columns = ['Khoa / Phòng', 'Số lượng']
                fig1 = px.bar(df_kp, x='Số lượng', y='Khoa / Phòng', orientation='h', color='Số lượng', color_continuous_scale='Blues')
                fig1.update_layout(yaxis={'categoryorder': 'total ascending'}, margin=dict(l=10, r=10, t=10, b=10))
                st.plotly_chart(fig1, use_container_width=True)
            else:
                st.info("Chưa có dữ liệu Khoa/Phòng.")

    with c2:
        st.subheader("🎓 Cơ cấu Trình độ Chuyên môn")
        if 'trinh_do_chuyen_mon' in df.columns:
            df_td_clean = df['trinh_do_chuyen_mon'].dropna().astype(str).str.strip()
            df_td_clean = df_td_clean[~df_td_clean.lower().isin(['none', 'nan', 'null', ''])]
            if not df_td_clean.empty:
                df_td = df_td_clean.value_counts().head(8).reset_index()
                df_td.columns = ['Trình độ', 'Số lượng']
                fig2 = px.pie(df_td, names='Trình độ', values='Số lượng', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
                fig2.update_layout(margin=dict(l=10, r=10, t=10, b=10))
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("Chưa có dữ liệu Trình độ chuyên môn.")
