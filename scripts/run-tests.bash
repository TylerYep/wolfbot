#!/usr/bin/env bash

# If any command inside script returns error, exit and return that error
set -e

# Ensure that we're always inside the root of our application,
# no matter which directory we run script: Run `./scripts/run-tests.bash`
cd "${0%/*}/.."

# Type Checking
mypy .

# Auto-code formatters
isort -y
black . -l 100
git add .

# Style Checking
flake8 .
pycodestyle .
find . -iname "*.py" | xargs pylint

# Testing
pytest --cov=src --cov-report=html unit_test
