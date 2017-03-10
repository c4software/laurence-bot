#!/bin/bash

# Couverture
# pip install coverage coverage-badge

coverage run --source=. -m unittest discover
coverage report -m
coverage-badge -o test/coverage.svg
