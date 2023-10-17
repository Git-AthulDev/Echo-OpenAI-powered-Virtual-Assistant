import speech_recognition as sr
import datetime
import webbrowser
import win32com.client
import subprocess
import openai
from config import apikey
from pathlib import Path
import requests


def get_weather(city):
    api_key = "[Your API key]"
    base_url = "https://api.weatherapi.com/v1/current.json"
    params = {
        "key": api_key,
        "q": city
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if "error" in data:
        return f"Sorry, I couldn't fetch the weather information for {city}."
    else:
        weather_description = data["current"]["condition"]["text"]
        temperature = data["current"]["temp_c"]
        humidity = data["current"]["humidity"]
        return f"The weather in {city} is {weather_description}. The temperature is {temperature}°C, and the humidity is {humidity}%."

chatStr = ""
def chat(query):
    global chatStr
    openai.api_key = apikey
    chatStr += f"User: {query}\n Echo:"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}"
    return response["choices"][0]["text"]

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n ***************** \n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    text += response["choices"][0]["text"]
    directory = Path("Openai")

    if not directory.exists():
        directory.mkdir()

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)

def say(text):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-gb")
            print(f"user said: {query}")
            return query
        except Exception as e:
            return "Some error occurred. Sorry. "

if __name__ == '__main__':
    print('Welcome to Echo AI')
    say("Greetings")
    while True:
        print("listening ...")
        query = takeCommand()
        # todo: sites
        sites = [["youtube", "https://youtube.com"],
                 ["wikipedia", "https://wikipedia.com"],
                 ["google", "https://google.com"],
                 ["twitch", "https://twitch.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} now.")
                webbrowser.open(site[1])
        # todo: music player
        if "open music" in query:
            musicPath = r"C:\Users\YourName\Downloads\Imagine-Dragons-Whatever-It-Takes.mp3"
            say(f"Playing music now")
            subprocess.Popen(["start", musicPath], shell=True)

        elif " what's the time" in query:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"The time is {current_time}")

        # todo: applications
        elif "open figma" in query:
            subprocess.Popen(["figma.exe"], shell=True)

        elif "open calculator" in query:
            subprocess.Popen(["calc.exe"], shell=True)

        elif "open pycharm" in query:
            subprocess.Popen([r"E:\PyCharm Community Edition 2023.2.2\bin\pycharm64.exe"], shell=True)

        elif "using artificial intelligence".lower() in query.lower():
            ai(prompt=query)
 
        elif "what's the weather in" in query.lower():
            city = query.lower().split("in", 1)[-1].strip()
            weather_info = get_weather(city)
            say(weather_info)


        elif "Echo quit".lower() in query.lower():
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            print("Conversing ... ")
            chat(query)
