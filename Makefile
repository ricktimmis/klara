# The dependency list for the venv creation
REQUIREMENTS = requirements.txt

# The venv folder. Change to desired virtual environment name
VENV_NAME = .venv

# Default python version can be overridden: make PYTHON=python3.6 ...
PYTHON = python3.10

all: build install run # package

clean:
	@echo "Cleaning up..."
	# rm ./bin/GoSpeak
	# rm -rf .venv/

build:
	@echo "Building GoSpeak..."
	@go build -o ./bin/GoSpeak main.go

# This is your target rule which uses the venv and REQUIREMENTS as dependencies
install: venv
	@echo "Installing..."
	. $(VENV_NAME)/bin/activate; pip install -r $(REQUIREMENTS)

# This will generate a new venv directory if it does not exist.
# By declaring it as a dependency for the ******** install-requirements ******** rule,
# It will execute first when `make install-requirements` is run.
venv:
	test -d $(VENV_NAME) || $(PYTHON) -m venv $(VENV_NAME)

# You can also add a rule to run your source code
run: venv
	. $(VENV_NAME)/bin/activate; python kompanion.py

package:
	@echo "Packaging..."
	# Add commands to package the project


# Register recipes
.PHONY: all clean build install package install venv run