#!/bin/bash

PROJECT=jalopy
export PROJECT_PATH=/opt/$PROJECT
export VENV=/opt/venvs/$PROJECT
export CONF=$HOME/.config/$PROJECT
export PYTHONPATH=$PROJECT_PATH
source $VENV/bin/activate
python $PROJECT_PATH/bin/run_jalopy.py --options $CONF/config.ini "$@"
