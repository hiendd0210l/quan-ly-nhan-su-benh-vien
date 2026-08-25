import streamlit as st
import pandas as pd
import io

# ==========================================
# 1. CẤU HÌNH TRANG STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Hệ thống Quản lý Nhân sự - Lọc Sinh nhật",
    page_icon="🎂",
    layout="wide"
)

st.title("🎂 HỆ THỐNG QUẢN LÝ NHÂN SỰ & LỌC SINH NHẬT")

# ==========================================
# 2. KHỞI TẠO DỮ LIỆU NHÂN SỰ
# ==========================================
if 'df_nhansu' not in st.session_state:
    sample_data = [
        {"Ma_NV": "N0009", "Ho_Ten": "Phạm Thị Thanh Tú", "Ngay_Sinh": "17/09/1980", "Gioi_Tinh": "Nữ", "Khoa_Phong": "Ban Giám đốc", "Chuc_Vu": "Phó Giám đốc"},
        {"Ma_NV": "N0295", "Ho_Ten": "Mai Anh Tuấn", "Ngay_Sinh": "03/09/1985", "Gioi_Tinh": "Nam", "Khoa_Phong": "Phòng Hành chính - Quản trị", "Chuc_Vu": "Phó trưởng phòng"},
        {"Ma_NV": "N0430", "Ho_Ten": "Vương Vũ Việt Hà", "Ngay_Sinh": "26/09/1982", "Gioi_Tinh": "Nam", "Khoa_Phong": "Trung tâm Hỗ trợ sinh sản", "Chuc_Vu": "Giám đốc TT"},
        {"Ma_NV": "N0324", "Ho_Ten": "Nguyễn Bảo Khánh", "Ngay_Sinh": "15/09/1988", "Gioi_Tinh": "Nam", "Khoa_Phong": "Trung tâm Y tế lao động Bưu điện", "Chuc_Vu": "Phó Giám đốc TT"},
        {"Ma_NV": "N0112", "Ho_Ten": "Nguyễn Thị Thu Hằng", "Ngay_Sinh": "18/09/1983", "Gioi_Tinh": "Nữ", "Khoa_Phong": "Khoa Khám bệnh", "Chuc_Vu": "Trưởng khoa"},
        {"Ma_NV": "N1070", "Ho_Ten": "Vũ Thị Nga", "Ngay_Sinh": "07/09/1990", "Gioi_Tinh": "Nữ", "Khoa_Phong": "Khoa Dược", "Chuc_Vu": "Phó trưởng khoa"},
        {"Ma_NV": "N0402", "Ho_Ten": "Lê Minh Thuận", "Ngay_Sinh": "15/09/1987", "Gioi_Tinh": "Nam", "Khoa_Phong": "Khoa Ngoại", "Chuc_Vu": "Phó trưởng khoa"},
        {"Ma_NV": "N0624", "Ho_Ten": "Đặng Ngọc Tuyến", "Ngay_Sinh": "15/09/1989", "Gioi_Tinh": "Nam", "Khoa_Phong": "Khoa Nội", "Chuc_Vu": "Phó trưởng khoa"},
    ]
    st.session_state.df_nhansu = pd.DataFrame(sample_data)

df = st.session_state.df_nhansu.copy()

# Chuẩn hóa cột ngày sinh về định dạng ngày tháng
df['Ngay_Sinh_DT'] = pd.to_datetime(df['Ngay_Sinh'], dayfirst=True, errors='coerce')
df['Thang_Sinh'] = df['Ngay_Sinh_DT'].dt.month

# ==========================================
# 3. DANH MỤC CHỨC NĂNG (SIDEBAR)
# ==========================================
st.sidebar.title("📌 MENUS")
menu = st.sidebar.radio(
    "Chọn chức năng:",
    [
        "🎂 Lọc Sinh nhật theo Tháng",
        "📂 Quản lý Danh sách Nhân sự"
    ]
)

# ==========================================
# CHỨC NĂNG 1: LỌC SINH NHẬT THEO THÁNG
# ==========================================
if menu == "🎂 Lọc Sinh nhật theo Tháng":
    st.subheader("🎂 DANH SÁCH CÁN BỘ CÔNG NHÂN VIÊN SINH NHẬT THEO THÁNG")
    
    selected_month = st.selectbox("Chọn tháng cần lọc:", range(1, 13), index=8) # Mặc định Tháng 9
    
    # Thực hiện lọc theo tháng sinh
    df_filtered = df[df['Thang_Sinh'] == selected_month].copy()
    
    st.info(f"Tổng số nhân sự sinh nhật trong **Tháng {selected_month}**: **{len(df_filtered)} người**")
    
    if not df_filtered.empty:
        # Hiển thị bảng danh sách
        st.dataframe(
            df_filtered[['Ma_NV', 'Ho_Ten', 'Ngay_Sinh', 'Gioi_Tinh', 'Khoa_Phong', 'Chuc_Vu']],
            use_container_width=True,
            hide_index=True
        )
        
        # Xuất file Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_filtered[['Ma_NV', 'Ho_Ten', 'Ngay_Sinh', 'Gioi_Tinh', 'Khoa_Phong', 'Chuc_Vu']].to_excel(
                writer, index=False, sheet_name=f'SinhNhat_Thang_{selected_month}'
            )
            
        st.download_button(
            label=f"📥 Tải danh sách Excel Tháng {selected_month}",
            data=output.getvalue(),
            file_name=f"DS_SinhNhat_Thang_{selected_month}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning(f"Không có nhân sự nào sinh nhật trong Tháng {selected_month}.")

# ==========================================
# CHỨC NĂNG 2: QUẢN LÝ DANH SÁCH NHÂN SỰ
# ==========================================
elif menu == "📂 Quản lý Danh sách Nhân sự":
    st.subheader("📂 DỮ LIỆU NHÂN SỰ HỆ THỐNG")
    
    st.dataframe(st.session_state.df_nhansu, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.write("**Thêm nhân sự mới:**")
    with st.form("add_employee_form"):
        c1, c2, c3 = st.columns(3)
        ma_nv = c1.text_input("Mã Nhân viên")
        ho_ten = c2.text_input("Họ và tên")
        ngay_sinh = c3.text_input("Ngày sinh (dd/mm/yyyy)")
        
        c4, c5, c6 = st.columns(3)
        gioi_tinh = c4.selectbox("Giới tính", ["Nam", "Nữ"])
        khoa_phong = c5.text_input("Khoa / Phòng")
        chuc_vu = c6.text_input("Chức vụ")
        
        submit = st.form_submit_button("Thêm vào danh sách")
        if submit:
            if ma_nv and ho_ten and ngay_sinh:
                new_data = {
                    "Ma_NV": ma_nv.strip().upper(),
                    "Ho_Ten": ho_ten.strip(),
                    "Ngay_Sinh": ngay_sinh.strip(),
                    "Gioi_Tinh": gioi_tinh,
                    "Khoa_Phong": khoa_phong.strip(),
                    "Chuc_Vu": chuc_vu.strip()
                }
                st.session_state.df_nhansu = pd.concat([st.session_state.df_nhansu, pd.DataFrame([new_data])], ignore_index=True)
                st.success(f"Đã thêm thành công nhân sự {ho_ten}!")
                st.rerun()
            else:
                st.error("Vui lòng điền đầy đủ Mã NV, Họ tên và Ngày sinh!")
