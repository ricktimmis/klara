package main

import (
	"flag"
	"fmt"
	htgotts "github.com/hegedustibor/htgo-tts"
	"github.com/hegedustibor/htgo-tts/handlers"
	"github.com/hegedustibor/htgo-tts/voices"
	"github.com/therecipe/qt/widgets"
	"os"
)

/*var TextToSpeak = "GPT4All is an ecosystem to train and deploy powerful and customized" +
" large language models that run locally on consumer grade CPUs." /* +
"The goal is simple - be the best instruction tuned assistant-style language model that" +
" any person or enterprise can freely use, distribute and build on. " +
"A GPT4All model is a 3GB - 8GB file that you can download and plug into the GPT4All" +
" open-source ecosystem software. Nomic AI supports and maintains this software " +
"ecosystem to enforce quality and security alongside spearheading the effort to " +
"allow any person or enterprise to easily train and deploy their own on-edge large language models."*/
/*
var (
	centralLayout       *widgets.QGridLayout
	centralLayoutRow    int
	centralLayoutColumn int
)*/

//	func main() {
//		widgets.NewQApplication(len(os.Args), os.Args)
//		w := widgets.NewQWidget(nil, 0)
//		wL := widgets.NewQVBoxLayout2(w)
//		iw := widgets.NewQTextEdit(w)
//		btn := widgets.NewQPushButton2("Speak", w)
//		wL.AddWidget(iw, 0, 0)
//		wL.AddWidget(btn, 0, 0)
//		btn.ConnectClick(func() {
//			go speak("Welcome")
//		})
//		w.Show()
//		widgets.QApplication_Exec()
//	}
func main() {

	// Command-line flag to accept a string
	textFlag := flag.String("text", "", "Text to speak")
	flag.Parse()

	if *textFlag != "" {
		// If the "text" flag is provided, speak the given text and exit
		Speak(*textFlag)
		return
	}
	// needs to be called once before you can start using the QWidgets
	app := widgets.NewQApplication(len(os.Args), os.Args)

	// create a window
	// with a minimum size of 250*200
	// and sets the title to "Hello Widgets Example"
	window := widgets.NewQMainWindow(nil, 0)
	window.SetMinimumSize2(250, 200)
	window.SetWindowTitle("Hello Widgets Example")

	// create a regular widget
	// give it a QVBoxLayout
	// and make it the central widget of the window
	widget := widgets.NewQWidget(nil, 0)
	widget.SetLayout(widgets.NewQVBoxLayout())
	window.SetCentralWidget(widget)

	// create a line edit
	// with a custom placeholder text
	// and add it to the central widgets layout
	input := widgets.NewQLineEdit(nil)
	input.SetPlaceholderText("Write something ...")
	widget.Layout().AddWidget(input)

	// create a button
	// connect the clicked signal
	// and add it to the central widgets layout
	button := widgets.NewQPushButton2("and click me!", nil)
	button.ConnectClicked(func(bool) {
		//widgets.QMessageBox_Information(nil, "OK", input.Text(), widgets.QMessageBox__Ok, widgets.QMessageBox__Ok)
		Answer, err := AskGPT(input.Text())
		if err != nil {
			fmt.Printf(err.Error())
		}
		Speak(Answer)
	})
	widget.Layout().AddWidget(button)

	// make the window visible
	window.Show()

	// start the main Qt event loop
	// and block until app.Exit() is called
	// or the window is closed by the user
	Speak("Good evening! Olivia Seven here, how can I help you ?")
	app.Exec()
}

func onButtonClick() {
	fmt.Println("Button clicked - onButtonClick()")
	Speak("Wrapper Function")
}

func Speak(say string) {
	fmt.Printf("Speaking,  %s\n", say)
	speech := htgotts.Speech{Folder: "audio", Language: voices.EnglishUK, Handler: &handlers.Native{}}
	if err := speech.Speak(say); err != nil {
		fmt.Printf("ERROR: %s\n", err)
	}
}

func AskGPT(q string) (string, error) {
	answer, _ := GPT4all()
	return answer, nil
}

func GPT4all() (string, error) {
	//// Load the model
	//model, err := gpt4all.New("~/.local/share/nomic.ai/GPT4All/ggml-gpt4all-j-v1.3-groovy.bin")
	//if err != nil {
	//	panic(err)
	//}
	//defer model.Free()
	//
	//model.SetTokenCallback(func(s string) bool {
	//	fmt.Print(s)
	//	return true
	//})
	//
	//answer, err := model.Predict("Here are 4 steps to create a website:", gpt4all.SetTemperature(0.1))
	//if err != nil {
	//	panic(err)
	//}
	return "Not Implemented", nil
}
