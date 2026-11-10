
import html

import pandas as pd
import streamlit as st

from software.config import (
    FINGERPRINTS_FILE,
    MATCH_THRESHOLD,
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
# QUANTUM NOIR STYLING
# ============================================================

def apply_explorer_styles():

    st.markdown("""
<style>

.qs-exp-hero {
    background: linear-gradient(
        120deg,
        #142137,
        #101827
    );

    border: 1px solid #293A54;
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 26px;
}

.qs-exp-eyebrow {
    color: #4DE3D1;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
}

.qs-exp-title {
    color: #F1F7FF;
    font-size: clamp(30px, 4vw, 46px);
    font-weight: 800;
    margin: 12px 0;
}

.qs-exp-description {
    color: #A5B7CC;
    font-size: 15px;
    line-height: 1.7;
}

.qs-exp-section {
    color: #F1F7FF;
    font-size: 21px;
    font-weight: 700;
    margin: 25px 0 12px;
}

.qs-exp-subtitle {
    color: #91A9C1;
    font-size: 13px;
    line-height: 1.7;
    margin-bottom: 18px;
}

.qs-exp-card {
    background: linear-gradient(
        145deg,
        #142137,
        #101827
    );

    border: 1px solid #293A54;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 12px;
}

.qs-exp-card-label {
    color: #9CB2C8;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
}

.qs-exp-card-value {
    color: #F1F7FF;
    font-size: 31px;
    font-weight: 800;
    margin-top: 10px;
}

.qs-exp-accent {
    width: 48px;
    height: 3px;
    border-radius: 10px;
    margin-top: 12px;
}

.qs-exp-feature {
    background: #142137;
    border: 1px solid #293A54;
    border-radius: 14px;
    padding: 20px;
    text-align: center;
    margin-bottom: 12px;
}

.qs-exp-feature-name {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
}

.qs-exp-feature-value {
    color: #F1F7FF;
    font-size: 29px;
    font-weight: 800;
    margin-top: 10px;
}

.qs-exp-info {
    background: #102B2E;
    border: 1px solid #23665F;
    border-radius: 14px;
    padding: 18px 20px;
    margin: 16px 0;
    color: #C5D4E4;
    font-size: 13px;
    line-height: 1.7;
}

.qs-exp-distance {
    background: linear-gradient(
        120deg,
        #14283A,
        #171E35
    );

    border: 1px solid #38516A;
    border-radius: 16px;
    padding: 25px;
    text-align: center;
    margin-top: 20px;
}

.qs-exp-distance-label {
    color: #A5B7CC;
    font-size: 12px;
    letter-spacing: 2px;
    font-weight: 700;
}

.qs-exp-distance-value {
    color: #4DE3D1;
    font-size: 42px;
    font-weight: 800;
    margin-top: 10px;
}

.qs-exp-note {
    color: #8EA6BE;
    font-size: 13px;
    line-height: 1.7;
    margin-top: 16px;
}

/* Dataframe appearance */

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
<div class="qs-exp-section">
<span style="color:#4DE3D1;">{safe_number} /</span>
{safe_title}
</div>
<div class="qs-exp-subtitle">
{safe_description}
</div>
""",
        unsafe_allow_html=True,
    )


def statistic_card(label, value, color="#4DE3D1"):

    safe_label = html.escape(str(label))
    safe_value = html.escape(str(value))

    st.markdown(
        f"""
<div class="qs-exp-card">
<div class="qs-exp-card-label">{safe_label}</div>
<div class="qs-exp-card-value">{safe_value}</div>
<div class="qs-exp-accent"
style="background-color:{color};"></div>
</div>
""",
        unsafe_allow_html=True,
    )


def feature_card(name, value, color):

    safe_name = html.escape(str(name))

    st.markdown(
        f"""
<div class="qs-exp-feature">
<div class="qs-exp-feature-name"
style="color:{color};">
{safe_name}
</div>
<div class="qs-exp-feature-value">
{float(value):.4f}
</div>
</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# FINGERPRINT EXPLORER
# ============================================================

def show_fingerprint_explorer():

    # --------------------------------------------------------
    # ADMIN ACCESS
    # --------------------------------------------------------

    if not st.session_state.get("is_admin", False):

        st.error("Admin access required.")
        st.stop()

    apply_explorer_styles()

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.markdown("""
<div class="qs-exp-hero">
<div class="qs-exp-eyebrow">
Q-SIGN / OPTICAL INTELLIGENCE
</div>
<div class="qs-exp-title">
Fingerprint Explorer
</div>
<div class="qs-exp-description">
Analyze registered optical signatures, inspect
normalized RGB features and compare the
characteristics of different optical tags.
</div>
</div>
""", unsafe_allow_html=True)

    # --------------------------------------------------------
    # LOAD FINGERPRINTS
    # --------------------------------------------------------

    if not FINGERPRINTS_FILE.exists():

        st.warning(
            "No fingerprint database found."
        )

        return

    try:

        fingerprints = (
            load_reference_fingerprints()
        )

    except (OSError, ValueError, KeyError) as error:

        st.error(
            f"Unable to load fingerprints: {error}"
        )

        return

    if not fingerprints:

        st.info(
            "No registered fingerprints available."
        )

        return

    tag_ids = list(fingerprints.keys())

    # --------------------------------------------------------
    # PLATFORM STATISTICS
    # --------------------------------------------------------

    section_heading(
        "01",
        "Fingerprint Intelligence",
        "Overview of registered optical reference signatures.",
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        statistic_card(
            "REGISTERED OPTICAL TAGS",
            len(fingerprints),
            "#4DE3D1",
        )

    with col2:

        statistic_card(
            "FEATURES PER SIGNATURE",
            len(FEATURE_NAMES),
            "#819BFF",
        )

    with col3:

        statistic_card(
            "MATCHING THRESHOLD",
            f"{MATCH_THRESHOLD:.4f}",
            "#C079F9",
        )

    st.markdown("""
<div class="qs-exp-info">
Q-SIGN represents each optical fingerprint using
three normalized RGB intensity ratios:
<strong>R/G, B/G and R/B</strong>.
These ratios are compared mathematically to
distinguish registered optical signatures.
</div>
""", unsafe_allow_html=True)

    # --------------------------------------------------------
    # REGISTERED FINGERPRINT TABLE
    # --------------------------------------------------------

    section_heading(
        "02",
        "Registered Fingerprints",
        "Browse all stored optical fingerprint references.",
    )

    rows = []

    for tag_id, values in fingerprints.items():

        rows.append(
            {
                "Tag ID": tag_id,
                "R/G": round(values[0], 4),
                "B/G": round(values[1], 4),
                "R/B": round(values[2], 4),
            }
        )

    fingerprint_df = pd.DataFrame(rows)

    st.dataframe(
        fingerprint_df,
        use_container_width=True,
        hide_index=True,
    )

    # --------------------------------------------------------
    # ALL-TAG SIGNATURE COMPARISON
    # --------------------------------------------------------

    section_heading(
        "03",
        "Optical Signature Landscape",
        "Compare normalized RGB features across all registered tags.",
    )

    landscape_df = fingerprint_df.set_index(
        "Tag ID"
    )

    st.bar_chart(
        landscape_df[
            FEATURE_NAMES
        ],
        use_container_width=True,
    )

    st.caption(
        "These bars represent normalized RGB ratios, "
        "not measured emission wavelengths."
    )

    # --------------------------------------------------------
    # INDIVIDUAL TAG INSPECTION
    # --------------------------------------------------------

    section_heading(
        "04",
        "Inspect Optical Tag",
        "Explore the three fingerprint features of a selected tag.",
    )

    selected_tag = st.selectbox(
        "Select Registered Optical Tag",
        tag_ids,
        key="explorer_tag",
    )

    selected_values = fingerprints[
        selected_tag
    ]

    st.markdown(
        f"""
<div class="qs-exp-card">
<div class="qs-exp-card-label">
SELECTED OPTICAL IDENTITY
</div>
<div class="qs-exp-card-value">
{html.escape(str(selected_tag))}
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    feature_columns = st.columns(3)

    for column, name, value, color in zip(
        feature_columns,
        FEATURE_NAMES,
        selected_values,
        FEATURE_COLORS,
    ):

        with column:

            feature_card(
                name,
                value,
                color,
            )

    selected_df = pd.DataFrame(
        {
            "Feature": FEATURE_NAMES,
            "Value": selected_values,
        }
    ).set_index("Feature")

    st.bar_chart(
        selected_df,
        use_container_width=True,
        color="#4DE3D1",
    )

    # --------------------------------------------------------
    # TWO-TAG COMPARISON
    # --------------------------------------------------------

    section_heading(
        "05",
        "Compare Optical Tags",
        "Measure the distance between two registered fingerprints.",
    )

    if len(fingerprints) < 2:

        st.info(
            "Register at least two optical tags "
            "to compare."
        )

        return

    left_col, right_col = st.columns(2)

    with left_col:

        first_tag = st.selectbox(
            "First Optical Tag",
            tag_ids,
            index=0,
            key="compare_first",
        )

    with right_col:

        second_tag = st.selectbox(
            "Second Optical Tag",
            tag_ids,
            index=1,
            key="compare_second",
        )

    first_values = fingerprints[
        first_tag
    ]

    second_values = fingerprints[
        second_tag
    ]

    comparison = pd.DataFrame(
        {
            first_tag: first_values,
            second_tag: second_values,
        },
        index=FEATURE_NAMES,
    )

    st.markdown("#### Signature Comparison")

    st.bar_chart(
        comparison,
        use_container_width=True,
    )

    # --------------------------------------------------------
    # FINGERPRINT DISTANCE
    # --------------------------------------------------------

    distance = calculate_distance(
        first_values,
        second_values,
    )

    st.markdown(
        f"""
<div class="qs-exp-distance">
<div class="qs-exp-distance-label">
FINGERPRINT DISTANCE
</div>
<div class="qs-exp-distance-value">
{distance:.4f}
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    # Distance relative to matching threshold

    if first_tag == second_tag:

        st.info(
            "You selected the same optical tag twice. "
            "The fingerprint distance should be zero."
        )

    elif distance <= MATCH_THRESHOLD:

        st.warning(
            "These two reference fingerprints are "
            "within the configured matching threshold. "
            "Their stored signatures may be difficult "
            "to distinguish using this comparison."
        )

    else:

        st.success(
            "These two reference fingerprints are "
            "separated by more than the configured "
            "matching threshold."
        )

    st.markdown("""
<div class="qs-exp-note">
Fingerprint distance measures mathematical similarity
between stored feature vectors. Comparing two registered
tags does not authenticate a physical product.
</div>
""", unsafe_allow_html=True)
