from os import system
import speech_recognition as sr
from gpt4all import GPT4All
import sys
import whisper
import warnings
import time
import os
import subprocess
import logging
from datetime import datetime

wake_word = 'clara'

model_complete_filepath='/home/ricktimmis/.local/share/nomic.ai/GPT4All/gpt4all-falcon-newbpe-q4_0.gguf'
model_path_directory, model_filename_complete = os.path.split(model_complete_filepath)
model_filename, model_extension = os.path.splitext(model_filename_complete)

device_for_running_LLM=input("Which device would you like to use for running the LLM?\nPlease type your selection without the quotes and press ENTER.\nSelections available: \"gpu\", \"cpu\", \"intel\", and \"amd\"\n\nYou've selected: ")

model = GPT4All(model_filename, model_path=model_path_directory, allow_download=False, device=device_for_running_LLM)
r = sr.Recognizer()
# tiny_model_path = os.path.expanduser('~/.cache/whisper/tiny.en')
# base_model_path = os.path.expanduser('~/.cache/whisper/base.en')
tiny_model = whisper.load_model('tiny.en')
base_model = whisper.load_model('base.en')
listening_for_wake_word = True
source = sr.Microphone()
warnings.filterwarnings("ignore", category=UserWarning, module='whisper.transcribe', lineno=114)

if sys.platform != 'darwin':
    import pyttsx3
    engine = pyttsx3.init()

# def speak(text):
#     if sys.platform == 'darwin':
#         ALLOWED_CHARS = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,?!-_$:+-/ ')
#         clean_text = ''.join(c for c in text if c in ALLOWED_CHARS)
#         system(f"say '{clean_text}'")
#     else:
#         engine.say(text)
#         engine.runAndWait()

def log(message, log_file='kompanion.log'):
    # Configuring the logging module
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )
    logging.info(message)

def speak(text):
    process = subprocess.Popen(['./bin/linux-talker.sh', text], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    if process.returncode != 0:
        print("Error occurred: ", error.decode("utf-8"))
    else:
        print("Output: ", output.decode("utf-8"))

def listen_for_wake_word(audio):
    global listening_for_wake_word
    with open('wake_detect.wav', 'wb') as f:
        f.write(audio.get_wav_data())
    result = tiny_model.transcribe('wake_detect.wav')
    text_input = result['text']
    print('Heard..' ,result['text'])
    if wake_word in text_input.lower().strip():
        print('Wake word detected. Please speak your prompt to GPT4All.')
        # listening_for_wake_word = False
        # speak('Listening')
        listening_for_wake_word = False

def prompt_gpt(audio):
    global listening_for_wake_word
    try:
        with open('prompt.wav', 'wb') as f:
            f.write(audio.get_wav_data())
        result = base_model.transcribe('prompt.wav')
        print(result['text'])
        prompt_text = result['text']
        if len(prompt_text.strip()) == 0:
            print('Empty prompt. Please speak again.')
            speak('Empty prompt. Please speak again.')
            listening_for_wake_word = True
        else:
            print('User: ' + prompt_text)
            log('User: ' + prompt_text)
            output = model.generate(prompt_text, max_tokens=200)
            print('GPT4All: ', output)
            log('GPT4All: ', output)
            speak(output)
            print('\nSay', wake_word, 'to wake me up. \n')
            listening_for_wake_word = True
    except Exception as e:
        print('Prompt error: ', e)

def callback(recognizer, audio):
    global listening_for_wake_word
    if listening_for_wake_word:
        print('Listening...')
        listen_for_wake_word(audio)
    else:
        prompt_gpt(audio)

def start_listening():
    with source as s:
        r.adjust_for_ambient_noise(s, duration=2)
    print('\nSay', wake_word, 'to wake me up. \n')
    r.listen_in_background(source, callback)
    while True:
        time.sleep(1)

if __name__ == '__main__':
    start_listening()
