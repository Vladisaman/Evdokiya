# This is a sample Python script.
import time
from concurrent.futures.thread import ThreadPoolExecutor
import speech_recognition as sr
from gtts import gTTS
import pygame
import concurrent.futures
from datetime import datetime
from nltk.tokenize import word_tokenize
import re

isResponding = None
recognizer = sr.Recognizer()
name = "Евдокия"
number_pattern = r'\d+'

# Create a ThreadPoolExecutor with a maximum of 5 threads
executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)


def processSpeech():
    with sr.Microphone() as source:
        print("Listening.")
        audio = recognizer.listen(source)
    try:
        user_input = recognizer.recognize_google(audio, language="ru", key="AIzaSyDy6lMIltumbjiVbpqyzcmC0qsfz7TX_q0")
        print(f"{user_input}")
        postProcessLogic(user_input)
        # Now you can process `user_input` as text.
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")


def timer(waitTime):
    time_string = str(waitTime)
    speakText('Поставила таймер на ' + time_string + ' секунд')
    time.sleep(waitTime)
    speakText('Ваш таймер на ' + time_string + ' секунд закончился')


def postProcessLogic(user_input):
    messageTokens = word_tokenize(user_input)
    # if isResponding:

    for token in messageTokens:
        if token == "таймер" or token == "Таймер":
            numbers_found = re.findall(number_pattern, user_input)
            if numbers_found:
                parsed_number = int(numbers_found[0])
                executor.submit(timer, parsed_number)

    isResponding = False
    if name in user_input:
        response_text = "Да-да?"
        speakText(response_text)
        isResponding = True


def speakText(text):
    tts = gTTS(text=text, lang='ru')
    audio_path = "temp.mp3"
    tts.save(audio_path)
    pygame.init()
    pygame.mixer.init()
    sound = pygame.mixer.Sound(audio_path)
    sound.play()
    pygame.time.wait(int(sound.get_length() * 1000))
    pygame.quit()


def main():
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    # speakText("Доброе утро. Сегодня " + str(dt_string))
    day_today = dt_string.split(" ")[0]

    with open('calendar.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        # Regular expression pattern for dates and text
        pattern = r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2})(.*)'

        # Iterate through the lines
        has_already_spoken = False
        for line in lines:
            match = re.match(pattern, line)
            if match:
                date = match.group(1)

                converted_date = match.string.split(" ")
                day = converted_date[0]
                hour = converted_date[1]
                text_after_date_time = match.group(2).strip()

                print(f"Date: {day}, Time of day: {hour} Text after date: {text_after_date_time}")

                if day_today == day:
                    if not has_already_spoken:
                        speakText("На сегодня у вас запланировано " + text_after_date_time + " в " + str(hour))
                        has_already_spoken = True
                    elif has_already_spoken:
                        speakText(
                            "Кроме этого, у вас сегодня запланировано " + text_after_date_time + " в " + str(hour))
            else:
                print(f"No date found in line: {line}")

    while True:
        processSpeech()
        if not isResponding:
            time.sleep(2.0)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
