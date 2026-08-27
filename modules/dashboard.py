import streamlit as st
import pandas as pd

def render_dashboard(engine, user_info=None):
    # Lấy thông tin user nếu có, nếu không lấy mặc định
    user_name = user_info.get("name", "admin") if user_info else "admin"
    user_role = user_info.get("role", "Hệ thống Quản trị Nhân sự & Điều hành — Bệnh viện Bưu điện") if user_info else "Hệ thống Quản trị Nhân sự"
    user_avatar = user_info.get("avatar", "https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=200&auto=format&fit=crop") if user_info else "https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=200&auto=format&fit=crop"

    # CSS TÙY CHỈNH THEO CONCEPT CÁNH CAM / BAMBOOHR
    st.markdown("""
    <style>
        /* Profile Header */
        .profile-container {
            display: flex;
            align-items: center;
            background-color: #ffffff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            margin-bottom: 25px;
        }
        .profile-avatar {
            width: 85px;
            height: 85px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid #0056b3;
            margin-right: 20px;
        }
        .profile-greeting {
            font-size: 32px;
            font-weight: 700;
            color: #2b3a4a;
            margin: 0;
            line-height: 1.2;
        }
        .profile-role {
            font-size: 16px;
            color: #6c757d;
            margin-top: 4px;
            font-weight: 500;
        }

        /* Metro Tile Cards */
        .tile-card {
            border-radius: 10px;
            padding: 22px;
            color: white;
            min-height: 180px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            margin-bottom: 20px;
        }
        .tile-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        }
        .tile-icon {
            font-size: 32px;
            margin-bottom: 10px;
        }
        .tile-title {
            font-size: 16px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }
        .tile-desc {
            font-size: 13px;
            opacity: 0.92;
            line-height: 1.4;
            flex-grow: 1;
        }
        .tile-action {
            font-size: 13px;
            font-weight: bold;
            text-align: right;
            margin-top: 15px;
            letter-spacing: 1px;
        }

        /* Màu nền riêng cho từng khối */
        .bg-red { background: linear-gradient(135deg, #ea5455, #e35d6a); }
        .bg-teal { background: linear-gradient(135deg, #1cb14b, #20c997); }
        .bg-blue { background: linear-gradient(135deg, #2b70e4, #3b82f6); }
        .bg-dark { background: linear-gradient(135deg, #343a40, #495057); }
        .bg-orange { background: linear-gradient(135deg, #fd7e14, #ff922b); }
        .bg-green { background: linear-gradient(135deg, #20c997, #0ca678); }
    </style>
    """, unsafe_allow_html=True)

    # 1. HEADER CHÀO MỪNG DỰA TRÊN THÔNG TIN ĐĂNG NHẬP
    st.markdown(f"""
        <div class="profile-container">
            <img class="profile-avatar" src="{user_avatar}" alt="User Avatar">
            <div>
                <div class="profile-greeting">Xin chào, {user_name}</div>
                <div class="profile-role">{user_role}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 2. HÀNG 1 CÁC KHỐI THẺ CHỨC NĂNG (METRO TILES - ROW 1)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
            <div class="tile-card bg-red">
                <div>
                    <div class="tile-icon">📇</div>
                    <div class="tile-title">HỒ SƠ CÁN BỘ CNV</div>
                    <div class="tile-desc">Theo dõi, cập nhật và quản lý toàn bộ danh sách hồ sơ 877 nhân sự toàn bệnh viện.</div>
                </div>
                <div class="tile-action">XEM CHI TIẾT ➔</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="tile-card bg-teal">
                <div>
                    <div class="tile-icon">📊</div>
                    <div class="tile-title">BÁO CÁO & THỐNG KÊ</div>
                    <div class="tile-desc">Truy xuất dữ liệu báo cáo BYT, Sở Y tế và biến động nhân sự theo thời gian thực.</div>
                </div>
                <div class="tile-action">XEM BÁO CÁO ➔</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="tile-card bg-blue">
                <div>
                    <div class="tile-icon">📜</div>
                    <div class="tile-title">GPHN & ĐÀO TẠO CME</div>
                    <div class="tile-desc">Quản lý Chứng chỉ hành nghề và tiến độ tích lũy 48 tiết CME của Bác sĩ / Điều dưỡng.</div>
                </div>
                <div class="tile-action">XEM CHI TIẾT ➔</div>
            </div>
        """, unsafe_allow_html=True)

    # 3. HÀNG 2 CÁC KHỐI THẺ CHỨC NĂNG (METRO TILES - ROW 2)
    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown("""
            <div class="tile-card bg-dark">
                <div>
                    <div class="tile-icon">📝</div>
                    <div class="tile-title">HỢP ĐỒNG LAO ĐỘNG</div>
                    <div class="tile-desc">Theo dõi hợp đồng xác định thời hạn, không xác định thời hạn và lịch tái ký.</div>
                </div>
                <div class="tile-action">QUẢN LÝ HĐ ➔</div>
            </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown("""
            <div class="tile-card bg-orange">
                <div>
                    <div class="tile-icon">💰</div>
                    <div class="tile-title">NÂNG BẬC LƯƠNG & NGẠCH</div>
                    <div class="tile-desc">Quản lý hệ số lương, ngạch viên chức và cảnh báo danh sách đủ điều kiện nâng lương.</div>
                </div>
                <div class="tile-action">XEM DANH SÁCH ➔</div>
            </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown("""
            <div class="tile-card bg-green">
                <div>
                    <div class="tile-icon">🩺</div>
                    <div class="tile-title">QUẢN LÝ BHXH & SỨC KHỎE</div>
                    <div class="tile-desc">Theo dõi chế độ Bảo hiểm xã hội, đóng BHXH và đợt khám sức khỏe định kỳ.</div>
                </div>
                <div class="tile-action">CHI TIẾT ➔</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. KHU VỰC CẢNH BÁO TỰ ĐỘNG BÊN DƯỚI
    st.subheader("📌 Cảnh báo Tự động & Lịch cần xử lý")
    
    alert_data = [
        {
            "Loại cảnh báo": "Hạn Hợp đồng",
            "Họ và tên / Đơn vị": "BS. Nguyễn Văn An (Khoa Ngoại TH)",
            "Nội dung chi tiết": "Hết hạn HĐLĐ 36 tháng (Đến hạn tái ký/đánh giá)",
            "Thời hạn / Trạng thái": "Còn 15 ngày (10/09/2026)"
        },
        {
            "Loại cảnh báo": "Nâng bậc lương",
            "Họ và tên / Đơn vị": "ĐĐ. Lê Thị Bích (Khoa GMHS)",
            "Nội dung chi tiết": "Đủ thời hạn nâng lương bậc 3/9 lên bậc 4/9",
            "Thời hạn / Trạng thái": "Đến hạn T9/2026"
        },
        {
            "Loại cảnh báo": "Cảnh báo CME",
            "Họ và tên / Đơn vị": "KTV. Phạm Quốc Cường (Khoa CĐHA)",
            "Nội dung chi tiết": "Mới đạt 32/48 tiết CME trong chu kỳ 2 năm",
            "Thời hạn / Trạng thái": "Thiếu 16 tiết (Cần bù gấp)"
        }
    ]
    st.dataframe(pd.DataFrame(alert_data), use_container_width=True, hide_index=True)
