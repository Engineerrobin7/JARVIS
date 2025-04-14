import pyttsx3
import pyautogui
import psutil
import pyjokes
import speech_recognition as sr
import json
import requests
import geocoder
from difflib import get_close_matches

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Get location data
g = geocoder.ip('me')
if not g.latlng:
    speak("Unable to fetch your location. Please check your internet connection.")
    print("Error: Unable to fetch geolocation data.")

# Load dictionary data
data = json.load(open('data.json'))

def speak(audio) -> None:
    """Speak the given text."""
    engine.say(audio)
    engine.runAndWait()

def screenshot() -> None:
    """Take a screenshot and save it."""
    img = pyautogui.screenshot()
    img.save('screenshot.png')  # Save to the current directory

def cpu() -> None:
    """Provide CPU usage and battery status."""
    usage = str(psutil.cpu_percent())
    speak("CPU is at " + usage + " percent")
    battery = psutil.sensors_battery()
    speak("Battery is at " + str(battery.percent) + " percent")

def joke() -> None:
    """Tell a joke."""
    speak(pyjokes.get_joke())

def takeCommand() -> str:
    """Listen to the user's voice command and return it as text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        r.energy_threshold = 494
        r.adjust_for_ambient_noise(source, duration=1.5)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("Listening timed out. Please try again.")
            return ""

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        print(f'User said: {query}\n')
        return query
    except sr.UnknownValueError:
        print('Sorry, I did not understand that.')
        speak('Sorry, I did not understand that.')
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        speak("Could not request results. Please check your internet connection.")
        return ""

def weather():
    """Fetch and speak the current weather information."""
    if not g.latlng:
        speak("Unable to fetch your location. Please check your internet connection.")
        return

    api_url = f"https://fcc-weather-api.glitch.me/api/current?lat={g.latlng[0]}&lon={g.latlng[1]}"

    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code != 200:
            speak("Unable to fetch weather data. Please try again later.")
            return

        data_json = response.json()
        if 'main' not in data_json or 'weather' not in data_json:
            speak("Invalid weather data received.")
            return

        main = data_json.get('main', {})
        weather_desc = data_json.get('weather', [{}])[0]
        temp = main.get('temp', 'unknown')
        description = weather_desc.get('main', 'unknown')
        speak(f"Temperature: {temp}°C, Weather: {description}")

    except requests.exceptions.RequestException as e:
        speak("There was an error connecting to the weather service.")
        print(f"RequestException: {e}")
    except json.JSONDecodeError:
        speak("Unable to decode the weather data.")

def translate(word):
    """Translate a word using the dictionary data."""
    word = word.lower()
    if word in data:
        speak(data[word])
    elif len(get_close_matches(word, data.keys())) > 0:
        x = get_close_matches(word, data.keys())[0]
        speak('Did you mean ' + x + ' instead? Respond with Yes or No.')
        ans = takeCommand().lower()
        if 'yes' in ans:
            speak(data[x])
        elif 'no' in ans:
            speak("Word doesn't exist. Please make sure you spelled it correctly.")
        else:
            speak("We didn't understand your entry.")
    else:
        speak("Word doesn't exist. Please double-check it.")
