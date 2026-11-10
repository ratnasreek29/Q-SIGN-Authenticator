
import streamlit as st

from software.config import MATCH_THRESHOLD
from software.authentication.fingerprint_matching import (
    load_reference_fingerprints,
)
from software.authentication.product_authentication import (
    authenticate_reading,
)
from software.database.product_registry import (
    load_product_registry,
)
from software.database.history import save_history


# ============================================================
# USER DASHBOARD STYLING
# ============================================================

def apply_user_styles():
    st.markdown("""
<style>
.qs-user-hero {
    background: linear-gradient(120deg, #142137, #101827);
    border: 1px solid #293A54;
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 26px;
}

.qs-user-label {
    color: #4DE3D1;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
}

.qs-user-title {
    color: #F1F7FF;
    font-size: clamp(30px, 4vw, 46px);
    font-weight: 800;
    margin: 12px 0;
}

.qs-user-description {
    color: #A5B7CC;
    font-size: 15px;
    line-height: 1.7;
}

.qs-section {
    color: #F1F7FF;
    font-size: 20px;
    font-weight: 700;
    margin: 18px 0 12px;
}

.qs-result {
    padding: 24px;
    border-radius: 16px;
    margin-top: 20px;
    margin-bottom: 18px;
}

.qs-match {
    background: #102B2E;
    border: 1px solid #23665F;
}

.qs-mismatch {
    background: #302024;
    border: 1px solid #8B4753;
}

.qs-result-title {
    font-size: 22px;
    font-weight: 800;
    margin-bottom: 10px;
}

.qs-result-desc {
    color: #C5D4E4;
    font-size: 14px;
    line-height: 1.7;
}

.qs-result-success {
    color: #4DE3D1;
}

.qs-result-danger {
    color: #FF8999;
}

.qs-note {
    color: #8EA6BE;
    font-size: 13px;
    line-height: 1.7;
    margin-top: 18px;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# USER VERIFICATION DASHBOARD
# ============================================================

def show_user_verification():

    apply_user_styles()

    # Dashboard header
    st.markdown("""
<div class="qs-user-hero">
<div class="qs-user-label">Q-SIGN / USER PORTAL</div>
<div class="qs-user-title">Optical Product Verification</div>
<div class="qs-user-description">
Compare a simulated RGB sensor reading against the
registered optical fingerprint associated with a product.
</div>
</div>
""", unsafe_allow_html=True)

    # Load existing registered data
    products = load_product_registry()
    references = load_reference_fingerprints()

    if not products:
        st.warning(
            "No products have been registered yet. "
            "Please ask an administrator to register a product."
        )
        return

    # Product information
    st.markdown("""
<div class="qs-section">01 / Product Identity</div>
""", unsafe_allow_html=True)

    product_id = st.text_input(
        "Product ID",
        placeholder="Example: PROD001",
        help="Enter the identifier of a registered product.",
    ).strip().upper()

    st.divider()

    # RGB sensor input
    st.markdown("""
<div class="qs-section">02 / Optical Sensor Reading</div>
""", unsafe_allow_html=True)

    st.caption(
        "Enter simulated RGB values from 0 to 255. "
        "Green and Blue must be greater than zero "
        "for the current ratio-based fingerprint calculation."
    )

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.markdown(
            "<span style='color:#FF8999;font-weight:700;'>"
            "RED CHANNEL</span>",
            unsafe_allow_html=True,
        )
        red = st.number_input(
            "Red (R)",
            min_value=0,
            max_value=255,
            value=100,
            key="user_red",
        )

    with col2:
        st.markdown(
            "<span style='color:#4DE3D1;font-weight:700;'>"
            "GREEN CHANNEL</span>",
            unsafe_allow_html=True,
        )
        green = st.number_input(
            "Green (G)",
            min_value=1,
            max_value=255,
            value=120,
            key="user_green",
        )

    with col3:
        st.markdown(
            "<span style='color:#819BFF;font-weight:700;'>"
            "BLUE CHANNEL</span>",
            unsafe_allow_html=True,
        )
        blue = st.number_input(
            "Blue (B)",
            min_value=1,
            max_value=255,
            value=110,
            key="user_blue",
        )

    st.divider()

    # Verification action
    st.markdown("""
<div class="qs-section">03 / Verify Optical Signature</div>
""", unsafe_allow_html=True)

    submitted = st.button(
        "◉  Verify Product Fingerprint",
        type="primary",
        use_container_width=True,
    )

    if submitted:

        if not product_id:
            st.error("Please enter a Product ID.")
            return

        # Existing authentication algorithm
        try:
            expected_tag, distance, possible_match = (
                authenticate_reading(
                    product_id=product_id,
                    rgb_reading=(
                        int(red),
                        int(green),
                        int(blue),
                    ),
                    products=products,
                    references=references,
                )
            )

        except KeyError:
            st.error(
                "Product ID not found, or its registered "
                "optical fingerprint is unavailable."
            )
            return

        except ValueError as error:
            st.error(str(error))
            return

        # Existing SQLite history logging
        try:
            save_history(
                source="User Verification",
                product_id=product_id,
                tag_id=expected_tag,
                rgb=(int(red), int(green), int(blue)),
                distance=distance,
                threshold=MATCH_THRESHOLD,
                possible_match=possible_match,
            )

        except Exception:
            st.warning(
                "Verification completed, but the result "
                "could not be saved to System History."
            )

        st.divider()

        st.markdown("""
<div class="qs-section">04 / Verification Result</div>
""", unsafe_allow_html=True)

        # Match or mismatch panel
        if possible_match:

            st.markdown("""
<div class="qs-result qs-match">
<div class="qs-result-title qs-result-success">
✓ POSSIBLE MATCH
</div>
<div class="qs-result-desc">
The simulated optical fingerprint is consistent
with the registered reference signature.
</div>
</div>
""", unsafe_allow_html=True)

        else:

            st.markdown("""
<div class="qs-result qs-mismatch">
<div class="qs-result-title qs-result-danger">
✕ FINGERPRINT MISMATCH
</div>
<div class="qs-result-desc">
The measured optical fingerprint differs from
the registered reference signature.
</div>
</div>
""", unsafe_allow_html=True)

        # Verification metrics
        metric_col1, metric_col2 = st.columns(2)

        with metric_col1:
            st.metric(
                "Fingerprint Distance",
                f"{distance:.4f}",
            )

        with metric_col2:
            st.metric(
                "Matching Threshold",
                f"{MATCH_THRESHOLD:.4f}",
            )

        # Product details
        st.markdown("#### Verification Details")

        st.write("**Product ID:**", product_id)
        st.write("**Registered Optical Tag:**", expected_tag)

        st.markdown("""
<div class="qs-note">
Research prototype: This verification compares
simulated optical readings against stored references.
A possible match does not independently establish
that a physical product is genuine.
</div>
""", unsafe_allow_html=True)
