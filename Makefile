PROJECT=jalo.py
SOURCE=$(shell pwd)
TARGET=/opt/$(PROJECT)
VENV=/opt/venv-$(PROJECT)
CONFIG=/etc/opt/$(PROJECT)

all: reqs setup install

reqs:
	poetry export -f requirements.txt -o requirements.txt --without-hashes

setup:
	echo "Setup install target"
	sudo mkdir -p $(TARGET)
	sudo mkdir -p $(CONFIG)
	sudo mkdir -p $(VENV)
	sudo chown $(USER) $(TARGET)
	sudo chown $(USER) $(CONFIG)
	sudo chown $(USER) $(VENV)
	python -m venv $(VENV)

install: reqs
	echo "Install project"
	echo $(SOURCE) $(TARGET)
	rsync -amv --exclude='__pycache__' --exclude='venv' --exclude='.git' --exclude='.mypy_cache' --exclude='.vscode' . $(TARGET)

	cp $(TARGET)/config.ini $(CONFIG)/config.ini
	$(VENV)/bin/python -m pip install -r $(TARGET)/requirements.txt

clean:
	sudo rm -rf $(TARGET)
	sudo rm -rf $(VENV)
