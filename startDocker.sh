#!/bin/bash

# override .env file
export FLASK_APP=flip

# run server
python -m flask run --no-reload --host=0.0.0.0