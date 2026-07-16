import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import subprocess
import pyautogui
import time
import wikipedia
import requests
import json
from plyer import notification
import pywhatkit
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class AIAssistant:
    def __init__(self, assistant_name="Jarvis"):
        """
        Initialize AI Assistant with customizable name
        """
        self.assistant_name = assistant_name
        self.engine = pyttsx3.init()
        self.setup_voice()
        
    def setup_voice(self):
        """Setup voice properties"""
        voices = self.engine.getProperty('voices')
        # Use female voice (index 1) or male voice (index 0)
        self.engine.setProperty('voice', voices[1].id)
        self.engine.setProperty('rate', 180)  # Speed of speech
        self.engine.setProperty('volume', 0.9)  # Volume level
        
    def speak(self, text):
        """Text to speech conversion"""
        print(f"{self.assistant_name}: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
        
    def listen(self):
        """Listen for voice commands"""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print(f"\n{self.assistant_name} is listening...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            recognizer.pause_threshold = 1
            
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                print("Processing...")
                query = recognizer.recognize_google(audio, language='en-US')
                print(f"You said: {query}")
                return query.lower()
            except sr.WaitTimeoutError:
                print("Listening timeout...")
                return ""
            except sr.UnknownValueError:
                print("Could not understand audio")
                return ""
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                return ""
    
    def get_time(self):
        """Get current time"""
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The time is {current_time}"
    
    def get_date(self):
        """Get current date"""
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        return f"Today is {current_date}"
    
    def open_application(self, app_name):
        """Open applications on computer (like phone apps)"""
        apps = {
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'paint': 'mspaint.exe',
            'chrome': 'chrome.exe',
            'camera': 'start microsoft.windows.camera:',
            'settings': 'ms-settings:',
            'music': 'start mswindowsmusic:',
            'photos': 'start ms-photos:',
            'calendar': 'start outlookcal:',
            'mail': 'start outlookmail:'
        }
        
        try:
            if app_name in apps:
                os.system(apps[app_name])
                return f"Opening {app_name}"
            else:
                # Try to open from start menu
                os.system(f'start {app_name}')
                return f"Trying to open {app_name}"
        except:
            return f"Sorry, I couldn't open {app_name}"
    
    def control_volume(self, action):
        """Control system volume like phone volume buttons"""
        try:
            if action == 'up':
                for _ in range(5):  # Increase volume 5 steps
                    pyautogui.press('volumeup')
                return "Volume increased"
            elif action == 'down':
                for _ in range(5):  # Decrease volume 5 steps
                    pyautogui.press('volumedown')
                return "Volume decreased"
            elif action == 'mute':
                pyautogui.press('volumemute')
                return "Volume muted"
        except:
            return "Could not control volume"
    
    def take_screenshot(self):
        """Take screenshot like phone screenshot"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            pyautogui.screenshot(filename)
            return f"Screenshot saved as {filename}"
        except:
            return "Could not take screenshot"
    
    def send_notification(self, title, message):
        """Send desktop notification like phone notification"""
        try:
            notification.notify(
                title=title,
                message=message,
                timeout=5
            )
            return "Notification sent"
        except:
            return "Could not send notification"
    
    def search_web(self, query):
        """Search the web"""
        try:
            pywhatkit.search(query)
            return f"Searching for {query}"
        except:
            return "Could not search the web"
    
    def play_youtube(self, video):
        """Play YouTube video"""
        try:
            pywhatkit.playonyt(video)
            return f"Playing {video} on YouTube"
        except:
            return "Could not play video"
    
    def get_weather(self, city):
        """Get weather information"""
        try:
            # Using wttr.in free weather API
            response = requests.get(f"https://wttr.in/{city}?format=3")
            if response.status_code == 200:
                return response.text
            return "Could not get weather"
        except:
            return "Could not connect to weather service"
    
    def send_email(self, to, subject, body):
        """Send email (configure with your email credentials)"""
        try:
            # Configure these settings
            sender_email = "your_email@gmail.com"
            sender_password = "your_app_password"  # Use App Password
            
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = to
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            return "Email sent successfully"
        except:
            return "Could not send email"
    
    def process_command(self, query):
        """Process voice commands"""
        
        # Greetings
        if any(greeting in query for greeting in ['hello', 'hi', 'hey']):
            return f"Hello! How can I help you today?"
        
        # Time and Date
        elif 'time' in query:
            return self.get_time()
        elif 'date' in query:
            return self.get_date()
        
        # Open applications
        elif 'open' in query:
            app = query.replace('open', '').strip()
            return self.open_application(app)
        
        # Volume control (like phone volume buttons)
        elif 'volume up' in query or 'increase volume' in query:
            return self.control_volume('up')
        elif 'volume down' in query or 'decrease volume' in query:
            return self.control_volume('down')
        elif 'mute' in query:
            return self.control_volume('mute')
        
        # Screenshot (like phone screenshot)
        elif 'screenshot' in query or 'capture screen' in query:
            return self.take_screenshot()
        
        # Web search
        elif 'search for' in query or 'google' in query:
            search_query = query.replace('search for', '').replace('google', '').strip()
            return self.search_web(search_query)
        
        # YouTube
        elif 'play' in query and 'youtube' in query:
            video = query.replace('play', '').replace('youtube', '').replace('on', '').strip()
            return self.play_youtube(video)
        
        # Weather
        elif 'weather' in query:
            city = query.replace('weather', '').replace('in', '').replace('what is the', '').strip()
            if not city:
                city = 'New York'  # Default city
            return self.get_weather(city)
        
        # Wikipedia
        elif 'wikipedia' in query or 'who is' in query or 'what is' in query:
            try:
                search_query = query.replace('wikipedia', '').replace('who is', '').replace('what is', '').strip()
                result = wikipedia.summary(search_query, sentences=2)
                return result
            except:
                return "Could not find information"
        
        # Notifications
        elif 'remind me' in query:
            reminder = query.replace('remind me', '').replace('to', '').strip()
            self.send_notification("Reminder", reminder)
            return f"I'll remind you to {reminder}"
        
        # System commands (like phone power button)
        elif 'lock' in query or 'sleep' in query:
            os.system("rundll32.exe user32.dll,LockWorkStation")
            return "Locking the system"
        
        elif 'shutdown' in query:
            return "Shutting down in 10 seconds. Say 'cancel shutdown' to cancel."
        
        elif 'cancel shutdown' in query:
            os.system("shutdown /a")
            return "Shutdown cancelled"
        
        # Name customization
        elif 'change your name to' in query:
            new_name = query.replace('change your name to', '').strip()
            self.assistant_name = new_name
            return f"Okay, you can now call me {new_name}"
        
        elif 'what is your name' in query or 'who are you' in query:
            return f"My name is {self.assistant_name}. I'm your AI assistant!"
        
        # Exit
        elif 'goodbye' in query or 'exit' in query or 'stop' in query:
            return "Goodbye! Have a great day!"
        
        else:
            return "I'm not sure how to help with that. Can you please repeat?"
    
    def run(self):
        """Main loop for the assistant"""
        greeting = f"Hello! I am {self.assistant_name}, your AI assistant. How can I help you?"
        self.speak(greeting)
        
        while True:
            query = self.listen()
            
            if query:
                response = self.process_command(query)
                
                if response:
                    self.speak(response)
                    
                    if 'goodbye' in response.lower():
                        break
                
                time.sleep(1)  # Small pause between commands

# Main execution
if __name__ == "__main__":
    print("=" * 50)
    print("    AI ASSISTANT - Your Virtual Companion")
    print("=" * 50)
    
    # Customize your assistant name here
    assistant_name = input("Enter your assistant's name (default: Jarvis): ").strip()
    
    if not assistant_name:
        assistant_name = "Jarvis"
    
    print(f"\nStarting {assistant_name}...")
    print("Say 'hello' to begin, 'goodbye' to exit")
    print("-" * 50)
    
    # Create and run your AI assistant
    my_assistant = AIAssistant(assistant_name)
    
    try:
        my_assistant.run()
    except KeyboardInterrupt:
        print(f"\n{assistant_name}: Goodbye!")
    except Exception as e:
        print(f"Error: {e}")
