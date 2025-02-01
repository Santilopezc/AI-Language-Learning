import streamlit as st

class ChatUI:
    def __init__(self, language_processor, voice_processor):
        self.language_processor = language_processor
        self.voice_processor = voice_processor
        self._init_session_state()

    def _init_session_state(self):
        """Initialize session state variables for audio handling."""
        if "audio_bytes" not in st.session_state:
            st.session_state.audio_bytes = None
        if "processed_audio" not in st.session_state:
            st.session_state.processed_audio = False
        if "last_message_count" not in st.session_state:
            st.session_state.last_message_count = 0

    def display_message(self, message, message_key, is_user_message=True):
        """Display a chat message with its buttons and expandable sections."""
        with st.chat_message(message["role"]):
            st.write(message["content"])
            col1, col2, col3 = st.columns([4, 1, 1])
            
            # Add correction button only for user messages
            if is_user_message:
                with col2:
                    if message_key not in st.session_state.corrections:
                        if st.button("📝 Check", key=f"correct_{message_key}", help="Get language corrections"):
                            corrections = self.language_processor.get_corrections(
                                message["content"],
                                st.session_state.target_language
                            )
                            if corrections:
                                st.session_state.corrections[message_key] = corrections
                                st.rerun()
            
            # Add translation button for all messages
            with col3:
                if message_key not in st.session_state.translations:
                    if st.button("🔄 Translate", key=f"translate_{message_key}", help="Show English translation"):
                        translation = self.language_processor.get_translation(
                            message["content"],
                            st.session_state.target_language
                        )
                        if translation:
                            st.session_state.translations[message_key] = translation
                            st.rerun()
            
            # Display corrections for user messages
            if is_user_message and message_key in st.session_state.corrections:
                with st.expander("✨ View Corrections", expanded=True):
                    st.markdown(st.session_state.corrections[message_key])
            
            # Display translations for all messages
            if message_key in st.session_state.translations:
                with st.expander("🔄 Translation", expanded=True):
                    st.markdown(f"**English:** {st.session_state.translations[message_key]}")

    def handle_audio_input(self):
        audio = self.voice_processor.get_audio_recorder()
        
        if audio and audio.get('bytes') and audio['bytes'] != st.session_state.get('prev_audio'):
            st.session_state.audio_bytes = audio['bytes']
            
            with st.spinner("Transcribing audio..."):
                transcribed_text = self.voice_processor.transcribe_audio(
                    st.session_state.audio_bytes
                )
                if transcribed_text:
                    # Update state BEFORE rerun
                    st.session_state.prev_audio = audio['bytes']
                    st.session_state.audio_bytes = None
                    
                    self.handle_new_message(transcribed_text, is_voice=True)
                    st.rerun()  # Now safe to rerun

    def handle_new_message(self, message_content, is_voice=False):
        """Handle a new message from either voice or text input."""
        if not message_content:
            return

        # Add user message
        st.session_state.messages.append({"role": "user", "content": message_content})
        st.session_state.last_message_count = len(st.session_state.messages)
        
        # Get AI response
        ai_response = self.language_processor.get_ai_response(
            message_content,
            st.session_state.target_language,
            st.session_state.chat_mode,
            st.session_state.role_play_scenario
        )
        
        if ai_response:
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            st.session_state.last_message_count = len(st.session_state.messages)

    def display_chat_interface(self):
        """Display the main chat interface."""
        st.header(f"Chatting in {st.session_state.target_language}")
        if st.session_state.chat_mode == "Role Play":
            st.subheader(f"Scenario: {st.session_state.role_play_scenario}")

        # Display chat messages
        for i, message in enumerate(st.session_state.messages):
            message_key = f"msg_{i}"
            self.display_message(message, message_key, is_user_message=message["role"]=="user")

        # Handle audio input
        self.handle_audio_input()

        # Text input
        if prompt := st.chat_input("Type your message..."):
            self.handle_new_message(prompt)
            st.rerun()

