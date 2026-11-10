
import html

import pandas as pd
import streamlit as st

from software.config import FINGERPRINTS_FILE
from software.authentication.fingerprint_matching import (
    load_reference_fingerprints,
)
from software.database.product_registry import (
    load_product_registry,
)
from software.database.history import load_history


# ============================================================
# QUANTUM NOIR ADMIN OVERVIEW STYLING
# ============================================================

def apply_overview_styles():
    st.markdown("""
<style>
.qs-admin-hero {
    background: linear-gradient(120deg, #142137, #101827);
    border: 1px solid #293A54;
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 26px;
}

.qs-admin-label {
    color: #4DE3D1;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
}

.qs-admin-title {
    color: #F1F7FF;
    font-size: clamp(30px, 4vw, 46px);
    font-weight: 800;
    margin: 12px 0;
}

.qs-admin-description {
    color: #A5B7CC;
    font-size: 15px;
    line-height: 1.7;
}

.qs-admin-section {
    color: #F1F7FF;
    font-size: 21px;
    font-weight: 700;
    margin: 25px 0 15px;
}

.qs-stat-card {
    background: linear-gradient(145deg, #142137, #101827);
    border: 1px solid #293A54;
    border-radius: 16px;
    padding: 20px;
    min-height: 135px;
    margin-bottom: 12px;
}

.qs-stat-label {
    color: #9CB2C8;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
}

.qs-stat-value {
    color: #F1F7FF;
    font-size: 34px;
    font-weight: 800;
    margin-top: 12px;
}

.qs-stat-accent {
    width: 48px;
    height: 3px;
    border-radius: 10px;
    margin-top: 12px;
}

.qs-status {
    background: #102B2E;
    border: 1px solid #23665F;
    border-radius: 14px;
    padding: 18px 22px;
    margin: 15px 0 24px;
}

.qs-status-title {
    color: #4DE3D1;
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 7px;
}

.qs-status-description {
    color: #C5D4E4;
    font-size: 13px;
    line-height: 1.7;
}

.qs-admin-note {
    color: #8EA6BE;
    font-size: 13px;
    line-height: 1.7;
    margin-top: 15px;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# REUSABLE STATISTIC CARD
# ============================================================

def statistic_card(label, value, accent="#4DE3D1"):
    safe_label = html.escape(str(label))
    safe_value = html.escape(str(value))

    # Accent colors are supplied only by this module.
    st.markdown(
        f"""
<div class="qs-stat-card">
<div class="qs-stat-label">{safe_label}</div>
<div class="qs-stat-value">{safe_value}</div>
<div class="qs-stat-accent"
     style="background-color:{accent};"></div>
</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# ADMIN OVERVIEW
# ============================================================

def show_overview():

    apply_overview_styles()

    # Dashboard header
    st.markdown("""
<div class="qs-admin-hero">
<div class="qs-admin-label">Q-SIGN / ADMIN CONTROL CENTER</div>
<div class="qs-admin-title">System Overview</div>
<div class="qs-admin-description">
Monitor registered optical identities, product records,
verification analytics and recent authentication activity.
</div>
</div>
""", unsafe_allow_html=True)

    # --------------------------------------------------------
    # LOAD REGISTERED DATA
    # --------------------------------------------------------

    try:
        tags = (
            load_reference_fingerprints()
            if FINGERPRINTS_FILE.exists()
            else {}
        )

        products = load_product_registry()

    except (OSError, ValueError, KeyError) as error:
        st.error(f"Unable to load project data: {error}")
        return

    # --------------------------------------------------------
    # LOAD VERIFICATION HISTORY
    # --------------------------------------------------------

    history_available = True

    try:
        records = load_history()
    except Exception as error:
        records = []
        history_available = False
        st.warning(
            f"Unable to load verification statistics: {error}"
        )

    history_df = pd.DataFrame(records)

    total_attempts = len(history_df)

    if "result" in history_df.columns:
        possible_matches = int(
            (history_df["result"] == "POSSIBLE MATCH").sum()
        )

        mismatches = int(
            (
                history_df["result"]
                == "FINGERPRINT MISMATCH"
            ).sum()
        )
    else:
        possible_matches = 0
        mismatches = 0

    match_rate = (
        possible_matches / total_attempts * 100
        if total_attempts > 0
        else 0.0
    )

    # --------------------------------------------------------
    # SUMMARY CARDS
    # --------------------------------------------------------

    st.markdown("""
<div class="qs-admin-section">Platform Statistics</div>
""", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        statistic_card(
            "REGISTERED TAGS",
            len(tags),
            "#4DE3D1",
        )

    with col2:
        statistic_card(
            "REGISTERED PRODUCTS",
            len(products),
            "#C079F9",
        )

    with col3:
        statistic_card(
            "VERIFICATION ATTEMPTS",
            total_attempts if history_available else "N/A",
            "#819BFF",
        )

    with col4:
        statistic_card(
            "POSSIBLE MATCH RATE",
            f"{match_rate:.1f}%" if history_available else "N/A",
            "#4DE3D1",
        )

    # --------------------------------------------------------
    # SYSTEM STATUS
    # --------------------------------------------------------

    st.markdown("""
<div class="qs-admin-section">System Status</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="qs-status">
<div class="qs-status-title">
● SOFTWARE SIMULATION ACTIVE
</div>
<div class="qs-status-description">
Q-SIGN is currently operating as a software-only
optical fingerprinting prototype using simulated
RGB sensor readings. Hardware scanner integration
is not active.
</div>
</div>
""", unsafe_allow_html=True)

    # --------------------------------------------------------
    # REGISTERED OPTICAL TAGS
    # --------------------------------------------------------

    st.markdown("""
<div class="qs-admin-section">Registered Optical Tags</div>
""", unsafe_allow_html=True)

    if tags:
        tag_data = [
            {
                "Tag ID": tag_id,
                "R/G": round(values[0], 4),
                "B/G": round(values[1], 4),
                "R/B": round(values[2], 4),
            }
            for tag_id, values in tags.items()
        ]

        st.dataframe(
            tag_data,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.warning("No optical tags registered yet.")

    # --------------------------------------------------------
    # REGISTERED PRODUCTS
    # --------------------------------------------------------

    st.markdown("""
<div class="qs-admin-section">Registered Products</div>
""", unsafe_allow_html=True)

    if products:
        product_data = [
            {
                "Product ID": product_id,
                "Optical Tag": tag_id,
            }
            for product_id, tag_id in products.items()
        ]

        st.dataframe(
            product_data,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.warning("No products registered yet.")

    # --------------------------------------------------------
    # VERIFICATION ANALYTICS
    # --------------------------------------------------------

    st.markdown("""
<div class="qs-admin-section">Verification Analytics</div>
""", unsafe_allow_html=True)

    if not history_available:
        st.info("Verification analytics are currently unavailable.")
        return

    if history_df.empty:
        st.info(
            "No verification activity recorded yet. "
            "Run a simulation or verify a product."
        )
        return

    metric_col1, metric_col2, metric_col3 = st.columns(3)

    with metric_col1:
        st.metric(
            "Total Attempts",
            total_attempts,
        )

    with metric_col2:
        st.metric(
            "Possible Matches",
            possible_matches,
        )

    with metric_col3:
        st.metric(
            "Fingerprint Mismatches",
            mismatches,
        )

    # Result distribution chart
    st.markdown("#### Verification Result Distribution")

    result_counts = pd.DataFrame(
        {
            "Result": [
                "Possible Match",
                "Fingerprint Mismatch",
            ],
            "Attempts": [
                possible_matches,
                mismatches,
            ],
        }
    )

    st.bar_chart(
        result_counts,
        x="Result",
        y="Attempts",
        color="#4DE3D1",
        use_container_width=True,
    )

    # --------------------------------------------------------
    # RECENT VERIFICATION ACTIVITY
    # --------------------------------------------------------

    st.markdown("""
<div class="qs-admin-section">Recent Verification Activity</div>
""", unsafe_allow_html=True)

    recent_columns = [
        "timestamp",
        "source",
        "product_id",
        "tag_id",
        "distance",
        "result",
    ]

    missing_columns = [
        column
        for column in recent_columns
        if column not in history_df.columns
    ]

    if missing_columns:
        st.warning(
            "Recent activity cannot be displayed because "
            "some history fields are unavailable: "
            + ", ".join(missing_columns)
        )
    else:
        recent_activity = history_df[
            recent_columns
        ].head(5).copy()

        recent_activity["distance"] = pd.to_numeric(
            recent_activity["distance"],
            errors="coerce",
        ).round(4)

        st.dataframe(
            recent_activity,
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("""
<div class="qs-admin-note">
Statistics include simulation and user verification records.
A possible fingerprint match does not independently establish
physical product authenticity.
</div>
""", unsafe_allow_html=True)
