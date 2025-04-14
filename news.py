import requests
import json
import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    """Speak the given text."""
    engine.say(audio)
    engine.runAndWait()

def speak_news():
    """Fetch and speak the latest news headlines."""
    # Replace 'yourapikey' with your actual NewsAPI key
    api_key = "7bc72613dc62422796aa78f7eecc18af"
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"

    try:
        # Fetch news data from NewsAPI
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Error: Unable to fetch news. HTTP Status Code: {response.status_code}")
            speak("I am unable to fetch the news at the moment. Please try again later.")
            return

        # Parse the JSON response
        news_dict = response.json()
        if news_dict.get('status') != 'ok':
            print(f"Error: {news_dict.get('message', 'Unknown error')}")
            speak("I couldn't fetch the news. Please check the API key or try again later.")
            return

        # Check if articles are available
        if 'articles' not in news_dict or not news_dict['articles']:
            print("Error: No articles found in the news response.")
            speak("I couldn't find any news articles at the moment. Please try again later.")
            return

        # Speak the news headlines
        arts = news_dict['articles']
        speak('Source: NewsAPI')
        speak('Today\'s Headlines are..')
        for i, article in enumerate(arts[:5], start=1):  # Limit to 5 articles
            speak(f"News {i}: {article['title']}")
            print(f"News {i}: {article['title']}")
            if i < len(arts[:5]):
                speak('Moving on to the next news headline..')
        speak('These were the top headlines. Have a nice day, Sir!')

    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        speak("There was an error connecting to the news service.")
    except Exception as e:
        print(f"Unexpected Error: {e}")
        speak("An unexpected error occurred while fetching the news.")

def getNewsUrl():
    """Return the URL for the news source."""
    return 'https://newsapi.org/v2/top-headlines?country=in&apiKey=yourapikey'

if __name__ == '__main__':
    speak_news()
