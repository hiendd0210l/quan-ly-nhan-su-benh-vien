import streamlit as st
import pandas as pd

# 1. CẤU HÌNH TRANG (PAGE CONFIG)
st.set_page_config(
    page_title="Hệ thống Quản lý Nhân sự - Bệnh viện Bưu điện",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CUSTOM CSS CHO GIAO DIỆN CHUYÊN NGHIỆP
st.markdown("""
    <style>
        /* Header Banner */
        .top-header {
            background: linear-gradient(135deg, #0d3b66 0%, #00509d 100%);
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .header-title {
            font-size: 22px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin: 0;
        }
        .header-subtitle {
            font-size: 13px;
            opacity: 0.9;
            margin-top: 4px;
        }

        /* Metric Cards Custom Styling */
        .metric-card {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 12px 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            height: 100%;
        }
        .metric-primary { border-top: 4px solid #00509d; }
        .metric-info { border-top: 4px solid #2980b9; }
        .metric-success { border-top: 4px solid #27ae60; }
        .metric-warning { border-top: 4px solid #f39c12; }

        .metric-title {
            font-size: 12px;
            font-weight: bold;
            color: #64748b;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            color: #0f172a;
            margin-bottom: 8px;
        }
        .metric-detail {
            font-size: 12px;
            color: #475569;
            line-height: 1.5;
        }

        /* Badge Styling */
        .badge {
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: bold;
            display: inline-block;
        }
        .badge-danger { background-color: #fee2e2; color: #991b1b; }
        .badge-warning { background-color: #fef3c7; color: #92400e; }
        .badge-info { background-color: #e0f2fe; color: #075985; }
        .badge-success { background-color: #dcfce7; color: #166534; }
        
        .count-tag {
            background-color: #e2e8f0;
            color: #0f172a;
            font-weight: bold;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
        }
    </style>
""", unsafe_allow_html=True)

# 3. HEADER
st.markdown("""
    <div class="top-header">
        <div class="header-title">HỆ THỐNG QUẢN LÝ NHÂN SỰ BỆNH VIỆN BƯU ĐIỆN</div>
        <div class="header-subtitle">Hệ thống thông tin Quản trị Nhân sự & Điều hành Trung tâm (Smart HR-Hospital)</div>
    </div>
""", unsafe_allow_html=True)

# 4. CỬA SỔ BÊN TRÁI: DANH MỤC MENU CHỨC NĂNG (SIDEBAR)
with st.sidebar:
    st.title("📌 DANH MỤC CHỨC NĂNG")
    
    st.caption("CHUNG & ĐIỀU HÀNH")
    menu_selected = st.radio(
        "Menu Điều hành",
        ["Trang chủ / Dashboard", "Thông báo & Văn bản"],
        label_visibility="collapsed"
    )
    
    st.caption("QUẢN LÝ HỒ SƠ NHÂN SỰ")
    st.selectbox("Nghiệp vụ Hồ sơ", [
        "Hồ sơ Cán bộ CNV", 
        "Phân loại lao động", 
        "Hợp đồng Lao động", 
        "Hồ sơ Đảng viên"
    ], index=0, label_visibility="collapsed")
    
    st.caption("NGHIỆP VỤ CHUYÊN SÂU")
    st.selectbox("Nghiệp vụ Chuyên môn", [
        "Giấy phép hành nghề (GPHN) [5]",
        "Theo dõi Đào tạo CME [12]",
        "Nâng bậc lương & Ngạch",
        "Bố trí & Điều chuyển"
    ], index=0, label_visibility="collapsed")
    
    st.caption("BÁO CÁO & THỐNG KÊ")
    st.selectbox("Hệ thống Báo cáo", [
        "Báo cáo BYT/Sở Y tế và VNPT",
        "Thống kê Biến động NS",
        "Cấu hình Hệ thống"
    ], index=0, label_visibility="collapsed")

# 5. CỬA SỔ BÊN PHẢI (MAIN CONTENT)
if menu_selected == "Trang chủ / Dashboard":
    
    st.subheader("📊 Thống kê Tổng quan Toàn Bệnh viện")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="metric-card metric-primary">
                <div class="metric-title">Tổng số lao động</div>
                <div class="metric-value">877</div>
                <div class="metric-detail">
                    • Khối Lâm sàng: <b>512</b><br>
                    • Khối Cận lâm sàng: <b>210</b><br>
                    • Khối Phòng ban: <b>155</b>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="metric-card metric-info">
                <div class="metric-title">Trình độ chuyên môn</div>
                <div class="metric-value">100%</div>
                <div class="metric-detail">
                    • TS/CKII/ThS/CKI: <b>245</b> (28%)<br>
                    • Bác sĩ / Dược sĩ: <b>180</b> (20.5%)<br>
                    • ĐD/KTV Đại học: <b>320</b> (36.5%)<br>
                    • Trình độ khác: <b>132</b> (15%)
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="metric-card metric-success">
                <div class="metric-title">Phân loại hợp đồng</div>
                <div class="metric-value">877</div>
                <div class="metric-detail">
                    • HĐ Không xác định TH: <b>620</b><br>
                    • HĐ Xác định thời hạn: <b>215</b><br>
                    • Chuyên gia hưu trí: <b>42</b>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
            <div class="metric-card metric-warning">
                <div class="metric-title">Trạng thái & Đảng viên</div>
                <div class="metric-value">238 <span style="font-size:14px; font-weight:normal;">Đảng viên</span></div>
                <div class="metric-detail">
                    • Đang làm việc: <b>865</b> (98.6%)<br>
                    • Tạm hoãn/Nghỉ thai sản: <b>12</b><br>
                    • Tỷ lệ Đảng viên: <b>27.1%</b>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.write("")

    st.subheader("🔔 Cảnh báo Tự động & Lịch cần xử lý")
    
    alerts_data = [
        {
            "Loại cảnh báo": "Hạn Hợp đồng",
            "Mức độ": "danger",
            "Số người": "8 người",
            "Cán bộ đại diện / Đơn vị": "BS. Nguyễn Văn An (Khoa Ngoại Tổng hợp)",
            "Nội dung cảnh báo chi tiết": "Hết hạn HĐLĐ 36 tháng (Đến hạn tái ký/đánh giá)",
            "Thời hạn / Trạng thái": "Còn 15 ngày (10/09/2026)"
        },
        {
            "Loại cảnh báo": "Nâng bậc lương",
            "Mức độ": "warning",
            "Số người": "14 người",
            "Cán bộ đại diện / Đơn vị": "ĐD. Lê Thị Bích (Khoa Gây mê Hồi sức)",
            "Nội dung cảnh báo chi tiết": "Đủ thời hạn nâng lương bậc 3/9 lên bậc 4/9",
            "Thời hạn / Trạng thái": "Đến hạn T9/2026"
        },
        {
            "Loại cảnh báo": "Cảnh báo CME",
            "Mức độ": "danger",
            "Số người": "12 người",
            "Cán bộ đại diện / Đơn vị": "KTV. Phạm Quốc Cường (Khoa CĐHA)",
            "Nội dung cảnh báo chi tiết": "Mới đạt 32/48 tiết CME trong chu kỳ 2 năm",
            "Thời hạn / Trạng thái": "Thiếu 16 tiết (Cần bù gấp)"
        },
        {
            "Loại cảnh báo": "Giấy phép CCHN",
            "Mức độ": "info",
            "Số người": "5 người",
            "Cán bộ đại diện / Đơn vị": "ThS.BS. Hoàng Minh Đức (TT Hỗ trợ sinh sản)",
            "Nội dung cảnh báo chi tiết": "Hồ sơ gia hạn Giấy phép hành nghề (Chu kỳ 5 năm)",
            "Thời hạn / Trạng thái": "Hạn nộp: 30/09/2026"
        },
        {
            "Loại cảnh báo": "Sinh nhật tháng",
            "Mức độ": "success",
            "Số người": "18 người",
            "Cán bộ đại diện / Đơn vị": "18 Cán bộ nhân viên (Toàn Bệnh viện)",
            "Nội dung cảnh báo chi tiết": "Danh sách CBCNV có sinh nhật trong tháng 09/2026",
            "Thời hạn / Trạng thái": "Xem danh sách Công đoàn"
        }
    ]

    table_html = """
    <table style="width:100%; border-collapse: collapse; font-size: 13px;">
        <thead>
            <tr style="background-color: #f1f5f9; text-align: left; border-bottom: 2px solid #cbd5e1;">
                <th style="padding: 10px;">Loại cảnh báo</th>
                <th style="padding: 10px; text-align:center;">Số người</th>
                <th style="padding: 10px;">Cán bộ đại diện / Đơn vị</th>
                <th style="padding: 10px;">Nội dung cảnh báo chi tiết</th>
                <th style="padding: 10px;">Thời hạn / Trạng thái</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for row in alerts_data:
        table_html += f"""
        <tr style="border-bottom: 1px solid #e2e8f0;">
            <td style="padding: 10px;"><span class="badge badge-{row['Mức độ']}">{row['Loại cảnh báo']}</span></td>
            <td style="padding: 10px; text-align:center;"><span class="count-tag">{row['Số người']}</span></td>
            <td style="padding: 10px;"><b>{row['Cán bộ đại diện / Đơn vị']}</b></td>
            <td style="padding: 10px;">{row['Nội dung cảnh báo chi tiết']}</td>
            <td style="padding: 10px;">{row['Thời hạn / Trạng thái']}</td>
        </tr>
        """
        
    table_html += """
        </tbody>
    </table>
    <div style="text-align: right; font-size: 11px; color: #94a3b8; margin-top: 8px;">
        * Cập nhật tự động theo thời gian thực từ CSDL Quản trị Nhân sự Bệnh viện Bưu điện
    </div>
    """
    
    st.markdown(table_html, unsafe_allow_html=True)

else:
    st.info(f"Bạn đang mở giao diện: **{menu_selected}**")
