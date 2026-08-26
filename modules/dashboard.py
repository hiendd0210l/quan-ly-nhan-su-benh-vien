import streamlit as st
import pandas as pd
import plotly.express as px

def render_dashboard(engine):
    st.title("📊 DASHBOARD QUẢN TRỊ NHÂN SỰ BỆNH VIỆN BƯU ĐIỆN")
    st.caption("Cập nhật theo tiêu chuẩn quản trị nhóm lao động V3")
    st.markdown("---")
    
    if engine:
        df = pd.read_sql("SELECT * FROM nhan_su", engine)
        
        col1, col2, col3, col4 = st.columns(4)
        total_staff = len(df)
        col1.metric("👥 Tổng nhân sự", f"{total_staff:,} người", "↗ +12 trong tháng")
        
        truc_tiep = len(df[df['nhom_lao_dong'] == '1. Lao động Trực tiếp sản xuất']) if not df.empty else 0
        col2.metric("🩺 Trực tiếp sản xuất", f"{truc_tiep} người", f"{(truc_tiep/total_staff*100):.1f}%" if total_staff else "0%")
        
        chuyen_mon = len(df[df['nhom_lao_dong'] == '2. Lao động Chuyên môn nghiệp vụ']) if not df.empty else 0
        col3.metric("📑 Chuyên môn nghiệp vụ", f"{chuyen_mon} người", f"{(chuyen_mon/total_staff*100):.1f}%" if total_staff else "0%")
        
        dang_vien = len(df[df['ngay_vao_dang'].notnull() & (df['ngay_vao_dang'] != '')]) if not df.empty else 0
        col4.metric("⭐ Đảng viên", f"{dang_vien} người", f"{(dang_vien/total_staff*100):.1f}%" if total_staff else "0%")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if not df.empty:
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("Chart 1: Cơ cấu Nhân sự theo Nhóm lao động")
                fig1 = px.pie(df, names='nhom_lao_dong', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig1, use_container_width=True)
                
            with c2:
                st.subheader("Chart 2: Trình độ Chuyên môn Y tế")
                fig2 = px.bar(df['trinh_do_chuyen_mon'].value_counts().reset_index(), 
                              x='trinh_do_chuyen_mon', y='count', color='trinh_do_chuyen_mon')
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("💡 Chưa có dữ liệu. Hãy nạp file Excel ở mục 'Thêm mới & Nhập Excel'.")
