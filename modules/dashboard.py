import streamlit as st
import pandas as pd
import plotly.express as px
import os

def render_dashboard(engine, user_info=None):
    fullname = user_info.get("fullname", "Đoàn Danh Hiển") if user_info else "Đoàn Danh Hiển"
    role = user_info.get("role", "Quản trị viên Hệ thống — Bệnh viện Bưu điện") if user_info else "Quản trị viên Hệ thống — Bệnh viện Bưu điện"
    avatar_path = user_info.get("avatar_path", "doan_danh_hien.jpg") if user_info else "doan_danh_hien.jpg"

    st.markdown("""
        <style>
            .dash-card {
                padding: 18px;
                border-radius: 12px;
                color: white !important;
                margin-bottom: 15px;
                min-height: 135px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                box-shadow: 0 4px 10px rgba(0,0,0,0.08);
            }
            .card-red { background: linear-gradient(135deg, #ef4444, #dc2626); }
            .card-green { background: linear-gradient(135deg, #10b981, #059669); }
            .card-blue { background: linear-gradient(135deg, #3b82f6, #2563eb); }
            .card-dark { background: linear-gradient(135deg, #334155, #1e293b); }
            .card-orange { background: linear-gradient(135deg, #f97316, #ea580c); }
            .card-title { font-size: 15px; font-weight: 800; text-transform: uppercase; }
            .card-desc { font-size: 12px; opacity: 0.9; margin-top: 5px; }
            .card-action { font-size: 11px; font-weight: 700; text-align: right; text-transform: uppercase; }

            /* CSS Thẻ Cảnh Báo Gọn Số Lượng */
            .alert-box {
                background: #ffffff;
                border-radius: 10px;
                padding: 12px 16px;
                margin-bottom: 10px;
                border-left: 5px solid #0284c7;
                box-shadow: 0 2px 6px rgba(0,0,0,0.05);
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-top: 1px solid #f1f5f9;
                border-right: 1px solid #f1f5f9;
                border-bottom: 1px solid #f1f5f9;
            }
            .alert-title { font-size: 13px; font-weight: 700; color: #334155; }
            .alert-sub { font-size: 11px; color: #64748b; margin-top: 2px; }
            .alert-badge {
                background-color: #fee2e2;
                color: #dc2626;
                font-weight: 800;
                font-size: 16px;
                padding: 4px 12px;
                border-radius: 20px;
                border: 1px solid #fca5a5;
            }
        </style>
    """, unsafe_allow_html=True)

    # 1. KHỐI XIN CHÀO
    with st.container():
        col_img, col_txt = st.columns([0.12, 0.88])
        with col_img:
            if os.path.exists(avatar_path):
                st.image(avatar_path, width=80)
            elif os.path.exists("assets/doan_danh_hien.jpg"):
                st.image("assets/doan_danh_hien.jpg", width=80)
            else:
                st.image("https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=200", width=80)
        with col_txt:
            st.markdown(f"""
                <div style="padding-top: 2px;">
                    <h2 style="margin: 0; font-size: 24px; font-weight: 800; color: #1e293b;">Xin chào, {fullname}</h2>
                    <p style="margin: 3px 0 0 0; font-size: 13.5px; color: #64748b; font-weight: 500;">{role}</p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. CÁC THẺ CHỨC NĂNG HÀNG TRÊN
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="dash-card card-red"><div><div class="card-title">📇 HỒ SƠ CÁN BỘ CNV</div><div class="card-desc">Theo dõi, cập nhật và quản lý toàn bộ danh sách hồ sơ 877 nhân sự toàn bệnh viện.</div></div><div class="card-action">XEM CHI TIẾT ➔</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="dash-card card-green"><div><div class="card-title">📊 BÁO CÁO & THỐNG KÊ</div><div class="card-desc">Truy xuất dữ liệu báo cáo BYT, SBYT và biến động nhân sự theo thời gian thực.</div></div><div class="card-action">XEM BÁO CÁO ➔</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="dash-card card-blue"><div><div class="card-title">📜 GPHN & ĐÀO TẠO CME</div><div class="card-desc">Quản lý Chứng chỉ hành nghề và tiến độ tích lũy 48 tiết CME của Bác sĩ / Điều dưỡng.</div></div><div class="card-action">XEM CHI TIẾT ➔</div></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="dash-card card-dark"><div><div class="card-title">📝 HỢP ĐỒNG LAO ĐỘNG</div><div class="card-desc">Theo dõi hợp đồng xác định thời hạn, không xác định thời hạn và lịch tái ký.</div></div><div class="card-action">QUẢN LÝ HỒ SƠ ➔</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="dash-card card-orange"><div><div class="card-title">💰 NÂNG BẬC LƯƠNG & NGẠCH</div><div class="card-desc">Quản lý hệ số lương, ngạch viên chức và cảnh báo danh sách đủ điều kiện nâng lương.</div></div><div class="card-action">XEM DANH SÁCH ➔</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="dash-card card-green"><div><div class="card-title">🏥 QUẢN LÝ BHXH & SỨC KHỎE</div><div class="card-desc">Theo dõi chế độ Bảo hiểm xã hội, đóng BHYT và đợt khám sức khỏe định kỳ.</div></div><div class="card-action">CHI TIẾT ➔</div></div>', unsafe_allow_html=True)

    st.markdown("<hr style='margin: 15px 0 20px 0; border: none; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)

    # 3. CHIA KHU VỰC THỐNG KÊ & CẢNH BÁO THÀNH 3 CỘT BẰNG NHAU HÀNG NGANG
    sec1, sec2, sec3 = st.columns(3)

    # ----- CỘT 1: CẢNH BÁO TỰ ĐỘNG (GỌN SỐ LƯỢNG) -----
    with sec1:
        st.subheader("📌 Cảnh báo tự động")
        
        st.markdown("""
            <div class="alert-box" style="border-left-color: #ef4444;">
                <div>
                    <div class="alert-title">⏰ Sắp hết hạn HĐLĐ</div>
                    <div class="alert-sub">Cần ký lại / gia hạn trong 30 ngày</div>
                </div>
                <div class="alert-badge" style="color: #dc2626; background: #fee2e2;">12</div>
            </div>
            <div class="alert-box" style="border-left-color: #f97316;">
                <div>
                    <div class="alert-title">💰 Đến hạn nâng bậc lương</div>
                    <div class="alert-sub">Đủ thời hạn xét nâng ngạch, bậc</div>
                </div>
                <div class="alert-badge" style="color: #ea580c; background: #ffedd5;">08</div>
            </div>
            <div class="alert-box" style="border-left-color: #3b82f6;">
                <div>
                    <div class="alert-title">⚠️ Cảnh báo thiếu giờ CME</div>
                    <div class="alert-sub">Chưa tích lũy đủ 48 tiết / 2 năm</div>
                </div>
                <div class="alert-badge" style="color: #2563eb; background: #dbeafe;">25</div>
            </div>
            <div class="alert-box" style="border-left-color: #10b981;">
                <div>
                    <div class="alert-title">📜 GPHN cần cập nhật</div>
                    <div class="alert-sub">Bổ sung thông tin chứng chỉ mới</div>
                </div>
                <div class="alert-badge" style="color: #059669; background: #d1fae5;">04</div>
            </div>
        """, unsafe_allow_html=True)

    # ----- CỘT 2: BIỂU ĐỒ XY TỔNG NHÂN SỰ & TRÌNH ĐỘ CHUYÊN MÔN -----
    with sec2:
        st.subheader("📊 Nhân sự theo Trình độ")
        
        # Dữ liệu mẫu trình độ chuyên môn (Tổng 877 nhân sự)
        df_degree = pd.DataFrame({
            'Trình độ': ['Tiến sĩ / CKI', 'Thạc sĩ / CKI', 'Đại học', 'Cao đẳng', 'Trung cấp / Khác'],
            'Số lượng': [25, 142, 450, 180, 80]
        })
        
        # Biểu đồ XY dạng Cột màu sắc rực rỡ
        fig_degree = px.bar(
            df_degree, 
            x='Trình độ', 
            y='Số lượng', 
            text='Số lượng',
            color='Trình độ',
            color_discrete_sequence=px.colors.qualitative.Vivid
        )
        fig_degree.update_traces(textposition='outside', textfont_size=12)
        fig_degree.update_layout(
            showlegend=False,
            height=300,
            margin=dict(l=10, r=10, t=20, b=10),
            xaxis_title=None,
            yaxis_title="Số người",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_degree, use_container_width=True)

    # ----- CỘT 3: BIỂU ĐỒ TRÒN PHÂN LOẠI LOẠI HỢP ĐỒNG LAO ĐỘNG -----
    with sec3:
        st.subheader("🍩 Phân loại Hợp đồng")
        
        # Dữ liệu loại hợp đồng
        df_contract = pd.DataFrame({
            'Loại HĐLĐ': ['Không xác định thời hạn', 'Xác định thời hạn (1-3 năm)', 'Thử việc / Ngắn hạn'],
            'Số lượng': [520, 310, 47]
        })
        
        # Biểu đồ hình tròn Donut sống động
        fig_contract = px.pie(
            df_contract, 
            names='Loại HĐLĐ', 
            values='Số lượng', 
            hole=0.45,
            color_discrete_sequence=['#0284c7', '#f97316', '#10b981']
        )
        fig_contract.update_traces(textinfo='percent+value', textfont_size=12)
        fig_contract.update_layout(
            height=300,
            margin=dict(l=10, r=10, t=20, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_contract, use_container_width=True)
