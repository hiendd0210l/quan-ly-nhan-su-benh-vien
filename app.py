import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io
import sqlite3
import os

# 1. CẤU HÌNH TRANG WEB
st.set_page_config(
    page_title="Hệ thống Quản lý Nhân sự Bệnh viện Bưu điện - Chuẩn 2C-BNV",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_FILE = "nhansu_benhvien.db"

# 2. KHỞI TẠO CƠ SỞ DỮ LIỆU SQLITE
def init_sqlite_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nhansu (
            Ma_NV TEXT PRIMARY KEY,
            Ho_Ten TEXT,
            Ten_Goi_Khac TEXT,
            Ngay_Sinh TEXT,
            Gioi_Tinh TEXT,
            Noi_Sinh TEXT,
            Que_Quan TEXT,
            Dan_Toc TEXT,
            Ton_Giao TEXT,
            Noi_O_Hien_Nay TEXT,
            Dien_Thoai TEXT,
            So_CCCD TEXT,
            Khoa_Phong TEXT,
            Chuc_Vu TEXT,
            Ngach_Vien_Chuc TEXT,
            Bac_Luong INTEGER,
            He_So_Luong REAL,
            Ngay_Nang_Luong TEXT,
            Trinh_Do_Giao_Duc TEXT,
            Trinh_Do_Chuyen_Mon TEXT,
            Ly_Luan_Chinh_Tri TEXT,
            Ngoai_Ngu TEXT,
            Tin_Hoc TEXT,
            So_CCHN TEXT,
            Gio_CME INTEGER,
            Ngay_Vao_Dang TEXT,
            Ngay_Nhap_Ngu TEXT,
            Danh_Hieu_Phong_Tang TEXT,
            Khen_Thuong_Ky_Luat TEXT,
            Suc_Khoe_Thuong_Binh TEXT,
            Loai_HD TEXT,
            Ngay_Het_Han_HD TEXT,
            Trang_Thai TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Hàm ép kiểu ngày tháng an toàn theo chuẩn Việt Nam (Ngày/Tháng/Năm)
def parse_date_vietnam(series):
    return pd.to_datetime(series, dayfirst=True, errors='coerce')

# Hàm làm sạch & chuẩn hóa dữ liệu DataFrame
def clean_dataframe(df_in):
    if df_in.empty:
        return df_in
    df_clean = df_in.copy()
    for col in df_clean.select_dtypes(include=['object']).columns:
        df_clean[col] = df_clean[col].astype(str).str.strip()
        df_clean[col] = df_clean[col].replace({'nan': '', 'None': '', 'NaN': ''})
    
    # Ép kiểu dữ liệu ngày tháng ưu tiên Ngày/Tháng/Năm (dayfirst=True)
    df_clean['Ngay_Nang_Luong'] = parse_date_vietnam(df_clean['Ngay_Nang_Luong'])
    df_clean['Ngay_Het_Han_HD'] = parse_date_vietnam(df_clean['Ngay_Het_Han_HD'])
    
    # Chuẩn hóa cột Ngay_Sinh
    df_clean['Ngay_Sinh_DT'] = parse_date_vietnam(df_clean['Ngay_Sinh'])
    valid_dates = df_clean['Ngay_Sinh_DT'].notnull()
    df_clean.loc[valid_dates, 'Ngay_Sinh_HienThi'] = df_clean.loc[valid_dates, 'Ngay_Sinh_DT'].dt.strftime('%d/%m/%Y')
    df_clean.loc[~valid_dates, 'Ngay_Sinh_HienThi'] = df_clean.loc[~valid_dates, 'Ngay_Sinh']
    
    return df_clean

# Đọc dữ liệu từ SQLite
def load_data_from_db():
    conn = sqlite3.connect(DB_FILE)
    df_loaded = pd.read_sql_query("SELECT * FROM nhansu", conn)
    conn.close()
    return clean_dataframe(df_loaded)

# Ghi dữ liệu vào SQLite
def save_data_to_db(df_to_save):
    conn = sqlite3.connect(DB_FILE)
    df_temp = clean_dataframe(df_to_save)
    
    cols_to_drop = [c for c in ['Ngay_Sinh_DT', 'Ngay_Sinh_HienThi'] if c in df_temp.columns]
    df_temp = df_temp.drop(columns=cols_to_drop)
    
    df_temp['Ngay_Nang_Luong'] = df_temp['Ngay_Nang_Luong'].dt.strftime('%Y-%m-%d')
    df_temp['Ngay_Het_Han_HD'] = df_temp['Ngay_Het_Han_HD'].dt.strftime('%Y-%m-%d')
    df_temp.to_sql('nhansu', conn, if_exists='replace', index=False)
    conn.close()

# Khởi tạo CSDL
init_sqlite_db()

if 'df_nhansu' not in st.session_state:
    st.session_state.df_nhansu = load_data_from_db()

df = st.session_state.df_nhansu
today = pd.to_datetime(datetime.now().date())

# 3. THANH MENU ĐIỀU HƯỚNG CHÍNH
st.sidebar.image("https://img.icons8.com/color/96/hospital-2.png", width=80)
st.sidebar.title("QUẢN LÝ NHÂN SỰ")
st.sidebar.caption("Giao diện Trang chủ Cảnh báo & Thống kê 2C")

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
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    total_emp = len(df)
    col1.metric("Tổng số Nhân sự", f"{total_emp} người")
    
    if not df.empty:
        bs_count = len(df[df['Trinh_Do_Chuyen_Mon'].astype(str).str.contains('Bác sĩ|Dược sĩ', case=False, na=False)])
        dd_count = len(df[df['Trinh_Do_Chuyen_Mon'].astype(str).str.contains('Điều dưỡng|Kỹ thuật viên', case=False, na=False)])
        
        dang_vien_df = df[
            df['Ngay_Vao_Dang'].notnull() & 
            ~df['Ngay_Vao_Dang'].astype(str).str.strip().str.lower().isin(['chưa', 'khong', 'không', '0', '-', '', 'none', 'nan'])
        ]
        dv_count = len(dang_vien_df)
    else:
        bs_count, dd_count, dv_count = 0, 0, 0
    
    col2.metric("Bác sĩ / Dược sĩ", f"{bs_count} người")
    col3.metric("Điều dưỡng / KTV", f"{dd_count} người")
    col4.metric("Đảng viên", f"{dv_count} người")

    st.markdown("---")
    
    left_col, right_col = st.columns([1.3, 1.0])
    
    with left_col:
        st.subheader("📊 THỐNG KÊ, LỌC & BÁO CÁO TỶ LỆ (2C-BNV)")
        
        if df.empty:
            st.info("Chưa có dữ liệu để lập báo cáo thống kê.")
        else:
            with st.expander("🔍 Lọc đa điều kiện nâng cao:", expanded=True):
                match_mode = st.radio(
                    "⚙️ Chế độ lọc:",
                    options=["🔍 Lựa chọn tương đối (Chứa chuỗi ký tự)", "🎯 Lựa chọn tuyệt đối (Chính xác 100%)"],
                    index=0,
                    horizontal=True
                )
                is_contains = "tương đối" in match_mode.lower()

                filtered_df = df.copy()
                f_col1, f_col2 = st.columns(2)
                
                def apply_filter(data_frame, col_name, selected_val, contains_mode=True):
                    if selected_val == "Tất cả" or not selected_val:
                        return data_frame
                    if contains_mode:
                        return data_frame[data_frame[col_name].astype(str).str.contains(selected_val, case=False, na=False, regex=False)]
                    else:
                        return data_frame[data_frame[col_name].astype(str) == selected_val]

                with f_col1:
                    kp_list = ["Tất cả"] + sorted([str(x) for x in df['Khoa_Phong'].unique() if str(x).strip() != ''])
                    sel_kp = st.selectbox("1. Khoa / Phòng:", kp_list)
                    filtered_df = apply_filter(filtered_df, 'Khoa_Phong', sel_kp, is_contains)
                        
                    td_list = ["Tất cả"] + sorted([str(x) for x in df['Trinh_Do_Chuyen_Mon'].unique() if str(x).strip() != ''])
                    sel_td = st.selectbox("2. Trình độ chuyên môn:", td_list)
                    filtered_df = apply_filter(filtered_df, 'Trinh_Do_Chuyen_Mon', sel_td, is_contains)

                    gt_list = ["Tất cả"] + sorted([str(x) for x in df['Gioi_Tinh'].unique() if str(x).strip() != ''])
                    sel_gt = st.selectbox("3. Giới tính:", gt_list)
                    filtered_df = apply_filter(filtered_df, 'Gioi_Tinh', sel_gt, is_contains)

                with f_col2:
                    tt_list = ["Tất cả"] + sorted([str(x) for x in df['Trang_Thai'].unique() if str(x).strip() != ''])
                    sel_tt = st.selectbox("4. Trạng thái công tác:", tt_list)
                    filtered_df = apply_filter(filtered_df, 'Trang_Thai', sel_tt, is_contains)

                    hd_list = ["Tất cả"] + sorted([str(x) for x in df['Loai_HD'].unique() if str(x).strip() != ''])
                    sel_hd = st.selectbox("5. Loại Hợp đồng:", hd_list)
                    filtered_df = apply_filter(filtered_df, 'Loai_HD', sel_hd, is_contains)

                    llct_list = ["Tất cả"] + sorted([str(x) for x in df['Ly_Luan_Chinh_Tri'].unique() if str(x).strip() != ''])
                    sel_llct = st.selectbox("6. Lý luận chính trị:", llct_list)
                    filtered_df = apply_filter(filtered_df, 'Ly_Luan_Chinh_Tri', sel_llct, is_contains)

            count_filtered = len(filtered_df)
            pct_over_total = (count_filtered / total_emp * 100) if total_emp > 0 else 0
            
            st.markdown(f"📌 **Kết quả lọc:** **{count_filtered}** / **{total_emp}** nhân sự (**{pct_over_total:.1f}%** toàn đơn vị)")
            
            st.markdown("📈 **Báo cáo Số lượng & Tỷ lệ Phân loại:**")
            group_col = st.selectbox(
                "Phân tích tỷ lệ phân loại danh sách đã lọc theo:",
                ["Khoa_Phong", "Trinh_Do_Chuyen_Mon", "Chuc_Vu", "Gioi_Tinh", "Loai_HD", "Trang_Thai", "Ly_Luan_Chinh_Tri"],
                format_func=lambda x: {
                    "Khoa_Phong": "1. Khoa / Phòng",
                    "Trinh_Do_Chuyen_Mon": "2. Trình độ chuyên môn",
                    "Chuc_Vu": "3. Chức vụ",
                    "Gioi_Tinh": "4. Giới tính",
                    "Loai_HD": "5. Loại Hợp đồng",
                    "Trang_Thai": "6. Trạng thái công tác",
                    "Ly_Luan_Chinh_Tri": "7. Lý luận chính trị"
                }[x]
            )

            if not filtered_df.empty:
                df_stat = filtered_df[group_col].value_counts().reset_index()
                df_stat.columns = ['Phân loại', 'Số lượng (người)']
                df_stat['Tỷ lệ / Nhóm lọc (%)'] = (df_stat['Số lượng (người)'] / count_filtered * 100).round(1).astype(str) + '%'
                df_stat['Tỷ lệ / Toàn đơn vị (%)'] = (df_stat['Số lượng (người)'] / total_emp * 100).round(1).astype(str) + '%'
                st.dataframe(df_stat, use_container_width=True)
            else:
                st.warning("Không có dữ liệu thỏa mãn điều kiện lọc.")

            st.markdown("📋 **Danh sách chi tiết nhân sự đã lọc:**")
            st.dataframe(
                filtered_df[['Ma_NV', 'Ho_Ten', 'Khoa_Phong', 'Chuc_Vu', 'Trinh_Do_Chuyen_Mon', 'Trang_Thai']], 
                use_container_width=True, 
                height=200
            )
            
            output_report = io.BytesIO()
            with pd.ExcelWriter(output_report, engine='openpyxl') as writer:
                if not filtered_df.empty:
                    df_stat.to_excel(writer, index=False, sheet_name='Thong_Ke_Ty_Le')
                filtered_df.to_excel(writer, index=False, sheet_name='Danh_Sach_Thong_Ke')
            
            st.download_button(
                label="📥 XUẤT BÁO CÁO THỐNG KÊ & TỶ LỆ (.XLSX)",
                data=output_report.getvalue(),
                file_name=f"Bao_Cao_Thong_Ke_Tyle_NhanSu_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    with right_col:
        st.subheader("🔔 TRUNG TÂM CẢNH BÁO TỰ ĐỘNG")
        
        if not df.empty:
            df_luong = df[(df['Ngay_Nang_Luong'] >= today) & (df['Ngay_Nang_Luong'] <= today + timedelta(days=60))]
            df_hd = df[(df['Ngay_Het_Han_HD'] >= today) & (df['Ngay_Het_Han_HD'] <= today + timedelta(days=30))]
            
            next_month = (today.month % 12) + 1
            if 'Ngay_Sinh_DT' not in df.columns:
                df['Ngay_Sinh_DT'] = parse_date_vietnam(df['Ngay_Sinh'])
            df_sn = df[df['Ngay_Sinh_DT'].dt.month == next_month]
        else:
            df_luong, df_hd, df_sn = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
            next_month = (today.month % 12) + 1

        t1, t2, t3 = st.tabs([
            f"📈 Nâng lương ({len(df_luong)})", 
            f"📄 Hợp đồng ({len(df_hd)})", 
            f"🎂 Sinh nhật T{next_month} ({len(df_sn)})"
        ])
        
        with t1:
            st.caption("Cán bộ sắp đến hạn nâng bậc lương trong 60 ngày tới:")
            if not df_luong.empty:
                st.dataframe(
                    df_luong[['Ma_NV', 'Ho_Ten', 'Khoa_Phong', 'Ngay_Nang_Luong']], 
                    use_container_width=True, 
                    height=320
                )
            else:
                st.success("Không có ai sắp nâng lương trong 60 ngày tới.")
                
        with t2:
            st.caption("Hợp đồng lao động sắp hết hạn trong 30 ngày tới:")
            if not df_hd.empty:
                st.dataframe(
                    df_hd[['Ma_NV', 'Ho_Ten', 'Khoa_Phong', 'Loai_HD', 'Ngay_Het_Han_HD']], 
                    use_container_width=True, 
                    height=320
                )
            else:
                st.success("Không có hợp đồng lao động nào sắp hết hạn.")
                
        with t3:
            st.caption(f"Danh sách nhân sự có sinh nhật trong tháng {next_month}:")
            if not df_sn.empty:
                display_sn = df_sn.copy()
                if 'Ngay_Sinh_HienThi' in display_sn.columns:
                    display_sn['Ngay_Sinh'] = display_sn['Ngay_Sinh_HienThi']
                st.dataframe(
                    display_sn[['Ma_NV', 'Ho_Ten', 'Khoa_Phong', 'Ngay_Sinh']], 
                    use_container_width=True, 
                    height=320
                )
            else:
                st.info(f"Không có nhân sự nào sinh nhật trong tháng {next_month}.")

# -----------------------------------------------------------------------------
# MENU 2: TRUNG TÂM CẢNH BÁO TỰ ĐỘNG
# -----------------------------------------------------------------------------
elif menu == "🔔 Trung tâm Cảnh báo Tự động":
    st.title("🔔 TRUNG TÂM CẢNH BÁO TỰ ĐỘNG CHI TIẾT")
    st.markdown("---")
    
    if not df.empty:
        df_luong = df[(df['Ngay_Nang_Luong'] >= today) & (df['Ngay_Nang_Luong'] <= today + timedelta(days=60))]
        df_hd = df[(df['Ngay_Het_Han_HD'] >= today) & (df['Ngay_Het_Han_HD'] <= today + timedelta(days=30))]
        df_cme = df[pd.to_numeric(df['Gio_CME'], errors='coerce').fillna(0) < 48]
    else:
        df_luong, df_hd, df_cme = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    
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
            st.info("Không có nhân sự nào sắp đến hạn nâng lương trong 60 ngày tới.")
            
    with tab2:
        st.subheader("📌 Danh sách Hợp đồng lao động sắp hết hạn trong 30 ngày tới")
        if not df_hd.empty:
            st.dataframe(df_hd[['Ma_NV', 'Ho_Ten', 'Khoa_Phong', 'Loai_HD', 'Ngay_Het_Han_HD']], use_container_width=True)
        else:
            st.info("Không có hợp đồng lao động nào sắp hết hạn trong 30 ngày tới.")
            
    with tab3:
        st.subheader("📌 Cảnh báo Bác sĩ/Điều dưỡng chưa đủ 48 tiết CME")
        if not df_cme.empty:
            st.dataframe(df_cme[['Ma_NV', 'Ho_Ten', 'Khoa_Phong', 'Chuc_Vu', 'So_CCHN', 'Gio_CME']], use_container_width=True)
        else:
            st.info("Tất cả nhân sự đã đạt đủ tiêu chuẩn giờ CME.")

# -----------------------------------------------------------------------------
# MENU 3: TRA CỨU & DANH SÁCH HỒ SƠ
# -----------------------------------------------------------------------------
elif menu == "📋 Tra cứu & Danh sách Hồ sơ":
    st.title("📋 TRA CỨU & QUẢN LÝ DANH SÁCH HỒ SƠ 2C-BNV")
    st.markdown("---")
    
    if df.empty:
        st.warning("⚠️ Cơ sở dữ liệu hiện chưa có hồ sơ nhân sự nào. Vui lòng nạp file Excel vào hệ thống.")
    else:
        c_search, c_khoa, c_tt, c_sn = st.columns([2, 1, 1, 1])
        
        with c_search:
            search_kw = st.text_input("🔍 Tìm kiếm theo Họ tên, Mã NV, Số CCCD, CCHN:")
        with c_khoa:
            khoa_opts = ["Tất cả"] + sorted([str(x) for x in df['Khoa_Phong'].dropna().unique() if str(x).strip() != ''])
            sel_khoa = st.selectbox("Lọc Khoa/Phòng:", khoa_opts)
        with c_tt:
            tt_opts = ["Tất cả"] + sorted([str(x) for x in df['Trang_Thai'].dropna().unique() if str(x).strip() != ''])
            sel_tt = st.selectbox("Lọc Trạng thái:", tt_opts)
        with c_sn:
            month_opts = ["Tất cả"] + [f"Tháng {m}" for m in range(1, 13)]
            sel_month = st.selectbox("🎂 Lọc Sinh nhật:", month_opts)
            
        filtered = df.copy()
        
        if search_kw:
            filtered = filtered[
                filtered['Ho_Ten'].astype(str).str.contains(search_kw, case=False, na=False) |
                filtered['Ma_NV'].astype(str).str.contains(search_kw, case=False, na=False) |
                filtered['So_CCCD'].astype(str).str.contains(search_kw, case=False, na=False) |
                filtered['So_CCHN'].astype(str).str.contains(search_kw, case=False, na=False)
            ]
            
        if sel_khoa != "Tất cả":
            filtered = filtered[filtered['Khoa_Phong'].astype(str) == sel_khoa]
            
        if sel_tt != "Tất cả":
            filtered = filtered[filtered['Trang_Thai'].astype(str) == sel_tt]
            
        if sel_month != "Tất cả":
            selected_m = int(sel_month.replace("Tháng ", ""))
            filtered['Ngay_Sinh_DT'] = parse_date_vietnam(filtered['Ngay_Sinh'])
            filtered = filtered[filtered['Ngay_Sinh_DT'].dt.month == selected_m]
            
        st.write(f"Hiển thị **{len(filtered)}** / **{len(df)}** hồ sơ nhân sự:")
        
        display_df = filtered.copy()
        if 'Ngay_Sinh_HienThi' in display_df.columns:
            display_df['Ngay_Sinh'] = display_df['Ngay_Sinh_HienThi']
            
        display_cols = ['Ma_NV', 'Ho_Ten', 'Ngay_Sinh', 'Gioi_Tinh', 'Khoa_Phong', 'Chuc_Vu', 'Trinh_Do_Chuyen_Mon', 'Trang_Thai']
        valid_cols = [c for c in display_cols if c in display_df.columns]
        
        st.dataframe(display_df[valid_cols] if not display_df.empty else display_df, use_container_width=True)

# -----------------------------------------------------------------------------
# MENU 4: THÊM MỚI HỒ SƠ NHÂN SỰ
# -----------------------------------------------------------------------------
elif menu == "➕ Thêm mới Hồ sơ Nhân sự":
    st.title("➕ THÊM MỚI HỒ SƠ NHÂN SỰ")
    st.markdown("---")
    
    with st.form("form_add_emp", clear_on_submit=True):
        st.subheader("I. Thông tin Hành chính & Cá nhân")
        col1, col2, col3 = st.columns(3)
        with col1:
            ma_nv = st.text_input("Mã Nhân viên (*):", value=f"BV{len(df)+1:04d}")
            ho_ten = st.text_input("Họ và Tên khai sinh (*):")
            ten_khac = st.text_input("Tên gọi khác / Bí danh:", value="Không")
            ngay_sinh = st.date_input("Ngày sinh:", value=datetime(1990, 1, 1), format="DD/MM/YYYY")
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
            ngay_dang = st.text_input("Ngày vào Đảng (DD/MM/YYYY hoặc Chưa):", value="Chưa")
            ngay_ngu = st.text_input("Ngày nhập ngũ / Quân hàm:", value="Không")

        st.subheader("II. Chức danh, Ngạch bậc & Chuyên môn Y tế")
        col4, col5, col6 = st.columns(3)
        with col4:
            khoa_phong = st.text_input("Khoa / Phòng làm việc:")
            chuc_vu = st.text_input("Chức vụ:", value="Nhiệm vụ chuyên môn")
            ngach = st.text_input("Ngạch viên chức:")
            td_chuyen_mon = st.text_input("Trình độ chuyên môn (BS/ĐD/Dược sĩ...):")
        with col5:
            bac_luong = st.number_input("Bậc lương:", min_value=1, max_value=12, value=1)
            he_so_luong = st.number_input("Hệ số lương:", min_value=1.0, max_value=10.0, value=2.34, step=0.01)
            ngay_luong = st.date_input("Ngày nâng lương tiếp theo:", value=datetime.now() + timedelta(days=1095), format="DD/MM/YYYY")
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
            ngay_hd = st.date_input("Ngày hết hạn HĐ:", value=datetime.now() + timedelta(days=365), format="DD/MM/YYYY")
        with col8:
            khen_thuong = st.text_input("Khen thưởng / Kỷ luật:", value="Không")
            danh_hieu = st.text_input("Danh hiệu phong tặng:", value="Không")
        with col9:
            trang_thai = st.selectbox("Trạng thái công tác:", ["Đang làm việc", "Nghỉ thai sản", "Đã nghỉ việc"])

        btn_save = st.form_submit_button("💾 LƯU HỒ SƠ VÀO CSDL")
        
        if btn_save:
            if not ma_nv or not ho_ten:
                st.error("Vui lòng điền đầy đủ Mã nhân viên và Họ tên!")
            else:
                str_ngay_sinh = ngay_sinh.strftime('%d/%m/%Y')
                new_row = {
                    "Ma_NV": ma_nv.strip(), "Ho_Ten": ho_ten.upper().strip(), "Ten_Goi_Khac": ten_khac.strip(),
                    "Ngay_Sinh": str_ngay_sinh, "Gioi_Tinh": gioi_tinh, "Noi_Sinh": noi_sinh.strip(), "Que_Quan": que_quan.strip(),
                    "Dan_Toc": dan_toc.strip(), "Ton_Giao": ton_giao.strip(), "Noi_O_Hien_Nay": noi_o.strip(), "Dien_Thoai": dien_thoai.strip(),
                    "So_CCCD": so_cccd.strip(), "Khoa_Phong": khoa_phong.strip(), "Chuc_Vu": chuc_vu.strip(), "Ngach_Vien_Chuc": ngach.strip(),
                    "Bac_Luong": bac_luong, "He_So_Luong": he_so_luong, "Ngay_Nang_Luong": pd.to_datetime(ngay_luong),
                    "Trinh_Do_Giao_Duc": "12/12", "Trinh_Do_Chuyen_Mon": td_chuyen_mon.strip(), "Ly_Luan_Chinh_Tri": td_llct,
                    "Ngoai_Ngu": ngoai_ngu.strip(), "Tin_Hoc": tin_hoc.strip(), "So_CCHN": so_cchn.strip(), "Gio_CME": gio_cme,
                    "Ngay_Vao_Dang": ngay_dang.strip(), "Ngay_Nhap_Ngu": ngay_ngu.strip(), "Danh_Hieu_Phong_Tang": danh_hieu.strip(),
                    "Khen_Thuong_Ky_Luat": khen_thuong.strip(), "Suc_Khoe_Thuong_Binh": suc_khoe.strip(), "Loai_HD": loai_hd,
                    "Ngay_Het_Han_HD": pd.to_datetime(ngay_hd), "Trang_Thai": trang_thai.strip()
                }
                st.session_state.df_nhansu = pd.concat([st.session_state.df_nhansu, pd.DataFrame([new_row])], ignore_index=True)
                save_data_to_db(st.session_state.df_nhansu)
                st.success(f"✅ Đã thêm mới thành công hồ sơ {ho_ten.upper()} vào CSDL!")

# -----------------------------------------------------------------------------
# MENU 5: CHỈNH SỬA / XÓA HỒ SƠ
# -----------------------------------------------------------------------------
elif menu == "✏️ Chỉnh sửa / Xóa Hồ sơ":
    st.title("✏️ CẬP NHẬT HOẶC XÓA HỒ SƠ NHÂN SỰ")
    st.markdown("---")
    
    if df.empty:
        st.warning("⚠️ Cơ sở dữ liệu hiện chưa có hồ sơ nào.")
    else:
        selected_id = st.selectbox("🔍 Chọn Mã Nhân Viên hoặc Họ Tên cần thao tác:", df['Ma_NV'].astype(str) + " - " + df['Ho_Ten'].astype(str))
        
        if selected_id:
            ma_selected = selected_id.split(" - ")[0]
            emp_idx = df[df['Ma_NV'].astype(str) == ma_selected].index[0]
            emp = df.loc[emp_idx]
            
            tab_edit, tab_delete = st.tabs(["✏️ Chỉnh sửa thông tin", "🗑️ Xóa hồ sơ"])
            
            with tab_edit:
                with st.form("form_edit_emp"):
                    st.subheader(f"Cập nhật thông tin: {emp['Ho_Ten']} ({emp['Ma_NV']})")
                    
                    ce1, ce2, ce3 = st.columns(3)
                    with ce1:
                        e_khoa = st.text_input("Khoa/Phòng:", value=str(emp['Khoa_Phong']))
                        e_chucvu = st.text_input("Chức vụ:", value=str(emp['Chuc_Vu']))
                        e_hsl = st.number_input("Hệ số lương:", value=float(emp['He_So_Luong']) if pd.notnull(emp['He_So_Luong']) else 2.34, step=0.01)
                    with ce2:
                        e_cme = st.number_input("Số giờ CME tích lũy:", value=int(emp['Gio_CME']) if pd.notnull(emp['Gio_CME']) else 0)
                        e_cchn = st.text_input("Số CCHN:", value=str(emp['So_CCHN']))
                        e_dang = st.text_input("Ngày vào Đảng:", value=str(emp['Ngay_Vao_Dang']))
                    with ce3:
                        e_trangthai = st.text_input("Trạng thái công tác:", value=str(emp['Trang_Thai']))
                        e_luong = st.date_input("Ngày nâng lương tiếp theo:", value=pd.to_datetime(emp['Ngay_Nang_Luong']) if pd.notnull(emp['Ngay_Nang_Luong']) else datetime.now(), format="DD/MM/YYYY")
                        e_hd = st.date_input("Ngày hết hạn HĐ:", value=pd.to_datetime(emp['Ngay_Het_Han_HD']) if pd.notnull(emp['Ngay_Het_Han_HD']) else datetime.now(), format="DD/MM/YYYY")
                        
                    btn_update = st.form_submit_button("💾 CẬP NHẬT & LƯU CSDL")
                    
                    if btn_update:
                        st.session_state.df_nhansu.at[emp_idx, 'Khoa_Phong'] = e_khoa.strip()
                        st.session_state.df_nhansu.at[emp_idx, 'Chuc_Vu'] = e_chucvu.strip()
                        st.session_state.df_nhansu.at[emp_idx, 'He_So_Luong'] = e_hsl
                        st.session_state.df_nhansu.at[emp_idx, 'Gio_CME'] = e_cme
                        st.session_state.df_nhansu.at[emp_idx, 'So_CCHN'] = e_cchn.strip()
                        st.session_state.df_nhansu.at[emp_idx, 'Ngay_Vao_Dang'] = e_dang.strip()
                        st.session_state.df_nhansu.at[emp_idx, 'Trang_Thai'] = e_trangthai.strip()
                        st.session_state.df_nhansu.at[emp_idx, 'Ngay_Nang_Luong'] = pd.to_datetime(e_luong)
                        st.session_state.df_nhansu.at[emp_idx, 'Ngay_Het_Han_HD'] = pd.to_datetime(e_hd)
                        save_data_to_db(st.session_state.df_nhansu)
                        st.success("✅ Đã cập nhật thành công dữ liệu!")
                        st.rerun()
                        
            with tab_delete:
                st.warning(f"⚠️ Bạn có chắc chắn muốn xóa hồ sơ cán bộ **{emp['Ho_Ten']}** ({emp['Ma_NV']})?")
                if st.button("❌ XÁC NHẬN XÓA HỒ SƠ"):
                    st.session_state.df_nhansu = st.session_state.df_nhansu.drop(emp_idx).reset_index(drop=True)
                    save_data_to_db(st.session_state.df_nhansu)
                    st.success("Đã xóa hồ sơ thành công!")
                    st.rerun()

# -----------------------------------------------------------------------------
# MENU 6: NHẬP / XUẤT EXCEL (MẪU 2C)
# -----------------------------------------------------------------------------
elif menu == "📂 Nhập / Xuất Excel (Mẫu 2C)":
    st.title("📂 ĐỒNG BỘ DỮ LIỆU EXCEL MẪU 2C-BNV")
    st.markdown("---")
    
    col_x, col_m = st.columns(2)
    
    with col_x:
        st.subheader("1. Xuất Báo cáo Excel từ CSDL")
        st.write(f"Đang lưu trữ: **{len(df)}** hồ sơ nhân sự")
        
        output_all = io.BytesIO()
        with pd.ExcelWriter(output_all, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='DanhSach_2C_BNV')
        
        st.download_button(
            label="📥 TẢI VỀ FILE EXCEL (.XLSX)",
            data=output_all.getvalue(),
            file_name=f"Danh_Sach_Nhan_Su_BV_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    with col_m:
        st.subheader("2. Tải File Excel Mẫu Chuẩn")
        sample_data = [{
            "Ma_NV": "BV0001", "Ho_Ten": "NGUYỄN VĂN AN", "Ten_Goi_Khac": "Không", 
            "Ngay_Sinh": "15/05/1980", "Gioi_Tinh": "Nam", "Noi_Sinh": "Hà Nội", "Que_Quan": "Nam Định",
            "Dan_Toc": "Kinh", "Ton_Giao": "Không", "Noi_O_Hien_Nay": "Hoàn Kiếm, Hà Nội", "Dien_Thoai": "0912345678",
            "So_CCCD": "001080012345", "Khoa_Phong": "Khoa Cấp cứu", "Chuc_Vu": "Trưởng khoa",
            "Ngach_Vien_Chuc": "Bác sĩ chính (V.08.01.01)", "Bac_Luong": 3, "He_So_Luong": 5.08, 
            "Ngay_Nang_Luong": "15/09/2026", "Trinh_Do_Giao_Duc": "12/12", "Trinh_Do_Chuyen_Mon": "Bác sĩ CKII",
            "Ly_Luan_Chinh_Tri": "Cao cấp", "Ngoai_Ngu": "Anh B2", "Tin_Hoc": "Ứng dụng CNTT cơ bản",
            "So_CCHN": "001234/BYT-CCHN", "Gio_CME": 52, "Ngay_Vao_Dang": "03/02/2010", "Ngay_Nhap_Ngu": "Không",
            "Danh_Hieu_Phong_Tang": "Thầy thuốc Ưu tú", "Khen_Thuong_Ky_Luat": "Bằng khen Bộ Y tế",
            "Suc_Khoe_Thuong_Binh": "Tốt", "Loai_HD": "Không xác định thời hạn", "Ngay_Het_Han_HD": "31/12/2035",
            "Trang_Thai": "Đang làm việc"
        }]
        output_tmp = io.BytesIO()
        with pd.ExcelWriter(output_tmp, engine='openpyxl') as writer:
            pd.DataFrame(sample_data).to_excel(writer, index=False, sheet_name='Mau_2C_BNV')
            
        st.download_button(
            label="📄 TẢI FILE EXCEL MẪU (.XLSX)",
            data=output_tmp.getvalue(),
            file_name="Mau_Ly_Lich_2C_BNV.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    st.markdown("---")
    st.subheader("3. Nạp File Excel Nhân Sự Đã Điền Vào CSDL")
    uploaded_file = st.file_uploader("Upload file Excel (.xlsx) chứa dữ liệu nhân sự", type=["xlsx", "csv"])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df_upload = pd.read_csv(uploaded_file)
            else:
                df_upload = pd.read_excel(uploaded_file)
                
            st.success(f"Đã đọc thành công {len(df_upload)} hồ sơ từ file!")
            st.dataframe(df_upload.head(5))
            
            if st.button("🚀 XÁC NHẬN NẠP VÀ LƯU VÀO CƠ SỞ DỮ LIỆU"):
                df_cleaned = clean_dataframe(df_upload)
                st.session_state.df_nhansu = df_cleaned
                save_data_to_db(df_cleaned)
                st.success(f"✅ ĐÃ NẠP THÀNH CÔNG {len(df_cleaned)} HỒ SƠ VÀO CSDL!")
                st.rerun()
        except Exception as e:
            st.error(f"Lỗi nạp file: {e}")

# -----------------------------------------------------------------------------
# MENU 7: THIẾT LẬP HỆ THỐNG
# -----------------------------------------------------------------------------
elif menu == "⚙️ Thiết lập Hệ thống":
    st.title("⚙️ THIẾT LẬP HỆ THỐNG & QUẢN TRỊ CSDL")
    st.markdown("---")
    
    st.subheader("1. Thông tin Cơ sở Dữ liệu")
    st.write(f"- File CSDL hiện tại: `{DB_FILE}`")
    st.write(f"- Tổng số bản ghi trong CSDL: **{len(df)}** hồ sơ")
    
    st.markdown("---")
    st.subheader("2. Dọn dẹp & Reset Cơ sở Dữ liệu")
    st.warning("⚠️ **CẢNH BÁO:** Thao tác xóa dữ liệu không thể hoàn tác. Hãy sao lưu/xuất file Excel trước khi tiến hành!")
    
    confirm_reset = st.checkbox("Tôi hiểu và muốn xóa toàn bộ dữ liệu hiện tại trong CSDL SQLite")
    if confirm_reset:
        if st.button("🔥 XÁC NHẬN XÓA SẠCH DỮ LIỆU CSDL"):
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM nhansu")
            conn.commit()
            conn.close()
            
            st.session_state.df_nhansu = pd.DataFrame()
            st.success("✅ Đã xóa toàn bộ dữ liệu trong cơ sở dữ liệu SQLite!")
            st.rerun()
