from openai import OpenAI
import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import wikipedia
from dotenv import load_dotenv
import random
import re

# ✅ Load OpenRouter API key from .env
load_dotenv()

# ✅ Setup OpenRouter client
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


# ✅ Speak text aloud + terminal print
def say(text):
    print(f"🗣️ Jarvis: {text}")

    word_count = len(text.split())
    if word_count > 50:
        print("📢 Skipping voice (response too long)")
        return

    engine = pyttsx3.init()
    engine.setProperty("rate", 160)
    engine.say(text)
    engine.runAndWait()


# 🎤 Voice command
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("🧠 Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"🗣️ You said: {query}")
        return query.lower()
    except sr.UnknownValueError:

        return "__silent__"
    except:
        print("❌ Sorry, I didn't catch that.")
        return ""


# 📁 Save prompt + response
def save_conversation(prompt, response):
    if not os.path.exists("OpenRouterChats"):
        os.makedirs("OpenRouterChats")

    filename = re.sub(r'[\\/*?:"<>|]', "", prompt[:40])
    filename = f"OpenRouterChats/{filename}_{random.randint(1000, 9999)}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"User: {prompt}\n\nAssistant: {response}\n")


# 🤖 Ask OpenRouter (with conditional save)
def ask_openrouter(prompt, save=False):
    try:
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[{"role": "user", "content": prompt}],
            # max_tokens=80,  # 🟡 Limit reply length to ~60-80 words
            temperature=0.7
        )
        reply = response.choices[0].message.content
        if save:
            save_conversation(prompt, reply)
        return reply
    except Exception as e:
        return f"Error: {e}"


# ⏸️ Pause after opening apps
def pause_until_enter():
    input("⏸️ Press Enter to continue Jarvis...")


# 🚀 Main loop
if __name__ == "__main__":
    say("Hello Meghna, I am your AI assistant. How can I help you?")

    while True:
        query = take_command()

        if "wikipedia" in query:
            webbrowser.open("https://www.wikipedia.com")
            say("Opening Wikipedia.")
            pause_until_enter()

        elif "open youtube" in query:
            webbrowser.open("https://www.youtube.com")
            say("Opening YouTube.")
            pause_until_enter()

        elif "open google" in query:
            webbrowser.open("https://www.google.com")
            say("Opening Google.")
            pause_until_enter()

        elif "open code" in query:
            code_path = "C:\\Users\\YourUsername\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(code_path)
            say("Opening Visual Studio Code.")
            pause_until_enter()

        elif "time" in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            say(f"The time is {current_time}")
            pause_until_enter()

        elif "exit" in query or "bye" in query or "stop" in query:
            say("Goodbye Meghna! Have a great day.")
            break

        elif query == "__silent__":
            input("⏸️ No voice detected. Press Enter to wake me up...")

        elif query != "":
            save = "using artificial intelligence" in query
            response = ask_openrouter(query, save=save)
            say(response)

