install:
	poetry install

serve-notebook:
	poetry run jupyter lab --notebook-dir=..


check: flakes fmt

flakes:
	poetry run pyflakes .

fmt:
	poetry run black .
