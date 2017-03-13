#!/bin/bash

# Couverture
# pip install coverage coverage-badge

coverage run --source="commands,tools" -m unittest discover
coverage report -m > test/coverage/coverage.txt
coverage-badge -f -o test/coverage/coverage.svg
