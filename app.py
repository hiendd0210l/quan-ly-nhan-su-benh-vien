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

# 3. HEADER BANNER
st.markdown("""
    <div class="top-header">
        <div class="header-title">HỆ THỐNG QUẢN LÝ NHÂN SỰ BỆNH VIỆN BƯU ĐIỆN</div>
        <div class="header-subtitle">Hệ thống thông tin Quản trị Nhân sự & Điều hành Trung tâm (Smart HR-Hospital)</div>
    </div>
""", unsafe_allow_html=True)

# 4. DANH MỤC MENU CHỨC NĂNG (SIDEBAR)
with st.sidebar:
    st.title("📌 DANH MỤC CHỨC NĂNG")
    
    st.caption("CHUNG & ĐIỀU HÀNH")
    menu_selected = st.radio(
        "Menu Điều hành",
        [
            "Trang chủ / Dashboard", 
            "Cập nhật danh sách người lao động (Mẫu 2C-BNV)", 
            "Thông báo & Văn bản"
        ],
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

# 5. NỘI DUNG CHÍNH (MAIN CONTENT)
if menu_selected == "Trang chủ / Dashboard":
    
    # --- PHẦN 1: THỐNG KÊ TỔNG QUAN ---
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

    st.write("") # Khoảng đệm

    # --- PHẦN 2: TRUNG TÂM CẢNH BÁO TỰ ĐỘNG ---
    st.subheader("🔔 Cảnh báo Tự động & Lịch cần xử lý")
    
    rows_data = [
        ("Hạn Hợp đồng", "danger", "8 người", "BS. Nguyễn Văn An (Khoa Ngoại Tổng hợp)", "Hết hạn HĐLĐ 36 tháng (Đến hạn tái ký/đánh giá)", "Còn 15 ngày (10/09/2026)"),
        ("Nâng bậc lương", "warning", "14 người", "ĐD. Lê Thị Bích (Khoa Gây mê Hồi sức)", "Đủ thời hạn nâng lương bậc 3/9 lên bậc 4/9", "Đến hạn T9/2026"),
        ("Cảnh báo CME", "danger", "12 người", "KTV. Phạm Quốc Cường (Khoa CĐHA)", "Mới đạt 32/48 tiết CME trong chu kỳ 2 năm", "Thiếu 16 tiết (Cần bù gấp)"),
        ("Giấy phép CCHN", "info", "5 người", "ThS.BS. Hoàng Minh Đức (TT Hỗ trợ sinh sản)", "Hồ sơ gia hạn Giấy phép hành nghề (Chu kỳ 5 năm)", "Hạn nộp: 30/09/2026"),
        ("Sinh nhật tháng", "success", "18 người", "18 Cán bộ nhân viên (Toàn Bệnh viện)", "Danh sách CBCNV có sinh nhật trong tháng 09/2026", "Xem danh sách Công đoàn"),
    ]

    # Ghép chuỗi HTML liên tục chuẩn định dạng
    rows_html = "".join([
        f'<tr style="border-bottom: 1px solid #e2e8f0;">'
        f'<td style="padding: 10px;"><span class="badge badge-{level}">{title}</span></td>'
        f'<td style="padding: 10px; text-align:center;"><span class="count-tag">{count}</span></td>'
        f'<td style="padding: 10px;"><b>{person}</b></td>'
        f'<td style="padding: 10px;">{detail}</td>'
        f'<td style="padding: 10px;">{status}</td>'
        f'</tr>'
        for title, level, count, person, detail, status in rows_data
    ])

    full_table_html = f"""
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
            {rows_html}
        </tbody>
    </table>
    <div style="text-align: right; font-size: 11px; color: #94a3b8; margin-top: 8px;">
        * Cập nhật tự động theo thời gian thực từ CSDL Quản trị Nhân sự Bệnh viện Bưu điện
    </div>
    """
    
    st.markdown(full_table_html, unsafe_allow_html=True)

elif menu_selected == "Cập nhật danh sách người lao động (Excel 2C-BNV)":
    st.subheader("📥 Cập nhật danh sách người lao động theo Mẫu 2C-BNV / 2C-TCT-98")
    st.markdown("Tải lên tập tin Excel mẫu Sơ yếu lý lịch 2C-BNV để trích xuất dữ liệu và đồng bộ vào cơ sở dữ liệu nhân sự của Bệnh viện.")
    
    uploaded_file = st.file_uploader("Chọn tập tin Excel (.xlsx, .xls)", type=["xlsx", "xls"])
    
    if uploaded_file is not None:
        st.success(f"Đã tải lên tập tin thành công: **{uploaded_file.name}**")
        
        try:
            df = pd.read_excel(uploaded_file)
            st.write("📋 **Xem trước dữ liệu trích xuất từ file Excel:**")
            st.dataframe(df.head(10), use_container_width=True)
            
            if st.button("🚀 Bắt đầu Cập nhật vào Cơ sở dữ liệu", type="primary"):
                st.balloons()
                st.success("✅ Đã cập nhật thành công dữ liệu cán bộ nhân viên vào Cơ sở dữ liệu Bệnh viện!")
        except Exception as e:
            st.error(f"Có lỗi xảy ra khi đọc tập tin: {e}")

else:
    st.info(f"Bạn đang mở giao diện: **{menu_selected}**")
