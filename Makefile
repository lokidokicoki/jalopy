PROJECT=jalopy
SOURCE=$(shell pwd)
TARGET=/opt/$(PROJECT)
VENV=/opt/venvs/$(PROJECT)
CONFIG=$$HOME/.config/$(PROJECT)
CACHE=$$HOME/.cache/$(PROJECT)

all: reqs setup install

test:
	echo $$HOME
	echo "config: $(CONFIG)"
	echo "cache: $(CACHE)"
	echo "target: $(TARGET)"
	echo "venv: $(VENV)"

reqs:
	poetry export -f requirements.txt -o requirements.txt --without-hashes

setup:
	echo "Setup install target"
	sudo mkdir -p $(TARGET)
	sudo mkdir -p $(VENV)
	sudo chown $(USER) $(TARGET)
	sudo chown $(USER) $(VENV)
	mkdir -p $(CONFIG)
	mkdir -p $(CACHE)
	python -m venv $(VENV)

install: reqs
	echo "Install project"
	echo $(SOURCE) $(TARGET)
	rsync -amv --exclude='__pycache__' --exclude='venv' --exclude='.git' --exclude='.mypy_cache' --exclude='.vscode' . $(TARGET)

	cp $(TARGET)/config.ini $(CONFIG)/config.ini
	$(VENV)/bin/python -m pip install -r $(TARGET)/requirements.txt
	

uninstall:
	sudo rm -rf $(TARGET)
	sudo rm -rf $(VENV)
	sudo rm -rf $(CONFIG)
	sudo rm -rf $(CACHE)
