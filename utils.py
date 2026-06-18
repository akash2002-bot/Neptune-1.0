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
    """Apply custom CSS styling to the app."""
    st.markdown(
        """
        <style>
        /* Global styles */
        .main {
            padding: 0 1rem;
        }
        .stApp {
            background-color: #f8faf8;
        }

        /* Headers */
        h1, h2, h3 {
            color: #1B5E20 !important;
            font-weight: 600 !important;
        }

        /* Cards */
        .card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
            border: 1px solid #e8f0e8;
            transition: transform 0.2s ease;
            margin-bottom: 1rem;
        }
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }
        .card-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: #1B5E20;
            margin-bottom: 0.5rem;
        }
        .card-value {
            font-size: 2rem;
            font-weight: 700;
            color: #2E7D32;
        }
        .card-subtitle {
            color: #666;
            font-size: 0.9rem;
        }

        /* Metric cards */
        .metric-card {
            background: white;
            border-radius: 10px;
            padding: 1.2rem;
            text-align: center;
            border: 1px solid #e8f0e8;
            box-shadow: 0 1px 4px rgba(0,0,0,0.04);
        }
        .metric-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #1B5E20;
        }
        .metric-label {
            color: #666;
            font-size: 0.85rem;
            margin-top: 0.2rem;
        }
        .metric-icon {
            font-size: 1.8rem;
            margin-bottom: 0.3rem;
        }

        /* Buttons */
        .stButton > button {
            background-color: #2E7D32 !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 0.6rem 1.8rem !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
        }
        .stButton > button:hover {
            background-color: #1B5E20 !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(46,125,50,0.3) !important;
        }

        /* Secondary button */
        .stButton > button.secondary {
            background-color: #e8f5e9 !important;
            color: #1B5E20 !important;
        }
        .stButton > button.secondary:hover {
            background-color: #c8e6c9 !important;
        }

        /* Sidebar */
        .css-1d391kg {
            background-color: #f8faf8 !important;
        }

        /* Expanders */
        .streamlit-expanderHeader {
            background-color: #f0f7f0 !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
            color: #1B5E20 !important;
        }
        .streamlit-expanderContent {
            background-color: white !important;
            border-radius: 0 0 8px 8px !important;
            border: 1px solid #e8f0e8 !important;
            border-top: none !important;
        }

        /* Progress bars */
        .stProgress > div > div {
            background-color: #2E7D32 !important;
            border-radius: 10px !important;
        }

        /* Chat */
        .chat-bot {
            background: #e8f5e9;
            padding: 0.8rem 1.2rem;
            border-radius: 12px 12px 12px 4px;
            margin: 0.4rem 0;
            max-width: 85%;
            display: inline-block;
        }
        .chat-user {
            background: #e3f2fd;
            padding: 0.8rem 1.2rem;
            border-radius: 12px 12px 4px 12px;
            margin: 0.4rem 0;
            max-width: 85%;
            display: inline-block;
            float: right;
        }
        .chat-container {
            display: flex;
            flex-direction: column;
            gap: 0.2rem;
        }
        .chat-row {
            display: flex;
            width: 100%;
        }
        .chat-row.bot {
            justify-content: flex-start;
        }
        .chat-row.user {
            justify-content: flex-end;
        }
        .chat-message {
            padding: 0.8rem 1.2rem;
            border-radius: 12px;
            max-width: 80%;
            word-wrap: break-word;
            line-height: 1.5;
        }
        .chat-message.bot {
            background: #e8f5e9;
            border-radius: 12px 12px 12px 4px;
            color: #1B3A1B;
        }
        .chat-message.user {
            background: #e3f2fd;
            border-radius: 12px 12px 4px 12px;
            color: #0D1F3C;
        }

        /* Tags */
        .tag {
            display: inline-block;
            padding: 0.2rem 0.8rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 500;
            margin: 0.1rem;
        }
        .tag-green {
            background: #e8f5e9;
            color: #1B5E20;
        }
        .tag-blue {
            background: #e3f2fd;
            color: #0D47A1;
        }
        .tag-orange {
            background: #fff3e0;
            color: #E65100;
        }
        .tag-purple {
            background: #f3e5f5;
            color: #4A148C;
        }

        /* Recommendation result */
        .result-card {
            background: linear-gradient(135deg, #f0f7f0 0%, #e8f5e9 100%);
            border-radius: 16px;
            padding: 2rem;
            border: 2px solid #2E7D32;
            margin: 1rem 0;
        }
        .result-species {
            font-size: 1.8rem;
            font-weight: 700;
            color: #1B5E20;
        }
        .result-score {
            font-size: 3rem;
            font-weight: 800;
            color: #2E7D32;
        }
        .result-confidence {
            font-size: 1.4rem;
            font-weight: 600;
            color: #1565C0;
        }

        /* Footer */
        .footer {
            text-align: center;
            padding: 2rem 0 1rem 0;
            color: #888;
            font-size: 0.8rem;
            border-top: 1px solid #e8f0e8;
            margin-top: 2rem;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .card-value {
                font-size: 1.5rem;
            }
            .result-species {
                font-size: 1.4rem;
            }
            .result-score {
                font-size: 2.2rem;
            }
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