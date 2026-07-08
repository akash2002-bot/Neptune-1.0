# chatbot.py
"""
Neptune 1.0 - Chatbot Module
Rule-based conversational agent for EPN recommendations.
"""

import re
from data import ALL_PESTS, SOIL_TYPES, SPECIES_NAMES, get_species_data
from recommendation import get_recommendation_details


class ChatbotEngine:
    """
    Rule-based chatbot engine for guiding users through EPN selection.
    """

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset the conversation state."""
        self.state = "INITIAL"  # INITIAL, ASK_SOIL, ASK_PH, ASK_MOISTURE, ASK_TEMP, ASK_EC, RECOMMEND
        self.collected_info = {
            "pest": None,
            "soil_type": None,
            "ph": None,
            "soil_moisture": None,
            "soil_temperature": None,
            "ec": None,
        }
        self.conversation_history = []
        self.pending_question = None

    def get_next_question(self):
        """Get the next question based on current state."""
        if self.state == "INITIAL":
            return "Hello! I'm Neptune 1.0, your EPN advisor. 🌱\n\nWhat pest are you dealing with? Please tell me the name of the pest you're facing."
        elif self.state == "ASK_SOIL":
            return f"What type of soil do you have? (e.g., {', '.join(SOIL_TYPES[:4])}...)"
        elif self.state == "ASK_PH":
            return "Do you know the pH of your soil? Please enter a value between 0 and 14."
        elif self.state == "ASK_MOISTURE":
            return "What is the soil moisture level? (percentage, e.g., 15)"
        elif self.state == "ASK_TEMP":
            return "What is the soil temperature? (°C, e.g., 28)"
        elif self.state == "ASK_EC":
            return "What is the EC (electrical conductivity) of your soil? (dS/m, e.g., 1.2)"
        elif self.state == "RECOMMEND":
            return self.generate_recommendation()
        return "How can I help you with your pest problem?"

    def generate_recommendation(self):
        """Generate recommendation based on collected info."""
        pest = self.collected_info.get("pest")
        if not pest:
            return "I don't have enough information to make a recommendation. Please tell me what pest you're dealing with."

        params = {
            "soil_type": self.collected_info.get("soil_type"),
            "ph": self.collected_info.get("ph"),
            "soil_moisture": self.collected_info.get("soil_moisture"),
            "soil_temperature": self.collected_info.get("soil_temperature"),
            "ec": self.collected_info.get("ec"),
        }

        result = get_recommendation_details(pest, params)

        if not result:
            return "I couldn't find a suitable recommendation for your pest. Please try again with more information."

        # Build response
        response = "## 📋 Recommendation\n\n"
        response += f"**Recommended Species:** {result['recommended_species']}\n\n"
        response += f"**Suitability Score:** {result['suitability_score']}%\n"
        response += f"**Confidence:** {result['confidence']}%\n\n"

        response += "**Why?**\n"
        for reason in result["reasons"]:
            response += f"- {reason}\n"

        response += "\n---\n"
        response += "💡 *Would you like to start a new consultation? Just say 'restart' or 'new'*"

        return response

    def process_message(self, user_input):
        """
        Process a user message and return bot response.

        Args:
            user_input: The user's message text

        Returns:
            Bot response text
        """
        user_input = user_input.strip()

        # Handle restart
        if user_input.lower() in ["restart", "new", "reset", "start over"]:
            self.reset()
            return self.get_next_question()

        # Route based on state
        if self.state == "INITIAL":
            return self.handle_initial(user_input)
        elif self.state == "ASK_SOIL":
            return self.handle_soil(user_input)
        elif self.state == "ASK_PH":
            return self.handle_ph(user_input)
        elif self.state == "ASK_MOISTURE":
            return self.handle_moisture(user_input)
        elif self.state == "ASK_TEMP":
            return self.handle_temperature(user_input)
        elif self.state == "ASK_EC":
            return self.handle_ec(user_input)
        elif self.state == "RECOMMEND":
            # If in recommend state, show recommendation again or restart
            if user_input.lower() in ["restart", "new", "reset"]:
                self.reset()
                return self.get_next_question()
            return self.generate_recommendation() + "\n\n" + "Type 'restart' to start a new consultation."

        return "I'm not sure how to help. Please type 'restart' to start over."

    def handle_initial(self, user_input):
        """Handle pest identification."""
        # Try to find a matching pest
        matched_pest = None
        for pest in ALL_PESTS:
            if pest.lower() in user_input.lower():
                matched_pest = pest
                break

        if matched_pest:
            self.collected_info["pest"] = matched_pest
            self.state = "ASK_SOIL"
            return f"I see you're dealing with **{matched_pest}**. Great! Let me gather some more information to give you the best recommendation.\n\n{self.get_next_question()}"
        else:
            # Try to find partial matches
            possible_pests = []
            for pest in ALL_PESTS:
                if any(word in user_input.lower() for word in pest.lower().split()):
                    possible_pests.append(pest)

            if possible_pests:
                pest_list = ", ".join(possible_pests[:5])
                if len(possible_pests) > 5:
                    pest_list += f" and {len(possible_pests) - 5} more"
                return f"I'm not sure which pest you're referring to. Did you mean one of these: {pest_list}?\n\nPlease tell me the specific pest name or type 'restart' to try again."

            return f"I couldn't identify the pest from your message. Please tell me the name of the pest you're dealing with. I can help with pests like: {', '.join(ALL_PESTS[:8])}...\n\nType 'restart' to start over."

    def handle_soil(self, user_input):
        """Handle soil type input."""
        matched_soil = None
        for soil in SOIL_TYPES:
            if soil.lower() in user_input.lower():
                matched_soil = soil
                break

        if matched_soil:
            self.collected_info["soil_type"] = matched_soil
            self.state = "ASK_PH"
            return f"Got it! Soil type: **{matched_soil}**.\n\n{self.get_next_question()}"
        else:
            # Try to extract any soil-related word
            soil_keywords = ["sand", "loam", "clay", "silt", "sandy", "clayey"]
            found = None
            for keyword in soil_keywords:
                if keyword in user_input.lower():
                    found = keyword
                    break

            if found:
                # Try to match with a known soil type
                for soil in SOIL_TYPES:
                    if found in soil.lower():
                        self.collected_info["soil_type"] = soil
                        self.state = "ASK_PH"
                        return f"I think you mean **{soil}**. Let's continue.\n\n{self.get_next_question()}"

            return f"I didn't recognize that soil type. Please choose from: {', '.join(SOIL_TYPES)}.\n\nOr type 'restart' to start over."

    def handle_ph(self, user_input):
        """Handle pH input."""
        # Extract number
        numbers = re.findall(r"(\d+\.?\d*)", user_input)
        if numbers:
            ph_value = float(numbers[0])
            if 0 <= ph_value <= 14:
                self.collected_info["ph"] = ph_value
                self.state = "ASK_MOISTURE"
                return f"pH recorded: **{ph_value}**.\n\n{self.get_next_question()}"
            else:
                return "pH must be between 0 and 14. Please enter a valid pH value.\n\nType 'restart' to start over."

        return "I didn't catch that. Please enter a pH value between 0 and 14 (e.g., 6.5).\n\nType 'restart' to start over."

    def handle_moisture(self, user_input):
        """Handle soil moisture input."""
        numbers = re.findall(r"(\d+\.?\d*)", user_input)
        if numbers:
            moisture = float(numbers[0])
            if 0 <= moisture <= 100:
                self.collected_info["soil_moisture"] = moisture
                self.state = "ASK_TEMP"
                return f"Soil moisture: **{moisture}%**.\n\n{self.get_next_question()}"
            else:
                return "Soil moisture must be between 0% and 100%. Please enter a valid percentage.\n\nType 'restart' to start over."

        return "Please enter the soil moisture percentage (e.g., 15 for 15%).\n\nType 'restart' to start over."

    def handle_temperature(self, user_input):
        """Handle soil temperature input."""
        numbers = re.findall(r"(\d+\.?\d*)", user_input)
        if numbers:
            temp = float(numbers[0])
            if -10 <= temp <= 60:
                self.collected_info["soil_temperature"] = temp
                self.state = "ASK_EC"
                return f"Soil temperature: **{temp}°C**.\n\n{self.get_next_question()}"
            else:
                return "Temperature must be between -10°C and 60°C. Please enter a valid temperature.\n\nType 'restart' to start over."

        return "Please enter the soil temperature in °C (e.g., 28).\n\nType 'restart' to start over."

    def handle_ec(self, user_input):
        """Handle EC input."""
        numbers = re.findall(r"(\d+\.?\d*)", user_input)
        if numbers:
            ec = float(numbers[0])
            if 0 <= ec <= 100:
                self.collected_info["ec"] = ec
                self.state = "RECOMMEND"
                return self.generate_recommendation()
            else:
                return "EC must be between 0 and 100 dS/m. Please enter a valid EC value.\n\nType 'restart' to start over."

        return "Please enter the EC value in dS/m (e.g., 1.2).\n\nType 'restart' to start over."


# ============================================================================
# CHATBOT HELPER FUNCTIONS
# ============================================================================

def get_initial_bot_message():
    """Get the initial bot greeting message."""
    return (
        "👋 Hello! I'm Neptune 1.0, your intelligent EPN advisor.\n\n"
        "I can help you find the best entomopathogenic nematode species for your pest problem.\n\n"
        "**Just tell me:**\n"
        "• What pest you're dealing with\n"
        "• Your soil conditions (as much as you know)\n\n"
        "I'll guide you step by step and recommend the most suitable species.\n\n"
        "**Let's get started!** What pest are you facing?"
    )


def process_user_message(user_input, engine):
    """
    Process user message and update engine state.

    Args:
        user_input: User's message
        engine: ChatbotEngine instance

    Returns:
        Bot response
    """
    return engine.process_message(user_input)
