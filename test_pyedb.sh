#!/bin/bash

# Set up the python virtual environment
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    python -m venv .venv && source .venv/bin/activate
else
    python -m venv .venv
    .venv/Scripts/activate.bat
fi

# Set up the .env.test file so we know where to find the install
echo "RPC_SERVER_ROOT="$RPC_SERVER_ROOT > .env.test

# Run tox
python -m pip install --upgrade pip flit tox tox-gh-actions
tox -e test -- --junitxml=junit/test-results.xml