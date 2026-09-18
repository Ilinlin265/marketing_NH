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

# Tùy chỉnh CSS giao diện Vietcombank (#005A36 - Xanh lá đậm)
st.markdown("""
    <style>
    :root {
        --vcb-primary: #005A36;
        --vcb-accent: #73C033;
        --vcb-bg: #F4F7F5;
    }
    
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
    
    .security-notice {
        background-color: #EFF6FF;
        border: 1px solid #BFDBFE;
        color: #1E40AF;
        padding: 12px 16px;
        border-radius: 8px;
        font-size: 13px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 2. HÀM BẢO MẬT & CHE MỜ DỮ LIỆU CÁ NHÂN (DATA MASKING)
# ----------------------------------------------------
def mask_phone(phone_str):
    """Che mờ Số điện thoại: 0912345678 -> 091*****78"""
    phone_str = str(phone_str).strip()
    if len(phone_str) >= 10:
        return phone_str[:3] + "*****" + phone_str[-2:]
    elif len(phone_str) >= 6:
        return phone_str[:2] + "*****" + phone_str[-2:]
    return "09xxxxx"

def mask_name(name_str):
    """Che mờ Họ tên: Nguyễn Văn A -> Nguyễn V*** A"""
    parts = str(name_str).strip().split()
    if len(parts) > 2:
        masked_middle = [p[0] + "*" * (len(p) - 1) if len(p) > 1 else "*" for p in parts[1:-1]]
        return f"{parts[0]} {' '.join(masked_middle)} {parts[-1]}"
    elif len(parts) == 2:
        return f"{parts[0]} {parts[1][0]}***"
    return name_str[0] + "***" if name_str else "Khách hàng"

# ----------------------------------------------------
# 3. KHỞI TẠO STATE
# ----------------------------------------------------
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

if 'show_full_pii' not in st.session_state:
    st.session_state.show_full_pii = False

if 'customer_df' not in st.session_state:
    columns = [
        "Họ và Tên", "Số Điện Thoại", "Gói Vay", "Số Tiền Vay (Triệu VNĐ)",
        "Thời Hạn (Tháng)", "Lãi Suất (%/năm)", "Thu Nhập Hàng Tháng (Triệu)",
        "Tỷ Lệ DTI (%)", "Nhóm Chiến Lược", "Trạng Thái", "Ngày Đăng Ký"
    ]
    st.session_state.customer_df = pd.DataFrame(columns=columns)

# ----------------------------------------------------
# 4. HÀM TỰ ĐỘNG PHÂN LOẠI NHÓM CHIẾN LƯỢC
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
# 5. SIDEBAR
# ----------------------------------------------------
with st.sidebar:
    try:
        st.image("LOGO.jpg", use_container_width=True)
    except Exception:
        st.markdown("### 🏦 VIETCOMBANK")
        
    st.markdown("---")
    
    menu = st.radio(
        "📌 DANH MỤC QUẢN LÝ",
        [
            "📊 Dashboard Tổng Quan",
            "🧮 Tính Vay & Đăng Ký Hồ Sơ",
            "🎯 Nhóm Chiến Lược Khách Hàng",
            "🔒 Cổng Quản Trị Viên (Admin)"
        ]
    )
    
    st.markdown("---")
    st.caption("🔒 Hệ thống bảo mật thông tin theo NĐ 13/2023/NĐ-CP")
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
        total_loan = (df["Số Tiền Vay (Triệu VNĐ)"].sum() / 1000) if not df.empty else 0.0
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Tổng Dư Nợ Đăng Ký</div>
                <div class="metric-value">{total_loan:.2f} Tỷ VNĐ</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        avg_rate = df["Lãi Suất (%/năm)"].mean() if not df.empty else 0.0
        avg_rate = 0.0 if np.isnan(avg_rate) else avg_rate
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Lãi Suất Bình Quân</div>
                <div class="metric-value">{avg_rate:.2f}% / năm</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        vip_count = len(df[df["Nhóm Chiến Lược"].str.contains("VIP", na=False)]) if not df.empty else 0
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
        if not df.empty:
            package_counts = df["Gói Vay"].value_counts().reset_index()
            package_counts.columns = ["Gói Vay", "Số Lượng"]
            st.bar_chart(package_counts, x="Gói Vay", y="Số Lượng", color="#005A36")
        else:
            st.info("💡 Chưa có dữ liệu khách hàng nào trong hệ thống.")

    with c2:
        st.markdown("##### 🎯 Cơ Cấu Nhóm Chiến Lược")
        if not df.empty:
            strat_counts = df["Nhóm Chiến Lược"].value_counts().reset_index()
            strat_counts.columns = ["Nhóm Chiến Lược", "Số Lượng"]
            st.dataframe(strat_counts, use_container_width=True, hide_index=True)
        else:
            st.info("💡 Chưa có dữ liệu khách hàng nào trong hệ thống.")

# ----------------------------------------------------
# MENU 2: TÍNH VAY & ĐĂNG KÝ HỒ SƠ
# ----------------------------------------------------
elif menu == "🧮 Tính Vay & Đăng Ký Hồ Sơ":
    st.subheader("🧮 Công Cụ Tính Gói Vay & Tạo Hồ Sơ Khách Hàng")
    
    st.markdown("""
        <div class="security-notice">
            🔒 <b>Cam kết bảo mật dữ liệu:</b> Thông tin cá nhân (Họ tên, SĐT) nhập vào đây được mã hóa và che mờ tự động để đảm bảo an toàn thông tin theo Nghị định 13/2023/NĐ-CP.
        </div>
    """, unsafe_allow_html=True)
    
    col_input, col_result = st.columns([1, 1])
    
    with col_input:
        st.markdown("##### 📝 Thông tin khoản vay")
        fullname = st.text_input("Họ và tên khách hàng", value="", placeholder="Ví dụ: Nguyễn Văn A")
        phone = st.text_input("Số điện thoại", value="", placeholder="Ví dụ: 0912345678")
        loan_type = st.selectbox("Chọn gói vay Vietcombank", [
            "Vay mua nhà",
            "Vay mua ô tô",
            "Vay tiêu dùng tín chấp",
            "Vay SXKD cá thể"
        ])
        
        amount_mb = st.number_input("Số tiền vay (Triệu VNĐ)", min_value=10, max_value=20000, value=1000, step=50)
        tenure_months = st.number_input("Thời hạn vay (Tháng)", min_value=6, max_value=360, value=120, step=6)
        interest_rate = st.number_input("Lãi suất ưu đãi (%/năm)", min_value=1.0, max_value=20.0, value=7.2, step=0.1)
        income = st.number_input("Thu nhập hàng tháng (Triệu VNĐ)", min_value=5, max_value=500, value=35, step=5)

        consent_privacy = st.checkbox("Khách hàng đã đồng ý điều khoản xử lý dữ liệu cá nhân theo quy định VCB.")

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
            if not fullname.strip() or not phone.strip():
                st.error("⚠️ Vui lòng nhập đầy đủ Họ tên và Số điện thoại khách hàng!")
            elif not consent_privacy:
                st.warning("⚠️ Vui lòng tích chọn xác nhận đồng ý điều khoản bảo mật dữ liệu cá nhân!")
            else:
                new_row = {
                    "Họ và Tên": fullname.strip(),
                    "Số Điện Thoại": phone.strip(),
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
                st.success(f"✅ Đã thêm hồ sơ an toàn cho khách hàng **{mask_name(fullname)}** (SĐT: {mask_phone(phone)})!")

# ----------------------------------------------------
# MENU 3: NHÓM CHIẾN LƯỢC KHÁCH HÀNG
# ----------------------------------------------------
elif menu == "🎯 Nhóm Chiến Lược Khách Hàng":
    st.subheader("🎯 Phân Loại & Định Hướng Nhóm Chiến Lược")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="strategy-card">
            <h4><span class="badge-vip">💎 NHÓM 1: KHÁCH HÀNG VIP / ƯU TIÊN</span></h4>
            <p><b>Tiêu chí:</b> Thu nhập ≥ 60 triệu hoặc khoản vay ≥ 2 Tỷ VNĐ.</p>
            <ul>
                <li><b>Chính sách Vietcombank:</b> Giảm thêm 0.5% - 0.8%/năm lãi suất.</li>
                <li><b>Chiến lược:</b> Phê duyệt luồng xanh trong 24h, cấp hạn mức Thẻ Tín Dụng Platinum.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="strategy-card">
            <h4><span class="badge-potential">🌟 NHÓM 2: TIỀM NĂNG TĂNG TRƯỜNG</span></h4>
            <p><b>Tiêu chí:</b> Thu nhập 30-60 triệu, gói vay mua nhà/xe chuẩn.</p>
            <ul>
                <li><b>Chính sách Vietcombank:</b> Lãi suất cạnh tranh, thời hạn vay dài lên đến 35 năm.</li>
                <li><b>Chiến lược:</b> Bán chéo bảo hiểm khoản vay (FWD), tài khoản số đẹp.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="strategy-card">
            <h4><span class="badge-standard">🌱 NHÓM 3: PHỔ THÔNG KHAI THÁC</span></h4>
            <p><b>Tiêu chí:</b> Khoản vay tiêu dùng, tín chấp nhỏ, thu nhập trung bình.</p>
            <ul>
                <li><b>Chính sách Vietcombank:</b> Quy trình xử lý tự động hóa qua VCB Digibank.</li>
                <li><b>Chiến lược:</b> Mở rộng quy mô, hướng dẫn thanh toán tự động.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="strategy-card">
            <h4><span class="badge-risk">⚠️ NHÓM 4: CẦN TĂNG CƯỜNG THẨM ĐỊNH</span></h4>
            <p><b>Tiêu chí:</b> DTI > 50% hoặc nguồn thu nhập từ hoạt động rủi ro.</p>
            <ul>
                <li><b>Chính sách Vietcombank:</b> Thẩm định thực tế nghiêm ngặt, định giá TSĐB sát thị trường.</li>
                <li><b>Chiến lược:</b> Quản lý rủi ro sát sao, yêu cầu thêm người đồng vay.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------------------------------
# MENU 4: CỔNG QUẢN TRỊ VIÊN (ADMIN - MẬT KHẨU: 123456)
# ----------------------------------------------------
elif menu == "🔒 Cổng Quản Trị Viên (Admin)":
    
    if not st.session_state.is_admin:
        st.markdown("<h3 style='text-align: center;'>🔒 ĐĂNG NHẬP CỔNG QUẢN TRỊ VIÊN VIETCOMBANK</h3>", unsafe_allow_html=True)
        
        col_m1, col_m2, col_m3 = st.columns([1, 2, 1])
        with col_m2:
            st.info("💡 Vui lòng nhập mật khẩu quản trị để mở khóa danh sách và thao tác dữ liệu.")
            input_pass = st.text_input("🔑 Mật khẩu Admin:", type="password", placeholder="Nhập mật khẩu...")
            
            if st.button("🔓 Đăng Nhập Quản Trị Viên", use_container_width=True):
                if input_pass == "123456":
                    st.session_state.is_admin = True
                    st.success("✅ Đăng nhập Admin thành công!")
                    st.rerun()
                else:
                    st.error("❌ Mật khẩu không chính xác! (Mật khẩu mặc định: 123456)")
                    
    else:
        top_col1, top_col2 = st.columns([3, 1])
        with top_col1:
            st.subheader("📑 Danh Sách Khách Hàng & Quyền Quản Trị Dữ Liệu")
        with top_col2:
            if st.button("🚪 Đăng Xuất Admin", use_container_width=True):
                st.session_state.is_admin = False
                st.session_state.show_full_pii = False
                st.rerun()

        st.success("🟢 Phiên làm việc: **Quản Trị Viên VIETCOMBANK**")

        # Nút chuyển đổi chế độ bảo mật hiển thị
        st.session_state.show_full_pii = st.toggle(
            "🔓 Giải mã & Hiển thị thông tin cá nhân đầy đủ (Họ tên & SĐT)", 
            value=st.session_state.show_full_pii
        )

        df = st.session_state.customer_df.copy()
        
        # Tạo bản sao hiển thị đã được Masking nếu chưa bật giải mã
        display_df = df.copy()
        if not display_df.empty and not st.session_state.show_full_pii:
            display_df["Họ và Tên"] = display_df["Họ và Tên"].apply(mask_name)
            display_df["Số Điện Thoại"] = display_df["Số Điện Thoại"].apply(mask_phone)
        
        # Bộ lọc dữ liệu
        st.markdown("##### 🔍 Bộ lọc tìm kiếm")
        f_col1, f_col2, f_col3 = st.columns(3)
        
        with f_col1:
            search_kw = st.text_input("Tìm kiếm nhanh (Từ khóa)")
        with f_col2:
            unique_strats = list(display_df["Nhóm Chiến Lược"].unique()) if not display_df.empty else []
            filter_strat = st.selectbox("Lọc theo Nhóm Chiến Lược", ["Tất cả"] + unique_strats)
        with f_col3:
            unique_status = list(display_df["Trạng Thái"].unique()) if not display_df.empty else []
            filter_status = st.selectbox("Lọc theo Trạng Thái", ["Tất cả"] + unique_status)
            
        # Áp dụng lọc
        if not display_df.empty:
            if search_kw:
                display_df = display_df[
                    display_df["Họ và Tên"].str.contains(search_kw, case=False, na=False) | 
                    display_df["Số Điện Thoại"].str.contains(search_kw, na=False)
                ]
            if filter_strat != "Tất cả":
                display_df = display_df[display_df["Nhóm Chiến Lược"] == filter_strat]
            if filter_status != "Tất cả":
                display_df = display_df[display_df["Trạng Thái"] == filter_status]
            
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        st.caption(f"Hiển thị {len(display_df)} trên tổng số {len(st.session_state.customer_df)} hồ sơ.")
        
        st.markdown("---")
        st.markdown("##### 🛠️ Thao Tác Xuất / Xóa Dữ Liệu Hồ Sơ")
        
        tab_action1, tab_action2 = st.columns(2)
        
        with tab_action1:
            st.write("📥 **Tải danh sách hồ sơ (Đã che mờ bảo mật theo chế độ hiện tại):**")
            
            # Export Excel
            output_excel = io.BytesIO()
            with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
                display_df.to_excel(writer, index=False, sheet_name='DS_KhachHang_VCB')
            excel_data = output_excel.getvalue()
            
            st.download_button(
                label="📊 Tải danh sách Excel (.xlsx)",
                data=excel_data,
                file_name=f"DS_KhachHang_Vay_VCB_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                disabled=display_df.empty
            )

            # Export CSV
            csv_data = display_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📄 Tải danh sách CSV (.csv)",
                data=csv_data,
                file_name=f"DS_KhachHang_Vay_VCB_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True,
                disabled=display_df.empty
            )

        with tab_action2:
            st.write("🗑️ **Xóa hồ sơ khách hàng:**")
            if not st.session_state.customer_df.empty:
                customer_names = st.session_state.customer_df["Họ và Tên"].tolist()
                selected_cust = st.selectbox("Chọn hồ sơ cần loại bỏ:", customer_names)
                
                if st.button("❌ Xác Nhận Xóa Hồ Sơ", use_container_width=True):
                    st.session_state.customer_df = st.session_state.customer_df[
                        st.session_state.customer_df["Họ và Tên"] != selected_cust
                    ].reset_index(drop=True)
                    st.success(f"✅ Đã loại bỏ hồ sơ khách hàng khỏi hệ thống!")
                    st.rerun()
            else:
                st.info("Chưa có dữ liệu nào để xóa.")
