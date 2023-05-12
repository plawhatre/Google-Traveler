SHELL := /bin/bash

venv:
	python3 -m venv traveler
	source ./traveler/bin/activate
	pip install -r requirements.txt

run:
	streamlit run ./app.py