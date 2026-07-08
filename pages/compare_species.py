"""
Neptune 1.0 - Compare Species Page
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from data import SPECIES_DATA, SPECIES_NAMES, get_species_data
from utils import display_pest_tags


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 6:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return (46, 125, 50)  # default green


def render():
    st.markdown(
        """
        <div style="margin-bottom: 1rem;">
            <h1 style="color: #1B5E20;">📊 Compare Species</h1>
            <p style="color: #555; font-size: 1rem;">
                Compare EPN species side by side to make an informed decision.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    species_list = SPECIES_NAMES

    col1, col2 = st.columns(2)

    with col1:
        species_a = st.selectbox("Select Species A", options=species_list, index=0)
    with col2:
        species_b = st.selectbox("Select Species B", options=species_list, index=min(1, len(species_list) - 1))

    if species_a and species_b:
        data_a = get_species_data(species_a)
        data_b = get_species_data(species_b)

        if not data_a or not data_b:
            st.warning("Species data not found.")
            return

        st.markdown("### 📋 Comparison Table")
        comparison_data = []

        a_m = data_a["soil_moisture"]
        b_m = data_b["soil_moisture"]
        comparison_data.append({"Parameter": "Soil Moisture", species_a: f"{a_m['min']}–{a_m['max']}%", species_b: f"{b_m['min']}–{b_m['max']}%"})

        a_t = data_a["soil_temperature"]
        b_t = data_b["soil_temperature"]
        comparison_data.append({"Parameter": "Soil Temperature", species_a: f"{a_t['min']}–{a_t['max']}°C", species_b: f"{b_t['min']}–{b_t['max']}°C"})

        a_at = data_a["atmospheric_temperature"]
        b_at = data_b["atmospheric_temperature"]
        comparison_data.append({"Parameter": "Atmospheric Temp", species_a: f"{a_at['min']}–{a_at['max']}°C", species_b: f"{b_at['min']}–{b_at['max']}°C"})

        a_ph = data_a["ph"]
        b_ph = data_b["ph"]
        a_ph_str = f"{a_ph['min']}–{a_ph['max']}"
        b_ph_str = f"{b_ph['min']}–{b_ph['max']}"
        if "up_to" in a_ph:
            a_ph_str += f" (up to {a_ph['up_to']})"
        if "up_to" in b_ph:
            b_ph_str += f" (up to {b_ph['up_to']})"
        comparison_data.append({"Parameter": "pH", species_a: a_ph_str, species_b: b_ph_str})

        a_rh = data_a["relative_humidity"]
        b_rh = data_b["relative_humidity"]
        comparison_data.append({"Parameter": "Relative Humidity", species_a: f">{a_rh['min']}%", species_b: f">{b_rh['min']}%"})

        comparison_data.append({"Parameter": "Preferred Soils", species_a: ", ".join(data_a["preferred_soils"]), species_b: ", ".join(data_b["preferred_soils"])})

        a_ec = data_a["ec"]
        b_ec = data_b["ec"]
        comparison_data.append({"Parameter": "EC", species_a: f"{a_ec['min']}–{a_ec['max']} dS/m", species_b: f"{b_ec['min']}–{b_ec['max']} dS/m"})

        a_d = data_a["penetration_depth"]["typical"]
        b_d = data_b["penetration_depth"]["typical"]
        comparison_data.append({"Parameter": "Penetration Depth", species_a: f"{a_d['min']}–{a_d['max']} cm", species_b: f"{b_d['min']}–{b_d['max']} cm"})

        comparison_data.append({"Parameter": "Number of Pests", species_a: str(len(data_a["pests"])), species_b: str(len(data_b["pests"]))})

        df = pd.DataFrame(comparison_data)
        st.dataframe(df, hide_index=True, use_container_width=True)

        st.markdown("### 📊 Performance Radar Chart")
        st.caption("Normalized scores based on environmental tolerance ranges (higher is better)")

        def normalize_range(value, min_val, max_val, ideal_min, ideal_max):
            if value is None:
                return 50
            if ideal_min <= value <= ideal_max:
                return 100
            if value < ideal_min:
                return max(0, 100 * (1 - (ideal_min - value) / (ideal_min + 5)))
            if value > ideal_max:
                return max(0, 100 * (1 - (value - ideal_max) / 10))
            return 50

        a_mid = {
            "moisture": (data_a["soil_moisture"]["min"] + data_a["soil_moisture"]["max"]) / 2,
            "temp": (data_a["soil_temperature"]["min"] + data_a["soil_temperature"]["max"]) / 2,
            "ph": (data_a["ph"]["min"] + data_a["ph"]["max"]) / 2,
            "ec": (data_a["ec"]["min"] + data_a["ec"]["max"]) / 2,
        }
        b_mid = {
            "moisture": (data_b["soil_moisture"]["min"] + data_b["soil_moisture"]["max"]) / 2,
            "temp": (data_b["soil_temperature"]["min"] + data_b["soil_temperature"]["max"]) / 2,
            "ph": (data_b["ph"]["min"] + data_b["ph"]["max"]) / 2,
            "ec": (data_b["ec"]["min"] + data_b["ec"]["max"]) / 2,
        }

        ideal_ranges = {"moisture": {"min": 10, "max": 20}, "temp": {"min": 25, "max": 30}, "ph": {"min": 5, "max": 7}, "ec": {"min": 0, "max": 2}}

        a_scores = {
            "Moisture": normalize_range(a_mid["moisture"], 0, 30, ideal_ranges["moisture"]["min"], ideal_ranges["moisture"]["max"]),
            "Temperature": normalize_range(a_mid["temp"], 15, 40, ideal_ranges["temp"]["min"], ideal_ranges["temp"]["max"]),
            "pH": normalize_range(a_mid["ph"], 3, 9, ideal_ranges["ph"]["min"], ideal_ranges["ph"]["max"]),
            "EC": normalize_range(a_mid["ec"], 0, 5, ideal_ranges["ec"]["min"], ideal_ranges["ec"]["max"]),
            "Pest Coverage": min(100, (len(data_a["pests"]) / 15) * 100),
        }
        b_scores = {
            "Moisture": normalize_range(b_mid["moisture"], 0, 30, ideal_ranges["moisture"]["min"], ideal_ranges["moisture"]["max"]),
            "Temperature": normalize_range(b_mid["temp"], 15, 40, ideal_ranges["temp"]["min"], ideal_ranges["temp"]["max"]),
            "pH": normalize_range(b_mid["ph"], 3, 9, ideal_ranges["ph"]["min"], ideal_ranges["ph"]["max"]),
            "EC": normalize_range(b_mid["ec"], 0, 5, ideal_ranges["ec"]["min"], ideal_ranges["ec"]["max"]),
            "Pest Coverage": min(100, (len(data_b["pests"]) / 15) * 100),
        }

        categories = ["Moisture", "Temperature", "pH", "EC", "Pest Coverage"]

        fig = go.Figure()

        # Get colors safely
        color_a = data_a.get("color", "#2E7D32")
        color_b = data_b.get("color", "#1565C0")

        # Convert hex to RGB for rgba()
        rgb_a = hex_to_rgb(color_a)
        rgb_b = hex_to_rgb(color_b)

        # Use rgba format with 25% opacity for fill
        rgba_a = f"rgba({rgb_a[0]}, {rgb_a[1]}, {rgb_a[2]}, 0.25)"
        rgba_b = f"rgba({rgb_b[0]}, {rgb_b[1]}, {rgb_b[2]}, 0.25)"

        fig.add_trace(go.Scatterpolar(
            r=[a_scores[c] for c in categories],
            theta=categories,
            fill='toself',
            name=species_a,
            line_color=color_a,
            fillcolor=rgba_a,
        ))

        fig.add_trace(go.Scatterpolar(
            r=[b_scores[c] for c in categories],
            theta=categories,
            fill='toself',
            name=species_b,
            line_color=color_b,
            fillcolor=rgba_b,
        ))

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100], tickvals=[20, 40, 60, 80, 100])),
            showlegend=True,
            height=450,
            margin=dict(l=40, r=40, t=20, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#1B5E20"),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 🐛 Pest Coverage Comparison")
        pests_a = set(data_a["pests"])
        pests_b = set(data_b["pests"])
        common_pests = pests_a & pests_b
        only_a = pests_a - pests_b
        only_b = pests_b - pests_a

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**{species_a} Only** ({len(only_a)})")
            if only_a:
                display_pest_tags(list(only_a), max_display=10)
            else:
                st.caption("None")
        with col2:
            st.markdown(f"**Common Pests** ({len(common_pests)})")
            if common_pests:
                display_pest_tags(list(common_pests), max_display=10)
            else:
                st.caption("None")
        with col3:
            st.markdown(f"**{species_b} Only** ({len(only_b)})")
            if only_b:
                display_pest_tags(list(only_b), max_display=10)
            else:
                st.caption("None")

    st.markdown(
        """
        <div class="footer">
            Neptune 1.0 v1.0 — Research-based Decision Support System
        </div>
        """,
        unsafe_allow_html=True,
    )
