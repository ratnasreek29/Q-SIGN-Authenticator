
import streamlit as st


def apply_quantum_theme():
    st.markdown(
        """
        <style>
        /* Main application */
        .stApp {
            background-color: #080D18;
            color: #E9F3FF;
        }

        /* Main content */
        .block-container {
            padding-top: 2rem;
            max-width: 1250px;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #101A2C;
            border-right: 1px solid #26374C;
        }

        /* Headings */
        h1, h2, h3 {
            color: #E9F3FF !important;
        }

        /* Paragraphs and labels */
        p, label {
            color: #D5E2F0;
        }

        /* Metric cards */
        [data-testid="stMetric"] {
            background-color: #142137;
            border: 1px solid #26374C;
            border-radius: 14px;
            padding: 18px;
        }

        [data-testid="stMetricValue"] {
            color: #4DE3D1;
        }

        /* Primary buttons */
        div.stButton > button[kind="primary"] {
            background-color: #4DE3D1;
            color: #08111F;
            border: none;
            border-radius: 10px;
            font-weight: 600;
        }

        div.stButton > button[kind="primary"]:hover {
            background-color: #75F2E4;
            color: #08111F;
        }

        /* Dividers */
        hr {
            border-color: #26374C;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
