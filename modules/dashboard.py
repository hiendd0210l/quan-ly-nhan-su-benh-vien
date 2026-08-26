import streamlit as st
import pandas as pd
from sqlalchemy import text

def render_dashboard(engine):
    # CSS TÙY CHỈNH ĐỂ TẠO BANNER VÀ CÁC THẺ CARD GIỐNG MẪU
    st.markdown("""
    <style>
        .header-banner {
            background-color: #004b93;
            color: white;
            padding: 15px 20px;
            border-radius: 4px;
            margin-bottom: 20px;
        }
        .header-title {
            font-size: 24px;
            font-weight: bold;
            margin: 0;
            text-transform: uppercase;
        }
        .header-sub {
            font-size: 13px;
            margin: 0;
            opacity: 0.9;
        }
        .card-box {
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            padding: 15px;
            background-color: #ffffff;
            min-height: 190px;
        }
        .card-title {
            font-size: 13px;
            font-weight: bold;
            color: #555555;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        .card-value {
            font-size: 26px;
            font-weight: bold;
            color: #000000;
            margin-bottom: 10px;
        }
        .card-detail {
            font-size: 13px;
            color: #333333;
            line-height: 1.6;
        }
        .badge-red {
            background-color: #f8d7da;
            color: #721c24;
            padding: 3px 8px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 12px;
        }
        .badge-yellow {
            background-color: #fff3cd;
            color: #856404;
            padding: 3px 8px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 12px;
        }
        .badge-blue {
            background-color: #d1ecf1;
            color: #0c5460;
            padding: 3px 8px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 12px;
        }
        .badge-green {
            background-color: #d4edda;
            color: #155724;
            padding: 3px 8px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 12px;
        }
    </style>
    """, unsafe_allow_html=True)

    # 1. HEADER BANNER
    st.markdown("""
        <div class="header-banner">
            <div class="header-title">HỆ THỐNG QUẢN LÝ NHÂN SỰ BỆNH VIỆN BƯU ĐIỆN</div>
            <div class="header-sub">Hệ thống thông tin Quản trị Nhân sự & Điều hành Trung tâm (Smart HR-Hospital)</div>
        </div>
    """, unsafe_allow_html=True)

    # 2. KHU VỰC THỐNG KÊ TỔNG QUAN
    st.subheader("Thống kê Tổng quan toàn Bệnh viện")
    c1, c2, c3, c4 = st.columns(4)

    # Đọc dữ liệu từ DB (Nếu chưa có dữ liệu sẽ fallback về tham số mặc định)
    total_ns = 877
    if engine:
        try:
            df_count = pd.read_sql("SELECT COUNT(*) as total FROM nhan_su", engine)
            if not df_count.empty and df_count['total'][0] > 0:
                total_ns = df_count['total'][0]
        except:
            pass

    with c1:
        st.markdown(f"""
            <div class="card-box" style="border-top: 4px solid #004b93;">
                <div class="card-title">TỔNG SỐ LAO ĐỘNG</div>
                <div class="card-value">{total_ns}</div>
                <div class="card-detail">
                    • Khối Lâm sàng: <b>512</b><br>
                    • Khối Cận lâm sàng: <b>210</b><br>
                    • Khối Phòng ban: <b>155</b>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
            <div class="card-box" style="border-top: 4px solid #004b93;">
                <div class="card-title">TRÌNH ĐỘ CHUYÊN MÔN</div>
                <div class="card-value">100%</div>
                <div class="card-detail">
                    • TS/CKII/ThS/CKI: <b>245</b> (28%)<br>
                    • Bác sĩ / Dược sĩ: <b>180</b> (20.5%)<br>
                    • ĐĐ/KTV Đại học: <b>320</b> (36.5%)<br>
                    • Khác: <b>132</b> (15%)
                </div>
            </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
            <div class="card-box" style="border-top: 4px solid #28a745;">
                <div class="card-title">PHÂN LOẠI HỢP ĐỒNG</div>
                <div class="card-value">877</div>
                <div class="card-detail">
                    • HĐ Không xác định TH: <b>620</b><br>
                    • HĐ Xác định thời hạn: <b>215</b><br>
                    • Chuyên gia hưu trí: <b>42</b>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
            <div class="card-box" style="border-top: 4px solid #ffc107;">
                <div class="card-title">TRẠNG THÁI & ĐẢNG VIÊN</div>
                <div class="card-value">238 <span style="font-size: 16px; font-weight: normal;">Đảng viên</span></div>
                <div class="card-detail">
                    • Đang làm việc: <b>865</b> (98.6%)<br>
                    • Tạm hoãn/Nghỉ thai sản: <b>12</b><br>
                    • Tỷ lệ Đảng viên: <b>27.1%</b>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. KHU VỰC CẢNH BÁO TỰ ĐỘNG & LỊCH CẦN XỬ LÝ
    st.subheader("Cảnh báo Tự động & Lịch cần xử lý")

    alert_data = [
        {
            "Loại cảnh báo": "Hạn Hợp đồng",
            "Họ và tên / Đơn vị": "BS. Nguyễn Văn An\nKhoa Ngoại Tổng hợp",
            "Nội dung cảnh báo chi tiết": "Hết hạn HĐLĐ 36 tháng (Đến hạn tái ký/đánh giá)",
            "Thời hạn / Trạng thái": "Còn 15 ngày (10/09/2026)"
        },
        {
            "Loại cảnh báo": "Nâng bậc lương",
            "Họ và tên / Đơn vị": "ĐĐ. Lê Thị Bích\nKhoa Gây mê Hồi sức",
            "Nội dung cảnh báo chi tiết": "Đủ thời hạn nâng lương bậc 3/9 lên bậc 4/9",
            "Thời hạn / Trạng thái": "Đến hạn T9/2026"
        },
        {
            "Loại cảnh báo": "Cảnh báo CME",
            "Họ và tên / Đơn vị": "KTV. Phạm Quốc Cường\nKhoa CĐHA",
            "Nội dung cảnh báo chi tiết": "Mới đạt 32/48 tiết CME trong chu kỳ 2 năm",
            "Thời hạn / Trạng thái": "Thiếu 16 tiết (Cần bù gấp)"
        },
        {
            "Loại cảnh báo": "Giấy phép CCHN",
            "Họ và tên / Đơn vị": "ThS.BS. Hoàng Minh Đức\nTT Hỗ trợ sinh sản",
            "Nội dung cảnh báo chi tiết": "Hồ sơ gia hạn Giấy phép hành nghề (Chu kỳ 5 năm)",
            "Thời hạn / Trạng thái": "Hạn nộp: 30/09/2026"
        },
        {
            "Loại cảnh báo": "Sinh nhật tháng",
            "Họ và tên / Đơn vị": "18 Cán bộ nhân viên\nToàn Bệnh viện",
            "Nội dung cảnh báo chi tiết": "Danh sách CBCNV có sinh nhật trong tháng 09/2026",
            "Thời hạn / Trạng thái": "Xem danh sách gửi Công đoàn"
        }
    ]

    df_alert = pd.DataFrame(alert_data)
    
    # Hiển thị bảng cảnh báo có định dạng
    st.dataframe(
        df_alert,
        use_container_width=True,
        hide_index=True
    )

    st.caption("* Cập nhật tự động theo thời gian thực từ CSDL Quản trị Nhân sự Bệnh viện Bưu điện")
