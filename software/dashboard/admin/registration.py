
import html
import streamlit as st

from software.registration.register_tag import register_tag
from software.registration.manage_tags import (
    load_tags,
    edit_tag,
    delete_tag,
)
from software.database.product_registry import (
    load_product_registry,
    register_product,
)


# ============================================================
# ADMIN ACCESS
# ============================================================

def require_admin():
    if not st.session_state.get("is_admin", False):
        st.error("Admin access required.")
        st.stop()


# ============================================================
# QUANTUM NOIR REGISTRATION STYLING
# ============================================================

def apply_registration_styles():

    st.markdown("""
<style>

.qs-reg-hero {
    background: linear-gradient(120deg, #142137, #101827);
    border: 1px solid #293A54;
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 26px;
}

.qs-reg-eyebrow {
    color: #4DE3D1;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
}

.qs-reg-title {
    color: #F1F7FF;
    font-size: clamp(30px, 4vw, 46px);
    font-weight: 800;
    margin: 12px 0;
}

.qs-reg-description {
    color: #A5B7CC;
    font-size: 15px;
    line-height: 1.7;
}

.qs-reg-section {
    color: #F1F7FF;
    font-size: 22px;
    font-weight: 700;
    margin: 24px 0 10px;
}

.qs-reg-subtitle {
    color: #91A9C1;
    font-size: 13px;
    line-height: 1.7;
    margin-bottom: 18px;
}

.qs-reg-card {
    background: linear-gradient(145deg, #142137, #101827);
    border: 1px solid #293A54;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 15px;
}

.qs-reg-card-title {
    color: #F1F7FF;
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 8px;
}

.qs-reg-card-desc {
    color: #A5B7CC;
    font-size: 13px;
    line-height: 1.6;
}

.qs-reg-step {
    display: inline-block;
    color: #4DE3D1;
    background: #143A43;
    border: 1px solid #286B72;
    border-radius: 8px;
    padding: 5px 10px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 12px;
}

.qs-reg-info {
    background: #102B2E;
    border: 1px solid #23665F;
    border-radius: 14px;
    padding: 17px 20px;
    margin: 15px 0;
    color: #C5D4E4;
    font-size: 13px;
    line-height: 1.7;
}

.qs-reg-warning {
    background: #30241C;
    border: 1px solid #775334;
    border-radius: 14px;
    padding: 17px 20px;
    margin: 15px 0;
    color: #F0C99C;
    font-size: 13px;
    line-height: 1.7;
}

.qs-reg-note {
    color: #8EA6BE;
    font-size: 12px;
    line-height: 1.7;
    margin-top: 15px;
}

/* Registration tabs */

.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    border-bottom: 1px solid #293A54;
}

.stTabs [data-baseweb="tab"] {
    background: #142137;
    border: 1px solid #293A54;
    border-radius: 10px;
    color: #B5C6D9;
    padding: 10px 20px;
}

.stTabs [aria-selected="true"] {
    background: #173E49;
    color: #4DE3D1;
    border-color: #348B91;
}

/* Form containers */

div[data-testid="stForm"] {
    background: linear-gradient(145deg, #121F32, #101827);
    border: 1px solid #293A54;
    border-radius: 16px;
    padding: 22px;
}

/* Input focus */

div[data-baseweb="input"]:focus-within {
    border-color: #4DE3D1;
}

/* Table appearance */

div[data-testid="stDataFrame"] {
    border: 1px solid #293A54;
    border-radius: 12px;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# REUSABLE HEADING
# ============================================================

def section_heading(number, title, description=""):

    safe_number = html.escape(str(number))
    safe_title = html.escape(str(title))
    safe_description = html.escape(str(description))

    st.markdown(
        f"""
<div class="qs-reg-section">
<span style="color:#4DE3D1;">{safe_number} /</span>
{safe_title}
</div>
<div class="qs-reg-subtitle">
{safe_description}
</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# REGISTRATION DASHBOARD
# ============================================================

def show_registration():

    require_admin()
    apply_registration_styles()

    st.markdown("""
<div class="qs-reg-hero">
<div class="qs-reg-eyebrow">Q-SIGN / IDENTITY MANAGEMENT</div>
<div class="qs-reg-title">Identity Registration</div>
<div class="qs-reg-description">
Create and manage unique optical fingerprints,
register product identities and link products
to their corresponding optical tags.
</div>
</div>
""", unsafe_allow_html=True)

    tag_tab, product_tab = st.tabs([
        "◉  Optical Tags",
        "▣  Products",
    ])

    with tag_tab:
        show_tag_management()

    with product_tab:
        show_product_registration()


# ============================================================
# OPTICAL TAG MANAGEMENT
# ============================================================

def show_tag_management():

    require_admin()

    # --------------------------------------------------------
    # REGISTER NEW OPTICAL TAG
    # --------------------------------------------------------

    section_heading(
        "01",
        "Register Optical Tag",
        "Create a reference fingerprint using simulated RGB readings.",
    )

    st.markdown("""
<div class="qs-reg-card">
<div class="qs-reg-step">NEW OPTICAL IDENTITY</div>
<div class="qs-reg-card-title">Fingerprint Enrollment</div>
<div class="qs-reg-card-desc">
Each optical tag is represented by a unique identifier
and normalized RGB intensity ratios.
</div>
</div>
""", unsafe_allow_html=True)

    with st.form(
        "register_tag_form",
        clear_on_submit=True,
    ):

        tag_id = st.text_input(
            "Optical Tag ID",
            placeholder="Example: TAG_D",
        )

        st.caption("Enter RGB sensor readings (0–255).")

        col1, col2, col3 = st.columns(3)

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
                key="register_red",
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
                key="register_green",
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
                key="register_blue",
            )

        submitted = st.form_submit_button(
            "◉  Register Optical Fingerprint",
            use_container_width=True,
            type="primary",
        )

    if submitted:

        try:

            register_tag(
                tag_id,
                int(red),
                int(green),
                int(blue),
            )

            st.success(
                "Optical tag registered successfully."
            )

        except (ValueError, OSError) as error:

            st.error(str(error))

    # --------------------------------------------------------
    # REGISTERED OPTICAL TAGS
    # --------------------------------------------------------

    section_heading(
        "02",
        "Registered Optical Tags",
        "View the reference signatures stored in the tag registry.",
    )

    try:
        tags = load_tags()

    except (OSError, ValueError, KeyError) as error:
        st.error(f"Unable to load tags: {error}")
        return

    if not tags:
        st.info("No optical tags registered yet.")
        return

    st.dataframe(
        tags,
        use_container_width=True,
        hide_index=True,
    )

    tag_ids = [
        row["Sample_ID"]
        for row in tags
    ]

    st.caption(
        f"Total registered optical tags: {len(tag_ids)}"
    )

    # --------------------------------------------------------
    # EDIT EXISTING OPTICAL TAG
    # --------------------------------------------------------

    section_heading(
        "03",
        "Edit Optical Tag",
        "Update an existing optical fingerprint reference.",
    )

    selected_tag = st.selectbox(
        "Select Optical Tag",
        tag_ids,
        key="edit_tag_selection",
    )

    selected_record = next(
        (
            row
            for row in tags
            if row["Sample_ID"] == selected_tag
        ),
        None,
    )

    st.markdown("""
<div class="qs-reg-info">
Editing a fingerprint changes how future sensor readings
are compared against this optical tag. Keep your original
RGB measurements in your project records.
</div>
""", unsafe_allow_html=True)

    # The registry may store normalized ratios rather than
    # raw RGB readings. Do not assume the original RGB values
    # can be recovered from those ratios.

    if st.session_state.get("edit_loaded_tag") != selected_tag:

        st.session_state.edit_loaded_tag = selected_tag

        st.session_state["edit_red_input"] = 100
        st.session_state["edit_green_input"] = 120
        st.session_state["edit_blue_input"] = 110

    with st.form("edit_tag_form"):

        st.caption(
            f"Editing reference: {selected_tag}"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            new_red = st.number_input(
                "New Red (R)",
                min_value=0,
                max_value=255,
                key="edit_red_input",
            )

        with col2:

            new_green = st.number_input(
                "New Green (G)",
                min_value=1,
                max_value=255,
                key="edit_green_input",
            )

        with col3:

            new_blue = st.number_input(
                "New Blue (B)",
                min_value=1,
                max_value=255,
                key="edit_blue_input",
            )

        edit_submitted = st.form_submit_button(
            "Update Tag Fingerprint",
            use_container_width=True,
        )

    if edit_submitted:

        try:

            edit_tag(
                selected_tag,
                int(new_red),
                int(new_green),
                int(new_blue),
            )

            st.success("Tag fingerprint updated.")
            st.rerun()

        except (ValueError, KeyError, OSError) as error:

            st.error(str(error))

    # --------------------------------------------------------
    # DELETE OPTICAL TAG
    # --------------------------------------------------------

    section_heading(
        "04",
        "Delete Optical Tag",
        "Remove a reference fingerprint from the registry.",
    )

    st.markdown("""
<div class="qs-reg-warning">
Deleting an optical tag removes its stored fingerprint
reference. Products assigned to that tag may no longer
be verifiable until their assignments are updated.
</div>
""", unsafe_allow_html=True)

    delete_selection = st.selectbox(
        "Select Tag to Delete",
        tag_ids,
        key="delete_tag_selection",
    )

    confirm_delete = st.checkbox(
        "I understand that deleting this tag removes "
        "its registered reference fingerprint.",
        key="confirm_tag_delete",
    )

    if st.button(
        "Delete Selected Optical Tag",
        disabled=not confirm_delete,
        use_container_width=True,
        key="delete_optical_tag_button",
    ):

        try:

            delete_tag(delete_selection)

            st.success("Tag deleted successfully.")
            st.rerun()

        except (ValueError, KeyError, OSError) as error:

            st.error(str(error))


# ============================================================
# PRODUCT REGISTRATION
# ============================================================

def show_product_registration():

    require_admin()

    section_heading(
        "01",
        "Register Product",
        "Assign an existing optical fingerprint to a product identity.",
    )

    st.markdown("""
<div class="qs-reg-card">
<div class="qs-reg-step">PRODUCT ENROLLMENT</div>
<div class="qs-reg-card-title">Product Identity Assignment</div>
<div class="qs-reg-card-desc">
Connect a product identifier to a registered optical tag.
This association will be used during future verification.
</div>
</div>
""", unsafe_allow_html=True)

    try:

        tags = load_tags()
        products = load_product_registry()

    except (OSError, ValueError, KeyError) as error:

        st.error(
            f"Unable to load registration data: {error}"
        )
        return

    tag_ids = [
        row["Sample_ID"]
        for row in tags
    ]

    if not tag_ids:

        st.warning(
            "Register at least one optical tag first."
        )

    else:

        with st.form(
            "register_product_form",
            clear_on_submit=True,
        ):

            product_id = st.text_input(
                "Product ID",
                placeholder="Example: PROD_002",
            )

            optical_tag = st.selectbox(
                "Assign Optical Tag",
                tag_ids,
            )

            st.caption(
                "Only registered optical tags can be "
                "assigned to products."
            )

            product_submitted = st.form_submit_button(
                "▣  Register Product",
                use_container_width=True,
                type="primary",
            )

        if product_submitted:

            try:

                current_tags = {
                    row["Sample_ID"]
                    for row in load_tags()
                }

                if optical_tag not in current_tags:

                    raise ValueError(
                        "Selected optical tag no longer exists."
                    )

                register_product(
                    product_id,
                    optical_tag,
                )

                st.success(
                    "Product registered successfully."
                )

                st.rerun()

            except (ValueError, KeyError, OSError) as error:

                st.error(str(error))

    # --------------------------------------------------------
    # REGISTERED PRODUCTS
    # --------------------------------------------------------

    section_heading(
        "02",
        "Registered Products",
        "View products and their assigned optical identities.",
    )

    if products:

        product_rows = [
            {
                "Product ID": product_id,
                "Optical Tag": tag_id,
            }
            for product_id, tag_id in products.items()
        ]

        st.dataframe(
            product_rows,
            use_container_width=True,
            hide_index=True,
        )

        st.caption(
            f"Total registered products: {len(products)}"
        )

    else:

        st.info("No products registered yet.")

    st.markdown("""
<div class="qs-reg-note">
Q-SIGN currently uses simulated RGB measurements
and stored optical fingerprints. Hardware scanner
integration is planned for a later development phase.
</div>
""", unsafe_allow_html=True)
