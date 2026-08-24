import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. CẤU HÌNH TRANG WEB
st.set_page_config(page_title="Hệ thống Quản lý Nhân sự Bệnh viện", layout="wide")

# 2. KHỞI TẠO DỮ LIỆU TRONG SESSION STATE (Lưu tạm bộ nhớ)
if 'df_nhansu' not in st.session_state:
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
    st.session_state.df_nhansu = df

df = st.session_state.df_nhansu
today = pd.to_datetime(datetime.now().date())

# 3. GIAO DIỆN CHÍNH & THANH MENU
st.title("🏥 HỆ THỐNG QUẢN LÝ NHÂN SỰ BỆNH VIỆN")
menu = st.sidebar.radio("CHỨC NĂNG HỆ THỐNG", [
    "📊 Tổng quan & Cảnh báo", 
    "📋 Danh sách Hồ sơ Nhân sự", 
    "➕ Thêm mới Nhân sự",
    "📂 Nhập Dữ liệu từ Excel",
    "📥 Xuất Báo cáo Excel"
])

# ----------------------------------------------------
# PHÂN HỆ 1: TỔNG QUAN & CẢNH BÁO TỰ ĐỘNG
# ----------------------------------------------------
if menu == "📊 Tổng quan & Cảnh báo":
    st.header("🔔 TRUNG TÂM CẢNH BÁO TỰ ĐỘNG")
    
    df_luong = df[(df['Ngày nâng lương tiếp'] >= today) & (df['Ngày nâng lương tiếp'] <= today + timedelta(days=60))]
    df_hd = df[(df['Ngày hết hạn HĐ'] >= today) & (df['Ngày hết hạn HĐ'] <= today + timedelta(days=30))]
    df_cme = df[df['Giờ CME lũy kế'] < 48]
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tổng số Nhân sự", f"{len(df)} người")
    col2.metric("Sắp nâng lương (60 ngày)", f"{len(df_luong)} người")
    col3.metric("Hợp đồng sắp hết hạn (30 ngày)", f"{len(df_hd)} người")
    col4.metric("Thiếu giờ CME (<48 tiết)", f"{len(df_cme)} người")
    
    st.markdown("---")
    
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
    st.header("📋 DANH SÁCH HỒ SƠ NHÂN SỰ")
    
    col_search, col_filter = st.columns([2, 1])
    with col_search:
        search_term = st.text_input("🔍 Tìm kiếm nhanh (Nhập Tên hoặc Mã NV):")
    with col_filter:
        khoa_list = ["Tất cả Khoa/Phòng"] + list(df["Khoa/Phòng"].unique())
        selected_khoa = st.selectbox("Lọc theo Khoa/Phòng:", khoa_list)
        
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
# PHÂN HỆ 3: THÊM MỚI NHÂN SỰ
# ----------------------------------------------------
elif menu == "➕ Thêm mới Nhân sự":
    st.header("➕ THÊM HỒ SƠ NHÂN SỰ MỚI")
    
    with st.form("add_employee_form"):
        col1, col2 = st.columns(2)
        with col1:
            ma_nv = st.text_input("Mã Nhân viên (VD: BV0004):")
            ho_ten = st.text_input("Họ và Tên:")
            khoa = st.selectbox("Khoa / Phòng:", ["Khoa Cấp cứu", "Khoa Khám bệnh", "Khoa Ngoại tổng hợp", "Khoa Nội", "Phòng TCHĐ"])
            chuc_vu = st.text_input("Chức vụ / Chức danh:")
            loai_hd = st.selectbox("Loại Hợp đồng:", ["Thử việc", "Xác định thời hạn", "Không xác định thời hạn"])
        
        with col2:
            ngay_hd = st.date_input("Ngày hết hạn Hợp đồng:")
            he_so_luong = st.number_input("Hệ số lương:", min_value=1.0, max_value=10.0, value=2.34, step=0.01)
            ngay_luong = st.date_input("Mốc nâng lương tiếp theo:")
            gio_cme = st.number_input("Số tiết CME đã tích lũy:", min_value=0, max_value=200, value=0)
            trang_thai = st.selectbox("Trạng thái:", ["Đang làm việc", "Nghỉ thai sản", "Đã nghỉ việc"])
            
        submit_button = st.form_submit_button("💾 Lưu Hồ Sơ Nhân Sự")
        
        if submit_button:
            new_data = {
                "Mã NV": ma_nv, "Họ tên": ho_ten, "Khoa/Phòng": khoa, "Chức vụ": chuc_vu,
                "Loại HĐ": loai_hd, "Ngày hết hạn HĐ": pd.to_datetime(ngay_hd),
                "Hệ số lương": he_so_luong, "Ngày nâng lương tiếp": pd.to_datetime(ngay_luong),
                "Giờ CME lũy kế": gio_cme, "Trạng thái": trang_thai
            }
            st.session_state.df_nhansu = pd.concat([st.session_state.df_nhansu, pd.DataFrame([new_data])], ignore_index=True)
            st.success(f"Đã thêm thành công nhân sự {ho_ten} vào hệ thống!")

# ----------------------------------------------------
# PHÂN HỆ 4: NHẬP EXCEL HÀNG LOẠT
# ----------------------------------------------------
elif menu == "📂 Nhập Dữ liệu từ Excel":
    st.header("📂 NHẬP DANH SÁCH 1.500 NHÂN SỰ TỪ FILE EXCEL / CSV")
    st.write("Tải lên file danh sách nhân sự của bệnh viện để cập nhật vào phần mềm:")
    
    uploaded_file = st.file_uploader("Chọn file Excel (.xlsx) hoặc CSV (.csv)", type=["csv", "xlsx"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df_upload = pd.read_csv(uploaded_file)
            else:
                df_upload = pd.read_excel(uploaded_file)
                
            st.write("📋 **Xem trước dữ liệu tải lên:**")
            st.dataframe(df_upload.head(10))
            
            if st.button("🚀 Xác nhận Nạp dữ liệu vào Hệ thống"):
                df_upload['Ngày nâng lương tiếp'] = pd.to_datetime(df_upload['Ngày nâng lương tiếp'])
                df_upload['Ngày hết hạn HĐ'] = pd.to_datetime(df_upload['Ngày hết hạn HĐ'])
                st.session_state.df_nhansu = df_upload
                st.success(f"Đã nạp thành công {len(df_upload)} hồ sơ nhân sự vào phần mềm!")
        except Exception as e:
            st.error(f"Lỗi khi đọc file: {e}. Vui lòng kiểm tra lại định dạng file.")

# ----------------------------------------------------
# PHÂN HỆ 5: XUẤT BÁO CÁO EXCEL
# ----------------------------------------------------
elif menu == "📥 Xuất Báo cáo Excel":
    st.header("📥 XUẤT BÁO CÁO HỒ SƠ NHÂN SỰ")
    st.write("Bấm nút bên dưới để tải về toàn bộ danh sách nhân sự hiện tại:")
    
    csv_data = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📄 Tải về danh sách Excel (.CSV)",
        data=csv_data,
        file_name='Danh_sach_nhan_su_Benh_vien.csv',
        mime='text/csv',
    )
