# Language Learning Chat App 🌍

A Python-based language learning application that lets you practice different languages by chatting with an AI language partner. You can engage in free conversations or participate in role-play scenarios to improve your language skills.

## Features

- Support for multiple languages (Spanish, French, German, Italian, Japanese, Mandarin Chinese)
- Two chat modes:
  - Free Conversation: Chat about any topic you want
  - Role Play: Practice specific scenarios like ordering at a restaurant or buying train tickets
- Real-time language corrections
- Interactive web interface

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Running the App

To start the application, run:

```bash
streamlit run app.py
```

The app will open in your default web browser. From there, you can:

1. Select your target language
2. Choose between free conversation or role-play mode
3. Start chatting and practicing!
