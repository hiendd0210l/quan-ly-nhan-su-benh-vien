import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io

# 1. CẤU HÌNH TRANG WEB
st.set_page_config(
    page_title="Hệ thống Quản lý Nhân sự Bệnh viện - Chuẩn 2C-BNV",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. KHỞI TẠO DỮ LIỆU BAN ĐẦU CHUẨN 2C-BNV/2008
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

# Tự động khởi tạo dữ liệu trong bộ nhớ
if 'df_nhansu' not in st.session_state or 'Noi_Sinh' not in st.session_state.df_nhansu.columns:
    df_temp = pd.DataFrame(get_initial_2c_data())
    df_temp['Ngay_Nang_Luong'] = pd.to_datetime(df_temp['Ngay_Nang_Luong'])
    df_temp['Ngay_Het_Han_HD'] = pd.to_datetime(df_temp['Ngay_Het_Han_HD'])
    st.session_state.df_nhansu = df_temp

df = st.session_state.df_nhansu
today = pd.to_datetime(datetime.now().date())

# Cấu hình danh mục Khoa/Phòng
KHOA_PHONG_LIST = [
    "Khoa Cấp cứu", "Khoa Khám bệnh", "Khoa Nội tổng hợp", "Khoa Ngoại tổng hợp",
    "Khoa Nhi", "Khoa Phụ sản", "Khoa Hồi sức tích cực", "Khoa Dược",
    "Khoa Xét nghiệm", "Khoa Chẩn đoán hình ảnh", "Phòng Tổ chức cán bộ",
    "Phòng Kế hoạch tổng hợp", "Phòng Tài chính kế toán", "Phòng Điều dưỡng"
]

# 3. THANH MENU ĐIỀU HƯỚNG CHÍNH (SIDEBAR)
st.sidebar.image("https://img.icons8.com/color/96/hospital-2.png", width=80)
st.sidebar.title("QUẢN LÝ NHÂN SỰ")
st.sidebar.caption("Phiên bản chuẩn 2C-BNV/2008")

menu = st.sidebar.radio(
    "DANH MỤC CHỨC NĂNG", 
    [
        "🏠 Trang chủ & Tổng quan",
        "🔔 Trung tâm Cảnh báo Tự động",
        "📋 Tra cứu & Danh sách Hồ sơ",
        "➕ Thêm mới Hồ sơ Nhân sự",
        "✏️ Chỉnh sửa / Xóa Hồ sơ",
        "📂 Nhập / Xuất Excel (Mẫu 2C)",
        "⚙️ Thiết lập Hệ thống"
    ]
)

# -----------------------------------------------------------------------------
# MENU 1: TRANG CHỦ & TỔNG QUAN
# -----------------------------------------------------------------------------
if menu == "🏠 Trang chủ & Tổng quan":
    st.title("🏥 HỆ THỐNG QUẢN LÝ NHÂN SỰ BỆNH VIỆN")
    st.markdown("### **Trang chủ & Báo cáo Thống kê Tổng hợp**")
    st.markdown("---")
    
    # Chỉ số nhanh
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tổng số Nhân sự", f"{len(df)} người", delta="Đang quản lý")
    col2.metric("Bác sĩ / Dược sĩ", f"{len(df[df['Trinh_Do_Chuyen_Mon'].str.contains('Bác sĩ|Dược sĩ', case=False, na=False)])} người")
    col3.metric("Điều dưỡng / KTV", f"{len(df[df['Trinh_Do_Chuyen_Mon'].str.contains('Điều dưỡng|Kỹ thuật viên', case=False, na=False)])} người")
    col4.metric("Đảng viên", f"{len(df[df['Ngay_Vao_Dang'] != 'Chưa'])} người")

    st.markdown("---")
    c_left, c_right = st.columns(2)
    
    with c_left:
        st.subheader("📊 Thống kê Nhân sự theo Khoa / Phòng")
        if not df.empty:
            df_khoa = df['Khoa_Phong'].value_counts().reset_index()
            df_khoa.columns = ['Khoa / Phòng', 'Số lượng (người)']
            st.dataframe(df_khoa, use_container_width=True)
            
    with c_right:
        st.subheader("🎓 Thống kê theo Trình độ Chuyên môn")
        if not df.empty:
            df_td = df['Trinh_Do_Chuyen_Mon'].value_counts().reset_index()
            df_td.columns = ['Trình độ', 'Số lượng (người)']
            st.dataframe(df_td, use_container_width=True)

# -----------------------------------------------------------------------------
# MENU 2: TRUNG TÂM CẢNH BÁO TỰ ĐỘNG
# -----------------------------------------------------------------------------
elif menu == "🔔 Trung tâm Cảnh báo Tự động":
    st.title("🔔 TRUNG TÂM CẢNH BÁO TỰ ĐỘNG")
    st.caption("Cảnh báo thời hạn Nâng lương, Hợp đồng lao động và Giờ đào tạo liên tục (CME)")
    st.markdown("---")
    
    df_luong = df[(df['Ngay_Nang_Luong'] >= today) & (df['Ngay_Nang_Luong'] <= today + timedelta(days=60))]
    df_hd = df[(df['Ngay_Het_Han_HD'] >= today) & (df['Ngay_Het_Han_HD'] <= today + timedelta(days=30))]
    df_cme = df[df['Gio_CME'] < 48]
    
    tab1, tab2, tab3 = st.tabs([
        f"📈 Sắp nâng bậc lương ({len(df_luong)})", 
        f"📄 Sắp hết hạn Hợp đồng ({len(df_hd)})", 
        f"🩺 Thiếu giờ CME <48h ({len(df_cme)})"
    ])
    
    with tab1:
        st.subheader("📌 Danh sách Nhân sự đến hạn nâng lương trong 60 ngày tới")
        if not df_luong.empty:
            st.dataframe(df_luong[['Ma_NV', 'Ho_Ten', 'Khoa_Phong', 'Ngach_Vien_Chuc', 'Bac_Luong', 'He_So_Luong', 'Ngay_Nang_Luong']], use_container_width=True)
        else:
            st.success("Không có nhân sự nào sắp đến hạn nâng lương trong 60 ngày tới.")
            
    with tab2:
        st.subheader("📌 Danh sách Hợp đồng lao động sắp hết hạn trong 30 ngày tới")
        if not df_hd.empty:
            st.dataframe(df_hd[['Ma_NV', 'Ho_Ten', 'Khoa_Phong', 'Loai_HD', 'Ngay_Het_Han_HD']], use_container_width=True)
        else:
            st.success("Không có hợp đồng lao động nào sắp hết hạn trong 30 ngày tới.")
            
    with tab3:
        st.subheader("📌 Cảnh báo Bác sĩ/Điều dưỡng chưa đủ 48 tiết CME (Nghị định 96/2023/NĐ-CP)")
        st.dataframe(df_cme[['Ma_NV', 'Ho_Ten', 'Khoa_Phong', 'Chuc_Vu', 'So_CCHN', 'Gio_CME']], use_container_width=True)

# -----------------------------------------------------------------------------
# MENU 3: TRA CỨU & DANH SÁCH HỒ SƠ
# -----------------------------------------------------------------------------
elif menu == "📋 Tra cứu & Danh sách Hồ sơ":
    st.title("📋 TRA CỨU & QUẢN LÝ DANH SÁCH HỒ SƠ 2C-BNV")
    st.markdown("---")
    
    c_search, c_khoa, c_tt = st.columns([2, 1, 1])
    with c_search:
        search_kw = st.text_input("🔍 Tìm kiếm theo Họ tên, Mã NV, Số CCCD hoặc Số CCHN:")
    with c_khoa:
        sel_khoa = st.selectbox("Lọc Khoa/Phòng:", ["Tất cả"] + list(df['Khoa_Phong'].unique()))
    with c_tt:
        sel_tt = st.selectbox("Trạng thái:", ["Tất cả", "Đang làm việc", "Nghỉ thai sản", "Đã nghỉ việc"])
        
    filtered = df.copy()
    if search_kw:
        filtered = filtered[
            filtered['Ho_Ten'].str.contains(search_kw, case=False, na=False) |
            filtered['Ma_NV'].str.contains(search_kw, case=False, na=False) |
            filtered['So_CCCD'].str.contains(search_kw, case=False, na=False) |
            filtered['So_CCHN'].str.contains(search_kw, case=False, na=False)
        ]
    if sel_khoa != "Tất cả":
        filtered = filtered[filtered['Khoa_Phong'] == sel_khoa]
    if sel_tt != "Tất cả":
        filtered = filtered[filtered['Trang_Thai'] == sel_tt]
        
    st.write(f"Hiển thị **{len(filtered)}** / **{len(df)}** hồ sơ nhân sự:")
    st.dataframe(filtered, use_container_width=True)

# -----------------------------------------------------------------------------
# MENU 4: THÊM MỚI HỒ SƠ NHÂN SỰ
# -----------------------------------------------------------------------------
elif menu == "➕ Thêm mới Hồ sơ Nhân sự":
    st.title("➕ THÊM MỚI HỒ SƠ NHÂN SỰ (MẪU 2C-BNV)")
    st.markdown("---")
    
    with st.form("form_add_emp", clear_on_submit=True):
        st.subheader("I. Thông tin Hành chính & Cá nhân")
        col1, col2, col3 = st.columns(3)
        with col1:
            ma_nv = st.text_input("Mã Nhân viên (*):", value=f"BV{len(df)+1:04d}")
            ho_ten = st.text_input("Họ và Tên khai sinh (*):")
            ten_khac = st.text_input("Tên gọi khác / Bí danh:", value="Không")
            ngay_sinh = st.date_input("Ngày sinh:", value=datetime(1990, 1, 1))
            gioi_tinh = st.selectbox("Giới tính:", ["Nam", "Nữ"])
        with col2:
            so_cccd = st.text_input("Số CCCD / CMND (*):")
            noi_sinh = st.text_input("Nơi sinh (Xã/Huyện/Tỉnh):")
            que_quan = st.text_input("Quê quán:")
            dan_toc = st.text_input("Dân tộc:", value="Kinh")
            ton_giao = st.text_input("Tôn giáo:", value="Không")
        with col3:
            dien_thoai = st.text_input("Số điện thoại:")
            noi_o = st.text_input("Nơi ở hiện nay:")
            suc_khoe = st.text_input("Tình trạng sức khỏe:", value="Tốt")
            ngay_dang = st.text_input("Ngày vào Đảng (YYYY-MM-DD):", value="Chưa")
            ngay_ngu = st.text_input("Ngày nhập ngũ / Quân hàm:", value="Không")

        st.subheader("II. Chức danh, Ngạch bậc & Chuyên môn Y tế")
        col4, col5, col6 = st.columns(3)
        with col4:
            khoa_phong = st.selectbox("Khoa / Phòng làm việc:", KHOA_PHONG_LIST)
            chuc_vu = st.text_input("Chức vụ:", value="Nhiệm vụ chuyên môn")
            ngach = st.text_input("Ngạch viên chức (VD: Bác sĩ - V.08.01.03):")
            td_chuyen_mon = st.text_input("Trình độ chuyên môn (BS/ĐD/Dược sĩ...):")
        with col5:
            bac_luong = st.number_input("Bậc lương:", min_value=1, max_value=12, value=1)
            he_so_luong = st.number_input("Hệ số lương:", min_value=1.0, max_value=10.0, value=2.34, step=0.01)
            ngay_luong = st.date_input("Ngày nâng lương tiếp theo:", value=datetime.now() + timedelta(days=1095))
            so_cchn = st.text_input("Số Chứng chỉ hành nghề (CCHN):")
        with col6:
            gio_cme = st.number_input("Số tiết CME lũy kế:", min_value=0, max_value=300, value=0)
            td_llct = st.selectbox("Lý luận chính trị:", ["Chưa", "Sơ cấp", "Trung cấp", "Cao cấp", "Cử nhân"])
            ngoai_ngu = st.text_input("Ngoại ngữ:", value="Anh A2")
            tin_hoc = st.text_input("Tin học:", value="CB")

        st.subheader("III. Hợp đồng lao động & Khen thưởng")
        col7, col8, col9 = st.columns(3)
        with col7:
            loai_hd = st.selectbox("Loại Hợp đồng:", ["Thử việc", "Xác định thời hạn", "Không xác định thời hạn"])
            ngay_hd = st.date_input("Ngày hết hạn HĐ:", value=datetime.now() + timedelta(days=365))
        with col8:
            khen_thuong = st.text_input("Khen thưởng / Kỷ luật:", value="Không")
            danh_hieu = st.text_input("Danh hiệu phong tặng:", value="Không")
        with col9:
            trang_thai = st.selectbox("Trạng thái công tác:", ["Đang làm việc", "Nghỉ thai sản", "Đã nghỉ việc"])

        btn_save = st.form_submit_button("💾 LƯU HỒ SƠ NHÂN SỰ MỚI")
        
        if btn_save:
            if not ma_nv or not ho_ten:
                st.error("Vui lòng điền đầy đủ Mã nhân viên và Họ tên!")
            else:
                new_row = {
                    "Ma_NV": ma_nv, "Ho_Ten": ho_ten.upper(), "Ten_Goi_Khac": ten_khac,
                    "Ngay_Sinh": str(ngay_sinh), "Gioi_Tinh": gioi_tinh, "Noi_Sinh": noi_sinh, "Que_Quan": que_quan,
                    "Dan_Toc": dan_toc, "Ton_Giao": ton_giao, "Noi_O_Hien_Nay": noi_o, "Dien_Thoai": dien_thoai,
                    "So_CCCD": so_cccd, "Khoa_Phong": khoa_phong, "Chuc_Vu": chuc_vu, "Ngach_Vien_Chuc": ngach,
                    "Bac_Luong": bac_luong, "He_So_Luong": he_so_luong, "Ngay_Nang_Luong": pd.to_datetime(ngay_luong),
                    "Trinh_Do_Giao_Duc": "12/12", "Trinh_Do_Chuyen_Mon": td_chuyen_mon, "Ly_Luan_Chinh_Tri": td_llct,
                    "Ngoai_Ngu": ngoai_ngu, "Tin_Hoc": tin_hoc, "So_CCHN": so_cchn, "Gio_CME": gio_cme,
                    "Ngay_Vao_Dang": ngay_dang, "Ngay_Nhap_Ngu": ngay_ngu, "Danh_Hieu_Phong_Tang": danh_hieu,
                    "Khen_Thuong_Ky_Luat": khen_thuong, "Suc_Khoe_Thuong_Binh": suc_khoe, "Loai_HD": loai_hd,
                    "Ngay_Het_Han_HD": pd.to_datetime(ngay_hd), "Trang_Thai": trang_thai
                }
                st.session_state.df_nhansu = pd.concat([st.session_state.df_nhansu, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"✅ Đã thêm mới thành công hồ sơ nhân sự {ho_ten.upper()} ({ma_nv})!")

# -----------------------------------------------------------------------------
# MENU 5: CHỈNH SỬA / XÓA HỒ SƠ
# -----------------------------------------------------------------------------
elif menu == "✏️ Chỉnh sửa / Xóa Hồ sơ":
    st.title("✏️ CẬP NHẬT HOẶC XÓA HỒ SƠ NHÂN SỰ")
    st.markdown("---")
    
    selected_id = st.selectbox("🔍 Chọn Mã Nhân Viên hoặc Họ Tên cần thao tác:", df['Ma_NV'] + " - " + df['Ho_Ten'])
    
    if selected_id:
        ma_selected = selected_id.split(" - ")[0]
        emp_idx = df[df['Ma_NV'] == ma_selected].index[0]
        emp = df.loc[emp_idx]
        
        tab_edit, tab_delete = st.tabs(["✏️ Chỉnh sửa thông tin", "🗑️ Xóa hồ sơ"])
        
        with tab_edit:
            with st.form("form_edit_emp"):
                st.subheader(f"Cập nhật thông tin cán bộ: {emp['Ho_Ten']} ({emp['Ma_NV']})")
                
                ce1, ce2, ce3 = st.columns(3)
                with ce1:
                    e_khoa = st.selectbox("Khoa/Phòng:", KHOA_PHONG_LIST, index=KHOA_PHONG_LIST.index(emp['Khoa_Phong']) if emp['Khoa_Phong'] in KHOA_PHONG_LIST else 0)
                    e_chucvu = st.text_input("Chức vụ:", value=emp['Chuc_Vu'])
                    e_hsl = st.number_input("Hệ số lương:", value=float(emp['He_So_Luong']), step=0.01)
                with ce2:
                    e_cme = st.number_input("Số giờ CME tích lũy:", value=int(emp['Gio_CME']))
                    e_cchn = st.text_input("Số CCHN:", value=emp['So_CCHN'])
                    e_trangthai = st.selectbox("Trạng thái:", ["Đang làm việc", "Nghỉ thai sản", "Đã nghỉ việc"], index=["Đang làm việc", "Nghỉ thai sản", "Đã nghỉ việc"].index(emp['Trang_Thai']))
                with ce3:
                    e_luong = st.date_input("Ngày nâng lương tiếp theo:", value=pd.to_datetime(emp['Ngay_Nang_Luong']))
                    e_hd = st.date_input("Ngày hết hạn HĐ:", value=pd.to_datetime(emp['Ngay_Het_Han_HD']))
                    
                btn_update = st.form_submit_button("💾 CẬP NHẬT LƯU HỒ SƠ")
                
                if btn_update:
                    st.session_state.df_nhansu.at[emp_idx, 'Khoa_Phong'] = e_khoa
                    st.session_state.df_nhansu.at[emp_idx, 'Chuc_Vu'] = e_chucvu
                    st.session_state.df_nhansu.at[emp_idx, 'He_So_Luong'] = e_hsl
                    st.session_state.df_nhansu.at[emp_idx, 'Gio_CME'] = e_cme
                    st.session_state.df_nhansu.at[emp_idx, 'So_CCHN'] = e_cchn
                    st.session_state.df_nhansu.at[emp_idx, 'Trang_Thai'] = e_trangthai
                    st.session_state.df_nhansu.at[emp_idx, 'Ngay_Nang_Luong'] = pd.to_datetime(e_luong)
                    st.session_state.df_nhansu.at[emp_idx, 'Ngay_Het_Han_HD'] = pd.to_datetime(e_hd)
                    st.success("✅ Đã cập nhật thành công thông tin hồ sơ!")
                    st.rerun()
                    
        with tab_delete:
            st.warning(f"⚠️ Bạn có chắc chắn muốn xóa hồ sơ của cán bộ **{emp['Ho_Ten']}** ({emp['Ma_NV']}) khỏi hệ thống?")
            if st.button("❌ XÁC NHẬN XÓA HỒ SƠ NÀY"):
                st.session_state.df_nhansu = st.session_state.df_nhansu.drop(emp_idx).reset_index(drop=True)
                st.success("Đã xóa hồ sơ thành công!")
                st.rerun()

# -----------------------------------------------------------------------------
# MENU 6: NHẬP / XUẤT EXCEL (MẪU 2C)
# -----------------------------------------------------------------------------
elif menu == "📂 Nhập / Xuất Excel (Mẫu 2C)":
    st.title("📂 ĐỒNG BỘ DỮ LIỆU EXCEL TƯƠNG THÍCH MẪU 2C-BNV/2008")
    st.markdown("---")
    
    col_x, col_m = st.columns(2)
    
    with col_x:
        st.subheader("1. Xuất Báo cáo Excel Nhân sự Hiện tại")
        st.write("Tải toàn bộ danh sách 1.500 nhân sự đang lưu trên hệ thống ra file Excel `.xlsx`:")
        
        output_all = io.BytesIO()
        with pd.ExcelWriter(output_all, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='DanhSach_2C_BNV')
        
        st.download_button(
            label="📥 TẢI VỀ TOÀN BỘ HỒ SƠ (.XLSX)",
            data=output_all.getvalue(),
            file_name=f"Danh_Sach_Nhan_Su_BV_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    with col_m:
        st.subheader("2. Tải File Excel Mẫu Chuẩn (Template)")
        st.write("Tải file Excel khung phân cột chuẩn 33 trường 2C-BNV để nhập liệu nhân sự mới:")
        
        sample_df = pd.DataFrame(get_initial_2c_data())
        output_tmp = io.BytesIO()
        with pd.ExcelWriter(output_tmp, engine='openpyxl') as writer:
            sample_df.to_excel(writer, index=False, sheet_name='Mau_2C_BNV')
            
        st.download_button(
            label="📄 TẢI FILE EXCEL MẪU (.XLSX)",
            data=output_tmp.getvalue(),
            file_name="Mau_Ly_Lich_2C_BNV.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    st.markdown("---")
    st.subheader("3. Tải File Excel Dữ Liệu Nhân Sự Lên Hệ Thống")
    uploaded_file = st.file_uploader("Upload file Excel (.xlsx) chứa danh sách nhân sự", type=["xlsx", "csv"])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df_upload = pd.read_csv(uploaded_file)
            else:
                df_upload = pd.read_excel(uploaded_file)
                
            st.success(f"Đã nạp thành công {len(df_upload)} bản ghi!")
            st.dataframe(df_upload.head(5))
            
            if st.button("🚀 NẠP DỮ LIỆU NÀY VÀO PHẦN MỀM"):
                df_upload['Ngay_Nang_Luong'] = pd.to_datetime(df_upload['Ngay_Nang_Luong'])
                df_upload['Ngay_Het_Han_HD'] = pd.to_datetime(df_upload['Ngay_Het_Han_HD'])
                st.session_state.df_nhansu = df_upload
                st.success("Đã đồng bộ toàn bộ dữ liệu vào ứng dụng thành công!")
                st.rerun()
        except Exception as e:
            st.error(f"Lỗi nạp file: {e}")

# -----------------------------------------------------------------------------
# MENU 7: THIẾT LẬP HỆ THỐNG
# -----------------------------------------------------------------------------
elif menu == "⚙️ Thiết lập Hệ thống":
    st.title("⚙️ THIẾT LẬP HỆ THỐNG & CƠ SỞ DỮ LIỆU")
    st.markdown("---")
    
    st.subheader("1. Cấu hình Tham số Cảnh báo Tự động")
    col_t1, col_t2, col_t3 = st.columns(3)
    col_t1.number_input("Cảnh báo Nâng lương trước (ngày):", value=60)
    col_t2.number_input("Cảnh báo Hết hạn HĐ trước (ngày):", value=30)
    col_t3.number_input("Định mức giờ CME tối thiểu (tiết):", value=48)
    
    st.markdown("---")
    st.subheader("2. Khôi phục Dữ liệu Mặc định (Reset)")
    st.warning("⚠️ Thao tác này sẽ đặt lại bộ nhớ tạm về 2 bản ghi mẫu ban đầu.")
    if st.button("🔄 ĐẶT LẠI DỮ LIỆU MẶC ĐỊNH"):
        df_reset = pd.DataFrame(get_initial_2c_data())
        df_reset['Ngay_Nang_Luong'] = pd.to_datetime(df_reset['Ngay_Nang_Luong'])
        df_reset['Ngay_Het_Han_HD'] = pd.to_datetime(df_reset['Ngay_Het_Han_HD'])
        st.session_state.df_nhansu = df_reset
        st.success("Đã đặt lại dữ liệu thành công!")
        st.rerun()
