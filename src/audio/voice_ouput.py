from gtts import gTTS
import base64
import streamlit as st



class tts_processor:
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
        target_language = st.session_state.target_language
        self.language = self.LANGUAGE_CODES.get(target_language)

    def autoplay_audio(self, file_path: str):
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio controls autoplay="true">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            st.markdown(
                md,
                unsafe_allow_html=True,
            )

    def text_to_voice(self, text, filename="src/audio/output.mp3"):
        # Create a gTTS object
        tts = gTTS(text=text, lang=self.language, slow=False, tld="co.uk")
    
        # Save the audio file
        tts.save(filename)
        #self.autoplay_audio(filename)

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

def text_to__voice(text, filename="output.mp3", language="pl"):
    # Create a gTTS object
    tts = gTTS(text=text, lang=language, slow=False, tld="co.uk")
 
    # Save the audio file
    tts.save(filename)
    autoplay_audio(filename)
