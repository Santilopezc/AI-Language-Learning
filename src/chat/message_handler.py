import streamlit as st

class ChatState:
    @staticmethod
    def initialize_session_state():
        """Initialize all session state variables."""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "target_language" not in st.session_state:
            st.session_state.target_language = None
        if "chat_mode" not in st.session_state:
            st.session_state.chat_mode = None
        if "role_play_scenario" not in st.session_state:
            st.session_state.role_play_scenario = None
        if "corrections" not in st.session_state:
            st.session_state.corrections = {}
        if "translations" not in st.session_state:
            st.session_state.translations = {}
        if "audio_bytes" not in st.session_state:
            st.session_state.audio_bytes = None
        if "processed_audio" not in st.session_state:
            st.session_state.processed_audio = False
        if "last_message_count" not in st.session_state:
            st.session_state.last_message_count = 0

    @staticmethod
    def clear_state():
        """Clear all session state variables."""
        # Store the API key temporarily if it exists
        api_key = st.session_state.get('api_key', None)
        
        # Clear all state
        st.session_state.clear()
        
        # Restore API key if it existed
        if api_key:
            st.session_state.api_key = api_key
            
        # Reinitialize session state with empty values
        ChatState.initialize_session_state()

    @staticmethod
    def get_available_languages():
        """Get list of available languages."""
        return [
            "Spanish",
            "French",
            "German",
            "Italian",
            "Japanese",
            "Mandarin Chinese"
        ]

    @staticmethod
    def get_available_scenarios():
        """Get list of available role-play scenarios."""
        return [
            "At a restaurant (ordering food)",
            "At a train station (buying tickets)",
            "Shopping at a store",
            "Job interview",
            "Making new friends at a party",
            "Asking for directions"
        ]

    @staticmethod
    def set_language(language):
        """Set the target language."""
        st.session_state.target_language = language

    @staticmethod
    def set_chat_mode(mode, scenario=None):
        """Set the chat mode and scenario if applicable."""
        st.session_state.chat_mode = mode
        if scenario:
            st.session_state.role_play_scenario = scenario 