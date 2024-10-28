export-requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

run:
	poetry run uvicorn src.main:app --port=5000 --reload

requirements-dev:
	poetry install --no-root
