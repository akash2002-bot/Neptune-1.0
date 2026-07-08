# pages/species_explorer.py
"""
Neptune 1.0 - Species Explorer Page
Detailed information about each EPN species.
"""

import streamlit as st
from data import SPECIES_DATA, SPECIES_NAMES, get_species_data
from utils import display_pest_tags


def render():
    """Render the Species Explorer page."""
    st.markdown(
        """
        <div style="margin-bottom: 1rem;">
            <h1 style="color: #1B5E20;">🧬 Species Explorer</h1>
            <p style="color: #555; font-size: 1rem;">
                Explore detailed information about each Entomopathogenic Nematode (EPN) species
                available in the Neptune 1.0 recommendation system.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Species selection
    species_options = SPECIES_NAMES
    selected_species = st.selectbox(
        "Select a species to explore:",
        options=species_options,
        index=0,
    )

    if selected_species:
        data = get_species_data(selected_species)
        if not data:
            st.warning("Species data not found.")
            return

        # Main species card
        icon = data.get("icon", "🧬")
        color = data.get("color", "#2E7D32")

        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #f8faf8 0%, #e8f5e9 100%); 
                        border-radius: 16px; padding: 2rem; border: 2px solid {color}; 
                        margin-bottom: 1.5rem;">
                <div style="display: flex; align-items: center; gap: 1rem; flex-wrap: wrap;">
                    <span style="font-size: 3rem;">{icon}</span>
                    <div>
                        <h2 style="color: {color}; margin: 0;">{selected_species}</h2>
                        <p style="color: #555; margin: 0.2rem 0 0 0; font-size: 1rem;">
                            {data.get('common_name', '')}
                        </p>
                    </div>
                </div>
                <p style="color: #444; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #c8e6c9;">
                    {data.get('description', '')}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Two-column layout for parameters
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🌡️ Environmental Parameters")

            # Soil Moisture
            moisture = data["soil_moisture"]
            st.metric(
                "Soil Moisture",
                f"{moisture['min']}–{moisture['max']}{moisture['unit']}",
                help="Optimal soil moisture range for this species.",
            )

            # Soil Temperature
            temp = data["soil_temperature"]
            st.metric(
                "Soil Temperature",
                f"{temp['min']}–{temp['max']}{temp['unit']}",
                help="Optimal soil temperature range for this species.",
            )

            # Atmospheric Temperature
            atm_temp = data["atmospheric_temperature"]
            st.metric(
                "Atmospheric Temperature",
                f"{atm_temp['min']}–{atm_temp['max']}{atm_temp['unit']}",
                help="Optimal atmospheric temperature range for this species.",
            )

            # pH
            ph = data["ph"]
            ph_display = f"{ph['min']}–{ph['max']}"
            if "up_to" in ph:
                ph_display += f" (up to {ph['up_to']})"
            st.metric(
                "pH",
                ph_display,
                help="Optimal pH range for this species.",
            )

            # Relative Humidity
            rh = data["relative_humidity"]
            st.metric(
                "Relative Humidity",
                f">{rh['min']}{rh['unit']}",
                help="Minimum relative humidity required.",
            )

        with col2:
            st.markdown("### 🏔️ Soil & Physical Properties")

            # Preferred Soils
            st.markdown("**Preferred Soils:**")
            for soil in data["preferred_soils"]:
                st.markdown(f"• {soil}")

            # Porosity
            porosity = data["porosity"]
            st.metric(
                "Porosity",
                f"{porosity['min']}–{porosity['max']}{porosity['unit']}",
                help="Optimal soil porosity range.",
            )

            # Bulk Density
            bd = data["bulk_density"]
            st.metric(
                "Bulk Density",
                f"{bd['min']}–{bd['max']} {bd['unit']}",
                help="Optimal bulk density range.",
            )

            # EC
            ec = data["ec"]
            ec_display = f"{ec['min']}–{ec['max']} {ec['unit']}"
            st.metric(
                "EC",
                ec_display,
                help="Optimal electrical conductivity range.",
            )

            # Penetration Depth
            depth = data["penetration_depth"]
            typical = depth["typical"]
            depth_display = f"{typical['min']}–{typical['max']} {typical['unit']}"
            if "sandy_optimum" in depth:
                depth_display += f" (sandy: up to {depth['sandy_optimum']}{typical['unit']})"
            st.metric(
                "Penetration Depth",
                depth_display,
                help="Typical penetration depth in soil.",
            )

        # Pests
        st.markdown("---")
        st.markdown("### 🐛 Target Pests")

        pests = data["pests"]
        col1, col2 = st.columns([3, 1])

        with col1:
            display_pest_tags(pests, max_display=20)

        with col2:
            st.metric("Total Pests", len(pests))

        # Additional details with expanders
        st.markdown("---")
        with st.expander("📊 Saline & Sodic Tolerance"):
            col1, col2 = st.columns(2)

            with col1:
                saline = data["saline_tolerance"]
                if isinstance(saline, dict):
                    if "min" in saline and "max" in saline:
                        st.metric("Saline Tolerance", f"{saline['min']}–{saline['max']} {saline['unit']}")
                    else:
                        st.metric("Saline Tolerance (Max)", f"{saline['max']} {saline['unit']}")

            with col2:
                sodic = data["sodic_tolerance"]
                st.metric("Sodic Tolerance", f"ESP < {sodic['max']}%")
                if "reduced_at" in sodic:
                    st.caption(f"⚠️ Movement reduces at ESP > {sodic['reduced_at']}%")

        with st.expander("📖 Scientific Details"):
            st.markdown(f"""
            **Species:** {selected_species}

            **Classification:** Entomopathogenic Nematode (EPN)

            **Symbiotic Bacteria:** *Photorhabdus* spp. (for *Heterorhabditis*) or *Xenorhabdus* spp. (for *Steinernema*)

            **Life Cycle:** EPNs have a symbiotic relationship with bacteria. The infective juveniles (IJs) enter the host, release bacteria, and the bacteria multiply, killing the host within 24-48 hours.

            **Mode of Action:** EPNs actively seek out hosts in the soil, entering through natural openings. The symbiotic bacteria produce toxins and enzymes that break down host tissues, providing nutrients for nematode reproduction.

            **Application:** Typically applied as a drench to soil or growing media. Best applied in the evening or early morning to avoid UV exposure.
            """)

        # Quick stats summary
        st.markdown("---")
        st.markdown("### 📊 Quick Summary")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Soil Moisture", f"{moisture['min']}–{moisture['max']}%")

        with col2:
            st.metric("Soil Temp", f"{temp['min']}–{temp['max']}°C")

        with col3:
            st.metric("pH", f"{ph['min']}–{ph['max']}")

        with col4:
            st.metric("Target Pests", len(pests))

    # Footer
    st.markdown(
        """
        <div class="footer">
            Neptune 1.0 v1.0 — Research-based Decision Support System
        </div>
        """,
        unsafe_allow_html=True,
    )
