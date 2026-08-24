import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. CẤU HÌNH TRANG WEB
st.set_page_config(page_title="Hệ thống Quản lý Nhân sự Bệnh viện", layout="wide")

# 2. KHỞI TẠO DỮ LIỆU MẪU (1500 nhân sự mô phỏng)
@st.cache_data
def load_data():
    data = [
        {
            "Mã NV": "BV0001", "Họ tên": "Nguyễn Văn An", "Khoa/Phòng": "Khoa Cấp cứu", "Chức vụ": "Bác sĩ CKI",
            "Loại HĐ": "Không xác định thời hạn", "Ngày hết hạn HĐ": "2030-12-31", 
            "Hệ số lương": 4.40, "Ngày nâng lương tiếp": "2026-09-15", "Giờ CME lũy kế": 32, "Trạng thái": "Đang làm việc"
        },
        {
            "Mã NV": "BV0002", "Họ tên": "Trần Thị Bích", "Khoa/Phòng": "Khoa Khám bệnh", "Chức vụ": "Điều dưỡng viên",
            "Loại HĐ": "Xác định thời hạn", "Ngày hết hạn HĐ": "2026-09-01", 
            "Hệ số lương": 2.67, "Ngày nâng lương tiếp": "2027-01-10", "Giờ CME lũy kế": 50, "Trạng thái": "Đang làm việc"
        },
        {
            "Mã NV": "BV0003", "Họ tên": "Lê Hoàng Nam", "Khoa/Phòng": "Khoa Ngoại tổng hợp", "Chức vụ": "Bác sĩ CKII",
            "Loại HĐ": "Không xác định thời hạn", "Ngày hết hạn HĐ": "2035-05-20", 
            "Hệ số lương": 5.08, "Ngày nâng lương tiếp": "2026-08-30", "Giờ CME lũy kế": 20, "Trạng thái": "Đang làm việc"
        }
    ]
    df = pd.DataFrame(data)
    df['Ngày nâng lương tiếp'] = pd.to_datetime(df['Ngày nâng lương tiếp'])
    df['Ngày hết hạn HĐ'] = pd.to_datetime(df['Ngày hết hạn HĐ'])
    return df

df = load_data()

# 3. GIAO DIỆN CHÍNH & THANH MENU
st.title("🏥 HỆ THỐNG QUẢN LÝ NHÂN SỰ BỆNH VIỆN")
menu = st.sidebar.radio("CHỨC NĂNG HỆ THỐNG", ["📊 Tổng quan & Cảnh báo", "📋 Danh sách Hồ sơ Nhân sự", "📥 Xuất Báo cáo Excel"])

today = pd.to_datetime(datetime.now().date())

# ----------------------------------------------------
# PHÂN HỆ 1: TỔNG QUAN & CẢNH BÁO TỰ ĐỘNG
# ----------------------------------------------------
if menu == "📊 Tổng quan & Cảnh báo":
    st.header("🔔 TRUNG TÂM CẢNH BÁO TỰ ĐỘNG")
    
    # Tính toán các chỉ số cảnh báo
    df_luong = df[(df['Ngày nâng lương tiếp'] >= today) & (df['Ngày nâng lương tiếp'] <= today + timedelta(days=60))]
    df_hd = df[(df['Ngày hết hạn HĐ'] >= today) & (df['Ngày hết hạn HĐ'] <= today + timedelta(days=30))]
    df_cme = df[df['Giờ CME lũy kế'] < 48]
    
    # Hiển thị các thẻ chỉ số (Metrics)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tổng số Nhân sự", f"{len(df)} người")
    col2.metric("Sắp nâng lương (60 ngày)", f"{len(df_luong)} người", delta_color="inverse")
    col3.metric("Hợp đồng sắp hết hạn (30 ngày)", f"{len(df_hd)} người", delta_color="inverse")
    col4.metric("Thiếu giờ CME (<48 tiết)", f"{len(df_cme)} người", delta_color="inverse")
    
    st.markdown("---")
    
    # Hiển thị danh sách chi tiết các cảnh báo
    st.subheader("📌 Danh sách Nhân sự sắp nâng bậc lương trong 60 ngày tới")
    if not df_luong.empty:
        st.dataframe(df_luong[['Mã NV', 'Họ tên', 'Khoa/Phòng', 'Hệ số lương', 'Ngày nâng lương tiếp']], use_container_width=True)
    else:
        st.success("Không có nhân sự nào sắp đến hạn nâng lương trong 60 ngày tới.")
        
    st.subheader("📌 Danh sách Bác sĩ / Điều dưỡng thiếu giờ đào tạo CME (<48 tiết)")
    st.dataframe(df_cme[['Mã NV', 'Họ tên', 'Khoa/Phòng', 'Chức vụ', 'Giờ CME lũy kế']], use_container_width=True)

# ----------------------------------------------------
# PHÂN HỆ 2: DANH SÁCH HỒ SƠ & TÌM KIẾM
# ----------------------------------------------------
elif menu == "📋 Danh sách Hồ sơ Nhân sự":
    st.header("📋 DANH SÁCH HỒ SƠ 1.500 NHÂN SỰ")
    
    # Thanh tìm kiếm và bộ lọc
    col_search, col_filter = st.columns([2, 1])
    with col_search:
        search_term = st.text_input("🔍 Tìm kiếm nhanh (Nhập Tên hoặc Mã NV):")
    with col_filter:
        khoa_list = ["Tất cả Khoa/Phòng"] + list(df["Khoa/Phòng"].unique())
        selected_khoa = st.selectbox("Lọc theo Khoa/Phòng:", khoa_list)
        
    # Áp dụng bộ lọc
    filtered_df = df.copy()
    if search_term:
        filtered_df = filtered_df[
            filtered_df['Họ tên'].str.contains(search_term, case=False, na=False) | 
            filtered_df['Mã NV'].str.contains(search_term, case=False, na=False)
        ]
    if selected_khoa != "Tất cả Khoa/Phòng":
        filtered_df = filtered_df[filtered_df['Khoa/Phòng'] == selected_khoa]
        
    st.dataframe(filtered_df, use_container_width=True)

# ----------------------------------------------------
# PHÂN HỆ 3: XUẤT BÁO CÁO EXCEL
# ----------------------------------------------------
elif menu == "📥 Xuất Báo cáo Excel":
    st.header("📥 XUẤT BÁO CÁO HỒ SƠ NHÂN SỰ")
    st.write("Bấm nút bên dưới để tải về danh sách toàn bộ nhân sự chuẩn file Excel:")
    
    # Chuyển đổi dữ liệu sang Excel để tải về
    @st.cache_data
    def convert_df(df_to_export):
        return df_to_export.to_csv(index=False).encode('utf-8-sig')

    csv_data = convert_df(df)
    st.download_button(
        label="📄 Tải về danh sách Excel (.CSV)",
        data=csv_data,
        file_name='Danh_sach_nhan_su_Benh_vien.csv',
        mime='text/csv',
    )
