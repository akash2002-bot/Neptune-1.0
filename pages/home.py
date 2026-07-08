# pages/home.py
"""
Neptune 1.0 - Home Page
"""

import streamlit as st
from data import SPECIES_DATA, ALL_PESTS


def render():
    """Render the home page."""
    st.markdown(
        """
        <div style="text-align: center; padding: 1rem 0 0.5rem 0;">
            <h1 style="font-size: 3rem; color: #1B5E20; margin: 0;">🌱 Neptune 1.0</h1>
            <p style="font-size: 1.2rem; color: #444; margin: 0.2rem 0 0 0;">
                Intelligent Entomopathogenic Nematode Recommendation System
            </p>
            <p style="font-size: 1rem; color: #666; margin: 0.5rem 0 0 0;">
                Protect crops naturally with intelligent nematode recommendations.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-icon">🧬</div>
                <div class="metric-value">{}</div>
                <div class="metric-label">Total Species</div>
            </div>
            """.format(len(SPECIES_DATA)),
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-icon">🐛</div>
                <div class="metric-value">{}</div>
                <div class="metric-label">Total Pests Covered</div>
            </div>
            """.format(len(ALL_PESTS)),
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-icon">📊</div>
                <div class="metric-value">✓</div>
                <div class="metric-label">Decision Support System</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-icon">🤖</div>
                <div class="metric-value">AI</div>
                <div class="metric-label">AI Guided Recommendation</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Call to Action
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="card" style="text-align: center; padding: 2rem;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">🔍</div>
                <h3 style="color: #1B5E20;">Find My Nematode</h3>
                <p style="color: #555;">Get a personalized EPN recommendation based on your pest and soil conditions.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Find My Nematode", key="home_find", use_container_width=True):
            st.session_state.page = "Find My Nematode"
            st.rerun()

    with col2:
        st.markdown(
            """
            <div class="card" style="text-align: center; padding: 2rem;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">🤖</div>
                <h3 style="color: #1B5E20;">Ask NemaGPT</h3>
                <p style="color: #555;">Chat with our AI advisor to get step-by-step guidance for EPN selection.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Ask NemaGPT", key="home_chat", use_container_width=True):
            st.session_state.page = "NemaGPT"
            st.rerun()

    # Quick info
    with st.expander("ℹ️ How does Neptune 1.0 work?"):
        st.markdown("""
        **Neptune 1.0** is an intelligent decision-support system for Entomopathogenic Nematode (EPN) selection.

        1. **Select your pest** — Tell us which pest you're dealing with
        2. **Provide soil information** — Share what you know about your soil conditions
        3. **Get recommendations** — Receive a suitability score and confidence level

        The system uses a weighted scoring algorithm based on research data to recommend the most suitable EPN species for your specific situation.
        """)

    # Footer
    st.markdown(
        """
        <div class="footer">
            Neptune 1.0 v1.0 — Research-based Decision Support System
        </div>
        """,
        unsafe_allow_html=True,
    )
