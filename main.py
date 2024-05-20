# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget
# import all the modules that we will need to use
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer
from gpt4all import GPT4All

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gpt_model = GPT4All("ggml-gpt4all-j-v1.3-groovy.bin")
        self.setWindowTitle("Olivia Seven")

        self.label = QLabel()

        self.input = QLineEdit()
        self.input.textChanged.connect(self.label.setText)
        self.button = QPushButton("Speak")
        self.button.clicked.connect(self.speak)

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)

    def run_gpt(self, question):
        """Run GPT4All model with input_data as input"""

        messages = [{"role": "user", "content": question}]
        response = self.gpt_model.chat_completion(
            messages,
            default_prompt_footer=False,
            default_prompt_header=False,
            verbose=False,
        )
        try:
            answer = response["choices"][0]["message"]["content"]
        except:
            answer = "ERROR: Wrong Response"
        return answer
    def speak(self):
        path = "./venv/lib/python3.11/site-packages/TTS/.models.json"

        model_manager = ModelManager(path)

        model_path, config_path, model_item = model_manager.download_model("tts_models/en/ljspeech/tacotron2-DDC")

        voc_path, voc_config_path, _ = model_manager.download_model(model_item["default_vocoder"])

        syn = Synthesizer(
            tts_checkpoint=model_path,
            tts_config_path=config_path,
            vocoder_checkpoint=voc_path,
            vocoder_config=voc_config_path
        )
        question = self.input.text()
        answer = self.run_gpt(self, question)
        print(answer)
        outputs = syn.tts(answer)
        syn.save_wav(outputs, "audio-1.wav")
        os.system("paplay ./audio-1.wav")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
