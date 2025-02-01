import streamlit as st
from src.audio.voice_input import VoiceProcessor
from dotenv import load_dotenv
import os
from src.language.language_processor import LanguageProcessor
from src.ui.components import ChatUI
from src.chat.message_handler import ChatState

# Load environment variables
load_dotenv()

# Configure OpenAI API
api_key = os.getenv("OPENAI_API_KEY")
if not api_key or api_key == "your_api_key_here":
    st.error("⚠️ OpenAI API key not found! Please add your API key to the .env file.")
    st.stop()

def main():
    st.title("🌍 Language Learning Chat")
    
    # Initialize session state
    ChatState.initialize_session_state()
    
    # Initialize components
    language_processor = LanguageProcessor(api_key)
    voice_processor = VoiceProcessor()  # Add this line
    chat_ui = ChatUI(language_processor, voice_processor)  # Update this line

    # Language selection
    if not st.session_state.target_language:
        st.header("Choose Your Target Language")
        languages = ChatState.get_available_languages()
        target_language = st.selectbox("Select the language you want to practice:", languages)
        
        if st.button("Confirm Language"):
            ChatState.set_language(target_language)
            st.rerun()

    # Chat mode selection
    elif not st.session_state.chat_mode:
        st.header("Choose Your Chat Mode")
        chat_modes = ["Free Conversation", "Role Play"]
        chat_mode = st.selectbox("Select how you want to practice:", chat_modes)
        
        scenario = None
        if chat_mode == "Role Play":
            scenarios = ChatState.get_available_scenarios()
            scenario = st.selectbox("Choose a role-play scenario:", scenarios)

        if st.button("Start Chatting"):
            ChatState.set_chat_mode(chat_mode, scenario)
            if chat_mode == "Role Play":
                # Start the conversation with an AI message
                initial_response = language_processor.get_ai_response(
                    "Let's start the conversation",
                    st.session_state.target_language,
                    chat_mode,
                    scenario
                )
                if initial_response:
                    st.session_state.messages.append({"role": "assistant", "content": initial_response})
            st.rerun()

    # Chat interface
    else:
        chat_ui.display_chat_interface()

        # Reset button
        if st.button("Start New Conversation"):
            ChatState.clear_state()
            st.rerun()

if __name__ == "__main__":
    main() 