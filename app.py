# app.py
"""
Neptune 1.0 - Intelligent Entomopathogenic Nematode Recommendation System
Main application entry point.
"""

import streamlit as st
from streamlit_option_menu import option_menu

# Import modules
from data import (
    SPECIES_DATA,
    PEST_MAPPING,
    ALL_PESTS,
    SPECIES_NAMES,
    SOIL_TYPES,
    get_species_for_pest,
    get_pests_for_species,
)
from recommendation import (
    calculate_suitability,
    get_confidence,
    get_recommendation_details,
    get_all_parameter_names,
)
from chatbot import (
    ChatbotEngine,
    get_initial_bot_message,
    process_user_message,
)
from utils import (
    apply_custom_css,
    display_metric_card,
    display_species_card,
    display_recommendation_result,
    display_confidence_gauge,
    display_comparison_table,
)

# Page configuration
st.set_page_config(
    page_title="Neptune 1.0 - EPN Recommendation System",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply custom CSS
apply_custom_css()

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "chatbot_engine" not in st.session_state:
    st.session_state.chatbot_engine = ChatbotEngine()

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
    initial_msg = get_initial_bot_message()
    st.session_state.chat_messages.append(("bot", initial_msg))

if "recommendation_result" not in st.session_state:
    st.session_state.recommendation_result = None

if "selected_pest" not in st.session_state:
    st.session_state.selected_pest = None

if "known_params" not in st.session_state:
    st.session_state.known_params = []

if "param_values" not in st.session_state:
    st.session_state.param_values = {}


# Sidebar navigation
with st.sidebar:
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="color: #2E7D32; margin: 0;">🌱 Neptune 1.0</h2>
            <p style="color: #555; font-size: 0.85rem; margin: 0;">
                Intelligent EPN Recommendation
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    selected = option_menu(
        menu_title=None,
        options=[
            "Home",
            "Find My Nematode",
            "NemaGPT",
            "Species Explorer",
            "Compare Species",
            "About Research",
        ],
        icons=[
            "house-fill",
            "search",
            "robot",
            "biomass",
            "arrow-left-right",
            "info-circle",
        ],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#2E7D32", "font-size": "18px"},
            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "margin": "2px 0",
                "padding": "10px 15px",
                "border-radius": "8px",
                "color": "#333",
            },
            "nav-link-selected": {
                "background-color": "#E8F5E9",
                "color": "#1B5E20",
                "font-weight": "600",
            },
        },
    )

    st.session_state.page = selected

    # Sidebar footer
    st.markdown(
        """
        <hr style="margin: 20px 0 10px 0; border-color: #ddd;">
        <div style="text-align: center; font-size: 0.75rem; color: #888;">
            <p>Neptune 1.0 v1.0</p>
            <p>🧪 Research-based Decision Support</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Page routing
page = st.session_state.page

if page == "Home":
    from pages.home import render as home_render
    home_render()

elif page == "Find My Nematode":
    from pages.find_my_nematode import render as find_render
    find_render()

elif page == "NemaGPT":
    from pages.nemagpt import render as chat_render
    chat_render()

elif page == "Species Explorer":
    from pages.species_explorer import render as species_render
    species_render()

elif page == "Compare Species":
    from pages.compare_species import render as compare_render
    compare_render()

elif page == "About Research":
    from pages.about_research import render as about_render
    about_render()
