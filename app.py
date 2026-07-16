import streamlit as st
import datetime
import webbrowser
import os
import pyautogui
import time
import wikipedia
import requests
import json
from plyer import notification
import pywhatkit
import base64
from gtts import gTTS
import io
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr

# Page configuration
st.set_page_config(
    page_title="AI Assistant - Your Virtual Companion",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for phone-like interface
st.markdown("""
<style>
    .phone-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 30px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }
    .assistant-header {
        text-align: center;
        color: white;
        padding: 20px 0;
    }
    .assistant-name {
        font-size: 24px;
        font-weight: bold;
        margin: 10px 0;
    }
    .status-dot {
        height: 10px;
        width: 10px;
        background-color: #4CAF50;
        border-radius: 50%;
        display: inline-block;
        margin-right: 5px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    .output-box {
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        color: white;
        min-height: 100px;
    }
    .stButton button {
        width: 100%;
        border-radius: 25px;
        background: white;
        color: #667eea;
        font-weight: bold;
        border: none;
        padding: 10px;
        margin: 5px 0;
    }
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        padding: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'assistant_name' not in st.session_state:
    st.session_state.assistant_name = "Jarvis"
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'listening' not in st.session_state:
    st.session_state.listening = False

class StreamlitAIAssistant:
    def __init__(self, name="Jarvis"):
        self.assistant_name = name
        
    def speak_text(self, text):
        """Convert text to speech"""
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            return audio_bytes
        except:
            return None
    
    def get_time(self):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The time is {current_time}"
    
    def get_date(self):
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        return f"Today is {current_date}"
    
    def get_weather(self, city):
        try:
            response = requests.get(f"https://wttr.in/{city}?format=3")
            if response.status_code == 200:
                return response.text
            return "Could not get weather information"
        except:
            return "Could not connect to weather service"
    
    def search_wikipedia(self, query):
        try:
            result = wikipedia.summary(query, sentences=2)
            return result
        except:
            return "Could not find information on Wikipedia"
    
    def process_text_command(self, command):
        """Process text commands"""
        command = command.lower().strip()
        
        # Greetings
        if any(word in command for word in ['hello', 'hi', 'hey']):
            return f"Hello! I'm {self.assistant_name}, your AI assistant. How can I help you?"
        
        # Time
        elif 'time' in command:
            return self.get_time()
        
        # Date
        elif 'date' in command:
            return self.get_date()
        
        # Weather
        elif 'weather' in command:
            city = command.replace('weather', '').replace('in', '').replace('of', '').strip()
            if not city:
                city = "New York"
            return self.get_weather(city)
        
        # Wikipedia
        elif 'who is' in command or 'what is' in command or 'tell me about' in command:
            search_query = command.replace('who is', '').replace('what is', '').replace('tell me about', '').strip()
            return self.search_wikipedia(search_query)
        
        # Change name
        elif 'change name to' in command:
            new_name = command.replace('change name to', '').strip()
            st.session_state.assistant_name = new_name
            self.assistant_name = new_name
            return f"Okay! You can now call me {new_name}"
        
        # Name query
        elif 'your name' in command or 'who are you' in command:
            return f"My name is {self.assistant_name}. I'm your AI assistant!"
        
        # Search web
        elif 'search for' in command or 'search' in command:
            search_query = command.replace('search for', '').replace('search', '').strip()
            if search_query:
                webbrowser.open(f"https://www.google.com/search?q={search_query}")
                return f"Searching Google for: {search_query}"
        
        # YouTube
        elif 'play' in command and 'youtube' in command:
            video = command.replace('play', '').replace('youtube', '').replace('on', '').strip()
            if video:
                pywhatkit.playonyt(video)
                return f"Playing {video} on YouTube"
        
        # Calculator
        elif 'calculate' in command or 'calculator' in command:
            try:
                expression = command.replace('calculate', '').replace('calculator', '').strip()
                result = eval(expression)
                return f"The result is: {result}"
            except:
                return "Could not calculate. Please try a valid expression."
        
        # Fun responses
        elif 'joke' in command:
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the AI go to therapy? It had too many deep learning issues!",
                "What do you call a computer that sings? A Dell!"
            ]
            import random
            return random.choice(jokes)
        
        elif 'thank' in command:
            return f"You're welcome! {self.assistant_name} at your service!"
        
        else:
            return f"I heard: '{command}'. You can ask me about time, date, weather, or search Wikipedia. Say 'help' for more options."

# Main App Interface
def main():
    # Phone-like container
    st.markdown('<div class="phone-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown(f"""
    <div class="assistant-header">
        <h1>🤖</h1>
        <div class="assistant-name">
            <span class="status-dot"></span>
            {st.session_state.assistant_name}
        </div>
        <p style="color: rgba(255,255,255,0.8);">Your AI Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize assistant
    assistant = StreamlitAIAssistant(st.session_state.assistant_name)
    
    # Chat output area
    st.markdown('<div class="output-box">', unsafe_allow_html=True)
    if st.session_state.chat_history:
        for chat in st.session_state.chat_history[-5:]:  # Show last 5 messages
            if chat['type'] == 'user':
                st.markdown(f"**You:** {chat['text']}")
            else:
                st.markdown(f"**{st.session_state.assistant_name}:** {chat['text']}")
                # Add audio playback
                audio_bytes = assistant.speak_text(chat['text'])
                if audio_bytes:
                    st.audio(audio_bytes, format='audio/mp3', label='🔊 Listen')
    else:
        st.markdown(f"**{st.session_state.assistant_name}:** Hello! I'm ready to help. Type a message or use the voice button.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick action buttons
    st.markdown('<div class="feature-grid">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🕐 Time", use_container_width=True):
            response = assistant.get_time()
            st.session_state.chat_history.append({"type": "user", "text": "What's the time?"})
            st.session_state.chat_history.append({"type": "assistant", "text": response})
            st.rerun()
    
    with col2:
        if st.button("🌤 Weather", use_container_width=True):
            response = assistant.get_weather("New York")
            st.session_state.chat_history.append({"type": "user", "text": "What's the weather?"})
            st.session_state.chat_history.append({"type": "assistant", "text": response})
            st.rerun()
    
    with col3:
        if st.button("😂 Joke", use_container_width=True):
            response = assistant.process_text_command("joke")
            st.session_state.chat_history.append({"type": "user", "text": "Tell me a joke"})
            st.session_state.chat_history.append({"type": "assistant", "text": response})
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Text input
    user_input = st.text_input("", placeholder="Type your message here...", key="text_input", label_visibility="collapsed")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("📤 Send", use_container_width=True):
            if user_input:
                st.session_state.chat_history.append({"type": "user", "text": user_input})
                response = assistant.process_text_command(user_input)
                st.session_state.chat_history.append({"type": "assistant", "text": response})
                st.rerun()
    
    # Voice input section
    st.markdown("---")
    st.markdown("**🎤 Voice Input**")
    
    # Record audio
    audio_data = mic_recorder(
        start_prompt="Start Recording",
        stop_prompt="Stop Recording",
        just_once=True,
        key='mic_recorder'
    )
    
    if audio_data:
        try:
            # Process recorded audio
            recognizer = sr.Recognizer()
            audio_bytes = audio_data['bytes']
            
            with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
                audio = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio)
                    st.success(f"Recognized: {text}")
                    
                    st.session_state.chat_history.append({"type": "user", "text": text})
                    response = assistant.process_text_command(text)
                    st.session_state.chat_history.append({"type": "assistant", "text": response})
                    st.rerun()
                    
                except sr.UnknownValueError:
                    st.error("Could not understand audio")
                except sr.RequestError:
                    st.error("Speech recognition service error")
                    
        except Exception as e:
            st.error(f"Error processing audio: {str(e)}")
    
    # Settings
    with st.expander("⚙️ Settings"):
        new_name = st.text_input("Change Assistant Name:", st.session_state.assistant_name)
        if st.button("Update Name"):
            if new_name:
                st.session_state.assistant_name = new_name
                st.success(f"Assistant name updated to {new_name}!")
                st.rerun()
        
        st.info("""
        **Available Commands:**
        - Time, Date queries
        - Weather [city name]
        - Who is / What is [anything]
        - Search for [anything]
        - Play [song] on YouTube
        - Calculate [expression]
        - Tell me a joke
        - Change name to [name]
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close phone container

if __name__ == "__main__":
    main()
