
import pandas as pd
import streamlit as st

from software.database.history import load_history


def show_system_history():
    if not st.session_state.get("is_admin", False):
        st.error("Admin access required.")
        return

    st.title("System History")
    st.caption("Q-SIGN simulation and verification records")

    try:
        records = load_history()
    except Exception as error:
        st.error(f"Unable to load history: {error}")
        return

    if not records:
        st.info(
            "No history recorded yet. "
            "Run a test in Simulation Lab."
        )
        return

    df = pd.DataFrame(records)

    total = len(df)
    matches = (df["result"] == "POSSIBLE MATCH").sum()
    mismatches = (df["result"] == "FINGERPRINT MISMATCH").sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Tests", total)
    col2.metric("Possible Matches", int(matches))
    col3.metric("Mismatches", int(mismatches))

    st.divider()
    st.subheader("Filter History")

    selected_tag = st.selectbox(
        "Optical Tag",
        ["All"] + sorted(df["tag_id"].dropna().unique().tolist()),
    )

    selected_result = st.selectbox(
        "Result",
        ["All", "POSSIBLE MATCH", "FINGERPRINT MISMATCH"],
    )

    filtered = df.copy()

    if selected_tag != "All":
        filtered = filtered[filtered["tag_id"] == selected_tag]

    if selected_result != "All":
        filtered = filtered[filtered["result"] == selected_result]

    st.divider()
    st.subheader("Verification Records")

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "Download History (CSV)",
        data=filtered.to_csv(index=False),
        file_name="qsign_history.csv",
        mime="text/csv",
    )

    st.caption(
        "These records represent software-based "
        "fingerprint comparisons, not independently "
        "verified product authenticity."
    )
