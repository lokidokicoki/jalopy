#!/bin/bash

source /home/loki/jalo.py/venv/bin/activate
export PYTHONPATH=/home/loki/jalo.py
python /home/loki/jalo.py/bin/jalo.py "$@"
