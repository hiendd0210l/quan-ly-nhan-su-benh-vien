import streamlit as st
import pandas as pd
from sqlalchemy import text

def render_cau_hinh(engine):
    st.title("⚙️ Cấu hình Hệ thống & Quản trị")
    st.caption("Quản lý tham số hệ thống, phân quyền người dùng, danh mục y tế và cập nhật ảnh hồ sơ nhân sự")

    # Tạo các tab chức năng chính
    tab_user, tab_org, tab_cme, tab_avatar, tab_system = st.tabs([
        "👤 Người dùng & Phân quyền",
        "🏢 Danh mục Khoa / Phòng",
        "🩺 Tham số Y tế & CME",
        "🖼️ Cập nhật Ảnh nhân sự",
        "🛠️ Cấu hình Chấm công & BHXH"
    ])

    # ---------------------------------------------------------
    # TAB 1: QUẢN LÝ NGƯỜI DÙNG & PHÂN QUYỀN
    # ---------------------------------------------------------
    with tab_user:
        st.subheader("📋 Danh sách Tài khoản & Phân quyền")
        
        # Form thêm người dùng mới
        with st.expander("➕ Thêm tài khoản người dùng mới", expanded=False):
            with st.form("form_add_user"):
                col1, col2 = st.columns(2)
                with col1:
                    new_username = st.text_input("Tên đăng nhập (*):")
                    new_fullname = st.text_input("Họ và tên người dùng (*):")
                    new_password = st.text_input("Mật khẩu (*):", type="password")
                with col2:
                    new_role = st.selectbox("Vai trò / Quyền hạn (*):", [
                        "Admin (Quản trị hệ thống)",
                        "Ban Giám đốc",
                        "Trưởng Khoa / Phòng",
                        "Chuyên viên HR",
                        "Nhân viên Y tế"
                    ])
                    new_department = st.text_input("Khoa / Phòng công tác:")
                    
                submit_user = st.form_submit_button("💾 Lưu tài khoản")
                if submit_user:
                    if new_username and new_password:
                        st.success(f"✅ Đã tạo thành công tài khoản **{new_username}** ({new_role})!")
                    else:
                        st.warning("⚠️ Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu!")

        # Bảng danh sách người dùng mẫu
        users_data = [
            {"ID": 1, "Tên đăng nhập": "admin", "Họ tên": "Quản trị viên", "Vai trò": "Admin", "Khoa/Phòng": "CNTT", "Trạng thái": "Hoạt động"},
            {"ID": 2, "Tên đăng nhập": "bgd_truong", "Họ tên": "Trần Văn A", "Vai trò": "Ban Giám đốc", "Khoa/Phòng": "Ban Giám đốc", "Trạng thái": "Hoạt động"},
            {"ID": 3, "Tên đăng nhập": "hr_lan", "Họ tên": "Nguyễn Thị Lan", "Vai trò": "Chuyên viên HR", "Khoa/Phòng": "Tổ chức Cán bộ", "Trạng thái": "Hoạt động"},
            {"ID": 4, "Tên đăng nhập": "bs_hung", "Họ tên": "Lê Văn Hùng", "Vai trò": "Nhân viên Y tế", "Khoa/Phòng": "Khoa Cấp cứu", "Trạng thái": "Hoạt động"}
        ]
        st.dataframe(pd.DataFrame(users_data), use_container_width=True, hide_index=True)

    # ---------------------------------------------------------
    # TAB 2: DANH MỤC KHOA / PHÒNG
    # ---------------------------------------------------------
    with tab_org:
        st.subheader("🏢 Quản lý Cơ cấu Tổ chức Khoa / Phòng / Trung tâm")
        
        col_list, col_add = st.columns([2, 1])
        with col_list:
            depts_data = [
                {"Mã đơn vị": "K01", "Tên Khoa/Phòng": "Khoa Cấp cứu", "Loại": "Lâm sàng", "Số nhân sự": 32},
                {"Mã đơn vị": "K02", "Tên Khoa/Phòng": "Khoa Ngoại Tổng hợp", "Loại": "Lâm sàng", "Số nhân sự": 45},
                {"Mã đơn vị": "P01", "Tên Khoa/Phòng": "Phòng Tổ chức Cán bộ", "Loại": "Phòng chức năng", "Số nhân sự": 12},
                {"Mã đơn vị": "P02", "Tên Khoa/Phòng": "Phòng Tài chính Kế toán", "Loại": "Phòng chức năng", "Số nhân sự": 15},
            ]
            st.dataframe(pd.DataFrame(depts_data), use_container_width=True, hide_index=True)
            
        with col_add:
            st.markdown("**➕ Thêm Khoa/Phòng mới**")
            with st.form("form_add_dept"):
                dept_code = st.text_input("Mã đơn vị:")
                dept_name = st.text_input("Tên Khoa / Phòng:")
                dept_type = st.selectbox("Phân loại:", ["Lâm sàng", "Cận lâm sàng", "Phòng chức năng", "Trung tâm"])
                if st.form_submit_button("➕ Thêm đơn vị"):
                    st.success(f"✅ Đã thêm **{dept_name}** vào hệ thống!")

    # ---------------------------------------------------------
    # TAB 3: THAM SỐ Y TẾ & QUY ĐỊNH CME
    # ---------------------------------------------------------
    with tab_cme:
        st.subheader("🩺 Quy định Giấy phép hành nghề & Đào tạo CME")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("##### 📜 Định mức giờ CME bắt buộc (Hàng năm)")
            cme_bs = st.number_input("Bác sĩ / Dược sĩ đại học (Tiết/năm):", value=24)
            cme_dd = st.number_input("Điều dưỡng / Kỹ thuật viên (Tiết/năm):", value=12)
            cme_alert = st.number_input("Cảnh báo trước khi thiếu chỉ tiêu (Ngày):", value=60)
            
        with c2:
            st.markdown("##### 🪪 Cấu hình cảnh báo Hạn GPHN")
            gphn_alert_days = st.number_input("Cảnh báo GPHN sắp hết hạn (Ngày):", value=90)
            st.checkbox("Tự động gửi Email cảnh báo tới Nhân sự", value=True)
            st.checkbox("Hiển thị thông báo trên Dashboard khi đăng nhập", value=True)
            
        if st.button("💾 Lưu tham số Y tế & CME"):
            st.success("✅ Đã cập nhật cấu hình tham số CME & GPHN thành công!")

    # ---------------------------------------------------------
    # TAB 4: CẬP NHẬT ẢNH HỒ SƠ NHÂN SỰ
    # ---------------------------------------------------------
    with tab_avatar:
        st.subheader("🖼️ Quản lý & Cập nhật Ảnh Hồ sơ Nhân sự")
        st.info("Tìm kiếm nhân viên và tải lên ảnh chân dung chuẩn để lưu vào hồ sơ.")

        # Tìm kiếm nhân viên
        col_search, col_upload = st.columns([1.2, 2])
        
        with col_search:
            st.markdown("**1. Chọn Nhân sự**")
            search_emp = st.text_input("🔍 Nhập Mã NV hoặc Họ tên:", placeholder="VD: NV001 hoặc Lê Văn Hùng")
            
            # Giả lập chọn nhân viên
            emp_selected = st.selectbox("Chọn nhân sự từ danh sách:", [
                "NV001 - Nguyễn Văn An (Khoa Cấp cứu)",
                "NV002 - Trần Thị Mai (Phòng TCCB)",
                "NV003 - Lê Hoàng Nam (Khoa Ngoại)"
            ])
            
            # Hiển thị ảnh hiện tại
            st.markdown("**Ảnh hiện tại:**")
            st.image("https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=200&auto=format&fit=crop", width=160, caption="Ảnh hồ sơ hiện tại")

        with col_upload:
            st.markdown("**2. Tải lên Ảnh mới**")
            uploaded_file = st.file_uploader("Chọn file ảnh (PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"])
            
            if uploaded_file is not None:
                st.markdown("**Xem trước ảnh mới:**")
                st.image(uploaded_file, width=180, caption="Ảnh xem trước")
                
                if st.button("💾 Cập nhật Ảnh Hồ sơ", type="primary"):
                    st.success(f"✅ Đã cập nhật ảnh hồ sơ thành công cho **{emp_selected}**!")

    # ---------------------------------------------------------
    # TAB 5: CẤU HÌNH CHẤM CÔNG & BHXH
    # ---------------------------------------------------------
    with tab_system:
        st.subheader("🛠️ Cấu hình Tham số Chấm công & Bảo hiểm")
        
        col_cc, col_bh = st.columns(2)
        with col_cc:
            st.markdown("##### ⏰ Tham số Chấm công")
            st.time_input("Giờ vào ca sáng:", value=pd.to_datetime("07:30").time())
            st.time_input("Giờ ra ca chiều:", value=pd.to_datetime("16:30").time())
            st.number_input("Số công chuẩn trong tháng (Ngày):", value=22)
            
        with col_bh:
            st.markdown("##### 🏥 Tham số Bảo hiểm (BHXH, BHYT, BHTN)")
            st.number_input("Mức lương cơ sở (VNĐ):", value=2340000, step=100000)
            st.number_input("Tỷ lệ đóng BHXH Doanh nghiệp (%):", value=17.5)
            st.number_input("Tỷ lệ đóng BHXH Người lao động (%):", value=8.0)

        if st.button("💾 Lưu Cấu hình Chấm công & BHXH"):
            st.success("✅ Đã cập nhật cài đặt Chấm công & BHXH!")
