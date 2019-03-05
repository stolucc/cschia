#!/bin/bash

rm chia.db
echo
echo
echo
rm -rf migrations/
echo
echo
echo

pipenv run flask db init
echo
echo
echo
pipenv run flask db migrate
echo
echo
echo
pipenv run flask db upgrade