import pyttsx3
import wikipedia
import speech_recognition as sr
import webbrowser
import datetime
import os
import smtplib
from news import speak_news, getNewsUrl
from OCR import OCR
from diction import translate
from helpers import *
from youtube import youtube
from sys import platform
import requests

# Use environment variables for sensitive data
EMAIL = os.getenv('EMAIL')  # Set your email in environment variables
PASSWORD = os.getenv('PASSWORD')  # Set your email password in environment variables

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

class Jarvis:
    def __init__(self) -> None:
        if platform == "linux" or platform == "linux2":
            self.chrome_path = '/usr/bin/google-chrome'
        elif platform == "darwin":
            self.chrome_path = 'open -a /Applications/Google\ Chrome.app'
        elif platform == "win32":
            self.chrome_path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        else:
            print('Unsupported OS')
            exit(1)
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(self.chrome_path))

    def wishMe(self) -> None:
        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour < 12:
            speak("Good Morning SIR")
        elif hour >= 12 and hour < 18:
            speak("Good Afternoon SIR")
        else:
            speak('Good Evening SIR')

        try:
            weather()
        except Exception as e:
            speak("I am unable to fetch the weather information at the moment.")
            print(f"Weather Error: {e}")

        speak('I am JARVIS. Please tell me how can I help you SIR?')

    def sendEmail(self, to, content) -> None:
        try:
            if not EMAIL or not PASSWORD:
                speak("Email credentials are not set. Please configure them in environment variables.")
                return

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, to, content)
            server.close()
            speak('Email has been sent!')
        except Exception as e:
            speak('Sorry sir, Not able to send email at the moment')
            print(f"Email Error: {e}")

    def execute_query(self, query):
        if not query.strip():
            speak("I didn't catch that. Could you please repeat?")
            return

        if 'wikipedia' in query:
            speak('Searching Wikipedia....')
            query = query.replace('wikipedia', '')
            try:
                results = wikipedia.summary(query, sentences=2)
                speak('According to Wikipedia')
                print(results)
                speak(results)
            except Exception as e:
                speak("Sorry, I couldn't fetch information from Wikipedia.")
                print(f"Wikipedia Error: {e}")
        elif 'youtube downloader' in query:
            try:
                exec(open('youtube_downloader.py').read())
            except FileNotFoundError:
                speak("YouTube downloader script not found.")
        elif 'optical text recognition' in query or 'text recognition' in query:
            OCR()
        elif 'voice' in query:
            if 'female' in query:
                engine.setProperty('voice', voices[1].id)
            else:
                engine.setProperty('voice', voices[0].id)
            speak("Hello Sir, I have switched my voice. How is it?")
        elif 'open youtube' in query:
            webbrowser.get('chrome').open_new_tab('https://youtube.com')
            speak("Opening YouTube.")
        elif 'open amazon' in query:
            webbrowser.get('chrome').open_new_tab('https://amazon.com')
            speak("Opening Amazon.")
        elif 'cpu' in query:
            cpu()
        elif 'joke' in query:
            joke()
        elif 'screenshot' in query:
            speak("Taking screenshot")
            screenshot()
        elif 'open google' in query:
            webbrowser.get('chrome').open_new_tab('https://google.com')
            speak("Opening Google.")
        elif 'play music' in query:
            try:
                os.startfile("D:\\RoiNa.mp3")  # Replace with a valid path
                speak("Playing music.")
            except FileNotFoundError:
                speak("Music file not found. Please check the file path.")
        elif 'search youtube' in query:
            speak('What do you want to search on YouTube?')
            youtube_query = takeCommand()
            youtube(youtube_query)
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f'Sir, the time is {strTime}')
        elif 'search' in query:
            speak('What do you want to search for?')
            search = takeCommand()
            url = 'https://google.com/search?q=' + search
            webbrowser.get('chrome').open_new_tab(url)
            speak('Here is what I found for ' + search)
        elif 'location' in query:
            speak('What is the location?')
            location = takeCommand()
            url = 'https://google.nl/maps/place/' + location + '/&amp;'
            webbrowser.get('chrome').open_new_tab(url)
            speak('Here is the location ' + location)
        elif 'your master' in query:
            speak('Gaurav is my master. He created me a couple of days ago')
        elif 'your name' in query:
            speak('My name is JARVIS')
        elif 'who made you' in query:
            speak('I was created by my AI master in 2021')
        elif 'shutdown' in query:
            if platform == "win32":
                os.system('shutdown /p /f')
            elif platform == "linux" or platform == "linux2" or "darwin":
                os.system('poweroff')
        elif 'remember that' in query:
            speak("What should I remember, sir?")
            rememberMessage = takeCommand()
            speak("You asked me to remember: " + rememberMessage)
            with open('data.txt', 'w') as remember:
                remember.write(rememberMessage)
        elif 'do you remember anything' in query:
            try:
                with open('data.txt', 'r') as remember:
                    speak("You asked me to remember: " + remember.read())
            except FileNotFoundError:
                speak("I don't have anything to remember, sir.")
        elif 'news' in query:
            speak('Of course, sir.')
            speak_news()
            speak('Do you want to read the full news?')
            test = takeCommand()
            if 'yes' in test:
                speak('Ok Sir, Opening browser...')
                webbrowser.open(getNewsUrl())
                speak('You can now read the full news from this website.')
            else:
                speak('No Problem Sir')

if __name__ == '__main__':
    bot_ = Jarvis()
    bot_.wishMe()
    while True:
        query = takeCommand().lower()
        bot_.execute_query(query)
