# pages/about_research.py
"""
Neptune 1.0 - About Research Page
Research background and disclaimer.
"""

import streamlit as st
from data import SPECIES_DATA, SPECIES_NAMES


def render():
    """Render the About Research page."""
    st.markdown(
        """
        <div style="margin-bottom: 1rem;">
            <h1 style="color: #1B5E20;">📖 About Research</h1>
            <p style="color: #555; font-size: 1rem;">
                Understanding the research foundation behind Neptune 1.0's recommendations.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Research Overview
    st.markdown("### 🔬 Research Foundation")

    st.markdown(
        """
        Neptune 1.0 is built upon extensive research on Entomopathogenic Nematodes (EPNs) and their 
        effectiveness against various agricultural pests. The recommendation engine uses 
        peer-reviewed data on EPN environmental preferences and host ranges.

        **Key Research Areas:**
        - Environmental tolerance ranges (temperature, moisture, pH, EC)
        - Host specificity and pest control efficacy
        - Soil physical properties and nematode movement
        - Saline and sodic soil tolerance
        - Penetration depth and foraging behavior
        """
    )

    # Data Sources
    with st.expander("📚 Research Data Sources"):
        st.markdown("""
        The data in Neptune 1.0 is compiled from:

        1. **Peer-reviewed journal articles** on EPN biology and application
        2. **Agricultural extension publications** from research institutions
        3. **Field trial data** from various agro-climatic zones
        4. **Laboratory studies** on EPN environmental tolerances

        **Key Species Data:**
        - *Heterorhabditis indica*: Extensive research on its efficacy against Coleoptera, Lepidoptera, Diptera, and Orthoptera
        - *Steinernema siamkayai*: Research on its effectiveness against Coleoptera, Lepidoptera, Diptera, and Thysanoptera
        """)

    # Species Summaries
    st.markdown("### 🧬 Species Research Summaries")

    for species in SPECIES_NAMES:
        data = SPECIES_DATA[species]
        icon = data.get("icon", "🧬")
        with st.expander(f"{icon} {species}"):
            st.markdown(f"**{data.get('common_name', species)}**")
            st.markdown(f"*{data.get('description', '')}*")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Environmental Preferences:**")
                st.markdown(f"- Soil Moisture: {data['soil_moisture']['min']}–{data['soil_moisture']['max']}%")
                st.markdown(f"- Soil Temperature: {data['soil_temperature']['min']}–{data['soil_temperature']['max']}°C")
                st.markdown(f"- pH: {data['ph']['min']}–{data['ph']['max']} (up to {data['ph']['up_to']})")
                st.markdown(f"- EC: {data['ec']['min']}–{data['ec']['max']} dS/m")

            with col2:
                st.markdown("**Soil & Physical Properties:**")
                st.markdown(f"- Preferred Soils: {', '.join(data['preferred_soils'])}")
                st.markdown(f"- Porosity: {data['porosity']['min']}–{data['porosity']['max']}%")
                st.markdown(f"- Bulk Density: {data['bulk_density']['min']}–{data['bulk_density']['max']} g/cm³")
                st.markdown(f"- Penetration Depth: {data['penetration_depth']['typical']['min']}–{data['penetration_depth']['typical']['max']} cm")

            st.markdown("**Target Pests:**")
            pests = data["pests"]
            pest_str = ", ".join(pests[:10]) + ("..." if len(pests) > 10 else "")
            st.markdown(pest_str)

    # Recommendation Methodology
    st.markdown("### ⚖️ Recommendation Methodology")

    st.markdown("""
    The Neptune 1.0 recommendation engine uses a **weighted scoring system**:

    | Factor | Weight | Description |
    |--------|--------|-------------|
    | Pest Match | 50% | Does the species control the specified pest? |
    | Soil Type Match | 20% | How well does the species perform in the given soil type? |
    | pH Match | 10% | Is the pH within the species' preferred range? |
    | Moisture Match | 10% | Is the soil moisture optimal for the species? |
    | Temperature Match | 5% | Is the soil temperature suitable? |
    | EC Match | 5% | Is the EC level within tolerance? |

    **Confidence Scoring:**
    The confidence level reflects how much information you provided:
    - Only pest identified: 40% confidence
    - Pest + 1 parameter: 55% confidence
    - Pest + 2 parameters: 70% confidence
    - Pest + 3 parameters: 82% confidence
    - Pest + 4 parameters: 92% confidence
    - All parameters: 100% confidence
    """)

    # Limitations and Disclaimer
    st.markdown("### ⚠️ Limitations & Disclaimer")

    st.warning(
        """
        **Important Disclaimer:**

        This application is a **decision-support tool** and recommendations should be 
        **validated with field conditions and expert guidance**.

        The recommendations are based on research data and may not account for:
        - Local micro-climatic variations
        - Soil heterogeneity within fields
        - Pest population dynamics
        - Nematode application methods and timing
        - Interactions with other soil organisms

        **Always consult with local agricultural experts** before making pest management decisions.
        """
    )

    # Research Contributors
    with st.expander("👨‍🔬 Research Contributors"):
        st.markdown("""
        Neptune 1.0 is developed based on research from:

        - **Agricultural Research Institutions** studying EPN biology and application
        - **Universities** conducting field trials and laboratory studies
        - **Extension Services** providing practical guidance to farmers

        *The data in this system is for educational and decision-support purposes only.*
        """)

    # Version
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #888; font-size: 0.85rem;">
            Neptune 1.0 v1.0 — Built with Streamlit<br>
            Research-based EPN Recommendation System
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Footer
    st.markdown(
        """
        <div class="footer">
            Neptune 1.0 v1.0 — Research-based Decision Support System
        </div>
        """,
        unsafe_allow_html=True,
    )
