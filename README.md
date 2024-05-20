# kompanion

Kompanion is a desktop AI companion, designed to support you in research, learning and general work. Kompanion is 
designed to provide a voice powered _human-esque_ desktop assistant.

# Dependencies

### Linux
ALSA is required. See: 
https://github.com/ebitengine/oto

On Ubuntu or Debian, run this command:

```apt install libasound2-dev portaudio19-dev ```

# Shoulders
_We stand upon the shoulders of Giants_

# GPT4ALL-Voice-Assistant
https://github.com/Ai-Austin/GPT4ALL-Voice-Assistant

This is a 100% offline GPT4ALL Voice Assistant. Completely open source and privacy-friendly. Use any language model on GPT4ALL. Background process voice detection. Watch the full YouTube tutorial for the setup guide: https://youtu.be/6zAk0KHmiGw
## Setup
I highly advise watching the YouTube tutorial to use this code. You will need to modify the OpenAI whisper library to work offline and I walk through that in the video as well as setting up all the other dependencies to function properly.

If you're planning on installing it on Arch-based distros, you need to install `espeak` and `python-espeak` packages from the AUR. You can install them using `yay` utility by running:
```bash
yay -S espeak python-espeak
```
## Improvements to think about adding to yours
Give a system prompt. These open-source models perform far better when you send a system prompt as specified in the GPT4ALL documentation: https://docs.gpt4all.io/gpt4all_python.html#introspection

