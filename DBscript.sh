#!/bin/bash
rm -rf chia.db
rm -rf migrations/
pipenv run flask db init 
pipenv run flask db migrate
pipenv run flask db upgrade
