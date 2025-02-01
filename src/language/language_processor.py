import streamlit as st
import openai

class LanguageProcessor:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key

    def get_ai_response(self, prompt, target_language, chat_mode, role_play_scenario=None):
        """Get AI response for the conversation."""
        try:
            system_prompt = f"You are a native {target_language} speaker having a conversation. "
            if chat_mode == "Role Play":
                system_prompt += f"""We are role-playing the following scenario: {role_play_scenario}. 
                Start the conversation in a natural way that fits the scenario. 
                In every response you make:
                1. Stay in character for the scenario
                2. Always end with a question to keep the conversation going
                3. Keep your responses focused on the scenario context"""
            system_prompt += f"\nRespond naturally in {target_language}."

            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(st.session_state.messages)
            messages.append({"role": "user", "content": prompt})

            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"Error getting AI response: {str(e)}")
            return None

    def get_corrections(self, message, target_language):
        """Get language corrections for user message."""
        try:
            system_prompt = f"""You are a helpful language teacher. Analyze the following message in {target_language} and provide corrections.
            Format your response as follows:
            1. First, list any grammar, vocabulary, or pronunciation mistakes
            2. Then provide the corrected version of the full message
            3. Finally, give a brief explanation of the corrections
            Keep your response concise and friendly."""

            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"Error getting corrections: {str(e)}")
            return None

    def get_translation(self, message, target_language):
        """Translate message to English."""
        try:
            system_prompt = f"""You are a translator. Translate the following message from {target_language} to English.
            Provide only the direct translation, no explanations."""

            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=0.3,
            )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"Error getting translation: {str(e)}")
            return None 