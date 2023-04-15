#!/bin/bash

PROJECT=jalo.py
export PROJECT_PATH=/opt/$PROJECT
export VENV=/opt/venv-$PROJECT
export CONF=/etc/opt/$PROJECT
export PYTHONPATH=$PROJECT_PATH
source $VENV/bin/activate
python $PROJECT_PATH/bin/jalo.py --options $CONF/config.ini "$@"
