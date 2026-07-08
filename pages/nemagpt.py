# pages/nemagpt.py
"""
Neptune 1.0 - NemaGPT Page
Rule-based chatbot for guided EPN recommendations.
"""

import streamlit as st
from chatbot import ChatbotEngine, get_initial_bot_message, process_user_message
from utils import display_recommendation_result


def render():
    """Render the NemaGPT page."""
    st.markdown(
        """
        <div style="margin-bottom: 1rem;">
            <h1 style="color: #1B5E20;">🤖 NemaGPT</h1>
            <p style="color: #555; font-size: 1rem;">
                Chat with our intelligent advisor. Tell me about your pest and soil conditions,
                and I'll guide you to the best EPN recommendation.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Initialize chat engine in session state
    if "chat_engine" not in st.session_state:
        st.session_state.chat_engine = ChatbotEngine()

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            ("bot", get_initial_bot_message())
        ]

    # ========== Chat Display ==========
    chat_container = st.container()

    with chat_container:
        st.markdown("### 💬 Conversation")

        # Display chat messages
        for role, message in st.session_state.chat_messages:
            if role == "bot":
                st.markdown(
                    f"""
                    <div class="chat-row bot">
                        <div class="chat-message bot">
                            {message.replace('\n', '<br>')}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div class="chat-row user">
                        <div class="chat-message user">
                            {message.replace('\n', '<br>')}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # Add a small spacer
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # ========== User Input ==========
    with st.container():
        col1, col2 = st.columns([5, 1])

        with col1:
            user_input = st.text_input(
                "Your message:",
                placeholder="Type your message here... (e.g., 'I have white grubs in my sugarcane field')",
                key="chat_input",
                label_visibility="collapsed",
            )

        with col2:
            send_btn = st.button(
                "Send",
                use_container_width=True,
                type="primary",
            )

    # ========== Process Input ==========
    if send_btn and user_input:
        # Add user message
        st.session_state.chat_messages.append(("user", user_input))

        # Process with chatbot
        engine = st.session_state.chat_engine
        response = process_user_message(user_input, engine)

        # Add bot response
        st.session_state.chat_messages.append(("bot", response))

        # Clear input (by rerunning)
        st.rerun()

    # ========== Quick Actions ==========
    st.markdown("---")
    st.markdown("### 🚀 Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔄 Restart Conversation", use_container_width=True):
            st.session_state.chat_engine = ChatbotEngine()
            st.session_state.chat_messages = [
                ("bot", get_initial_bot_message())
            ]
            st.rerun()

    with col2:
        if st.button("🐛 Show All Pests", use_container_width=True):
            from data import ALL_PESTS
            pest_list = ", ".join(ALL_PESTS[:15]) + ("..." if len(ALL_PESTS) > 15 else "")
            st.session_state.chat_messages.append(
                ("bot", f"Here are all the pests I can help with:\n\n{pest_list}\n\nTell me which one you're dealing with!")
            )
            st.rerun()

    with col3:
        if st.button("📋 Example Scenario", use_container_width=True):
            example = "I have white grubs in my sugarcane field. The soil is sandy loam with pH 6.5 and moisture around 15%."
            st.session_state.chat_messages.append(("user", example))
            engine = st.session_state.chat_engine
            response = process_user_message(example, engine)
            st.session_state.chat_messages.append(("bot", response))
            st.rerun()

    # ========== Tips ==========
    with st.expander("💡 Tips for using NemaGPT"):
        st.markdown("""
        **How to get the best recommendations:**

        1. **Start with your pest** — Tell me the name of the pest you're dealing with.
        2. **Share soil information** — Provide as much soil data as you know:
           - Soil type (Sandy Loam, Sand, etc.)
           - pH value
           - Soil moisture (%)
           - Soil temperature (°C)
           - EC (dS/m)

        3. **Be specific** — The more precise your information, the better the recommendation.

        4. **Use 'restart'** — Type 'restart' at any time to start a new conversation.

        5. **Don't worry** — I'll guide you step by step and only ask for what I need.
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
