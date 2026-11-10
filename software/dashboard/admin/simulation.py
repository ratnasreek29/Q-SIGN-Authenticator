
import html

import pandas as pd
import streamlit as st

from software.database.history import save_history

from software.config import (
    MATCH_THRESHOLD,
    FINGERPRINTS_FILE,
)

from software.processing.preprocessing import (
    extract_rgb_features,
)

from software.authentication.fingerprint_matching import (
    load_reference_fingerprints,
    calculate_distance,
)


# ============================================================
# FEATURE DEFINITIONS
# ============================================================

FEATURE_NAMES = ["R/G", "B/G", "R/B"]

FEATURE_COLORS = [
    "#FF8999",
    "#4DE3D1",
    "#819BFF",
]


# ============================================================
# ADMIN ACCESS
# ============================================================

def require_admin():
    if not st.session_state.get("is_admin", False):
        st.error("Admin access required.")
        st.stop()


# ============================================================
# QUANTUM NOIR STYLING
# ============================================================

def apply_simulation_styles():

    st.markdown("""
<style>

.qs-sim-hero {
    background: linear-gradient(120deg, #142137, #101827);
    border: 1px solid #293A54;
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 25px;
}

.qs-sim-eyebrow {
    color: #4DE3D1;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
}

.qs-sim-title {
    color: #F1F7FF;
    font-size: clamp(30px, 4vw, 46px);
    font-weight: 800;
    margin: 12px 0;
}

.qs-sim-description {
    color: #A5B7CC;
    font-size: 15px;
    line-height: 1.7;
}

.qs-sim-section {
    color: #F1F7FF;
    font-size: 21px;
    font-weight: 700;
    margin: 25px 0 12px;
}

.qs-sim-subtitle {
    color: #91A9C1;
    font-size: 13px;
    line-height: 1.7;
    margin-bottom: 18px;
}

.qs-sim-card {
    background: linear-gradient(145deg, #142137, #101827);
    border: 1px solid #293A54;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 14px;
}

.qs-sim-card-label {
    color: #9CB2C8;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
}

.qs-sim-card-value {
    color: #F1F7FF;
    font-size: 28px;
    font-weight: 800;
    margin-top: 9px;
}

.qs-sim-feature {
    background: #142137;
    border: 1px solid #293A54;
    border-radius: 14px;
    padding: 18px;
    text-align: center;
}

.qs-sim-feature-label {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
}

.qs-sim-feature-value {
    color: #F1F7FF;
    font-size: 27px;
    font-weight: 800;
    margin-top: 9px;
}

.qs-sim-info {
    background: #102B2E;
    border: 1px solid #23665F;
    border-radius: 14px;
    padding: 18px 20px;
    margin: 15px 0;
    color: #C5D4E4;
    font-size: 13px;
    line-height: 1.7;
}

.qs-sim-result {
    background: linear-gradient(120deg, #14283A, #171E35);
    border: 1px solid #38516A;
    border-radius: 18px;
    padding: 25px;
    text-align: center;
    margin: 18px 0;
}

.qs-sim-result-label {
    color: #A5B7CC;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
}

.qs-sim-result-value {
    font-size: 32px;
    font-weight: 800;
    margin-top: 12px;
}

.qs-sim-rgb-preview {
    width: 74px;
    height: 74px;
    border-radius: 15px;
    border: 2px solid #52647A;
    margin: 12px 0;
}

.qs-sim-note {
    color: #8EA6BE;
    font-size: 13px;
    line-height: 1.7;
    margin-top: 15px;
}

div[data-testid="stForm"] {
    background: linear-gradient(145deg, #121F32, #101827);
    border: 1px solid #293A54;
    border-radius: 16px;
    padding: 22px;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #293A54;
    border-radius: 12px;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# REUSABLE COMPONENTS
# ============================================================

def section_heading(number, title, description=""):

    safe_number = html.escape(str(number))
    safe_title = html.escape(str(title))
    safe_description = html.escape(str(description))

    st.markdown(
        f"""
<div class="qs-sim-section">
<span style="color:#4DE3D1;">{safe_number} /</span>
{safe_title}
</div>
<div class="qs-sim-subtitle">
{safe_description}
</div>
""",
        unsafe_allow_html=True,
    )


def stat_card(label, value, color="#4DE3D1"):

    safe_label = html.escape(str(label))
    safe_value = html.escape(str(value))

    st.markdown(
        f"""
<div class="qs-sim-card">
<div class="qs-sim-card-label">{safe_label}</div>
<div class="qs-sim-card-value" style="color:{color};">
{safe_value}
</div>
</div>
""",
        unsafe_allow_html=True,
    )


def feature_card(name, value, color):

    st.markdown(
        f"""
<div class="qs-sim-feature">
<div class="qs-sim-feature-label" style="color:{color};">
{html.escape(str(name))}
</div>
<div class="qs-sim-feature-value">
{float(value):.4f}
</div>
</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# SIMULATION LAB
# ============================================================

def show_simulation_lab():

    require_admin()
    apply_simulation_styles()

    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    st.markdown("""
<div class="qs-sim-hero">
<div class="qs-sim-eyebrow">
Q-SIGN / EXPERIMENTAL WORKSPACE
</div>
<div class="qs-sim-title">
Optical Simulation Lab
</div>
<div class="qs-sim-description">
Simulate RGB sensor responses, extract optical
fingerprint features and evaluate their similarity
to registered reference signatures.
</div>
</div>
""", unsafe_allow_html=True)

    # --------------------------------------------------------
    # STATUS CARDS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        stat_card("OPERATING MODE", "Software", "#4DE3D1")

    with col2:
        stat_card("FINGERPRINT FEATURES", "03", "#819BFF")

    with col3:
        stat_card("SCANNER STATUS", "Offline", "#C079F9")

    st.markdown("""
<div class="qs-sim-info">
<strong>Software simulation mode:</strong>
RGB readings are entered manually. No physical
optical scanner is currently connected.
</div>
""", unsafe_allow_html=True)

    # --------------------------------------------------------
    # LOAD REFERENCE FINGERPRINTS
    # --------------------------------------------------------

    if not FINGERPRINTS_FILE.exists():
        st.warning("Fingerprint database not found.")
        return

    try:
        references = load_reference_fingerprints()

    except (OSError, ValueError, KeyError) as error:
        st.error(f"Unable to load fingerprints: {error}")
        return

    if not references:
        st.warning("Register an optical tag before testing.")
        return

    # --------------------------------------------------------
    # SELECT REFERENCE
    # --------------------------------------------------------

    section_heading(
        "01",
        "Reference Fingerprint",
        "Choose a registered optical tag for comparison.",
    )

    selected_tag = st.selectbox(
        "Registered Optical Tag",
        list(references.keys()),
        key="simulation_tag",
    )

    reference_features = references[selected_tag]

    st.caption(
        f"Selected reference: {selected_tag}"
    )

    # --------------------------------------------------------
    # SENSOR INPUT
    # --------------------------------------------------------

    section_heading(
        "02",
        "Simulated Sensor Input",
        "Enter the RGB intensity values to be tested.",
    )

    with st.form("simulation_form"):

        col1, col2, col3 = st.columns(3)

        with col1:
            red = st.number_input(
                "Red (R)",
                min_value=0,
                max_value=255,
                value=95,
            )

        with col2:
            green = st.number_input(
                "Green (G)",
                min_value=1,
                max_value=255,
                value=130,
            )

        with col3:
            blue = st.number_input(
                "Blue (B)",
                min_value=1,
                max_value=255,
                value=105,
            )

        submitted = st.form_submit_button(
            "◉  Run Optical Simulation",
            use_container_width=True,
            type="primary",
        )

    # --------------------------------------------------------
    # LIVE INPUT PREVIEW
    # --------------------------------------------------------

    st.markdown(
        f"""
<div class="qs-sim-card">
<div class="qs-sim-card-label">
CURRENT RGB INPUT
</div>
<div class="qs-sim-rgb-preview"
style="background:rgb({red},{green},{blue});">
</div>
<div style="color:#F1F7FF;font-size:17px;font-weight:700;">
RGB ({red}, {green}, {blue})
</div>
<div class="qs-sim-note">
Preview of the manually entered RGB values.
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # RUN SIMULATION
    # --------------------------------------------------------

    if submitted:

        try:

            test_features = extract_rgb_features(
                int(red),
                int(green),
                int(blue),
            )

            distance = calculate_distance(
                test_features,
                reference_features,
            )

            possible_match = (
                distance <= MATCH_THRESHOLD
            )

            # Store result in Streamlit session
            st.session_state.simulation_result = {
                "tag": selected_tag,
                "rgb": (
                    int(red),
                    int(green),
                    int(blue),
                ),
                "test_features": test_features,
                "reference_features": reference_features,
                "distance": distance,
                "possible_match": possible_match,
            }

            # Preserve history logging
            try:

                save_history(
                    source="Simulation Lab",
                    tag_id=selected_tag,
                    rgb=(
                        int(red),
                        int(green),
                        int(blue),
                    ),
                    distance=distance,
                    threshold=MATCH_THRESHOLD,
                    possible_match=possible_match,
                )

            except Exception as error:

                st.error(
                    f"History saving failed: {error}"
                )

        except (
            ValueError,
            KeyError,
            ZeroDivisionError,
        ) as error:

            st.error(
                f"Simulation failed: {error}"
            )

            return

    # --------------------------------------------------------
    # DISPLAY RESULT
    # --------------------------------------------------------

    result = st.session_state.get(
        "simulation_result"
    )

    if result is None:

        st.info(
            "Enter RGB values and run a simulation "
            "to view the optical analysis."
        )

        return

    section_heading(
        "03",
        "Simulation Result",
        "Outcome of the latest optical fingerprint comparison.",
    )

    result_color = (
        "#4DE3D1"
        if result["possible_match"]
        else "#FF8999"
    )

    result_text = (
        "POSSIBLE MATCH"
        if result["possible_match"]
        else "FINGERPRINT MISMATCH"
    )

    st.markdown(
        f"""
<div class="qs-sim-result">
<div class="qs-sim-result-label">
OPTICAL VERIFICATION STATUS
</div>
<div class="qs-sim-result-value"
style="color:{result_color};">
{result_text}
</div>
<div class="qs-sim-note">
Reference tag: {html.escape(str(result["tag"]))}
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        stat_card(
            "FINGERPRINT DISTANCE",
            f'{result["distance"]:.4f}',
            "#4DE3D1",
        )

    with col2:
        stat_card(
            "MATCHING THRESHOLD",
            f"{MATCH_THRESHOLD:.4f}",
            "#819BFF",
        )

    # --------------------------------------------------------
    # EXTRACTED FEATURES
    # --------------------------------------------------------

    section_heading(
        "04",
        "Extracted Optical Features",
        "Normalized RGB ratios calculated from the test reading.",
    )

    feature_columns = st.columns(3)

    for column, name, value, color in zip(
        feature_columns,
        FEATURE_NAMES,
        result["test_features"],
        FEATURE_COLORS,
    ):

        with column:
            feature_card(
                name,
                value,
                color,
            )

    # --------------------------------------------------------
    # FEATURE COMPARISON TABLE
    # --------------------------------------------------------

    section_heading(
        "05",
        "Fingerprint Comparison",
        "Compare the simulated reading with the registered reference.",
    )

    feature_data = pd.DataFrame({
        "Feature": FEATURE_NAMES,
        "Test Reading": result["test_features"],
        "Reference": result["reference_features"],
    })

    st.dataframe(
        feature_data,
        use_container_width=True,
        hide_index=True,
    )

    comparison = feature_data.set_index(
        "Feature"
    )[
        ["Test Reading", "Reference"]
    ]

    st.bar_chart(
        comparison,
        use_container_width=True,
    )

    st.markdown("""
<div class="qs-sim-note">
Results indicate mathematical similarity between
RGB-derived optical fingerprints. They do not
establish physical product authenticity.
</div>
""", unsafe_allow_html=True)
