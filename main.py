#pip install SpeechRecognition pyttsx3 pyaudiopip install SpeechRecognition pyttsx3 pyaudio
import speech_recognition as sr   #захват речи в текст
import pyttsx3             #текст в речь      
import sys                     
def init_engine(): #настройка речи
    engine = pyttsx3.init() #движок речи
    voices = engine.getProperty('voices')
    russian_voice = None
    for voice in voices:
        if 'russian' in voice.name.lower() or 'russian' in getattr(voice, 'id', '').lower():
            russian_voice = voice.id
            break
    engine.setProperty('voice', russian_voice if russian_voice else voices[0].id) #выбрали
    engine.setProperty('rate', 180)  # слова в минуту
    return engine

def speak(engine, text): #произнос текста
    print(f"[Голос]: {text}")
    engine.say(text)
    engine.runAndWait()