#pip install SpeechRecognition pyttsx3 pyaudiopip install SpeechRecognition pyttsx3 pyaudio
import speech_recognition as sr   #захват речи в текст
import pyttsx3             #текст в речь      
import sys                     
def speech_engine(): #настройка речи
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

def format_result(value):
    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))  # 5.0 → "5"
        else:
            
            rounded = round(value, 6)
            formatted = f"{rounded:.6f}".rstrip('0').rstrip('.')
            return formatted
    return str(value)
def calculate(tokens):
    
    if not tokens or len(tokens) % 2 == 0: 
        return None
    if not isinstance(tokens[0], (int, float)):
        return None

    processed = [tokens[0]]
    i = 1
    while i < len(tokens):
        op = tokens[i]
        next_val = tokens[i + 1]
        
        if not isinstance(next_val, (int, float)):
            return None
        
        if op == '*':
            processed[-1] *= next_val
        elif op == '/':
            if next_val == 0:
                return "деление_на_ноль"
            processed[-1] /= next_val
        else:
            
            processed.append(op)
            processed.append(next_val)
        i += 2
    result = processed[0]
    i = 1
    while i < len(processed):
        op = processed[i]
        next_val = processed[i + 1]
        if op == '+':
            result += next_val
        elif op == '-':
            result -= next_val
        else:
            return None  
        i += 2

    return result
def parse_voice_input(text): #парсинг речи
    
    clean_text = text.lower()
    for prefix in ["посчитай", "посчитать"]: #оставили ток выражение
        if clean_text.startswith(prefix):
            clean_text = clean_text[len(prefix):].strip()
            break
    
    words = clean_text.split()
    tokens = [] 
    i = 0

    word_to_op = {
        'плюс': '+', 'минус': '-', 'умножить': '*', 'разделить': '/','+': '+', '-': '-', '*': '*', '/': '/', 'x': '*', 'х': '*'   }

    while i < len(words):
        word = words[i]

        try:
            num_str = word.replace(',', '.')  # "1,5" → "1.5"
            tokens.append(float(num_str))
            i += 1
            continue
        except ValueError:
            pass

        if word == "умножить" and i + 1 < len(words) and words[i + 1] == "на":
            tokens.append('*')
            i += 2
            continue
        if word == "разделить" and i + 1 < len(words) and words[i + 1] == "на":
            tokens.append('/')
            i += 2
            continue

        if word in word_to_op:
            tokens.append(word_to_op[word])
            i += 1
            continue
        i += 1

    return tokens

