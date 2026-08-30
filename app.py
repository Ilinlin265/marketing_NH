```python
import streamlit as st
import pandas as pd
from io import BytesIO


# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Customer Management",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.image("logo.jpg")

# =========================================================
# CSS - GIAO DIỆN SANG TRỌNG
# =========================================================

st.markdown("""
<style>

    /* =========================
       FONT & BACKGROUND
    ========================= */

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            linear-gradient(
                135deg,
                #f8fafc 0%,
                #eef3f8 50%,
                #f8fafc 100%
            );
    }


    /* =========================
       SIDEBAR
    ========================= */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #071d35 0%,
                #0b2d4f 55%,
                #09233e 100%
            );
        border-right: 1px solid #d6b36a;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    section[data-testid="stSidebar"] .stRadio label {
        background: rgba(255,255,255,0.06);
        border-radius: 10px;
        padding: 10px 14px;
        margin-bottom: 8px;
        transition: 0.2s;
    }

    section[data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(214,179,106,0.20);
    }


    /* =========================
       LOGO
    ========================= */

    .logo-box {
        text-align: center;
        padding: 8px 0 18px 0;
    }

    .logo-box img {
        max-height: 75px;
        width: auto;
    }


    /* =========================
       HEADER
    ========================= */

    .main-header {
        background: white;
        padding: 28px 32px;
        border-radius: 18px;
        margin-bottom: 24px;
        border: 1px solid #e3e8ee;
        box-shadow: 0 8px 25px rgba(7,29,53,0.06);
    }

    .main-header h1 {
        color: #08233f;
        font-size: 30px;
        font-weight: 700;
        margin: 0;
        letter-spacing: 0.3px;
    }

    .main-header p {
        color: #718096;
        margin: 8px 0 0 0;
        font-size: 14px;
    }


    /* =========================
       CARD
    ========================= */

    .card {
        background: white;
        padding: 28px;
        border-radius: 18px;
        border: 1px solid #e4e9ef;
        box-shadow: 0 8px 25px rgba(7,29,53,0.06);
        margin-bottom: 22px;
    }

    .card-title {
        color: #08233f;
        font-size: 19px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .card-subtitle {
        color: #7b8794;
        font-size: 13px;
        margin-bottom: 20px;
    }


    /* =========================
       INPUT
    ========================= */

    .stTextInput label,
    .stTextArea label {
        color: #243b53 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    .stTextInput input,
    .stTextArea textarea {
        border: 1px solid #d8e0e8 !important;
        border-radius: 10px !important;
        background-color: #fbfcfd !important;
        padding: 11px 14px !important;
        transition: all 0.2s ease;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: #b99752 !important;
        box-shadow: 0 0 0 2px rgba(185,151,82,0.12) !important;
    }


    /* =========================
       BUTTON
    ========================= */

    .stButton button,
    .stDownloadButton button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        min-height: 44px;
        transition: all 0.2s ease;
    }

    .stButton button[kind="primary"] {
        background:
            linear-gradient(
                135deg,
                #0b3156,
                #08233f
            ) !important;
        border: 1px solid #0b3156 !important;
    }

    .stButton button[kind="primary"]:hover {
        background:
            linear-gradient(
                135deg,
                #123f68,
                #0b2d4f
            ) !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 15px rgba(8,35,63,0.20);
    }


    /* =========================
       METRIC
    ========================= */

    div[data-testid="stMetric"] {
        background: white;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 6px 20px rgba(7,29,53,0.05);
    }

    div[data-testid="stMetricLabel"] {
        color: #718096 !important;
        font-weight: 500 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #08233f !important;
        font-weight: 700 !important;
    }


    /* =========================
       DATAFRAME
    ========================= */

    div[data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid #dfe6ed;
    }


    /* =========================
       ALERT
    ========================= */

    .stAlert {
        border-radius: 12px !important;
    }


    /* =========================
       FOOTER
    ========================= */

    .footer {
        text-align: center;
        color: #8a96a3;
        font-size: 12px;
        margin-top: 35px;
        padding: 20px;
    }

    .gold-line {
        height: 2px;
        background: linear-gradient(
            90deg,
            transparent,
            #d6b36a,
            transparent
        );
        margin: 10px 0 25px 0;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOGO
# =========================================================

st.image("LOGO.jpg", width=180)

st.markdown("""
<div style="text-align:center; margin-top:-10px;">
    <div style="
        color:#08233f;
        font-size:15px;
        font-weight:600;
        letter-spacing:2px;
    ">
        CUSTOMER MANAGEMENT SYSTEM
    </div>

    <div style="
        width:120px;
        height:2px;
        background:#d6b36a;
        margin:10px auto 25px auto;
    ">
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# KHỞI TẠO DANH SÁCH KHÁCH HÀNG
# =========================================================

if "customers" not in st.session_state:
    st.session_state.customers = []


# =========================================================
# HÀM XUẤT EXCEL
# =========================================================

def export_excel():

    df = pd.DataFrame(
        st.session_state.customers
    )

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Khách hàng"
        )

    return output.getvalue()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("""
    <div style="
        text-align:center;
        padding:10px 0 20px 0;
    ">
        <div style="
            font-size:22px;
            font-weight:700;
            letter-spacing:1px;
        ">
            QUẢN LÝ
        </div>

        <div style="
            color:#d6b36a;
            font-size:13px;
            letter-spacing:2px;
        ">
            KHÁCH HÀNG
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div style="height:1px;background:#d6b36a;margin-bottom:20px;"></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        "### 📋 MENU"
    )

    page = st.radio(
        "Chọn chức năng",
        [
            "👤 Nhập khách hàng",
            "🔐 Admin"
        ],
        label_visibility="collapsed"
    )

    st.markdown("""
    <div style="
        position:fixed;
        bottom:25px;
        left:25px;
        right:25px;
        text-align:center;
        color:#b8c4d0;
        font-size:11px;
    ">
        CUSTOMER MANAGEMENT<br>
        <span style="color:#d6b36a;">●</span>
        Secure Internal System
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# TRANG NHẬP KHÁCH HÀNG
# =========================================================

if page == "👤 Nhập khách hàng":

    st.markdown("""
    <div class="main-header">
        <h1>👤 Thông tin khách hàng</h1>
        <p>
            Vui lòng nhập đầy đủ thông tin để lưu hồ sơ khách hàng vào hệ thống.
        </p>
    </div>
    """, unsafe_allow_html=True)


    # -----------------------------------------------------
    # FORM
    # -----------------------------------------------------

    st.markdown("""
    <div class="card">
        <div class="card-title">
            📄 Hồ sơ khách hàng
        </div>

        <div class="card-subtitle">
            Các trường có thông tin bắt buộc cần được nhập đầy đủ.
        </div>
    """, unsafe_allow_html=True)


    col1, col2 = st.columns(2)

    with col1:

        phone = st.text_input(
            "📱 Số điện thoại *",
            placeholder="Ví dụ: 0901234567"
        )

    with col2:

        name = st.text_input(
            "👤 Tên khách hàng *",
            placeholder="Nhập họ và tên khách hàng"
        )


    col3, col4 = st.columns(2)

    with col3:

        address = st.text_input(
            "📍 Địa chỉ",
            placeholder="Nhập địa chỉ khách hàng"
        )

    with col4:

        note = st.text_area(
            "📝 Ghi chú",
            placeholder="Nhập thông tin cần lưu ý...",
            height=100
        )


    st.markdown("</div>", unsafe_allow_html=True)


    # -----------------------------------------------------
    # NÚT LƯU
    # -----------------------------------------------------

    st.markdown("""
    <div style="margin-top:10px;"></div>
    """, unsafe_allow_html=True)


    if st.button(
        "💾  LƯU THÔNG TIN KHÁCH HÀNG",
        type="primary",
        use_container_width=True
    ):

        if phone.strip() == "":

            st.error(
                "❌ Vui lòng nhập số điện thoại."
            )

        elif name.strip() == "":

            st.error(
                "❌ Vui lòng nhập tên khách hàng."
            )

        else:

            customer = {
                "Số điện thoại": phone.strip(),
                "Tên khách hàng": name.strip(),
                "Địa chỉ": address.strip(),
                "Ghi chú": note.strip()
            }

            st.session_state.customers.append(
                customer
            )

            st.success(
                "✅ Đã lưu thông tin khách hàng thành công!"
            )

            st.balloons()


    # -----------------------------------------------------
    # THỐNG KÊ NHANH
    # -----------------------------------------------------

    st.markdown(
        '<div class="gold-line"></div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "👥 Khách hàng đã lưu",
            len(st.session_state.customers)
        )

    with col2:

        st.metric(
            "🔐 Trạng thái",
            "Đang hoạt động"
        )

    with col3:

        st.metric(
            "📊 Hệ thống",
            "Online"
        )


# =========================================================
# TRANG ADMIN
# =========================================================

elif page == "🔐 Admin":

    st.markdown("""
    <div class="main-header">
        <h1>🔐 Khu vực quản trị</h1>
        <p>
            Quản lý, kiểm tra và xuất dữ liệu khách hàng.
        </p>
    </div>
    """, unsafe_allow_html=True)


    # =====================================================
    # KHỞI TẠO TRẠNG THÁI ĐĂNG NHẬP
    # =====================================================

    if "admin_logged_in" not in st.session_state:

        st.session_state.admin_logged_in = False


    # =====================================================
    # CHƯA ĐĂNG NHẬP
    # =====================================================

    if not st.session_state.admin_logged_in:

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:

            st.markdown("""
            <div class="card">

                <div style="
                    text-align:center;
                    font-size:45px;
                    margin-bottom:10px;
                ">
                    🔐
                </div>

                <div style="
                    text-align:center;
                    color:#08233f;
                    font-size:22px;
                    font-weight:700;
                ">
                    ADMIN LOGIN
                </div>

                <div style="
                    text-align:center;
                    color:#7b8794;
                    font-size:13px;
                    margin:8px 0 25px 0;
                ">
                    Đăng nhập để truy cập dữ liệu khách hàng
                </div>
            """, unsafe_allow_html=True)


            password = st.text_input(
                "🔑 Mật khẩu",
                type="password",
                placeholder="Nhập mật khẩu quản trị"
            )


            if st.button(
                "🔓 ĐĂNG NHẬP HỆ THỐNG",
                type="primary",
                use_container_width=True
            ):

                if password == "123456":

                    st.session_state.admin_logged_in = True

                    st.success(
                        "Đăng nhập thành công."
                    )

                    st.rerun()

                else:

                    st.error(
                        "❌ Mật khẩu không chính xác."
                    )


            st.markdown("""
            </div>
            """, unsafe_allow_html=True)


    # =====================================================
    # ADMIN ĐÃ ĐĂNG NHẬP
    # =====================================================

    else:

        col1, col2 = st.columns([6, 1])

        with col1:

            st.markdown("""
            <div style="
                color:#08233f;
                font-size:20px;
                font-weight:700;
                margin-bottom:10px;
            ">
                📊 Dashboard khách hàng
            </div>
            """, unsafe_allow_html=True)

        with col2:

            if st.button(
                "🚪 Đăng xuất",
                use_container_width=True
            ):

                st.session_state.admin_logged_in = False

                st.rerun()


        # =================================================
        # DASHBOARD
        # =================================================

        total = len(
            st.session_state.customers
        )


        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "👥 Tổng khách hàng",
                total
            )

        with col2:

            st.metric(
                "📁 Hồ sơ",
                total
            )

        with col3:

            st.metric(
                "🟢 Trạng thái hệ thống",
                "Hoạt động"
            )


        st.markdown(
            '<div class="gold-line"></div>',
            unsafe_allow_html=True
        )


        # =================================================
        # KIỂM TRA DỮ LIỆU
        # =================================================

        if total == 0:

            st.markdown("""
            <div class="card" style="text-align:center;">

                <div style="font-size:45px;">
                    📭
                </div>

                <div style="
                    color:#08233f;
                    font-size:20px;
                    font-weight:700;
                    margin-top:10px;
                ">
                    Chưa có dữ liệu khách hàng
                </div>

                <div style="
                    color:#7b8794;
                    margin-top:5px;
                ">
                    Hãy nhập thông tin khách hàng để dữ liệu xuất hiện tại đây.
                </div>

            </div>
            """, unsafe_allow_html=True)


        else:

            # =============================================
            # DATAFRAME
            # =============================================

            df = pd.DataFrame(
                st.session_state.customers
            )


            st.markdown("""
            <div class="card">

                <div class="card-title">
                    👥 Danh sách khách hàng
                </div>

                <div class="card-subtitle">
                    Dữ liệu khách hàng được lưu trong phiên làm việc hiện tại.
                </div>
            """, unsafe_allow_html=True)


            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                height=420
            )


            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


            # =============================================
            # XUẤT EXCEL
            # =============================================

            st.markdown("""
            <div class="card">

                <div class="card-title">
                    📥 Xuất dữ liệu
                </div>

                <div class="card-subtitle">
                    Tải toàn bộ danh sách khách hàng dưới dạng Excel.
                </div>
            """, unsafe_allow_html=True)


            excel_file = export_excel()


            st.download_button(
                label="📥  XUẤT DANH SÁCH KHÁCH HÀNG EXCEL",
                data=excel_file,
                file_name="danh_sach_khach_hang.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                ),
                use_container_width=True
            )


            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    <div class="gold-line"></div>
    © 2026 Customer Management System
    <br>
    Secure • Professional • Reliable
</div>
""", unsafe_allow_html=True)
```
