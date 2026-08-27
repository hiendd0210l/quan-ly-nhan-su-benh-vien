import streamlit as st
import pandas as pd

def render_dashboard(engine, user_info=None):
    fullname = user_info.get("fullname", "Đoàn Danh Hiển") if user_info else "Đoàn Danh Hiển"
    role = user_info.get("role", "Quản trị viên Hệ thống — Bệnh viện Bưu điện") if user_info else "Quản trị viên Hệ thống — Bệnh viện Bưu điện"
    avatar_data = user_info.get("avatar") if user_info else ""

    st.markdown("""
        <style>
            .welcome-card {
                display: flex;
                align-items: center;
                gap: 20px;
                background-color: #ffffff;
                padding: 20px 24px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.06);
                border: 1px solid #e2e8f0;
                margin-bottom: 25px;
            }
            .avatar-img {
                width: 85px;
                height: 85px;
                border-radius: 50%;
                object-fit: cover;
                border: 3px solid #0056b3;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            .dash-card {
                padding: 20px;
                border-radius: 12px;
                color: white !important;
                margin-bottom: 15px;
                min-height: 140px;
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
            .card-title { font-size: 16px; font-weight: 800; text-transform: uppercase; }
            .card-desc { font-size: 12.5px; opacity: 0.9; margin-top: 6px; }
            .card-action { font-size: 12px; font-weight: 700; text-align: right; text-transform: uppercase; }
        </style>
    """, unsafe_allow_html=True)

    # KHỐI XIN CHÀO VỚI ẢNH BASE64
    st.markdown(f"""
        <div class="welcome-card">
            <img src="{avatar_data}" class="avatar-img" alt="Avatar Admin">
            <div>
                <div style="font-size: 26px; font-weight: 800; color: #1e293b;">Xin chào, {fullname}</div>
                <div style="font-size: 14px; color: #64748b; font-weight: 500; margin-top: 4px;">{role}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # CÁC THẺ CHỨC NĂNG
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

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📌 Cảnh báo Tự động & Lịch cần xử lý")

    alerts_data = [
        {"Loại cảnh báo": "Hạn Hợp đồng", "Họ và tên / Đơn vị": "BS. Nguyễn Văn An (Khoa Ngoại TH)", "Nội dung chi tiết": "Hết hạn HĐLĐ 36 tháng (Đến hạn tái ký/đánh giá)", "Thời hạn / Trạng thái": "Còn 15 ngày (10/09/2026)"},
        {"Loại cảnh báo": "Nâng bậc lương", "Họ và tên / Đơn vị": "ĐĐ. Lê Thị Bích (Khoa GMHS)", "Nội dung chi tiết": "Đủ thời hạn nâng lương bậc 3/9 lên bậc 4/9", "Thời hạn / Trạng thái": "Đến hạn T9/2026"},
        {"Loại cảnh báo": "Cảnh báo CME", "Họ và tên / Đơn vị": "KTV. Phạm Quốc Cường (Khoa CĐHA)", "Nội dung chi tiết": "Mới đạt 12/48 tiết CME trong chu kỳ 2 năm", "Thời hạn / Trạng thái": "Thiếu 36 tiết (Cần bổ sung)"}
    ]
    st.dataframe(pd.DataFrame(alerts_data), use_container_width=True, hide_index=True)
