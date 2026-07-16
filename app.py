# app_simple.py - Simplified version without audio recording
import streamlit as st
import datetime
import webbrowser
import requests
import wikipedia

st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="centered")

st.title("🤖 AI Assistant")
st.markdown("### Your Virtual Companion")

# Assistant class (simplified)
class SimpleAssistant:
    def __init__(self, name="Jarvis"):
        self.name = name
    
    def process(self, command):
        command = command.lower()
        
        if 'time' in command:
            return datetime.datetime.now().strftime("%I:%M %p")
        elif 'date' in command:
            return datetime.datetime.now().strftime("%B %d, %Y")
        elif 'weather' in command:
            city = command.replace('weather', '').strip() or 'London'
            try:
                response = requests.get(f"https://wttr.in/{city}?format=3")
                return response.text
            except:
                return "Weather service unavailable"
        elif 'search' in command:
            query = command.replace('search', '').strip()
            webbrowser.open(f"https://google.com/search?q={query}")
            return f"Searching for: {query}"
        elif 'joke' in command:
            import random
            jokes = ["Why don't programmers like nature? Too many bugs!", 
                    "What's a computer's favorite snack? Microchips!"]
            return random.choice(jokes)
        else:
            try:
                return wikipedia.summary(command, sentences=1)
            except:
                return f"I heard: {command}. Try asking about time, weather, or search for something."

# Initialize
assistant = SimpleAssistant()

# Chat interface
user_input = st.text_input("Type your command:")

if user_input:
    response = assistant.process(user_input)
    st.success(f"**Assistant:** {response}")
    
    # Text-to-speech button
    if st.button("🔊 Speak Response"):
        from gtts import gTTS
        import io
        tts = gTTS(text=response, lang='en')
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        st.audio(audio_bytes, format='audio/mp3')

# Quick buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🕐 Time"): st.info(assistant.process("time"))
with col2:
    if st.button("🌤 Weather"): st.info(assistant.process("weather London"))
with col3:
    if st.button("😂 Joke"): st.info(assistant.process("joke"))
