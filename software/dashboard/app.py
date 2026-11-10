
import sys
from pathlib import Path
import hmac
import streamlit as st

# Make the Q-SIGN project root accessible to Python
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from software.dashboard.admin.overview import show_overview
from software.dashboard.admin.registration import show_registration
from software.dashboard.admin.fingerprints import show_fingerprint_explorer
from software.dashboard.admin.simulation import show_simulation_lab
from software.dashboard.admin.history import show_system_history
from software.dashboard.user.verification import show_user_verification


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Q-SIGN Authentication",
    page_icon="🔐",
    layout="wide",
)


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "login"

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

if "admin_section" not in st.session_state:
    st.session_state.admin_section = "Overview"


# ============================================================
# QUANTUM NOIR + OPTICAL SPECTRUM THEME
# ============================================================

st.markdown("""
<style>

/* Main application */

.stApp {
    background-color: #080D18 !important;
    color: #E9F3FF !important;
}

h1, h2, h3 {
    color: #E9F3FF !important;
}

/* Global buttons */

div.stButton > button {
    border-radius: 10px;
    transition: all 0.25s ease;
}

div.stButton > button:hover {
    border-color: #4DE3D1;
}


/* ============================================================
   WELCOME SCREEN
   ============================================================ */

.qsign-hero {
    text-align: center;
    padding: 38px 20px 15px;
}

.qsign-eyebrow {
    color: #4DE3D1;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 3px;
    margin-bottom: 18px;
}

.qsign-title {
    color: #F1F7FF;
    font-size: clamp(52px, 7vw, 88px);
    font-weight: 800;
    letter-spacing: 5px;
    line-height: 1.15;
    margin: 0;
}

.qsign-gradient {
    background: linear-gradient(
        90deg,
        #4DE3D1,
        #7285FF,
        #C079F9
    );

    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}

.qsign-tagline {
    color: #F1F7FF;
    font-size: 24px;
    font-weight: 600;
    margin-top: 18px;
}

.qsign-subtitle {
    color: #A5B7CC;
    font-size: 16px;
    line-height: 1.8;
    max-width: 650px;
    margin: 12px auto 0;
}


/* Optical spectrum */

.qsign-spectrum {
    height: 3px;
    max-width: 500px;
    margin: 25px auto 15px;
    border-radius: 20px;

    background: linear-gradient(
        90deg,
        transparent,
        #4DE3D1,
        #7285FF,
        #C079F9,
        transparent
    );

    box-shadow: 0 0 25px #7285FF55;
}


/* Optical animation */

.qsign-optical {
    max-width: 620px;
    height: 145px;
    margin: 10px auto 30px;
    position: relative;
    overflow: hidden;
    border-radius: 18px;

    background: radial-gradient(
        ellipse at center,
        #142137 0%,
        #080D18 75%
    );
}

.qsign-optical::before {
    content: "";
    position: absolute;
    inset: 0;

    background: repeating-linear-gradient(
        90deg,
        transparent 0px,
        transparent 18px,
        #4DE3D120 19px,
        transparent 20px
    );
}

.qsign-optical::after {
    content: "";
    position: absolute;

    width: 140px;
    height: 140px;
    left: calc(50% - 70px);
    top: 2px;

    border: 1px solid #4DE3D1;
    border-radius: 50%;

    box-shadow:
        0 0 25px #4DE3D130,
        inset 0 0 25px #7285FF20;

    animation: qsign-pulse 3s ease-in-out infinite;
}

.qsign-optical-core {
    position: absolute;

    width: 16px;
    height: 16px;
    left: calc(50% - 8px);
    top: 64px;

    border-radius: 50%;
    background: #4DE3D1;
    box-shadow: 0 0 22px #4DE3D1;

    animation: qsign-pulse 3s ease-in-out infinite;
}

@keyframes qsign-pulse {
    0%, 100% {
        opacity: 0.45;
        transform: scale(0.94);
    }

    50% {
        opacity: 1;
        transform: scale(1.05);
    }
}


/* Portal cards */

.qsign-card {
    background: linear-gradient(
        145deg,
        #142137,
        #101827
    );

    border: 1px solid #293A54;
    border-radius: 18px;
    padding: 30px;
    min-height: 210px;
    margin-bottom: 12px;

    transition: all 0.25s ease;
}

.qsign-card:hover {
    border-color: #4DE3D1;
    box-shadow: 0 0 25px #4DE3D115;
}

.qsign-card-icon {
    font-size: 30px;
    margin-bottom: 18px;
}

.qsign-card-title {
    color: #F1F7FF;
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 12px;
}

.qsign-card-desc {
    color: #A5B7CC;
    font-size: 14px;
    line-height: 1.7;
}


/* Footer */

.qsign-footer {
    text-align: center;
    color: #71869F;
    font-size: 12px;
    letter-spacing: 1px;
    padding: 35px 10px 20px;
}


/* ============================================================
   NEW ADMIN SIDEBAR
   ============================================================ */

/* Sidebar background */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #101A2C 0%,
        #080D18 100%
    ) !important;

    border-right: 1px solid #263A50;
}

section[data-testid="stSidebar"]
[data-testid="stSidebarUserContent"] {
    padding-top: 24px;
}


/* Q-SIGN branding panel */

.qs-side-brand {
    background: linear-gradient(
        135deg,
        #14283A,
        #141A32
    );

    border: 1px solid #29435B;
    border-radius: 16px;
    padding: 18px 15px;
    margin: 5px 0 24px;
}

.qs-side-logo {
    color: #F1F7FF;
    font-size: 26px;
    font-weight: 800;
    letter-spacing: 2px;
}

.qs-side-logo span {
    color: #4DE3D1;
}

.qs-side-subtitle {
    color: #94A9C1;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.6px;
    margin-top: 4px;
}

.qs-side-online {
    color: #4DE3D1;
    font-size: 12px;
    margin-top: 18px;
}


/* Workspace label */

.qs-side-heading {
    color: #829AB6;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    margin: 8px 0 10px;
}


/* Navigation buttons */

section[data-testid="stSidebar"]
div.stButton > button {
    width: 100%;
    text-align: left;
    justify-content: flex-start;

    min-height: 46px;
    border-radius: 11px;
    margin: 2px 0;

    background: #111E31;
    color: #DCE8F6;

    border: 1px solid #26364B;
    font-weight: 500;
    box-shadow: none;
}


/* Navigation hover */

section[data-testid="stSidebar"]
div.stButton > button:hover {
    background: #1A3044;
    color: #4DE3D1;
    border-color: #398D92;
}


/* Active navigation button */

section[data-testid="stSidebar"]
div.stButton > button[kind="primary"] {
    background: linear-gradient(
        90deg,
        #173E49,
        #1B2A46
    );

    color: #4DE3D1;
    border: 1px solid #348B91;

    box-shadow:
        inset 3px 0 0 #4DE3D1,
        0 0 16px #4DE3D110;

    font-weight: 700;
}


/* Admin profile */

.qs-side-profile {
    border-top: 1px solid #293A54;
    margin-top: 25px;
    padding-top: 17px;

    color: #DCE8F6;
    font-size: 13px;
}

.qs-side-profile small {
    color: #8DA5BF;
    font-size: 11px;
}


/* Sidebar footer */

.qs-side-footer {
    color: #637C99;
    text-align: center;
    font-size: 10px;
    letter-spacing: 1px;
    margin-top: 20px;
}


/* Reduced motion accessibility */

@media (prefers-reduced-motion: reduce) {
    .qsign-optical::after,
    .qsign-optical-core {
        animation: none;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOGOUT
# ============================================================

def logout():

    st.session_state.is_admin = False
    st.session_state.page = "login"

    st.session_state.pop(
        "admin_code_input",
        None,
    )

    st.session_state.pop(
        "admin_section",
        None,
    )


# ============================================================
# WELCOME SCREEN
# ============================================================

def login_page():

    # Hero section

    st.markdown("""
<div class="qsign-hero">
<div class="qsign-eyebrow">QUANTUM-DOT OPTICAL AUTHENTICATION</div>
<div class="qsign-title">Q-<span class="qsign-gradient">SIGN</span></div>
<div class="qsign-tagline">Every product has a signature.</div>
<div class="qsign-subtitle">
Explore the science of optical fingerprinting through intelligent product verification.
</div>
<div class="qsign-spectrum"></div>
</div>
""", unsafe_allow_html=True)

    # Animated optical fingerprint

    st.markdown("""
<div class="qsign-optical">
<div class="qsign-optical-core"></div>
</div>
""", unsafe_allow_html=True)

    # Portal selection

    st.markdown("""
<h3 style="text-align:center;color:#F1F7FF;">
Choose Your Portal
</h3>
""", unsafe_allow_html=True)

    st.write("")

    user_col, admin_col = st.columns(
        2,
        gap="large",
    )

    # --------------------------------------------------------
    # USER PORTAL CARD
    # --------------------------------------------------------

    with user_col:

        st.markdown("""
<div class="qsign-card">
<div class="qsign-card-icon" style="color:#4DE3D1;">
◉
</div>
<div class="qsign-card-title">
User Portal
</div>
<div class="qsign-card-desc">
Verify registered products using simulated
RGB optical readings and compare their
signatures against stored references.
</div>
</div>
""", unsafe_allow_html=True)

        if st.button(
            "Enter User Portal",
            use_container_width=True,
            type="primary",
        ):

            st.session_state.is_admin = False
            st.session_state.page = "user"

            st.rerun()

    # --------------------------------------------------------
    # ADMIN PORTAL CARD
    # --------------------------------------------------------

    with admin_col:

        st.markdown("""
<div class="qsign-card">
<div class="qsign-card-icon" style="color:#C079F9;">
◈
</div>
<div class="qsign-card-title">
Admin Portal
</div>
<div class="qsign-card-desc">
Manage optical tags, register products,
explore fingerprints, run simulations
and monitor verification history.
</div>
</div>
""", unsafe_allow_html=True)

        if st.button(
            "Enter Admin Portal",
            use_container_width=True,
        ):

            st.session_state.page = "admin_login"
            st.rerun()

    # Footer

    st.markdown("""
<div class="qsign-footer">
Q-SIGN AUTHENTICATOR
&nbsp; • &nbsp;
SOFTWARE PROTOTYPE
&nbsp; • &nbsp;
OPTICAL FINGERPRINTING
</div>
""", unsafe_allow_html=True)


# ============================================================
# ADMIN LOGIN
# ============================================================

def admin_login_page():

    st.title("Admin Access")

    st.write(
        "Enter the secret code to continue."
    )

    with st.form("admin_login_form"):

        entered_code = st.text_input(
            "Admin Secret Code",
            type="password",
        )

        submitted = st.form_submit_button(
            "Unlock Admin Dashboard",
            use_container_width=True,
        )

    if submitted:

        try:

            correct_code = st.secrets[
                "ADMIN_CODE"
            ]

        except (KeyError, FileNotFoundError):

            st.error(
                "Admin configuration is missing."
            )

            return

        if hmac.compare_digest(
            entered_code,
            correct_code,
        ):

            st.session_state.is_admin = True
            st.session_state.page = "admin"

            st.rerun()

        else:

            st.error(
                "Incorrect secret code. Access denied."
            )

    if st.button("Back to Welcome"):

        logout()
        st.rerun()


# ============================================================
# ADMIN DASHBOARD
# ============================================================

def admin_dashboard():

    # Check admin authentication

    if not st.session_state.is_admin:

        st.error("Unauthorized access.")

        logout()
        st.rerun()

    # --------------------------------------------------------
    # ADMIN NAVIGATION PAGES
    # --------------------------------------------------------

    pages = {
        "Overview": "▦  Overview",
        "Registration": "⊞  Registration",
        "Fingerprint Explorer": "◉  Fingerprint Explorer",
        "Simulation Lab": "◇  Simulation Lab",
        "System History": "◷  System History",
    }

    # Remember selected section across reruns

    if (
        st.session_state.get("admin_section")
        not in pages
    ):

        st.session_state.admin_section = "Overview"

    # --------------------------------------------------------
    # CUSTOM ADMIN SIDEBAR
    # --------------------------------------------------------

    with st.sidebar:

        # Q-SIGN branding

        st.markdown("""
<div class="qs-side-brand">
<div class="qs-side-logo">
Q-<span>SIGN</span>
</div>
<div class="qs-side-subtitle">
ADMIN CONTROL CENTER
</div>
<div class="qs-side-online">
● &nbsp; System Online
</div>
</div>
<div class="qs-side-heading">
WORKSPACE
</div>
""", unsafe_allow_html=True)

        # Navigation buttons

        for page_name, label in pages.items():

            active = (
                st.session_state.admin_section
                == page_name
            )

            if st.button(
                label,
                key=f"admin_nav_{page_name}",
                type=(
                    "primary"
                    if active
                    else "secondary"
                ),
                use_container_width=True,
            ):

                st.session_state.admin_section = (
                    page_name
                )

                st.rerun()

        # Administrator profile

        st.markdown("""
<div class="qs-side-profile">
🔐 &nbsp; <strong>Administrator</strong>
<div>
<small>Authorized admin session</small>
</div>
</div>
""", unsafe_allow_html=True)

        # Logout button

        if st.button(
            "↪  Logout",
            key="admin_sidebar_logout",
            use_container_width=True,
        ):

            logout()
            st.rerun()

        # Sidebar footer

        st.markdown("""
<div class="qs-side-footer">
Q-SIGN • OPTICAL AUTHENTICATION
</div>
""", unsafe_allow_html=True)

    # --------------------------------------------------------
    # ADMIN PAGE ROUTING
    # --------------------------------------------------------

    selected_page = (
        st.session_state.admin_section
    )

    if selected_page == "Overview":

        show_overview()

    elif selected_page == "Registration":

        show_registration()

    elif selected_page == "Fingerprint Explorer":

        show_fingerprint_explorer()

    elif selected_page == "Simulation Lab":

        show_simulation_lab()

    elif selected_page == "System History":

        show_system_history()


# ============================================================
# USER DASHBOARD
# ============================================================

def user_dashboard():

    show_user_verification()

    st.divider()

    if st.button("Back to Welcome"):

        logout()
        st.rerun()


# ============================================================
# APPLICATION NAVIGATION
# ============================================================

if st.session_state.page == "login":

    login_page()

elif st.session_state.page == "admin_login":

    admin_login_page()

elif st.session_state.page == "admin":

    admin_dashboard()

elif st.session_state.page == "user":

    user_dashboard()

else:

    logout()
    st.rerun()
