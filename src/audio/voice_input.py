import streamlit as st
import whisper
from streamlit_mic_recorder import mic_recorder
import tempfile
import os
import numpy as np

@st.cache_resource
def load_whisper_model():
    """Load and cache the Whisper model."""
    return whisper.load_model("base", device="cpu")

class VoiceProcessor:
    # Language codes mapping for Whisper
    LANGUAGE_CODES = {
        "Spanish": "es",
        "French": "fr",
        "German": "de",
        "Italian": "it",
        "Japanese": "ja",
        "Mandarin Chinese": "zh",
        "Polish": "pl",
        "Russian": "ru"
    }

    def __init__(self):
        self.model = load_whisper_model()

    def transcribe_audio(self, audio_bytes):
        """Transcribe recorded audio using Whisper with the target language."""
        if not audio_bytes:
            return None
            
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            tmpfile.write(audio_bytes)
            tmpfile.flush()
            
            try:
                target_language = st.session_state.target_language
                language_code = self.LANGUAGE_CODES.get(target_language)
                
                result = self.model.transcribe(
                    tmpfile.name,
                    language=language_code,
                    task="transcribe"
                )
                return result["text"].strip()
            except Exception as e:
                st.error(f"Error transcribing audio: {str(e)}")
                return None
            finally:
                os.unlink(tmpfile.name)

    def get_audio_recorder(self):
        """Return the mic recorder component and handle audio processing."""
        audio = mic_recorder(
            start_prompt="🎤 Start Recording",
            stop_prompt="⏹️ Stop Recording",
            just_once=False,
            use_container_width=False,
            format="wav",
            key="recorder"
        )
        return audio