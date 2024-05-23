#!/bin/bash


# Function to check and install required tools & dependencies
check_and_install_tool() {
    local tool_name="$1"
    local package_name="$2" # Package name might differ from tool name

    if ! command -v "$tool_name" &> /dev/null; then
        echo "$tool_name could not be found, attempting to install."
        pkexec apt-get install -y "$package_name"
    fi
}

# Enable the user to choose their LLM Model
function choose_model() {
    # See: https://gpt4all.io/index.html for models and path info etc...
    choice=$(kdialog --menu "Select LLM Model" 1 "GPT4ALL Falcon" 2 "Mistral Instruct" 3 "Mistral OpenOrca")
    case $choice in
          1) MODEL="Falcon"
             URL="https://gpt4all.io/models/gguf/gpt4all-falcon-newbpe-q4_0.gguf"
             SAVEAS="gpt4all-falcon-newbpe-q4_0.gguf";;
          2) MODEL="Mistral Instruct"
             URL="https://gpt4all.io/models/gguf/mistral-7b-instruct-v0.1.Q4_0.gguf"
             SAVEAS="mistral-7b-instruct-v0.1.Q4_0.gguf";;
          3) MODEL="Mistral OpenOrca"
             URL="https://gpt4all.io/models/gguf/mistral-7b-openorca.gguf2.Q4_0.gguf"
             SAVEAS="mistral-7b-openorca.gguf2.Q4_0.gguf"
    esac

wget $URL --output-document=./model/$SAVEAS
}

# MAIN
# ----
# Check first run
if [ -f "config.local" ]; then
  echo "installer.sh has already been run. Remove ./config.local to reinstall"
  exit 0
fi

# Prompt the user with information about downloading dependencies and model
if kdialog --yesno "This installation script will install dependencies, and download your choice of LLM Model. \
                    Models are about 4Gb please be patient whilst download completes. \n Proceed ? "; then
    # Debian/Ubuntu Dependency installer
    pkexec apt-get install -y "python3.10-venv libasound2-dev portaudio19-dev golang-1.18"

    # Ensure required tools are installed
    check_and_install_tool kdialog kdialog
    check_and_install_tool wget wget
    choose_model
else
    exit
fi

# Write configuration
echo "Local configuration file for KLARA" > config.local
echo "MODEL=./models/$SAVEAS" >> config.local

# Offer to launch klara
if kdialog --yesno "Launch Klara ?"; then
  make all
else
  exit 0
fi