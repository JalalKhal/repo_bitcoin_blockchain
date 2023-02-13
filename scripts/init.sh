#!/bin/bash
#run in sudo mode, the script must be executed in the scripts folder
poetry_install=$(curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -)

if [ $? -eq 0 ]
        then
          echo "Successfully installed poetry"
          echo "Load python packages for the app"
          cd ../
          /etc/poetry/bin/poetry install
fi