import streamlit as st
import pandas as pd
import plotly.express as px

def render_dashboard(engine):
    st.title("📊 DASHBOARD QUẢN TRỊ NHÂN SỰ BỆNH VIỆN BƯU ĐIỆN")
    st.caption("Cập nhật dữ liệu thời gian thực từ CSDL Mẫu 2C-BNV")
    st.markdown("---")
    
    if engine:
        try:
            df = pd.read_sql("SELECT * FROM nhan_su", engine)
        except Exception as e:
            st.error(f"❌ Lỗi truy vấn CSDL: {e}")
            return

        if df.empty:
            st.info("💡 Chưa có dữ liệu nhân sự trong Cơ sở dữ liệu. Vui lòng nạp file Excel ở mục 'Thêm mới & Nhập Excel'.")
            return

        # Làm sạch khoảng trắng thừa và chuẩn hóa chuỗi
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace(['nan', 'None', 'NULL', 'null', 'NoneType', ''], None)

        total_staff = len(df)

        # 1. Logic lọc chính xác từng chỉ số
        # Bác sĩ/Y sĩ
        bac_si = df['trinh_do_chuyen_mon'].dropna().apply(
            lambda x: any(kw in str(x).lower() for kw in ['bác sĩ', 'bac si', 'bs', 'cki', 'ckii', 'thạc sĩ'])
        ).sum()

        # Số có Chứng chỉ hành nghề (không trống và khác 'không', 'none')
        co_cchn = df['so_cchn'].dropna().apply(
            lambda x: str(x).strip().lower() not in ['', 'không', 'khong', 'none', 'nan', '0']
        ).sum()

        # Số Đảng viên (có ngày vào Đảng hợp lệ)
        dang_vien = df['ngay_vao_dang'].dropna().apply(
            lambda x: str(x).strip().lower() not in ['', 'không', 'khong', 'none', 'nan', '0']
        ).sum()

        # 2. Hàng KPI tổng quan
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("👥 Tổng nhân sự", f"{total_staff:,} người")
        col2.metric("🩺 Bác sĩ / Y sĩ", f"{bac_si:,} người", f"{(bac_si/total_staff*100):.1f}%" if total_staff else "0%")
        col3.metric("📜 Nhân sự có CCHN", f"{co_cchn:,} người", f"{(co_cchn/total_staff*100):.1f}%" if total_staff else "0%")
        col4.metric("⭐ Đảng viên", f"{dang_vien:,} người", f"{(dang_vien/total_staff*100):.1f}%" if total_staff else "0%")

        st.markdown("<br>", unsafe_allow_html=True)

        # 3. Biểu đồ phân tích
        c1, c2 = st.columns(2)

        with c1:
            st.subheader("📊 Cơ cấu Nhân sự theo Khoa / Phòng")
            df_kp_clean = df['khoa_phong'].dropna()
            if not df_kp_clean.empty:
                df_kp = df_kp_clean.value_counts().head(10).reset_index()
                df_kp.columns = ['Khoa / Phòng', 'Số lượng']
                
                fig1 = px.bar(
                    df_kp, 
                    x='Số lượng', 
                    y='Khoa / Phòng', 
                    orientation='h',
                    color='Số lượng',
                    color_continuous_scale='Blues',
                    text='Số lượng'
                )
                fig1.update_layout(
                    yaxis={'categoryorder': 'total ascending'},
                    margin=dict(l=10, r=10, t=10, b=10)
                )
                st.plotly_chart(fig1, use_container_width=True)
            else:
                st.info("Chưa có dữ liệu Khoa/Phòng.")

        with c2:
            st.subheader("🎓 Trình độ Chuyên môn Top đầu")
            df_td_clean = df['trinh_do_chuyen_mon'].dropna()
            if not df_td_clean.empty:
                df_td = df_td_clean.value_counts().head(8).reset_index()
                df_td.columns = ['Trình độ', 'Số lượng']
                
                fig2 = px.pie(
                    df_td, 
                    names='Trình độ', 
                    values='Số lượng', 
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig2.update_layout(margin=dict(l=10, r=10, t=10, b=10))
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("Chưa có dữ liệu Trình độ chuyên môn.")
