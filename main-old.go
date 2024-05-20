package kompanion

import (
	"fmt"
)

func main() {
	// Initialize the SpeechRecognizer with your desired language and other options
	recognizer := speech.NewSpeechRecognizer("en-US")

	// Start listening for audio input (microphone or audio file)
	err := recognizer.StartListening()
	if err != nil {
		panic(err)
	}

	// Wait for speech to be recognized and text to be transcribed
	result, err := recognizer.Recognize()
	if err != nil {
		panic(err)
	}

	fmt.Println("Transcribed text:", *result)
}
