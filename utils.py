# utils.py
"""
NemaIQ - Utility Functions
Helper functions for UI components and styling.
"""

import streamlit as st
import pandas as pd
from data import SPECIES_DATA, ALL_PESTS, SOIL_TYPES, get_species_data
import plotly.graph_objects as go
import plotly.express as px


def apply_custom_css():
    """Apply custom CSS with improved contrast and modern styling."""
    st.markdown(
        """
        <style>

        /* ============ APP ============ */

        .stApp{
            background:#F5FAF5;
            color:#263238;
        }

        section.main{
            background:#F5FAF5;
        }

        /* ============ SIDEBAR ============ */

        [data-testid="stSidebar"]{
            background:#E8F5E9;
            border-right:2px solid #C8E6C9;
        }

        [data-testid="stSidebar"] *{
            color:#263238 !important;
        }

        /* ============ HEADINGS ============ */

        h1,h2,h3,h4,h5,h6{
            color:#1B5E20 !important;
            font-weight:700;
        }

        p,label,span,li{
            color:#263238 !important;
        }

        /* ============ BUTTONS ============ */

        .stButton>button{
            width:100%;
            background:#2E7D32;
            color:white;
            border:none;
            border-radius:12px;
            padding:12px;
            font-weight:600;
            transition:.3s;
        }

        .stButton>button:hover{
            background:#1B5E20;
            transform:translateY(-2px);
            box-shadow:0 8px 20px rgba(0,0,0,.15);
            color:white;
        }

        /* ============ INPUTS ============ */

        input{
            background:white !important;
            color:#263238 !important;
            border-radius:10px !important;
        }

        textarea{
            background:white !important;
            color:#263238 !important;
        }

        /* ============ SELECTBOX ============ */

        [data-baseweb="select"]{
            background:white !important;
            border-radius:10px;
        }

        [data-baseweb="select"] *{
            color:#263238 !important;
        }

        div[role="listbox"]{
            background:white !important;
        }

        div[role="option"]{
            color:#263238 !important;
        }

        div[role="option"]:hover{
            background:#E8F5E9 !important;
        }

        /* ============ NUMBER INPUT ============ */

        [data-testid="stNumberInput"] input{
            background:white !important;
            color:#263238 !important;
        }

        /* ============ CHECKBOX ============ */

        [data-testid="stCheckbox"] label{
            color:#263238 !important;
            font-weight:500;
        }

        /* ============ EXPANDER ============ */

        details{
            background:white;
            border-radius:16px;
            padding:8px;
            border:1px solid #E0E0E0;
        }

        summary{
            color:#1B5E20 !important;
            font-weight:600;
        }

        /* ============ DATAFRAME ============ */

        .dataframe{
            background:white;
            color:#263238;
        }

        /* ============ METRIC ============ */

        [data-testid="stMetric"]{
            background:white;
            padding:18px;
            border-radius:18px;
            box-shadow:0 4px 12px rgba(0,0,0,.08);
        }

        [data-testid="stMetricValue"]{
            color:#2E7D32 !important;
            font-size:32px;
            font-weight:700;
        }

        [data-testid="stMetricLabel"]{
            color:#607D8B !important;
        }

        /* ============ TABS ============ */

        button[data-baseweb="tab"]{
            color:#263238 !important;
            font-weight:600;
        }

        button[data-baseweb="tab"][aria-selected="true"]{
            background:#E8F5E9 !important;
            border-radius:10px;
        }

        /* ============ ALERTS ============ */

        [data-testid="stAlert"]{
            border-radius:12px;
        }

        /* ============ PROGRESS ============ */

        .stProgress > div > div{
            background:#2E7D32 !important;
        }

        /* ============ SCROLLBAR ============ */

        ::-webkit-scrollbar{
            width:10px;
        }

        ::-webkit-scrollbar-thumb{
            background:#81C784;
            border-radius:20px;
        }

        ::-webkit-scrollbar-track{
            background:#F5FAF5;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def display_metric_card(icon, value, label, color="#2E7D32"):
    """Display a metric card."""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">{icon}</div>
            <div class="metric-value" style="color:{color}">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def display_species_card(species_name, expanded=False):
    """Display a species information card."""
    data = get_species_data(species_name)
    if not data:
        return

    with st.expander(
        f"{data.get('icon', '🧬')} {species_name} — {data.get('common_name', '')}",
        expanded=expanded,
    ):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**🌡️ Soil Moisture:** {data['soil_moisture']['min']}–{data['soil_moisture']['max']}%")
            st.markdown(f"**🌡️ Soil Temperature:** {data['soil_temperature']['min']}–{data['soil_temperature']['max']}°C")
            st.markdown(f"**🌡️ Atmospheric Temp:** {data['atmospheric_temperature']['min']}–{data['atmospheric_temperature']['max']}°C")
            st.markdown(f"**🧪 pH:** {data['ph']['min']}–{data['ph']['max']} (up to {data['ph']['up_to']})")
            st.markdown(f"**💧 Relative Humidity:** >{data['relative_humidity']['min']}%")

        with col2:
            st.markdown(f"**🏔️ Preferred Soils:** {', '.join(data['preferred_soils'])}")
            st.markdown(f"**📊 EC:** {data['ec']['min']}–{data['ec']['max']} dS/m")
            st.markdown(f"**📏 Penetration Depth:** {data['penetration_depth']['typical']['min']}–{data['penetration_depth']['typical']['max']} cm")
            st.markdown(f"**🐛 Target Pests:** {', '.join(data['pests'][:8])}" + ("..." if len(data['pests']) > 8 else ""))

        st.markdown("---")
        st.markdown(f"**📝 Description:** {data['description']}")


def display_recommendation_result(result):
    """Display recommendation results."""
    if not result:
        st.warning("No recommendation available. Please provide more information.")
        return

    species = result["recommended_species"]
    score = result["suitability_score"]
    confidence = result["confidence"]
    reasons = result["reasons"]

    # Color based on score
    if score >= 80:
        color = "#2E7D32"
        emoji = "🌟"
    elif score >= 60:
        color = "#F9A825"
        emoji = "👍"
    else:
        color = "#E53935"
        emoji = "⚠️"

    st.markdown(
        f"""
        <div class="result-card">
            <div style="display: flex; align-items: center; gap: 1rem; flex-wrap: wrap;">
                <div>
                    <div style="font-size: 0.9rem; color: #666;">Recommended Species</div>
                    <div class="result-species">{emoji} {species}</div>
                </div>
                <div style="flex: 1; min-width: 120px;">
                    <div style="font-size: 0.9rem; color: #666;">Suitability Score</div>
                    <div class="result-score" style="color:{color}">{score}%</div>
                </div>
                <div>
                    <div style="font-size: 0.9rem; color: #666;">Confidence</div>
                    <div class="result-confidence">{confidence}%</div>
                </div>
            </div>
            <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #c8e6c9;">
                <div style="font-weight: 600; color: #1B5E20; margin-bottom: 0.5rem;">Why this recommendation?</div>
                {"".join([f"<div style='padding: 0.2rem 0;'>• {r}</div>" for r in reasons])}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Display all scores in a dataframe
    st.markdown("### 📊 Species Comparison")
    df_data = []
    for sp, sc in result["all_scores"]:
        df_data.append({
            "Species": sp,
            "Suitability Score": f"{sc}%",
            "Score": sc,
        })
    df = pd.DataFrame(df_data)
    st.dataframe(df, hide_index=True, use_container_width=True)


def display_confidence_gauge(confidence):
    """Display a confidence gauge using plotly."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "Confidence Level"},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "darkblue"},
            "bar": {"color": "#2E7D32"},
            "bgcolor": "white",
            "borderwidth": 2,
            "bordercolor": "gray",
            "steps": [
                {"range": [0, 40], "color": "#ffcdd2"},
                {"range": [40, 60], "color": "#fff9c4"},
                {"range": [60, 75], "color": "#c8e6c9"},
                {"range": [75, 90], "color": "#a5d6a7"},
                {"range": [90, 100], "color": "#66bb6a"},
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": confidence,
            },
        },
    ))
    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#1B5E20"),
    )
    st.plotly_chart(fig, use_container_width=True)


def display_comparison_table(params):
    """Display a comparison table for species."""
    species_list = list(SPECIES_DATA.keys())

    # Build comparison data
    compare_data = []
    for species in species_list:
        data = get_species_data(species)
        if not data:
            continue
        row = {
            "Species": species,
            "Moisture": f"{data['soil_moisture']['min']}–{data['soil_moisture']['max']}%",
            "Soil Temp": f"{data['soil_temperature']['min']}–{data['soil_temperature']['max']}°C",
            "pH": f"{data['ph']['min']}–{data['ph']['max']}",
            "Soils": ", ".join(data['preferred_soils'][:2]),
            "EC": f"{data['ec']['min']}–{data['ec']['max']} dS/m",
            "Pests": len(data['pests']),
        }
        compare_data.append(row)

    df = pd.DataFrame(compare_data)
    st.dataframe(df, hide_index=True, use_container_width=True)


def display_pest_tags(pests, max_display=8):
    """Display pest names as tags."""
    tags = ""
    for i, pest in enumerate(pests):
        if i >= max_display:
            tags += f'<span class="tag tag-orange">+{len(pests) - max_display} more</span>'
            break
        color_class = "tag-green" if i % 2 == 0 else "tag-blue"
        tags += f'<span class="tag {color_class}">{pest}</span>'
    st.markdown(tags, unsafe_allow_html=True)
