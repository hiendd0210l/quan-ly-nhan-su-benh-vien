import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io

# 1. CẤU HÌNH TRANG WEB
st.set_page_config(page_title="Hệ thống Quản lý Nhân sự Bệnh viện - Mẫu 2C-BNV", layout="wide")

# 2. KHỞI TẠO BỘ DỮ LIỆU ĐẦY ĐỦ CÁC TRƯỜNG CHUẨN 2C-BNV/2008
def get_initial_2c_data():
    return [
        {
            "Ma_NV": "BV0001", "Ho_Ten": "NGUYỄN VĂN AN", "Ten_Goi_Khac": "Không", 
            "Ngay_Sinh": "1980-05-15", "Gioi_Tinh": "Nam", "Noi_Sinh": "Hà Nội", "Que_Quan": "Nam Định",
            "Dan_Toc": "Kinh", "Ton_Giao": "Không", "Noi_O_Hien_Nay": "Hoàn Kiếm, Hà Nội", "Dien_Thoai": "0912345678",
            "So_CCCD": "001080012345", "Khoa_Phong": "Khoa Cấp cứu", "Chuc_Vu": "Trưởng khoa",
            "Ngach_Vien_Chuc": "Bác sĩ chính (V.08.01.01)", "Bac_Luong": 3, "He_So_Luong": 5.08, 
            "Ngay_Nang_Luong": "2026-09-15", "Trinh_Do_Giao_Duc": "12/12", "Trinh_Do_Chuyen_Mon": "Bác sĩ CKII",
            "Ly_Luan_Chinh_Tri": "Cao cấp", "Ngoai_Ngu": "Anh B2", "Tin_Hoc": "Ứng dụng CNTT cơ bản",
            "So_CCHN": "001234/BYT-CCHN", "Gio_CME": 52, "Ngay_Vao_Dang": "2010-02-03", "Ngay_Nhap_Ngu": "Không",
            "Danh_Hieu_Phong_Tang": "Thầy thuốc Ưu tú", "Khen_Thuong_Ky_Luat": "Bằng khen Bộ Y tế",
            "Suc_Khoe_Thuong_Binh": "Tốt", "Loai_HD": "Không xác định thời hạn", "Ngay_Het_Han_HD": "2035-12-31",
            "Trang_Thai": "Đang làm việc"
        },
        {
            "Ma_NV": "BV0002", "Ho_Ten": "TRẦN THỊ BÍCH", "Ten_Goi_Khac": "Không", 
            "Ngay_Sinh": "1992-08-20", "Gioi_Tinh": "Nữ", "Noi_Sinh": "Hải Phòng", "Que_Quan": "Hải Phòng",
            "Dan_Toc": "Kinh", "Ton_Giao": "Không", "Noi_O_Hien_Nay": "Cầu Giấy, Hà Nội", "Dien_Thoai": "0987654321",
            "So_CCCD": "001192098765", "Khoa_Phong": "Khoa Khám bệnh", "Chuc_Vu": "Điều dưỡng viên",
            "Ngach_Vien_Chuc": "Điều dưỡng hạng III (V.08.05.12)", "Bac_Luong": 2, "He_So_Luong": 2.67, 
            "Ngay_Nang_Luong": "2027-01-10", "Trinh_Do_Giao_Duc": "12/12", "Trinh_Do_Chuyen_Mon": "Cử nhân Điều dưỡng",
            "Ly_Luan_Chinh_Tri": "Sơ cấp", "Ngoai_Ngu": "Anh A2", "Tin_Hoc": "Ứng dụng CNTT cơ bản",
            "So_CCHN": "005678/BYT-CCHN", "Gio_CME": 30, "Ngay_Vao_Dang": "Chưa", "Ngay_Nhap_Ngu": "Không",
            "Danh_Hieu_Phong_Tang": "Chiến sĩ thi đua cơ sở", "Khen_Thuong_Ky_Luat": "Giấy khen Giám đốc BV",
            "Suc_Khoe_Thuong_Binh": "Tốt", "Loai_HD": "Xác định thời hạn", "Ngay_Het_Han_HD": "2026-09-10",
            "Trang_Thai": "Đang làm việc"
        }
    ]

# Tự động đồng bộ bộ nhớ
if 'df_nhansu' not in st.session_state or 'Noi_Sinh' not in st.session_state.df_nhansu.columns:
    df_temp = pd.DataFrame(get_initial_2c_data())
    df_temp['Ngay_Nang_Luong'] = pd.to_datetime(df_temp['Ngay_Nang_Luong'])
    df_temp['Ngay_Het_Han_HD'] = pd.to_datetime(df_temp['Ngay_Het_Han_HD'])
    st.session_state.df_nhansu = df_temp

df = st.session_state.df_nhansu
today = pd.to_datetime(datetime.now().date())

# 3. GIAO DIỆN CHÍNH
st.title("🏥 HỆ THỐNG QUẢN LÝ HỒ SƠ LÝ LỊCH CÁN BỘ/VIÊN CHỨC (MẪU 2C-BNV/2008)")
menu = st.sidebar.radio("CHỨC NĂNG HỆ THỐNG", [
    "📊 Trung tâm Cảnh báo", 
    "📋 Danh sách Hồ sơ Lý lịch 2C", 
    "📂 Nhập/Xuất File Excel Mẫu 2C (.xlsx)"
])

# ----------------------------------------------------
# PHÂN HỆ 1: TỔNG QUAN & CẢNH BÁO
# ----------------------------------------------------
if menu == "📊 Trung tâm Cảnh báo":
    st.header("🔔 TỰ ĐỘNG CẢNH BÁO NÂNG LƯƠNG, HỢP ĐỒNG & GIỜ CME")
    
    df_luong = df[(df['Ngay_Nang_Luong'] >= today) & (df['Ngay_Nang_Luong'] <= today + timedelta(days=60))]
    df_hd = df[(df['Ngay_Het_Han_HD'] >= today) & (df['Ngay_Het_Han_HD'] <= today + timedelta(days=30))]
    df_cme = df[df['Gio_CME'] < 48]
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tổng số Nhân sự", f"{len(df)} người")
    c2.metric("Sắp nâng lương (60 ngày)", f"{len(df_luong)} người")
    c3.metric("HĐ sắp hết hạn (30 ngày)", f"{len(df_hd)} người")
    c4.metric("Thiếu giờ CME (<48 tiết)", f"{len(df_cme)} người")
    
    st.markdown("---")
    st.subheader("📌 Danh sách nhân sự chuẩn bị họp Hội đồng Nâng lương")
    st.dataframe(df_luong[['Ma_NV', 'Ho_Ten', 'Khoa_Phong', 'Ngach_Vien_Chuc', 'Bac_Luong', 'He_So_Luong', 'Ngay_Nang_Luong']], use_container_width=True)

# ----------------------------------------------------
# PHÂN HỆ 2: DANH SÁCH LÝ LỊCH 2C
# ----------------------------------------------------
elif menu == "📋 Danh sách Hồ sơ Lý lịch 2C":
    st.header("📋 DANH SÁCH TỔNG HỢP HỒ SƠ LÝ LỊCH 2C-BNV")
    
    col_search, col_filter = st.columns([2, 1])
    with col_search:
        search_term = st.text_input("🔍 Tìm kiếm nhanh (Họ tên, Mã NV, CCCD hoặc Số CCHN):")
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
elif menu == "📂 Nhập/Xuất File Excel Mẫu 2C (.xlsx)":
    st.header("📂 ĐỒNG BỘ BỘ DỮ LIỆU EXCEL TƯƠNG THÍCH MẪU 2C-BNV/2008")
    
    st.subheader("1. Tải về File Excel Mẫu Chuẩn (.xlsx)")
    st.info("File Excel xuất ra chuẩn định dạng Microsoft Excel (.xlsx), chia sẵn 33 cột rõ ràng để nhập liệu 1.500 nhân sự.")
    
    # Tạo dữ liệu mẫu Excel chuẩn
    sample_df = pd.DataFrame(get_initial_2c_data())
    
    # Xuất định dạng chuẩn .xlsx bằng openpyxl
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        sample_df.to_excel(writer, index=False, sheet_name='LyLich_2C_BNV')
    excel_data = output.getvalue()
    
    st.download_button(
        label="📥 TẢI FILE EXCEL MẪU CHUẨN (.XLSX)", 
        data=excel_data, 
        file_name="Mau_Sơ_Yếu_Lý_Lịch_2C_BNV.xlsx", 
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    st.markdown("---")
    st.subheader("2. Nạp File Excel Nhân Sự Đã Điền Lên Phần Mềm")
    uploaded_file = st.file_uploader("Upload file Excel (.xlsx) hoặc CSV chứa dữ liệu nhân sự", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df_upload = pd.read_csv(uploaded_file)
            else:
                df_upload = pd.read_excel(uploaded_file)
                
            st.success(f"Đã đọc thành công {len(df_upload)} hồ sơ nhân sự!")
            st.write("📋 **Xem trước 5 hồ sơ đầu tiên:**")
            st.dataframe(df_upload.head(5))
            
            if st.button("🚀 XÁC NHẬN NẠP DỮ LIỆU VÀO HỆ THỐNG"):
                df_upload['Ngay_Nang_Luong'] = pd.to_datetime(df_upload['Ngay_Nang_Luong'])
                df_upload['Ngay_Het_Han_HD'] = pd.to_datetime(df_upload['Ngay_Het_Han_HD'])
                st.session_state.df_nhansu = df_upload
                st.success("Đã nạp toàn bộ dữ liệu nhân sự thành công vào hệ thống!")
                st.rerun()
        except Exception as e:
            st.error(f"Lỗi cấu trúc file: {e}. Vui lòng tải đúng file mẫu .xlsx ở trên về điền.")
