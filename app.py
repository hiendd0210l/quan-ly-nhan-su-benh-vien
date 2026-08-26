import streamlit as st
import pandas as pd
import datetime
from sqlalchemy import create_engine, text

# ==============================================================================
# 1. KHỞI TẠO VÀ CẤU HÌNH CƠ SỞ DỮ LIỆU (POSTGRESQL - NEON.TECH)
# ==============================================================================

@st.cache_resource
def get_db_engine():
    try:
       # Kiểm tra xem cấu hình Secrets đã tồn tại chưa
        if "postgres" in st.secrets and "url" in st.secrets["postgres"]:
            db_url = st.secrets["postgres"]["url"]
            if db_url.startswith("postgres://"):
                db_url = db_url.replace("postgres://", "postgresql://", 1)
            return create_engine(db_url)
        else:
            st.error("⚠️ Chưa cấu hình chuỗi kết nối trong mục Secrets trên Streamlit Cloud!")
            return None
    except Exception as e:
        st.error(f"⚠️ Lỗi kết nối CSDL: {e}")
        return None

engine = get_db_engine()

def init_db():
    """Khởi tạo các bảng dữ liệu nếu chưa tồn tại"""
    if engine:
        with engine.begin() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS nhan_su (
                    ma_nv VARCHAR(50) PRIMARY KEY,
                    ho_ten VARCHAR(100) NOT NULL,
                    phong_ban VARCHAR(100),
                    khoi VARCHAR(100),
                    chuc_vu VARCHAR(100),
                    trinh_do VARCHAR(100),
                    chuyen_mon VARCHAR(100),
                    loai_hop_dong VARCHAR(100),
                    ngay_het_han_hd DATE,
                    bac_luong VARCHAR(50),
                    ngay_nang_luong DATE,
                    tiet_cme INTEGER DEFAULT 0,
                    so_cchn VARCHAR(100),
                    ngay_het_han_cchn DATE,
                    ngay_sinh DATE,
                    is_dang_vien INTEGER DEFAULT 0,
                    trang_thai VARCHAR(50) DEFAULT 'Đang làm việc'
                );
            """))

init_db()


def insert_sample_data_if_empty():
    """Chèn dữ liệu mẫu thực tế ban đầu nếu CSDL đang trống"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM nhan_su")
    count = cursor.fetchone()[0]
    
    if count == 0:
        sample_records = [
            ("NV001", "BS. Nguyễn Văn An", "Khoa Ngoại Tổng hợp", "Lâm sàng", "Bác sĩ điều trị", "TS/CKII", "Bác sĩ", "Xác định thời hạn", "2026-09-10", "3/9", "2026-11-01", 45, "CCHN-001", "2027-05-10", "1985-09-15", 1, "Đang làm việc"),
            ("NV002", "ĐD. Lê Thị Bích", "Khoa Gây mê Hồi sức", "Lâm sàng", "Điều dưỡng trưởng", "Đại học", "Điều dưỡng", "Không xác định TH", "2030-01-01", "3/9", "2026-09-15", 50, "CCHN-002", "2028-12-20", "1990-09-20", 0, "Đang làm việc"),
            ("NV003", "KTV. Phạm Quốc Cường", "Khoa Chẩn đoán Hình ảnh", "Cận lâm sàng", "Kỹ thuật viên", "Đại học", "KTV", "Xác định thời hạn", "2027-03-15", "2/9", "2027-05-10", 32, "CCHN-003", "2026-10-15", "1992-04-12", 0, "Đang làm việc"),
            ("NV004", "ThS.BS. Hoàng Minh Đức", "Trung tâm Hỗ trợ sinh sản", "Lâm sàng", "Trưởng khoa", "TS/CKII", "Bác sĩ", "Không xác định TH", "2035-01-01", "5/9", "2027-08-20", 48, "CCHN-004", "2026-09-30", "1980-09-05", 1, "Đang làm việc"),
            ("NV005", "NV. Trần Thị Hoa", "Phòng Tổ chức Cán bộ", "Phòng ban", "Chuyên viên", "Đại học", "Khác", "Không xác định TH", "2032-01-01", "4/9", "2026-09-25", 20, "", "", "1995-09-28", 1, "Đang làm việc")
        ]
        cursor.executemany("""
            INSERT INTO nhan_su VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_records)
        conn.commit()
    conn.close()

# Khởi tạo Database
init_db()
insert_sample_data_if_empty()

# ==============================================================================
# 2. CẤU HÌNH TRANG STREAMLIT & CUSTOM CSS
# ==============================================================================
st.set_page_config(
    page_title="Hệ thống Quản lý Nhân sự - Bệnh viện Bưu điện",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
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

# ==============================================================================
# 4. THANH MENUBAR VÀ ĐIỀU HƯỚNG SIDEBAR
# ==============================================================================
with st.sidebar:
    st.title("📌 DANH MỤC CHỨC NĂNG")
    
    st.caption("CHUNG & ĐIỀU HÀNH")
    menu_selected = st.radio(
        "Menu Điều hành",
        [
            "Trang chủ / Dashboard", 
            "Cập nhật danh sách (Excel 2C-BNV)", 
            "Thông báo & Văn bản"
        ],
        label_visibility="collapsed"
    )
    
    st.caption("QUẢN LÝ HỒ SƠ NHÂN SỰ")
    menu_hoso = st.selectbox("Nghiệp vụ Hồ sơ", [
        "Danh sách Hồ sơ Cán bộ CNV", 
        "Phân loại lao động", 
        "Hợp đồng Lao động", 
        "Hồ sơ Đảng viên"
    ], index=0, label_visibility="collapsed")
    
    st.caption("NGHIỆP VỤ CHUYÊN SÂU")
    menu_chuyenmôn = st.selectbox("Nghiệp vụ Chuyên môn", [
        "Giấy phép hành nghề (GPHN)",
        "Theo dõi Đào tạo CME",
        "Nâng bậc lương & Ngạch"
    ], index=0, label_visibility="collapsed")

# Kết nối CSDL lấy dữ liệu chung
conn = sqlite3.connect(DB_FILE)
df_all = pd.read_sql_query("SELECT * FROM nhan_su", conn)
conn.close()

# ==============================================================================
# 5. XỬ LÝ GIAO DIỆN CHÍNH THEO MENU
# ==============================================================================

# ------------------------------------------------------------------------------
# TRANG 1: TRANG CHỦ / DASHBOARD (TÍNH TOÁN THEO DỮ LIỆU THẬT)
# ------------------------------------------------------------------------------
if menu_selected == "Trang chủ / Dashboard":
    st.subheader("📊 Thống kê Tổng quan Toàn Bệnh viện")
    
    # Tính toán chỉ số động
    total_staff = len(df_all)
    lam_sang = len(df_all[df_all['khoi'] == 'Lâm sàng'])
    can_lam_sang = len(df_all[df_all['khoi'] == 'Cận lâm sàng'])
    phong_ban = len(df_all[df_all['khoi'] == 'Phòng ban'])
    
    trinh_do_cao = len(df_all[df_all['trinh_do'] == 'TS/CKII'])
    bac_si = len(df_all[df_all['chuyen_mon'] == 'Bác sĩ'])
    dd_ktv = len(df_all[df_all['chuyen_mon'].isin(['Điều dưỡng', 'KTV'])])
    
    hd_kxd = len(df_all[df_all['loai_hop_dong'] == 'Không xác định TH'])
    hd_xd = len(df_all[df_all['loai_hop_dong'] == 'Xác định thời hạn'])
    
    dang_vien = len(df_all[df_all['is_dang_vien'] == 1])
    dang_lam = len(df_all[df_all['trang_thai'] == 'Đang làm việc'])

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card metric-primary">
                <div class="metric-title">Tổng số lao động</div>
                <div class="metric-value">{total_staff}</div>
                <div class="metric-detail">
                    • Khối Lâm sàng: <b>{lam_sang}</b><br>
                    • Khối Cận lâm sàng: <b>{can_lam_sang}</b><br>
                    • Khối Phòng ban: <b>{phong_ban}</b>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-card metric-info">
                <div class="metric-title">Trình độ chuyên môn</div>
                <div class="metric-value">100%</div>
                <div class="metric-detail">
                    • TS/CKII/ThS/CKI: <b>{trinh_do_cao}</b><br>
                    • Bác sĩ / Dược sĩ: <b>{bac_si}</b><br>
                    • ĐD/KTV Đại học: <b>{dd_ktv}</b>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="metric-card metric-success">
                <div class="metric-title">Phân loại hợp đồng</div>
                <div class="metric-value">{total_staff}</div>
                <div class="metric-detail">
                    • HĐ Không xác định TH: <b>{hd_kxd}</b><br>
                    • HĐ Xác định thời hạn: <b>{hd_xd}</b><br>
                    • Chuyên gia/Khác: <b>{total_staff - hd_kxd - hd_xd}</b>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div class="metric-card metric-warning">
                <div class="metric-title">Trạng thái & Đảng viên</div>
                <div class="metric-value">{dang_vien} <span style="font-size:14px; font-weight:normal;">Đảng viên</span></div>
                <div class="metric-detail">
                    • Đang làm việc: <b>{dang_lam}</b><br>
                    • Tỷ lệ Đảng viên: <b>{(dang_vien/total_staff*100) if total_staff>0 else 0:.1f}%</b>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.write("") 

    # --- CẢNH BÁO TỰ ĐỘNG DỰA TRÊN DỮ LIỆU THẬT ---
    st.subheader("🔔 Cảnh báo Tự động & Lịch cần xử lý")
    
    today = datetime.date.today()
    alerts_data = []

    for _, r in df_all.iterrows():
        # 1. Cảnh báo hạn hợp đồng (trong vòng 60 ngày)
        if r['ngay_het_han_hd']:
            dt_hd = datetime.datetime.strptime(str(r['ngay_het_han_hd']), "%Y-%m-%d").date()
            days_left = (dt_hd - today).days
            if 0 <= days_left <= 60:
                alerts_data.append(("Hạn Hợp đồng", "danger", "1 người", f"{r['ho_ten']} ({r['phong_ban']})", f"Hết hạn HĐLĐ ({r['loai_hop_dong']})", f"Còn {days_left} ngày ({dt_hd.strftime('%d/%m/%Y')})"))

        # 2. Cảnh báo nâng lương
        if r['ngay_nang_luong']:
            dt_nl = datetime.datetime.strptime(str(r['ngay_nang_luong']), "%Y-%m-%d").date()
            if (dt_nl - today).days <= 30:
                alerts_data.append(("Nâng bậc lương", "warning", "1 người", f"{r['ho_ten']} ({r['phong_ban']})", f"Đến hạn xét nâng lương (Bậc hiện tại: {r['bac_luong']})", f"Hạn: {dt_nl.strftime('%d/%m/%Y')}"))

        # 3. Cảnh báo tiết CME (Dưới 48 tiết)
        if r['tiet_cme'] < 48 and r['chuyen_mon'] in ['Bác sĩ', 'Điều dưỡng', 'KTV']:
            alerts_data.append(("Cảnh báo CME", "danger", "1 người", f"{r['ho_ten']} ({r['phong_ban']})", f"Tích lũy đạt {r['tiet_cme']}/48 tiết CME", f"Thiếu {48 - r['tiet_cme']} tiết"))

        # 4. Cảnh báo hạn CCHN (trong vòng 60 ngày)
        if r['ngay_het_han_cchn']:
            dt_cchn = datetime.datetime.strptime(str(r['ngay_het_han_cchn']), "%Y-%m-%d").date()
            days_cchn = (dt_cchn - today).days
            if 0 <= days_cchn <= 60:
                alerts_data.append(("Giấy phép CCHN", "info", "1 người", f"{r['ho_ten']} ({r['phong_ban']})", "Đến hạn gia hạn CCHN 5 năm", f"Hạn nộp: {dt_cchn.strftime('%d/%m/%Y')}"))

    if alerts_data:
        rows_html = "".join([
            f'<tr style="border-bottom: 1px solid #e2e8f0;">'
            f'<td style="padding: 10px;"><span class="badge badge-{level}">{title}</span></td>'
            f'<td style="padding: 10px; text-align:center;"><span class="count-tag">{count}</span></td>'
            f'<td style="padding: 10px;"><b>{person}</b></td>'
            f'<td style="padding: 10px;">{detail}</td>'
            f'<td style="padding: 10px;">{status}</td>'
            f'</tr>'
            for title, level, count, person, detail, status in alerts_data
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
        """
        st.markdown(full_table_html, unsafe_allow_html=True)
    else:
        st.success("🎉 Hiện tại không có cảnh báo tồn đọng cần xử lý.")

# ------------------------------------------------------------------------------
# TRANG 2: CẬP NHẬT DỮ LIỆU TỪ EXCEL (MẪU 2C-BNV) LƯU CSDL VĨNH VIỄN
# ------------------------------------------------------------------------------
elif menu_selected == "Cập nhật danh sách (Excel 2C-BNV)":
    st.subheader("📥 Cập nhật danh sách người lao động từ File Excel Mẫu 2C-BNV")
    st.info("Vui lòng tải lên tập tin Excel chứa danh sách nhân sự để cập nhật vĩnh viễn vào hệ thống Database.")

    uploaded_file = st.file_uploader("Chọn file Excel (.xlsx, .xls)", type=["xlsx", "xls"])
    
    if uploaded_file:
        try:
            df_excel = pd.read_excel(uploaded_file)
            st.write("📋 **Xem trước 5 bản ghi đầu tiên trong file:**")
            st.dataframe(df_excel.head(), use_container_width=True)

            if st.button("🚀 Bắt đầu lưu dữ liệu vào CSDL SQLite", type="primary"):
                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                count_success = 0
                
                # Ánh xạ cột từ Excel vào CSDL (Hỗ trợ cấu trúc linh hoạt)
                for _, row in df_excel.iterrows():
                    ma_nv = str(row.get('Mã NV', f"NV{1000 + count_success}"))
                    ho_ten = str(row.get('Họ và tên', row.get('Họ tên', 'Chưa rõ')))
                    phong_ban = str(row.get('Phòng ban', 'Khoa Ngoại Tổng hợp'))
                    khoi = str(row.get('Khối', 'Lâm sàng'))
                    chuc_vu = str(row.get('Chức vụ', 'Nghiệp vụ'))
                    trinh_do = str(row.get('Trình độ', 'Đại học'))
                    chuyen_mon = str(row.get('Chuyên môn', 'Bác sĩ'))
                    loai_hd = str(row.get('Loại HĐ', 'Xác định thời hạn'))
                    ngay_hd = str(row.get('Ngày hết hạn HĐ', '2026-12-31'))
                    bac_luong = str(row.get('Bậc lương', '1/9'))
                    ngay_nl = str(row.get('Ngày nâng lương', '2027-01-01'))
                    tiet_cme = int(row.get('Tiết CME', 24))
                    cchn = str(row.get('Số CCHN', ''))
                    ngay_cchn = str(row.get('Ngày hết hạn CCHN', ''))
                    ngay_sinh = str(row.get('Ngày sinh', '1990-01-01'))
                    dang_vien = int(row.get('Đảng viên', 0))

                    cursor.execute("""
                        INSERT OR REPLACE INTO nhan_su 
                        (ma_nv, ho_ten, phong_ban, khoi, chuc_vu, trinh_do, chuyen_mon, loai_hop_dong, ngay_het_han_hd, bac_luong, ngay_nang_luong, tiet_cme, so_cchn, ngay_het_han_cchn, ngay_sinh, is_dang_vien)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (ma_nv, ho_ten, phong_ban, khoi, chuc_vu, trinh_do, chuyen_mon, loai_hd, ngay_hd, bac_luong, ngay_nl, tiet_cme, cchn, ngay_cchn, ngay_sinh, dang_vien))
                    count_success += 1

                conn.commit()
                conn.close()
                st.balloons()
                st.success(f"✅ Đã lưu vĩnh viễn {count_success} bản ghi vào Cơ sở dữ liệu thành công!")
        except Exception as e:
            st.error(f"Lỗi khi xử lý file Excel: {e}")

# ------------------------------------------------------------------------------
# TRANG 3: QUẢN LÝ DỮ LIỆU HỒ SƠ & THÊM/SỬA/XÓA NHÂN SỰ DIRECTLY
# ------------------------------------------------------------------------------
elif menu_selected == "Thông báo & Văn bản":
    st.subheader("📢 Thông báo Internal & Văn bản Điều hành")
    st.write("• **Thông báo số 128/TB-BVBD:** V/v Rà soát hồ sơ CCHN và đăng ký lịch học CME đợt 2.")
    st.write("• **Quyết định 45/QĐ-BV:** Ban hành quy chế đánh giá xếp loại lao động Bệnh viện Bưu điện.")

# Xử lý khi chọn từ Menu Hồ sơ Nhân sự
if menu_hoso == "Danh sách Hồ sơ Cán bộ CNV":
    st.subheader("🗂️ Quản lý Hồ sơ Cán bộ Công nhân viên toàn Bệnh viện")
    
    # Bảng xem & Lọc dữ liệu
    col_search, col_filter = st.columns([2, 1])
    with col_search:
        kw = st.text_input("🔍 Tìm kiếm theo Họ tên hoặc Mã NV:")
    with col_filter:
        phong_filter = st.selectbox("Lọc theo Phòng/Khoa:", ["Tất cả"] + list(df_all['phong_ban'].unique()))

    df_show = df_all.copy()
    if kw:
        df_show = df_show[df_show['ho_ten'].str.contains(kw, case=False) | df_show['ma_nv'].str.contains(kw, case=False)]
    if phong_filter != "Tất cả":
        df_show = df_show[df_show['phong_ban'] == phong_filter]

    st.dataframe(df_show, use_container_width=True)

    # Form thêm nhân sự trực tiếp vào Database
    with st.expander("➕ Thêm mới Hồ sơ Nhân sự vào CSDL"):
        with st.form("add_nv_form"):
            c1, c2, c3 = st.columns(3)
            with c1:
                new_ma = st.text_input("Mã Nhân viên (*)")
                new_ten = st.text_input("Họ và Tên (*)")
                new_phong = st.text_input("Phòng / Khoa", "Khoa Ngoại Tổng hợp")
            with c2:
                new_khoi = st.selectbox("Khối", ["Lâm sàng", "Cận lâm sàng", "Phòng ban"])
                new_chuyenmon = st.selectbox("Chuyên môn", ["Bác sĩ", "Điều dưỡng", "KTV", "Dược sĩ", "Khác"])
                new_trinhdo = st.selectbox("Trình độ", ["TS/CKII", "ThS/CKI", "Đại học", "Cao đẳng", "Khác"])
            with c3:
                new_hd = st.selectbox("Loại HĐ", ["Không xác định TH", "Xác định thời hạn"])
                new_ngay_hd = st.date_input("Hạn HĐLĐ", datetime.date(2027, 12, 31))
                new_is_dv = st.checkbox("Là Đảng viên")

            submit_btn = st.form_submit_button("Lưu Hồ Sơ")
            
            if submit_btn:
                if not new_ma or not new_ten:
                    st.error("Vui lòng điền đầy đủ Mã NV và Họ tên!")
                else:
                    conn = sqlite3.connect(DB_FILE)
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO nhan_su (ma_nv, ho_ten, phong_ban, khoi, chuyen_mon, trinh_do, loai_hop_dong, ngay_het_han_hd, is_dang_vien)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (new_ma, new_ten, new_phong, new_khoi, new_chuyenmon, new_trinhdo, new_hd, str(new_ngay_hd), 1 if new_is_dv else 0))
                    conn.commit()
                    conn.close()
                    st.success(f"✅ Đã thêm mới thành công cán bộ **{new_ten}**!")
                    st.rerun()
