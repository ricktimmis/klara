from os import system
import speech_recognition as sr
from gpt4all import GPT4All
import sys
import whisper
import warnings
import time
import os
import nltk
import subprocess
import logging
from datetime import datetime

# Enable Debug Mode
DEBUG=True

# The name of your K.L.A.R.A Digital Assistant
wake_word = 'clara'

model_complete_filepath = '/home/ricktimmis/.local/share/nomic.ai/GPT4All/gpt4all-falcon-newbpe-q4_0.gguf'
model_path_directory, model_filename_complete = os.path.split(model_complete_filepath)
model_filename, model_extension = os.path.splitext(model_filename_complete)

# FIXME This needs to test for the presence of the 'punkt' model and download ONLY if missing
#nltk.download('punkt')

device_for_running_LLM = input(
    "Which device would you like to use for running the LLM?\nPlease type your selection without the quotes and press ENTER.\nSelections available: \"gpu\", \"cpu\", \"intel\", and \"amd\"\n\nYou've selected: ")

model = GPT4All(model_filename, model_path=model_path_directory, allow_download=False, device=device_for_running_LLM)
r = sr.Recognizer()
# tiny_model_path = os.path.expanduser('~/.cache/whisper/tiny.en')
# base_model_path = os.path.expanduser('~/.cache/whisper/base.en')
tiny_model = whisper.load_model('tiny.en')
base_model = whisper.load_model('base.en')
listening_for_wake_word = True
source = sr.Microphone()
warnings.filterwarnings("ignore", category=UserWarning, module='whisper.transcribe', lineno=114)


def log(message, log_file='klara.log'):
    # Configuring the logging module
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )
    logging.info(message)


# split_and_speak tokenises string into sentences to be spoken
def split_and_speak(text):
    # Splitting the text into sentences
    sentences = nltk.sent_tokenize(text)

    # Loop over each sentence
    for sentence in sentences:
        # Calling the 'speak' function
        speak(sentence)


def speak(sentence):
    if DEBUG:
        print(sentence)
    process = subprocess.Popen(['./bin/linux-talker.sh', sentence], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if DEBUG:
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
    if DEBUG:
        print('Heard..', result['text'])
    if wake_word in text_input.lower().strip():
        #if DEBUG:
        print('Wake word detected. Please speak your prompt to GPT4All.')
        #else:
        #    split_and_speak('Listening')
        listening_for_wake_word = False


def prompt_gpt(audio):
    global listening_for_wake_word
    try:
        with open('prompt.wav', 'wb') as f:
            f.write(audio.get_wav_data())
        result = base_model.transcribe('prompt.wav')
        if DEBUG:
            print(result['text'])
        prompt_text = result['text']
        if len(prompt_text.strip()) == 0:
            if DEBUG:
                print('Sorry. I missed that, Please speak again.')
            else:
                split_and_speak('Sorry. I missed that, Please speak again.')
            f.truncate(0) # Clear Klaras speech from the prompt audio buffer
            listening_for_wake_word = False
        else:
            print('User: ' + prompt_text)
            log('User: ' + prompt_text)
            output = model.generate(prompt_text, max_tokens=200)
            print('KLARA: ', output)
            log('KLARA: ' + output)
            split_and_speak(output)
            print('\nSay', wake_word, 'to wake me up. \n')
            listening_for_wake_word = True
    except Exception as e:
        if DEBUG:
            print('Prompt error: ', e)
        else:
            split_and_speak('Sorry, neural network, had a bit of a brain fart.')


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
    split_and_speak("Hi there, ready when you are")
    r.listen_in_background(source, callback)
    while True:
        time.sleep(1)


if __name__ == '__main__':
    start_listening()
