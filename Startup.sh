#!/bin/bash

set -e
pipenv install
pipenv run flask db upgrade
FLASK_ENV=development pipenv run flask run
