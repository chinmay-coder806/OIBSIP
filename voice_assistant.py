import datetime
import sys
import webbrowser

import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()
engine.setProperty("rate", 175)

recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8


def speak(text: str) -> None:
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()


def list_microphones() -> None:
    print("Available microphones:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"  [{index}] {name}")


def listen(mic_index=None) -> str:
    with sr.Microphone(device_index=mic_index) as source:
        print("\nCalibrating for background noise... please stay quiet.")
        recognizer.adjust_for_ambient_noise(source, duration=1.5)
        print("Listening... (speak clearly now)")
        try:
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Please try again.")
            return ""

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you please repeat, "
              "speaking a little slower and closer to the microphone?")
        return ""
    except sr.RequestError:
        speak("I'm having trouble reaching the speech recognition service. "
              "Please check your internet connection.")
        return ""


def handle_command(command: str) -> bool:
    if not command:
        return True

    if "hello" in command or "hi " in command or command.strip() == "hi":
        speak("Hello there! How can I help you today?")

    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}.")

    elif "date" in command:
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today's date is {today}.")

    elif "search" in command:
        query = command.replace("search for", "").replace("search", "").strip()
        if query:
            speak(f"Searching the web for {query}.")
            webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        else:
            speak("What would you like me to search for?")

    elif "exit" in command or "quit" in command or "stop" in command:
        speak("Goodbye! Have a great day.")
        return False

    else:
        speak("I'm not sure how to help with that yet. "
              "You can ask me to say hello, tell the time or date, "
              "or search the web for something.")

    return True


def main() -> None:
    speak("Voice assistant is ready. Say 'hello' to get started, "
          "or say 'exit' anytime to quit.")

    running = True
    consecutive_failures = 0

    while running:
        command = listen()

        if not command:
            consecutive_failures += 1
            # fallback to typed input after repeated misrecognition
            if consecutive_failures >= 3:
                speak("I'm having trouble hearing you. "
                      "You can type your command instead, or press Enter to keep trying by voice.")
                typed = input("Type a command (or press Enter to try voice again): ").strip().lower()
                if typed:
                    command = typed
                consecutive_failures = 0
            else:
                continue
        else:
            consecutive_failures = 0

        running = handle_command(command)


if __name__ == "__main__":
    # python voice_assistant.py --list-mics  -> find your mic's device index
    if "--list-mics" in sys.argv:
        list_microphones()
    else:
        main()
