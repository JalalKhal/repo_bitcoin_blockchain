#!/bin/bash
#run in sudo mode,the script must be executed in the scripts folder

./init.sh

if [ $? -eq 0 ]
        then
          sudo /etc/poetry/bin/poetry run python ../app.py
fi