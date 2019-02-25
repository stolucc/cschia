#!/bin/bash

set -e
pipenv install
FLASK_ENV=development 
pipenv run flask run
