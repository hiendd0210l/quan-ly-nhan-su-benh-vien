import streamlit as st
import pandas as pd
import io
import re
from datetime import datetime

# ==========================================
# 1. CẤU HÌNH TRANG & GIAO DIỆN STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Hệ thống Quản lý Nhân sự & Kiểm tra Sinh nhật",
    page_icon="🏥",
    layout="wide"
)

# Thêm CSS tùy chỉnh giao diện
st.markdown("""
<style>
    .main-header {
        font-size: 26px;
        font-weight: bold;
        color: #0e4ead;
        text-align: center;
        margin-bottom: 20px;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #e9ecef;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-header'>🏥 BỆNH VIỆN BƯU ĐIỆN - HỆ THỐNG QUẢN LÝ NHÂN SỰ & ĐỐI CHIẾU KẾT QUẢ</div>", unsafe_allow_html=True)

# ==========================================
# 2. KHỞI TẠO DỮ LIỆU MẪU HỆ THỐNG (SESSION STATE)
# ==========================================
if 'df_nhansu' not in st.session_state:
    # Khai báo dữ liệu mẫu hệ thống để kiểm thử
    sample_data = [
        {"Ma_NV": "N0009", "Ho_Ten": "Phạm Thị Thanh Tú", "Ngay_Sinh": "17/09/1980", "Gioi_Tinh": "Nữ", "Khoa_Phong": "Ban Giám đốc", "Chuc_Vu": "Phó Giám đốc"},
        {"Ma_NV": "N0295", "Ho_Ten": "Mai Anh Tuấn", "Ngay_Sinh": "03/09/1985", "Gioi_Tinh": "Nam", "Khoa_Phong": "Phòng Hành chính - Quản trị", "Chuc_Vu": "Phó trưởng phòng"},
        {"Ma_NV": "N0430", "Ho_Ten": "Vương Vũ Việt Hà", "Ngay_Sinh": "26/09/1982", "Gioi_Tinh": "Nam", "Khoa_Phong": "Trung tâm Hỗ trợ sinh sản", "Chuc_Vu": "Giám đốc TT"},
        {"Ma_NV": "N0324", "Ho_Ten": "Nguyễn Bảo Khánh", "Ngay_Sinh": "15/09/1988", "Gioi_Tinh": "Nam", "Khoa_Phong": "Trung tâm Y tế lao động Bưu điện", "Chuc_Vu": "Phó Giám đốc TT"},
        {"Ma_NV": "N0112", "Ho_Ten": "Nguyễn Thị Thu Hằng", "Ngay_Sinh": "18/09/1983", "Gioi_Tinh": "Nữ", "Khoa_Phong": "Khoa Khám bệnh", "Chuc_Vu": "Trưởng khoa"},
        {"Ma_NV": "N1070", "Ho_Ten": "Vũ Thị Nga", "Ngay_Sinh": "07/09/1990", "Gioi_Tinh": "Nữ", "Khoa_Phong": "Khoa Dược", "Chuc_Vu": "Phó trưởng khoa"},
        {"Ma_NV": "N0402", "Ho_Ten": "Lê Minh Thuận", "Ngay_Sinh": "15/09/1987", "Gioi_Tinh": "Nam", "Khoa_Phong": "Khoa Ngoại", "Chuc_Vu": "Phó trưởng khoa"},
        {"Ma_NV": "N0624", "Ho_Ten": "Đặng Ngọc Tuyến", "Ngay_Sinh": "15/09/1989", "Gioi_Tinh": "Nam", "Khoa_Phong": "Khoa Nội", "Chuc_Vu": "Phó trưởng khoa"},
        {"Ma_NV": "N0999", "Ho_Ten": "Trần Văn Bỏ Sót", "Ngay_Sinh": "10/09/1992", "Gioi_Tinh": "Nam", "Khoa_Phong": "Phòng TSKT", "Chuc_Vu": "Chuyên viên"}, # Người có trên App nhưng Excel bị thiếu
    ]
    st.session_state.df_nhansu = pd.DataFrame(sample_data)

df_db = st.session_state.df_nhansu.copy()

# ==========================================
# 3. XỬ LÝ DỮ LIỆU ĐỊNH DẠNG NGÀY THÁNG
# ==========================================
# Đồng bộ chuyển đổi cột Ngay_Sinh về định dạng datetime chuẩn
df_db['Ngay_Sinh_DT'] = pd.to_datetime(df_db['Ngay_Sinh'], dayfirst=True, errors='coerce')
df_db['Thang_Sinh'] = df_db['Ngay_Sinh_DT'].dt.month
df_db['Ngay_Thang_Short'] = df_db['Ngay_Sinh_DT'].dt.strftime('%d-%m')

# ==========================================
# 4. HÀM XỬ LÝ BÓC TÁCH & ĐỐI CHIẾU EXCEL
# ==========================================
def clean_and_parse_uploaded_excel(file_bytes):
    """
    Tự động quét và làm sạch file Excel dạng báo cáo đặc thù của BVBĐ.
    Loại bỏ các dòng gộp tên Khoa/Phòng và các dòng chữ ký cuối file.
    """
    df_raw = pd.read_excel(file_bytes)
    
    # 1. Tìm vị trí dòng chứa Tiêu đề bảng (Header)
    header_row_idx = None
    for idx, row in df_raw.iterrows():
        row_values = [str(val).lower() for val in row.values]
        if any('mã nv' in v for v in row_values) or any('họ và tên' in v for v in row_values):
            header_row_idx = idx
            break
            
    if header_row_idx is not None:
        df_raw.columns = df_raw.iloc[header_row_idx].values
        df_raw = df_raw.iloc[header_row_idx + 1:].copy()
        
    # Chuẩn hóa tên cột
    df_raw.columns = [str(c).strip() for c in df_raw.columns]
    
    # Ánh ánh tên cột về chuẩn
    col_mapping = {}
    for col in df_raw.columns:
        cl = col.lower()
        if 'mã nv' in cl: col_mapping[col] = 'Ma_NV'
        elif 'họ và tên' in cl: col_mapping[col] = 'Ho_Ten'
        elif 'ngày' in cl: col_mapping[col] = 'Ngay_Thang'
        elif 'chức vụ' in cl: col_mapping[col] = 'Chuc_Vu'
        elif 'số tiền' in cl: col_mapping[col] = 'So_Tien'
        elif 'stt' in cl: col_mapping[col] = 'STT'
        
    df_cleaned = df_raw.rename(columns=col_mapping)
    
    # Lọc lấy những dòng chứa Mã NV thực sự (Format bắt đầu bằng N)
    if 'Ma_NV' in df_cleaned.columns:
        df_cleaned['Ma_NV'] = df_cleaned['Ma_NV'].astype(str).str.strip().str.upper()
        # Loại bỏ các dòng tiêu đề khoa/phòng và các dòng chữ ký (như TRƯỞNG PHÒNG, GIÁM ĐỐC...)
        df_emp = df_cleaned[df_cleaned['Ma_NV'].str.startswith('N')].copy()
        return df_emp
    else:
        return pd.DataFrame()

def run_reconciliation(df_app_month, df_excel_cleaned):
    """
    Thực hiện so sánh đối chiếu danh sách Lọc của App với danh sách Excel upload.
    Khóa chính định danh: Ma_NV.
    """
    report = {
        'match': [],
        'missing_in_excel': [],
        'extra_in_excel': [],
        'mismatch_detail': []
    }
    
    df_app = df_app_month.copy()
    df_exc = df_excel_cleaned.copy()
    
    df_app['Ma_NV_Key'] = df_app['Ma_NV'].astype(str).str.strip().str.upper()
    df_exc['Ma_NV_Key'] = df_exc['Ma_NV'].astype(str).str.strip().str.upper()
    
    set_app = set(df_app['Ma_NV_Key'])
    set_exc = set(df_exc['Ma_NV_Key'])
    
    # 1. Tập mã trùng khớp giữa 2 bên
    common_ids = set_app.intersection(set_exc)
    
    # 2. Nhân sự hệ thống có nhưng Excel lập thiếu
    missing_ids = set_app - set_exc
    report['missing_in_excel'] = df_app[df_app['Ma_NV_Key'].isin(missing_ids)]
    
    # 3. Nhân sự Excel có nhưng hệ thống không thuộc tháng này
    extra_ids = set_exc - set_app
    report['extra_in_excel'] = df_exc[df_exc['Ma_NV_Key'].isin(extra_ids)]
    
    # 4. Kiểm tra sai lệch thông tin chi tiết với mã trùng
    mismatches = []
    matches = []
    
    for eid in common_ids:
        row_app = df_app[df_app['Ma_NV_Key'] == eid].iloc[0]
        row_exc = df_exc[df_exc['Ma_NV_Key'] == eid].iloc[0]
        
        # So sánh Ngày/Tháng (dd-mm)
        app_date_str = str(row_app.get('Ngay_Thang_Short', '')).strip()
        exc_date_str = str(row_exc.get('Ngay_Thang', '')).strip()
        
        diffs = []
        if str(row_app.get('Ho_Ten', '')).strip().lower() != str(row_exc.get('Ho_Ten', '')).strip().lower():
            diffs.append(f"Họ tên: App='{row_app.get('Ho_Ten')}' ⚡ Excel='{row_exc.get('Ho_Ten')}'")
            
        if app_date_str != exc_date_str:
            diffs.append(f"Ngày/tháng sinh: App='{app_date_str}' ⚡ Excel='{exc_date_str}'")
            
        if diffs:
            mismatches.append({
                'Ma_NV': eid,
                'Ho_Ten_App': row_app.get('Ho_Ten'),
                'Khoa_Phong': row_app.get('Khoa_Phong'),
                'Chi_Tiet_Sai_Lech': " | ".join(diffs)
            })
        else:
            matches.append(row_app)
            
    report['match'] = pd.DataFrame(matches)
    report['mismatch_detail'] = pd.DataFrame(mismatches)
    
    return report

# ==========================================
# 5. ĐIỀU HƯỚNG MENU CHỨC NĂNG (SIDEBAR)
# ==========================================
st.sidebar.title("📌 DANH MỤC CHỨC NĂNG")
menu = st.sidebar.radio(
    "Chọn phân hệ làm việc:",
    [
        "🎂 1. Lọc Danh sách Sinh nhật",
        "🔍 2. Kiểm tra & Đối chiếu File Excel",
        "📂 3. Quản lý Hồ sơ Nhân sự"
    ]
)

# ==========================================
# PHÂN HỆ 1: LỌC DANH SÁCH SINH NHẬT
# ==========================================
if menu == "🎂 1. Lọc Danh sách Sinh nhật":
    st.subheader("🎂 LỌC SINH NHẬT CÁN BỘ CÔNG NHÂN VIÊN THEO THÁNG")
    
    col_sel, col_space = st.columns([1, 2])
    with col_sel:
        selected_month = st.selectbox("Chọn tháng sinh nhật:", range(1, 13), index=8) # Mặc định tháng 9
        
    # Lọc dữ liệu
    df_filtered = df_db[df_db['Thang_Sinh'] == selected_month].copy()
    
    st.success(f"Tổng số nhân sự có sinh nhật trong **Tháng {selected_month}**: **{len(df_filtered)} người**")
    
    if not df_filtered.empty:
        # Bảng hiển thị kết quả
        st.dataframe(
            df_filtered[['Ma_NV', 'Ho_Ten', 'Ngay_Sinh', 'Gioi_Tinh', 'Khoa_Phong', 'Chuc_Vu']],
            use_container_width=True,
            hide_index=True
        )
        
        # Xuất dữ liệu Excel chuẩn
        output_month = io.BytesIO()
        with pd.ExcelWriter(output_month, engine='openpyxl') as writer:
            df_filtered.to_excel(writer, index=False, sheet_name=f'Sinh_Nhat_T{selected_month}')
            
        st.download_button(
            label=f"📥 Tải danh sách sinh nhật Tháng {selected_month} (.xlsx)",
            data=output_month.getvalue(),
            file_name=f"DS_SinhNhat_Thang_{selected_month}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning(f"Không có nhân sự nào sinh nhật trong Tháng {selected_month}.")

# ==========================================
# PHÂN HỆ 2: KIỂM TRA & ĐỐI CHIẾU FILE EXCEL
# ==========================================
elif menu == "🔍 2. Kiểm tra & Đối chiếu File Excel":
    st.subheader("🔍 ĐỐI CHIẾU FILE EXCEL BÊN NGOÀI VỚI DỮ LIỆU ĐÃ LỌC")
    st.caption("Chức năng cho phép upload tệp Excel do người khác lập ra để ứng dụng tự động kiểm tra xem có khớp với danh sách hệ thống hay không.")
    
    col_m, col_up = st.columns([1, 2])
    with col_m:
        check_month = st.selectbox("Chọn tháng cần kiểm tra đối chiếu:", range(1, 13), index=8)
    
    # Lấy danh sách chuẩn của tháng từ ứng dụng
    df_app_target = df_db[df_db['Thang_Sinh'] == check_month].copy()
    
    st.info(f"📌 Danh sách hệ thống đang có: **{len(df_app_target)}** nhân sự sinh nhật Tháng {check_month}.")
    
    uploaded_file = st.file_uploader("Upload tệp Excel cần kiểm tra (.xlsx, .xls):", type=["xlsx", "xls"])
    
    if uploaded_file is not None:
        try:
            # 1. Bóc tách và làm sạch dữ liệu tệp upload
            df_excel_cleaned = clean_and_parse_uploaded_excel(uploaded_file)
            
            if df_excel_cleaned.empty:
                st.error("Không tìm thấy dữ liệu nhân sự hợp lệ trong tệp Excel upload! Vui lòng kiểm tra lại cấu trúc file.")
            else:
                st.success(f"Đã đọc và lọc sạch dữ liệu từ tệp Excel: Tìm thấy **{len(df_excel_cleaned)}** bản ghi nhân sự.")
                
                # 2. Thực hiện đối chiếu
                res = run_reconciliation(df_app_target, df_excel_cleaned)
                
                st.markdown("---")
                st.subheader("📊 BÁO CÁO KẾT QUẢ ĐỐI CHIẾU")
                
                # Hiển thị chỉ số
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("✅ Khớp 100%", f"{len(res['match'])} người")
                c2.metric("❌ File Excel THIẾU", f"{len(res['missing_in_excel'])} người")
                c3.metric("⚠️ File Excel THỪA/LỆCH", f"{len(res['extra_in_excel'])} người")
                c4.metric("⚡ LỆCH thông tin", f"{len(res['mismatch_detail'])} trường hợp")
                
                # Tab chi tiết
                t_missing, t_extra, t_mismatch, t_match = st.tabs([
                    f"❌ File Excel thiếu ({len(res['missing_in_excel'])})",
                    f"⚠️ File Excel thừa / Sai tháng ({len(res['extra_in_excel'])})",
                    f"⚡ Lệch thông tin chi tiết ({len(res['mismatch_detail'])})",
                    f"✅ Khớp hoàn toàn ({len(res['match'])})"
                ])
                
                with t_missing:
                    st.write("**Danh sách nhân sự có sinh nhật trong tháng trên Hệ thống nhưng tệp Excel lập thiếu:**")
                    if not res['missing_in_excel'].empty:
                        st.dataframe(res['missing_in_excel'][['Ma_NV', 'Ho_Ten', 'Ngay_Sinh', 'Khoa_Phong', 'Chuc_Vu']], use_container_width=True, hide_index=True)
                    else:
                        st.success("Tệp Excel không bị thiếu nhân sự nào!")
                        
                with t_extra:
                    st.write("**Danh sách nhân sự có trong tệp Excel nhưng Hệ thống xác định không thuộc sinh nhật tháng này:**")
                    if not res['extra_in_excel'].empty:
                        st.dataframe(res['extra_in_excel'], use_container_width=True, hide_index=True)
                    else:
                        st.success("Tệp Excel không có nhân sự bị thừa/nhầm tháng!")
                        
                with t_mismatch:
                    st.write("**Nhân sự trùng Mã NV nhưng sai lệch Ngày sinh hoặc Họ tên giữa 2 bên:**")
                    if not res['mismatch_detail'].empty:
                        st.dataframe(res['mismatch_detail'], use_container_width=True, hide_index=True)
                    else:
                        st.success("Không có trường hợp nào bị sai lệch thông tin chi tiết!")
                        
                with t_match:
                    st.write("**Danh sách nhân sự hoàn toàn trùng khớp giữa Hệ thống và tệp Excel:**")
                    if not res['match'].empty:
                        st.dataframe(res['match'][['Ma_NV', 'Ho_Ten', 'Ngay_Sinh', 'Khoa_Phong', 'Chuc_Vu']], use_container_width=True, hide_index=True)
                        
                # 3. Xuất file Báo cáo tổng hợp đối chiếu
                output_report = io.BytesIO()
                with pd.ExcelWriter(output_report, engine='openpyxl') as writer:
                    res['missing_in_excel'].to_excel(writer, index=False, sheet_name='Excel_Thieu')
                    res['extra_in_excel'].to_excel(writer, index=False, sheet_name='Excel_Thua_NhamThang')
                    res['mismatch_detail'].to_excel(writer, index=False, sheet_name='Sai_Lech_Thong_Tin')
                    res['match'].to_excel(writer, index=False, sheet_name='Khop_Hoan_Toan')
                    
                st.download_button(
                    label="📥 TẢI BÁO CÁO KẾT QUẢ ĐỐI CHIẾU (.XLSX)",
                    data=output_report.getvalue(),
                    file_name=f"Bao_Cao_Doi_Chieu_T{check_month}_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                
        except Exception as e:
            st.error(f"Xảy ra lỗi khi đọc và đối chiếu tệp Excel: {e}")

# ==========================================
# PHÂN HỆ 3: QUẢN LÝ HỒ SƠ NHÂN SỰ
# ==========================================
elif menu == "📂 3. Quản lý Hồ sơ Nhân sự":
    st.subheader("📂 DỮ LIỆU HỒ SƠ NHÂN SỰ TRÊN HỆ THỐNG")
    
    st.dataframe(st.session_state.df_nhansu, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.write("**Thêm nhân sự mới vào hệ thống:**")
    with st.form("add_nv_form"):
        c_m, c_h, c_n = st.columns(3)
        ma_nv = c_m.text_input("Mã Nhân viên (Ví dụ: N1025)")
        ho_ten = c_h.text_input("Họ và tên")
        ngay_sinh = c_n.text_input("Ngày sinh (dd/mm/yyyy)")
        
        c_g, c_k, c_cv = st.columns(3)
        gioi_tinh = c_g.selectbox("Giới tính", ["Nam", "Nữ"])
        khoa_phong = c_k.text_input("Khoa/Phòng")
        chuc_vu = c_cv.text_input("Chức vụ")
        
        submitted = st.form_submit_button("Lưu nhân sự")
        if submitted:
            if ma_nv and ho_ten and ngay_sinh:
                new_row = {
                    "Ma_NV": ma_nv.strip().upper(),
                    "Ho_Ten": ho_ten.strip(),
                    "Ngay_Sinh": ngay_sinh.strip(),
                    "Gioi_Tinh": gioi_tinh,
                    "Khoa_Phong": khoa_phong.strip(),
                    "Chuc_Vu": chuc_vu.strip()
                }
                st.session_state.df_nhansu = pd.concat([st.session_state.df_nhansu, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"Đã thêm thành công nhân sự {ho_ten} ({ma_nv})!")
                st.rerun()
            else:
                st.error("Vui lòng nhập đầy đủ Mã NV, Họ tên và Ngày sinh!")
