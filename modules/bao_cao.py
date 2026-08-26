import streamlit as st
import pandas as pd
import io

def render_bao_cao(engine):
    st.title("📈 BÁO CÁO THỐNG KÊ QUẢN TRỊ NHÂN SỰ Y TẾ")
    st.caption("Báo cáo tuân thủ Bộ Y tế, Sở Y tế, BHXH & Ban Giám đốc")
    st.markdown("---")

    report_type = st.selectbox(
        "Mẫu báo cáo xuất dữ liệu",
        [
            "Báo cáo 01/SYT: Cơ cấu Nhân lực Y tế theo Trình độ & Khoa phòng",
            "Báo cáo 02/BHXH: Danh sách Nhân sự tham gia BHXH & Biến động",
            "Báo cáo 03/BYT: Thống kê Chứng chỉ hành nghề & Giờ CME tích lũy",
            "Báo cáo Quỹ lương & Phụ cấp ưu đãi nghề Y tế"
        ]
    )

    if engine and st.button("📊 Trích xuất Báo cáo"):
        try:
            df = pd.read_sql("SELECT * FROM nhan_su", engine)
            st.success(f"✅ Đã trích xuất thành công dữ liệu cho '{report_type}' ({len(df)} dòng dữ liệu)")
            st.dataframe(df.head(10), use_container_width=True)

            # Xuất File Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Bao_Cao', index=False)
            
            st.download_button(
                label="📥 Tải Báo cáo dạng Excel (.xlsx)",
                data=output.getvalue(),
                file_name=f"Bao_Cao_HRM.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"❌ Lỗi khi xuất báo cáo: {e}")
