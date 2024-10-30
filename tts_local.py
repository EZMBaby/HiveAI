import pyttsx3


def speak(text):
    engine = pyttsx3.init()

    rate = engine.getProperty('rate')
    engine.setProperty('rate', float(rate) * 1.15)
    voice = engine.getProperty('voices')
    engine.setProperty('voice', voice[0].id)

    engine.say(text)
    engine.runAndWait()
