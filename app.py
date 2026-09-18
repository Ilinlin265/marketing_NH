import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime, date

# ----------------------------------------------------
# 1. CẤU HÌNH TRANG & GIAO DIỆN CHUẨN VIETCOMBANK
# ----------------------------------------------------
st.set_page_config(
    page_title="Vietcombank - Quản Lý & Phân Tích Gói Vay Cá Nhân",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tùy chỉnh CSS giao diện theo tông màu Vietcombank (#005A36 - Xanh lá đậm, #73C033 - Xanh lá tươi)
st.markdown("""
    <style>
    :root {
        --vcb-primary: #005A36;
        --vcb-accent: #73C033;
        --vcb-bg: #F4F7F5;
    }
    
    /* Style Tiêu đề chính */
    .vcb-header {
        background: linear-gradient(135deg, #005A36 0%, #003B22 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0, 90, 54, 0.2);
    }
    .vcb-header h1 {
        color: #FFFFFF !important;
        font-weight: 700;
        margin: 0;
        font-size: 26px;
    }
    .vcb-header p {
        color: #E0F2E9;
        margin-top: 6px;
        margin-bottom: 0;
        font-size: 14px;
    }
    
    /* Metric Cards */
    .metric-card {
        background-color: white;
        padding: 18px;
        border-radius: 10px;
        border-left: 5px solid #005A36;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        text-align: center;
    }
    .metric-title {
        font-size: 13px;
        color: #64748B;
        text-transform: uppercase;
        font-weight: 600;
    }
    .metric-value {
        font-size: 22px;
        font-weight: bold;
        color: #005A36;
        margin-top: 5px;
    }

    /* Style Thẻ Nhóm Chiến Lược */
    .strategy-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .badge-vip { background-color: #FEF3C7; color: #92400E; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }
    .badge-potential { background-color: #E0E7FF; color: #3730A3; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }
    .badge-standard { background-color: #D1FAE5; color: #065F46; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }
    .badge-risk { background-color: #FEE2E2; color: #991B1B; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 2. KHỞI TẠO DỮ LIỆU MẪU (SESSION STATE)
# ----------------------------------------------------
if 'customer_df' not in st.session_state:
    sample_data = [
        {
            "Họ và Tên": "Nguyễn Văn An", "Số Điện Thoại": "0903123456",
            "Gói Vay": "Vay mua nhà (An Cư)", "Số Tiền Vay (Triệu VNĐ)": 2500, "Thời Hạn (Tháng)": 240,
            "Lãi Suất (%/năm)": 6.8, "Thu Nhập Hàng Tháng (Triệu)": 65, "Tỷ Lệ DTI (%)": 38.5,
            "Nhóm Chiến Lược": "💎 VIP - Khách hàng Ưu tiên", "Trạng Thái": "Đã phê duyệt", "Ngày Đăng Ký": "2026-09-01"
        },
        {
            "Họ và Tên": "Trần Thị Bích", "Số Điện Thoại": "0918234567",
            "Gói Vay": "Vay mua ô tô", "Số Tiền Vay (Triệu VNĐ)": 600, "Thời Hạn (Tháng)": 60,
            "Lãi Suất (%/năm)": 7.5, "Thu Nhập Hàng Tháng (Triệu)": 35, "Tỷ Lệ DTI (%)": 42.0,
            "Nhóm Chiến Lược": "🌟 Tiềm Năng Tăng Trưởng", "Trạng Thái": "Đang thẩm định", "Ngày Đăng Ký": "2026-09-05"
        },
        {
            "Họ và Tên": "Lê Hoàng Cường", "Số Điện Thoại": "0989345678",
            "Gói Vay": "Vay tiêu dùng tín chấp", "Số Tiền Vay (Triệu VNĐ)": 150, "Thời Hạn (Tháng)": 36,
            "Lãi Suất (%/năm)": 10.5, "Thu Nhập Hàng Tháng (Triệu)": 22, "Tỷ Lệ DTI (%)": 32.1,
            "Nhóm Chiến Lược": "🌱 Phổ Thông Khai Thác", "Trạng Thái": "Đã phê duyệt", "Ngày Đăng Ký": "2026-09-10"
        },
        {
            "Họ và Tên": "Phạm Quốc Dũng", "Số Điện Thoại": "0977456789",
            "Gói Vay": "Vay SXKD cá thể", "Số Tiền Vay (Triệu VNĐ)": 1200, "Thời Hạn (Tháng)": 84,
            "Lãi Suất (%/năm)": 8.0, "Thu Nhập Hàng Tháng (Triệu)": 40, "Tỷ Lệ DTI (%)": 58.2,
            "Nhóm Chiến Lược": "⚠️ Cần Tăng Cường Thẩm Định", "Trạng Thái": "Yêu cầu bổ sung HS", "Ngày Đăng Ký": "2026-09-12"
        },
        {
            "Họ và Tên": "Đặng Mai Phương", "Số Điện Thoại": "0934567890",
            "Gói Vay": "Vay mua nhà (An Cư)", "Số Tiền Vay (Triệu VNĐ)": 4000, "Thời Hạn (Tháng)": 180,
            "Lãi Suất (%/năm)": 6.5, "Thu Nhập Hàng Tháng (Triệu)": 110, "Tỷ Lệ DTI (%)": 29.5,
            "Nhóm Chiến Lược": "💎 VIP - Khách hàng Ưu tiên", "Trạng Thái": "Đã phê duyệt", "Ngày Đăng Ký": "2026-09-15"
        }
    ]
    st.session_state.customer_df = pd.DataFrame(sample_data)

# ----------------------------------------------------
# 3. HÀM TỰ ĐỘNG PHÂN LOẠI NHÓM CHIẾN LƯỢC
# ----------------------------------------------------
def classify_strategic_group(income, loan_amount, dti):
    if income >= 60 and loan_amount >= 2000:
        return "💎 VIP - Khách hàng Ưu tiên"
    elif income >= 30 or loan_amount >= 500:
        if dti > 50:
            return "⚠️ Cần Tăng Cường Thẩm Định"
        return "🌟 Tiềm Năng Tăng Trưởng"
    elif dti > 50:
        return "⚠️ Cần Tăng Cường Thẩm Định"
    else:
        return "🌱 Phổ Thông Khai Thác"

# ----------------------------------------------------
# 4. SIDEBAR (LOGO & ĐIỀU HƯỚNG)
# ----------------------------------------------------
with st.sidebar:
    try:
        st.image("LOGO.JPG", use_container_width=True)
    except Exception:
        st.error("⚠️ Không tìm thấy file LOGO.JPG")
        st.markdown("### 🏦 VIETCOMBANK")
        
    st.markdown("---")
    
    menu = st.radio(
        "📌 DANH MỤC QUẢN LÝ",
        [
            "📊 Dashboard Tổng Quan",
            "🧮 Tính Vay & Đăng Ký Hồ Sơ",
            "🎯 Nhóm Chiến Lược Khách Hàng",
            "📑 Danh Sách & Xuất File KH"
        ]
    )
    
    st.markdown("---")
    st.caption("🟢 Hệ thống quản trị gói vay cá nhân VCB v2.5")
    st.caption("© Ngân hàng TMCP Ngoại thương Việt Nam")

# ----------------------------------------------------
# HEADER BẢN QUYỀN
# ----------------------------------------------------
st.markdown("""
    <div class="vcb-header">
        <h1>NGÂN HÀNG TMCP NGOẠI THƯƠNG VIỆT NAM - VIETCOMBANK</h1>
        <p>Hệ Thống Phân Tích, Phân Loại Nhóm Chiến Lược & Quản Lý Khách Hàng Vay Cá Nhân</p>
    </div>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# MENU 1: DASHBOARD TỔNG QUAN
# ----------------------------------------------------
if menu == "📊 Dashboard Tổng Quan":
    st.subheader("📊 Báo Cáo Tổng Quan Dư Nợ & Khách Hàng")
    df = st.session_state.customer_df

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Tổng Khách Hàng</div>
                <div class="metric-value">{len(df)} KH</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        total_loan = df["Số Tiền Vay (Triệu VNĐ)"].sum() / 1000
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Tổng Dư Nợ Đăng Ký</div>
                <div class="metric-value">{total_loan:.2f} Tỷ VNĐ</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        avg_rate = df["Lãi Suất (%/năm)"].mean()
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Lãi Suất Bình Quân</div>
                <div class="metric-value">{avg_rate:.2f}% / năm</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        vip_count = len(df[df["Nhóm Chiến Lược"].str.contains("VIP")])
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Khách Hàng VIP</div>
                <div class="metric-value">{vip_count} KH</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("##### 📌 Phân Bố Theo Gói Vay Cá Nhân")
        package_counts = df["Gói Vay"].value_counts().reset_index()
        package_counts.columns = ["Gói Vay", "Số Lượng"]
        st.bar_chart(package_counts, x="Gói Vay", y="Số Lượng", color="#005A36")

    with c2:
        st.markdown("##### 🎯 Cơ Cấu Nhóm Chiến Lược")
        strat_counts = df["Nhóm Chiến Lược"].value_counts().reset_index()
        strat_counts.columns = ["Nhóm Chiến Lược", "Số Lượng"]
        st.dataframe(strat_counts, use_container_width=True, hide_index=True)

# ----------------------------------------------------
# MENU 2: TÍNH VAY & ĐĂNG KÝ HỒ SƠ
# ----------------------------------------------------
elif menu == "🧮 Tính Vay & Đăng Ký Hồ Sơ":
    st.subheader("🧮 Công Cụ Tính Gói Vay & Tạo Hồ Sơ Khách Hàng")
    
    col_input, col_result = st.columns([1, 1])
    
    with col_input:
        st.markdown("##### 📝 Thông tin khoản vay")
        fullname = st.text_input("Họ và tên khách hàng", "Nguyễn Văn Trọng")
        phone = st.text_input("Số điện thoại", "0912345678")
        loan_type = st.selectbox("Chọn gói vay Vietcombank", [
            "Vay mua nhà (An Cư Vietcombank)",
            "Vay mua ô tô",
            "Vay tiêu dùng tín chấp",
            "Vay SXKD cá thể"
        ])
        
        amount_mb = st.number_input("Số tiền vay (Triệu VNĐ)", min_value=10, max_value=20000, value=1500, step=50)
        tenure_months = st.number_input("Thời hạn vay (Tháng)", min_value=6, max_value=360, value=120, step=6)
        interest_rate = st.number_input("Lãi suất ưu đãi (%/năm)", min_value=1.0, max_value=20.0, value=7.2, step=0.1)
        income = st.number_input("Thu nhập hàng tháng (Triệu VNĐ)", min_value=5, max_value=500, value=45, step=5)

    # Tính toán khoản vay
    monthly_rate = (interest_rate / 100) / 12
    principal_per_month = amount_mb / tenure_months
    first_month_interest = amount_mb * monthly_rate
    first_month_total = principal_per_month + first_month_interest
    dti_ratio = (first_month_total / income) * 100 if income > 0 else 0
    
    strat_group = classify_strategic_group(income, amount_mb, dti_ratio)

    with col_result:
        st.markdown("##### 📊 Kết quả tính toán & Đánh giá chiến lược")
        st.info(f"**Số tiền trả tháng đầu tiên:** `{first_month_total:,.2f} Triệu VNĐ`")
        st.write(f"- **Tiền gốc hàng tháng:** {principal_per_month:,.2f} Triệu VNĐ")
        st.write(f"- **Tiền lãi tháng đầu:** {first_month_interest:,.2f} Triệu VNĐ")
        st.write(f"- **Tỷ lệ DTI (Nợ / Thu nhập):** `{dti_ratio:.1f}%`")
        
        st.markdown("---")
        st.markdown("**🎯 Phân loại Nhóm Chiến Lược Tự Động:**")
        st.success(f"**{strat_group}**")
        
        if dti_ratio > 50:
            st.warning("⚠️ Cảnh báo: Tỷ lệ DTI vượt quá 50%. Cần xem xét thêm tài sản bảo đảm!")
            
        if st.button("➕ Thêm Hồ Sơ Vào Danh Sách Khách Hàng", use_container_width=True):
            new_row = {
                "Họ và Tên": fullname,
                "Số Điện Thoại": phone,
                "Gói Vay": loan_type,
                "Số Tiền Vay (Triệu VNĐ)": amount_mb,
                "Thời Hạn (Tháng)": tenure_months,
                "Lãi Suất (%/năm)": interest_rate,
                "Thu Nhập Hàng Tháng (Triệu)": income,
                "Tỷ Lệ DTI (%)": round(dti_ratio, 1),
                "Nhóm Chiến Lược": strat_group,
                "Trạng Thái": "Đang thẩm định",
                "Ngày Đăng Ký": date.today().strftime("%Y-%m-%d")
            }
            st.session_state.customer_df = pd.concat([st.session_state.customer_df, pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"✅ Đã thêm hồ sơ thành công cho khách hàng **{fullname}**!")

# ----------------------------------------------------
# MENU 3: NHÓM CHIẾN LƯỢC KHÁCH HÀNG
# ----------------------------------------------------
elif menu == "🎯 Nhóm Chiến Lược Khách Hàng":
    st.subheader("🎯 Phân Loại & Định Hướng Nhóm Chiến Lược")
    
    st.markdown("""
    Mô hình phân loại chiến lược dựa trên quy mô vay, năng lực tài chính và mức độ rủi ro nhằm tối ưu hóa chính sách ưu đãi của **Vietcombank**:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="strategy-card">
            <h4><span class="badge-vip">💎 NHÓM 1: KHÁCH HÀNG VIP / ƯU TIÊN</span></h4>
            <p><b>Tiêu chí:</b> Thu nhập ≥ 60 triệu hoặc khoản vay ≥ 2 Tỷ VNĐ.</p>
            <ul>
                <li><b>Chính sách Vietcombank:</b> Giảm thêm 0.5% - 0.8%/năm lãi suất.</li>
                <li><b>Chiến lược:</b> Phê duyệt luồng xanh trong 24h, cấp hạn mức Thẻ Tín Dụng Platinum, phát triển dịch vụ ngân hàng ưu tiên (VCB Priority).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="strategy-card">
            <h4><span class="badge-potential">🌟 NHÓM 2: TIỀM NĂNG TĂNG TRƯỞNG</span></h4>
            <p><b>Tiêu chí:</b> Thu nhập 30-60 triệu, gói vay mua nhà/xe chuẩn.</p>
            <ul>
                <li><b>Chính sách Vietcombank:</b> Lãi suất cạnh tranh, thời hạn vay dài lên đến 35 năm.</li>
                <li><b>Chiến lược:</b> Bán chéo bảo hiểm khoản vay (FWD), tài khoản số đẹp, gói gửi tiết kiệm tích lũy.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="strategy-card">
            <h4><span class="badge-standard">🌱 NHÓM 3: PHỔ THÔNG KHAI THÁC</span></h4>
            <p><b>Tiêu chí:</b> Khoản vay tiêu dùng, tín chấp nhỏ, thu nhập trung bình.</p>
            <ul>
                <li><b>Chính sách Vietcombank:</b> Quy trình xử lý tự động hóa qua ứng dụng VCB Digibank.</li>
                <li><b>Chiến lược:</b> Mở rộng quy mô, hướng dẫn thanh toán tự động, thu hút dòng tiền trả lương.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="strategy-card">
            <h4><span class="badge-risk">⚠️ NHÓM 4: CẦN TĂNG CƯỜNG THẨM ĐỊNH</span></h4>
            <p><b>Tiêu chí:</b> DTI > 50% hoặc nguồn thu nhập từ hoạt động rủi ro.</p>
            <ul>
                <li><b>Chính sách Vietcombank:</b> Thẩm định thực tế nghiêm ngặt, định giá TSĐB sát thị trường.</li>
                <li><b>Chiến lược:</b> Quản lý rủi ro sát sao, yêu cầu thêm người đồng vay hoặc TSĐB bổ sung.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------------------------------
# MENU 4: DANH SÁCH & XUẤT FILE KHÁCH HÀNG
# ----------------------------------------------------
elif menu == "📑 Danh Sách & Xuất File KH":
    st.subheader("📑 Danh Sách Khách Hàng Vay Cá Nhân & Xuất Dữ Liệu")
    
    df = st.session_state.customer_df.copy()
    
    # Bộ lọc dữ liệu
    st.markdown("##### 🔍 Bộ lọc tìm kiếm")
    f_col1, f_col2, f_col3 = st.columns(3)
    
    with f_col1:
        search_kw = st.text_input("Tìm theo Họ tên / Số điện thoại")
    with f_col2:
        filter_strat = st.selectbox("Lọc theo Nhóm Chiến Lược", ["Tất cả"] + list(df["Nhóm Chiến Lược"].unique()))
    with f_col3:
        filter_status = st.selectbox("Lọc theo Trạng Thái", ["Tất cả"] + list(df["Trạng Thái"].unique()))
        
    # Áp dụng bộ lọc
    if search_kw:
        df = df[df["Họ và Tên"].str.contains(search_kw, case=False) | df["Số Điện Thoại"].str.contains(search_kw)]
    if filter_strat != "Tất cả":
        df = df[df["Nhóm Chiến Lược"] == filter_strat]
    if filter_status != "Tất cả":
        df = df[df["Trạng Thái"] == filter_status]
        
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.caption(f"Hiển thị {len(df)} trên tổng số {len(st.session_state.customer_df)} khách hàng.")
    
    st.markdown("---")
    st.markdown("##### 📥 Xuất danh sách khách hàng ra File")
    
    exp_col1, exp_col2 = st.columns(2)
    
    # Xuất file Excel (.xlsx)
    with exp_col1:
        output_excel = io.BytesIO()
        with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='DS_KhachHang_VCB')
        excel_data = output_excel.getvalue()
        
        st.download_button(
            label="📊 Tải file Danh sách Khách hàng (Excel .xlsx)",
            data=excel_data,
            file_name=f"DS_KhachHang_Vay_VCB_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    # Xuất file CSV (UTF-8)
    with exp_col2:
        csv_data = df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📄 Tải file Danh sách Khách hàng (CSV .csv)",
            data=csv_data,
            file_name=f"DS_KhachHang_Vay_VCB_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
