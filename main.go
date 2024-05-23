package main

import (
	"fmt"
	htgotts "github.com/hegedustibor/htgo-tts"
	"github.com/hegedustibor/htgo-tts/handlers"
	"github.com/hegedustibor/htgo-tts/voices"
	"os"
)

func speak(say string) {
	fmt.Printf("Speaking,  %s\n", say)
	speech := htgotts.Speech{Folder: "audio", Language: voices.EnglishUK, Handler: &handlers.Native{}}
	if err := speech.Speak(say); err != nil {
		fmt.Printf("ERROR: %s\n", err)
	}
}

func main() {
   	if len(os.Args) > 1 {
   		speak(os.Args[1])
   	} else {
   		fmt.Println("No arguments provided.")
   	}
}



