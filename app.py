import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io

# 1. CẤU HÌNH TRANG WEB
st.set_page_config(page_title="Hệ thống Quản lý Nhân sự Bệnh viện - Mẫu 2C-BNV", layout="wide")

# 2. KHỞI TẠO DỮ LIỆU BAN ĐẦU
def get_initial_data():
    return [
        {
            "Ma_NV": "BV0001", "Ho_Ten": "Nguyễn Văn An", "Gioi_Tinh": "Nam", "Ngay_Sinh": "1980-05-15",
            "So_CCCD": "001080012345", "Khoa_Phong": "Khoa Cấp cứu", "Chuc_Vu": "Trưởng khoa",
            "Ngach_Vien_Chuc": "Bác sĩ chính (V.08.01.01)", "Trinh_Do_Chuyen_Mon": "Bác sĩ CKII",
            "Ly_Luan_Chinh_Tri": "Cao cấp", "So_CCHN": "001234/BYT-CCHN", "Gio_CME": 52,
            "Loai_HD": "Không xác định thời hạn", "Ngay_Het_Han_HD": "2035-12-31",
            "Bac_Luong": 3, "He_So_Luong": 5.08, "Ngay_Nang_Luong": "2026-09-15", "Trang_Thai": "Đang làm việc"
        },
        {
            "Ma_NV": "BV0002", "Ho_Ten": "Trần Thị Bích", "Gioi_Tinh": "Nữ", "Ngay_Sinh": "1992-08-20",
            "So_CCCD": "001192098765", "Khoa_Phong": "Khoa Khám bệnh", "Chuc_Vu": "Điều dưỡng viên",
            "Ngach_Vien_Chuc": "Điều dưỡng hạng III (V.08.05.12)", "Trinh_Do_Chuyen_Mon": "Cử nhân Điều dưỡng",
            "Ly_Luan_Chinh_Tri": "Sơ cấp", "So_CCHN": "005678/BYT-CCHN", "Gio_CME": 30,
            "Loai_HD": "Xác định thời hạn", "Ngay_Het_Han_HD": "2026-09-10",
            "Bac_Luong": 2, "He_So_Luong": 2.67, "Ngay_Nang_Luong": "2027-01-10", "Trang_Thai": "Đang làm việc"
        }
    ]

if 'df_nhansu' not in st.session_state or 'Ngay_Nang_Luong' not in st.session_state.df_nhansu.columns:
    df_temp = pd.DataFrame(get_initial_data())
    df_temp['Ngay_Nang_Luong'] = pd.to_datetime(df_temp['Ngay_Nang_Luong'])
    df_temp['Ngay_Het_Han_HD'] = pd.to_datetime(df_temp['Ngay_Het_Han_HD'])
    st.session_state.df_nhansu = df_temp

df = st.session_state.df_nhansu
today = pd.to_datetime(datetime.now().date())

# 3. GIAO DIỆN CHÍNH
st.title("🏥 QUẢN LÝ HỒ SƠ LÝ LỊCH NHÂN SỰ BỆNH VIỆN (CHUẨN 2C-BNV)")
menu = st.sidebar.radio("CHỨC NĂNG HỆ THỐNG", [
    "📊 Trung tâm Cảnh báo", 
    "📋 Danh sách Hồ sơ Lý lịch 2C", 
    "📂 Nhập/Xuất File Excel Mẫu 2C"
])

# ----------------------------------------------------
# PHÂN HỆ 1: CẢNH BÁO
# ----------------------------------------------------
if menu == "📊 Trung tâm Cảnh báo":
    st.header("🔔 CẢNH BÁO TỰ ĐỘNG THỜI HẠN & ĐÀO TẠO")
    
    df_luong = df[(df['Ngay_Nang_Luong'] >= today) & (df['Ngay_Nang_Luong'] <= today + timedelta(days=60))]
    df_hd = df[(df['Ngay_Het_Han_HD'] >= today) & (df['Ngay_Het_Han_HD'] <= today + timedelta(days=30))]
    df_cme = df[df['Gio_CME'] < 48]
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tổng Nhân sự", f"{len(df)} người")
    c2.metric("Sắp nâng lương (60 ngày)", f"{len(df_luong)} người")
    c3.metric("HĐ sắp hết hạn (30 ngày)", f"{len(df_hd)} người")
    c4.metric("Thiếu giờ CME (<48h)", f"{len(df_cme)} người")
    
    st.markdown("---")
    st.subheader("📌 Cảnh báo nâng lương trong 60 ngày tới")
    st.dataframe(df_luong[['Ma_NV', 'Ho_Ten', 'Khoa_Phong', 'He_So_Luong', 'Ngay_Nang_Luong']], use_container_width=True)

# ----------------------------------------------------
# PHÂN HỆ 2: DANH SÁCH HỒ SƠ
# ----------------------------------------------------
elif menu == "📋 Danh sách Hồ sơ Lý lịch 2C":
    st.header("📋 DANH SÁCH LÝ LỊCH CÁN BỘ/VIÊN CHỨC")
    
    col_search, col_filter = st.columns([2, 1])
    with col_search:
        search_term = st.text_input("🔍 Tìm kiếm theo Họ tên, Mã NV, Số CCCD hoặc Số CCHN:")
    with col_filter:
        khoa_list = ["Tất cả Khoa/Phòng"] + list(df["Khoa_Phong"].unique())
        selected_khoa = st.selectbox("Lọc theo Khoa/Phòng:", khoa_list)
        
    filtered_df = df.copy()
    if search_term:
        filtered_df = filtered_df[
            filtered_df['Ho_Ten'].str.contains(search_term, case=False, na=False) | 
            filtered_df['Ma_NV'].str.contains(search_term, case=False, na=False) |
            filtered_df['So_CCCD'].str.contains(search_term, case=False, na=False)
        ]
    if selected_khoa != "Tất cả Khoa/Phòng":
        filtered_df = filtered_df[filtered_df['Khoa_Phong'] == selected_khoa]
        
    st.dataframe(filtered_df, use_container_width=True)

# ----------------------------------------------------
# PHÂN HỆ 3: NHẬP / XUẤT EXCEL CHUẨN XLSX
# ----------------------------------------------------
elif menu == "📂 Nhập/Xuất File Excel Mẫu 2C":
    st.header("📂 ĐỒNG BỘ DỮ LIỆU EXCEL TƯƠNG THÍCH MẪU 2C-BNV")
    
    st.subheader("1. Tải về File Excel Mẫu Chuẩn (.xlsx)")
    
    # Tạo sẵn 1 dòng dữ liệu mẫu chuẩn Excel
    sample_data = [{
        "Ma_NV": "BV0001", "Ho_Ten": "Nguyễn Văn A", "Gioi_Tinh": "Nam", "Ngay_Sinh": "1990-01-01",
        "So_CCCD": "001090123456", "Khoa_Phong": "Khoa Cấp cứu", "Chuc_Vu": "Bác sĩ",
        "Ngach_Vien_Chuc": "Bác sĩ (V.08.01.03)", "Trinh_Do_Chuyen_Mon": "Bác sĩ CKI",
        "Ly_Luan_Chinh_Tri": "Trung cấp", "So_CCHN": "001234/BYT-CCHN", "Gio_CME": 50,
        "Loai_HD": "Không xác định thời hạn", "Ngay_Het_Han_HD": "2030-12-31",
        "Bac_Luong": 1, "He_So_Luong": 2.34, "Ngay_Nang_Luong": "2026-12-31", "Trang_Thai": "Đang làm việc"
    }]
    template_df = pd.DataFrame(sample_data)
    
    # Xuất file dạng .xlsx chuẩn Excel bằng io.BytesIO
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        template_df.to_excel(writer, index=False, sheet_name='Mau_2C_BNV')
    excel_data = output.getvalue()
    
    st.download_button(
        label="📄 Tải File Excel Mẫu (.xlsx)", 
        data=excel_data, 
        file_name="Mau_Ly_Lich_2C_BNV.xlsx", 
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    st.markdown("---")
    st.subheader("2. Tải File Excel Nhân Sự Đã Điền Lên Hệ Thống")
    uploaded_file = st.file_uploader("Upload file .xlsx hoặc .csv chứa dữ liệu nhân sự", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df_upload = pd.read_csv(uploaded_file)
            else:
                df_upload = pd.read_excel(uploaded_file)
                
            st.success(f"Đã đọc thành công {len(df_upload)} hồ sơ!")
            st.dataframe(df_upload.head(5))
            
            if st.button("🚀 Nạp Dữ Liệu Vào Phần Mềm"):
                df_upload['Ngay_Nang_Luong'] = pd.to_datetime(df_upload['Ngay_Nang_Luong'])
                df_upload['Ngay_Het_Han_HD'] = pd.to_datetime(df_upload['Ngay_Het_Han_HD'])
                st.session_state.df_nhansu = df_upload
                st.success("Đã nạp toàn bộ dữ liệu nhân sự thành công!")
                st.rerun()
        except Exception as e:
            st.error(f"Lỗi đọc file: {e}. Vui lòng kiểm tra lại cấu trúc cột.")
