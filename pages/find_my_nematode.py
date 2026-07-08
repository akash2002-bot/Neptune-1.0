# pages/find_my_nematode.py
"""
Neptune 1.0 - Find My Nematode Page
Recommendation engine with partial information support.
"""

import streamlit as st
from data import ALL_PESTS, SOIL_TYPES, get_species_for_pest, SPECIES_DATA
from recommendation import (
    get_recommendation_details,
    get_confidence,
    calculate_suitability,
    get_all_parameter_names,
)
from utils import display_recommendation_result, display_confidence_gauge


def render():
    """Render the Find My Nematode page."""
    st.markdown(
        """
        <div style="margin-bottom: 1rem;">
            <h1 style="color: #1B5E20;">🔍 Find My Nematode</h1>
            <p style="color: #555; font-size: 1rem;">
                Get a personalized EPN recommendation based on your pest and soil conditions.
                <br>Provide as much information as you can — the more you share, the higher the confidence.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Initialize session state for this page
    if "fm_pest" not in st.session_state:
        st.session_state.fm_pest = None
    if "fm_params" not in st.session_state:
        st.session_state.fm_params = {}
    if "fm_known" not in st.session_state:
        st.session_state.fm_known = []
    if "fm_result" not in st.session_state:
        st.session_state.fm_result = None

    # ========== STEP 1: Select Pest ==========
    st.markdown("### Step 1: Select Your Pest")

    pest_options = sorted(ALL_PESTS)
    selected_pest = st.selectbox(
        "Which pest are you facing?",
        options=[""] + pest_options,
        index=0,
        help="Select the pest you're dealing with from the list.",
    )

    if selected_pest:
        st.session_state.fm_pest = selected_pest

        # Show which species can control this pest
        controlling_species = get_species_for_pest(selected_pest)
        if controlling_species:
            species_icons = {"Heterorhabditis indica": "🐛", "Steinernema siamkayai": "🪱"}
            species_display = " ".join(
                [f"{species_icons.get(s, '🧬')} {s}" for s in controlling_species]
            )
            st.info(f"✅ This pest can be controlled by: {species_display}")

        # ========== STEP 2: Select Known Parameters ==========
        st.markdown("---")
        st.markdown("### Step 2: What Information Do You Know?")

        st.markdown(
            """
            <div style="background: #f0f7f0; padding: 0.8rem 1.2rem; border-radius: 8px; margin-bottom: 1rem;">
                <span style="color: #1B5E20;">💡 </span>
                <span style="color: #444;">Check the parameters you know. Only selected fields will appear below.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        param_options = [
            "Soil Type",
            "pH",
            "Soil Moisture",
            "Soil Temperature",
            "EC",
        ]

        known_params = st.multiselect(
            "Select the parameters you know:",
            options=param_options,
            default=st.session_state.fm_known,
            help="Check all that apply. You can provide partial information.",
        )

        st.session_state.fm_known = known_params

        # ========== STEP 3: Input Values ==========
        st.markdown("---")
        st.markdown("### Step 3: Provide Your Soil Data")

        if not known_params:
            st.info("📝 Select at least one parameter above to provide soil data.")
        else:
            params = {}

            for param in known_params:
                if param == "Soil Type":
                    soil_type = st.selectbox(
                        "Soil Type",
                        options=[""] + SOIL_TYPES,
                        index=0,
                        help="Select your soil type.",
                    )
                    if soil_type:
                        params["soil_type"] = soil_type

                elif param == "pH":
                    ph = st.number_input(
                        "pH Value",
                        min_value=0.0,
                        max_value=14.0,
                        value=7.0,
                        step=0.1,
                        format="%.1f",
                        help="Enter the pH of your soil (0-14).",
                    )
                    params["ph"] = ph

                elif param == "Soil Moisture":
                    moisture = st.number_input(
                        "Soil Moisture (%)",
                        min_value=0.0,
                        max_value=100.0,
                        value=15.0,
                        step=0.5,
                        format="%.1f",
                        help="Enter the soil moisture percentage.",
                    )
                    params["soil_moisture"] = moisture

                elif param == "Soil Temperature":
                    temp = st.number_input(
                        "Soil Temperature (°C)",
                        min_value=-10.0,
                        max_value=60.0,
                        value=28.0,
                        step=0.5,
                        format="%.1f",
                        help="Enter the soil temperature in Celsius.",
                    )
                    params["soil_temperature"] = temp

                elif param == "EC":
                    ec = st.number_input(
                        "EC (dS/m)",
                        min_value=0.0,
                        max_value=100.0,
                        value=1.0,
                        step=0.1,
                        format="%.1f",
                        help="Enter the electrical conductivity in dS/m.",
                    )
                    params["ec"] = ec

            st.session_state.fm_params = params

        # ========== STEP 4: Generate Recommendation ==========
        st.markdown("---")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            generate_btn = st.button(
                "🚀 Generate Recommendation",
                use_container_width=True,
                disabled=not selected_pest,
            )

        if generate_btn and selected_pest:
            params = st.session_state.fm_params

            # Get recommendation
            result = get_recommendation_details(selected_pest, params)
            st.session_state.fm_result = result

        # ========== Display Results ==========
        if st.session_state.fm_result:
            st.markdown("---")
            st.markdown("### 📋 Recommendation Results")

            result = st.session_state.fm_result

            # Display recommendation card
            display_recommendation_result(result)

            # Confidence gauge
            col1, col2 = st.columns([1, 2])
            with col1:
                display_confidence_gauge(result["confidence"])
            with col2:
                st.markdown(
                    f"""
                    <div style="background: white; border-radius: 12px; padding: 1.5rem; border: 1px solid #e8f0e8; height: 100%;">
                        <h4 style="color: #1B5E20; margin-top: 0;">📊 Information Provided</h4>
                        <div style="margin: 0.5rem 0;">
                            <span class="tag tag-green">✅ Pest: {selected_pest}</span>
                        </div>
                        {''.join([
                            f'<div style="margin: 0.3rem 0;"><span class="tag tag-blue">📌 {k}: {v}</span></div>'
                            for k, v in st.session_state.fm_params.items()
                            if v
                        ])}
                        <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #eee;">
                            <span style="color: #666; font-size: 0.9rem;">
                                Confidence: {result["confidence"]}%
                                {" (High)" if result["confidence"] >= 80 else " (Moderate)" if result["confidence"] >= 60 else " (Low)"}
                            </span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Display all scores
            st.markdown("---")
            st.markdown("### 📊 Detailed Scoring")

            # Show score breakdown
            scores = result["all_scores"]
            import pandas as pd

            df_data = []
            for sp, sc in scores:
                # Get pest match status
                species_data = SPECIES_DATA.get(sp, {})
                pest_match = "✓" if selected_pest in species_data.get("pests", []) else "✗"
                df_data.append({
                    "Species": sp,
                    "Pest Match": pest_match,
                    "Suitability Score": f"{sc}%",
                    "Score": sc,
                })
            df = pd.DataFrame(df_data)
            st.dataframe(df, hide_index=True, use_container_width=True)

            # Explanation of weights
            with st.expander("ℹ️ How scores are calculated"):
                st.markdown("""
                **Weighted Scoring System:**

                | Factor | Weight |
        |--------|--------|
        | Pest Match | 50% |
        | Soil Type Match | 20% |
        | pH Match | 10% |
        | Moisture Match | 10% |
        | Temperature Match | 5% |
        | EC Match | 5% |

                **Confidence** is determined by how much information you provided:
                - Only pest: 40%
                - Pest + 1 parameter: 55%
                - Pest + 2 parameters: 70%
                - Pest + 3 parameters: 82%
                - Pest + 4 parameters: 92%
                - All parameters: 100%
                """)

        elif selected_pest and not st.session_state.fm_result:
            st.info(
                "🔬 Select your parameters and click 'Generate Recommendation' to get your personalized EPN recommendation."
            )

        elif not selected_pest:
            st.warning("⚠️ Please select a pest to get started.")

    else:
        st.info("👆 Select a pest from the dropdown above to begin.")

    # Footer
    st.markdown(
        """
        <div class="footer">
            Neptune 1.0 v1.0 — Research-based Decision Support System
        </div>
        """,
        unsafe_allow_html=True,
    )
