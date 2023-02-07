#!/bin/bash

export PROJECT_PATH=/home/loki/code/jalo.py
source $PROJECT_PATH/venv/bin/activate
export PYTHONPATH=$PROJECT_PATH
python $PROJECT_PATH/bin/jalo.py "$@"
